// src/components/MessagesList.tsx
import React from 'react';
import { MessagesContainer } from '../styles/StyledComponents';
import { Message } from '../types/Message';
import MessageBubble from './MessageBubble';

type MessagesListProps = {
  messages: Message[];
  onReaction: (index: number, reaction: string) => void;
  onReply: (message: Message) => void;
};

const MessagesList: React.FC<MessagesListProps> = ({
  messages,
  onReaction,
  onReply,
}) => {
  return (
    <MessagesContainer>
      {messages.map((message, index) => (
        <MessageBubble
          key={index}
          message={message}
          isUser={message.sender === 'me'}
          onReaction={(reaction) => onReaction(index, reaction)}
          onReply={() => onReply(message)}
        />
      ))}
    </MessagesContainer>
  );
};

export default MessagesList;
