import asyncio
import os
import json
from httpx import AsyncClient, ASGITransport
from app.main import app

async def run_tests():
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            print("1. Testing relevant query...")
            response = await ac.post("/api/research", json={"query": "deep learning for medical image analysis"})
            print(f"Status Code: {response.status_code}")
            if response.status_code != 200:
                print("Error Response:", response.text)
                return
            data = response.json()
            print(f"Data status: {data.get('status')}")
            print(f"Papers found: {len(data.get('papers', []))}")
            if not len(data.get('papers', [])) > 0:
                print("FAILED: No papers found when there should be.")
                return
            if not data.get("research_gaps"):
                print("FAILED: No research gaps generated.")
                return
            
            print("\n2. Testing irrelevant query...")
            response2 = await ac.post("/api/research", json={"query": "ancient roman pottery techniques from 200 BC"})
            print(f"Status Code: {response2.status_code}")
            data2 = response2.json()
            print(f"Data status: {data2.get('status')}")
            print(f"Papers found: {len(data2.get('papers', []))}")
            if len(data2.get('papers', [])) > 0:
                print("FAILED: Papers found for irrelevant query.")
                return
                
            print("\n3. Testing stats endpoint...")
            response3 = await ac.get("/api/stats")
            print(f"Status Code: {response3.status_code}")
            data3 = response3.json()
            print("Stats:", data3)
            
            print("\nALL CLEAR. Tests passed!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_tests())
