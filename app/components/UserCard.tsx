// UserCard.tsx
import { useState, useEffect } from 'react';
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
  handleSwipe: (direction: string, currentUserId: number, targetUserId: number) => void;
};

const UserCard: React.FC<UserCardProps> = ({ user, handleSwipe }) => {
  const onSwipe = async (direction: string) => {
    if (direction === 'Right') {
      const id1 = user.id; // User who is swiping
      const id2 = target_user.id; // The user being swiped on

      try {
        const response = await fetch(`http://0.0.0.0:3000/api/swipeRight/${id1}/${id2}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({}),
        });

        const data = await response.json();
        console.log(data.message);
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  return (
    <MotionUserCard
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0.9, opacity: 0 }}
      whileTap={{ scale: 0.95 }}
    >
      <MotionUserPhoto

        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        onDragEnd={(event, info) => {
          if (info.offset.x > 100) {
            const handleSwipe = async (direction: string) => {
              try {
                const response = await fetch('0.0.0.0:5000/api/swipeRight/', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                    userId: user.id, // Assuming `user.id` is available
                    direction,
                  }),
                });

                const data = await response.json();
                console.log(data.message);
              } catch (error) {
                console.error('Error:', error);
              }
            };


            onSwipe('Right');

          } else if (info.offset.x < -100) {
            onSwipe('Left');
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
          onClick={() => onSwipe('Left')}
          size="large"
          sx={{ backgroundColor: '#f8bbd0', '&:hover': { backgroundColor: '#f48fb1' } }}
        >
          <CloseIcon fontSize="large" />
        </IconButton>
        <IconButton
          color="primary"
          onClick={() => onSwipe('Right')}
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