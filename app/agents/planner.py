from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Breaks query into structured execution plan."""

    def __init__(self):
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=0,
            groq_api_key=settings.GROQ_API_KEY,
        )

    async def plan(self, query: str, max_papers: int = 20) -> Dict[str, Any]:
        system_prompt = """You are a research planning assistant. Given a user's research topic,
        create a structured execution plan for retrieving relevant papers.
        Return a JSON object with:
        - search_query: optimized search string
        - year_range: optional {"from": YYYY, "to": YYYY} or null
        - fields_of_study: list of relevant fields
        - max_papers: integer (default 20)
        - additional_keywords: list of important terms
        Ensure the JSON is valid."""

        human = f"Topic: {query}\nMax papers: {max_papers}"

        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human),
            ])
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            plan = json.loads(content)
            plan["max_papers"] = plan.get("max_papers", max_papers)
            return plan
        except Exception as e:
            logger.error(f"Planner failed: {e}. Using fallback plan.")
            return {
                "search_query": query,
                "year_range": None,
                "fields_of_study": [],
                "max_papers": max_papers,
                "additional_keywords": [],
            }