import React from 'react';
import { Box, Typography, IconButton } from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Sidebar';
import MatchesList from './MatchesList';
import { User } from '../types/User';

type MatchesScreenProps = {
  matches: User[];
  onSelectMatch: (user: User) => void;
  onAcceptMatch: (userId: string) => void;
  onRejectMatch: (userId: string) => void;
  timers: { [key: string]: number };
};

const MatchesScreen: React.FC<MatchesScreenProps> = ({
  matches,
  onSelectMatch,
  onAcceptMatch,
  onRejectMatch,
  timers,
}) => {
  const navigate = useNavigate();

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', padding: 2 }}>
        <IconButton onClick={() => navigate('/home')} color="primary">
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h5" sx={{ marginLeft: 2 }}>
          Matches
        </Typography>
      </Box>
      <Sidebar title="Matches">
        <MatchesList
          matches={matches}
          onSelectMatch={onSelectMatch}
          onAcceptMatch={onAcceptMatch}
          onRejectMatch={onRejectMatch}
          timers={timers}
        />
      </Sidebar>
    </Box>
  );
};

export default MatchesScreen;
