import json
import logging
from typing import List, Dict, Any
from app.utils import call_deepseek
from app.services import encoder, qdrant
from app.models.roadmap import RoadmapResponse, LearningStep, SkillNode

logger = logging.getLogger(__name__)

class RoadmapService:
    def __init__(self):
        self.system_prompt = """You are an expert learning path designer. Your job is to:
1. Analyze user learning goals and create structured learning paths
2. Break down complex skills into manageable sub-skills
3. Create step-by-step learning roadmaps with realistic time estimates
4. Provide clear progression paths from beginner to advanced levels
5. Generate contextual questions to guide users through the learning path discovery process
6. Generate multiple search queries to find relevant courses

Always respond in JSON format for structured data."""

    async def generate_search_prompts(self, area: str, current_level: str, desired_outcome: str) -> List[Dict[str, str]]:
        """Generate 5 different search prompts based on user goals"""
        try:
            prompt = f"""
            Based on the user's learning goals, generate 5 different search queries to find relevant courses.
            
            User Information:
            - Learning Area: {area}
            - Current Level: {current_level}
            - Desired Outcome: {desired_outcome}
            
            Generate 5 different search queries that cover:
            1. Core fundamentals and basics
            2. Intermediate skills and techniques
            3. Advanced concepts and specialization
            4. Practical applications and tools
            5. Industry-specific knowledge
            
            Each query should be different and focus on specific aspects needed to reach the goal.
            
            Return as JSON array:
            [
                {{
                    "prompt": "search query text",
                    "description": "what this search focuses on",
                    "category": "basics|intermediate|advanced|practical|industry"
                }},
                ...
            ]
            
            Example for Product Management:
            [
                {{
                    "prompt": "product management basics fundamentals",
                    "description": "Core PM concepts and fundamentals",
                    "category": "basics"
                }},
                {{
                    "prompt": "market analysis competitive research",
                    "description": "Market research and competitive analysis skills",
                    "category": "intermediate"
                }},
                {{
                    "prompt": "unit economics business metrics",
                    "description": "Business metrics and unit economics",
                    "category": "advanced"
                }},
                {{
                    "prompt": "SQL data analysis product metrics",
                    "description": "Data analysis and SQL for product managers",
                    "category": "practical"
                }},
                {{
                    "prompt": "agile scrum product development",
                    "description": "Agile methodologies and product development",
                    "category": "industry"
                }}
            ]
            """
            
            response = call_deepseek(prompt, self.system_prompt)
            if response.strip().startswith('['):
                return json.loads(response)
            else:
                # Fallback prompts
                return [
                    {
                        "prompt": f"{area} {current_level} basics fundamentals",
                        "description": "Основы и фундаментальные концепции",
                        "category": "basics"
                    },
                    {
                        "prompt": f"{area} {current_level} intermediate skills",
                        "description": "Промежуточные навыки и техники",
                        "category": "intermediate"
                    },
                    {
                        "prompt": f"{area} {current_level} advanced concepts",
                        "description": "Продвинутые концепции и специализация",
                        "category": "advanced"
                    },
                    {
                        "prompt": f"{area} {current_level} practical tools applications",
                        "description": "Практические инструменты и приложения",
                        "category": "practical"
                    },
                    {
                        "prompt": f"{area} {current_level} industry specific",
                        "description": "Отраслевые знания и специфика",
                        "category": "industry"
                    }
                ]
                
        except Exception as e:
            logger.error(f"Error generating search prompts: {e}")
            # Fallback prompts
            return [
                {
                    "prompt": f"{area} {current_level} basics",
                    "description": "Основы",
                    "category": "basics"
                },
                {
                    "prompt": f"{area} {current_level} intermediate",
                    "description": "Средний уровень",
                    "category": "intermediate"
                },
                {
                    "prompt": f"{area} {current_level} advanced",
                    "description": "Продвинутый уровень",
                    "category": "advanced"
                },
                {
                    "prompt": f"{area} {current_level} practical",
                    "description": "Практика",
                    "category": "practical"
                },
                {
                    "prompt": f"{area} {current_level} industry",
                    "description": "Отраслевые знания",
                    "category": "industry"
                }
            ]

    async def search_courses_with_multiple_prompts(self, area: str, current_level: str, desired_outcome: str) -> Dict[str, Any]:
        """Search courses using multiple AI-generated prompts"""
        try:
            # Generate search prompts
            search_prompts = await self.generate_search_prompts(area, current_level, desired_outcome)
            
            # Search for courses using each prompt
            search_results = []
            
            for prompt_data in search_prompts:
                try:
                    # Vectorize the search prompt
                    vector = await encoder.vectorize(prompt_data["prompt"])
                    
                    # Search in Qdrant
                    qdrant_results = await qdrant.search(vector, "courses", limit=5)
                    
                    # Format results
                    courses = [course.payload for course in qdrant_results]
                    
                    search_results.append({
                        "prompt": prompt_data["prompt"],
                        "description": prompt_data["description"],
                        "category": prompt_data["category"],
                        "courses": courses,
                        "courses_count": len(courses)
                    })
                    
                    logger.info(f"Search prompt '{prompt_data['prompt']}' found {len(courses)} courses")
                    
                except Exception as e:
                    logger.error(f"Error searching with prompt '{prompt_data['prompt']}': {e}")
                    search_results.append({
                        "prompt": prompt_data["prompt"],
                        "description": prompt_data["description"],
                        "category": prompt_data["category"],
                        "courses": [],
                        "courses_count": 0,
                        "error": str(e)
                    })
            
            return {
                "search_prompts": search_prompts,
                "search_results": search_results,
                "total_courses_found": sum(result["courses_count"] for result in search_results)
            }
            
        except Exception as e:
            logger.error(f"Error in multiple prompt search: {e}")
            raise

    async def generate_next_question(self, conversation_history: List[Dict[str, str]], current_step: int) -> str:
        """Generate the next contextual question based on conversation history"""
        try:
            # Create context from conversation history
            context = ""
            for i, msg in enumerate(conversation_history):
                context += f"Step {i+1}: {msg.get('question', '')} - User: {msg.get('answer', '')}\n"
            
            prompt = f"""
            Based on this conversation history:
            {context}
            
            Current step: {current_step}
            
            Generate the next contextual question to gather information needed for creating a personalized learning roadmap.
            
            Rules:
            1. If this is step 1 (no history): Ask "Доброго времени суток! Что бы вы хотели освоить?"
            2. If step 2: Ask "Какой у вас уже уровень в этой области?"
            3. If step 3: Ask "Какой ваш желаемый итог? Что вы хотите достичь?"
            4. Make questions contextual and personalized based on previous answers
            5. Keep questions clear, friendly, and specific
            
            Return only the question text, no JSON formatting.
            """
            
            response = call_deepseek(prompt, self.system_prompt)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating next question: {e}")
            # Fallback questions
            fallback_questions = [
                "Доброго времени суток! Что бы вы хотели освоить?",
                "Какой у вас уже уровень в этой области?",
                "Какой ваш желаемый итог? Что вы хотите достичь?",
                "Отлично! Теперь я создам для вас персональный план обучения."
            ]
            return fallback_questions[min(current_step - 1, len(fallback_questions) - 1)]

    async def analyze_user_response(self, question: str, user_answer: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze user response and extract relevant information"""
        try:
            prompt = f"""
            Analyze this user response to the question: "{question}"
            User answer: "{user_answer}"
            
            Previous conversation context:
            {json.dumps(conversation_history, ensure_ascii=False, indent=2)}
            
            Extract and structure the information:
            1. Learning area/domain (if mentioned) - this is the most important field
            2. Current skill level (if mentioned)
            3. Desired outcome/goal (if mentioned)
            4. Any additional context that could help with roadmap generation
            
            IMPORTANT: If the user mentions a learning area (like "marketing", "programming", "design", etc.), 
            make sure to extract it correctly in the "area" field.
            
            Return as JSON:
            {{
                "extracted_info": {{
                    "area": "extracted area or null",
                    "level": "extracted level or null", 
                    "outcome": "extracted desired outcome or null",
                    "context": "additional context"
                }},
                "confidence": 0.0-1.0,
                "needs_clarification": true/false,
                "clarification_question": "if needs clarification, what to ask"
            }}
            """
            
            response = call_deepseek(prompt, self.system_prompt)
            if response.strip().startswith('{'):
                result = json.loads(response)
                
                # Additional validation for area extraction
                if not result.get("extracted_info", {}).get("area") and user_answer.strip():
                    # If AI didn't extract area but user provided an answer, use the answer as area
                    result["extracted_info"]["area"] = user_answer.strip()
                    result["confidence"] = 0.8
                
                return result
            else:
                # Fallback analysis - improved to better extract area
                area = None
                level = None
                outcome = None
                
                # Simple keyword-based extraction
                answer_lower = user_answer.lower()
                question_lower = question.lower()
                
                # Extract area if this is the first question or if user mentions a learning area
                if "освоить" in question_lower or "область" in question_lower or "что" in question_lower:
                    area = user_answer.strip()
                elif any(keyword in answer_lower for keyword in ["маркетинг", "программирование", "дизайн", "менеджмент", "аналитика", "продажи"]):
                    area = user_answer.strip()
                
                # Extract level
                if "уровень" in question_lower:
                    level = user_answer.strip()
                elif any(keyword in answer_lower for keyword in ["начинающий", "средний", "продвинутый", "новичок", "опытный"]):
                    level = user_answer.strip()
                
                # Extract outcome
                if "итог" in question_lower or "достичь" in question_lower:
                    outcome = user_answer.strip()
                
                return {
                    "extracted_info": {
                        "area": area,
                        "level": level,
                        "outcome": outcome,
                        "context": user_answer
                    },
                    "confidence": 0.7,
                    "needs_clarification": False,
                    "clarification_question": None
                }
                
        except Exception as e:
            logger.error(f"Error analyzing user response: {e}")
            # Improved fallback - use user answer as area if it's the first response
            return {
                "extracted_info": {
                    "area": user_answer.strip() if user_answer.strip() else None,
                    "level": None,
                    "outcome": None,
                    "context": user_answer
                },
                "confidence": 0.5,
                "needs_clarification": False,
                "clarification_question": None
            }

    async def analyze_input(self, input_text: str) -> List[str]:
        """Extract main learning goals or skills from user input"""
        prompt = f"""
        Extract the main learning goals or skills from: '{input_text}'.
        Return a JSON array of 3-5 key skills or areas to focus on.
        Example: ["Python Programming", "Data Analysis", "Machine Learning"]
        """
        
        try:
            response = call_deepseek(prompt, self.system_prompt)
            # Try to parse JSON response
            if response.strip().startswith('['):
                return json.loads(response)
            else:
                # Fallback: extract skills from text
                skills = [skill.strip() for skill in response.split(',')]
                return skills[:5]  # Limit to 5 skills
        except Exception as e:
            logger.error(f"Error analyzing input: {e}")
            return [input_text]

    async def generate_subskills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Generate sub-skills for each main skill"""
        prompt = f"""
        For each of these skills: {skills}, list 2-3 important sub-skills.
        Return as JSON object where keys are main skills and values are arrays of sub-skills.
        Example: {{"Python Programming": ["Basic Syntax", "Functions", "OOP"]}}
        """
        
        try:
            response = call_deepseek(prompt, self.system_prompt)
            if response.strip().startswith('{'):
                return json.loads(response)
            else:
                # Fallback: create simple mapping
                return {skill: [f"{skill} Basics", f"{skill} Advanced"] for skill in skills}
        except Exception as e:
            logger.error(f"Error generating subskills: {e}")
            return {skill: [f"{skill} Basics"] for skill in skills}

    async def create_learning_steps(self, skills: Dict[str, List[str]], current_level: str) -> List[LearningStep]:
        """Create structured learning steps from skills"""
        steps = []
        step_number = 1
        
        for main_skill, sub_skills in skills.items():
            # Create skill nodes for this step
            skill_nodes = []
            for sub_skill in sub_skills:
                skill_node = SkillNode(
                    skill=sub_skill,
                    sub_skills=[],  # Could be expanded further
                    difficulty=self._determine_difficulty(current_level, step_number),
                    estimated_time=f"{2-4} weeks",
                    prerequisites=[]
                )
                skill_nodes.append(skill_node)
            
            # Create learning step
            step = LearningStep(
                step_number=step_number,
                title=f"Master {main_skill}",
                description=f"Learn the fundamentals and advanced concepts of {main_skill}",
                skills=skill_nodes,
                estimated_duration=f"{len(sub_skills) * 2-4} weeks",
                difficulty=self._determine_difficulty(current_level, step_number)
            )
            steps.append(step)
            step_number += 1
        
        return steps

    def _determine_difficulty(self, current_level: str, step_number: int) -> str:
        """Determine difficulty based on current level and step progression"""
        if current_level.lower() in ['beginner', 'начальный']:
            if step_number == 1:
                return "Beginner"
            elif step_number <= 3:
                return "Intermediate"
            else:
                return "Advanced"
        elif current_level.lower() in ['intermediate', 'средний']:
            if step_number == 1:
                return "Intermediate"
            else:
                return "Advanced"
        else:
            return "Advanced"

    async def search_courses_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Search for courses that match the skills"""
        try:
            # Combine all skills into a search query
            query_text = " ".join(skills)
            vector = await encoder.vectorize(query_text)
            results = [course.payload for course in await qdrant.search(vector, "courses")]
            
            # Limit to top 10 courses
            return results[:10]
        except Exception as e:
            logger.error(f"Error searching courses for skills: {e}")
            return []

    async def generate_roadmap(self, area: str, current_level: str, desired_skills: str, include_courses: bool = True) -> RoadmapResponse:
        """Generate a complete learning roadmap"""
        try:
            # Analyze input to extract skills
            input_text = f"{area} {desired_skills}"
            skills = await self.analyze_input(input_text)
            
            # Generate sub-skills
            skills_with_subskills = await self.generate_subskills(skills)
            
            # Create learning steps
            steps = await self.create_learning_steps(skills_with_subskills, current_level)
            
            # Search for relevant courses if requested
            courses = None
            if include_courses:
                all_skills = [skill for sublist in skills_with_subskills.values() for skill in sublist]
                courses = await self.search_courses_for_skills(all_skills)
            
            # Calculate total estimated time
            total_weeks = sum(len(step.skills) * 3 for step in steps)  # Rough estimate
            
            roadmap = RoadmapResponse(
                title=f"Learning Path: {area}",
                description=f"Complete roadmap to master {area} from {current_level} level",
                total_estimated_time=f"{total_weeks} weeks",
                difficulty_progression=f"{current_level} → Advanced",
                steps=steps,
                courses=courses
            )
            
            return roadmap
            
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            raise

# Global instance
roadmap_service = RoadmapService() 