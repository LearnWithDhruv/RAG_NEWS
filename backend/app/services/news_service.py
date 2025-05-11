import feedparser
import requests
from bs4 import BeautifulSoup
from backend.app.utils.logger import logger

class NewsService:
    def __init__(self):
        self.sources = [
            "https://www.aljazeera.com/xml/rss/all.xml",
            "http://rss.cnn.com/rss/edition.rss",  # Fallback RSS feed
        ]

    def fetch_articles(self, limit=50):
        articles = []
        for source in self.sources:
            logger.info(f"Fetching articles from source: {source}")
            try:
                # Add a timeout to prevent hanging
                response = requests.get(source, timeout=10)
                if response.status_code != 200:
                    logger.error(f"Failed to fetch RSS feed from {source}: Status code {response.status_code}")
                    continue

                feed = feedparser.parse(response.content)
                if not feed.entries:
                    logger.warning(f"No entries found for source: {source}")
                    continue

                for entry in feed.entries[:limit]:
                    article = {
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "published_date": entry.get("published", ""),
                        "source": source,
                        "content": self._extract_content(entry)
                    }
                    article["chunks"] = self._chunk_content(article["content"])
                    if article["title"] and article["url"] and article["chunks"]:
                        articles.append(article)
                        logger.info(f"Successfully fetched article from {source}: {article['url']}")
                    else:
                        logger.warning(f"Skipping article due to missing fields: {article}")
            except Exception as e:
                logger.error(f"Failed to fetch articles from {source}: {e}")
                continue

        # If no articles are fetched, log a warning and return an empty list
        if not articles:
            logger.warning("No articles fetched from any source.")
        else:
            logger.info(f"Total articles fetched: {len(articles)}")

        return articles[:limit]

    def _extract_content(self, entry):
        # Extract content from the feed entry
        content = entry.get("summary", "")
        if "content" in entry:
            content = entry.content[0].value
        # Clean HTML tags if present
        if content:
            soup = BeautifulSoup(content, "html.parser")
            content = soup.get_text()
        return content

    def _chunk_content(self, content):
        # Simple chunking logic: split content into chunks of 500 characters
        if not content:
            return []
        return [content[i:i+500] for i in range(0, len(content), 500)]