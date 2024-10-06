// src/components/SwipeButtons.tsx

import React from 'react';
import { IconButton } from '@mui/material';
import { Close as CloseIcon, Chat as ChatIcon } from '@mui/icons-material';
import { SwipeButtonsContainer } from '../styles/StyledComponents';

type SwipeButtonsProps = {
  handleSwipe: (direction: string) => void;
};

const SwipeButtons: React.FC<SwipeButtonsProps> = ({ handleSwipe }) => {
  return (
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
  );
};

export default SwipeButtons;
