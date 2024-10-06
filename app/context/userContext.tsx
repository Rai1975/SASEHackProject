// src/context/UserContext.tsx
import React, { createContext, useContext } from 'react';
import { User } from '../types/User';

// Create the context
const UserContext = createContext<User | null>(null);

// Custom hook to use the context
export const useUser = () => {
  return useContext(UserContext);
};

// Provider component to wrap your app
export const UserProvider: React.FC<{ user: User }> = ({ user }) => {
  return <UserContext.Provider value={user}></UserContext.Provider>;
};
