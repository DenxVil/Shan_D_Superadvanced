# main.py

import os
from dotenv import load_dotenv

def load_environment_overrides():
    """
    1. Loads variables from a `.env` file (if present).
    2. Reads existing shell environment variables.
    3. Exposes both via os.environ for downstream modules.
    """
    # 1. Locate and load .env in project root
    load_dotenv()  # by default looks for a .env file alongside main.py
    
    # 2. Optionally, enforce required variables
    required = ["API_KEY", "DB_URL", "TELEGRAM_TOKEN"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing required environment vars: {', '.join(missing)}")
    
    # 3. Example of in-process override:
    #    If you want to force a non-production DB in DEV, you can detect an ENV flag:
    if os.getenv("ENV") == "development":
        os.environ["DB_URL"] = os.getenv("DB_URL", "sqlite:///dev.db")


# Call our loader as early as possible
load_environment_overrides()


import sys
from src.TelegramX.telegram_bot import TelegramBot
from src.core.conversation_flow import ConversationFlow
from src.core.emotion_engine import EmotionEngine
from src.core.error_handler import ErrorHandler
from src.core.learning_engine import LearningEngine
from src.core.memory_manager import MemoryManager
from src.core.model_manager import ModelManager
from src.core.personality import Personality
from src.core.reasoning_engine import ReasoningEngine
from src.core.shan_d_enhanced import ShanDEnhanced
from src.storage.analytics_engine import AnalyticsEngine
from src.storage.user_data_manager import UserDataManager
from src.utils.config import load_config
from src.utils.advanced_security import advanced_security_scan


def main():
    # 4. Load file-based defaults
    cfg = load_config()

    # 5. Override config values from environment
    #    Assume load_config returns a simple Namespace or dict
    cfg.telegram.token = os.getenv("TELEGRAM_TOKEN", cfg.telegram.token)
    cfg.database.url   = os.getenv("DB_URL", cfg.database.url)
    cfg.api_key        = os.getenv("API_KEY", cfg.api_key)

    # Initialize storage & analytics
    user_db   = UserDataManager(cfg)
    analytics = AnalyticsEngine()

    # Initialize core engines
    memory      = MemoryManager(cfg)
    model_mgr   = ModelManager(cfg)
    learning    = LearningEngine(cfg)
    reasoning   = ReasoningEngine(cfg)
    personality = Personality(cfg)
    emotion     = EmotionEngine(cfg)
    convo_flow  = ConversationFlow(
        memory=memory,
        model_manager=model_mgr,
        personality=personality,
        emotion_engine=emotion,
        learning_engine=learning,
        analytics_engine=analytics,
    )
    enhanced   = ShanDEnhanced(convo_flow, cfg)

    # Error handling
    error_handler = ErrorHandler()

    # CLI vs Telegram
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("Shan-D Superadvanced CLI: Type your message or 'exit' to quit.")
        while True:
            user_input = input("> ")
            if user_input.lower() in ("exit", "quit"):
                break

            advanced_security_scan(user_input)

            try:
                response = enhanced.get_response(user_input)
            except Exception as e:
                response = error_handler.handle_errors(e, context=user_input)

            user_db.save_interaction(user_input, response)
            analytics._update_metrics(user_input, response)

            print(response)
    else:
        # Telegram bot
        bot = TelegramBot(
            token=cfg.telegram.token,
            get_response=enhanced.get_response
        )
        bot.start_polling()


if __name__ == "__main__":
    main()
