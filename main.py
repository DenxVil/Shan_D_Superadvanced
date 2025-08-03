#!/usr/bin/env python3

"""
Shan_D_Superadvanced - Advanced AI Assistant Main Entry Point
"""

import os
import sys
import asyncio
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import json
import yaml

from fastapi import FastAPI, HTTPException
import uvicorn
from telegram.ext import ApplicationBuilder, CommandHandler

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))


class EnhancedLogger:
    """Enhanced logging system with multiple output streams"""
    def __init__(self):
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        detailed = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        simple = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_h = logging.FileHandler(log_dir / f"shan_d_{datetime.now():%Y%m%d}.log", encoding="utf-8")
        file_h.setLevel(logging.DEBUG)
        file_h.setFormatter(detailed)

        err_h = logging.FileHandler(log_dir / f"errors_{datetime.now():%Y%m%d}.log", encoding="utf-8")
        err_h.setLevel(logging.ERROR)
        err_h.setFormatter(detailed)

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(simple)

        self.logger = logging.getLogger("ShanD")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_h)
        self.logger.addHandler(err_h)
        self.logger.addHandler(console)

        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("anthropic").setLevel(logging.WARNING)

    def get_logger(self):
        return self.logger


# Global logger
log_manager = EnhancedLogger()
logger = log_manager.get_logger()


class DirectoryStructureManager:
    """Ensures required directories and files exist"""
    REQUIRED_DIRECTORIES = [
        "src", "configs", "api", "logs", "data", "temp",
        "cache", "uploads", "models", "static", "templates",
        "data/conversations", "data/memories", "data/models",
        "cache/embeddings", "cache/responses"
    ]
    CRITICAL_FILES = [
        "configs/config.py",
        "configs/settings.yaml",
        "src/core/model_manager.py",
        "src/core/emotion_engine.py",
        "src/core/learning_engine.py",
        "src/core/memory_manager.py"
    ]

    @classmethod
    def validate_and_setup(cls) -> bool:
        logger.info("🔄 Validating application structure...")
        try:
            root = Path.cwd()
            logger.info(f"Application root: {root}")

            for d in cls.REQUIRED_DIRECTORIES:
                (root / d).mkdir(parents=True, exist_ok=True)
                logger.debug(f"✅ Directory ensured: {d}")

            missing = [f for f in cls.CRITICAL_FILES if not (root / f).exists()]
            if missing:
                logger.warning(f"⚠️ Missing critical files: {missing}")

            cls._ensure_runtime_config(root)
            logger.info("✅ Directory validation complete")
            return True
        except Exception as e:
            logger.error(f"❌ Directory validation failed: {e}")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def _ensure_runtime_config(cls, root: Path):
        cfg = root / "runtime_config.json"
        if not cfg.exists():
            data = {
                "startup_time": datetime.now().isoformat(),
                "version": "2.0.0",
                "environment": "production",
                "features": {
                    "emotion_engine": True,
                    "learning_system": True,
                    "memory_persistence": True,
                    "multimodal_processing": True,
                    "conversation_flow": True
                },
                "performance": {
                    "max_concurrent_requests": 10,
                    "memory_limit_mb": 512,
                    "cache_size_mb": 128
                }
            }
            with open(cfg, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Created runtime config: {cfg}")


class ConfigurationManager:
    """Loads and validates configuration"""
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {}

    def load_configurations(self) -> bool:
        try:
            logger.info("🔄 Loading configurations...")
            self._load_yaml()
            self._load_env()
            self._load_api_keys()
            self._validate()
            logger.info("✅ Configurations loaded")
            return True
        except Exception as e:
            logger.error(f"❌ Configuration load failed: {e}")
            return False

    def _load_yaml(self):
        f = Path("configs/settings.yaml")
        if f.exists():
            with open(f, "r", encoding="utf-8") as fp:
                self.settings = yaml.safe_load(fp) or {}
            logger.debug("✅ YAML settings loaded")
        else:
            logger.warning("⚠️ settings.yaml missing, using defaults")
            self.settings = self._defaults()

    def _load_env(self):
        self.config.update({
            "debug": os.getenv("DEBUG", "false").lower() == "true",
            "host": os.getenv("HOST", "0.0.0.0"),
            "port": int(os.getenv("PORT", 8000)),
            "environment": os.getenv("ENVIRONMENT", "production")
        })

    def _load_api_keys(self):
        keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "google": os.getenv("GOOGLE_API_KEY"),
            "telegram": os.getenv("TELEGRAM_BOT_TOKEN")
        }
        self.config["api_keys"] = {k: v for k, v in keys.items() if v}
        logger.info(f"🔑 Loaded {len(self.config['api_keys'])} API keys")

    def _validate(self):
        if not self.config.get("api_keys"):
            logger.warning("⚠️ No API keys configured")
        p = self.config.get("port", 8000)
        if not (1024 <= p <= 65535):
            logger.warning(f"⚠️ Invalid port {p}, defaulting to 8000")
            self.config["port"] = 8000

    def _defaults(self) -> Dict[str, Any]:
        return {
            "app": {"name": "Shan_D_Superadvanced", "version": "2.0.0"},
            "features": {
                "emotion_processing": True,
                "adaptive_learning": True,
                "memory_persistence": True,
                "multimodal_support": True
            },
            "limits": {"max_conversation_length": 50, "memory_retention_days": 30}
        }


class ShanDApplication:
    """Main application orchestrator"""
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.components: Dict[str, Any] = {}
        self.app: Optional[FastAPI] = None
        self.telegram_app = None

    async def initialize(self) -> bool:
        try:
            logger.info("🔄 Initializing application...")
            if not self.config_manager.load_configurations():
                return False

            DirectoryStructureManager.validate_and_setup()
            await self._init_core()
            await self._init_models()
            await self._setup_routes()
            await self._setup_integrations()

            logger.info("✅ Initialization complete")
            return True
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            logger.error(traceback.format_exc())
            return False

    async def _init_core(self):
        logger.info("🔧 Loading core components...")
        try:
            from src.core.emotion_engine import AdvancedEmotionEngine
            from src.core.memory_manager import AdvancedMemoryManager
            from src.core.learning_engine import ContinuousLearningEngine
            from src.core.model_manager import AdvancedModelManager
            from src.core.conversation_flow import ShanDConversationFlow
            from src.core.multimodal_processor import MultimodalProcessor

            cfg = {"debug": True}
            self.components = {
                "emotion_engine": AdvancedEmotionEngine(),
                "memory_manager": AdvancedMemoryManager(),
                "learning_engine": ContinuousLearningEngine(),
                "model_manager": AdvancedModelManager(cfg),
                "conversation_flow": ShanDConversationFlow(),
                "multimodal_processor": MultimodalProcessor(cfg)
            }
            for name, comp in self.components.items():
                if hasattr(comp, "initialize"):
                    await comp.initialize()
                    logger.debug(f"✅ {name} initialized")
            logger.info("✅ Core loaded")
        except ImportError as e:
            logger.error(f"❌ Core import failed: {e}")
            self.components = {n: None for n in self.components}
        except Exception as e:
            logger.error(f"❌ Core init error: {e}")
            raise

    async def _init_models(self):
        logger.info("🔄 Loading AI models...")
        try:
            mgr = self.components.get("model_manager")
            if mgr and hasattr(mgr, "initialize_models"):
                await mgr.initialize_models(self.config_manager.config.get("api_keys", {}))
                logger.info("✅ Models loaded")
            else:
                logger.warning("⚠️ Model manager unavailable")
        except Exception as e:
            logger.error(f"❌ Model init failed: {e}")

    async def _setup_routes(self):
        self.app = FastAPI()

        @self.app.get("/")
        async def root():
            return {
                "message": "Welcome to Shan_D_Superadvanced",
                "version": "2.0.0",
                "status": "operational",
                "features": list(self.components.keys()),
                "docs": "/docs"
            }

        @self.app.get("/health")
        async def health():
            status = {n: ("active" if c else "inactive") for n, c in self.components.items()}
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": status,
                "memory_usage": self._memory_usage()
            }

        @self.app.post("/chat")
        async def chat(msg: Dict[str, Any]):
            try:
                flow = self.components.get("conversation_flow")
                if flow:
                    return await flow.process_message(msg.get("text", ""), msg.get("user_id", ""), msg.get("context", {}))
                return {"text": "Initializing", "status": "initializing"}
            except Exception as e:
                logger.error(f"❌ Chat error: {e}")
                raise HTTPException(status_code=500, detail="Internal error")

        logger.info("✅ Routes configured")

    async def _setup_integrations(self):
    logger.info("🔗 Setting up integrations...")
    try:
        telegram_token = self.config_manager.config.get('api_keys', {}).get('telegram')
        if not telegram_token:
            logger.error("❌ Telegram token not found—skipping bot setup")
            return

        # Build the Telegram Application
        bot_app = ApplicationBuilder().token(telegram_token).build()

        # /start command handler
        async def _setup_integrations(self):
    logger.info("🔗 Setting up integrations...")
    try:
        telegram_token = self.config_manager.config.get('api_keys', {}).get('telegram')
        if not telegram_token:
            logger.error("❌ Telegram token not found—skipping bot setup")
            return

        # Build the Telegram Application
        bot_app = ApplicationBuilder().token(telegram_token).build()

        # /start command handler
        async def _start(update, context):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ Shan-D bot is alive!"
            )
        bot_app.add_handler(CommandHandler("start", _start))

        # Store for later and log
        self.telegram_app = bot_app
        logger.info("✅ Telegram Application built successfully")
    except Exception as e:
        logger.error(f"❌ Integration setup failed: {e}")
        logger.error(traceback.format_exc())
    def _memory_usage(self) -> Dict[str, Any]:
        try:
            import psutil
            p = psutil.Process()
            m = p.memory_info()
            return {
                "rss_mb": round(m.rss / 1024 / 1024, 2),
                "vms_mb": round(m.vms / 1024 / 1024, 2),
                "cpu_percent": p.cpu_percent()
            }
        except Exception:
            return {"status": "unavailable"}


async def main():
    print("\n" + "="*80)
    print("💡 SHAN_D_SUPERADVANCED - ADVANCED AI ASSISTANT 💡")
    print("="*80 + "\n")

    app = ShanDApplication()
    if not await app.initialize():
        return 1

    # ——— NEW: launch FastAPI HTTP server ———
    cfg = app.config_manager.config
    host, port = cfg.get("host", "0.0.0.0"), cfg.get("port", 8000)
    server = uvicorn.Server(
        config=uvicorn.Config(app.app, host=host, port=port, loop="asyncio")
    )
    asyncio.create_task(server.serve())
    logger.info(f"🚀 FastAPI serving on http://{host}:{port}")

    # ——— NEW: start Telegram polling ———
    if app.telegram_app:
        asyncio.create_task(app.telegram_app.run_polling())
        logger.info("🚀 Telegram bot polling started")
    else:
        logger.error("⚠️ Telegram app not initialized; skipping polling")

    # Keep alive
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped by user")
        if app.telegram_app:
            await app.telegram_app.stop()
        return 0
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.error(traceback.format_exc())
        return 1
    finally:
        logger.info("📝 Application shutdown completed")

def run():
    try:
        code = asyncio.run(main())
        sys.exit(code)
    except Exception as e:
        logger.error(f"🔥 Critical failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
