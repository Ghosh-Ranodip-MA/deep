from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AuthorInfo(BaseModel):
    name: str
    affiliation: str = ""


class PaperMetadata(BaseModel):
    paperId: str
    title: str
    abstract: str | None = None
    authors: List[AuthorInfo] = Field(default_factory=list)
    methodology: str | None = None
    year: int | None = None
    citationCount: int | None = None
    university: str | None = None
    journal: str | None = None
    url: str | None = None


class ScoredPaper(PaperMetadata):
    similarity: float = 0.0
    citation_score: float = 0.0
    recency_score: float = 0.0
    novelty_score: float = 0.0
    final_score: float = 0.0


class Plan(BaseModel):
    query: str
    search_keywords: List[str]
    intent: str


class PaperSummary(BaseModel):
    title: str
    abstract_overview: str = ""
    methodology: str = ""
    key_findings: str = ""
    score: float = 0.0


class WorkflowState(TypedDict):
    query: str
    plan: Optional[Plan]
    papers: List[PaperMetadata]
    scores: List[ScoredPaper]
    best_paper: Optional[ScoredPaper]
    best_paper_summary: Optional[str]
    best_paper_mermaid_img: Optional[str]
    combined_summary: Optional[str]
    combined_mermaid_img: Optional[str]
    all_paper_summaries: List[PaperSummary]
    research_gaps: Optional[str]
    pdf_paths: List[str]
    reproducible_report: Dict[str, Any]
    status: str
