from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from pathlib import Path
import logging

from ..services.livekit_service import LiveKitService
from ..utils.storage import read_json
from ..config import RESULTS_DIR

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/candidate",
    tags=["candidate"],
)

# Initialize LiveKit service
livekit_service = LiveKitService()

@router.get("/interviews/{interview_id}/join", response_model=Dict[str, Any])
async def join_interview(interview_id: str):
    """
    Retrieve interview details for a candidate to join.
    """
    try:
        interview_path = RESULTS_DIR / f"{interview_id}.json"
        if not interview_path.exists():
            raise HTTPException(status_code=404, detail="Interview not found")
        
        interview_data = read_json(interview_path)
        
        return {
            "interview_id": interview_data["id"],
            "status": interview_data["status"],
            "interviewer_name": interview_data.get("interviewer_name", "AI Interviewer")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error joining interview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to join interview: {str(e)}")

@router.post("/interviews/{interview_id}/livekit-token")
async def get_livekit_token(interview_id: str, participant_name: str):
    """
    Generate a LiveKit token for the candidate to join the interview room.
    """
    try:
        interview_path = RESULTS_DIR / f"{interview_id}.json"
        if not interview_path.exists():
            raise HTTPException(status_code=404, detail="Interview not found")
        
        token = livekit_service.create_token(
            room_name=f"interview-{interview_id}",
            participant_name=participant_name
        )
        
        if not token:
            raise HTTPException(status_code=500, detail="Failed to generate LiveKit token")
        
        return {"token": token}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating LiveKit token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")