import React from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import { ArrowBack as ArrowBackIcon, ArrowForward as ArrowForwardIcon } from '@mui/icons-material';
import UserCard from '../components/UserCard';
import { User } from '../types/User';

interface UserCardPageProps {
  users: User[];
  currentIndex: number;
  handleSwipe: (direction: string) => void;
  onNavigate: (direction: 'left' | 'right') => void;
}

const UserCardPage: React.FC<UserCardPageProps> = ({ users, currentIndex, handleSwipe, onNavigate }) => {
  return (
    <Box sx={{ height: '100%', padding: '20px', position: 'relative' }}>
      <IconButton
        onClick={() => onNavigate('left')}
        sx={{ position: 'absolute', top: '50%', left: '-40px', zIndex: 1 }}
      >
        <ArrowBackIcon />
      </IconButton>
      <IconButton
        onClick={() => onNavigate('right')}
        sx={{ position: 'absolute', top: '50%', right: '-40px', zIndex: 1 }}
      >
        <ArrowForwardIcon />
      </IconButton>
      <Typography variant="h5" mb={2}>
        User Card
      </Typography>
      {users[currentIndex] ? (
        <UserCard user={users[currentIndex]} handleSwipe={handleSwipe} />
      ) : (
        <Typography variant="h6">No more users available.</Typography>
      )}
    </Box>
  );
};

export default UserCardPage;
