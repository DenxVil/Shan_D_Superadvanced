#!/usr/bin/env python3
"""
Shan_D_TelegramBot – Main entry point for async Telegram polling only
"""

import os
import sys
import asyncio
import logging
import traceback
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# ─── Enhanced Logger ────────────────────────────────────────────────────────────

class EnhancedLogger:
    def __init__(self):
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        detailed = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        simple = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_h = logging.FileHandler(
            log_dir / f"shan_d_{datetime.now():%Y%m%d}.log", encoding="utf-8"
        )
        file_h.setLevel(logging.DEBUG)
        file_h.setFormatter(detailed)

        err_h = logging.FileHandler(
            log_dir / f"errors_{datetime.now():%Y%m%d}.log", encoding="utf-8"
        )
        err_h.setLevel(logging.ERROR)
        err_h.setFormatter(detailed)

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(simple)

        root = logging.getLogger("ShanD")
        root.setLevel(logging.DEBUG)
        root.addHandler(file_h)
        root.addHandler(err_h)
        root.addHandler(console)

        # Silence noisy third-party logs
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("telegram").setLevel(logging.WARNING)

        self.logger = root

    def get_logger(self):
        return self.logger

logger = EnhancedLogger().get_logger()

# ─── Configuration Manager ─────────────────────────────────────────────────────

class ConfigurationManager:
    def __init__(self):
        self.config: Dict[str, Any] = {}

    def load(self) -> bool:
        try:
            logger.info("🔍 Loading configuration...")
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            if not token:
                raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")
            self.config["telegram_token"] = token
            logger.info("✔ Configuration loaded")
            return True
        except Exception as e:
            logger.error(f"✖ Configuration load failed: {e}")
            logger.error(traceback.format_exc())
            return False

# ─── Telegram-Only Bot Application ────────────────────────────────────────────

class ShanDTelegramBot:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.bot_app = None

    async def initialize(self) -> bool:
        if not self.config_manager.load():
            return False

        token = self.config_manager.config["telegram_token"]
        app = ApplicationBuilder().token(token).build()

        # /start command handler
        async def start_handler(update, context):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✔ Shan_D Bot is online!"
            )

        # Echo text messages handler
        async def echo_handler(update, context):
            text = update.message.text
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Echo: {text}"
            )

        app.add_handler(CommandHandler("start", start_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))

        # Initialize and start polling
        await app.initialize()
        await app.updater.start_polling()
        logger.info("🚀 Telegram polling started")

        self.bot_app = app
        return True

    async def shutdown(self):
        if self.bot_app:
            await self.bot_app.updater.stop_polling()
            await self.bot_app.shutdown()
            logger.info("📦 Telegram bot shutdown complete")

# ─── Entrypoint & Graceful Shutdown ───────────────────────────────────────────

async def _serve():
    bot = ShanDTelegramBot()
    if not await bot.initialize():
        sys.exit(1)

    # Wait for SIGINT/SIGTERM
    stop_event = asyncio.Future()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set_result, None)
    await stop_event

    # Shutdown sequence
    await bot.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    # Ensure logs directory exists before anything else
    Path("logs").mkdir(exist_ok=True)
    asyncio.run(_serve())
