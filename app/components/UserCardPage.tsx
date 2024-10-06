import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import UserCard from './UserCard'; // Assuming you already have a UserCard component
import { User } from '../types/User'; // Make sure the User type is defined properly

type UserCardPageProps = {
  users: User[];  // Users array to display cards
  currentIndex: number;  // Index of current user to display
  handleSwipe: (direction: string) => void;  // Function to handle swipe (right/left)
  onNavigate: (direction: 'left' | 'right') => void;  // Navigation function (previous/next)
};

const UserCardPage: React.FC<UserCardPageProps> = ({
  users,
  currentIndex,
  handleSwipe,
  onNavigate,
}) => {
  const currentUser = users[currentIndex]; // Get current user based on index

  return (
    <Box sx={{ p: 5, backgroundColor: '#f5f5f5', textAlign: 'center', minHeight: '100vh' }}>
      <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#ff4081', mb: 4 }}>
        Meet New Friends!
      </Typography>

      {users.length > 0 && currentUser ? (
        <UserCard user={currentUser} />  // Pass current user to UserCard
      ) : (
        <Typography variant="h5" sx={{ color: '#757575', mt: 4 }}>
          No more users to display.
        </Typography>
      )}

      <Box sx={{ mt: 3 }}>
        <Button
          variant="contained"
          color="secondary"
          sx={{ mx: 1, backgroundColor: '#ff1744', fontWeight: 'bold', fontSize: '18px' }}
          onClick={() => handleSwipe('left')}  // Handle left swipe
        >
          Pass
        </Button>
        <Button
          variant="contained"
          color="primary"
          sx={{ mx: 1, backgroundColor: '#00e676', fontWeight: 'bold', fontSize: '18px' }}
          onClick={() => handleSwipe('right')}  // Handle right swipe
        >
          Like
        </Button>
      </Box>

      <Box sx={{ mt: 4 }}>
        <Button
          variant="outlined"
          color="primary"
          sx={{ mx: 1, fontWeight: 'bold', fontSize: '16px' }}
          onClick={() => onNavigate('left')}  // Navigate to previous card
        >
          Previous
        </Button>
        <Button
          variant="outlined"
          color="primary"
          sx={{ mx: 1, fontWeight: 'bold', fontSize: '16px' }}
          onClick={() => onNavigate('right')}  // Navigate to next card
        >
          Next
        </Button>
      </Box>
    </Box>
  );
};

export default UserCardPage;
