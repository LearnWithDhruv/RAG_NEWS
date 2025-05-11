import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  List, 
  ListItem, 
  ListItemText, 
  Avatar, 
  Typography,
  Paper
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const ChatInterface = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    { text: 'Hello! Ask me anything about recent news.', sender: 'bot' }
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage = { text: message, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setMessage('');

    try {
      const response = await onSendMessage(message);
      setMessages(prev => [...prev, { text: response.answer, sender: 'bot' }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error. Please try again.', 
        sender: 'bot' 
      }]);
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ flexGrow: 1, overflow: 'auto', mb: 2 }}>
        <List>
          {messages.map((msg, index) => (
            <ListItem key={index}>
              <Box sx={{ 
                display: 'flex', 
                flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
                width: '100%'
              }}>
                <Avatar sx={{ 
                  bgcolor: msg.sender === 'user' ? 'primary.main' : 'secondary.main',
                  ml: msg.sender === 'user' ? 2 : 0,
                  mr: msg.sender === 'user' ? 0 : 2
                }}>
                  {msg.sender === 'user' ? 'U' : 'B'}
                </Avatar>
                <Paper 
                  sx={{ 
                    p: 2, 
                    bgcolor: msg.sender === 'user' ? 'primary.light' : 'secondary.light',
                    color: msg.sender === 'user' ? 'primary.contrastText' : 'secondary.contrastText'
                  }}
                >
                  <Typography>{msg.text}</Typography>
                </Paper>
              </Box>
            </ListItem>
          ))}
          <div ref={messagesEndRef} />
        </List>
      </Box>
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your question..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleSend}
          endIcon={<SendIcon />}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatInterface;