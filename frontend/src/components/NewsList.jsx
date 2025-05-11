import React from 'react';
import { List, ListItem, ListItemText, Typography, Link } from '@mui/material';

const NewsList = ({ articles }) => {
  if (!articles || articles.length === 0) {
    return <Typography>No articles found. Try a different search.</Typography>;
  }

  return (
    <List>
      {articles.map((article, index) => (
        <ListItem key={index} divider>
          <ListItemText
            primary={<Link href={article.url} target="_blank" rel="noopener">{article.title}</Link>}
            secondary={article.snippet}
          />
        </ListItem>
      ))}
    </List>
  );
};

export default NewsList;