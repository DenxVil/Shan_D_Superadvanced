#DENVIL

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from core.model_manager import AdvancedModelManager
from core.reasoning_engine import AdvancedReasoningEngine
from core.multimodal_processor import MultimodalProcessor
from core.error_handler import AdvancedErrorHandler, handle_errors

class ShanDAdvanced:
    def __init__(self, config):
        self.config = config
        self.model_manager = AdvancedModelManager(config)
        self.reasoning_engine = AdvancedReasoningEngine(self.model_manager)
        self.multimodal_processor = MultimodalProcessor(self.model_manager)
        self.error_handler = AdvancedErrorHandler(self.model_manager)
        self.application = None
        
    async def initialize(self):
        """Initialize all components"""
        await self.model_manager.initialize()
        
        # Create Telegram application
        self.application = Application.builder().token(self.config['telegram_bot_token']).build()
        
        # Add handlers
        self.application.add_handler(MessageHandler(filters.ALL, self.process_message))
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("errorstats", self.error_stats_command))
        
        print("✅ Shan-D Advanced AI initialized successfully!")
    
    @handle_errors
    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main message processing method"""
        
        user_id = str(update.effective_user.id)
        message_data = {
            'text': update.message.text if update.message.text else None,
            'user_id': user_id,
            'chat_id': str(update.effective_chat.id),
            'message_id': update.message.message_id
        }
        
        # Check for media content
        if update.message.photo:
            message_data['photo'] = update.message.photo[-1]
        elif update.message.video:
            message_data['video'] = update.message.video
        elif update.message.audio or update.message.voice:
            message_data['audio'] = update.message.audio or update.message.voice
        elif update.message.document:
            message_data['document'] = update.message.document
        
        # Process with multimodal processor
        result = await self.multimodal_processor.process_media_message(message_data)
        
        # If it's a complex query, use reasoning engine
        if result['analysis_type'] == 'conversation' and len(message_data.get('text', '')) > 100:
            reasoning_context = {
                'user_id': user_id,
                'conversation_history': context.user_data.get('history', [])
            }
            result = await self.reasoning_engine.process_with_reasoning(
                message_data['text'], 
                reasoning_context
            )
        
        # Send response
        await update.message.reply_text(result['response'])
        
        # Update conversation history
        if 'history' not in context.user_data:
            context.user_data['history'] = []
        
        context.user_data['history'].append({
            'role': 'user',
            'content': message_data.get('text', '[Media message]')
        })
        context.user_data['history'].append({
            'role': 'assistant',
            'content': result['response']
        })
        
        # Keep only last 10 exchanges
        if len(context.user_data['history']) > 20:
            context.user_data['history'] = context.user_data['history'][-20:]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 **Welcome to Shan-D Advanced AI!**

I'm your advanced AI assistant with enhanced capabilities:

🧠 **Advanced Reasoning** - Complex problem solving
🎨 **Multimodal Processing** - Images, videos, documents
🔧 **Self-Healing** - Automatic error detection and fixing
⚡ **High Performance** - Optimized for speed and accuracy

Type anything to get started!

Commands:
/help - Show help information
/stats - Show performance statistics
/errorstats - Show error statistics
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
🆘 **Shan-D Advanced AI Help**

**What I can do:**
• Answer complex questions with step-by-step reasoning
• Analyze images and describe what I see
• Process documents and extract information
• Handle multiple languages
• Learn from our conversations
• Self-diagnose and fix technical issues

**Tips for best results:**
• Be specific in your questions
• For complex topics, ask for step-by-step explanations
• Send images with descriptions for better analysis
• Use natural language - I understand context

**Commands:**
/start - Welcome message
/help - This help message
/stats - Performance statistics
/errorstats - Error handling statistics

**Examples:**
"Explain quantum computing step by step"
"Analyze this image and tell me what you see"
"Solve this math problem: 2x + 5 = 15"
"Translate this to French: Hello world"
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        stats = self.model_manager.performance_metrics
        
        if not stats:
            await update.message.reply_text("📊 No statistics available yet. Start chatting to generate data!")
            return
        
        stats_message = "📊 **Performance Statistics**\n\n"
        
        for model_name, metrics in stats.items():
            stats_message += f"**{model_name}:**\n"
            stats_message += f"• Total calls: {metrics['total_calls']}\n"
            stats_message += f"• Avg response time: {metrics['avg_response_time']:.2f}s\n"
            stats_message += f"• Avg response length: {metrics['avg_response_length']:.0f} chars\n"
            stats_message += f"• Total cost: ${metrics['total_cost']:.4f}\n\n"
        
        await update.message.reply_text(stats_message, parse_mode='Markdown')
    
    async def error_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /errorstats command"""
        stats = await self.error_handler.get_error_statistics()
        
        stats_message = f"""
🔧 **Error Statistics**

Total Errors: {stats['total_errors']}
Auto-fix Success Rate: {stats.get('auto_fix_success_rate', 0):.1f}%

**By Severity:**
{self._format_dict(stats.get('severity_distribution', {}))}

**By Category:**
{self._format_dict(stats.get('category_distribution', {}))}
        """
        
        await update.message.reply_text(stats_message)
    
    def _format_dict(self, d: dict) -> str:
        """Format dictionary for display"""
        return '\n'.join([f"• {k}: {v}" for k, v in d.items()])
    
    async def run(self):
        """Run the bot"""
        await self.application.run_polling()
    
    async def shutdown(self):
        """Cleanup resources"""
        await self.model_manager.close()
        if self.application:
            await self.application.shutdown()
