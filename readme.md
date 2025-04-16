# AI Interviewer

A full-stack application that simulates voice-based AI interviews. The system uses Text-to-Speech (TTS) to ask questions, Speech-to-Text (STT) to transcribe candidate responses, and a Language Model (GPT-4) to provide context-driven follow-up questions and rate candidates.

## System Architecture

### Overview

The AI Interviewer follows a client-server architecture with these key components:

1. **Frontend**
   - Admin Dashboard: For uploading CVs, job descriptions, and configuring the interview
   - Candidate Interface: For participating in the interview

2. **Backend**
   - Python FastAPI server
   - WebSocket connections for real-time communication
   - API endpoints for interview orchestration

3. **External Services**
   - LiveKit for real-time audio/video
   - OpenAI GPT-4 for question generation and evaluation
   - Deepgram for Speech-to-Text
   - ElevenLabs for Text-to-Speech  

4. **Local Storage**
   - File system storage for interview data
   - JSON files for configuration and results

### System Flow Diagram

```
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
                                      │  - Transcripts     │
                                      │  - Results         │
                                      └────────────────────┘
```

### Interview Flow Sequence

1. Admin uploads CV, job description, and configures system prompt
2. System generates unique interview URL for candidate
3. Candidate joins interview through URL
4. AI interviewer greets candidate using TTS
5. Candidate responds, audio is processed via STT
6. LLM generates contextual follow-up questions
7. Process repeats until interview completion
8. LLM provides final rating and verdict
9. Results stored locally for admin review

## Project Structure

```
ai-interviewer/
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── config.py             # Configuration and environment variables
│   │   ├── routers/              # API route definitions
│   │   │   ├── __init__.py
│   │   │   ├── admin.py          # Admin panel API endpoints
│   │   │   ├── candidate.py      # Candidate API endpoints
│   │   │   └── interviews.py     # Interview management endpoints
│   │   ├── services/             # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py    # GPT-4 integration
│   │   │   ├── stt_service.py    # Speech-to-Text service
│   │   │   ├── tts_service.py    # Text-to-Speech service
│   │   │   └── livekit_service.py # LiveKit integration
│   │   ├── models/               # Data models
│   │   │   ├── __init__.py
│   │   │   ├── interview.py      # Interview data model
│   │   │   └── schemas.py        # Pydantic schemas
│   │   └── utils/                # Utility functions
│   │       ├── __init__.py
│   │       ├── storage.py        # Local file storage utilities
│   │       └── prompt_utils.py   # LLM prompt engineering
│   ├── data/                     # Local data storage
│   │   ├── cv/                   # CV storage
│   │   ├── jd/                   # Job description storage
│   │   ├── prompts/              # System prompts
│   │   ├── transcripts/          # Interview transcripts
│   │   └── results/              # Interview results
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Example environment variables
│
├── frontend/                     # React frontend
│   ├── admin/                    # Admin dashboard
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/       # React components
│   │   │   ├── pages/            # Admin pages
│   │   │   ├── services/         # API services
│   │   │   ├── utils/            # Utility functions
│   │   │   └── App.js            # Admin application
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── candidate/                # Candidate interface
│       ├── public/
│       ├── src/
│       │   ├── components/       # React components
│       │   ├── services/         # API services
│       │   ├── utils/            # Utility functions
│       │   └── App.js            # Candidate application
│       ├── package.json
│       └── README.md
│
├── docker-compose.yml            # Docker setup (optional)
├── LICENSE
└── README.md                     # Main README file
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- API keys for:
  - OpenAI
  - Deepgram
  - ElevenLabs
  - LiveKit (or alternative)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Arihantkumar2022/gen-ai-intern_.git
   cd ai-interviewer/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   ```

6. Run the backend server:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

### Frontend Setup

#### Admin Dashboard

1. Navigate to the admin directory:
   ```bash
   cd ai-interviewer/frontend/admin
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

#### Candidate Interface

1. Navigate to the candidate directory:
   ```bash
   cd ai-interviewer/frontend/candidate
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

## Usage Guide

### Admin Flow

1. **Access the Admin Dashboard**
   - Open your browser and navigate to `http://localhost:3000`
   - Login with your credentials (if implemented)

2. **Configure a New Interview**
   - Click "New Interview" button
   - Upload or paste the candidate's CV
   - Upload or paste the job description
   - Configure the system prompt for the AI interviewer
   - Customize interviewer personality (optional)
   - Set interview duration or question count (optional)

3. **Generate Interview Link**
   - Click "Generate Link" button
   - Copy the unique interview URL
   - Share this URL with the candidate

4. **Review Interview Results**
   - Access the "Interviews" section
   - Select a completed interview
   - View transcript, ratings, and verdict
   - Export results (if implemented)

### Candidate Flow

1. **Access the Interview**
   - Open the shared interview URL
   - Grant microphone and camera permissions
   - Test audio/video settings

2. **Participate in Interview**
   - AI interviewer will greet you and begin the interview
   - Listen to questions delivered via TTS
   - Respond naturally - your voice will be transcribed
   - AI will ask contextual follow-up questions

3. **Complete the Interview**
   - AI will indicate when the interview is complete
   - You may receive immediate feedback (if configured)
   - Results are saved for admin review

## API Documentation

The backend exposes the following key endpoints:

### Admin API

- `POST /api/interviews` - Create a new interview
- `GET /api/interviews` - List all interviews
- `GET /api/interviews/{id}` - Get interview details
- `GET /api/interviews/{id}/results` - Get interview results
- `POST /api/interviews/{id}/system-prompt` - Update system prompt

### Candidate API

- `GET /api/interviews/{id}/join` - Join an interview
- `WS /api/ws/interview/{id}` - WebSocket for interview session

### LiveKit Integration

- `POST /api/livekit/token` - Generate LiveKit token
- `GET /api/livekit/room/{id}` - Get room info

## Core Features Implementation

### LLM Integration

The system uses OpenAI's GPT-4 for three primary functions:
- Generating initial interview questions based on CV and job description
- Creating contextual follow-up questions based on candidate responses
- Providing a final assessment with ratings and verdict

### STT & TTS

- **Speech-to-Text**: Deepgram processes candidate's spoken responses
- **Text-to-Speech**: ElevenLabs converts AI questions to natural speech

### LiveKit Integration

LiveKit handles real-time audio/video communication, providing:
- Low-latency audio transmission
- Optional video capabilities
- Reliable connection management

## Troubleshooting

### Common Issues

- **Audio not working**: Ensure browser permissions are granted
- **API errors**: Verify API keys in `.env` file
- **TTS delays**: May occur with longer AI responses
- **Transcription errors**: Background noise can impact STT quality

### Logs and Debugging

- Backend logs: Check terminal running FastAPI server
- Frontend console: Open browser developer tools

## Known Limitations

- No persistent database (local storage only)
- Limited simultaneous interview capacity
- API rate limits may apply (OpenAI, Deepgram, ElevenLabs)

## License

[MIT License](LICENSE)

## Acknowledgements

- OpenAI for GPT-4 API
- Deepgram for Speech-to-Text
- ElevenLabs for Text-to-Speech
- LiveKit for real-time communication