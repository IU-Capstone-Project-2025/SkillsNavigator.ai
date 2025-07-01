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

    async def generate_search_queries(self, area: str, current_level: str, desired_skills: str, attempt: int = 0) -> List[str]:
        """
        Generate 5 different search queries using Deepseek API based on user input
        """
        logger.info(f"API Key check: {self.api_key[:10] if self.api_key else 'None'}...")
        
        if not self.api_key or self.api_key == "":
            logger.warning("Deepseek API key not configured, using fallback queries")
            fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
            query_logger.log_queries(area, current_level, desired_skills, fallback_queries, "fallback")
            return fallback_queries

        try:
            # Adjust prompt based on attempt number
            if attempt == 0:
                # First attempt: specific, tool-focused queries with common software
                prompt = f"""
                Generate 5 specific search queries for finding courses about {area}.
                
                User wants to learn: {area}
                Current level: {current_level}
                Desired skills: {desired_skills}
                
                Create 5 diverse queries for finding educational courses covering different tools, software, techniques, or specific skills within {area}.
                Focus on popular and common tools, software, or techniques that are likely to have courses available in educational platforms.
                
                IMPORTANT: These queries are for finding educational courses, not apps, websites, or general internet resources.
                Avoid queries like "best apps for..." or "top websites for..." - focus on learning content and course topics.
                
                For interior design, focus on:
                - Popular 3D software: SketchUp, 3ds Max, Blender, AutoCAD, ArchiCAD
                - Design principles: color theory, space planning, lighting design
                - Visualization tools: V-Ray, Lumion, Twinmotion
                - Design software: Photoshop, Illustrator, InDesign
                
                Examples for "Interior Design":
                - "sketchup interior design course"
                - "3ds max interior modeling tutorial"
                - "interior design color theory fundamentals"
                - "autocad interior design basics"
                - "vray rendering interior scenes course"
                
                Examples for "3D Artist":
                - "blender 3d modeling course"
                - "substance painter texturing tutorial" 
                - "maya character animation course"
                - "vray rendering setup tutorial"
                - "zbrush sculpting fundamentals course"
                
                Examples for "Web Development":
                - "javascript es6 modern features course"
                - "react hooks and state management tutorial"
                - "node.js backend api development course"
                - "mongodb database design tutorial"
                - "docker containerization course"
                
                Make each query specific to a tool, technique, or software that is commonly taught in courses.
                Return only: ["query1", "query2", "query3", "query4", "query5"]
                """
            elif attempt == 1:
                # Second attempt: broader, more general queries
                prompt = f"""
                Generate 5 broader search queries for finding courses about {area}.
                
                User wants to learn: {area}
                Current level: {current_level}
                Desired skills: {desired_skills}
                
                Create 5 broader queries for finding educational courses that cover general concepts, fundamentals, and introductory topics.
                Focus on learning paths, basics, and foundational knowledge that would be taught in courses.
                
                IMPORTANT: These queries are for finding educational courses, not apps, websites, or general internet resources.
                Focus on course topics and learning content.
                
                Examples for "Interior Design":
                - "interior design fundamentals course"
                - "design principles and basics tutorial"
                - "interior design introduction course"
                - "space planning and layout tutorial"
                - "interior design software overview course"
                
                Examples for "3D Artist":
                - "3d modeling fundamentals course"
                - "digital art basics tutorial"
                - "computer graphics introduction course"
                - "3d software comparison course"
                - "digital design fundamentals tutorial"
                
                Examples for "Web Development":
                - "programming fundamentals course"
                - "web development basics tutorial"
                - "coding for beginners course"
                - "software development introduction tutorial"
                - "computer science fundamentals course"
                
                Make queries broader and more general to catch more courses, but still focused on educational content.
                Return only: ["query1", "query2", "query3", "query4", "query5"]
                """
            else:
                # Third attempt: very broad, alternative approaches
                prompt = f"""
                Generate 5 very broad search queries for finding courses about {area}.
                
                User wants to learn: {area}
                Current level: {current_level}
                Desired skills: {desired_skills}
                
                Create 5 very broad queries for finding educational courses that might be related to this field.
                Include alternative terms, related fields, and general learning topics that could be taught in courses.
                
                IMPORTANT: These queries are for finding educational courses, not apps, websites, or general internet resources.
                Focus on course topics and learning content.
                
                Examples for "Interior Design":
                - "design and creativity course"
                - "visual arts and design tutorial"
                - "architecture and design course"
                - "creative software tutorial"
                - "design and multimedia course"
                
                Examples for "3D Artist":
                - "digital design and creativity course"
                - "visual arts and design tutorial"
                - "computer skills for artists course"
                - "creative software tutorial"
                - "design and multimedia course"
                
                Examples for "Web Development":
                - "computer programming basics course"
                - "technology and software tutorial"
                - "digital skills and tools course"
                - "computer science introduction tutorial"
                - "software and applications course"
                
                Make queries very broad to maximize chances of finding relevant courses, but still focused on educational content.
                Return only: ["query1", "query2", "query3", "query4", "query5"]
                """

            logger.info(f"Making API call to Deepseek with prompt: {prompt[:100]}... (attempt {attempt + 1})")
            
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
                        "temperature": 0.7,
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
                        queries = json.loads(content)
                        if isinstance(queries, list) and len(queries) == 5:
                            logger.info(f"Generated queries (attempt {attempt + 1}): {queries}")
                            # Log the queries to file
                            query_logger.log_queries(area, current_level, desired_skills, queries, f"deepseek_attempt_{attempt + 1}")
                            return queries
                        else:
                            logger.warning("Invalid response format from Deepseek API")
                            fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
                            query_logger.log_queries(area, current_level, desired_skills, fallback_queries, f"fallback_invalid_format_attempt_{attempt + 1}")
                            return fallback_queries
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse JSON from Deepseek API response")
                        fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
                        query_logger.log_queries(area, current_level, desired_skills, fallback_queries, f"fallback_json_error_attempt_{attempt + 1}")
                        return fallback_queries
                else:
                    logger.error(f"Deepseek API error: {response.status_code} - {response.text}")
                    fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
                    query_logger.log_queries(area, current_level, desired_skills, fallback_queries, f"fallback_api_error_attempt_{attempt + 1}")
                    return fallback_queries

        except Exception as e:
            logger.exception(f"Error calling Deepseek API: {str(e)}")
            fallback_queries = self._generate_fallback_queries(area, current_level, desired_skills, attempt)
            query_logger.log_queries(area, current_level, desired_skills, fallback_queries, f"fallback_exception_attempt_{attempt + 1}")
            return fallback_queries

    def _generate_fallback_queries(self, area: str, current_level: str, desired_skills: str, attempt: int = 0) -> List[str]:
        """
        Generate fallback queries when Deepseek API is not available
        """
        if attempt == 0:
            # First attempt: specific queries with common tools
            if "interior" in area.lower() or "дизайн" in area.lower():
                base_queries = [
                    f"sketchup {current_level} course",
                    f"3ds max {current_level} tutorial",
                    f"interior design {current_level} course",
                    f"autocad {current_level} tutorial",
                    f"vray rendering {current_level} course"
                ]
            elif "3d" in area.lower() or "artist" in area.lower():
                base_queries = [
                    f"blender {current_level} course",
                    f"maya {current_level} tutorial",
                    f"3d modeling {current_level} course",
                    f"texturing {current_level} tutorial",
                    f"rendering {current_level} course"
                ]
            elif "web" in area.lower() or "development" in area.lower():
                base_queries = [
                    f"javascript {current_level} course",
                    f"react {current_level} tutorial",
                    f"web development {current_level} course",
                    f"node.js {current_level} tutorial",
                    f"html css {current_level} course"
                ]
            else:
                base_queries = [
                    f"{area} {current_level} course",
                    f"{area} fundamentals {current_level} tutorial",
                    f"{desired_skills} {area} course",
                    f"{area} basics {current_level} tutorial",
                    f"{area} introduction {current_level} course"
                ]
        elif attempt == 1:
            # Second attempt: broader queries
            if "interior" in area.lower() or "дизайн" in area.lower():
                base_queries = [
                    f"interior design fundamentals course",
                    f"design principles tutorial",
                    f"interior design basics course",
                    f"space planning tutorial",
                    f"design software course"
                ]
            elif "3d" in area.lower() or "artist" in area.lower():
                base_queries = [
                    f"3d modeling fundamentals course",
                    f"digital art basics tutorial",
                    f"3d software course",
                    f"computer graphics tutorial",
                    f"digital design course"
                ]
            elif "web" in area.lower() or "development" in area.lower():
                base_queries = [
                    f"programming fundamentals course",
                    f"web development basics tutorial",
                    f"coding for beginners course",
                    f"software development tutorial",
                    f"computer science course"
                ]
            else:
                base_queries = [
                    f"{area} fundamentals course",
                    f"{area} basics tutorial",
                    f"{area} introduction course",
                    f"{area} for beginners tutorial",
                    f"{area} overview course"
                ]
        else:
            # Third attempt: very broad queries
            if "interior" in area.lower() or "дизайн" in area.lower():
                base_queries = [
                    f"design course",
                    f"interior design tutorial",
                    f"architecture course",
                    f"creative software tutorial",
                    f"visual design course"
                ]
            elif "3d" in area.lower() or "artist" in area.lower():
                base_queries = [
                    f"3d course",
                    f"digital art tutorial",
                    f"computer graphics course",
                    f"creative software tutorial",
                    f"visual arts course"
                ]
            elif "web" in area.lower() or "development" in area.lower():
                base_queries = [
                    f"programming course",
                    f"web development tutorial",
                    f"coding course",
                    f"software tutorial",
                    f"computer science course"
                ]
            else:
                base_queries = [
                    f"{area} course",
                    f"learn {area} tutorial",
                    f"{area} tutorial",
                    f"{area} training course",
                    f"{area} education tutorial"
                ]
        
        logger.info(f"Using fallback queries (attempt {attempt + 1}): {base_queries}")
        return base_queries


deepseek = DeepseekService() 