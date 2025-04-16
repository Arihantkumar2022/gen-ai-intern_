# backend/app/services/tts_service.py

import os
import logging
import asyncio
import base64
import requests
import tempfile
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

class TTSService:
    """Service for converting text to speech using ElevenLabs"""
    
    def __init__(self):
        """Initialize the TTS service with API key from environment"""
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            logger.warning("ELEVENLABS_API_KEY not found in environment variables")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice
        self.model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_monolingual_v1")
        
        # Create directory for audio files if it doesn't exist
        self.audio_dir = Path(__file__).parent.parent.parent / "data" / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
    
    async def text_to_speech(self, text: str) -> str:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert to speech
            
        Returns:
            URL path to the generated audio file
        """
        try:
            # Generate unique filename for the audio
            filename = f"{uuid.uuid4()}.mp3"
            file_path = self.audio_dir / filename
            
            # Prepare request to ElevenLabs API
            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            body = {
                "text": text,
                "model_id": self.model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8
                }
            }
            
            # Make API request
            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
            
            # Save audio file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Return relative URL to audio file
            return f"/data/audio/{filename}"
            
        except Exception as e:
            logger.error(f"Error in text to speech conversion: {str(e)}")
            return ""
    
    async def generate_voice_sample(self, text: str, voice_id: str = None) -> str:
        """
        Generate a sample audio with a specific voice
        
        Args:
            text: Text to convert to speech
            voice_id: ID of the voice to use
            
        Returns:
            Base64 encoded audio data
        """
        try:
            # Use provided voice ID or default
            voice = voice_id if voice_id else self.voice_id
            
            # Prepare request to ElevenLabs API
            url = f"{self.base_url}/text-to-speech/{voice}"
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            body = {
                "text": text,
                "model_id": self.model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8
                }
            }
            
            # Make API request
            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
            
            # Convert to base64
            audio_base64 = base64.b64encode(response.content).decode('utf-8')
            
            return audio_base64
            
        except Exception as e:
            logger.error(f"Error generating voice sample: {str(e)}")
            return ""
    
    async def get_available_voices(self):
        """Get list of available voices from ElevenLabs"""
        try:
            url = f"{self.base_url}/voices"
            headers = {"xi-api-key": self.api_key}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json().get("voices", [])
            
        except Exception as e:
            logger.error(f"Error getting available voices: {str(e)}")
            return []