from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pathlib import Path
import logging

from ..models.schemas import InterviewResponse, InterviewResult
from ..utils.storage import read_json
from ..config import RESULTS_DIR

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/interviews",
    tags=["interviews"],
)

@router.get("", response_model=List[InterviewResponse])
async def list_interviews():
    """
    List all interviews.
    """
    try:
        interviews = []
        for file_path in RESULTS_DIR.glob("*.json"):
            interview_data = read_json(file_path)
            interviews.append({
                "interview_id": interview_data["id"],
                "status": interview_data["status"],
                "candidate_url": f"/interview/{interview_data['id']}"
            })
        return interviews
    except Exception as e:
        logger.error(f"Error listing interviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list interviews: {str(e)}")

@router.get("/{interview_id}", response_model=Dict[str, Any])
async def get_interview(interview_id: str):
    """
    Get detailed information about a specific interview.
    """
    try:
        interview_path = RESULTS_DIR / f"{interview_id}.json"
        if not interview_path.exists():
            raise HTTPException(status_code=404, detail="Interview not found")
        
        interview_data = read_json(interview_path)
        return interview_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting interview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get interview: {str(e)}")

@router.get("/{interview_id}/results", response_model=InterviewResult)
async def get_interview_results(interview_id: str):
    """
    Retrieve the results of a completed interview.
    """
    try:
        interview_path = RESULTS_DIR / f"{interview_id}.json"
        if not interview_path.exists():
            raise HTTPException(status_code=404, detail="Interview not found")
        
        interview_data = read_json(interview_path)
        
        if interview_data["status"] != "completed":
            raise HTTPException(status_code=400, detail="Interview not completed yet")
        
        return {
            "interview_id": interview_id,
            "transcript": interview_data.get("transcript", []),
            "rating": interview_data.get("rating"),
            "verdict": interview_data.get("verdict"),
            "detailed_feedback": interview_data.get("detailed_feedback", {})
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting interview results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get interview results: {str(e)}")