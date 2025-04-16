import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getInterviewDetails = async (interviewId: string): Promise<any> => {
  const response = await axios.get(`${API_URL}/api/candidate/interviews/${interviewId}/join`);
  return response.data;
};

export const getLiveKitToken = async (
  interviewId: string,
  participantName: string
): Promise<{ token: string }> => {
  const response = await axios.post(`${API_URL}/api/candidate/interviews/${interviewId}/livekit-token`, {
    participant_name: participantName,
  });
  return response.data;
};