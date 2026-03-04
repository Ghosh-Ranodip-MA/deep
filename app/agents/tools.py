import json
import logging
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.config import settings
from app.rag.prompts import (
    PLANNER_PROMPT,
    NOVELTY_SCORER_PROMPT,
    SUMMARIZE_PAPER_PROMPT,
    COMBINED_SUMMARY_PROMPT,
    RESEARCH_GAPS_PROMPT,
    MERMAID_WORKFLOW_PROMPT,
)
import aiohttp
import base64
import os
import uuid

logger = logging.getLogger(__name__)


def get_gemini_llm():
    """Primary LLM: Google Gemini (generous free tier)."""
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0,
    )


def get_groq_llm():
    """Fallback LLM: Groq with fast 8b model."""
    return ChatGroq(
        temperature=0,
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.LLM_MODEL,
    )


async def invoke_with_fallback(chain_builder, inputs: dict) -> str:
    """Try Gemini first, fall back to Groq if Gemini fails."""
    # Try Gemini
    if settings.GEMINI_API_KEY:
        try:
            llm = get_gemini_llm()
            chain = chain_builder(llm)
            response = await chain.ainvoke(inputs)
            return response.content
        except Exception as e:
            logger.warning(f"Gemini failed, falling back to Groq: {e}")

    # Fallback to Groq
    llm = get_groq_llm()
    chain = chain_builder(llm)
    response = await chain.ainvoke(inputs)
    return response.content


class ToolAgents:
    @staticmethod
    async def get_query_plan(query: str) -> dict:
        prompt = PromptTemplate(input_variables=["query"], template=PLANNER_PROMPT)
        try:
            content = await invoke_with_fallback(lambda llm: prompt | llm, {"query": query})
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception:
            return {"query": query, "search_keywords": [query], "intent": "General research"}

    @staticmethod
    async def evaluate_novelty(abstract: str) -> float:
        if not abstract:
            return 0.0
        prompt = PromptTemplate(input_variables=["abstract"], template=NOVELTY_SCORER_PROMPT)
        try:
            content = await invoke_with_fallback(lambda llm: prompt | llm, {"abstract": abstract})
            return float(content.strip())
        except Exception:
            return 0.5

    @staticmethod
    async def summarize_paper(text: str) -> str:
        if not text:
            return ""
        prompt = PromptTemplate(input_variables=["text"], template=SUMMARIZE_PAPER_PROMPT)
        return await invoke_with_fallback(lambda llm: prompt | llm, {"text": text})

    @staticmethod
    async def generate_combined_summary(texts: list[str]) -> str:
        if not texts:
            return ""
        combined_text = "\n\n---\n\n".join(texts)
        prompt = PromptTemplate(input_variables=["text"], template=COMBINED_SUMMARY_PROMPT)
        return await invoke_with_fallback(lambda llm: prompt | llm, {"text": combined_text})

    @staticmethod
    async def extract_research_gaps(text: str) -> str:
        if not text:
            return ""
        prompt = PromptTemplate(input_variables=["text"], template=RESEARCH_GAPS_PROMPT)
        return await invoke_with_fallback(lambda llm: prompt | llm, {"text": text})

    @staticmethod
    async def generate_workflow_mermaid(text: str) -> str:
        if not text:
            return ""
        prompt = PromptTemplate(input_variables=["text"], template=MERMAID_WORKFLOW_PROMPT)
        try:
            content = await invoke_with_fallback(lambda llm: prompt | llm, {"text": text})
            content = content.replace("```mermaid", "").replace("```", "").strip()
            if not content.startswith("graph ") and "->" in content:
                content = "graph TD;\n" + content
            elif not content.startswith("graph "):
                content = "graph TD;\n" + content
            return content
        except Exception:
            return ""

    @staticmethod
    async def download_mermaid_image(mermaid_syntax: str, output_dir: str) -> str | None:
        if not mermaid_syntax:
            return None
            
        try:
            graph_json = json.dumps({"code": mermaid_syntax, "mermaid": {"theme": "default"}})
            graph_b64 = base64.urlsafe_b64encode(graph_json.encode('utf-8')).decode('ascii')
            
            url = f"https://mermaid.ink/img/{graph_b64}"
            
            os.makedirs(output_dir, exist_ok=True)
            filename = f"workflow_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(output_dir, filename)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open(filepath, 'wb') as f:
                            f.write(await resp.read())
                        return filepath
                    else:
                        print(f"Failed to fetch mermaid image. Status: {resp.status}")
                        return None
        except Exception as e:
            print(f"Error downloading mermaid image: {e}")
            return None