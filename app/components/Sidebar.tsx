// src/components/Sidebar.tsx
import React from 'react';
import { Typography, Divider } from '@mui/material';
import { SidebarContainer } from '../styles/StyledComponents';

type SidebarProps = {
  title: string;
  children: React.ReactNode;
};

const Sidebar: React.FC<SidebarProps> = ({ title, children }) => {
  return (
    <SidebarContainer>
      <Typography variant="h6" align="center" sx={{ padding: '10px' }}>
        {title}
      </Typography>
      <Divider />
      {children}
    </SidebarContainer>
  );
};

export default Sidebar;
