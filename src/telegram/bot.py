"""
Telegram Bot for Shan-D Ultra-Enhanced AI Assistant
Created by: ◉Ɗєиνιℓ x
"""
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from typing import Optional

logger = logging.getLogger(__name__)

class ShanDBot:
    """Enhanced Telegram bot with ultra-human AI capabilities"""
    
    def __init__(self, shan_d_brain, command_processor, user_data_manager):
        self.brain = shan_d_brain
        self.command_processor = command_processor
        self.user_data_manager = user_data_manager
        self.application = None
        
        logger.info("🤖 ShanDBot initialized with ultra-human capabilities")
    
    async def start(self):
        """Start the Telegram bot"""
        
        # Create application
        self.application = Application.builder().token(self.brain.config.TELEGRAM_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.COMMAND, self.handle_command))
        
        # Start bot
        logger.info("🚀 Starting Shan-D Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("✅ Shan-D bot is now running!")
    
    async def stop(self):
        """Stop the bot gracefully"""
        if self.application:
            await self.application.stop()
            await self.application.shutdown()
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages with ultra-human AI"""
        
        user_id = str(update.effective_user.id)
        message = update.message.text
        
        try:
            # Get platform context
            platform_context = {
                "platform": "telegram",
                "user_info": {
                    "username": update.effective_user.username,
                    "first_name": update.effective_user.first_name,
                    "last_name": update.effective_user.last_name
                },
                "chat_type": update.effective_chat.type
            }
            
            # Process with ultra-human AI
            response = await self.brain.process_message_ultra_human(
                user_id, message, platform_context
            )
            
            # Send response
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "🤖 Sorry, I had a small glitch there! Can you try again? 😊"
            )
    
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle commands"""
        
        user_id = str(update.effective_user.id)
        command_text = update.message.text
        
        try:
            # Process command
            response = await self.command_processor.process_command(
                user_id, command_text, {"platform": "telegram"}
            )
            
            # Send response
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            await update.message.reply_text(
                "❌ Sorry, something went wrong with that command. Please try again!"
            )
