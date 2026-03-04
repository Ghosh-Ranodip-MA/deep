"""
LangGraph state definition.
Re-exports from the canonical state module.
"""
from app.models.state import WorkflowState, PaperMetadata, ScoredPaper, Plan, PaperSummary, AuthorInfo

ResearchState = WorkflowState

__all__ = ["WorkflowState", "ResearchState", "PaperMetadata", "ScoredPaper", "Plan", "PaperSummary", "AuthorInfo"]
