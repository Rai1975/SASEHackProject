// page.tsx
"use client";

import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  CssBaseline,
  ThemeProvider,
} from '@mui/material';
import { Settings as SettingsIcon } from '@mui/icons-material';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { SelectChangeEvent } from '@mui/material';

import { themes } from './themes/themes';
import { User } from './types/User';
import { Message } from './types/Message';
import { Task } from './types/Task';
import { ThemeName } from './types/ThemeName';
import ReactDOM from 'react-dom';
import { UserProvider, useUser } from './context/UserContext'; // Updated import
import FriendsPage from './components/FriendsPage';
import UserCardPage from './components/UserCardPage';
import ProspectivePage from './components/ProspectivePage';
import SettingsModal from './components/SettingsModal';

const Page: React.FC = () => {
  const [themeName, setThemeName] = useState<ThemeName>('default');
  const theme = themes[themeName];

  // State variables
  const [users, setUsers] = useState<User[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [matches, setMatches] = useState<User[]>([]);
  const [friends, setFriends] = useState<User[]>([]);
  const [selectedChatUser, setSelectedChatUser] = useState<User | null>(null);
  const [messages, setMessages] = useState<{ [key: string]: Message[] }>({});
  const [inputText, setInputText] = useState('');
  const [timers, setTimers] = useState<{ [key: string]: number }>({});
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [chatBackgrounds, setChatBackgrounds] = useState<{ [key: string]: string }>({});
  const [milestones, setMilestones] = useState<{ [key: string]: string[] }>({});

  // Access user data from context
  const { user, setUser } = useUser(); // Destructure user and setUser from context

  const handleThemeChange = (event: SelectChangeEvent<string>) => {
    setThemeName(event.target.value as ThemeName);
  };

  const navigatePage = (direction: 'left' | 'right') => {
    if (direction === 'left') {
      if (currentIndex > 0) {
        setCurrentIndex(currentIndex - 1);
      }
    } else if (direction === 'right') {
      if (currentIndex < users.length - 1) {
        setCurrentIndex(currentIndex + 1);
      }
    }
  };

  // Fetch current user from API when component mounts or when user.email changes
  useEffect(() => {
    const fetchCurrentUser = async () => {
      if (!user || !user.email) {
        console.error('No user or email available to fetch user data.');
        return;
      }
      try {
        const response = await fetch(`http://0.0.0.0:5000/api/userData?email=${encodeURIComponent(user.email)}`);
        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }
        const userData: User = await response.json();
        console.log(userData); // Handle the user data as needed
        setUser(userData); // Update user in context
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };
    fetchCurrentUser();
  }, [user?.email, setUser]); // Depend on user.email and setUser

  // Fetch potential friends when user.id changes
  useEffect(() => {
    const fetchUsers = async () => {
      if (!user || !user.id) {
        console.error('No user or user ID available to fetch potential friends.');
        return;
      }
      try {
        const response = await fetch(`http://0.0.0.0:5000/api/getPotentialFriends/${user.id}`); // API call
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }
        const data: User[] = await response.json();
        setUsers(data); // Set the users data
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
  
    fetchUsers();
  }, [user?.id]); 

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppBar position="static" color="primary">
          <Toolbar sx={{ justifyContent: 'space-between' }}>
            <IconButton color="inherit" onClick={() => setSettingsOpen(true)}>
              <SettingsIcon />
            </IconButton>
            <Typography variant="h6" fontWeight="bold">
              Hi-Five
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Navigation Links */}
        <nav style={{ padding: '10px', display: 'flex', justifyContent: 'space-around' }}>
          <Link to="/friends">Friends</Link>
          <Link to="/user-card">User Cards</Link>
          <Link to="/prospective">Prospective Matches</Link>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route
            path="/friends"
            element={
              <FriendsPage
                friends={friends}
                onSelectFriend={setSelectedChatUser}
                onRemoveFriend={(userId) => setFriends(friends.filter((f) => f.id !== userId))}
                milestones={milestones}
                onNavigate={navigatePage}
              />
            }
          />
          <Route
            path="/user-card"
            element={
              <UserCardPage
                users={users} {/* Fixed the incomplete prop */}
                currentIndex={currentIndex}
                handleSwipe={(direction) => {
                  if (direction === 'Right' && users[currentIndex]) {
                    setMatches((prevMatches) => [...prevMatches, users[currentIndex]]);
                  }
                  setCurrentIndex((prevIndex) => prevIndex + 1); // Use functional update
                }}
                onNavigate={navigatePage}
              />
            }
          />
          <Route
            path="/prospective"
            element={
              <ProspectivePage
                matches={matches}
                onSelectMatch={setSelectedChatUser}
                onAcceptMatch={(userId) => {
                  const userToAdd = matches.find((m) => m.id === userId);
                  if (userToAdd) {
                    setFriends((prevFriends) => [...prevFriends, userToAdd]); // Use functional update
                  }
                }}
                onRejectMatch={(userId) => setMatches((prevMatches) => prevMatches.filter((m) => m.id !== userId))}
                timers={timers}
                selectedChatUser={selectedChatUser}
                messages={messages}
                inputText={inputText}
                setInputText={setInputText}
                handleSendMessage={(text) => {
                  if (selectedChatUser) {
                    setMessages((prevMessages) => ({
                      ...prevMessages,
                      [selectedChatUser.id]: [
                        ...(prevMessages[selectedChatUser.id] || []),
                        { sender: 'me', text, timestamp: new Date() },
                      ],
                    }));
                  }
                }}
                onClose={() => setSelectedChatUser(null)}
                chatBackgrounds={selectedChatUser ? chatBackgrounds[selectedChatUser.id] : ''}
              />
            }
          />
        </Routes>

        {/* Settings Modal */}
        {settingsOpen && (
          <SettingsModal
            themeName={themeName}
            onThemeChange={handleThemeChange}
            onClose={() => setSettingsOpen(false)}
            selectedChatUserId={selectedChatUser?.id}
            chatBackgrounds={chatBackgrounds}
            onBackgroundChange={(background) => {
              if (selectedChatUser) {
                setChatBackgrounds((prev) => ({
                  ...prev,
                  [selectedChatUser.id]: background,
                }));
              }
            }}
          />
        )}
      </Router>
    </ThemeProvider>
  );
};

// Wrapping the Page component with UserProvider
const App: React.FC = () => {
  return (
    <UserProvider>
      <Page />
    </UserProvider>
  );
};

export default App;
