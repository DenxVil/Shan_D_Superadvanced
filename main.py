# main.py

import os
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
    # 1. Read Telegram credentials explicitly from environment
    try:
        api_token = os.environ["TELEGRAM_BOT_TOKEN"]
    except KeyError:
        sys.exit("Error: Missing env var TELEGRAM_BOT_TOKEN. Please set it and rerun.")

    # Load other configuration
    cfg = load_config()

    # Override cfg.telegram.token with the environment value
    cfg.telegram.token = api_token

    # Initialize storage & analytics
    user_db    = UserDataManager(cfg)
    analytics  = AnalyticsEngine()

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
    enhanced    = ShanDEnhanced(convo_flow, cfg)

    # Setup error handling
    error_handler = ErrorHandler()

    # Initialize Telegram bot interface with only the env var token
    bot = TelegramBot(
        token=cfg.telegram.token,
        get_response=enhanced.get_response
    )

    # Command-line loop fallback
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
        bot.start_polling()


if __name__ == "__main__":
    main()
