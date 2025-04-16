import { Link } from 'react-router-dom';
import styled from 'styled-components';

const HomeContainer = styled.div`
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 20px;
`;

const Button = styled(Link)`
  display: inline-block;
  text-decoration: none;
  margin: 10px;
`;

const Home: React.FC = () => {
  return (
    <HomeContainer>
      <Title>AI Interviewer Admin Dashboard</Title>
      <Button to="/setup">Create New Interview</Button>
      <Button to="/results">View Past Interviews</Button>
    </HomeContainer>
  );
};

export default Home;