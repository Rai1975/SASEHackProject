// ProspectivePage.tsx
import React from 'react';
import { Box, Typography } from '@mui/material';
import MatchesList from './MatchesList';
import Chat from './Chat';
import { User } from '../types/User';
import { Message } from '../types/Message';

interface ProspectivePageProps {
  matches: User[];
  onSelectMatch: (user: User) => void;
  onAcceptMatch: (userId: string) => void;
  onRejectMatch: (userId: string) => void;
  timers: { [key: string]: number };
  selectedChatUser: User | null;
  messages: { [key: string]: Message[] };
  inputText: string;
  setInputText: (text: string) => void;
  handleSendMessage: (text: string) => void;
  onClose: () => void;
  chatBackgrounds: string;
}

const ProspectivePage: React.FC<ProspectivePageProps> = ({
    matches,
    onSelectMatch,
    onAcceptMatch,
    onRejectMatch,
    timers,
    selectedChatUser,
    messages,
    inputText,
    setInputText,
    handleSendMessage,
    onClose,
    chatBackgrounds,
  }) => {
    const userMessages = selectedChatUser ? messages[selectedChatUser.id] || [] : [];
  
    return (
      <Box>
        {/* Existing UI Elements */}
        {selectedChatUser && (
          <Chat
            selectedUser={selectedChatUser}
            messages={userMessages}  // Use userMessages here
            onClose={onClose}
            onSendMessage={handleSendMessage}
            inputText={inputText}
            setInputText={setInputText}
            chatBackground={chatBackgrounds}
          />
        )}
      </Box>
    );
  };
  

export default ProspectivePage;
