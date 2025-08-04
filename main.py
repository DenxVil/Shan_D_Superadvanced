#!/usr/bin/env python3
"""
Shan_D_Superadvanced – Main entry point for async Telegram polling only
"""

import os
import sys
import asyncio
import logging
import traceback
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import yaml

from telegram.ext import ApplicationBuilder, CommandHandler

# Enhanced Logger (unchanged)
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
        file_h = logging.FileHandler(log_dir / f"shan_d_{datetime.now():%Y%m%d}.log", encoding="utf-8")
        file_h.setLevel(logging.DEBUG); file_h.setFormatter(detailed)
        err_h = logging.FileHandler(log_dir / f"errors_{datetime.now():%Y%m%d}.log", encoding="utf-8")
        err_h.setLevel(logging.ERROR); err_h.setFormatter(detailed)
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO); console.setFormatter(simple)
        root = logging.getLogger("ShanD")
        root.setLevel(logging.DEBUG)
        root.addHandler(file_h); root.addHandler(err_h); root.addHandler(console)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        self.logger = root
    def get_logger(self):
        return self.logger

logger = EnhancedLogger().get_logger()

# Configuration Manager (unchanged)
class ConfigurationManager:
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {}
    def load(self) -> bool:
        try:
            logger.info("🔍 Loading configurations...")
            self._load_yaml(); self._load_env(); self._validate()
            logger.info("✔ Configurations loaded")
            return True
        except Exception as e:
            logger.error(f"✖ Configuration load failed: {e}")
            logger.error(traceback.format_exc())
            return False
    def _load_yaml(self):
        p = Path("configs/settings.yaml")
        if p.exists():
            self.settings = yaml.safe_load(p.read_text()) or {}
            logger.debug("✔ YAML settings loaded")
        else:
            logger.warning("⚠ settings.yaml missing, using defaults")
            self.settings = {}
    def _load_env(self):
        self.config.update({
            "environment": os.getenv("ENVIRONMENT", "production"),
            "telegram_token": os.getenv("TELEGRAM_BOT_TOKEN")
        })
    def _validate(self):
        if not self.config.get("telegram_token"):
            logger.error("✖ TELEGRAM_BOT_TOKEN missing")
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

# Telegram-Only Application
class ShanDTelegramBot:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.telegram_app = None

    async def initialize(self) -> bool:
        if not self.config_manager.load():
            return False
        token = self.config_manager.config["telegram_token"]
        bot_app = ApplicationBuilder().token(token).build()
        # /start command
        async def start_cmd(update, context):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✔ Shan_D Telegram Bot is online!"
            )
        bot_app.add_handler(CommandHandler("start", start_cmd))
        # Add more handlers here...
        await bot_app.initialize()
        await bot_app.updater.start_polling()
        logger.info("🚀 Telegram polling started")
        self.telegram_app = bot_app
        return True

    async def shutdown(self):
        if self.telegram_app:
            await self.telegram_app.updater.stop_polling()
            await self.telegram_app.shutdown()
            logger.info("📦 Telegram bot shutdown complete")

# Entrypoint
async def _serve():
    app = ShanDTelegramBot()
    if not await app.initialize():
        sys.exit(1)

    # Wait for termination signal
    stop_event = asyncio.Future()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set_result, None)
    await stop_event

    # Graceful shutdown
    await app.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(_serve())
