import os
import json
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.graph.workflow import graph
from app.config import settings
from app.models import ResearchState
from app.routers import research  # Import the module, not the router

logger = logging.getLogger(__name__)

# Create main router
router = APIRouter()

# Include research routes with a prefix (optional)
router.include_router(research.router, prefix="/research")

# ... rest of your existing routes (keep everything below this line) ...
# All your @router.post("/research"), @router.get("/pdf"), etc. stay exactly as they are
HISTORY_FILE = os.path.join(settings.JSON_OUTPUT_DIR, "history.json")

class ResearchRequest(BaseModel):
    query: str

def _load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading history: {e}")
        return []

def _save_history(history_list):
    os.makedirs(settings.JSON_OUTPUT_DIR, exist_ok=True)
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history_list, f, indent=2)
    except Exception as e:
        logger.error(f"Error writing history: {e}")


class AuthorOut(BaseModel):
    name: str = ""
    affiliation: str = ""


class PaperOut(BaseModel):
    paperId: str
    title: str
    abstract: str | None = None
    authors: list[AuthorOut] = []
    methodology: str | None = None
    year: int | None = None
    citationCount: int | None = None
    university: str | None = None
    journal: str | None = None
    url: str | None = None
    similarity: float = 0.0
    citation_score: float = 0.0
    recency_score: float = 0.0
    novelty_score: float = 0.0
    final_score: float = 0.0


class ResearchResponse(BaseModel):
    query: str
    status: str
    papers: list[PaperOut] = []
    best_paper: PaperOut | None = None
    best_paper_summary: str | None = None
    combined_summary: str | None = None
    research_gaps: str | None = None
    pdf_paths: list[str] = []


class IngestRequest(BaseModel):
    paper_id: str
    title: str
    abstract: str | None = None
    authors: list[dict] = []
    methodology: str | None = None
    year: int | None = None
    citation_count: int = 0
    university: str | None = None
    journal: str | None = None
    url: str | None = None


@router.post("/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest):
    try:
        initial_state = {
            "query": request.query,
            "plan": None,
            "papers": [],
            "scores": [],
            "best_paper": None,
            "best_paper_summary": None,
            "combined_summary": None,
            "all_paper_summaries": [],
            "research_gaps": None,
            "pdf_paths": [],
            "reproducible_report": {},
            "status": "started",
        }

        final_state = await graph.ainvoke(initial_state)

        papers = final_state.get("papers") or []
        if not papers:
            result = ResearchResponse(
                query=final_state.get("query"),
                status="no_papers_found",
                papers=[],
                combined_summary="No matching papers were found in the database. Try modifying your search keywords or broading the topic.",
            )
        else:
            scores = final_state.get("scores", [])
            papers_out = []
            for s in scores:
                authors_out = [
                    AuthorOut(name=a.name, affiliation=a.affiliation)
                    for a in (s.authors or [])
                ]
                papers_out.append(PaperOut(
                    paperId=s.paperId, title=s.title, abstract=s.abstract,
                    authors=authors_out, methodology=s.methodology,
                    year=s.year, citationCount=s.citationCount,
                    university=s.university, journal=s.journal, url=s.url,
                    similarity=s.similarity, citation_score=s.citation_score,
                    recency_score=s.recency_score, novelty_score=s.novelty_score,
                    final_score=s.final_score,
                ))

            best = final_state.get("best_paper")
            best_out = papers_out[0] if papers_out else None

            result = ResearchResponse(
                query=final_state.get("query"),
                status=final_state.get("status", "failed"),
                papers=papers_out,
                best_paper=best_out,
                best_paper_summary=final_state.get("best_paper_summary"),
                combined_summary=final_state.get("combined_summary"),
                research_gaps=final_state.get("research_gaps"),
                pdf_paths=final_state.get("pdf_paths", []),
            )

        try:
            history_list = _load_history()
            new_id = 1
            if history_list:
                new_id = max(h.get("id", 0) for h in history_list) + 1
            
            history_record = {
                "id": new_id,
                "query": result.query,
                "status": result.status,
                "papers": [p.model_dump() for p in result.papers],
                "best_paper": result.best_paper.model_dump() if result.best_paper else None,
                "best_paper_summary": result.best_paper_summary,
                "combined_summary": result.combined_summary,
                "research_gaps": result.research_gaps,
                "pdf_paths": result.pdf_paths,
                "created_at": datetime.utcnow().isoformat()
            }
            history_list.insert(0, history_record) # Add to front
            _save_history(history_list)
        except Exception as he:
            logger.error(f"Failed to save history to json: {he}")

        return result
    except Exception as e:
        logger.error(f"Research error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pdf")
async def get_pdf(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(path, media_type="application/pdf", filename=os.path.basename(path))


@router.get("/papers")
async def list_papers():
    return {"total": 0, "papers": []}


@router.get("/stats")
async def get_stats():
    """Return an overview of the platform stats for the dashboard."""
    return {
        "total_papers": 0,
        "total_queries": 0,
        "year_range": "N/A",
        "total_citations": 0,
    }


@router.get("/history")
async def list_history():
    history_list = _load_history()
    
    summary_list = []
    for h in history_list:
        summary_list.append({
            "id": h.get("id"),
            "query": h.get("query"),
            "status": h.get("status"),
            "created_at": h.get("created_at"),
            "paper_count": len(h.get("papers", []))
        })
        
    return {"total": len(summary_list), "history": summary_list}


@router.get("/history/{history_id}")
async def get_history(history_id: int):
    history_list = _load_history()
    for h in history_list:
        if h.get("id") == history_id:
            return h
            
    raise HTTPException(status_code=404, detail="History record not found")


@router.delete("/history/{history_id}")
async def delete_history(history_id: int):
    history_list = _load_history()
    new_history = [h for h in history_list if int(h.get("id", -1)) != history_id]
    
    if len(new_history) == len(history_list):
        raise HTTPException(status_code=404, detail="History record not found")
        
    _save_history(new_history)
    return {"message": "History deleted successfully"}
