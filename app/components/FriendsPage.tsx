// FriendsPage.tsx
import React from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import { ArrowBack as ArrowBackIcon, ArrowForward as ArrowForwardIcon } from '@mui/icons-material';
import FriendsList from './FriendsList';
import { User } from '../types/User';

interface FriendsPageProps {
  friends: User[];
  onSelectFriend: (user: User) => void;
  onRemoveFriend: (userId: string) => void;
  milestones: { [key: string]: string[] };
  onNavigate: (direction: 'left' | 'right') => void;
}

const FriendsPage: React.FC<FriendsPageProps> = ({
  friends,
  onSelectFriend,
  onRemoveFriend,
  milestones,
  onNavigate,
}) => {
  return (
    <Box sx={{ height: '100%', padding: '20px', position: 'relative' }}>
      <IconButton
        onClick={() => onNavigate('right')}
        sx={{ position: 'absolute', top: '50%', right: '-40px', zIndex: 1 }}
      >
        <ArrowForwardIcon />
      </IconButton>
      <Typography variant="h5" mb={2}>
        Friends
      </Typography>
      <FriendsList
        friends={friends}
        onSelectFriend={onSelectFriend}
        onRemoveFriend={onRemoveFriend}
        milestones={milestones}
      />
    </Box>
  );
};

export default FriendsPage;
