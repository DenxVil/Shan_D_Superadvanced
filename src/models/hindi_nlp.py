"""
Hindi NLP Processing for Shan-D
Created by: ◉Ɗєиνιℓ 
Advanced Hindi language processing and understanding
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
import re
from googletrans import Translator

logger = logging.getLogger(__name__)

class HindiNLPProcessor:
    """Advanced Hindi NLP processing"""
    
    def __init__(self):
        self.translator = Translator()
        self.hindi_patterns = self._load_hindi_patterns()
        logger.info("🇮🇳 HindiNLPProcessor initialized by ◉Ɗєиνιℓ")
    
    def _load_hindi_patterns(self) -> Dict:
        """Load Hindi language patterns"""
        return {
            "greetings": ["नमस्ते", "हैलो", "प्रणाम", "आदाब"],
            "emotions": {
                "खुश": "happy",
                "दुखी": "sad", 
                "गुस्सा": "angry",
                "प्रेम": "love"
            },
            "common_words": {
                "हाँ": "yes",
                "नहीं": "no",
                "ठीक है": "okay",
                "समझ गया": "understood"
            }
        }
    
    async def process_hindi_text(self, text: str) -> Dict:
        """Process Hindi text for understanding"""
        
        analysis = {
            "language": "hindi",
            "contains_hindi": self._contains_hindi(text),
            "emotion": self._detect_hindi_emotion(text),
            "intent": self._detect_hindi_intent(text),
            "translation": None
        }
        
        if analysis["contains_hindi"]:
            try:
                analysis["translation"] = await self._translate_to_english(text)
            except Exception as e:
                logger.error(f"Translation error: {e}")
        
        return analysis
    
    def _contains_hindi(self, text: str) -> bool:
        """Check if text contains Hindi characters"""
        hindi_pattern = r'[\u0900-\u097F]'
        return bool(re.search(hindi_pattern, text))
    
    def _detect_hindi_emotion(self, text: str) -> str:
        """Detect emotion in Hindi text"""
        for hindi_emotion, english_emotion in self.hindi_patterns["emotions"].items():
            if hindi_emotion in text:
                return english_emotion
        return "neutral"
    
    def _detect_hindi_intent(self, text: str) -> str:
        """Detect intent in Hindi text"""
        if any(greeting in text for greeting in self.hindi_patterns["greetings"]):
            return "greeting"
        elif "कैसे हो" in text or "कैसी हो" in text:
            return "how_are_you"
        elif "क्या" in text:
            return "question"
        else:
            return "general"
    
    async def _translate_to_english(self, text: str) -> str:
        """Translate Hindi text to English"""
        try:
            result = self.translator.translate(text, src='hi', dest='en')
            return result.text
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text
