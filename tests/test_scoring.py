import pytest
from unittest.mock import patch, AsyncMock
from app.graph.nodes import score_node
from app.models.state import PaperMetadata

@pytest.mark.asyncio
async def test_score_node():
    with patch("app.graph.nodes.compute_similarity", return_value=0.8), \
         patch("app.agents.tools.ToolAgents.evaluate_novelty", new_callable=AsyncMock, return_value=0.9):
        
        state = {
            "query": "LLMs in robotics",
            "papers": [
                PaperMetadata(
                    paperId="1", title="Test Paper", abstract="Test abstract", year=2023, citationCount=10, url=""
                )
            ]
        }
        
        new_state = await score_node(state)
        scores = new_state.get("scores", [])
        assert len(scores) == 1
        assert scores[0].final_score > 0
        assert scores[0].similarity == 0.8
        assert scores[0].novelty_score == 0.9
