# main.py

import os
import sys
from dotenv import load_dotenv

# 1. Early .env loading & validation
def load_environment_overrides():
    """
    - Load `.env`.
    - Enforce required vars.
    """
    load_dotenv()  # loads .env into os.environ

    required = [
        "API_KEY",
        "DB_URL",
        "TELEGRAM_TOKEN",
        # add any other required names here…
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing required environment vars: {', '.join(missing)}")

load_environment_overrides()


# 2. Build config purely from environment
class Config:
    def __init__(self):
        self.api_key        = os.environ["API_KEY"]
        self.database_url   = os.environ["DB_URL"]
        self.telegram_token = os.environ["TELEGRAM_TOKEN"]
        # add any other settings here…
        # e.g. self.log_level = os.environ.get("LOG_LEVEL", "INFO")

cfg = Config()


# 3. Imports only after cfg is ready
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
from src.utils.advanced_security import advanced_security_scan


def main():
    # 4. Initialize all components with env-only config
    user_db     = UserDataManager(cfg)
    analytics   = AnalyticsEngine()

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
    enhanced    = ShanDEnhanced(convo_flow, cfg)
    error_hdlr  = ErrorHandler()

    # 5. Choose interface
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("CLI mode: type messages or 'exit'.")
        while True:
            text = input("> ")
            if text.lower() in ("exit","quit"):
                break
            advanced_security_scan(text)
            try:
                resp = enhanced.get_response(text)
            except Exception as e:
                resp = error_hdlr.handle_errors(e, context=text)
            user_db.save_interaction(text, resp)
            analytics._update_metrics(text, resp)
            print(resp)
    else:
        bot = TelegramBot(token=cfg.telegram_token, get_response=enhanced.get_response)
        bot.start_polling()


if __name__ == "__main__":
    main()
