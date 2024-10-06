// UserCard.tsx
import React from 'react';
import { Typography, IconButton } from '@mui/material';
import { Close as CloseIcon, Chat as ChatIcon } from '@mui/icons-material';
import {
  MotionUserCard,
  MotionUserPhoto,
  UserInfo,
  SwipeButtonsContainer,
} from '../styles/StyledComponents';
import { User } from '../types/User';

type UserCardProps = {
  user: User;
  handleSwipe: (direction: string) => void;
};

const UserCard: React.FC<UserCardProps> = ({ user, handleSwipe }) => {
  return (
    <MotionUserCard
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0.9, opacity: 0 }}
      whileTap={{ scale: 0.95 }}
    >
      <MotionUserPhoto
        src={user.photo}
        alt={`${user.name}'s photo`}
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        onDragEnd={(event, info) => {
          if (info.offset.x > 100) {
            handleSwipe('Right');
          } else if (info.offset.x < -100) {
            handleSwipe('Left');
          }
        }}
      />
      <UserInfo>
        <Typography variant="h6">
          {user.name}, {user.age}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Interests: {user.interests.join(', ')}
        </Typography>
      </UserInfo>
      <SwipeButtonsContainer>
        <IconButton
          color="secondary"
          onClick={() => handleSwipe('Left')}
          size="large"
          sx={{ backgroundColor: '#f8bbd0', '&:hover': { backgroundColor: '#f48fb1' } }}
        >
          <CloseIcon fontSize="large" />
        </IconButton>
        <IconButton
          color="primary"
          onClick={() => handleSwipe('Right')}
          size="large"
          sx={{ backgroundColor: '#c5cae9', '&:hover': { backgroundColor: '#9fa8da' } }}
        >
          <ChatIcon fontSize="large" />
        </IconButton>
      </SwipeButtonsContainer>
    </MotionUserCard>
  );
};

export default UserCard;