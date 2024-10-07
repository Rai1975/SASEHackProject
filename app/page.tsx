"use client";

import React, { useState, useEffect } from 'react';
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
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Chip,
} from '@mui/material';
import { Check as CheckIcon, Close as CloseIcon, Settings as SettingsIcon } from '@mui/icons-material';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';

import { themes } from './themes/themes';
import { ThemeName } from './types/ThemeName';

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
    bio: ''
  });

  const handleAnswerChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    trait: string
  ) => {
    setAnswers((prev) => ({ ...prev, [trait]: event.target.value }));
  };

  const handleSubmitAnswers = () => {
    onQuestionsSubmit(answers);  
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

      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Bio</Typography>
        <Typography variant="body1">
          Enter a quick little bio about yourself!
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
        onInterestsSubmit(selectedInterests); 
        
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

// ADDITION 1: UserCard Component with check and cross buttons
interface UserCardProps {
  pid: number;
  alias: string;
  interests: string[];
  bio: string[];
  onRemove: (pid: number) => void;
  onSelect: (user: { pid: number; alias: string }) => void;
}

const UserCard: React.FC<UserCardProps> = ({ pid, alias, interests, onRemove, onSelect }) => {
  return (
    <Card sx={{ minWidth: 275, margin: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {alias} {/* Render the alias */}
        </Typography>
        <Box sx={{ mt: 2 }}>
          {interests.map((interest, index) => (
            <Chip key={index} label={interest} sx={{ margin: 0.5 }} />
          ))}
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
          <IconButton color="primary" onClick={() => onSelect({ pid, alias })}>
            <CheckIcon />
          </IconButton>
          <IconButton color="secondary" onClick={() => onRemove(pid)}>
            <CloseIcon />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );
};

// ADDITION 2: ChatPage Component for chatting with selected users
const ChatPage: React.FC<{ selectedUser: { alias: string } }> = ({ selectedUser }) => {
  const [messages, setMessages] = useState([
    { sender: 'User', text: `Hi! My name is ${selectedUser.alias}.` },
    { sender: 'You', text: 'Nice to meet you! Do you like hiking?' },
    { sender: 'User', text: 'Yes! I love hiking, especially in the mountains.' }
  ]);
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      setMessages([...messages, { sender: 'You', text: newMessage }]);
      setNewMessage('');
    }
  };

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Chat with {selectedUser.alias}
      </Typography>
      <Box sx={{ border: '1px solid grey', borderRadius: 2, padding: 2, minHeight: '300px', mb: 2 }}>
        {messages.map((msg, index) => (
          <Typography key={index} align={msg.sender === 'You' ? 'right' : 'left'}>
            <strong>{msg.sender}:</strong> {msg.text}
          </Typography>
        ))}
      </Box>
      <TextField
        fullWidth
        variant="outlined"
        label="Type a message"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={handleSendMessage} sx={{ mt: 2 }}>
        Send
      </Button>
    </Container>
  );
};

// PotentialFriends Component to fetch and render the user cards
const PotentialFriends: React.FC = () => {
  const [friends, setFriends] = useState<UserCardProps[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedUser, setSelectedUser] = useState<{ pid: number; alias: string } | null>(null); // ADDITION 3: Manage selected user for chat

  useEffect(() => {
    const fetchPotentialFriends = async () => {
      try {
        const userId = "1"; // Hardcoded user ID
        const response = await fetch(`http://localhost:5000/api/getPotentialFriends/${userId}`);
        if (response.ok) {
          const data = await response.json();
          const friendsData = data.map((friend: any) => ({
            pid: friend[0],
            alias: friend[2],
            interests: friend[3],
            bio: friend[4],
          }));

          setFriends(friendsData);
        } else {
          console.error('Failed to fetch potential friends');
        }
      } catch (error) {
        console.error('Error fetching potential friends:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPotentialFriends();
  }, []);

  const handleRemoveFriend = (pid: number) => {
    setFriends((prevFriends) => prevFriends.filter((friend) => friend.pid !== pid));
  };

  const handleSelectFriend = (user: { pid: number; alias: string }) => {
    setSelectedUser(user); // ADDITION 4: Select user and open chat
  };

  if (loading) {
    return (
      <Container sx={{ textAlign: 'center', mt: 5 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Potential Friends
      </Typography>

      {selectedUser ? ( // ADDITION 5: Conditionally render chat or user cards
        <ChatPage selectedUser={selectedUser} /> // Chat interface if a user is selected
      ) : (
        <Grid container spacing={2}>
          {friends.map((friend) => (
            <Grid item xs={12} sm={6} md={4} key={friend.pid}>
              <UserCard
                pid={friend.pid}
                alias={friend.alias}
                interests={friend.interests}
                bio = {friend.bio}
                onRemove={handleRemoveFriend}
                onSelect={handleSelectFriend}
              />
            </Grid>
          ))}
        </Grid>
      )}
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
    console.log('Selected Interests:', selectedInterests);
    navigate('/user-cards');
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
        <Link to="/user-cards">User Cards</Link>
        <Link to="/prospective">Prospective Matches</Link>
      </nav>

      {/* Route Definitions */}
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/questions" element={username && password && <QuestionsPage username={username} password={password} onQuestionsSubmit={handleQuestionsSubmit} />} />
        <Route path="/interests" element={username && password && answers && <InterestsPage username={username} password={password} answers={answers} onInterestsSubmit={handleInterestsSubmit} />} />
        <Route path="/user-cards" element={<PotentialFriends />} />
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
