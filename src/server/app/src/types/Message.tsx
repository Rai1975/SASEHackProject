// src/types/Message.ts
export type Message = {
    sender: 'me' | 'them';
    text: string;
    timestamp: Date;
    reactions?: { [key: string]: number };
    repliedTo?: Message;
  };
  