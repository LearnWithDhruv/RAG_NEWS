import os
import asyncio
import google.generativeai as genai
from backend.app.utils.logger import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    raise

async def generate_response(question: str, context: str) -> str:
    """Generate a response using Gemini API with a timeout"""
    try:
        prompt = f"Question: {question}\n\nContext:\n{context}\n\nAnswer the question based on the provided context in a concise manner."
        logger.debug(f"Sending prompt to Gemini API: {prompt[:100]}...")

        # Use Gemini API with a timeout
        response = await asyncio.to_thread(model.generate_content, prompt)
        if not response or not response.text:
            logger.error("Gemini API returned empty response")
            return "Sorry, I couldn't generate a response. Please try again."

        logger.debug("Successfully generated response from Gemini API")
        return response.text.strip()

    except Exception as e:
        logger.error(f"Error generating response with Gemini API: {e}")
        return "Sorry, I encountered an error while generating a response."