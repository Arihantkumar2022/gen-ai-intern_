# AI Interviewer Admin Dashboard

React-based admin interface for the AI Interviewer application.

## Setup Instructions

1. Navigate to the admin directory:
   ```bash
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
Usage
Home: Navigate to create a new interview or view past interviews.
Create Interview: Upload CV and JD (PDFs), set system prompt, interviewer name, and max questions.
View Results: See transcripts, ratings, verdicts, and feedback for completed interviews.
Dependencies
React 18
TypeScript
styled-components
axios
react-router-dom
text

Copy

**Explanation**:
- Documentation mirroring the backend's `readme.md` style.
- Includes setup and usage instructions.

---

### Step 2: Candidate Interface

The Candidate Interface allows users to:

- Join an interview via a unique URL.
- Connect to LiveKit for real-time audio.
- Hear AI questions via TTS and respond via microphone (STT).
- Receive completion feedback (if configured).

#### Candidate Files

##### `frontend/candidate/package.json`

```json
{
  "name": "ai-interviewer-candidate",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@livekit/components-react": "^2.0.0",
    "axios": "^1.6.8",
    "livekit-client": "^2.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.3",
    "styled-components": "^6.1.8",
    "typescript": "^5.4.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.67",
    "@types/react-dom": "^18.2.22",
    "@types/styled-components": "^5.1.34",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.1.6",
    "vite-plugin-env-compatible": "^2.0.1"
  },
  "scripts": {
    "start": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}