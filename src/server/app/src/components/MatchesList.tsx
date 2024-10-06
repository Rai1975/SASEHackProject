// MatchesList.tsx
import React from 'react';
import {
  ListItem,
  ListItemButton,
  Badge,
  Avatar,
  ListItemText,
  IconButton,
} from '@mui/material';
import {
  Close as CloseIcon,
  Check as CheckIcon,
} from '@mui/icons-material';
import {
  MatchesListContainer,
  StatusIndicator,
} from '../styles/StyledComponents';
import { User } from '../types/User';
import { formatTime } from '../Utils/formatTime';

type MatchesListProps = {
  matches: User[];
  onSelectMatch: (user: User) => void;
  onAcceptMatch: (userId: string) => void;
  onRejectMatch: (userId: string) => void;
  timers: { [key: string]: number };
};

const MatchesList: React.FC<MatchesListProps> = ({
  matches,
  onSelectMatch,
  onAcceptMatch,
  onRejectMatch,
  timers,
}) => {
  return (
    <MatchesListContainer>
      {matches.map((user) => (
        <ListItem key={user.id} disablePadding>
          <ListItemButton onClick={() => onSelectMatch(user)}>
            <Badge
              variant="dot"
              color="success"
              invisible={user.status !== 'online'}
              overlap="circular"
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
            >
              <Avatar src={user.photo} sx={{ marginRight: '10px' }} />
            </Badge>
            <ListItemText
              primary={
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <StatusIndicator status={user.status} />
                  {user.name}
                </div>
              }
              secondary={`Time Left: ${formatTime(timers[user.id])}`}
            />
            <IconButton onClick={() => onRejectMatch(user.id)}>
              <CloseIcon />
            </IconButton>
            <IconButton onClick={() => onAcceptMatch(user.id)}>
              <CheckIcon />
            </IconButton>
          </ListItemButton>
        </ListItem>
      ))}
    </MatchesListContainer>
  );
};

export default MatchesList;