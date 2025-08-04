#!/usr/bin/env python3

"""
Shan_D_Superadvanced - Advanced AI Assistant Main Entry Point
Enhanced version with full integration of existing modules and robust error handling
"""

import os
import sys
import asyncio
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json
import yaml

# Telegram imports
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Add src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

class EnhancedLogger:
    """Enhanced logging system with multiple output streams"""
    def __init__(self):
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        """Setup comprehensive logging configuration"""
        log_dir = Path("logs"); log_dir.mkdir(exist_ok=True)
        detailed_fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handlers
        lf = log_dir / f"shan_d_{datetime.now().strftime('%Y%m%d')}.log"
        ef = log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        fh = logging.FileHandler(lf, encoding='utf-8'); fh.setLevel(logging.DEBUG); fh.setFormatter(detailed_fmt)
        eh = logging.FileHandler(ef, encoding='utf-8'); eh.setLevel(logging.ERROR); eh.setFormatter(detailed_fmt)

        # Console handler
        ch = logging.StreamHandler(sys.stdout); ch.setLevel(logging.INFO); ch.setFormatter(simple_fmt)

        self.logger = logging.getLogger("ShanD")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(fh); self.logger.addHandler(eh); self.logger.addHandler(ch)

        # Suppress noisy libs
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("anthropic").setLevel(logging.WARNING)

    def get_logger(self):
        return self.logger

# Initialize global logger
log_manager = EnhancedLogger()
logger = log_manager.get_logger()

class DirectoryStructureManager:
    """Manages application directory structure and validates environment"""
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
        logger.info("🔍 Validating application structure...")
        try:
            root = Path.cwd()
            for d in cls.REQUIRED_DIRECTORIES:
                (root / d).mkdir(parents=True, exist_ok=True)
                logger.debug(f"✅ Directory ensured: {d}")
            missing = [f for f in cls.CRITICAL_FILES if not (root / f).exists()]
            if missing:
                logger.warning(f"⚠️ Missing critical files: {missing}")
            cls._ensure_runtime_config(root)
            logger.info("✅ Directory structure validation completed")
            return True
        except Exception as e:
            logger.error(f"❌ Directory validation failed: {e}")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def _ensure_runtime_config(cls, app_root: Path):
        rc = app_root / "runtime_config.json"
        if not rc.exists():
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
            rc.write_text(json.dumps(data, indent=2), encoding='utf-8')
            logger.info(f"✅ Created runtime configuration: {rc}")

class ConfigurationManager:
    """Manages application configuration loading and validation"""
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {}

    def load_configurations(self) -> bool:
        try:
            logger.info("📝 Loading application configurations...")
            self._load_yaml_settings()
            self._load_env_config()
            self._load_api_keys()
            self._validate_config()
            logger.info("✅ Configuration loading completed")
            return True
        except Exception as e:
            logger.error(f"❌ Configuration loading failed: {e}")
            return False

    def _load_yaml_settings(self):
        sf = Path("configs/settings.yaml")
        if sf.exists():
            self.settings = yaml.safe_load(sf.read_text()) or {}
            logger.debug("✅ YAML settings loaded")
        else:
            logger.warning("⚠️ settings.yaml not found, using defaults")
            self.settings = self._get_default_settings()

    def _load_env_config(self):
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

    def _validate_config(self):
        if not self.config.get("api_keys"):
            logger.warning("⚠️ No API keys configured - some features may not work")
        p = self.config.get("port", 8000)
        if not (1024 <= p <= 65535):
            logger.warning(f"⚠️ Invalid port {p}, using default 8000")
            self.config["port"] = 8000

    def _get_default_settings(self) -> Dict[str, Any]:
        return {
            "app": {"name": "Shan_D_Superadvanced", "version": "2.0.0"},
            "features": {
                "emotion_processing": True,
                "adaptive_learning": True,
                "memory_persistence": True,
                "multimodal_support": True
            },
            "limits": {
                "max_conversation_length": 50,
                "memory_retention_days": 30,
                "max_file_size_mb": 10
            }
        }

class ShanDApplication:
    """Main application class integrating all components"""
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.components: Dict[str, Any] = {}
        self.app = None
        self.telegram_app = None

    async def initialize(self) -> bool:
        try:
            logger.info("🚀 Initializing Shan_D_Superadvanced...")
            if not self.config_manager.load_configurations():
                return False
            await self._initialize_core_components()
            await self._setup_web_interface()
            await self._initialize_ai_models()
            await self._setup_integrations()
            logger.info("✅ Initialization completed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            logger.error(traceback.format_exc())
            return False

    async def _initialize_core_components(self):
        logger.info("🧠 Initializing core AI components...")
        # Dynamic import & init with isolation
        pairs = [
            ("emotion_engine", "AdvancedEmotionEngine"),
            ("memory_manager", "AdvancedMemoryManager"),
            ("learning_engine", "ContinuousLearningEngine"),
            ("model_manager", "AdvancedModelManager"),
            ("conversation_flow", "ShanDConversationFlow"),
            ("multimodal_processor", "MultimodalProcessor"),
        ]
        for name, cls_name in pairs:
            try:
                module = __import__(f"src.core.{name}", fromlist=[cls_name])
                cls = getattr(module, cls_name)
                inst = cls()
                if hasattr(inst, "initialize"):
                    await inst.initialize()
                self.components[name] = inst
                logger.debug(f"✅ {name} initialized")
            except Exception as e:
                logger.error(f"⚠️ {name} failed: {e}")
                self.components[name] = None

    async def _setup_web_interface(self):
        logger.info("🌐 Setting up web interface...")
        try:
            from fastapi import FastAPI, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.staticfiles import StaticFiles
            import uvicorn

            self.app = FastAPI(
                title="Shan_D_Superadvanced",
                version="2.0.0",
                docs_url="/docs",
                redoc_url="/redoc",
            )
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"], allow_credentials=True,
                allow_methods=["*"], allow_headers=["*"],
            )
            if Path("static").exists():
                self.app.mount("/static", StaticFiles(directory="static"), name="static")

            @self.app.get("/")
            async def root():
                return {
                    "message": "Welcome to Shan_D_Superadvanced",
                    "status": "operational",
                    "features": list(self.components.keys()),
                }

            @self.app.get("/health")
            async def health_check():
                status = {
                    n: ("active" if c else "inactive")
                    for n, c in self.components.items()
                }
                return {"status": "healthy", "components": status}

            @self.app.post("/chat")
            async def chat_endpoint(message: Dict[str, Any]):
                try:
                    conv = self.components.get("conversation_flow")
                    if conv:
                        resp = await conv.process_message(
                            message.get("text", ""),
                            message.get("user_id", "anon"),
                            message.get("context", {}),
                        )
                        return resp
                    return {"text": "Initializing…", "status": "initializing"}
                except Exception as e:
                    logger.error(f"Chat error: {e}")
                    raise HTTPException(status_code=500, detail="Internal error")

            logger.info("✅ Web interface setup completed")
        except ImportError:
            logger.warning("⚠️ FastAPI not available; web interface disabled")
            self.app = None
        except Exception as e:
            logger.error(f"❌ Web setup failed: {e}")
            self.app = None

    async def _initialize_ai_models(self):
        logger.info("🤖 Initializing AI models...")
        try:
            mgr = self.components.get("model_manager")
            if mgr and hasattr(mgr, "initialize_models"):
                await mgr.initialize_models(self.config_manager.config.get("api_keys", {}))
                logger.info("✅ AI models initialized")
            else:
                logger.warning("⚠️ Model manager unavailable")
        except Exception as e:
            logger.error(f"❌ AI model initialization failed: {e}")

    async def _setup_integrations(self):
        logger.info("🔗 Setting up integrations...")
        try:
            token = self.config_manager.config["api_keys"].get("telegram")
            if token:
                self.telegram_app = (
                    ApplicationBuilder().token(token).build()
                )
                # Handlers
                self.telegram_app.add_handler(CommandHandler("start", self._on_start))
                self.telegram_app.add_handler(
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_telegram_message)
                )
                logger.info("✅ Telegram integration configured")
            else:
                logger.info("ℹ️ Telegram integration not configured")
        except Exception as e:
            logger.error(f"❌ Integration setup failed: {e}")

    async def _on_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👋 Welcome! I'm online and ready to chat.")

    async def _on_telegram_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        text = update.message.text
        uid = str(update.effective_user.id)
        try:
            conv = self.components.get("conversation_flow")
            if conv:
                resp = await conv.process_message(text, uid, {})
                await update.message.reply_text(resp.get("text", "..."))
            else:
                await update.message.reply_text("🤖 Initializing, please wait…")
        except Exception as e:
            logger.warning(f"Feature failure: {e}")
            await update.message.reply_text("⚠️ Sorry, something's not available right now.")

    async def start_server(self):
        # FastAPI server
        if self.app:
            import uvicorn
            cfg = self.config_manager.config
            server = uvicorn.Server(
                uvicorn.Config(
                    self.app,
                    host=cfg.get("host", "0.0.0.0"),
                    port=cfg.get("port", 8000),
                    log_level="info" if not cfg.get("debug") else "debug",
                )
            )
            # Run both servers concurrently
            server_task = asyncio.create_task(server.serve())
        else:
            server_task = None

        # Telegram polling
        if self.telegram_app:
            tg_task = asyncio.create_task(
                self.telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)
            )
        else:
            tg_task = None

        # Await both
        tasks = [t for t in (server_task, tg_task) if t]
        if tasks:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    async def shutdown(self):
        # Clean up Telegram
        if self.telegram_app:
            logger.info("👋 Stopping Telegram bot…")
            await self.telegram_app.shutdown()
            await self.telegram_app.wait_closed()

async def main():
    print("\n" + "=" * 80)
    print("🌟 SHAN_D_SUPERADVANCED - ADVANCED AI ASSISTANT 🌟")
    print("=" * 80)
    logger.info("🔍 Starting application validation...")
    if not DirectoryStructureManager.validate_and_setup():
        return 1

    app = ShanDApplication()
    if not await app.initialize():
        return 1

    try:
        await app.start_server()
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")
    finally:
        await app.shutdown()
        logger.info("🏁 Application shutdown completed")
    return 0

def run():
    """Synchronous entry point"""
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"❌ Critical failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
