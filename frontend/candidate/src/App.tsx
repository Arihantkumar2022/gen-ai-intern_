import { Routes, Route } from 'react-router-dom';
import Interview from './pages/Interview';
import styled from 'styled-components';

const AppContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

const App: React.FC = () => {
  return (
    <AppContainer>
      <Routes>
        <Route path="/interview/:interviewId" element={<Interview />} />
      </Routes>
    </AppContainer>
  );
};

export default App;