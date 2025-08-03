#!/usr/bin/env python3
"""
Shan-D Bot Main Entry Point
"""
import sys
import os
import asyncio
import logging

# Add current directory to Python path for absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking imports...")
    
    try:
        from src.telegram.bot import ShanDBot
        print("   ✅ src.telegram.bot.ShanDBot")
    except ImportError as e:
        print(f"   ❌ src.telegram.bot.ShanDBot: {e}")
        return False
    
    try:
        from core.shan_d_enhanced import ShanDEnhanced  # NO LEADING DOT
        print("   ✅ core.shan_d_enhanced.ShanDEnhanced")
    except ImportError as e:
        print(f"   ❌ core.shan_d_enhanced.ShanDEnhanced: {e}")
        return False
    
    try:
        from core.conversation_flow import ShanDConversationFlow  # NO LEADING DOT
        print("   ✅ core.conversation_flow.ShanDConversationFlow")
    except ImportError as e:
        print(f"   ❌ core.conversation_flow.ShanDConversationFlow: {e}")
        return False
    
    return True

async def main():
    """Main entry point"""
    print("\n🌟 " + "="*70 + " 🌟")
    print("🤖 Shan-D - Ultra-Enhanced Human-like AI Assistant")
    print("🧠 Advanced Learning + User Personalization + Self-Improvement")
    print("🏷️ Created by: ◉Ɗєиνιℓ")
    print("🎭 AI Name: Shan-D")
    print("📅 Version: 4.0.0 Ultra-Human Enhanced")
    print("🌍 Features: Complete User Analysis + Adaptive Learning")
    print("🌟 " + "="*70 + " 🌟\n")
    
    # Check imports first
    if not check_imports():
        logger.error("Import check failed. Please fix import issues.")
        return
    
    # Import after path setup - USE ABSOLUTE IMPORTS (NO DOTS)
    from core.shan_d_enhanced import ShanDEnhanced
    from src.telegram.bot import ShanDBot
    
    try:
        # Initialize Shan-D core
        print("🚀 Initializing Shan-D Enhanced...")
        shan_d = ShanDEnhanced()
        
        # Initialize Telegram bot
        print("🤖 Initializing Telegram Bot...")
        bot = ShanDBot(shan_d)
        
        # Start the bot
        print("✅ Starting Shan-D Bot...")
        await bot.start()
        
    except Exception as e:
        logger.error(f"Error starting Shan-D: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
