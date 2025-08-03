#!/usr/bin/env python3
"""
Shan-D Bot Main Entry Point
"""
import sys
import os
import asyncio
import logging

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add both current and parent directories to Python path
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

# Also try the Render-specific path structure
render_src_path = "/opt/render/project/src"
if os.path.exists(render_src_path):
    sys.path.insert(0, render_src_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_directories():
    """Check if required directories exist"""
    print("🔍 Checking directory structure...")
    
    core_dir = os.path.join(current_dir, 'core')
    src_dir = os.path.join(current_dir, 'src')
    
    if os.path.exists(core_dir):
        print(f"   ✅ Core directory found: {core_dir}")
    else:
        print(f"   ❌ Core directory NOT found: {core_dir}")
        return False
    
    if os.path.exists(src_dir):
        print(f"   ✅ Src directory found: {src_dir}")
    else:
        print(f"   ❌ Src directory NOT found: {src_dir}")
        return False
    
    # Check for __init__.py files
    init_files = [
        os.path.join(core_dir, '__init__.py'),
        os.path.join(src_dir, '__init__.py'),
        os.path.join(src_dir, 'telegram', '__init__.py')
    ]
    
    for init_file in init_files:
        if os.path.exists(init_file):
            print(f"   ✅ Found: {init_file}")
        else:
            print(f"   ❌ Missing: {init_file}")
            # Try to create the missing __init__.py file
            try:
                os.makedirs(os.path.dirname(init_file), exist_ok=True)
                with open(init_file, 'w') as f:
                    f.write('# Auto-generated __init__.py\n')
                print(f"   ✅ Created: {init_file}")
            except Exception as e:
                print(f"   ❌ Could not create {init_file}: {e}")
    
    return True

def check_imports():
    """Check if all required modules can be imported"""
    print("\n🔍 Checking imports...")
    
    try:
        from src.telegram.bot import ShanDBot
        print("   ✅ src.telegram.bot.ShanDBot")
    except ImportError as e:
        print(f"   ❌ src.telegram.bot.ShanDBot: {e}")
        return False
    
    try:
        from core.shan_d_enhanced import ShanDEnhanced
        print("   ✅ core.shan_d_enhanced.ShanDEnhanced")
    except ImportError as e:
        print(f"   ❌ core.shan_d_enhanced.ShanDEnhanced: {e}")
        return False
    
    try:
        from core.conversation_flow import ShanDConversationFlow
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
    print("🌟 " + "="*70 + " 🌟")
    
    # Debug path information
    print(f"\n🔧 Debug Info:")
    print(f"   Current Directory: {current_dir}")
    print(f"   Python Path: {sys.path[:3]}...")  # Show first 3 entries
    
    # Check directories first
    if not check_directories():
        logger.error("Directory structure check failed.")
        return
    
    # Check imports
    if not check_imports():
        logger.error("Import check failed. Please fix import issues.")
        return
    
    # Import after path setup
    from core.shan_d_enhanced import ShanDEnhanced
    from src.telegram.bot import ShanDBot
    
    try:
        # Initialize Shan-D core
        print("\n🚀 Initializing Shan-D Enhanced...")
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
