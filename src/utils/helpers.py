"""
Utility functions for Shan-D
Created by: ◉Ɗєиνιℓ 👨‍💻
"""
import logging
import re
import random
from typing import Dict, List, Optional
from datetime import datetime

def setup_logging() -> logging.Logger:
    """Setup enhanced logging with ◉Ɗєиνιℓ branding"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - 🧠 Shan-D - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('shan_d.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("📊 Logging system initialized by ◉Ɗєиνιℓ")
    
    return logger

def detect_language(text: str) -> str:
    """Detect language of text"""
    # Simple language detection
    hindi_chars = re.findall(r'[\u0900-\u097F]', text)
    english_chars = re.findall(r'[a-zA-Z]', text)
    
    if len(hindi_chars) > len(english_chars):
        return "hi"
    elif len(hindi_chars) > 0 and len(english_chars) > 0:
        return "mixed"
    else:
        return "en"

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove potentially harmful content
    text = re.sub(r'[<>]', '', text)
    return text.strip()

def check_dependencies() -> bool:
    """Check if all dependencies are available"""
    try:
        import telegram
        import transformers
        import aiofiles
        return True
    except ImportError:
        return False

def validate_permissions(user_id: str) -> bool:
    """Validate user permissions"""
    # Simple permission check - in production, use proper auth
    return True

def generate_casual_response(fallback_type: str = "general") -> str:
    """Generate casual fallback responses"""
    
    responses = {
        "general": [
            "Hey! What's on your mind? 😊",
            "I'm here to chat! What would you like to talk about?",
            "Ready for a conversation! How can I help you today?",
            "Let's chat! I'm all ears 👂"
        ],
        "error": [
            "Oops! Something went a bit wonky. Can you try that again? 😅",
            "My brain had a tiny hiccup there! What were you saying? 🤖",
            "Sorry about that! I'm back to normal now. What's up? 😊"
        ]
    }
    
    return random.choice(responses.get(fallback_type, responses["general"]))
