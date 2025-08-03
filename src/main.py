#Denvil


import asyncio
import os
import sys
import yaml
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent))

from core.model_manager import AdvancedModelManager
from core.reasoning_engine import AdvancedReasoningEngine
from core.multimodal_processor import MultimodalProcessor
from core.error_handler import AdvancedErrorHandler, handle_errors
from bot.telegram_bot import ShanDAdvanced
from utils.config import load_config
from src.utils.advanced_security import advanced_security_scan

async def main():
    """Main function to run the bot"""
    
    try:
        # Load configuration
        config = load_config()
        
        # Initialize Shan-D
        shan_d = ShanDAdvanced(config)
        await shan_d.initialize()
        
        # Start the bot
        scan_results = advanced_security_scan()
        print("Security Scan Results:", scan_results)
        print("🚀 Starting Shan-D Advanced AI Bot...")
        await shan_d.run()
        
    except Exception as e:
        print(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
