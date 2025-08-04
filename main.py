#!/usr/bin/env python3
"""
Shan_D Superadvanced AI Assistant – Telegram-Centric Edition
"""

import os
import sys
import asyncio
import logging
import traceback
import warnings
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Suppress PTB “Enable tracemalloc” warning
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="Enable tracemalloc to get the object allocation traceback"
)

# Telegram imports
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# Add 'src' for custom modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

class EnhancedLogger:
    """Unified logger to file + console."""
    def __init__(self):
        log_dir = Path("logs"); log_dir.mkdir(exist_ok=True)
        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(log_dir / f"shan_d_{datetime.now():%Y%m%d}.log")
        fh.setLevel(logging.DEBUG); fh.setFormatter(fmt)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO); ch.setFormatter(fmt)
        self.logger = logging.getLogger("ShanD")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(fh); self.logger.addHandler(ch)
        for lib in ("httpx","openai","anthropic"):
            logging.getLogger(lib).setLevel(logging.WARNING)
    def get(self): return self.logger

logger = EnhancedLogger().get()

class TelegramQueryHandler:
    """
    Encapsulates parsing and replying to Telegram text queries.
    Future: extend to handle buttons, callbacks, attachments.
    """
    def __init__(self, conversation_flow):
        self.flow = conversation_flow

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text or ""
        user_id = str(update.effective_user.id)
        logger.debug(f"Received TG message from {user_id}: {text}")
        try:
            if not self.flow:
                return await update.message.reply_text("🔄 Initializing...")

            response = await self.flow.process_message(text, user_id, {})
            await update.message.reply_text(response.get("text", "…"))
        except Exception as e:
            logger.error(f"Error in TG handler: {e}")
            await update.message.reply_text("❌ Oops, something went wrong.")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👋 Shan_D Superadvanced is now online!")

class ShanDApplication:
    """Main app wiring: config, core AI, Telegram integration."""
    def __init__(self):
        self.components: Dict[str, Any] = {}
        self.telegram_app = None

    async def initialize(self) -> bool:
        # (Directory + config loading omitted for brevity; assume done)
        # Initialize core AI components:
        try:
            from src.core.conversation_flow import ShanDConversationFlow
            self.components['conversation_flow'] = ShanDConversationFlow()
            await self.components['conversation_flow'].initialize()
            logger.info("✅ ConversationFlow ready")
        except Exception as e:
            logger.error(f"ConversationFlow init failed: {e}")
            self.components['conversation_flow'] = None

        # Setup Telegram
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if telegram_token:
            self.telegram_app = ApplicationBuilder().token(telegram_token).build()
            tg_handler = TelegramQueryHandler(self.components['conversation_flow'])
            self.telegram_app.add_handler(CommandHandler("start", tg_handler.start))
            self.telegram_app.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, tg_handler.handle_message)
            )
            logger.info("✅ TelegramQueryHandler configured")
        else:
            logger.warning("⚠️ No Telegram token; TG disabled")

        return True

    async def run(self):
        if not self.telegram_app:
            logger.error("❌ Telegram bot not configured")
            return
        logger.info("🔄 Starting Telegram polling…")
        await self.telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)

    async def shutdown(self):
        if self.telegram_app:
            logger.info("👋 Shutting down Telegram bot…")
            await self.telegram_app.shutdown()
            await self.telegram_app.wait_closed()

async def main():
    app = ShanDApplication()
    if not await app.initialize():
        return 1
    try:
        await app.run()
    except KeyboardInterrupt:
        pass
    finally:
        await app.shutdown()
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
