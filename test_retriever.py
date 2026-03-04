import asyncio
from app.services.paper_retriever import retrieve_papers

async def main():
    papers = await retrieve_papers("polar bears")
    print(f"Retrieved: {len(papers)}")
    if papers:
        print(papers[0].title)

asyncio.run(main())
