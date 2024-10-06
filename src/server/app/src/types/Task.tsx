// src/types/Task.ts
export type Task = {
    id: string;
    text: string;
    completed: boolean;
    deadline?: Date;
    assignedTo: string[];
  };
  