from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
import logging

from app.models.roadmap import RoadmapRequest, RoadmapResponse, ChatMessage, ChatResponse
from app.services.roadmap_service import roadmap_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])

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