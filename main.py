#!/usr/bin/env python3

"""
Shan-D: Ultra-Enhanced Human-like AI Assistant with Advanced Learning
Created by: ◉Ɗєиνιℓ
Version: 4.0.0 Ultra-Human Enhanced
Features: User Analysis, Self-Improvement, Adaptive Personalization
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from datetime import datetime
import signal

print("🌟 Shan-D Ultra-Human AI Starting… 🌟")

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.telegram.bot import ShanDBot
    from configs.config import Config
    from utils.helpers import setup_logging, check_dependencies
    from core.shan_d_enhanced import EnhancedShanD
    from core.command_processor import AdvancedCommandProcessor
    from storage.user_data_manager import UserDataManager
    from core.learning_engine import ContinuousLearningEngine
except ImportError as e:
    print(f"❌ Import error: {e}")
    os.system("pip install -r requirements.txt")
    sys.exit(1)

logger = setup_logging()

class UltraShanDApplication:
    def __init__(self):
        self.config = Config()
        self.bot = None
        self.shan_d_brain = None
        self.command_processor = None
        self.user_data_manager = None
        self.learning_engine = None
        self.running = False

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info("🛑 Shutdown signal received")
        self.running = False

    async def startup_checks(self):
        try:
            logger.info("🔍 Running startup checks")
            if not check_dependencies():
                raise RuntimeError("Missing dependencies")
            if not self.config.TELEGRAM_TOKEN:
                raise RuntimeError("TELEGRAM_TOKEN missing")
            os.makedirs("data/users", exist_ok=True)
            os.makedirs("data/learning", exist_ok=True)
            os.makedirs("data/analytics", exist_ok=True)
            logger.info("✅ Startup checks passed")
        except Exception as e:
            logger.error(f"⚠️ startup_checks failed: {e}")
            # continue anyway

    async def init_components(self):
        # Initialize each component separately
        try:
            self.user_data_manager = UserDataManager()
        except Exception as e:
            logger.error(f"⚠️ UserDataManager init failed: {e}")
        try:
            self.learning_engine = ContinuousLearningEngine()
        except Exception as e:
            logger.error(f"⚠️ LearningEngine init failed: {e}")
        try:
            self.shan_d_brain = EnhancedShanD(
                user_data_manager=self.user_data_manager,
                learning_engine=self.learning_engine
            )
        except Exception as e:
            logger.error(f"⚠️ EnhancedShanD init failed: {e}")
        try:
            self.command_processor = AdvancedCommandProcessor(self.shan_d_brain)
        except Exception as e:
            logger.error(f"⚠️ CommandProcessor init failed: {e}")

    async def start_bot(self):
        if not all([self.shan_d_brain, self.command_processor, self.user_data_manager]):
            logger.warning("🚧 Bot dependencies missing; skipping bot.start()")
            return
        try:
            self.bot = ShanDBot(
                self.shan_d_brain,
                self.command_processor,
                self.user_data_manager
            )
            await self.bot.start()
        except Exception as e:
            logger.error(f"⚠️ bot.start failed: {e}")
            self.bot = None

    async def start(self):
        await self.startup_checks()
        await self.init_components()

        self.running = True

        # background tasks
        try:
            if self.learning_engine:
                asyncio.create_task(self.learning_engine.continuous_learning_loop())
        except Exception as e:
            logger.error(f"⚠️ background learning loop failed: {e}")
        try:
            if self.user_data_manager:
                asyncio.create_task(self.user_data_manager.periodic_user_analysis())
        except Exception as e:
            logger.error(f"⚠️ periodic user analysis failed: {e}")
        try:
            asyncio.create_task(self._performance_monitoring())
        except Exception as e:
            logger.error(f"⚠️ performance monitoring failed: {e}")

        # Start bot (handles Telegram)
        await self.start_bot()

        # keep running
        while self.running:
            await asyncio.sleep(1)

        await self.cleanup()

    async def _performance_monitoring(self):
        while self.running:
            await asyncio.sleep(3600)
            try:
                if self.shan_d_brain:
                    analytics = await self.shan_d_brain.get_ultra_human_analytics()
                    logger.info(f"📊 Human-like responses: {analytics.get('human_like_percentage',0):.1f}%")
            except Exception as e:
                logger.error(f"⚠️ performance monitoring error: {e}")

    async def cleanup(self):
        logger.info("🧹 Cleaning up…")
        if self.bot:
            try: await self.bot.stop()
            except Exception as e: logger.error(f"cleanup bot.stop failed: {e}")
        if self.shan_d_brain:
            try: await self.shan_d_brain.emergency_save()
            except Exception as e: logger.error(f"cleanup brain.save failed: {e}")
        if self.user_data_manager:
            try: await self.user_data_manager.save_all_pending_data()
            except Exception as e: logger.error(f"cleanup user_data_manager.save failed: {e}")
        if self.learning_engine:
            try: await self.learning_engine.save_learning_state()
            except Exception as e: logger.error(f"cleanup learning_engine.save failed: {e}")
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
