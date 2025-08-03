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
from typing import Dict, Any, Optional
import json
from fastapi import FastAPI, HTTPException
import yaml

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
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        log_file = log_dir / f"shan_d_{datetime.now():%Y%m%d}.log"
        error_log_file = log_dir / f"errors_{datetime.now():%Y%m%d}.log"

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        self.logger = logging.getLogger("ShanD")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)

        # Suppress noisy third-party loggers
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
        logger.info("🔄 Validating application structure...")
        try:
            app_root = Path.cwd()
            logger.info(f"Application root: {app_root}")

            for dir_path in cls.REQUIRED_DIRECTORIES:
                full_path = app_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"✅ Directory ensured: {dir_path}")

            missing_files = []
            for file_path in cls.CRITICAL_FILES:
                if not (app_root / file_path).exists():
                    missing_files.append(file_path)
            if missing_files:
                logger.warning(f"⚠️ Missing critical files: {missing_files}")

            cls._ensure_runtime_config(app_root)
            logger.info("✅ Directory structure validation completed")
            return True

        except Exception as e:
            logger.error(f"❌ Directory validation failed: {e}")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def _ensure_runtime_config(cls, app_root: Path):
        """Ensure runtime configuration files exist"""
        runtime_config = app_root / "runtime_config.json"
        if not runtime_config.exists():
            config_data = {
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
            with open(runtime_config, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
            logger.info(f"✅ Created runtime configuration: {runtime_config}")


class ConfigurationManager:
    """Manages application configuration loading and validation"""

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {}

    def load_configurations(self) -> bool:
        try:
            logger.info("🔄 Loading application configurations...")
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
        settings_file = Path("configs/settings.yaml")
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                self.settings = yaml.safe_load(f) or {}
            logger.debug("✅ YAML settings loaded")
        else:
            logger.warning("⚠️ settings.yaml not found, using defaults")
            self.settings = self._get_default_settings()

    def _load_env_config(self):
        self.config.update({
            'debug': os.getenv('DEBUG', 'false').lower() == 'true',
            'host': os.getenv('HOST', '0.0.0.0'),
            'port': int(os.getenv('PORT', 8000)),
            'environment': os.getenv('ENVIRONMENT', 'production')
        })

    def _load_api_keys(self):
        api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY'),
            'google': os.getenv('GOOGLE_API_KEY'),
            'telegram': os.getenv('TELEGRAM_BOT_TOKEN')
        }
        self.config['api_keys'] = {k: v for k, v in api_keys.items() if v}
        logger.info(f"🔑 Loaded {len(self.config['api_keys'])} API keys")

    def _validate_config(self):
        if not self.config.get('api_keys'):
            logger.warning("⚠️ No API keys configured - some features may not work")
        port = self.config.get('port', 8000)
        if not (1024 <= port <= 65535):
            logger.warning(f"⚠️ Invalid port {port}, using default 8000")
            self.config['port'] = 8000

    def _get_default_settings(self) -> Dict[str, Any]:
        return {
            'app': {
                'name': 'Shan_D_Superadvanced',
                'version': '2.0.0',
                'description': 'Advanced AI Assistant with Emotional Intelligence'
            },
            'features': {
                'emotion_processing': True,
                'adaptive_learning': True,
                'memory_persistence': True,
                'multimodal_support': True
            },
            'limits': {
                'max_conversation_length': 50,
                'memory_retention_days': 30,
                'max_file_size_mb': 10
            }
        }


class ShanDApplication:
    """Main application class integrating all components"""

    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.components: Dict[str, Any] = {}
        self.is_initialized: bool = False
        self.app: Optional[FastAPI] = None
        self.telegram_app = None

    async def initialize(self) -> bool:
        try:
            logger.info("🔄 Initializing Shan_D_Superadvanced...")
            if not self.config_manager.load_configurations():
                return False

            DirectoryStructureManager.validate_and_setup()
            await self._initialize_core_components()
            await self._initialize_ai_models()
            await self._setup_routes()
            await self._setup_integrations()

            self.is_initialized = True
            logger.info("✅ Shan_D_Superadvanced initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Application initialization failed: {e}")
            logger.error(traceback.format_exc())
            return False

    async def _initialize_core_components(self):
        logger.info("🔧 Initializing core AI components...")
        try:
            from src.core.emotion_engine import AdvancedEmotionEngine
            from src.core.memory_manager import AdvancedMemoryManager
            from src.core.learning_engine import ContinuousLearningEngine
            from src.core.model_manager import AdvancedModelManager
            from src.core.conversation_flow import ShanDConversationFlow
            from src.core.multimodal_processor import MultimodalProcessor

            cfg = {'debug': True}
            self.components['emotion_engine'] = AdvancedEmotionEngine()
            self.components['memory_manager'] = AdvancedMemoryManager()
            self.components['learning_engine'] = ContinuousLearningEngine()
            self.components['model_manager'] = AdvancedModelManager(cfg)
            self.components['conversation_flow'] = ShanDConversationFlow()
            self.components['multimodal_processor'] = MultimodalProcessor(cfg)

            for name, comp in self.components.items():
                if hasattr(comp, 'initialize'):
                    await comp.initialize()
                    logger.debug(f"✅ {name} initialized")

            logger.info("✅ Core components initialized successfully")

        except ImportError as e:
            logger.error(f"❌ Failed to import core modules: {e}")
            self.components = {n: None for n in self.components}

        except Exception as e:
            logger.error(f"❌ Core component initialization failed: {e}")
            raise

    async def _initialize_ai_models(self):
        logger.info("🔄 Initializing AI models...")
        try:
            mm = self.components.get('model_manager')
            if mm and hasattr(mm, 'initialize_models'):
                await mm.initialize_models(self.config_manager.config.get('api_keys', {}))
                logger.info("✅ AI models initialized")
            else:
                logger.warning("⚠️ Model manager not available")

        except Exception as e:
            logger.error(f"❌ AI model initialization failed: {e}")

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
        async def health_check():
            component_status = {
                name: "active" if comp else "inactive"
                for name, comp in self.components.items()
            }
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": component_status,
                "memory_usage": self._get_memory_usage()
            }

        @self.app.post("/chat")
        async def chat_endpoint(message: Dict[str, Any]):
            try:
                flow = self.components.get('conversation_flow')
                if flow:
                    resp = await flow.process_message(
                        message.get('text', ''), 
                        message.get('user_id', 'anonymous'), 
                        message.get('context', {})
                    )
                else:
                    resp = {"text": "Initializing, try again soon", "status": "initializing"}
                return resp

            except Exception as e:
                logger.error(f"❌ Chat endpoint error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

        logger.info("✅ API routes configured")

    async def _setup_integrations(self):
        """Setup external integrations (Telegram, etc.)"""
        logger.info("🔗 Setting up integrations...")
        try:
            token = self.config_manager.config.get('api_keys', {}).get('telegram')
            if token:
                from telegram.ext import ApplicationBuilder, CommandHandler

                app_bot = ApplicationBuilder().token(token).build()

                async def _start(update, context):
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Hi there! Shan-D bot is alive."
                    )

                app_bot.add_handler(CommandHandler("start", _start))

                await app_bot.initialize()
                await app_bot.start()
                self.telegram_app = app_bot
                logger.info("🚀 Telegram bot launched via Application")

            else:
                logger.info("⚠️ Telegram integration not configured")

        except Exception as e:
            logger.error(f"❌ Integration setup failed: {e}")
            logger.error(traceback.format_exc())

    def _get_memory_usage(self) -> Dict[str, Any]:
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
    """Main application entry point"""
    print("\n" + "=" * 80)
    print("💡 SHAN_D_SUPERADVANCED - ADVANCED AI ASSISTANT 💡")
    print("=" * 80 + "\n")

    app = ShanDApplication()
    if not await app.initialize():
        return 1

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
    """Synchronous entry point"""
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"🔥 Critical failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
