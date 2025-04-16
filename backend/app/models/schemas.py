# backend/app/models/schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union

class InterviewCreate(BaseModel):
    """Request model for creating a new interview"""
    system_prompt: str
    interviewer_name: Optional[str] = "AI Interviewer"
    max_questions: Optional[int] = 10

class InterviewResponse(BaseModel):
    """Response model for interview operations"""
    interview_id: str
    status: str
    candidate_url: str

class SystemPrompt(BaseModel):
    """System prompt model"""
    system_prompt: str
    interviewer_name: Optional[str] = "AI Interviewer"
    max_questions: Optional[int] = 10

class TranscriptEntry(BaseModel):
    """Single entry in the interview transcript"""
    speaker: str  # "ai" or "candidate"
    text: str

class InterviewResult(BaseModel):
    """Interview results model"""
    interview_id: str
    transcript: List[Dict[str, str]]
    rating: int
    verdict: str
    detailed_feedback: Optional[Dict[str, Any]] = {}

class AudioRequest(BaseModel):
    """Request model for audio data"""
    audio_data: str  # Base64 encoded audio data

class TextResponse(BaseModel):
    """Response model for text data"""
    text: str

class LiveKitTokenRequest(BaseModel):
    """Request model for LiveKit token"""
    interview_id: str
    participant_name: str