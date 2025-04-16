# AI Interviewer Candidate Interface

React-based interface for candidates to participate in AI-driven interviews.

## Setup Instructions

1. Navigate to the candidate directory:
   ```bash
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
Usage
Access the interview via the unique URL (e.g., /interview/:interviewId).
Grant microphone permissions to enable audio input.
Listen to AI questions and respond naturally.
View completion message and results (if configured).
Dependencies
React 18
TypeScript
styled-components
axios
react-router-dom
livekit-client
text

Copy

---

### Integration Notes

- **Backend Compatibility**: The frontend uses the exact API endpoints defined in the backend (`/api/admin/interviews`, `/api/candidate/interviews/:id/join`, etc.), ensuring seamless integration.
- **LiveKit**: The candidate interface uses `@livekit/components-react` for audio visualization and `livekit-client` for room management, connecting to the backend's LiveKit token endpoint.
- **TTS/STT**: The backend handles TTS (ElevenLabs) and STT (Deepgram), so the frontend only needs to play audio files and send recorded audio chunks via WebSocket.
- **Error Handling**: Both interfaces include loading spinners, success messages, and error messages, mirroring the backend's robust error handling.
- **Styling**: `styled-components` provides a clean, maintainable way to style components, with a consistent design across both apps.

---

### Testing Instructions

To test the frontend with the backend:

1. **Start the Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   cd app
   uvicorn main:app --reload
Start the Admin Dashboard:
bash

Copy
cd frontend/admin
npm install
npm start
Open http://localhost:3000.
Create an interview by uploading PDFs and setting a prompt.
Copy the candidate URL.
Start the Candidate Interface:
bash

Copy
cd frontend/candidate
npm install
npm start
Open the candidate URL (e.g., http://localhost:3001/interview/:interviewId).
Grant microphone permissions and participate in the interview.
Verify Results:
Return to the admin dashboard.
Navigate to the results page to view the transcript, rating, and verdict.