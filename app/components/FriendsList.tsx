// FriendsList.tsx
import React from 'react';
import {
  ListItem,
  ListItemButton,
  Badge,
  Avatar,
  ListItemText,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Close as CloseIcon,
  Report as ReportIcon,
  EmojiEvents as EmojiEventsIcon,
} from '@mui/icons-material';
import { FriendsListContainer, StatusIndicator } from '../styles/StyledComponents';
import { User } from '../types/User';

type FriendsListProps = {
  friends: User[];
  onSelectFriend: (user: User) => void;
  onRemoveFriend: (userId: string) => void;
  milestones: { [key: string]: string[] };
};

const FriendsList: React.FC<FriendsListProps> = ({
  friends,
  onSelectFriend,
  onRemoveFriend,
  milestones,
}) => {
  return (
    <FriendsListContainer>
      {friends.map((user) => (
        <ListItem key={user.id} disablePadding>
          <ListItemButton onClick={() => onSelectFriend(user)}>
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
                  {milestones[user.id]?.includes('1_month') && (
                    <Tooltip title="1 Month of Friendship">
                      <EmojiEventsIcon color="primary" sx={{ marginLeft: '20px' }} />
                    </Tooltip>
                  )}
                </div>
              }
            />
            <IconButton onClick={() => onRemoveFriend(user.id)}>
              <CloseIcon />
            </IconButton>
            <IconButton color="secondary">
              <ReportIcon />
            </IconButton>
          </ListItemButton>
        </ListItem>
      ))}
    </FriendsListContainer>
  );
};

export default FriendsList;
