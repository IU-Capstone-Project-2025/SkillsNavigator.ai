import pytest
from httpx import AsyncClient, ASGITransport, Response
from fastapi import status
from unittest.mock import AsyncMock, patch

from app.main import app

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.routers.users import get_current_user
from app.services import database, Base


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    database.engine = test_engine
    database.session = sessionmaker(bind=test_engine)


@pytest.mark.asyncio
async def test_check_search_endpoint_exists():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/courses/roadmaps", json={})
    assert response.status_code != 404  # просто убедиться, что он существует


def make_course_payload(overrides: dict = None) -> dict:
    """Генератор валидного словаря курса для мок-ответов."""
    data = {
        "id": 1,
        "cover_url": "https://example.com/image.jpg",
        "title": "Test Course",
        "duration": 4,
        "difficulty": "medium",
        "price": 0,
        "currency_code": "USD",
        "pupils_num": 123,
        "authors": "John Doe",
        "rating": 5,
        "url": "https://stepik.org/course/1/promo",
        "description": "Learn test-driven development",
        "summary": "Course for testing",
        "target_audience": "Developers",
        "acquired_skills": "testing, mocking",
        "acquired_assets": "project templates",
        "title_en": "Test Course",
        "learning_format": "online"
    }
    if overrides:
        data.update(overrides)
    return data


@pytest.mark.asyncio
@patch("app.services.qdrant.qdrant.search", new_callable=AsyncMock)
@patch("app.services.encoder.encoder.vectorize", new_callable=AsyncMock)
async def test_search_courses_success(mock_vectorize, mock_search):
    mock_vectorize.return_value = [0.1, 0.2, 0.3]

    class MockPoint:
        payload = make_course_payload()

    mock_search.return_value = [MockPoint()]

    app.dependency_overrides[get_current_user] = lambda: "test_user_id"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/courses/roadmaps", json={
            "area": "Data Science",
            "current_level": "beginner",
            "desired_skills": "python, ml",
        })

    # Очистить overrides, чтобы не повлияло на другие тесты
    app.dependency_overrides = {}

    assert response.status_code == status.HTTP_200_OK


@patch("httpx.AsyncClient")
@pytest.mark.asyncio
async def test_get_popular_courses_success(mock_client_class):
    """Тест успешного получения популярных курсов через Stepik API."""

    # Создаём мок экземпляра клиента
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client

    # Настраиваем, что будет возвращать mock_client.get(...) при каждом вызове
    mock_client.get.side_effect = [
        Response(200, json={
            "course-recommendations": [{"courses": [101]}]
        }),
        Response(200, json={
            "courses": [{
                "id": 101,
                "cover": "https://example.com/image.jpg",
                "title": "Popular Course",
                "time_to_complete": 7200,
                "difficulty": "easy",
                "price": 0,
                "currency_code": "RUB",
                "learners_count": 456,
                "authors": [1],
                "review_summary": 1001,
                "description": "Popular course description",
                "summary": "Popular course summary",
                "target_audience": "All",
                "acquired_skills": "skill1, skill2",
                "acquired_assets": "asset1",
                "title_en": "Popular Course EN",
                "learning_format": "online"
            }]
        }),
        Response(200, json={
            "course-review-summaries": [{"course": 101, "average": 5}]
        }),
        Response(200, json={
            "users": [{"id": 1, "full_name": "Stepik Author"}]
        })
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/courses/popular")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result[0]["title"] == "Popular Course"
    assert result[0]["authors"] == "Stepik Author"
