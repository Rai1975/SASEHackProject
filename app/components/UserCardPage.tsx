import React, { useState, useEffect } from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import { ArrowBack as ArrowBackIcon, ArrowForward as ArrowForwardIcon } from '@mui/icons-material';
import UserCard from './UserCard';
import { User } from '../types/User'; // Assuming this type represents your User data structure

interface UserCardPageProps {
  handleSwipe: (direction: string) => void;
  onNavigate: (direction: 'left' | 'right') => void;
}

const UserCardPage: React.FC<UserCardPageProps> = ({ handleSwipe, onNavigate }) => {
  const [users, setUsers] = useState<User[]>([]); // State to store fetched users
  const [currentIndex, setCurrentIndex] = useState(0); // State to track the current index
  const [loading, setLoading] = useState(true); // State to show loading state
  const [error, setError] = useState<string | null>(null); // State for handling errors

  // Fetch users from the API when the component mounts
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true); // Set loading to true before fetching data
        const response = await fetch('http://0.0.0.0:3000/api/users'); // Your API endpoint
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }
        const data = await response.json();
        setUsers(data); // Set fetched users
        setLoading(false); // Set loading to false after data is fetched
      } catch (error) {
        console.log(error); // Set error message if fetching fails
        setLoading(false); // Set loading to false in case of error
      }
    };

    fetchUsers();
  }, []);

  // Handle navigation between user cards (left and right)
  const handleNavigate = (direction: 'left' | 'right') => {
    if (direction === 'left' && currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    } else if (direction === 'right' && currentIndex < users.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  // Display loading or error states if necessary
  if (loading) {
    return <Typography variant="h6">Loading users...</Typography>;
  }

  if (error) {
    return <Typography variant="h6">Error loading users: {error}</Typography>;
  }

  return (
    <Box sx={{ height: '100%', padding: '20px', position: 'relative' }}>
      <IconButton
        onClick={() => handleNavigate('left')}
        sx={{ position: 'absolute', top: '50%', left: '-40px', zIndex: 1 }}
        disabled={currentIndex === 0} // Disable left navigation if at the start
      >
        <ArrowBackIcon />
      </IconButton>
      <IconButton
        onClick={() => handleNavigate('right')}
        sx={{ position: 'absolute', top: '50%', right: '-40px', zIndex: 1 }}
        disabled={currentIndex === users.length - 1} // Disable right navigation if at the end
      >
        <ArrowForwardIcon />
      </IconButton>
      <Typography variant="h5" mb={2}>
        User Card
      </Typography>
      {users.length > 0 ? (
        <UserCard user={users[currentIndex]} handleSwipe={handleSwipe} />
      ) : (
        <Typography variant="h6">No more users available.</Typography>
      )}
    </Box>
  );
};

export default UserCardPage;
