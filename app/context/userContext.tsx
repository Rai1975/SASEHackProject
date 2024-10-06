// src/context/UserContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { User } from '../types/User';

// Define the shape of the context
interface UserContextType {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

// Create the context with default values
const UserContext = createContext<UserContextType>({
  user: null,
  setUser: () => {},
});

// Custom hook to use the UserContext
export const useUser = () => {
  return useContext(UserContext);
};

// Provider component to wrap your app
interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};
