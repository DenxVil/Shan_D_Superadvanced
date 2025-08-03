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
import yaml
import argparse
from aiohttp import web

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
        # Ensure logs directory exists
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Setup file handlers
        log_file = log_dir / f"shan_d_{datetime.now().strftime('%Y%m%d')}.log"
        error_log_file = log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Setup console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # Configure root logger
        self.logger = logging.getLogger("ShanD")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
        
        # Suppress noisy third-party loggers
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("anthropic").setLevel(logging.WARNING)
        try:
            from src.web_app import create_web_app
            WEB_APP_AVAILABLE = True
        except ImportError: 
            WEB_APP_AVAILABLE = False
    
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
        """Validate existing structure and create missing components"""
        logger.info("🔍 Validating application structure...")
        
        try:
            app_root = Path.cwd()
            logger.info(f"Application root: {app_root}")
            
            # Create missing directories
            for dir_path in cls.REQUIRED_DIRECTORIES:
                full_path = app_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"✅ Directory ensured: {dir_path}")
            
            # Validate critical files exist
            missing_files = []
            for file_path in cls.CRITICAL_FILES:
                full_path = app_root / file_path
                if not full_path.exists():
                    missing_files.append(file_path)
            
            if missing_files:
                logger.warning(f"⚠️ Missing critical files: {missing_files}")
                # Continue anyway as some files might be optional
            
            # Create runtime configuration if needed
            cls._ensure_runtime_config(app_root)
            
            logger.info("✅ Directory structure validation completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Directory validation failed: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    @classmethod
    def _ensure_runtime_config(cls, app_root: Path):
        """Ensure runtime configuration files exist"""
        
        # Create runtime settings if missing
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
        self.config = {}
        self.settings = {}
        
    def load_configurations(self) -> bool:
        """Load all configuration files"""
        try:
            logger.info("📝 Loading application configurations...")
            
            # Load YAML settings
            self._load_yaml_settings()
            
            # Load environment variables
            self._load_env_config()
            
            # Load API keys
            self._load_api_keys()
            
            # Validate configuration
            self._validate_config()
            
            logger.info("✅ Configuration loading completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Configuration loading failed: {str(e)}")
            return False
    
    def _load_yaml_settings(self):
        """Load settings from YAML file"""
        settings_file = Path("configs/settings.yaml")
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                self.settings = yaml.safe_load(f) or {}
            logger.debug("✅ YAML settings loaded")
        else:
            logger.warning("⚠️ settings.yaml not found, using defaults")
            self.settings = self._get_default_settings()
    
    def _load_env_config(self):
        """Load environment-based configuration"""
        self.config.update({
            'debug': os.getenv('DEBUG', 'false').lower() == 'true',
            'host': os.getenv('HOST', '0.0.0.0'),
            'port': int(os.getenv('PORT', 8000)),
            'environment': os.getenv('ENVIRONMENT', 'production')
        })
    
    def _load_api_keys(self):
        """Load API keys from environment or config files"""
        api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY'),
            'google': os.getenv('GOOGLE_API_KEY'),
            'telegram': os.getenv('TELEGRAM_BOT_TOKEN')
        }
        
        # Filter out None values
        self.config['api_keys'] = {k: v for k, v in api_keys.items() if v}
        
        logger.info(f"🔑 Loaded {len(self.config['api_keys'])} API keys")
    
    def _validate_config(self):
        """Validate critical configuration values"""
        if not self.config.get('api_keys'):
            logger.warning("⚠️ No API keys configured - some features may not work")
        
        # Validate port range
        port = self.config.get('port', 8000)
        if not (1024 <= port <= 65535):
            logger.warning(f"⚠️ Invalid port {port}, using default 8000")
            self.config['port'] = 8000
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Return default settings if YAML file is missing"""
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
        self.config = config or {}
        self.logger = logging.getLogger("ShanD")
        self.web_app = None
        self.config_manager = ConfigurationManager()
        self.components = {}
        self.is_initialized = False
        self.app = Nonet
        
    async def initialize(self) -> bool:
        """Initialize the complete application"""
        self.logger.info("✅ Shan_D_Superadvanced initialization completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {str(e)}")
            raise
            
            # Load configurations
            if not self.config_manager.load_configurations():
                return False
            
            # Initialize core components
            await self._initialize_core_components()
            
            # Setup web interface
            await self._setup_web_interface()
            
            # Initialize AI models
            await self._initialize_ai_models()
            
            # Setup integrations
            await self._setup_integrations()
            
            self.is_initialized = True
            self.logger.info("✅ Shan_D_Superadvanced initialization completed successfully")
            return True
            
        self.logger.info("✅ Shan_D_Superadvanced initialization completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {str(e)}")
            raise
    
    
    async def initialize_web_app(self):
        """NEW METHOD: Initialize web application"""
        if not WEB_APP_AVAILABLE:
            raise RuntimeError("❌ Web application module not available")
        
        try:
            self.web_app = await create_web_app(self)
            self.logger.info("✅ Web application initialized successfully")
            return self.web_app
        except Exception as e:
            self.logger.error(f"❌ Web application initialization failed: {str(e)}")
            raise
    
    async def run_web_server(self, host="0.0.0.0", port=8080):
        """NEW METHOD: Run web server"""
        if not self.web_app:
            await self.initialize_web_app()
        
        self.logger.info(f"🌐 Starting web server on {host}:{port}")
        web.run_app(self.web_app, host=host, port=port)
    
    async def _initialize_core_components(self):
        """Initialize core AI components"""
        logger.info("🧠 Initializing core AI components...")
        
        try:
            # Import and initialize core modules
            from src.core.emotion_engine import AdvancedEmotionEngine
            from src.core.memory_manager import AdvancedMemoryManager
            from src.core.learning_engine import ContinuousLearningEngine 
            from src.core.model_manager import AdvancedModelManager
            from src.core.conversation_flow import ShanDConversationFlow
            from src.core.multimodal_processor import MultimodalProcessor
            
            # Initialize components
            self.components['emotion_engine'] = AdvancedEmotionEngine()
            self.components['memory_manager'] = AdvancedMemoryManager()
            self.components['learning_engine'] = ContinuousLearningEngine()
            # Replace line  main.py
            config = {'debug': True}  # Minimal config
            self.components['model_manager'] = AdvancedModelManager(config)
            
            self.components['conversation_flow'] = ShanDConversationFlow()
            self.components['multimodal_processor'] = MultimodalProcessor(config)
            
            # Initialize each component
            for name, component in self.components.items():
                if hasattr(component, 'initialize'):
                    await component.initialize()
                logger.debug(f"✅ {name} initialized")
            
            logger.info("✅ Core components initialized successfully")
            
        except ImportError as e:
            logger.error(f"❌ Failed to import core modules: {str(e)}")
            # Create mock components for graceful degradation
            self.components = {name: None for name in [
                'emotion_engine', 'memory_manager', 'learning_engine',
                'model_manager', 'conversation_flow', 'multimodal_processor'
            ]}
        except Exception as e:
            logger.error(f"❌ Core component initialization failed: {str(e)}")
            raise
    
    async def _setup_web_interface(self):
        """Setup FastAPI web interface"""
        logger.info("🌐 Setting up web interface...")
        
        try:
            from fastapi import FastAPI, HTTPException, Depends
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.responses import JSONResponse
            from fastapi.staticfiles import StaticFiles
            import uvicorn
            
            # Create FastAPI app
            self.app = FastAPI(
                title="Shan_D_Superadvanced",
                version="2.0.0",
                description="Advanced AI Assistant with Emotional Intelligence",
                docs_url="/docs",
                redoc_url="/redoc"
            )
            
            # Add CORS middleware
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Setup static files
            if Path("static").exists():
                self.app.mount("/static", StaticFiles(directory="static"), name="static")
            
            # Setup routes
            await self._setup_routes()
            
            logger.info("✅ Web interface setup completed")
            
        except ImportError:
            logger.warning("⚠️ FastAPI not available, web interface disabled")
            self.app = None
        except Exception as e:
            logger.error(f"❌ Web interface setup failed: {str(e)}")
            self.app = None
    
    async def _setup_routes(self):
        """Setup API routes"""
        if not self.app:
            return
        
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
            component_status = {}
            for name, component in self.components.items():
                component_status[name] = "active" if component else "inactive"
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": component_status,
                "memory_usage": self._get_memory_usage()
            }
        
        @self.app.post("/chat")
        async def chat_endpoint(message: dict):
            try:
                # Process message through conversation flow
                if self.components.get('conversation_flow'):
                    response = await self.components['conversation_flow'].process_message(
                        message.get('text', ''),
                        message.get('user_id', 'anonymous'),
                        message.get('context', {})
                    )
                else:
                    response = {
                        "text": "I'm currently initializing. Please try again in a moment.",
                        "status": "initializing"
                    }
                
                return response
                
            except Exception as e:
                logger.error(f"Chat endpoint error: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        logger.info("✅ API routes configured")
    
    async def _initialize_ai_models(self):
        """Initialize AI models and validate API connections"""
        logger.info("🤖 Initializing AI models...")
        
        try:
            model_manager = self.components.get('model_manager')
            if model_manager and hasattr(model_manager, 'initialize_models'):
                await model_manager.initialize_models(
                    self.config_manager.config.get('api_keys', {})
                )
                logger.info("✅ AI models initialized")
            else:
                logger.warning("⚠️ Model manager not available")
                
        except Exception as e:
            logger.error(f"❌ AI model initialization failed: {str(e)}")
    
    async def _setup_integrations(self):
        """Setup external integrations (Telegram, etc.)"""
        logger.info("🔗 Setting up integrations...")
        
        try:
            # Setup Telegram bot if token is available
            telegram_token = self.config_manager.config.get('api_keys', {}).get('telegram')
            if telegram_token:
                # Import and setup telegram integration
                logger.info("✅ Telegram integration available")
            else:
                logger.info("ℹ️ Telegram integration not configured")
                
        except Exception as e:
            logger.error(f"❌ Integration setup failed: {str(e)}")
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                "rss_mb": round(memory_info.rss / 1024 / 1024, 2),
                "vms_mb": round(memory_info.vms / 1024 / 1024, 2),
                "cpu_percent": process.cpu_percent()
            }
        except ImportError:
            return {"status": "psutil not available"}
        except Exception as e:
            return {"error": str(e)}
    
    async def start_server(self):
        """Start the web server"""
        if not self.app:
            logger.error("❌ No web application available to start")
            return False
        
        try:
            import uvicorn
            
            config = self.config_manager.config
            host = config.get('host', '0.0.0.0')
            port = config.get('port', 8000)
            
            logger.info(f"🌟 Starting Shan_D_Superadvanced server...")
            logger.info(f"🌐 Server available at http://{host}:{port}")
            logger.info(f"📚 API documentation at http://{host}:{port}/docs")
            
            uvicorn_config = uvicorn.Config(
                self.app,
                host=host,
                port=port,
                log_level="info" if not config.get('debug') else "debug",
                access_log=True
            )
            
            server = uvicorn.Server(uvicorn_config)
            await server.serve()
            
        except ImportError:
            logger.error("❌ uvicorn not available, cannot start web server")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to start server: {str(e)}")
            return False

async def main():
    """Main application entry point"""
    print("\n" + "="*80)
    print("🌟 SHAN_D_SUPERADVANCED - ADVANCED AI ASSISTANT 🌟")
    print("="*80)
    print("🧠 Features: Emotion Engine | Learning System | Memory Management")
    print("🤖 Models: Multi-AI Support | Multimodal Processing")
    print("🌐 Interface: REST API | Telegram Bot | Web UI")
    print("="*80 + "\n")
    
    try:
        args = parse_args()
        # Step 1: Validate directory structure
        logger.info("🔍 Starting application validation...")
        if not DirectoryStructureManager.validate_and_setup():
            logger.error("❌ Directory structure validation failed")
            return 1
        
        # Step 2: Initialize application
        app = ShanDApplication()
        if not await app.initialize():
            logger.error("❌ Application initialization failed")
            return 1
        
        # Step 3: Start server
        await app.start_server()
        shan_d = ShanDAdvanced()  # Use your existing initialization
        await shan_d.initialize()
        
        # Run based on mode
        if args.mode == "web":
            if not WEB_APP_AVAILABLE:
                print("❌ Web application not available. Install aiohttp: pip install aiohttp")
                return
            await shan_d.run_web_server(host=args.host, port=args.port)
            
        elif args.mode == "hybrid":
            if not WEB_APP_AVAILABLE:
                print("❌ Web application not available. Running bot only...")
                # Your existing bot start code
                return
            
            # Start web app in background
            await shan_d.initialize_web_app()
            
            # Start both (this is simplified - you might need to adjust based on your bot implementation)
            import asyncio
            bot_task = asyncio.create_task(shan_d.start_bot())  # Your existing bot start method
            web_task = asyncio.create_task(shan_d.run_web_server(args.host, args.port))
            await asyncio.gather(bot_task, web_task)
        return 0
        
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return 1
    finally:
        logger.info("🏁 Application shutdown completed")

def run():
    """Synchronous entry point"""
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"❌ Critical failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start: {str(e)}")
