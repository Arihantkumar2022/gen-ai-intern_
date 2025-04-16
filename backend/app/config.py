# backend/app/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
CV_DIR = DATA_DIR / "cv"
JD_DIR = DATA_DIR / "jd"
PROMPT_DIR = DATA_DIR / "prompts"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
RESULTS_DIR = DATA_DIR / "results"
AUDIO_DIR = DATA_DIR / "audio"

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# Service configurations
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://your-livekit-instance.livekit.cloud")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# CORS settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")