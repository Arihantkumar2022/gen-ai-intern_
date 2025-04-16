# backend/app/services/livekit_service.py

import os
import logging
import time
import jwt

logger = logging.getLogger(__name__)

class LiveKitService:
    """Service for integrating with LiveKit for real-time communication"""
    
    def __init__(self):
        """Initialize the LiveKit service with API key and secret from environment"""
        self.api_key = os.getenv("LIVEKIT_API_KEY")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET")
        self.livekit_url = os.getenv("LIVEKIT_URL", "wss://your-livekit-instance.livekit.cloud")
        
        if not self.api_key or not self.api_secret:
            logger.warning("LIVEKIT_API_KEY or LIVEKIT_API_SECRET not found in environment variables")
    
    def create_token(self, room_name: str, participant_name: str, ttl: int = 3600) -> str:
        """
        Create a LiveKit access token
        
        Args:
            room_name: Name of the LiveKit room
            participant_name: Name of the participant
            ttl: Time to live for the token in seconds (default: 1 hour)
            
        Returns:
            JWT token for LiveKit access
        """
        try:
            # Set token validity time
            now = int(time.time())
            exp = now + ttl
            
            # Define token claims
            claims = {
                # Token metadata
                "iss": self.api_key,  # Issuer
                "nbf": now,           # Not before time
                "exp": exp,           # Expiration time
                
                # LiveKit specific claims
                "video": {
                    "room": room_name,
                    "room_join": True,
                    "can_publish": True,
                    "can_subscribe": True,
                    "room_create": True
                },
                "metadata": participant_name
            }
            
            # Generate JWT token
            token = jwt.encode(claims, self.api_secret, algorithm="HS256")
            
            return token
            
        except Exception as e:
            logger.error(f"Error creating LiveKit token: {str(e)}")
            return ""
    
    def create_room(self, room_name: str):
        """
        Create a LiveKit room (Note: this would typically use LiveKit's admin API)
        
        Args:
            room_name: Name of the room to create
        """
        # In a full implementation, this would make an API call to LiveKit's admin API
        # to create a room. For this example, we're simplifying since rooms are 
        # automatically created when participants join with a valid token.
        logger.info(f"Room '{room_name}' will be created when participants join")
        return {"name": room_name, "status": "will_create_on_join"}