// src/components/HealthDashboard.tsx
import React from 'react';
import { Typography } from '@mui/material';
import { HealthDashboardContainer } from '../styles/StyledComponents';
import { User } from '../types/User';

type HealthDashboardProps = {
  friends: User[];
  lastInteraction: { [key: string]: Date };
};

const HealthDashboard: React.FC<HealthDashboardProps> = ({
  friends,
  lastInteraction,
}) => {
  return (
    <HealthDashboardContainer>
      <Typography variant="h6">Friendship Health</Typography>
      {friends.map((user) => {
        const lastMsgDate = lastInteraction[user.id];
        const daysSinceLastMsg = lastMsgDate
          ? Math.floor((new Date().getTime() - lastMsgDate.getTime()) / (1000 * 60 * 60 * 24))
          : 'No interactions yet';
        return (
          <Typography key={user.id} variant="body1">
            {user.name}: {typeof daysSinceLastMsg === 'number' ? `${daysSinceLastMsg} day(s) ago` : daysSinceLastMsg}
          </Typography>
        );
      })}
    </HealthDashboardContainer>
  );
};

export default HealthDashboard;
