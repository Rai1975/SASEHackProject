// Chat.tsx
import React from 'react';
import {
  Box,
  Typography,
  IconButton,
  TextField,
} from '@mui/material';
import {
  Close as CloseIcon,
  Send as SendIcon,
  Report as ReportIcon,
} from '@mui/icons-material';
import {
  ChatContainer,
  MessagesContainer,
  InputContainer,
  StickyHeader,
} from '../styles/StyledComponents';
import { Message } from '../types/Message';
import { User } from '../types/User';
import MessageBubble from './MessageBubble';

type ChatProps = {
  selectedUser: User;
  messages: Message[];
  onClose: () => void;
  onSendMessage: (text: string) => void;
  inputText: string;
  setInputText: (text: string) => void;
  chatBackground: string;
};

const Chat: React.FC<ChatProps> = ({
  selectedUser,
  messages,
  onClose,
  onSendMessage,
  inputText,
  setInputText,
  chatBackground,
}) => {
  const handleSendMessage = () => {
    if (inputText.trim() !== '') {
      onSendMessage(inputText);
      setInputText('');
    }
  };

  return (
    <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', border: '1px solid #ccc' }}>
      <StickyHeader>
        <IconButton edge="start" color="inherit" onClick={onClose}>
          <CloseIcon />
        </IconButton>
        <Typography variant="h6">{selectedUser.name}</Typography>
        <IconButton color="secondary" sx={{ marginLeft: 'auto', animation: 'pulse 1s infinite' }}>
          <ReportIcon />
        </IconButton>
      </StickyHeader>
      <ChatContainer backgroundImage={chatBackground}>
        <MessagesContainer>
          {messages.map((message, index) => (
            <MessageBubble
              key={index}
              message={message}
              isUser={message.sender === 'me'}
              onReaction={(reaction) => {
                /* Implement reaction handler */
              }}
              onReply={() => {
                /* Implement reply handler */
              }}
            />
          ))}
        </MessagesContainer>
        <InputContainer>
          <TextField
            variant="outlined"
            fullWidth
            placeholder="Type your message..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSendMessage();
              }
            }}
          />
          <IconButton color="primary" onClick={handleSendMessage}>
            <SendIcon />
          </IconButton>
        </InputContainer>
      </ChatContainer>
    </Box>
  );
};

export default Chat;