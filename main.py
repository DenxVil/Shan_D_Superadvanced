#!/usr/bin/env python3
"""
Shan_D_Superadvanced – Main entry point using long-polling for Telegram
"""

import os
import sys
import asyncio
import logging
import signal
from pathlib import Path
from fastapi import FastAPI, HTTPException  # kept if you ever mix FastAPI
import uvicorn
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment")

# Ensure repo root and src on PYTHONPATH (if needed)
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # DEBUG to see telegram library logs
)
logger = logging.getLogger("ShanD")
# Also set telegram library to debug
logging.getLogger("telegram").setLevel(logging.DEBUG)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🤖 Shan-D is online and ready to assist!")
    except Exception as e:
        logger.error(f"Error in start handler: {e}", exc_info=True)

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = (
            "Available commands:\n"
            "/start – Check bot status\n"
            "/help – Show this message\n"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Error in help_command handler: {e}", exc_info=True)

# Fallback: echo any text to verify flow
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Echo handler received: {update.message.text}")
    try:
        await update.message.reply_text("Echo: " + (update.message.text or ""))
    except Exception as e:
        logger.error(f"Error in echo handler: {e}", exc_info=True)

def main():
    # Build Telegram application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register handlers on the same Application instance
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Graceful shutdown on signals
    def _shutdown(signum, frame):
        logger.info("Signal %s received, shutting down...", signum)
        asyncio.get_event_loop().stop()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    # Start polling
    logger.info("Starting long-polling for Telegram bot")
    application.run_polling()

if __name__ == "__main__":
    main()
