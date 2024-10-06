// SettingsModal.tsx
import React from 'react';
import {
  Modal,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
} from '@mui/material';
import { SelectChangeEvent } from '@mui/material';
import { ThemeName } from '../types/ThemeName';

interface SettingsModalProps {
  themeName: ThemeName;
  onThemeChange: (event: SelectChangeEvent<string>) => void;
  onClose: () => void;
  selectedChatUserId?: string; // Optional selected user
  chatBackgrounds: { [key: string]: string };
  onBackgroundChange: (background: string) => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({
  themeName,
  onThemeChange,
  onClose,
  selectedChatUserId,
  chatBackgrounds,
  onBackgroundChange,
}) => {
  return (
    <Modal open={true} onClose={onClose}>
      <Paper sx={{ padding: '20px', minWidth: '300px' }}>
        <Typography variant="h6">Settings</Typography>
        <FormControl fullWidth sx={{ marginTop: '10px' }}>
          <InputLabel>Theme</InputLabel>
          <Select value={themeName} label="Theme" onChange={onThemeChange}>
            <MenuItem value="default">Default</MenuItem>
            <MenuItem value="dark">Dark</MenuItem>
            <MenuItem value="vibrant">Vibrant</MenuItem>
          </Select>
        </FormControl>
        {selectedChatUserId && (
          <FormControl fullWidth sx={{ marginTop: '10px' }}>
            <InputLabel>Chat Background</InputLabel>
            <Select
              value={chatBackgrounds[selectedChatUserId] || ''}
              label="Chat Background"
              onChange={(e) => onBackgroundChange(e.target.value)}
            >
              <MenuItem value="">Default</MenuItem>
              <MenuItem value="background1">Background 1</MenuItem>
              <MenuItem value="background2">Background 2</MenuItem>
              <MenuItem value="background3">Background 3</MenuItem>
            </Select>
          </FormControl>
        )}
        <Button onClick={onClose} sx={{ marginTop: '10px' }}>
          Close
        </Button>
      </Paper>
    </Modal>
  );
};

export default SettingsModal;