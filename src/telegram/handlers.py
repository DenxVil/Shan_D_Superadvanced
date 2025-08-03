"""
Advanced Telegram Handlers for Shan-D
Created by: ◉Ɗєиνιℓ 
Comprehensive message and interaction handlers
"""
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class TelegramHandlers:
    """Advanced handlers for Telegram interactions"""
    
    def __init__(self, brain, user_data_manager):
        self.brain = brain
        self.user_data_manager = user_data_manager
        logger.info("📱 TelegramHandlers initialized by ◉Ɗєиνιℓ")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages"""
        user_id = str(update.effective_user.id)
        
        response = "I can see you've shared a photo! 📸 While I can't analyze images yet, I'd love to hear about what you've shared. What's the story behind this photo?"
        
        await update.message.reply_text(response)
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages"""
        user_id = str(update.effective_user.id)
        
        response = "I heard your voice message! 🎤 Voice processing is coming soon. For now, could you type what you wanted to say? I'm all ears!"
        
        await update.message.reply_text(response)
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        user_id = str(update.effective_user.id)
        document = update.message.document
        
        response = f"Thanks for sharing '{document.file_name}'! 📄 Document analysis is in development. Can you tell me what this document is about or what you'd like to discuss regarding it?"
        
        await update.message.reply_text(response)
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        user_id = str(query.from_user.id)
        
        await query.answer()
        
        if query.data == "get_help":
            response = await self.brain.command_processor.cmd_help(user_id, "", {})
            await query.edit_message_text(response, parse_mode='Markdown')
        
        elif query.data == "about_shan_d":
            response = await self.brain.command_processor.cmd_about(user_id, "", {})
            await query.edit_message_text(response, parse_mode='Markdown')
    
    def get_welcome_keyboard(self) -> InlineKeyboardMarkup:
        """Get welcome message keyboard"""
        keyboard = [
            [InlineKeyboardButton("📚 Help & Commands", callback_data="get_help")],
            [InlineKeyboardButton("🤖 About Shan-D", callback_data="about_shan_d")],
            [InlineKeyboardButton("🎭 Start Chatting", callback_data="start_chat")]
        ]
        return InlineKeyboardMarkup(keyboard)
