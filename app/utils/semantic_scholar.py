import aiohttp
import asyncio
import logging
from typing import List
from app.config import settings
from app.models.state import PaperMetadata

logger = logging.getLogger(__name__)

class SemanticScholarClient:
    MAX_RETRIES = 5
    BASE_DELAY = 3

    def __init__(self):
        self.base_url = settings.SEMANTIC_SCHOLAR_URL

    async def search_papers(self, query: str, limit: int = 10) -> List[PaperMetadata]:
        url = f"{self.base_url}/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "url,title,abstract,year,citationCount"
        }

        for attempt in range(self.MAX_RETRIES):
            async with aiohttp.ClientSession() as session:
                try:
                    timeout = aiohttp.ClientTimeout(total=15)
                    async with session.get(url, params=params, timeout=timeout) as response:
                        if response.status == 429:
                            delay = self.BASE_DELAY * (2 ** attempt)
                            logger.warning(f"Rate limited (429). Retrying in {delay}s (attempt {attempt+1}/{self.MAX_RETRIES})")
                            await asyncio.sleep(delay)
                            continue

                        response.raise_for_status()
                        data = await response.json()
                        papers = []
                        for item in data.get("data", []):
                            if item.get("paperId"):
                                papers.append(PaperMetadata(
                                    paperId=item["paperId"],
                                    title=item.get("title") or "",
                                    abstract=item.get("abstract"),
                                    year=item.get("year"),
                                    citationCount=item.get("citationCount"),
                                    url=item.get("url")
                                ))
                        logger.info(f"Retrieved {len(papers)} papers for query: {query[:50]}")
                        return papers
                except aiohttp.ClientResponseError as e:
                    if e.status == 429:
                        delay = self.BASE_DELAY * (2 ** attempt)
                        logger.warning(f"Rate limited (429). Retrying in {delay}s (attempt {attempt+1}/{self.MAX_RETRIES})")
                        await asyncio.sleep(delay)
                        continue
                    logger.error(f"HTTP error from Semantic Scholar: {e}")
                    return []
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout on attempt {attempt+1}/{self.MAX_RETRIES}")
                    await asyncio.sleep(self.BASE_DELAY)
                    continue
                except Exception as e:
                    logger.error(f"Error fetching from Semantic Scholar: {e}")
                    return []

        logger.error(f"All {self.MAX_RETRIES} retries exhausted for query: {query[:50]}")
        return []
