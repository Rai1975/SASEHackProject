// src/components/MotionPaper.tsx
import { motion } from 'framer-motion';
import { forwardRef } from 'react';
import { Paper } from '@mui/material';

export const MotionPaper = motion(
  forwardRef<HTMLDivElement, React.ComponentProps<typeof Paper>>(
    function MotionPaper(props, ref) {
      return <Paper {...props} ref={ref} />;
    }
  )
);
