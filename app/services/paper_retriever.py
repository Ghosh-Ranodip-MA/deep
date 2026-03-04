import logging
import aiohttp
from typing import List

from app.models.state import PaperMetadata, AuthorInfo
from app.config import settings

logger = logging.getLogger(__name__)

async def retrieve_papers(query: str, top_k: int = 10) -> List[PaperMetadata]:
    """Retrieve top-K valid papers from OpenAlex."""
    logger.info(f"Querying OpenAlex for: {query[:60]}")
    
    url = f"{settings.OPENALEX_URL}/works"
    params = {
        "search": query,
        "per_page": top_k,
    }
    
    if settings.OPENALEX_EMAIL:
        params["mailto"] = settings.OPENALEX_EMAIL
        
    results = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    text_resp = await response.text()
                    logger.error(f"OpenAlex API error: {response.status} - {text_resp}")
                    return []
                
                data = await response.json()
                papers_data = data.get("results", [])
                
                for item in papers_data:
                    authors = []
                    for a in item.get("authorships", []):
                        author_info = a.get("author", {})
                        inst_info = a.get("institutions", [{}])
                        authors.append(AuthorInfo(
                            name=author_info.get("display_name", ""),
                            affiliation=inst_info[0].get("display_name", "") if inst_info else ""
                        ))
                    
                    # OpenAlex returns an inverted index for abstracts to avoid copyright issues
                    abs_idx = item.get("abstract_inverted_index")
                    abstract_text = ""
                    if abs_idx:
                        # Find the max position to construct the array
                        max_pos = max([pos for positions in abs_idx.values() for pos in positions])
                        words = [""] * (max_pos + 1)
                        for word, positions in abs_idx.items():
                            for pos in positions:
                                words[pos] = word
                        abstract_text = " ".join(words).strip()
                        
                    pm = PaperMetadata(
                        paperId=item.get("id", "").split("/")[-1],
                        title=item.get("title") or "Untitled",
                        abstract=abstract_text,
                        authors=authors,
                        methodology="Not specified",
                        year=item.get("publication_year"),
                        citationCount=item.get("cited_by_count") or 0,
                        university="",
                        journal=item.get("primary_location", {}).get("source", {}).get("display_name") if item.get("primary_location") and item.get("primary_location").get("source") else "",
                        url=item.get("doi") or item.get("id", ""),
                    )
                    results.append(pm)
                    
        logger.info(f"Retrieved {len(results)} papers from OpenAlex.")
        return results
        
    except Exception as e:
        logger.error(f"Error calling OpenAlex API: {e}", exc_info=True)
        return []

async def get_paper_count() -> int:
    """Return count of papers. With Semantic Scholar, we return 0 or a mocked number."""
    return 0
