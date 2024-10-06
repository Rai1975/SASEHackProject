// src/themes/themes.ts
import { createTheme } from '@mui/material';

export const themes = {
  default: createTheme({
    palette: {
      primary: { main: '#673ab7' },
      secondary: { main: '#ff9800' },
    },
    typography: { fontFamily: 'Roboto, sans-serif' },
  }),
  dark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#90caf9' },
      secondary: { main: '#f48fb1' },
    },
    typography: { fontFamily: 'Roboto, sans-serif' },
  }),
  vibrant: createTheme({
    palette: {
      primary: { main: '#e91e63' },
      secondary: { main: '#00bcd4' },
    },
    typography: { fontFamily: 'Roboto, sans-serif' },
  }),
};
