import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { getInterviewResults, listInterviews } from '../services/api';

const ResultsContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const Transcript = styled.div`
  margin: 20px 0;
  padding: 20px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const TranscriptEntry = styled.div`
  margin-bottom: 10px;
  strong {
    color: ${(props: { speaker: string }) =>
      props.speaker === 'ai' ? '#007bff' : '#28a745'};
  }
`;

const InterviewResults: React.FC = () => {
  const { interviewId } = useParams<{ interviewId: string }>();
  const [results, setResults] = useState<any>(null);
  const [interviews, setInterviews] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        if (interviewId) {
          const result = await getInterviewResults(interviewId);
          setResults(result);
        } else {
          const interviewList = await listInterviews();
          setInterviews(interviewList);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to fetch data.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [interviewId]);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <div>Error: {error}</div>;

  return (
    <ResultsContainer>
      <h2>{interviewId ? 'Interview Results' : 'All Interviews'}</h2>
      {interviewId && results ? (
        <>
          <p><strong>Rating:</strong> {results.rating}/10</p>
          <p><strong>Verdict:</strong> {results.verdict}</p>
          <h3>Detailed Feedback</h3>
          <ul>
            {results.detailed_feedback?.strengths?.map((s: string, i: number) => (
              <li key={i}>Strength: {s}</li>
            ))}
            {results.detailed_feedback?.weaknesses?.map((w: string, i: number) => (
              <li key={i}>Weakness: {w}</li>
            ))}
          </ul>
          <h3>Transcript</h3>
          <Transcript>
            {results.transcript.map((entry: any, index: number) => (
              <TranscriptEntry key={index} speaker={entry.speaker}>
                <strong>{entry.speaker === 'ai' ? 'AI:' : 'Candidate:'}</strong> {entry.text}
              </TranscriptEntry>
            ))}
          </Transcript>
        </>
      ) : (
        <ul>
          {interviews.map((interview) => (
            <li key={interview.interview_id}>
              <a href={`/results/${interview.interview_id}`}>
                Interview {interview.interview_id} ({interview.status})
              </a>
            </li>
          ))}
        </ul>
      )}
    </ResultsContainer>
  );
};

export default InterviewResults;