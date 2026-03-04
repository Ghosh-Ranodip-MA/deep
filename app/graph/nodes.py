import os
import json
import asyncio
import logging
from app.models.state import WorkflowState, ScoredPaper, PaperSummary
from app.services.paper_retriever import retrieve_papers
from app.utils.embeddings import compute_similarity
from app.agents.tools import ToolAgents
from app.pdf.generator import PDFGenerator
from app.config import settings

logger = logging.getLogger(__name__)
pdf_generator = PDFGenerator()

GraphState = WorkflowState


async def planner_node(state: WorkflowState) -> WorkflowState:
    query = state["query"]
    plan = await ToolAgents.get_query_plan(query)
    state["plan"] = plan
    return state


async def retrieve_node(state: WorkflowState) -> WorkflowState:
    """Retrieve papers from Semantic Scholar API."""
    plan = state.get("plan") or {}
    kw = plan.get("search_keywords", [state["query"]]) if isinstance(plan, dict) else [state["query"]]
    
    # Try with LLM planned keywords first
    query_str = " ".join(kw)
    papers = await retrieve_papers(query_str, top_k=5)
    
    # Fallback to raw query if the LLM plan was too restrictive or poor
    if not papers and query_str != state["query"]:
        logger.info(f"Fallback to raw query search for: {state['query']}")
        papers = await retrieve_papers(state["query"], top_k=5)
        
    state["papers"] = papers

    if not papers:
        logger.info(f"No papers found for query: {state['query'][:80]}")
        state["status"] = "no_papers_found"
    else:
        logger.info(f"Retrieved {len(papers)} papers from OpenAlex")
    return state


async def score_node(state: WorkflowState) -> WorkflowState:
    papers = state.get("papers", [])
    if not papers:
        state["scores"] = []
        return state

    query = state["query"]
    scored = []

    max_cit = max([p.citationCount or 0 for p in papers] + [1])
    current_year = 2026

    # Parallelize novelty scoring for speed
    novelty_tasks = [ToolAgents.evaluate_novelty(p.abstract) for p in papers]
    try:
        novelty_scores = await asyncio.gather(*novelty_tasks, return_exceptions=True)
    except Exception:
        novelty_scores = [0.5] * len(papers)

    for i, p in enumerate(papers):
        sim = compute_similarity(query, p.abstract or p.title)
        cit = (p.citationCount or 0) / max_cit
        recency = max(0, 1.0 - (current_year - (p.year or current_year)) * 0.1)
        nov = novelty_scores[i] if not isinstance(novelty_scores[i], Exception) else 0.5

        final = (
            settings.WEIGHT_SIMILARITY * sim
            + settings.WEIGHT_CITATION * cit
            + settings.WEIGHT_RECENCY * recency
            + settings.WEIGHT_NOVELTY * nov
        )

        scored_p = ScoredPaper(
            **p.model_dump(),
            similarity=round(sim, 4),
            citation_score=round(cit, 4),
            recency_score=round(recency, 4),
            novelty_score=round(nov, 4),
            final_score=round(final, 4),
        )
        scored.append(scored_p)

    state["scores"] = scored
    return state


async def select_top_node(state: WorkflowState) -> WorkflowState:
    scores = state.get("scores", [])
    if not scores:
        state["best_paper"] = None
        return state
    scores.sort(key=lambda x: x.final_score, reverse=True)
    state["best_paper"] = scores[0]
    state["scores"] = scores
    return state


async def summarize_best_node(state: WorkflowState) -> WorkflowState:
    best = state.get("best_paper")
    if best:
        text = f"Title: {best.title}\n"
        if best.abstract:
            text += f"Abstract: {best.abstract}\n"
        if best.methodology:
            text += f"Methodology: {best.methodology}\n"
        try:
            summary = await ToolAgents.summarize_paper(text)
            state["best_paper_summary"] = summary
        except Exception as e:
            logger.warning(f"Best paper summarization failed (LLM error): {e}")
            state["best_paper_summary"] = "Summary unavailable (LLM rate limit reached). Please try again later."
        
        try:
            if best.methodology:
                mermaid_code = await ToolAgents.generate_workflow_mermaid(best.methodology)
                if mermaid_code:
                    img_path = await ToolAgents.download_mermaid_image(mermaid_code, settings.JSON_OUTPUT_DIR)
                    state["best_paper_mermaid_img"] = img_path
        except Exception as e:
            logger.warning(f"Mermaid generation failed: {e}")
    else:
        state["best_paper_summary"] = ""
        state["best_paper_mermaid_img"] = None
    return state


async def summarize_combined_node(state: WorkflowState) -> WorkflowState:
    scores = state.get("scores", [])
    papers = scores if scores else (state.get("papers") or [])
    paper_list = papers[:10]

    if not paper_list:
        state["all_paper_summaries"] = []
        state["combined_summary"] = ""
        return state

    all_summaries = []
    abstracts = []
    for p in paper_list:
        authors_str = ", ".join(a.name for a in (p.authors or []))
        abstract_text = p.abstract or "No abstract available"
        abstracts.append(f"Title: {p.title}\nAuthors: {authors_str}\n{abstract_text}")
        ps = PaperSummary(
            title=p.title,
            abstract_overview=abstract_text[:300],
            methodology=p.methodology or "Not specified",
            key_findings="See full summary",
            score=getattr(p, "final_score", 0.0),
        )
        all_summaries.append(ps)

    state["all_paper_summaries"] = all_summaries

    if abstracts:
        try:
            comb = await ToolAgents.generate_combined_summary(abstracts)
            state["combined_summary"] = comb
        except Exception as e:
            logger.warning(f"Combined summarization failed (LLM error): {e}")
            state["combined_summary"] = "Combined summary unavailable (LLM rate limit reached). Please try again later."
        
        try:
            mermaid_code = await ToolAgents.generate_workflow_mermaid(state.get("combined_summary", ""))
            if mermaid_code:
                img_path = await ToolAgents.download_mermaid_image(mermaid_code, settings.JSON_OUTPUT_DIR)
                state["combined_mermaid_img"] = img_path
        except Exception as e:
            logger.warning(f"Combined mermaid generation failed: {e}")
    else:
        state["combined_summary"] = ""
        state["combined_mermaid_img"] = None
    return state


async def gap_node(state: WorkflowState) -> WorkflowState:
    """Extract research gaps from the summaries. Always populate this field
    so that the PDF and API response contain gap analysis."""
    best_summary = state.get("best_paper_summary") or ""
    comb_summary = state.get("combined_summary") or ""

    context_parts = []
    if best_summary:
        context_parts.append(f"Best Paper Summary:\n{best_summary}")
    if comb_summary:
        context_parts.append(f"Combined Research Synthesis:\n{comb_summary}")

    scores = state.get("scores", [])
    if scores:
        paper_info = []
        for p in scores[:5]:
            paper_info.append(
                f"- {p.title} ({p.year or 'N/A'}, citations: {p.citationCount or 0})"
            )
        context_parts.append(f"Top Papers Analyzed:\n" + "\n".join(paper_info))

    context = "\n\n".join(context_parts)

    if context.strip():
        gaps = await ToolAgents.extract_research_gaps(context)
        state["research_gaps"] = gaps
    else:
        state["research_gaps"] = ""
    return state


async def pdf_node(state: WorkflowState) -> WorkflowState:
    papers = state.get("papers", [])
    if not papers:
        state["pdf_paths"] = []
        return state

    pdf_paths = []
    try:
        p1 = pdf_generator.generate_best_paper_pdf(state)
        pdf_paths.append(p1)
    except Exception as e:
        logger.error(f"Best paper PDF error: {e}")
    try:
        p2 = pdf_generator.generate_combined_pdf(state)
        pdf_paths.append(p2)
    except Exception as e:
        logger.error(f"Combined PDF error: {e}")
    state["pdf_paths"] = pdf_paths
    return state


async def finalize_node(state: WorkflowState) -> WorkflowState:
    best = state.get("best_paper")
    scores = state.get("scores", [])

    papers_out = []
    for s in scores:
        authors_list = [{"name": a.name, "affiliation": a.affiliation} for a in (s.authors or [])]
        papers_out.append({
            "paperId": s.paperId,
            "title": s.title,
            "abstract": s.abstract,
            "authors": authors_list,
            "methodology": s.methodology,
            "year": s.year,
            "citationCount": s.citationCount,
            "university": s.university,
            "journal": s.journal,
            "url": s.url,
            "similarity": s.similarity,
            "citation_score": s.citation_score,
            "recency_score": s.recency_score,
            "novelty_score": s.novelty_score,
            "final_score": s.final_score,
        })

    report = {
        "query": state.get("query"),
        "plan": state.get("plan"),
        "papers": papers_out,
        "best_paper": papers_out[0] if papers_out else None,
        "best_paper_summary": state.get("best_paper_summary"),
        "combined_summary": state.get("combined_summary"),
        "research_gaps": state.get("research_gaps"),
        "pdf_paths": state.get("pdf_paths"),
    }

    os.makedirs(settings.JSON_OUTPUT_DIR, exist_ok=True)
    rpath = os.path.join(settings.JSON_OUTPUT_DIR, f"report_{os.urandom(4).hex()}.json")
    with open(rpath, "w") as f:
        json.dump(report, f, indent=2, default=str)

    state["reproducible_report"] = report
    if state.get("status") != "no_papers_found":
        state["status"] = "completed"
    return state