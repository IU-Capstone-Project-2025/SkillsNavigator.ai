import logging

from sympy.physics.mechanics import Body
from fastapi import HTTPException

from app.models import CourseSearchRequest
from app.services import deepseek, encoder, qdrant
from app.utils import query_logger

logger = logging.getLogger(__name__)

async def get_courses(payload: CourseSearchRequest):
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
            min_threshold = 0  # Lowered threshold to capture more relevant courses

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

                            logger.info(
                                f"Query '{query}' found course '{course['title']}' with similarity score: {similarity_score}")

                            # Check if this course meets minimum threshold
                            if similarity_score >= min_threshold:
                                # Only consider if we haven't seen this course before
                                if course["id"] not in seen_course_ids:
                                    good_courses.append((course, similarity_score))
                                    logger.info(
                                        f"Good course found for query '{query}': '{course['title']}' (score: {similarity_score})")
                                else:
                                    logger.info(f"Course {course['title']} already found, skipping duplicate")
                            else:
                                logger.info(
                                    f"Course '{course['title']}' rejected due to low similarity score: {similarity_score} < {min_threshold}")

                        # Sort by similarity score and take up to 2 best courses per query
                        good_courses.sort(key=lambda x: x[1], reverse=True)
                        courses_to_add = good_courses

                        for course, score in courses_to_add:
                            all_results.append(course)
                            seen_course_ids.add(course["id"])
                            logger.info(f"Added course from query '{query}': '{course['title']}' (score: {score})")

                        if not courses_to_add:
                            logger.info(
                                f"No suitable courses found for query '{query}' (all below {min_threshold} threshold)")
                    else:
                        logger.info(f"No results found for query: {query}")

                except Exception as e:
                    logger.warning(f"Error searching for query '{query}': {str(e)}")
                    continue

            # If we have too many results, prioritize by similarity score
            if len(all_results) > 5:
                logger.info(f"Found {len(all_results)} courses, limiting to top 5 by deepseek mind")
                # Sort all results by their similarity scores (we'll need to track this)
                # For now, just take the first 5
                for attempt2 in range(3):
                    res = await deepseek.choose_courses(payload.area, payload.current_level, payload.desired_skills, attempt2,
                                                  all_results)
                    if res is not None:
                        all_results = res
                        break

            if all_results:
                logger.info(
                    f"Found {len(all_results)} unique courses from {len(search_queries)} queries (min threshold: {min_threshold})")
                return all_results
            else:
                logger.warning(
                    f"No search results found that meet minimum threshold {min_threshold} (attempt {attempt + 1})")
                if attempt < 2:  # Don't log on the last attempt
                    logger.info("Will retry with new queries")
    except Exception as e:
        logger.exception(f"Error course searching: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_courses_v2(payload: CourseSearchRequest):
    try:
        all_results = []
        min_threshold = 0  # Lowered threshold to capture more relevant courses
        query = payload.area + " " + payload.current_level + " " + payload.desired_skills
        try:
            vector = await encoder.vectorize(query)
            results = await qdrant.search(vector, "courses", limit=100)  # Get 100 results

            # Log search results with similarity scores
            query_logger.log_search_results(query, results, min_threshold)

            if results and len(results) > 0:
                # Find multiple good courses from this query that meet the threshold
                good_courses = []

                for result in results:
                    course = result.payload
                    similarity_score = result.score

                    logger.info(
                        f"Query '{query}' found course '{course['title']}' with similarity score: {similarity_score}")

                    # Check if this course meets minimum threshold
                    if similarity_score >= min_threshold:
                        # Only consider if we haven't seen this course before
                        good_courses.append((course, similarity_score))
                        logger.info(
                            f"Good course found for query '{query}': '{course['title']}' (score: {similarity_score})")
                    else:
                        logger.info(
                            f"Course '{course['title']}' rejected due to low similarity score: {similarity_score} < {min_threshold}")

                # Sort by similarity score and take up to 2 best courses per query
                good_courses.sort(key=lambda x: x[1], reverse=True)
                courses_to_add = good_courses

                for course, score in courses_to_add:
                    all_results.append(course)
                    logger.info(f"Added course from query '{query}': '{course['title']}' (score: {score})")

                if not courses_to_add:
                    logger.info(
                        f"No suitable courses found for query '{query}' (all below {min_threshold} threshold)")
            else:
                logger.info(f"No results found for query: {query}")

        except Exception as e:
            logger.warning(f"Error searching for query '{query}': {str(e)}")

        # If we have too many results, prioritize by similarity score
        flag = True
        if len(all_results) > 5:
            logger.info(f"Found {len(all_results)} courses, limiting to top 5 by deepseek mind")
            # Sort all results by their similarity scores (we'll need to track this)
            # For now, just take the first 5
            for attempt2 in range(3):
                res = await deepseek.choose_courses(payload.area, payload.current_level, payload.desired_skills, payload.hours, payload.cost, attempt2,
                                              all_results)
                if res is not None:
                    all_results = res
                    flag = False
                    break
        if flag:
            logger.info("No search results found")
            return []
        if all_results:
            logger.info(
                f"Found {len(all_results)} unique courses from {1} queries (min threshold: {min_threshold})")
            return all_results
        else:
            logger.warning(
                f"No search results found that meet minimum threshold {min_threshold} (attempt {1})")
    except Exception as e:
        logger.exception(f"Error course searching: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")