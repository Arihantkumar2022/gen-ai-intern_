import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface InterviewResponse {
  interview_id: string;
  status: string;
  candidate_url: string;
}

export interface InterviewResult {
  interview_id: string;
  transcript: { speaker: string; text: string }[];
  rating: number;
  verdict: string;
  detailed_feedback: {
    strengths: string[];
    weaknesses: string[];
    fit_for_role: string;
  };
}

export const createInterview = async (data: {
  cv: File;
  jd: File;
  systemPrompt: string;
  interviewerName: string;
  maxQuestions: number;
}): Promise<InterviewResponse> => {
  const formData = new FormData();
  formData.append('cv', data.cv);
  formData.append('jd', data.jd);
  formData.append('system_prompt', data.systemPrompt);
  formData.append('interviewer_name', data.interviewerName);
  formData.append('max_questions', data.maxQuestions.toString());

  const response = await axios.post(`${API_URL}/api/admin/interviews`, formData);
  return response.data;
};

export const listInterviews = async (): Promise<InterviewResponse[]> => {
  const response = await axios.get(`${API_URL}/api/interviews`);
  return response.data;
};

export const getInterviewResults = async (interviewId: string): Promise<InterviewResult> => {
  const response = await axios.get(`${API_URL}/api/interviews/${interviewId}/results`);
  return response.data;
};