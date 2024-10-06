// src/components/TaskList.tsx
import React from 'react';
import {
  Box,
  Typography,
  ListItem,
  ListItemIcon,
  ListItemText,
  Checkbox,
  TextField,
  List,
} from '@mui/material';
import { Task } from '../types/Task';
import { TaskListContainer } from '../styles/StyledComponents';

type TaskListProps = {
  tasks: Task[];
  onAddTask: (text: string) => void;
  onToggleTaskCompletion: (taskId: string) => void;
};

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onAddTask,
  onToggleTaskCompletion,
}) => {
  const handleTaskInput = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const inputElement = e.currentTarget as HTMLInputElement;
      onAddTask(inputElement.value);
      inputElement.value = '';
    }
  };

  return (
    <Box sx={{ padding: '10px' }}>
      <Typography variant="h6">Shared Tasks</Typography>
      <TaskListContainer>
        {tasks.map((task) => (
          <ListItem key={task.id} disablePadding>
            <ListItemIcon>
              <Checkbox
                edge="start"
                checked={task.completed}
                tabIndex={-1}
                disableRipple
                onChange={() => onToggleTaskCompletion(task.id)}
              />
            </ListItemIcon>
            <ListItemText primary={task.text} />
          </ListItem>
        ))}
      </TaskListContainer>
      <TextField
        variant="outlined"
        fullWidth
        placeholder="Add a new task..."
        onKeyPress={handleTaskInput}
      />
    </Box>
  );
};

export default TaskList;
