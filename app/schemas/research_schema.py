from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    topic: str
    max_papers: Optional[int] = 20

class AnalysisResponse(BaseModel):
    report_id: int
    status: str
    message: str

class ReportResponse(BaseModel):
    topic: str
    timestamp: str
    plan: Optional[Dict[str, Any]]
    papers: List[Dict[str, Any]]
    best_paper: Optional[Dict[str, Any]]
    combined_summary: Optional[Dict[str, str]]
    research_gaps: Optional[Dict[str, List[str]]]
    pdf_paths: Optional[Dict[str, str]]
    status: str
    error: Optional[str]