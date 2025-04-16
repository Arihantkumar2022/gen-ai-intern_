# backend/app/services/stt_service.py

import os
import logging
import base64
import asyncio
from typing import Optional
import tempfile
from deepgram import Deepgram

logger = logging.getLogger(__name__)

class STTService:
    """Service for converting speech to text using Deepgram"""
    
    def __init__(self):
        """Initialize the STT service with API key from environment"""
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            logger.warning("DEEPGRAM_API_KEY not found in environment variables")
        
        self.deepgram = Deepgram(self.api_key)
        self.language = os.getenv("DEEPGRAM_LANGUAGE", "en-US")
    
    async def speech_to_text(self, audio_data: str) -> str:
        """
        Convert audio data to text
        
        Args:
            audio_data: Base64 encoded audio data
            
        Returns:
            Transcribed text
        """
        try:
            # Decode base64 audio data
            decoded_audio = base64.b64decode(audio_data)
            
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(decoded_audio)
            
            try:
                # Open the audio file
                with open(temp_file_path, 'rb') as audio_file:
                    # Send to Deepgram
                    source = {'buffer': audio_file, 'mimetype': 'audio/wav'}
                    response = await self.deepgram.transcription.prerecorded(
                        source,
                        {
                            'punctuate': True,
                            'language': self.language,
                            'model': 'nova',
                            'smart_format': True
                        }
                    )
                
                # Extract the transcript
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                
                return transcript if transcript else "I couldn't hear your response clearly."
                
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logger.error(f"Error in speech to text conversion: {str(e)}")
            return "I'm sorry, there was an issue processing your audio. Could you please repeat?"

    async def live_transcription(self, websocket):
        """
        Real-time transcription for continuous audio stream
        
        Args:
            websocket: WebSocket connection for receiving audio chunks
        """
        # This method would be implemented for streaming audio transcription
        # if required by the application
        pass