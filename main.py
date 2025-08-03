#!/usr/bin/env python3
"""
Shan_D_Superadvanced – Main entry point combining FastAPI and async Telegram polling
"""
import os
import sys
import asyncio
import logging
import traceback
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import yaml
from fastapi import FastAPI, HTTPException
import uvicorn
from telegram.ext import ApplicationBuilder, CommandHandler

# Ensure src on PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

#
# Enhanced Logger
#
class EnhancedLogger:
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

        root = logging.getLogger("ShanD")
        root.setLevel(logging.DEBUG)
        root.addHandler(file_h)
        root.addHandler(err_h)
        root.addHandler(console)

        # Silence noisy libs
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("anthropic").setLevel(logging.WARNING)

        self.logger = root

    def get_logger(self):
        return self.logger

# Global logger
logger = EnhancedLogger().get_logger()


#
# Directory & Config Management
#
class DirectoryManager:
    REQUIRED_DIRS = [
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
        try:
            logger.info("🔍 Validating directory structure...")
            root = Path.cwd()
            for d in cls.REQUIRED_DIRS:
                (root / d).mkdir(parents=True, exist_ok=True)
            missing = [f for f in cls.CRITICAL_FILES if not (root / f).exists()]
            if missing:
                logger.warning(f"⚠ Missing critical files: {missing}")
                cls._create_runtime_config(root)
            logger.info("✔ Directory validation complete")
            return True
        except Exception as e:
            logger.error(f"✖ Directory validation failed: {e}")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def _create_runtime_config(cls, root: Path):
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
            cfg.write_text(yaml.safe_dump(data, sort_keys=False))
            logger.info(f"✔ Created runtime config: {cfg}")


class ConfigurationManager:
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {}

    def load(self) -> bool:
        try:
            logger.info("🔍 Loading configurations...")
            self._load_yaml()
            self._load_env()
            self._load_api_keys()
            self._validate()
            logger.info("✔ Configurations loaded")
            return True
        except Exception as e:
            logger.error(f"✖ Configuration load failed: {e}")
            logger.error(traceback.format_exc())
            return False

    def _load_yaml(self):
        p = Path("configs/settings.yaml")
        if p.exists():
            self.settings = yaml.safe_load(p.read_text()) or {}
            logger.debug("✔ YAML settings loaded")
        else:
            logger.warning("⚠ settings.yaml missing, using defaults")
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
            logger.warning("⚠ No API keys configured")
        p = self.config.get("port", 8000)
        if not (1024 < p < 65535):
            logger.warning(f"⚠ Invalid port {p}, defaulting to 8000")
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


#
# Main Application
#
class ShanDApplication:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.components: Dict[str, Any] = {}
        self.app: Optional[FastAPI] = None
        self.telegram_app = None

    async def initialize(self) -> bool:
        try:
            if not self.config_manager.load():
                return False
            DirectoryManager.validate_and_setup()
            await self._init_core_components()
            await self._init_models()
            self._setup_http_routes()
            await self._setup_telegram_integration()
            return True
        except Exception as e:
            logger.error(f"✖ Initialization failed: {e}")
            logger.error(traceback.format_exc())
            return False

    async def _init_core_components(self):
        from src.core.emotion_engine import AdvancedEmotionEngine
        from src.core.memory_manager import AdvancedMemoryManager
        from src.core.learning_engine import ContinuousLearningEngine
        from src.core.model_manager import AdvancedModelManager
        from src.core.conversation_flow import ShanDConversationFlow
        from src.core.multimodal_processor import MultimodalProcessor

        self.components = {
            "emotion_engine": AdvancedEmotionEngine(),
            "memory_manager": AdvancedMemoryManager(),
            "learning_engine": ContinuousLearningEngine(),
            "model_manager": AdvancedModelManager({"debug": True}),
            "conversation_flow": ShanDConversationFlow(),
            "multimodal_processor": MultimodalProcessor({"debug": True})
        }
        for name, comp in self.components.items():
            if hasattr(comp, "initialize"):
                await comp.initialize()
                logger.info(f"✔ Initialized {name}")

    async def _init_models(self):
        mgr = self.components.get("model_manager")
        if mgr:
            await mgr.initialize_models(self.config_manager.config.get("api_keys", {}))
            logger.info("✔ Models initialized")

    def _setup_http_routes(self):
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
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    name: ("active" if comp else "inactive")
                    for name, comp in self.components.items()
                }
            }

        @self.app.post("/chat")
        async def chat(msg: Dict[str, Any]):
            flow = self.components.get("conversation_flow")
            if not flow:
                raise HTTPException(status_code=503, detail="Not initialized")
            try:
                return await flow.process_message(
                    msg.get("text", ""),
                    msg.get("user_id", ""),
                    msg.get("context", {})
                )
            except Exception as ex:
                logger.error(f"Chat error: {ex}")
                raise HTTPException(status_code=500, detail="Internal error")

    async def _setup_telegram_integration(self):
        token = self.config_manager.config["api_keys"].get("telegram")
        if not token:
            logger.warning("⚠ Telegram token missing—bot disabled")
            return

        bot_app = ApplicationBuilder().token(token).build()

        async def start_cmd(update, context):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✔ Shan_D is online!"
            )

        bot_app.add_handler(CommandHandler("start", start_cmd))
        await bot_app.initialize()
        await bot_app.updater.start_polling()
        logger.info("🚀 Telegram polling started")
        self.telegram_app = bot_app


#
# Serve and run
#
async def _serve():
    app_obj = ShanDApplication()
    if not await app_obj.initialize():
        sys.exit(1)

    cfg = app_obj.config_manager.config
    host, port = cfg["host"], cfg["port"]

    server = uvicorn.Server(config=uvicorn.Config(app_obj.app, host=host, port=port))
    http_task = asyncio.create_task(server.serve())

    stop_event = asyncio.Future()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set_result, None)

    if app_obj.telegram_app:
        # Keep the Telegram app running alongside HTTP
        # (polling already started in initialize)
        pass

    await stop_event
    logger.info("🔋 Shutdown signal received")

    if app_obj.telegram_app:
        await app_obj.telegram_app.updater.stop_polling()
        await app_obj.telegram_app.stop()
        await app_obj.telegram_app.shutdown()

    server.should_exit = True
    http_task.cancel()

    logger.info("📦 Shutdown complete")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(_serve())
