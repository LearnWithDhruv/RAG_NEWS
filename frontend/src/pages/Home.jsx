import React, { useState } from 'react';
import { Box, Typography, Container } from '@mui/material';
import SearchBar from '../components/SearchBar';
import NewsList from '../components/NewsList';
import { searchNews, getRecentNews } from '../services/api';

const Home = () => {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (query) => {
    setIsLoading(true);
    try {
      const results = await searchNews(query);
      setArticles(results.articles);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Load recent news on initial render
  React.useEffect(() => {
    const loadRecentNews = async () => {
      setIsLoading(true);
      try {
        const results = await getRecentNews();
        setArticles(results.articles);
      } catch (error) {
        console.error('Error loading recent news:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadRecentNews();
  }, []);

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          News Chatbot
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          Search and ask questions about recent news articles
        </Typography>
        
        <Box sx={{ my: 4 }}>
          <SearchBar onSearch={handleSearch} />
        </Box>
        
        {isLoading ? (
          <Typography>Loading...</Typography>
        ) : (
          <NewsList articles={articles} />
        )}
      </Box>
    </Container>
  );
};

export default Home;