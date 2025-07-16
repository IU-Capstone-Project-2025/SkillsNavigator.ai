import httpx
import logging
import json
from typing import List
from app.config import settings
from app.utils.query_logger import query_logger

logger = logging.getLogger(__name__)


class DeepseekService:
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_url = settings.deepseek_api_url

    async def choose_courses(self, area, current_level, desired_skills, hours, cost, attempt, courses):
        logger.info(f"API Key is {'present' if self.api_key else 'missing'}...")

        if not self.api_key or self.api_key == "":
            logger.warning("Deepseek API key not configured")
            # fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
            # query_logger.log_queries(area, current_level, desired_skills, fallback_queries, "fallback")
            return None

        try:
            prompt = f"""
            You are a course recommender AI. Your job is to select up to 5 courses from the list of {len(courses)} that together form a coherent learning roadmap for the user.

            User's learning profile:
            - Goal: {area}
            - Current level: {current_level}
            - Desired skills to acquire: {desired_skills}
            - Maximum total time to complete all courses in hours: {hours}
            - Maximum total cost of all courses in RUB: {cost}

            Each course includes:
            - Title
            - Summary
            - Difficulty level (e.g., Beginner, Intermediate, Advanced)
            - Number of learners who completed it
            - Time to complete in hours
            - Price
            - Currency code

            Courses:
            """
            for idx, course in enumerate(courses):
                prompt += f"\n{idx}. Title: {course['title']}; Summary: {course['summary']}; Difficulty: {course['difficulty']}; Learners: {course['pupils_num']}; Duration: {course['duration']}; Price: {course['price']}; Currency code: {course['currency_code']}"

            prompt += (
                "\n\nYour task:"
                "\n- Select up to 5 courses that form a logical learning roadmap for the user's goal and desired skills."
                "\n- The roadmap should make sense in order — start with foundational topics and build toward more advanced ones."
                "\n- Avoid overlapping or redundant content."
                "\n- Only include courses that are clearly relevant to the user's goals."
                "\n- The **total time** of all selected courses must not exceed the user's limit."
                "\n- The **total price** of all selected courses must not exceed the user's budget."
                "\n- Among equally suitable options, prefer those with more learners (as a proxy for quality)."
                "\n- If fewer than 5 courses are needed to build a roadmap, return only those."

                "\n\nReturn a Python list of the selected course indexes in the recommended order of completion."
                "\nOnly return the list, like this: [2, 7, 10] (no explanations)."
            )

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.05,
                        "max_tokens": 500
                    }
                )

                logger.info(f"API Response status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    logger.info(f"API Response content: {content}")

                    # Try to parse JSON from the response
                    try:
                        idxs = json.loads(content)
                        if isinstance(idxs, list):
                            logger.info(f"Chosen indexes (attempt {attempt + 1}): {idxs}")
                            # Log the queries to file
                            # query_logger.log_queries(area, current_level, desired_skills, idxs,
                            #                          f"deepseek_attempt_{attempt + 1}")
                            return [courses[i] for i in idxs]
                        else:
                            logger.warning("Invalid response format from Deepseek API")
                            # fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
                            # query_logger.log_queries(area, current_level, desired_skills, fallback_queries,
                            #                          f"fallback_invalid_format_attempt_{attempt + 1}")
                            return None
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse JSON from Deepseek API response")
                        # fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
                        # query_logger.log_queries(area, current_level, desired_skills, fallback_queries,
                        #                          f"fallback_json_error_attempt_{attempt + 1}")
                        return None
                else:
                    logger.error(f"Deepseek API error: {response.status_code} - {response.text}")
                    # fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
                    # query_logger.log_queries(area, current_level, desired_skills, fallback_queries,
                    #                          f"fallback_api_error_attempt_{attempt + 1}")
                    return None

        except Exception as e:
            logger.exception(f"Error calling Deepseek API: {str(e)}")
            # fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
            # query_logger.log_queries(area, current_level, desired_skills, fallback_queries,
            #                          f"fallback_exception_attempt_{attempt + 1}")
            return None


deepseek = DeepseekService()
