#!/usr/bin/env python3

"""
Shan-D: Ultra-Enhanced Human-like AI Assistant with Advanced Learning
Created by: ◉Ɗєиνιℓ
Version: 4.0.0 Ultra-Human Enhanced
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from datetime import datetime
import signal

# Branding banner
print("""
🌟 Shan-D Ultra-Enhanced Human-like AI Assistant 🌟
Created by: ◉Ɗєиνιℓ | Version: 4.0.0 Ultra-Human Enhanced
Features: User Analysis, Self-Improvement, Adaptive Personalization
""")

# Ensure project root on import path
ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))

try:
    from src.telegram.bot import ShanDBot
    from configs.config import Config
    from utils.helpers import setup_logging, check_dependencies
    from core.shan_d_enhanced import EnhancedShanD
    from core.command_processor import AdvancedCommandProcessor
    from storage.user_data_manager import UserDataManager
    from core.learning_engine import ContinuousLearningEngine
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("📦 Installing required packages...")
    os.system("pip install -r requirements.txt")
    sys.exit(1)

# Initialize logger
logger = setup_logging()

class UltraShanDApplication:
    """Manages startup, bot, learning loops, and cleanup."""

    def __init__(self):
        self.config = Config()
        self.bot = None
        self.shan_d_brain = None
        self.command_processor = None
        self.user_data_manager = None
        self.learning_engine = None
        self.running = False

        # Graceful shutdown handlers
        signal.signal(signal.SIGINT,  self._on_shutdown)
        signal.signal(signal.SIGTERM, self._on_shutdown)

    def _on_shutdown(self, signum, frame):
        logger.info("🛑 Shutdown signal received")
        self.running = False

    async def startup_checks(self):
        logger.info("🔍 Running startup checks")
        if not check_dependencies():
            logger.error("❌ Missing dependencies")
        if not self.config.TELEGRAM_TOKEN:
            logger.error("❌ TELEGRAM_TOKEN not set")
        # Create data directories
        for d in ("data/users", "data/learning", "data/analytics"):
            os.makedirs(d, exist_ok=True)
        logger.info("✅ Startup checks complete")

    async def init_components(self):
        try:
            self.user_data_manager = UserDataManager()
            logger.info("UserDataManager initialized")
        except Exception as e:
            logger.error(f"UserDataManager failed: {e}")

        try:
            self.learning_engine = ContinuousLearningEngine()
            logger.info("LearningEngine initialized")
        except Exception as e:
            logger.error(f"LearningEngine failed: {e}")

        try:
            self.shan_d_brain = EnhancedShanD(
                user_data_manager=self.user_data_manager,
                learning_engine=self.learning_engine
            )
            logger.info("EnhancedShanD brain initialized")
        except Exception as e:
            logger.error(f"EnhancedShanD init failed: {e}")

        try:
            self.command_processor = AdvancedCommandProcessor(self.shan_d_brain)
            logger.info("CommandProcessor initialized")
        except Exception as e:
            logger.error(f"CommandProcessor failed: {e}")

    async def start(self):
        await self.startup_checks()
        await self.init_components()

        self.running = True

        # Launch background tasks
        if self.learning_engine:
            asyncio.create_task(self.learning_engine.continuous_learning_loop())
        if self.user_data_manager:
            asyncio.create_task(self.user_data_manager.periodic_user_analysis())
        asyncio.create_task(self._performance_monitoring())

        # Start Telegram bot
        try:
            self.bot = ShanDBot(
                self.shan_d_brain,
                self.command_processor,
                self.user_data_manager
            )
            await self.bot.start()
            logger.info("✅ Telegram bot started")
        except Exception as e:
            logger.error(f"Telegram bot start failed: {e}")

        # Keep application alive until shutdown signal
        while self.running:
            await asyncio.sleep(1)

        await self.cleanup()

    async def _performance_monitoring(self):
        while self.running:
            await asyncio.sleep(3600)
            try:
                stats = await self.shan_d_brain.get_ultra_human_analytics()
                pct = stats.get("human_like_percentage", 0)
                logger.info(f"📊 Human-like responses: {pct:.1f}%")
            except Exception as e:
                logger.error(f"Monitoring error: {e}")

    async def cleanup(self):
        logger.info("🧹 Cleaning up resources")
        if self.bot:
            await self.bot.stop()
        if self.shan_d_brain:
            await self.shan_d_brain.emergency_save()
        if self.user_data_manager:
            await self.user_data_manager.save_all_pending_data()
        if self.learning_engine:
            await self.learning_engine.save_learning_state()
        logger.info("👋 Shutdown complete")

async def main():
    app = UltraShanDApplication()
    await app.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)
