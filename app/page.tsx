"use client";

import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  CssBaseline,
  ThemeProvider,
  TextField,
  Button,
  Box,
  Paper,
  Container,
  FormGroup,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import { Settings as SettingsIcon } from '@mui/icons-material';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { SelectChangeEvent } from '@mui/material';

import { themes } from './themes/themes';
import { User } from './types/User';
import { Message } from './types/Message';
import { ThemeName } from './types/ThemeName';
import { UserProvider } from './context/userContext';
import FriendsPage from './components/FriendsPage';
import UserCardPage from './components/UserCardPage';
import ProspectivePage from './components/ProspectivePage';
import SettingsModal from './components/SettingsModal';

// Interests list
const unique_interests = [
  'Art', 'Cooking', 'Crafting', 'Education', 'Fashion', 'Finance',
  'Fitness', 'Gaming', 'History', 'Literature', 'Music', 'Nature',
  'Photography', 'Psychology', 'Science', 'Social Media', 'Sports',
  'Technology', 'Travel', 'Volunteering'
];

// LoginPage Component
const LoginPage: React.FC<{ onLogin: (username: string, password: string) => void }> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault(); // Prevent form submission
    onLogin(username, password);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 5 }}>
      <Box
        sx={{
          fontSize: '100px',
          animation: 'wave 1s infinite',
          '@keyframes wave': {
            '0%': { transform: 'rotate(0deg)' },
            '25%': { transform: 'rotate(15deg)' },
            '50%': { transform: 'rotate(0deg)' },
            '75%': { transform: 'rotate(-15deg)' },
            '100%': { transform: 'rotate(0deg)' },
          },
        }}
      >
        👋
      </Box>
      <Typography variant="h3" fontWeight="bold" gutterBottom>
        Welcome to Hi-Five!
      </Typography>
      <form onSubmit={handleLogin}>
        <TextField
          label="Username"
          variant="outlined"
          sx={{ mb: 2, width: '300px' }}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          label="Password"
          variant="outlined"
          type="password"
          sx={{ mb: 2, width: '300px' }}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit" variant="contained" color="primary">
          Login
        </Button>
      </form>
    </Box>
  );
};

// QuestionsPage Component
const QuestionsPage: React.FC<{ username: string; password: string; onQuestionsSubmit: (answers: any) => void }> = ({ username, password, onQuestionsSubmit }) => {
  const [answers, setAnswers] = useState({
    openness: '',
    conscientiousness: '',
    extraversion: '',
    agreeableness: '',
    neuroticism: '',
  });

  const handleAnswerChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    trait: string
  ) => {
    setAnswers((prev) => ({ ...prev, [trait]: event.target.value }));
  };

  const handleSubmitAnswers = () => {
    onQuestionsSubmit(answers);  // Pass the answers back to the parent component
  };

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Personality Questions
      </Typography>

      {/* Openness Question */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Openness</Typography>
        <Typography variant="body1">
          How do you feel about trying new experiences, like exploring unfamiliar places or learning
          something outside of your usual interests?
        </Typography>
        <TextField
          fullWidth
          multiline
          minRows={4}
          variant="outlined"
          value={answers.openness}
          onChange={(e) => handleAnswerChange(e, 'openness')}
          sx={{ mt: 2 }}
        />
      </Paper>

      {/* Conscientiousness Question */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Conscientiousness</Typography>
        <Typography variant="body1">
          When working on a project, how likely are you to create a detailed plan and stick to it
          until completion?
        </Typography>
        <TextField
          fullWidth
          multiline
          minRows={4}
          variant="outlined"
          value={answers.conscientiousness}
          onChange={(e) => handleAnswerChange(e, 'conscientiousness')}
          sx={{ mt: 2 }}
        />
      </Paper>

      {/* Extraversion Question */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Extraversion</Typography>
        <Typography variant="body1">
          Do you prefer spending time in large social gatherings, or do you feel more energized when
          you're alone or with a few close friends?
        </Typography>
        <TextField
          fullWidth
          multiline
          minRows={4}
          variant="outlined"
          value={answers.extraversion}
          onChange={(e) => handleAnswerChange(e, 'extraversion')}
          sx={{ mt: 2 }}
        />
      </Paper>

      {/* Agreeableness Question */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Agreeableness</Typography>
        <Typography variant="body1">
          How inclined are you to prioritize others’ needs and feelings, even if it means
          compromising your own preferences?
        </Typography>
        <TextField
          fullWidth
          multiline
          minRows={4}
          variant="outlined"
          value={answers.agreeableness}
          onChange={(e) => handleAnswerChange(e, 'agreeableness')}
          sx={{ mt: 2 }}
        />
      </Paper>

      {/* Neuroticism Question */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Neuroticism</Typography>
        <Typography variant="body1">
          When facing stressful situations, how often do you feel overwhelmed or anxious, as opposed
          to staying calm and composed?
        </Typography>
        <TextField
          fullWidth
          multiline
          minRows={4}
          variant="outlined"
          value={answers.neuroticism}
          onChange={(e) => handleAnswerChange(e, 'neuroticism')}
          sx={{ mt: 2 }}
        />
      </Paper>

      <Button variant="contained" color="primary" onClick={handleSubmitAnswers}>
        Submit Answers
      </Button>
    </Container>
  );
};

// InterestsPage Component
const InterestsPage: React.FC<{ username: string; password: string; answers: any; onInterestsSubmit: (selectedInterests: string[]) => void }> = ({ username, password, answers, onInterestsSubmit }) => {
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);

  const handleInterestChange = (interest: string) => {
    setSelectedInterests((prevSelected) =>
      prevSelected.includes(interest)
        ? prevSelected.filter((item) => item !== interest)
        : [...prevSelected, interest]
    );
  };

  const handleSubmitInterests = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/postCreateUser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          password,
          answers,
          interests: selectedInterests,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert('Thank you for submitting your answers and interests!');
      } else {
        alert('Failed to submit.');
      }
    } catch (error) {
      console.error('Error submitting:', error);
      alert('An error occurred while submitting.');
    }
  };

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Select Your Interests
      </Typography>

      <FormGroup>
        {unique_interests.map((interest) => (
          <FormControlLabel
            key={interest}
            control={
              <Checkbox
                checked={selectedInterests.includes(interest)}
                onChange={() => handleInterestChange(interest)}
              />
            }
            label={interest}
          />
        ))}
      </FormGroup>

      <Button variant="contained" color="primary" onClick={handleSubmitInterests}>
        Submit Interests
      </Button>
    </Container>
  );
};

// Main Page Component
const MainPage: React.FC = () => {
  const [themeName, setThemeName] = useState<ThemeName>('default');
  const theme = themes[themeName];
  const navigate = useNavigate();

  const [username, setUsername] = useState<string | null>(null);
  const [password, setPassword] = useState<string | null>(null);
  const [answers, setAnswers] = useState<any | null>(null);

  const handleLogin = (username: string, password: string) => {
    setUsername(username);
    setPassword(password);
    navigate('/questions');
  };

  const handleQuestionsSubmit = (answers: any) => {
    setAnswers(answers);
    navigate('/interests');
  };

  const handleInterestsSubmit = (selectedInterests: string[]) => {
    // All data (username, password, answers, and interests) will be sent via the API.
    console.log('Selected Interests:', selectedInterests);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" color="primary">
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <IconButton color="inherit" onClick={() => console.log('Settings')}>
            <SettingsIcon />
          </IconButton>
          <Typography variant="h6" fontWeight="bold">
            Hi-Five
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Navigation */}
      <nav style={{ padding: '10px', display: 'flex', justifyContent: 'space-around' }}>
        <Link to="/login">Login</Link>
        <Link to="/friends">Friends</Link>
        <Link to="/user-card">User Cards</Link>
        <Link to="/prospective">Prospective Matches</Link>
      </nav>

      {/* Route Definitions */}
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/questions" element={username && password && <QuestionsPage username={username} password={password} onQuestionsSubmit={handleQuestionsSubmit} />} />
        <Route path="/interests" element={username && password && answers && <InterestsPage username={username} password={password} answers={answers} onInterestsSubmit={handleInterestsSubmit} />} />
      </Routes>
    </ThemeProvider>
  );
};

// App Component: Wrapping with BrowserRouter
const App: React.FC = () => {
  return (
    <Router>
      <MainPage />
    </Router>
  );
};

export default App;
