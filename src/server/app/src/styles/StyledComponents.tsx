// src/styles/StyledComponents.tsx
import { styled } from '@mui/material/styles';
import { List, Toolbar, IconButton, Paper, Modal } from '@mui/material';
import { motion } from 'framer-motion';

export const AppContainer = styled('div')({
  display: 'flex',
  height: '100vh',
});

export const SidebarContainer = styled('div')(({ theme }) => ({
  width: '25%',
  backgroundColor: theme.palette.background.paper,
  overflowY: 'auto',
  borderRight: `1px solid ${theme.palette.divider}`,
}));

export const MainContent = styled('div')({
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
});

export const MatchesListContainer = styled(List)({
  padding: 0,
});

export const FriendsListContainer = styled(List)({
  padding: 0,
});

export const MotionUserCard = styled(motion.div)(({ theme }) => ({
  width: 350,
  maxWidth: '90%',
  margin: '20px auto',
  overflow: 'hidden',
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[3],
}));

export const MotionUserPhoto = styled(motion.img)({
  width: '100%',
  height: 300,
  objectFit: 'cover',
});

export const UserInfo = styled('div')({
  padding: '16px',
});

export const SwipeButtonsContainer = styled('div')({
  display: 'flex',
  justifyContent: 'space-around',
  marginTop: 20,
});

export const ChatContainer = styled('div')<{ backgroundImage: string }>(({ backgroundImage }) => ({
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  backgroundImage: `url(${backgroundImage})`,
  backgroundSize: 'cover',
}));

export const MessagesContainer = styled('div')({
  flex: 1,
  overflowY: 'auto',
  padding: '10px',
});

export const MessageBubble = styled(Paper)<{ isUser: boolean }>(({ isUser, theme }) => ({
  maxWidth: '70%',
  marginBottom: '10px',
  alignSelf: isUser ? 'flex-end' : 'flex-start',
  backgroundColor: isUser ? theme.palette.primary.main : theme.palette.background.paper,
  color: isUser ? '#fff' : '#000',
  padding: '10px',
  borderRadius: '10px',
  position: 'relative',
}));

export const InputContainer = styled('div')({
  display: 'flex',
  padding: '10px',
});

export const StickyHeader = styled(Toolbar)({
  position: 'sticky',
  top: 0,
  zIndex: 1,
  backgroundColor: 'inherit',
});

export const HealthDashboardContainer = styled('div')({
  padding: '20px',
});

export const ReactionIcon = styled(IconButton)({
  padding: '5px',
});

export const StatusIndicator = styled('span')<{ status: string }>(({ status }) => ({
  display: 'inline-block',
  width: '10px',
  height: '10px',
  borderRadius: '50%',
  backgroundColor:
    status === 'online'
      ? 'green'
      : status === 'offline'
      ? 'gray'
      : status === 'busy'
      ? 'red'
      : 'yellow',
  marginRight: '5px',
}));

export const TaskListContainer = styled(List)({
  width: '100%',
});

export const SettingsModalContainer = styled(Modal)({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
});
