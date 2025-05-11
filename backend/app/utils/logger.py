import logging
import os

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts')
os.makedirs(log_dir, exist_ok=True)

# Configure logger
logger = logging.getLogger("News Chatbot")
logger.setLevel(logging.DEBUG)

# File handler for app.log
file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Console handler for terminal output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)