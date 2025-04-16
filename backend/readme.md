# AI Interviewer

A full-stack application that simulates voice-based AI interviews. The system uses Text-to-Speech (TTS) to ask questions, Speech-to-Text (STT) to transcribe candidate responses, and a Language Model (GPT-4) to provide context-driven follow-up questions and rate candidates.

## System Architecture

### Overview

The AI Interviewer follows a client-server architecture with these key components:

1. **Frontend**
   - **Admin Dashboard**: For uploading CVs, job descriptions, configuring interviews, and reviewing results (React, TypeScript, Vite).
   - **Candidate Interface**: For participating in interviews with real-time audio (React, TypeScript, Vite, LiveKit).

2. **Backend**
   - Python FastAPI server handling API requests and WebSocket connections.
   - API endpoints for interview management, file uploads, and real-time orchestration.

3. **External Services**
   - **LiveKit**: For real-time audio communication.
   - **OpenAI GPT-4**: For question generation and candidate evaluation.
   - **Deepgram**: For Speech-to-Text transcription.
   - **ElevenLabs**: For Text-to-Speech conversion.

4. **Local Storage**
   - File system storage for CVs, job descriptions, prompts, transcripts, results, and audio files.
   - Stored in `backend/data/` with subdirectories: `cv`, `jd`, `prompts`, `transcripts`, `results`, `audio`.

### System Flow Diagram
┌─────────────────┐                   ┌────────────────────┐
│                 │                   │                    │
│  Admin Frontend │◄───────────────►  │  Python FastAPI    │
│  (React)        │   HTTP/REST       │  Backend           │
│                 │                   │                    │
└─────────────────┘                   └────────────────────┘
▲          ▲
│          │
▼          ▼
┌─────────────────┐                   ┌────────────────────┐
│                 │                   │  External Services  │
│ Candidate UI    │◄───────────────►  │  - LiveKit         │
│ (React)         │   WebSockets      │  - OpenAI          │
│                 │                   │  - Deepgram        │
└─────────────────┘                   │  - ElevenLabs      │
└────────────────────┘
▲
│
▼
┌────────────────────┐
│   Local Storage    │
│  - CV/JD Files     │
│  - Prompts         │
│  - Transcripts     │
│  - Results         │
│  - Audio           │
└────────────────────┘

text

Copy

### Interview Flow Sequence

1. Admin uploads CV, job description, and configures system prompt via the dashboard.
2. Backend generates a unique interview URL for the candidate.
3. Candidate joins the interview through the URL in the candidate interface.
4. AI interviewer greets the candidate using TTS.
5. Candidate responds via microphone, processed by STT.
6. LLM generates contextual follow-up questions.
7. Process repeats until the maximum question limit is reached.
8. LLM provides a final rating and verdict.
9. Results are stored locally for admin review.

## Project Structure
ai-interviewer/
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── init.py
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── config.py             # Configuration and environment variables
│   │   ├── routers/              # API route definitions
│   │   │   ├── init.py
│   │   │   ├── admin.py          # Admin endpoints
│   │   │   ├── candidate.py      # Candidate endpoints
│   │   │   └── interviews.py     # Interview management endpoints
│   │   ├── services/             # Core business logic
│   │   │   ├── init.py
│   │   │   ├── llm_service.py    # GPT-4 integration
│   │   │   ├── stt_service.py    # Speech-to-Text service
│   │   │   ├── tts_service.py    # Text-to-Speech service
│   │   │   └── livekit_service.py # LiveKit integration
│   │   ├── models/               # Data models
│   │   │   ├── init.py
│   │   │   ├── interview.py      # Interview data model
│   │   │   └── schemas.py        # Pydantic schemas
│   │   ├── utils/                # Utility functions
│   │   │   ├── init.py
│   │   │   ├── storage.py        # File storage utilities
│   │   │   └── prompt_utils.py   # LLM prompt engineering
│   ├── data/                     # Local storage
│   │   ├── cv/                   # CV storage
│   │   ├── jd/                   # Job description storage
│   │   ├── prompts/              # System prompts
│   │   ├── transcripts/          # Interview transcripts
│   │   ├── results/              # Interview results
│   │   ├── audio/                # TTS audio files
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Example environment variables
│   └── Dockerfile                # Backend Dockerfile
│
├── frontend/                     # React frontend
│   ├── admin/                    # Admin dashboard
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/       # React components
│   │   │   ├── pages/            # Page components
│   │   │   ├── services/         # API services
│   │   │   ├── utils/            # Utility functions
│   │   │   └── App.tsx           # Admin application
│   │   ├── package.json
│   │   ├── README.md
│   │   └── Dockerfile            # Admin Dockerfile
│   │
│   └── candidate/                # Candidate interface
│       ├── public/
│       ├── src/
│       │   ├── components/       # React components
│       │   ├── services/         # API services
│       │   ├── utils/            # Utility functions
│       │   └── App.tsx           # Candidate application
│       ├── package.json
│       ├── README.md
│       └── Dockerfile            # Candidate Dockerfile
│
├── docker-compose.yml            # Docker Compose configuration
├── .env                          # Environment variables (not in version control)
├── LICENSE
└── README.md                     # Main README file

text

Copy

## Setup Instructions

### Prerequisites

- **Docker** and **Docker Compose** (for containerized setup)
- **Python 3.9+** (for local backend setup)
- **Node.js 18+** (for local frontend setup)
- **API Keys** for:
  - OpenAI (GPT-4)
  - Deepgram (STT)
  - ElevenLabs (TTS)
  - LiveKit (real-time audio)

### Option 1: Docker Setup (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/Arihantkumar2022/gen-ai-intern_.git
   cd ai-interviewer
Create a .env file at the project root with your API keys (use .env.example as a template):
bash

Copy
cp backend/.env.example .env
Edit .env:
text

Copy
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
Build and run the services:
bash

Copy
docker-compose up --build
Access the application:
Admin Dashboard: http://localhost:3000
Candidate Interface: http://localhost:3001/interview/<interview_id>
Backend API: http://localhost:8000
Stop the services:
bash

Copy
docker-compose down
Option 2: Local Setup
Backend Setup
Navigate to the backend directory:
bash

Copy
cd backend
Create and activate a virtual environment:
bash

Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bash

Copy
pip install -r requirements.txt
Create a .env file:
bash

Copy
cp .env.example .env
Edit .env with your API keys (see Docker setup for example).
Run the backend server:
bash

Copy
cd app
uvicorn main:app --reload
Admin Frontend Setup
Navigate to the admin directory:
bash

Copy
cd frontend/admin
Install dependencies:
bash

Copy
npm install
Create a .env.local file:
bash

Copy
echo "VITE_API_URL=http://localhost:8000" > .env.local
Start the development server:
bash

Copy
npm start
Candidate Frontend Setup
Navigate to the candidate directory:
bash

Copy
cd frontend/candidate
Install dependencies:
bash

Copy
npm install
Create a .env.local file:
bash

Copy
echo "VITE_API_URL=http://localhost:8000" > .env.local
Start the development server:
bash

Copy
npm start
Usage Guide
Admin Flow
Access the Admin Dashboard
Open http://localhost:3000.
Navigate to "Create New Interview".
Configure a New Interview
Upload a candidate CV (PDF).
Upload a job description (PDF).
Enter a system prompt for the AI interviewer.
Set the interviewer name and maximum questions (optional).
Click "Create Interview" to generate a candidate URL.
Share Interview Link
Copy the generated URL (e.g., http://localhost:3001/interview/<interview_id>).
Share it with the candidate.
Review Interview Results
Go to the "Interviews" section in the dashboard.
Select a completed interview to view:
Transcript of AI and candidate interactions.
Rating (1-10).
Verdict and detailed feedback.
Export results if needed (optional feature).
Candidate Flow
Access the Interview
Open the provided interview URL (e.g., http://localhost:3001/interview/<interview_id>).
Grant microphone permissions.
Test audio settings if prompted.
Participate in Interview
The AI interviewer greets you via TTS.
Listen to questions and respond naturally using your microphone.
The AI asks follow-up questions based on your responses.
Complete the Interview
The AI signals when the interview is complete.
View immediate feedback (if enabled).
Results are saved for admin review.
API Documentation
The backend exposes the following key endpoints:

Admin API
POST /api/admin/interviews - Create a new interview (uploads CV, JD, prompt).
POST /api/admin/interviews/{interview_id}/system-prompt - Update system prompt.
Candidate API
GET /api/candidate/interviews/{interview_id}/join - Get interview details.
POST /api/candidate/interviews/{interview_id}/livekit-token - Generate LiveKit token.
WS /api/ws/interview/{interview_id} - WebSocket for real-time interview.
Interview Management API
GET /api/interviews - List all interviews.
GET /api/interviews/{interview_id} - Get interview details.
GET /api/interviews/{interview_id}/results - Get results for a completed interview.
Core Features Implementation
LLM Integration
Uses OpenAI's GPT-4 to:
Generate initial questions based on CV and job description.
Create follow-up questions based on candidate responses.
Provide a final assessment with rating and verdict.
STT & TTS
Speech-to-Text: Deepgram transcribes candidate responses in real-time.
Text-to-Speech: ElevenLabs converts AI questions to natural-sounding audio.
LiveKit Integration
Handles real-time audio communication with low latency.
Supports microphone input and audio playback for candidates.
Troubleshooting
Common Issues
Docker: Backend fails to start:
Ensure API keys are set in .env.
Check Docker volume permissions: chmod -R 777 backend/data.
Audio not working:
Verify browser microphone permissions.
Ensure LiveKit API keys are correct.
API errors:
Confirm .env contains valid API keys.
Check backend logs: docker logs ai-interviewer-backend-1.
TTS delays:
Longer AI responses may cause slight delays due to ElevenLabs processing.
Transcription errors:
Minimize background noise for better STT accuracy.
Logs and Debugging
Backend: View logs with docker logs ai-interviewer-backend-1 or check terminal for local setup.
Frontend: Open browser developer tools (Console tab) for admin/candidate interfaces.
Docker: Use docker-compose logs to view all service logs.
Known Limitations
No persistent database; all data is stored locally in backend/data/.
Limited simultaneous interview capacity due to WebSocket handling.
API rate limits may apply for OpenAI, Deepgram, and ElevenLabs.
Audio files in data/audio/ may accumulate; manual cleanup may be needed.
License
Acknowledgements
OpenAI for GPT-4 API
Deepgram for Speech-to-Text
ElevenLabs for Text-to-Speech
LiveKit for real-time communication
text

Copy

**Changes from Original**:

- **Docker Section**: Added detailed instructions for running with Docker Compose, including `.env` setup and port mappings.
- **Frontend Updates**: Updated to mention TypeScript and Vite, with consolidated setup steps.
- **Data Folder**: Explicitly listed `data` subdirectories for clarity.
- **API Documentation**: Streamlined to reflect router-based endpoints (`admin`, `candidate`, `interviews`).
- **Troubleshooting**: Added Docker-specific issues (e.g., volume permissions) and improved debugging tips.
- **Formatting**: Enhanced readability with consistent headings and bullet points.
- **Project Structure**: Updated to include Dockerfiles and `.env`.

The updated `readme.md` retains all critical information from the original while making it more user-friendly and aligned with the Docker setup.

---

### Steps to Use Docker Compose

1. **Create Dockerfiles**:
   - Save the provided `Dockerfile` files in `backend/`, `frontend/admin/`, and `frontend/candidate/`.

2. **Create `.env`**:
   - Copy `backend/.env.example` to the project root as `.env` and fill in your API keys:
     ```bash
     cp backend/.env.example .env
Edit .env with valid keys (do not commit to version control).
Run Docker Compose:
From the project root:
bash

Copy
docker-compose up --build
This builds and starts all services.
Access the Application:
Admin Dashboard: http://localhost:3000
Candidate Interface: http://localhost:3001/interview/<interview_id>
API Docs (FastAPI): http://localhost:8000/docs
Verify Data Persistence:
Check backend/data/ for generated files (cv, jd, prompts, results, audio).
Ensure the folder is writable: chmod -R 777 backend/data.
Stop Services:
bash

Copy
docker-compose down