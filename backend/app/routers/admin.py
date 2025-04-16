from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
import uuid
from pathlib import Path
import logging

from ..models.schemas import InterviewCreate, InterviewResponse, SystemPrompt
from ..utils.storage import save_file, save_json, read_json
from ..services.llm_service import LLMService
from ..config import CV_DIR, JD_DIR, PROMPT_DIR, RESULTS_DIR

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
)

# Initialize LLM service
llm_service = LLMService()

@router.post("/interviews", response_model=InterviewResponse)
async def create_interview(
    cv: UploadFile = File(...),
    jd: UploadFile = File(...),
    system_prompt: str = Form(...),
    interviewer_name: Optional[str] = Form("AI Interviewer"),
    max_questions: Optional[int] = Form(10)
):
    """
    Create a new interview session with uploaded CV and job description.
    """
    try:
        # Generate unique ID for the interview
        interview_id = str(uuid.uuid4())
        
        # Save uploaded files
        cv_path = await save_file(cv, CV_DIR / f"{interview_id}.pdf")
        jd_path = await save_file(jd, JD_DIR / f"{interview_id}.pdf")
        
        # Save system prompt
        prompt_data = {
            "system_prompt": system_prompt,
            "interviewer_name": interviewer_name,
            "max_questions": max_questions
        }
        prompt_path = save_json(prompt_data, PROMPT_DIR / f"{interview_id}.json")
        
        # Prepare initial interview data
        interview_data = {
            "id": interview_id,
            "cv_path": str(cv_path),
            "jd_path": str(jd_path),
            "prompt_path": str(prompt_path),
            "status": "created",
            "transcript": [],
            "questions_asked": 0,
            "max_questions": max_questions,
            "interviewer_name": interviewer_name
        }
        
        # Save interview data
        save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        # Initialize interview with LLM
        initial_questions = await llm_service.generate_initial_questions(
            cv_path=str(cv_path),
            jd_path=str(jd_path),
            system_prompt=system_prompt,
            max_questions=max_questions
        )
        
        # Update interview data with initial questions
        interview_data["initial_questions"] = initial_questions
        save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        return {
            "interview_id": interview_id,
            "status": "created",
            "candidate_url": f"/interview/{interview_id}"
        }
        
    except Exception as e:
        logger.error(f"Error creating interview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create interview: {str(e)}")

@router.post("/interviews/{interview_id}/system-prompt")
async def update_system_prompt(interview_id: str, prompt: SystemPrompt):
    """
    Update the system prompt for an existing interview.
    """
    try:
        interview_path = RESULTS_DIR / f"{interview_id}.json"
        if not interview_path.exists():
            raise HTTPException(status_code=404, detail="Interview not found")
        
        interview_data = read_json(interview_path)
        if interview_data["status"] != "created":
            raise HTTPException(status_code=400, detail="Cannot update prompt for an active or completed interview")
        
        # Update prompt data
        prompt_data = {
            "system_prompt": prompt.system_prompt,
            "interviewer_name": prompt.interviewer_name or interview_data["interviewer_name"],
            "max_questions": prompt.max_questions or interview_data["max_questions"]
        }
        save_json(prompt_data, PROMPT_DIR / f"{interview_id}.json")
        
        # Regenerate initial questions with new prompt
        initial_questions = await llm_service.generate_initial_questions(
            cv_path=interview_data["cv_path"],
            jd_path=interview_data["jd_path"],
            system_prompt=prompt.system_prompt,
            max_questions=prompt_data["max_questions"]
        )
        
        interview_data["initial_questions"] = initial_questions
        interview_data["max_questions"] = prompt_data["max_questions"]
        interview_data["interviewer_name"] = prompt_data["interviewer_name"]
        save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        return {"message": "System prompt updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating system prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update system prompt: {str(e)}")