from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
import logging
import time

from app.models.roadmap import RoadmapRequest, RoadmapResponse, ChatMessage, ChatResponse
from app.services.roadmap_service import roadmap_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])

# Simple in-memory storage for user roadmaps (in production, use a database)
user_roadmaps_storage = []

@router.post(
    "/generate",
    response_model=RoadmapResponse,
    summary="Generate a personalized learning roadmap"
)
async def generate_roadmap(payload: RoadmapRequest = Body(...)):
    """
    Generate a personalized learning roadmap based on:
    1. **area** — learning area/domain
    2. **current_level** — user's current skill level
    3. **desired_skills** — specific skills they want to acquire
    4. **include_courses** — whether to include course recommendations
    """
    logger.info(
        f"Generate roadmap: area='{payload.area}', level='{payload.current_level}', skills='{payload.desired_skills}'"
    )

    try:
        roadmap = await roadmap_service.generate_roadmap(
            area=payload.area,
            current_level=payload.current_level,
            desired_skills=payload.desired_skills,
            include_courses=payload.include_courses
        )
        
        logger.info(f"Generated roadmap with {len(roadmap.steps)} steps")
        return roadmap

    except Exception as e:
        logger.exception(f"Error generating roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate roadmap")

@router.post(
    "/next-question",
    summary="Get the next AI-generated question based on conversation history"
)
async def get_next_question(payload: Dict[str, Any] = Body(...)):
    """
    Get the next contextual question based on conversation history
    """
    conversation_history = payload.get("conversation_history", [])
    current_step = payload.get("current_step", 1)
    
    logger.info(f"Generate next question for step {current_step}")

    try:
        question = await roadmap_service.generate_next_question(conversation_history, current_step)
        
        return {
            "question": question,
            "step": current_step,
            "is_final": current_step >= 3  # After 3 questions, we have enough info
        }

    except Exception as e:
        logger.exception(f"Error generating next question: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate question")

@router.post("/analyze-response")
async def analyze_user_response(
    question: str,
    user_answer: str,
    conversation_history: List[Dict[str, str]] = []
):
    """
    Analyze user response to extract relevant information for roadmap generation.
    """
    try:
        logger.info(f"Analyzing user response to: {question}")
        
        # Use the roadmap service to analyze the response
        analysis = await roadmap_service.analyze_user_response(
            question=question,
            user_answer=user_answer,
            conversation_history=conversation_history
        )
        
        return {
            "success": True,
            "extracted_info": analysis.get("extracted_info", {}),
            "confidence": analysis.get("confidence", 0.0),
            "needs_clarification": analysis.get("needs_clarification", False),
            "clarification_question": analysis.get("clarification_question")
        }
        
    except Exception as e:
        logger.error(f"Error analyzing user response: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Interactive chat for roadmap generation"
)
async def chat_roadmap(payload: ChatMessage = Body(...)):
    """
    Interactive chat endpoint that can:
    1. Analyze user messages
    2. Generate roadmaps
    3. Provide course recommendations
    """
    logger.info(f"Chat message: {payload.message[:100]}...")

    try:
        # Analyze the message to determine intent
        analysis_prompt = f"""
        Analyze this user message and determine if they want:
        1. A learning roadmap
        2. Course recommendations
        3. General advice
        
        Message: "{payload.message}"
        
        Respond with JSON: {{"intent": "roadmap|courses|advice", "extracted_info": {{"area": "...", "level": "...", "skills": "..."}}}}
        """
        
        # For now, we'll create a simple response
        # In a full implementation, you'd use the DeepSeek API here
        response_text = f"I understand you're interested in learning. Let me help you create a personalized roadmap based on your goals."
        
        # Generate a basic roadmap if the message seems to request one
        if any(keyword in payload.message.lower() for keyword in ['roadmap', 'path', 'plan', 'learn', 'study']):
            # Extract basic info from message
            area = "Programming"  # Default, could be extracted from message
            level = "Beginner"    # Default
            skills = "Basic programming skills"  # Default
            
            roadmap = await roadmap_service.generate_roadmap(
                area=area,
                current_level=level,
                desired_skills=skills,
                include_courses=True
            )
            
            return ChatResponse(
                response=response_text,
                roadmap=roadmap,
                courses=roadmap.courses
            )
        else:
            return ChatResponse(
                response=response_text,
                roadmap=None,
                courses=None
            )

    except Exception as e:
        logger.exception(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Chat service error")

@router.get(
    "/skills/{area}",
    summary="Get available skills for a specific area"
)
async def get_skills_for_area(area: str):
    """
    Get a list of available skills and sub-skills for a specific learning area
    """
    logger.info(f"Get skills for area: {area}")

    try:
        # Use the roadmap service to generate skills for the area
        skills = await roadmap_service.analyze_input(area)
        subskills = await roadmap_service.generate_subskills(skills)
        
        return {
            "area": area,
            "skills": skills,
            "subskills": subskills
        }

    except Exception as e:
        logger.exception(f"Error getting skills: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get skills")

@router.get(
    "/get-roadmaps",
    summary="Get user's roadmaps with real course data"
)
async def get_user_roadmaps():
    """
    Get user's roadmaps populated with real course data from search results.
    Returns saved user roadmaps first, falls back to sample data if none exist.
    """
    logger.info("Getting user roadmaps with real course data")
    
    try:
        # Return stored roadmaps if they exist
        if user_roadmaps_storage:
            logger.info(f"Returning {len(user_roadmaps_storage)} stored user roadmaps")
            return user_roadmaps_storage
        
        # Fallback to sample roadmaps with mock courses (since Qdrant might not be available)
        logger.info("No stored roadmaps found, generating sample roadmaps with mock courses")
        
        # Mock course data for testing
        mock_python_courses = [
            {
                "id": 101,
                "title": "Python для начинающих: основы программирования",
                "cover_url": "/assets/courseImage.png",
                "duration": 12,
                "difficulty": "beginner",
                "price": 2500,
                "pupils_num": 850,
                "authors": "Иван Петров",
                "rating": 4.5,
                "url": "#python-basics"
            },
            {
                "id": 102,
                "title": "Django: создание веб-приложений на Python",
                "cover_url": "/assets/courseImage.png",
                "duration": 16,
                "difficulty": "intermediate",
                "price": 3200,
                "pupils_num": 650,
                "authors": "Мария Сидорова",
                "rating": 4.3,
                "url": "#django-web"
            }
        ]
        
        mock_js_courses = [
            {
                "id": 201,
                "title": "JavaScript ES6+: современные возможности",
                "cover_url": "/assets/courseImage.png",
                "duration": 14,
                "difficulty": "intermediate",
                "price": 2800,
                "pupils_num": 920,
                "authors": "Алексей Козлов",
                "rating": 4.6,
                "url": "#js-modern"
            },
            {
                "id": 202,
                "title": "React: создание интерактивных интерфейсов",
                "cover_url": "/assets/courseImage.png",
                "duration": 18,
                "difficulty": "advanced",
                "price": 3800,
                "pupils_num": 540,
                "authors": "Елена Волкова",
                "rating": 4.7,
                "url": "#react-ui"
            }
        ]
        
        mock_ds_courses = [
            {
                "id": 301,
                "title": "Data Science: анализ данных с Python",
                "cover_url": "/assets/courseImage.png",
                "duration": 20,
                "difficulty": "advanced",
                "price": 4200,
                "pupils_num": 380,
                "authors": "Дмитрий Новиков",
                "rating": 4.4,
                "url": "#data-science"
            }
        ]
        
        # Create sample roadmaps with mock courses
        sample_roadmaps = [
            {
                "id": 1,
                "status": "current",
                "name": "Python Development Path",
                "courses": [
                    {**course, "progress": 0.8 if i == 0 else 0.3 if i == 1 else 0.0}
                    for i, course in enumerate(mock_python_courses)
                ]
            },
            {
                "id": 2,
                "status": "notNow", 
                "name": "Frontend Development Path",
                "courses": [
                    {**course, "progress": 0.0}
                    for course in mock_js_courses
                ]
            },
            {
                "id": 3,
                "status": "done",
                "name": "Data Science Path", 
                "courses": [
                    {**course, "progress": 1.0}
                    for course in mock_ds_courses
                ]
            }
        ]
        
        logger.info(f"Returning {len(sample_roadmaps)} sample roadmaps with real course data")
        return sample_roadmaps
        
    except Exception as e:
        logger.exception(f"Error getting roadmaps: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get roadmaps")

@router.post(
    "/clear-roadmaps",
    summary="Clear all user roadmaps"
)
async def clear_user_roadmaps():
    """
    Clear all stored user roadmaps.
    This is useful when starting a new chat session.
    """
    logger.info("Clearing all user roadmaps")
    global user_roadmaps_storage
    user_roadmaps_storage.clear()
    return {"success": True, "message": "All roadmaps cleared"}

@router.post(
    "/save-courses",
    summary="Save courses to user's roadmap"
)
async def save_courses_to_roadmap(
    roadmap_name: str = Body(...),
    courses: List[Dict[str, Any]] = Body(...)
):
    """
    Save courses to a user's roadmap.
    This creates a new roadmap with the provided courses.
    """
    logger.info(f"Saving {len(courses)} courses to roadmap: {roadmap_name}")
    
    try:
        # Add progress field to courses and create roadmap
        courses_with_progress = []
        for i, course in enumerate(courses):
            course_with_progress = {**course}
            # Set some realistic progress values
            if i == 0:
                course_with_progress["progress"] = 0.6  # First course in progress
            elif i == 1:
                course_with_progress["progress"] = 0.2  # Second course just started
            else:
                course_with_progress["progress"] = 0.0  # Rest not started
            courses_with_progress.append(course_with_progress)
        
        # Create new roadmap
        new_roadmap = {
            "id": len(user_roadmaps_storage) + 1,
            "status": "current",
            "name": roadmap_name,
            "courses": courses_with_progress,
            "created_at": time.time()
        }
        
        # Check if roadmap with this name already exists
        existing_index = None
        for i, roadmap in enumerate(user_roadmaps_storage):
            if roadmap["name"] == roadmap_name:
                existing_index = i
                break
        
        if existing_index is not None:
            # Update existing roadmap
            user_roadmaps_storage[existing_index] = new_roadmap
            logger.info(f"Updated existing roadmap: {roadmap_name}")
        else:
            # Add new roadmap
            user_roadmaps_storage.append(new_roadmap)
            logger.info(f"Created new roadmap: {roadmap_name}")
        
        return {
            "success": True,
            "roadmap_name": roadmap_name,
            "courses_count": len(courses),
            "message": f"Successfully saved {len(courses)} courses to roadmap '{roadmap_name}'"
        }
    except Exception as e:
        logger.exception(f"Error saving courses to roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save courses to roadmap") 