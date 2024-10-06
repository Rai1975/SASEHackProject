// src/components/AppContainer.tsx
import React from 'react';
import { AppContainer as StyledAppContainer } from '../styles/StyledComponents';

type AppContainerProps = {
  children: React.ReactNode;
};

const AppContainer: React.FC<AppContainerProps> = ({ children }) => {
  return <StyledAppContainer>{children}</StyledAppContainer>;
};

export default AppContainer;
