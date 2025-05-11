import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchNews = async (query) => {
  try {
    const response = await api.post('/news/search', { query });
    return response.data;
  } catch (error) {
    console.error('Error searching news:', error);
    throw error;
  }
};

export const getChatResponse = async (sessionId, message) => {
  try {
    const response = await api.post('/chat/', { sessionId, message });
    return response.data;
  } catch (error) {
    console.error('Error getting chat response:', error);
    throw error;
  }
};

export const getRecentNews = async () => {
  try {
    const response = await api.get('/news/recent');
    return response.data;
  } catch (error) {
    console.error('Error fetching recent news:', error);
    throw error;
  }
};