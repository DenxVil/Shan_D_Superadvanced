#!/usr/bin/env python3
"""
Unified Shan_D Superadvanced – all modules in one Telegram bot entrypoint
"""

import os
import sys
import logging
import warnings
import functools
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Suppress PTB tracemalloc warning
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="Enable tracemalloc to get the object allocation traceback"
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s – %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Safe‐execution decorator
def safe_handler(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await func(update, context)
        except Exception as e:
            user = update.effective_user.id if update.effective_user else "unknown"
            chat = update.effective_chat.id if update.effective_chat else "unknown"
            logger.error(
                "Error in handler %s (user=%s chat=%s): %s",
                func.__name__, user, chat, e,
                exc_info=True
            )
            try:
                await context.bot.send_message(
                    chat_id=chat,
                    text="⚠️ An error occurred—skipping this command."
                )
            except Exception:
                pass
    return wrapper

# Load environment (override existing)
load_dotenv(override=True)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable")

# Ensure modules can be imported
ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

# Import core services
from core.model_manager import AdvancedModelManager
from core.reasoning_engine import AdvancedReasoningEngine
from core.multimodal_processor import MultimodalProcessor
from core.error_handler import AdvancedErrorHandler, handle_errors
from core.conversation_flow import ShanDConversationFlow
from core.learning_engine import ContinuousLearningEngine
from core.memory_manager import AdvancedMemoryManager
from core.personality import PersonalityProfile

# Import AI wrappers
from models.llm_handler import LLMHandler
from models.knowledge_retriever import KnowledgeRetriever

# Import storage
from storage.user_data_manager import UserDataManager
from storage.analytics_engine import AnalyticsEngine

# Import utils
from utils.helpers import format_message
from utils.config import load_config

# Import TelegramX helpers
from TelegramX.telegram_bot import TelegramBotHelper
from TelegramX.handlers import register_handlers as register_tx_handlers

def main():
    logger.info("Starting Shan_D Superadvanced bot…")

    # Initialize core services
    cfg = load_config()
    ai = LLMHandler(cfg)
    km = KnowledgeRetriever(cfg)
    memory = MemoryManager()
    multimodal = MultimodalProcessor(cfg)
    personality = PersonalityProfile(cfg)
    reasoning = AdvancedReasoningEngine(ai, memory)
    learning = LearningEngine(ai, memory)
    conversation = ConversationFlow(ai, reasoning, km, multimodal, personality, learning)
    user_data = UserDataManager()
    analytics = AnalyticsEngine()

    # Build Telegram application
    app = ApplicationBuilder().token(TOKEN).build()

    # Wrap services in helper
    bot_helper = TelegramBotHelper(
        app=app,
        ai=ai,
        knowledge=km,
        memory=memory,
        reasoning=reasoning,
        multimodal=multimodal,
        personality=personality,
        learning=learning,
        conversation=conversation,
        user_data=user_data,
        analytics=analytics,
        config=cfg,
    )

    # Register all handlers (with safe wrapper)
    register_tx_handlers(app, bot_helper, wrapper=safe_handler)

    # Example: expose generic /ask command
    @safe_handler
    async def ask(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        question = " ".join(ctx.args)
        if not question:
            await update.message.reply_text("Usage: /ask <your question>")
            return
        answer = await conversation.handle_question(question, user_id=update.effective_user.id)
        await update.message.reply_text(answer)

    app.add_handler(CommandHandler("ask", ask))

    # Start polling
    logger.info("Running Telegram polling…")
    app.run_polling()

if __name__ == "__main__":
    main()
