import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { LiveAudioVisualizer } from '@livekit/components-react';
import { Room, RoomEvent } from 'livekit-client';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { getInterviewDetails, getLiveKitToken } from '../services/api';

const InterviewContainer = styled.div`
  text-align: center;
`;

const QuestionDisplay = styled.div`
  margin: 20px 0;
  padding: 20px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const AudioPlayer = styled.audio`
  margin: 10px 0;
`;

const VisualizerContainer = styled.div`
  margin: 20px 0;
`;

const Message = styled.div`
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
  background-color: ${(props: { type: string }) =>
    props.type === 'error' ? '#f8d7da' : '#d4edda'};
  color: ${(props) => (props.type === 'error' ? '#721c24' : '#155724')};
`;

const Interview: React.FC = () => {
  const { interviewId } = useParams<{ interviewId: string }>();
  const [room, setRoom] = useState<Room | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<string>('');
  const [audioUrl, setAudioUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const setupInterviewchrom = async () => {
      if (!interviewId) {
        setError('Invalid interview ID.');
        setIsLoading(false);
        return;
      }

      try {
        // Fetch interview details
        const details = await getInterviewDetails(interviewId);
        if (details.status === 'completed') {
          setError('This interview has already been completed.');
          setIsLoading(false);
          return;
        }

        // Get LiveKit token
        const tokenResponse = await getLiveKitToken(interviewId, 'Candidate');
        const token = tokenResponse.token;

        // Initialize LiveKit room
        const room = new Room();
        await room.connect(import.meta.env.VITE_API_URL.replace('http', 'ws') || 'ws://localhost:8000', token);
        setRoom(room);

        // Request microphone access
        await room.localParticipant.enableMicrophone();

        // Setup WebSocket
        wsRef.current = new WebSocket(`${import.meta.env.VITE_API_URL}/api/ws/interview/${interviewId}`);

        wsRef.current.onopen = () => {
          console.log('WebSocket connected');
        };

        wsRef.current.onmessage = async (event) => {
          const data = JSON.parse(event.data);
          switch (data.type) {
            case 'greeting':
            case 'question':
              setCurrentQuestion(data.text);
              setAudioUrl(`${import.meta.env.VITE_API_URL}${data.audio_url}`);
              break;
            case 'completion':
              setMessage('Interview completed. Thank you for participating!');
              setCurrentQuestion('');
              setAudioUrl('');
              break;
            case 'results':
              setMessage(`Rating: ${data.rating}/10. Verdict: ${data.verdict}`);
              break;
            case 'error':
              setError(data.message);
              break;
          }
        };

        wsRef.current.onerror = () => {
          setError('WebSocket connection failed.');
        };

        wsRef.current.onclose = () => {
          setMessage('Interview session closed.');
        };

        // Send audio data
        room.on(RoomEvent.AudioTrackPublished, async (track) => {
          const stream = track.audioStream;
          if (stream) {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
              if (event.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
                event.data.arrayBuffer().then((buffer) => {
                  const base64 = btoa(
                    new Uint8Array(buffer).reduce(
                      (data, byte) => data + String.fromCharCode(byte),
                      ''
                    )
                  );
                  wsRef.current?.send(
                    JSON.stringify({
                      type: 'response',
                      audio_data: base64,
                    })
                  );
                });
              }
            };
            mediaRecorder.start(1000); // Send audio chunks every second
          }
        });

        setIsLoading(false);
      } catch (err: any) {
        setError(err.message || 'Failed to setup interview.');
        setIsLoading(false);
      }
    };

    setupInterview();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (room) {
        room.disconnect();
      }
    };
  }, [interviewId]);

  return (
    <InterviewContainer>
      <h2>AI Interview</h2>
      {isLoading ? (
        <LoadingSpinner />
      ) : error ? (
        <Message type="error">{error}</Message>
      ) : (
        <>
          {currentQuestion && (
            <QuestionDisplay>
              <p>{currentQuestion}</p>
              {audioUrl && <AudioPlayer controls src={audioUrl} autoPlay />}
            </QuestionDisplay>
          )}
          {room && (
            <VisualizerContainer>
              <LiveAudioVisualizer participant={room.localParticipant} />
            </VisualizerContainer>
          )}
          {message && <Message type="success">{message}</Message>}
        </>
      )}
    </InterviewContainer>
  );
};

export default Interview;