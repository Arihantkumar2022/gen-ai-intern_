# backend/app/utils/prompt_utils.py

from typing import List, Dict, Any

def create_initial_questions_prompt(
    cv_text: str, 
    jd_text: str, 
    system_prompt: str,
    max_questions: int = 10
) -> Dict[str, str]:
    """
    Create a prompt for generating initial interview questions
    
    Args:
        cv_text: Text content of the CV
        jd_text: Text content of the job description
        system_prompt: Custom system prompt for the interviewer personality
        max_questions: Maximum number of questions to generate
        
    Returns:
        Dict containing system and user prompts
    """
    # Truncate texts if they are too long to fit within token limits
    cv_text = cv_text[:4000]  # Arbitrary limit, adjust as needed
    jd_text = jd_text[:4000]  # Arbitrary limit, adjust as needed
    
    system_message = f"""
    {system_prompt}
    
    You are conducting a professional job interview. Your task is to generate {max_questions} thoughtful interview 
    questions based on the candidate's CV and the job description. The questions should help assess the 
    candidate's suitability for the role.
    
    Format your response as a JSON object with a single key "questions" containing an array of 
    question strings. Each question should be clear, concise, and directly relevant to assessing 
    the candidate's fit for this specific role.
    """
    
    user_message = f"""
    Please generate {max_questions} interview questions based on the following CV and job description:
    
    ## CV
    {cv_text}
    
    ## Job Description
    {jd_text}
    
    Generate questions that will assess the candidate's relevant skills, experience, and fit for this role.
    """
    
    return {
        "system": system_message,
        "user": user_message
    }

def create_follow_up_prompt(
    transcript: List[Dict[str, str]], 
    cv_text: str,
    jd_text: str,
    system_prompt: str
) -> Dict[str, str]:
    """
    Create a prompt for generating follow-up questions
    
    Args:
        transcript: List of conversation entries so far
        cv_text: Text content of the CV
        jd_text: Text content of the job description
        system_prompt: Custom system prompt for the interviewer personality
        
    Returns:
        Dict containing system and user prompts
    """
    # Truncate texts if they are too long
    cv_text = cv_text[:2000]  # Shorter than initial as we need space for transcript
    jd_text = jd_text[:2000]  # Shorter than initial as we need space for transcript
    
    # Format transcript for inclusion in prompt
    formatted_transcript = ""
    for entry in transcript:
        speaker = "AI Interviewer" if entry["speaker"] == "ai" else "Candidate"
        formatted_transcript += f"{speaker}: {entry['text']}\n\n"
    
    system_message = f"""
    {system_prompt}
    
    You are conducting a professional job interview. Your task is to generate the next follow-up question 
    based on the interview transcript so far, the candidate's CV, and the job description.
    
    Ask only ONE follow-up question that digs deeper into the candidate's previous response or explores 
    a new relevant area based on their CV and the job requirements. Make your question clear, concise,
    and conversational. Avoid asking multiple questions at once.
    
    The question should help assess the candidate's suitability for the role and provide valuable insights
    beyond what's already been discussed.
    """
    
    user_message = f"""
    ## CV Summary
    {cv_text}
    
    ## Job Description Summary
    {jd_text}
    
    ## Interview Transcript So Far
    {formatted_transcript}
    
    Based on the above transcript, please generate ONE thoughtful follow-up question to ask the candidate next.
    """
    
    return {
        "system": system_message,
        "user": user_message
    }

def create_assessment_prompt(
    transcript: List[Dict[str, str]], 
    cv_text: str,
    jd_text: str
) -> Dict[str, str]:
    """
    Create a prompt for generating final candidate assessment
    
    Args:
        transcript: Complete interview transcript
        cv_text: Text content of the CV
        jd_text: Text content of the job description
        
    Returns:
        Dict containing system and user prompts
    """
    # Truncate texts if they are too long
    cv_text = cv_text[:2000]
    jd_text = jd_text[:2000]
    
    # Format transcript for inclusion in prompt
    formatted_transcript = ""
    for entry in transcript:
        speaker = "AI Interviewer" if entry["speaker"] == "ai" else "Candidate"
        formatted_transcript += f"{speaker}: {entry['text']}\n\n"
    
    system_message = """
    You are an experienced hiring manager tasked with evaluating a job candidate based on their interview responses.
    
    Provide a comprehensive assessment of the candidate including:
    1. A rating from 1-10 (where 1 is completely unsuitable and 10 is perfect for the role)
    2. A brief verdict on whether they should be hired
    3. Detailed feedback on their strengths and weaknesses
    
    Format your response as a JSON object with the following structure:
    {
        "rating": <number between 1-10>,
        "verdict": "<brief hiring recommendation>",
        "detailed_feedback": {
            "strengths": ["<strength 1>", "<strength 2>", ...],
            "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
            "fit_for_role": "<assessment of fit>"
        }
    }
    
    Be objective and fair in your assessment, focusing on the candidate's responses in relation to 
    the job requirements.
    """
    
    user_message = f"""
    ## CV Summary
    {cv_text}
    
    ## Job Description
    {jd_text}
    
    ## Complete Interview Transcript
    {formatted_transcript}
    
    Based on the above information, please provide your assessment of this candidate as a JSON object.
    """
    
    return {
        "system": system_message,
        "user": user_message
    }