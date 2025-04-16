# backend/app/services/llm_service.py

import os
import openai
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
import PyPDF2
from utils.prompt_utils import (
    create_initial_questions_prompt,
    create_follow_up_prompt,
    create_assessment_prompt
)

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with OpenAI's GPT models"""
    
    def __init__(self):
        """Initialize the LLM service with API key from environment"""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    async def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    async def generate_initial_questions(
        self, 
        cv_path: str, 
        jd_path: str, 
        system_prompt: str,
        max_questions: int = 10
    ) -> List[str]:
        """Generate initial interview questions based on CV and job description"""
        try:
            # Extract text from PDFs
            cv_text = await self._extract_text_from_pdf(cv_path)
            jd_text = await self._extract_text_from_pdf(jd_path)
            
            if not cv_text or not jd_text:
                logger.error("Failed to extract text from CV or JD")
                return ["Could you tell me about your background and experience?"]
            
            # Create prompt for GPT
            prompt = create_initial_questions_prompt(
                cv_text=cv_text, 
                jd_text=jd_text, 
                system_prompt=system_prompt,
                max_questions=max_questions
            )
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse response
            content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                questions_data = json.loads(content)
                questions = questions_data.get("questions", [])
                if not questions:
                    # Fallback to text parsing if JSON structure doesn't contain questions
                    questions = content.split("\n")
                    questions = [q.strip() for q in questions if q.strip()]
            except json.JSONDecodeError:
                # If not valid JSON, treat as list of questions separated by newlines
                questions = content.split("\n")
                questions = [q.strip() for q in questions if q.strip()]
            
            # Ensure we have at least some questions
            if not questions:
                questions = ["Could you tell me about your background and experience?"]
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating initial questions: {str(e)}")
            # Return a default question if there's an error
           # backend/app/services/llm_service.py (continued)

            return ["Could you tell me about your background and experience?"]
            
        except Exception as e:
            logger.error(f"Error generating initial questions: {str(e)}")
            # Return a default question if there's an error
            return ["Could you tell me about your background and experience?"]
    
    async def generate_follow_up_question(
        self, 
        transcript: List[Dict[str, str]], 
        system_prompt: str,
        cv_path: str,
        jd_path: str
    ) -> str:
        """Generate a follow-up question based on the interview transcript so far"""
        try:
            # Extract text from PDFs
            cv_text = await self._extract_text_from_pdf(cv_path)
            jd_text = await self._extract_text_from_pdf(jd_path)
            
            # Create prompt for GPT
            prompt = create_follow_up_prompt(
                transcript=transcript,
                cv_text=cv_text,
                jd_text=jd_text,
                system_prompt=system_prompt
            )
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the follow-up question
            follow_up = response.choices[0].message.content.strip()
            
            return follow_up
            
        except Exception as e:
            logger.error(f"Error generating follow-up question: {str(e)}")
            # Return a default follow-up question
            return "Can you elaborate more on your previous answer?"
    
    async def generate_final_assessment(
        self, 
        transcript: List[Dict[str, str]], 
        cv_path: str,
        jd_path: str
    ) -> Dict[str, Any]:
        """Generate final assessment, rating, and verdict for the candidate"""
        try:
            # Extract text from PDFs
            cv_text = await self._extract_text_from_pdf(cv_path)
            jd_text = await self._extract_text_from_pdf(jd_path)
            
            # Create prompt for GPT
            prompt = create_assessment_prompt(
                transcript=transcript,
                cv_text=cv_text,
                jd_text=jd_text
            )
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # Extract the assessment
            content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                assessment = json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, create a structured assessment manually
                assessment = {
                    "rating": 5,  # Default middle rating
                    "verdict": "Unable to parse assessment properly. Please review the interview transcript.",
                    "detailed_feedback": {
                        "strengths": ["Unable to parse assessment"],
                        "weaknesses": ["Unable to parse assessment"],
                        "fit_for_role": "Uncertain"
                    }
                }
                
                # Try to extract rating from text
                rating_line = [line for line in content.split('\n') if "rating" in line.lower()]
                if rating_line:
                    try:
                        rating_text = rating_line[0].split(':')[1].strip()
                        rating = int(rating_text[0])
                        if 1 <= rating <= 10:
                            assessment["rating"] = rating
                    except:
                        pass
                
                # Try to extract verdict
                verdict_lines = []
                verdict_section = False
                for line in content.split('\n'):
                    if "verdict" in line.lower():
                        verdict_section = True
                        continue
                    if verdict_section and line.strip() and not any(kw in line.lower() for kw in ["strength", "weakness", "feedback"]):
                        verdict_lines.append(line.strip())
                    if verdict_section and any(kw in line.lower() for kw in ["strength", "weakness", "feedback"]):
                        break
                
                if verdict_lines:
                    assessment["verdict"] = " ".join(verdict_lines)
            
            # Ensure required fields exist
            if "rating" not in assessment:
                assessment["rating"] = 5
            if "verdict" not in assessment:
                assessment["verdict"] = "Review the transcript for a complete assessment."
            if "detailed_feedback" not in assessment:
                assessment["detailed_feedback"] = {}
            
            return assessment
            
        except Exception as e:
            logger.error(f"Error generating final assessment: {str(e)}")
            # Return a default assessment if there's an error
            return {
                "rating": 5,
                "verdict": "Unable to generate assessment due to an error. Please review the interview transcript.",
                "detailed_feedback": {
                    "error": str(e)
                }
            }