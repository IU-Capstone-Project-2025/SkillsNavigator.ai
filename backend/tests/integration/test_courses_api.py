import pytest
from httpx import AsyncClient, ASGITransport, Response
from fastapi import status
from unittest.mock import AsyncMock, patch

from app.main import app


@pytest.mark.asyncio
@patch("app.services.encoder.encoder.vectorize", new_callable=AsyncMock)
@patch("app.services.qdrant.qdrant.search", new_callable=AsyncMock)
async def test_search_courses_integration(mock_search, mock_vectorize):
    """
    Интеграционный тест для POST /api/courses/search.

    Проверяет полный путь от запроса до ответа с рабочими зависимостями.
    """
    # Настраиваем mock-ответы
    mock_vectorize.return_value = [0.1, 0.2, 0.3]
    mock_search.return_value = [
        AsyncMock(payload={
            "id": 1,
            "cover_url": "https://example.com/image.jpg",
            "title": "Integration Course",
            "duration": 2,
            "difficulty": "medium",
            "price": 0,
            "currency_code": "USD",
            "pupils_num": 111,
            "authors": "Jane Doe",
            "rating": 4,
            "url": "https://stepik.org/course/1",
            "description": "Integration test",
            "summary": "summary",
            "target_audience": "everyone",
            "acquired_skills": "skill1",
            "acquired_assets": "asset1",
            "title_en": "Integration Course",
            "learning_format": "online"
        })
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/courses/search", json={
            "area": "ML",
            "current_level": "beginner",
            "desired_skills": "python"
        })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["title"] == "Integration Course"


@patch("httpx.AsyncClient")
@pytest.mark.asyncio
async def test_popular_courses_integration(mock_client_class):
    """
    Интеграционный тест GET /api/courses/popular с подменой внешнего API Stepik.
    """
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.get.side_effect = [
        Response(200, json={"course-recommendations": [{"courses": [202]}]}),
        Response(200, json={"courses": [{
            "id": 202,
            "cover": "https://example.com/image.jpg",
            "title": "Popular Integration Course",
            "time_to_complete": 3600,
            "difficulty": "easy",
            "price": 0,
            "currency_code": "USD",
            "learners_count": 500,
            "authors": [1],
            "review_summary": 999,
            "description": "Popular desc",
            "summary": "Popular sum",
            "target_audience": "All",
            "acquired_skills": ["skillA"],
            "acquired_assets": ["assetA"],
            "title_en": "Popular Integration Course",
            "learning_format": "online"
        }]}),
        Response(200, json={"course-review-summaries": [{"course": 202, "average": 5}]}),
        Response(200, json={"users": [{"id": 1, "full_name": "Author Name"}]})
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/courses/popular")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["title"] == "Popular Integration Course"
    assert data[0]["authors"] == "Author Name"
