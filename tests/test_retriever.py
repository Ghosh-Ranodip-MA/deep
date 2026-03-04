import pytest
from unittest.mock import patch, AsyncMock
from app.utils.semantic_scholar import SemanticScholarClient
from app.models.state import PaperMetadata

@pytest.mark.asyncio
async def test_semantic_scholar_search():
    client = SemanticScholarClient()
    mock_papers = [
        PaperMetadata(paperId="1", title="Mock Paper", abstract="Abstract", year=2024, citationCount=5)
    ]
    
    with patch.object(client, 'search_papers', new_callable=AsyncMock, return_value=mock_papers):
        results = await client.search_papers("test query")
        assert len(results) == 1
        assert results[0].title == "Mock Paper"
