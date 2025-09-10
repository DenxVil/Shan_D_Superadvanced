import os
import sys
import asyncio
from pathlib import Path

# Add src directory to Python path for local imports
sys.path.append(str(Path(__file__).parent / "src"))

# --- Configuration and Security ---
from src.utils.config import load_config
from src.utils.advanced_security import advanced_security_scan

# --- Core Engines ---
from src.core.model_manager import AdvancedModelManager
from src.core.reasoning_engine import AdvancedReasoningEngine
from src.core.emotion_engine import AdvancedEmotionEngine
from src.core.memory_manager import AdvancedMemoryManager
from src.core.learning_engine import ContinuousLearningEngine
from src.core.multimodal_processor import MultimodalProcessor
from src.core.error_handler import AdvancedErrorHandler, handle_errors

# --- NLP and Models ---
from src.models.hindi_nlp import HindiNLPProcessor

# --- Storage and Analytics ---
from src.storage.analytics_engine import AnalyticsEngine
from src.storage.user_data_manager import UserDataManager

# --- Telegram Bot ---
from src.TelegramX.telegram_bot import ShanDAdvanced

def validate_env():
    api_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not api_token:
        sys.exit("Error: Missing env var TELEGRAM_BOT_TOKEN. Please set it and rerun.")
    return api_token

async def initialize_all(cfg):
    # Storage and analytics
    user_db = UserDataManager(cfg)
    analytics = AnalyticsEngine()

    # Core engines
    model_manager = AdvancedModelManager(cfg)
    reasoning_engine = AdvancedReasoningEngine(model_manager)
    emotion_engine = AdvancedEmotionEngine()
    memory_manager = AdvancedMemoryManager()
    learning_engine = ContinuousLearningEngine()
    multimodal_processor = MultimodalProcessor(model_manager)
    error_handler = AdvancedErrorHandler(model_manager)
    hindi_nlp = HindiNLPProcessor()
    
    # Security scan
    advanced_security_scan(cfg)

    return {
        "user_db": user_db,
        "analytics": analytics,
        "model_manager": model_manager,
        "reasoning_engine": reasoning_engine,
        "emotion_engine": emotion_engine,
        "memory_manager": memory_manager,
        "learning_engine": learning_engine,
        "multimodal_processor": multimodal_processor,
        "error_handler": error_handler,
        "hindi_nlp": hindi_nlp,
    }

async def main():
    print("🚀 Shan-D Superadvanced AI: Starting Unified Main...")
    api_token = validate_env()

    # Load config
    cfg = load_config()
    cfg.telegram.token = api_token  # Always override with env token

    # Initialize all components
    engines = await initialize_all(cfg)

    # Pass all engines to Telegram bot
    bot_config = {
        "telegram_bot_token": cfg.telegram.token,
        "model_manager": engines["model_manager"],
        "reasoning_engine": engines["reasoning_engine"],
        "multimodal_processor": engines["multimodal_processor"],
        "error_handler": engines["error_handler"],
        "analytics": engines["analytics"],
        "memory_manager": engines["memory_manager"],
        "learning_engine": engines["learning_engine"],
        "emotion_engine": engines["emotion_engine"],
        "hindi_nlp": engines["hindi_nlp"],
        # You can add more components as needed
    }
    bot_app = ShanDAdvanced(bot_config)
    await bot_app.initialize()
    await bot_app.run()

if __name__ == "__main__":
    asyncio.run(main())