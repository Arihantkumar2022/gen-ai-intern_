import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { FileUploader } from '../components/FileUploader';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { createInterview } from '../services/api';

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 600px;
  margin: 0 auto;
`;

const TextArea = styled.textarea`
  min-height: 150px;
  resize: vertical;
`;

const Input = styled.input`
  padding: 10px;
`;

const SubmitButton = styled.button`
  align-self: flex-start;
`;

const SuccessMessage = styled.div`
  background-color: #d4edda;
  color: #155724;
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
`;

const ErrorMessage = styled.div`
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
`;

const InterviewSetup: React.FC = () => {
  const [cv, setCv] = useState<File | null>(null);
  const [jd, setJd] = useState<File | null>(null);
  const [systemPrompt, setSystemPrompt] = useState('');
  const [interviewerName, setInterviewerName] = useState('AI Interviewer');
  const [maxQuestions, setMaxQuestions] = useState(10);
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState<string>('');
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cv || !jd || !systemPrompt) {
      setError('Please provide CV, Job Description, and System Prompt.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await createInterview({
        cv,
        jd,
        systemPrompt,
        interviewerName,
        maxQuestions,
      });
      setSuccess(`Interview created! Candidate URL: ${window.location.origin}${response.candidate_url}`);
    } catch (err: any) {
      setError(err.message || 'Failed to create interview.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2>Create New Interview</h2>
      <Form onSubmit={handleSubmit}>
        <FileUploader label="Upload Candidate CV (PDF)" onChange={setCv} />
        <FileUploader label="Upload Job Description (PDF)" onChange={setJd} />
        <div>
          <label>System Prompt</label>
          <TextArea
            value={systemPrompt}
            onChange={(e) => setSystemPrompt(e.target.value)}
            placeholder="Enter the system prompt for the AI interviewer..."
            required
          />
        </div>
        <div>
          <label>Interviewer Name</label>
          <Input
            type="text"
            value={interviewerName}
            onChange={(e) => setInterviewerName(e.target.value)}
            placeholder="AI Interviewer"
          />
        </div>
        <div>
          <label>Max Questions</label>
          <Input
            type="number"
            value={maxQuestions}
            onChange={(e) => setMaxQuestions(Number(e.target.value))}
            min="1"
            max="50"
          />
        </div>
        <SubmitButton type="submit" disabled={isLoading}>
          Create Interview
        </SubmitButton>
      </Form>
      {isLoading && <LoadingSpinner />}
      {success && <SuccessMessage>{success}</SuccessMessage>}
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </div>
  );
};

export default InterviewSetup;