# backend/app/utils/storage.py

import json
import os
import logging
from pathlib import Path
from fastapi import UploadFile
import shutil

logger = logging.getLogger(__name__)

async def save_file(upload_file: UploadFile, destination: Path) -> Path:
    """
    Save an uploaded file to the specified destination
    
    Args:
        upload_file: The uploaded file
        destination: Destination path
        
    Returns:
        Path to the saved file
    """
    try:
        # Ensure the directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        return destination
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise e

def save_json(data: dict, destination: Path) -> Path:
    """
    Save JSON data to a file
    
    Args:
        data: The data to save
        destination: Destination path
        
    Returns:
        Path to the saved file
    """
    try:
        # Ensure the directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the JSON data
        with open(destination, "w") as f:
            json.dump(data, f, indent=2)
        
        return destination
    
    except Exception as e:
        logger.error(f"Error saving JSON: {str(e)}")
        raise e

def read_json(file_path: Path) -> dict:
    """
    Read JSON data from a file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The loaded JSON data
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    
    except Exception as e:
        logger.error(f"Error reading JSON: {str(e)}")
        raise e

def read_file(file_path: Path) -> str:
    """
    Read text from a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        The file contents as a string
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise e