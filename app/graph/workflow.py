from langgraph.graph import StateGraph, END
from app.models.state import WorkflowState
from app.graph.nodes import (
    planner_node, retrieve_node, score_node, select_top_node,
    summarize_best_node, summarize_combined_node, gap_node, pdf_node, finalize_node
)


def build_graph():
    workflow = StateGraph(WorkflowState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("score", score_node)
    workflow.add_node("select_top", select_top_node)
    workflow.add_node("summarize_best", summarize_best_node)
    workflow.add_node("summarize_combined", summarize_combined_node)
    workflow.add_node("gap", gap_node)
    workflow.add_node("pdf", pdf_node)
    workflow.add_node("finalize", finalize_node)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "retrieve")

    def route_after_retrieve(state: WorkflowState):
        if state.get("status") == "no_papers_found" or not state.get("papers"):
            return "finalize"
        return "score"

    workflow.add_conditional_edges(
        "retrieve",
        route_after_retrieve,
        {
            "score": "score",
            "finalize": "finalize"
        }
    )

    workflow.add_edge("score", "select_top")
    workflow.add_edge("select_top", "summarize_best")
    workflow.add_edge("summarize_best", "summarize_combined")
    workflow.add_edge("summarize_combined", "gap")
    workflow.add_edge("gap", "pdf")
    workflow.add_edge("pdf", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile()


graph = build_graph()
