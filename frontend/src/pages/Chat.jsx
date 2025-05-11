import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import ChatInterface from '../components/ChatInterface';
import { getChatResponse } from '../services/api';

const Chat = () => {
  const handleSendMessage = async (message) => {
    try {
      const response = await getChatResponse(message);
      return response;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Chat with News Bot
        </Typography>
        <Box sx={{ height: '70vh' }}>
          <ChatInterface onSendMessage={handleSendMessage} />
        </Box>
      </Box>
    </Container>
  );
};

export default Chat;