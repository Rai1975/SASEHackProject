// src/types/User.ts
export type User = {
    id: string;
    name: string;
    email: string;
    age: number;
    photo: string;
    interests: string[];
    status: 'online' | 'offline' | 'busy' | 'away';
  };
  