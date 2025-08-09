#!/usr/bin/env python3

"""
Shan_D Superadvanced AI Assistant – Telegram-Centric Edition
"""

import os
import sys
import asyncio
import logging
import warnings
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Suppress PTB “Enable tracemalloc” warning
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="Enable tracemalloc to get the object allocation traceback"
)

class ShanDAssistant:
    def __init__(self):
        # 1. Load .env and override any existing environment variables
        load_dotenv(override=True)

        # 2. Retrieve and confirm the token
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("Environment variable TELEGRAM_BOT_TOKEN is required")
        print(f"Using TELEGRAM_BOT_TOKEN={token}")

        # 3. Build the PTB v20 Application
        self.telegram_app = (
            ApplicationBuilder()
            .token(token)
            .build()
        )

        # 4. Register handlers
        self._register_handlers()

    def _register_handlers(self):
        # Simple /start handler
        self.telegram_app.add_handler(
            CommandHandler("start", self.start)
        )
        # Simple /help handler
        self.telegram_app.add_handler(
            CommandHandler("help", self.help)
        )
        # Add your other handlers here...

    async def start(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Welcome to Shan-D, {user.first_name}!"
        )

    async def help(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Type /start to begin or ask me anything."
        )

    def run(self) -> int:
        # 5. Run polling (handles initialize(), start(), and idle() internally)
        self.telegram_app.run_polling()

        return 0

if __name__ == "__main__":
    assistant = ShanDAssistant()
    sys.exit(assistant.run())
