#!/usr/bin/env python3
"""
Unified entrypoint: loads env, builds the Telegram bot with all handlers from TelegramX,
and runs polling.
"""

import os
import sys
import logging
import warnings
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

# Suppress PTB “Enable tracemalloc” warnings
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="Enable tracemalloc to get the object allocation traceback"
)

# Ensure project root is on PYTHONPATH so src/TelegramX can be imported
ROOT = os.path.dirname(__file__)
sys.path.insert(0, ROOT)

# 1. Load .env (override existing env vars) and configure logging
load_dotenv(override=True)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment")

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s – %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logger.info("Using TELEGRAM_BOT_TOKEN=%s", TELEGRAM_TOKEN)

# 2. Import your TelegramX bot and handlers
from src.TelegramX.telegram_bot import TelegramBot
from src.TelegramX.handlers import register_handlers

def main():
    # 3. Build the Application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # 4. Instantiate your TelegramBot helper (if it wraps shared state)
    bot_helper = TelegramBot(app)

    # 5. Register all handlers defined in TelegramX/handlers.py
    register_handlers(app, bot_helper)

    # 6. Start polling (initializes bot, dispatcher, etc.)
    logger.info("Starting bot polling…")
    app.run_polling()

if __name__ == "__main__":
    main()
