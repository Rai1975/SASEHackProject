// src/types/User.ts
export type User = {
    id: string;
    name: string;
    age: number;
    photo: string;
    interests: string[];
    status: 'online' | 'offline' | 'busy' | 'away';
    friendshipStartDate?: Date;
  };
  