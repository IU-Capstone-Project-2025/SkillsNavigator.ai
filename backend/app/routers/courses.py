from fastapi import APIRouter, HTTPException, Body
from typing import List

from app.models import *
from app.services import qdrant, encoder, deepseek
from app.config import settings
from app.utils.query_logger import query_logger

import traceback
import httpx
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.post(
    "/search",
    response_model=List[CourseSummary],
    summary="Поиск курсов по заданным критериям"
)
async def search_courses(payload: CourseSearchRequest = Body(...)):
    """
    Поиск курсов:
    1. **area** — область знаний, которую хочет освоить пользователь
    2. **current_level** — текущий уровень (начальный/средний/продвинутый)
    3. **desired_skills** — конкретные навыки для обучения
    """
    logger.info(
        f"Search courses: area='{payload.area}', level='{payload.current_level}', slills='{payload.desired_skills}'"
    )

    try:
        # Try up to 3 times with different strategies
        for attempt in range(3):
            logger.info(f"Search attempt {attempt + 1}/3")
            
            # Generate search queries using Deepseek API
            search_queries = await deepseek.generate_search_queries(
                payload.area, 
                payload.current_level, 
                payload.desired_skills,
                attempt
            )
            
            logger.info(f"Generated search queries (attempt {attempt + 1}): {search_queries}")
            
            # Search for top 10 results for each query and select the best one
            all_results = []
            seen_course_ids = set()
            min_threshold = 0.4  # Lowered threshold to capture more relevant courses
            
            for query in search_queries:
                try:
                    vector = await encoder.vectorize(query)
                    results = await qdrant.search(vector, "courses", limit=10)  # Get 10 results
                    
                    # Log search results with similarity scores
                    query_logger.log_search_results(query, results, min_threshold)
                    
                    if results and len(results) > 0:
                        # Find multiple good courses from this query that meet the threshold
                        good_courses = []
                        
                        for result in results:
                            course = result.payload
                            similarity_score = result.score
                            
                            logger.info(f"Query '{query}' found course '{course['title']}' with similarity score: {similarity_score}")
                            
                            # Check if this course meets minimum threshold
                            if similarity_score >= min_threshold:
                                # Only consider if we haven't seen this course before
                                if course["id"] not in seen_course_ids:
                                    good_courses.append((course, similarity_score))
                                    logger.info(f"Good course found for query '{query}': '{course['title']}' (score: {similarity_score})")
                                else:
                                    logger.info(f"Course {course['title']} already found, skipping duplicate")
                            else:
                                logger.info(f"Course '{course['title']}' rejected due to low similarity score: {similarity_score} < {min_threshold}")
                        
                        # Sort by similarity score and take up to 2 best courses per query
                        good_courses.sort(key=lambda x: x[1], reverse=True)
                        courses_to_add = good_courses[:2]  # Take up to 2 best courses per query
                        
                        for course, score in courses_to_add:
                            all_results.append(course)
                            seen_course_ids.add(course["id"])
                            logger.info(f"Added course from query '{query}': '{course['title']}' (score: {score})")
                        
                        if not courses_to_add:
                            logger.info(f"No suitable courses found for query '{query}' (all below {min_threshold} threshold)")
                    else:
                        logger.info(f"No results found for query: {query}")
                        
                except Exception as e:
                    logger.warning(f"Error searching for query '{query}': {str(e)}")
                    continue

            # If we have too many results, prioritize by similarity score
            if len(all_results) > 10:
                logger.info(f"Found {len(all_results)} courses, limiting to top 10 by similarity score")
                # Sort all results by their similarity scores (we'll need to track this)
                # For now, just take the first 10
                all_results = all_results[:10]

            if all_results:
                logger.info(f"Found {len(all_results)} unique courses from {len(search_queries)} queries (min threshold: {min_threshold})")
                return all_results
            else:
                logger.warning(f"No search results found that meet minimum threshold {min_threshold} (attempt {attempt + 1})")
                if attempt < 2:  # Don't log on the last attempt
                    logger.info("Will retry with new queries")

        # If we get here, no courses were found after all attempts
        logger.warning("No search results found after all retry attempts")
        raise HTTPException(status_code=404, detail="Курсы не найдены")

    except Exception as e:
        logger.exception(f"Error course searching: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/popular",
    response_model=List[CourseSummary],
    summary="Get popular courses"
)
async def get_popular_courses():
    """
    Возвращает список самых популярных курсов.
    """

    logger.info("Requesting popular courses")

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            logger.info("Send request to Stepik: course-recommendations")
            req = await client.get("https://stepik.org/api/course-recommendations")
            courses_ids_set = req.json()["course-recommendations"][0]["courses"]
            logger.info(f"Got {len(courses_ids_set)} courses")

            params = {'ids[]': courses_ids_set}
            logger.info("Request detailed course info")
            courses_info_req = await client.get("https://stepik.org/api/courses", params=params)
            courses_info = courses_info_req.json()["courses"]

            review_ids = []
            author_ids = []
            courses = {}

            for course_info in courses_info:
                if course_info["authors"]:
                    author_ids.append(course_info["authors"][0])
                review_ids.append(course_info["review_summary"])
                courses[course_info["id"]] = {
                    "id": course_info["id"],
                    "cover_url": course_info["cover"],
                    "title": course_info["title"],
                    "duration": int(course_info["time_to_complete"] / 3600) if course_info["time_to_complete"] else 0,
                    "difficulty": course_info["difficulty"],
                    "price": 0 if course_info["price"] is None else course_info["price"],
                    "currency_code": course_info["currency_code"],
                    "pupils_num": course_info["learners_count"],
                    "authors": course_info["authors"][0] if course_info["authors"] else "",
                    "rating": 5,
                    "url": f"https://stepik.org/course/{course_info['id']}/promo",
                    "description": course_info["description"],
                    "summary": course_info["summary"],
                    "target_audience": course_info["target_audience"],
                    "acquired_skills": ''.join(course_info["acquired_skills"]),
                    "acquired_assets": ''.join(course_info["acquired_assets"]),
                    "title_en": course_info["title_en"],
                    "learning_format": course_info["learning_format"],
                }

            logger.info("Get rating via review_summary")
            reviews = (await client.get("https://stepik.org/api/course-review-summaries", params={'ids[]': review_ids})).json()
            for review in reviews["course-review-summaries"]:
                if review["course"] in courses:
                    courses[review["course"]]["rating"] = int(review["average"])

            logger.info("Get authors info")
            authors = (await client.get("https://stepik.org/api/users", params={'ids[]': author_ids})).json()
            for author in authors["users"]:
                for i in courses:
                    if courses[i]["authors"] == author["id"]:
                        courses[i]["authors"] = author["full_name"]

            for i in courses:
                if str(courses[i]["authors"]).isdigit():
                    courses[i]["authors"] = ""

        results = list(courses.values())
        if not results:
            logger.warning("Popular courses not found")
            raise HTTPException(status_code=404, detail="Popular courses not found")

        logger.info(f"Return {len(results)} popular courses")
        return results

    except Exception as e:
        logger.exception("Error getting popular courses")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/reload-data", summary="Manually reload course data from Stepik")
async def reload_course_data():
    """
    Manually trigger reloading of course data from Stepik API.
    This will re-download and re-index all courses in Qdrant.
    Use this endpoint when you want to update the course database.
    """
    try:
        logger.info("Manual course data reload requested")
        await qdrant.loadCourses()
        return {"message": "Course data reloaded successfully"}
    except Exception as e:
        logger.exception("Error reloading course data")
        raise HTTPException(status_code=500, detail=f"Failed to reload course data: {str(e)}")
