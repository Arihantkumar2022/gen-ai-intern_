import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routers
from routers import admin_router, candidate_router, interviews_router

# Import services
from services.llm_service import LLMService
from services.stt_service import STTService
from services.tts_service import TTSService
from services.livekit_service import LiveKitService

# Import utils and config
from utils.storage import save_file, read_file, save_json, read_json
from config import RESULTS_DIR, PROMPT_DIR

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Interviewer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_router)
app.include_router(candidate_router)
app.include_router(interviews_router)

# Initialize services
llm_service = LLMService()
stt_service = STTService()
tts_service = TTSService()
livekit_service = LiveKitService()

# Store active interview connections
active_interviews = {}

# Helper function to get interview data
def get_interview_data(interview_id: str):
    interview_path = RESULTS_DIR / f"{interview_id}.json"
    if not interview_path.exists():
        raise HTTPException(status_code=404, detail="Interview not found")
    return read_json(interview_path)

# WebSocket for the interview session
@app.websocket("/api/ws/interview/{interview_id}")
async def interview_websocket(websocket: WebSocket, interview_id: str):
    await websocket.accept()
    
    try:
        # Get interview data
        interview_data = get_interview_data(interview_id)
        
        if interview_data["status"] == "completed":
            await websocket.send_json({"type": "error", "message": "Interview already completed"})
            await websocket.close()
            return
        
        # Update interview status
        interview_data["status"] = "in_progress"
        save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        # Add to active interviews
        active_interviews[interview_id] = websocket
        
        # Get system prompt and initial questions
        prompt_data = read_json(PROMPT_DIR / f"{interview_id}.json")
        system_prompt = prompt_data["system_prompt"]
        interviewer_name = prompt_data.get("interviewer_name", "AI Interviewer")
        
        # Get initial questions if available, or generate them
        initial_questions = interview_data.get("initial_questions", [])
        if not initial_questions:
            cv_path = interview_data["cv_path"]
            jd_path = interview_data["jd_path"]
            
            initial_questions = await llm_service.generate_initial_questions(
                cv_path=cv_path,
                jd_path=jd_path,
                system_prompt=system_prompt,
                max_questions=interview_data["max_questions"]
            )
            
            interview_data["initial_questions"] = initial_questions
            save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        # Send greeting
        greeting = f"Hello, I'm {interviewer_name}. Thank you for joining this interview. I'll be asking you some questions to learn more about your skills and experience."
        
        # Convert greeting to speech
        audio_url = await tts_service.text_to_speech(greeting)
        
        # Send greeting to candidate
        await websocket.send_json({
            "type": "greeting",
            "text": greeting,
            "audio_url": audio_url
        })
        
        # Update transcript
        transcript = interview_data.get("transcript", [])
        transcript.append({"speaker": "ai", "text": greeting})
        interview_data["transcript"] = transcript
        save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        # Start with first question
        if initial_questions:
            first_question = initial_questions[0]
            audio_url = await tts_service.text_to_speech(first_question)
            
            await websocket.send_json({
                "type": "question",
                "text": first_question,
                "audio_url": audio_url,
                "question_number": 1
            })
            
            # Update transcript and question count
            transcript.append({"speaker": "ai", "text": first_question})
            interview_data["transcript"] = transcript
            interview_data["questions_asked"] = 1
            save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        # Main interview loop
        while True:
            # Wait for candidate response
            message = await websocket.receive_json()
            
            if message["type"] == "response":
                # Process candidate audio response
                audio_data = message.get("audio_data")
                if audio_data:
                    # Transcribe audio using STT
                    candidate_response = await stt_service.speech_to_text(audio_data)
                else:
                    # If text response provided directly
                    candidate_response = message.get("text", "")
                
                # Update transcript
                transcript.append({"speaker": "candidate", "text": candidate_response})
                interview_data["transcript"] = transcript
                
                # Check if we've reached max questions
                current_question = interview_data["questions_asked"]
                max_questions = interview_data["max_questions"]
                
                if current_question >= max_questions:
                    # Complete the interview
                    await complete_interview(interview_id, websocket)
                    break
                
                # Generate next question
                next_question = await llm_service.generate_follow_up_question(
                    transcript=transcript,
                    system_prompt=system_prompt,
                    cv_path=interview_data["cv_path"],
                    jd_path=interview_data["jd_path"]
                )
                
                # Convert question to speech
                audio_url = await tts_service.text_to_speech(next_question)
                
                # Send question to candidate
                await websocket.send_json({
                    "type": "question",
                    "text": next_question,
                    "audio_url": audio_url,
                    "question_number": current_question + 1
                })
                
                # Update transcript and question count
                transcript.append({"speaker": "ai", "text": next_question})
                interview_data["transcript"] = transcript
                interview_data["questions_asked"] = current_question + 1
                save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
                
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from interview {interview_id}")
        if interview_id in active_interviews:
            del active_interviews[interview_id]
    except Exception as e:
        logger.error(f"Error in interview websocket: {str(e)}")
        await websocket.send_json({"type": "error", "message": f"Error: {str(e)}"})
        await websocket.close()
        if interview_id in active_interviews:
            del active_interviews[interview_id]

async def complete_interview(interview_id: str, websocket: WebSocket):
    """
    Complete the interview and generate results
    """
    try:
        # Get interview data
        interview_data = get_interview_data(interview_id)
        transcript = interview_data.get("transcript", [])
        
        # Generate final assessment using LLM
        assessment = await llm_service.generate_final_assessment(
            transcript=transcript,
            cv_path=interview_data["cv_path"],
            jd_path=interview_data["jd_path"]
        )
        
        # Update interview data with results
        interview_data["status"] = "completed"
        interview_data["rating"] = assessment.get("rating")
        interview_data["verdict"] = assessment.get("verdict")
        interview_data["detailed_feedback"] = assessment.get("detailed_feedback")
        save_json(interview_data, RESULTS_DIR / f"{interview_id}.json")
        
        # Send completion message
        completion_message = "Thank you for completing this interview. Your responses have been recorded."
        audio_url = await tts_service.text_to_speech(completion_message)
        
        await websocket.send_json({
            "type": "completion",
            "text": completion_message,
            "audio_url": audio_url
        })
        
        # If immediate feedback is enabled, send it to candidate
        await websocket.send_json({
            "type": "results",
            "rating": assessment.get("rating"),
            "verdict": assessment.get("verdict")
        })
        
        # Close the connection
        await websocket.close()
        
        # Remove from active interviews
        if interview_id in active_interviews:
            del active_interviews[interview_id]
            
    except Exception as e:
        logger.error(f"Error completing interview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to complete interview: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)