from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Interview(BaseModel):
    """
    Internal model representing an interview's state.
    """
    id: str
    cv_path: str
    jd_path: str
    prompt_path: str
    status: str = "created"
    transcript: List[Dict[str, str]] = []
    questions_asked: int = 0
    max_questions: int
    interviewer_name: str = "AI Interviewer"
    initial_questions: List[str] = []
    rating: Optional[int] = None
    verdict: Optional[str] = None
    detailed_feedback: Optional[Dict[str, Any]] = {}