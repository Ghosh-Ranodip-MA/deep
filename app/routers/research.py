from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.schemas.research_schema import AnalysisRequest, AnalysisResponse, ReportResponse
from app.models.database import get_db
from app.models.research_model import AnalysisReport
from app.graph.graph_builder import build_graph
from app.graph.nodes import GraphState
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["research"])

@router.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    report = AnalysisReport(
        topic=request.topic,
        query=request.topic,
        status="pending"
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    
    background_tasks.add_task(run_workflow, report.id, request.topic, request.max_papers)
    
    return AnalysisResponse(
        report_id=report.id,
        status="pending",
        message="Analysis started. Use /report/{report_id} to get results."
    )

@router.get("/status/{report_id}")
async def get_status(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await db.get(AnalysisReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report_id": report_id, "status": report.status}

@router.get("/report/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await db.get(AnalysisReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != "completed":
        raise HTTPException(status_code=400, detail=f"Analysis not completed yet. Status: {report.status}")
    return ReportResponse(**report.reproducible_report)

async def run_workflow(report_id: int, query: str, max_papers: int):
    logger.info(f"Starting workflow for report {report_id}")
    graph = build_graph()
    initial_state: GraphState = {
        "query": query,
        "papers": [],
        "scores": [],
        "best_paper": None,
        "combined_summary": None,
        "research_gaps": None,
        "pdf_paths": None,
        "reproducible_report": None,
        "status": "pending",
        "error": None,
        "report_id": report_id,
        "max_papers": max_papers,
        "plan": None
    }
    try:
        final_state = await graph.ainvoke(initial_state)
        logger.info(f"Workflow completed for report {report_id} with status {final_state['status']}")
    except Exception as e:
        logger.error(f"Workflow crashed: {e}")
        async with AsyncSessionLocal() as db:
            db_report = await db.get(AnalysisReport, report_id)
            if db_report:
                db_report.status = "failed"
                db_report.reproducible_report = {"error": str(e)}
                await db.commit()