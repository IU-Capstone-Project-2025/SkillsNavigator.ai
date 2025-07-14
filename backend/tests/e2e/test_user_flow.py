import pytest
from httpx import AsyncClient
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@pytest.mark.asyncio
async def test_live_search_and_popular():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/courses/roadmaps", json={
            "area": "AI",
            "current_level": "beginner",
            "desired_skills": "python"
        })
        assert response.status_code in (200, 404)

        response = await client.get("/api/courses/popular", timeout=20.0)
        assert response.status_code in (200, 404)