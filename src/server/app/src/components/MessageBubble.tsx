// src/components/MessageBubble.tsx
import React from 'react';
import { Typography, IconButton, Paper } from '@mui/material';
import {
  ThumbUp as ThumbUpIcon,
  Favorite as FavoriteIcon,
  EmojiEmotions as EmojiEmotionsIcon,
  Reply as ReplyIcon,
} from '@mui/icons-material';
import { MotionPaper } from './MotionPaper';
import { ReactionIcon } from '../styles/StyledComponents';
import { Message } from '../types/Message';

type MessageBubbleProps = {
  message: Message;
  isUser: boolean;
  onReaction: (reaction: string) => void;
  onReply: () => void;
};

const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  isUser,
  onReaction,
  onReply,
}) => {
  return (
    <MotionPaper
      elevation={3}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      sx={{
        maxWidth: '70%',
        marginBottom: '10px',
        alignSelf: isUser ? 'flex-end' : 'flex-start',
        backgroundColor: isUser ? 'primary.main' : 'background.paper',
        color: isUser ? '#fff' : '#000',
        padding: '10px',
        borderRadius: '10px',
        position: 'relative',
      }}
    >
      {message.repliedTo && (
        <Paper
          sx={{
            padding: '5px',
            backgroundColor: '#f0f0f0',
            marginBottom: '5px',
          }}
        >
          <Typography variant="caption">
            {message.repliedTo.sender}: {message.repliedTo.text}
          </Typography>
        </Paper>
      )}
      <Typography>{message.text}</Typography>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <ReactionIcon onClick={() => onReaction('👍')}>
          <ThumbUpIcon fontSize="small" />
        </ReactionIcon>
        <ReactionIcon onClick={() => onReaction('❤️')}>
          <FavoriteIcon fontSize="small" />
        </ReactionIcon>
        <ReactionIcon onClick={() => onReaction('😂')}>
          <EmojiEmotionsIcon fontSize="small" />
        </ReactionIcon>
        <IconButton
          onClick={onReply}
          size="small"
          sx={{ marginLeft: 'auto' }}
        >
          <ReplyIcon fontSize="small" />
        </IconButton>
      </div>
      {message.reactions && (
        <Typography variant="caption">
          {Object.entries(message.reactions).map(
            ([emoji, count]) => `${emoji} ${count} `
          )}
        </Typography>
      )}
    </MotionPaper>
  );
};

export default MessageBubble;
