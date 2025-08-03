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
from fastapi import FastAPI
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
        logger.info("ð Validating application structure...")
        
        try:
            app_root = Path.cwd()
            logger.info(f"Application root: {app_root}")
            
            # Create missing directories
            for dir_path in cls.REQUIRED_DIRECTORIES:
                full_path = app_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"â Directory ensured: {dir_path}")
            
            # Validate critical files exist
            missing_files = []
            for file_path in cls.CRITICAL_FILES:
                full_path = app_root / file_path
                if not full_path.exists():
                    missing_files.append(file_path)
            
            if missing_files:
                logger.warning(f"â ï¸ Missing critical files: {missing_files}")
                # Continue anyway as some files might be optional
            
            # Create runtime configuration if needed
            cls._ensure_runtime_config(app_root)
            
            logger.info("â Directory structure validation completed")
            return True
            
        except Exception as e:
            logger.error(f"â Directory validation failed: {str(e)}")
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
            
            logger.info(f"â Created runtime configuration: {runtime_config}")

class ConfigurationManager:
    """Manages application configuration loading and validation"""
    
    def __init__(self):
        self.config = {}
        self.settings = {}
        
    def load_configurations(self) -> bool:
        """Load all configuration files"""
        try:
            logger.info("ð Loading application configurations...")
            
            # Load YAML settings
            self._load_yaml_settings()
            
            # Load environment variables
            self._load_env_config()
            
            # Load API keys
            self._load_api_keys()
            
            # Validate configuration
            self._validate_config()
            
            logger.info("â Configuration loading completed")
            return True
            
        except Exception as e:
            logger.error(f"â Configuration loading failed: {str(e)}")
            return False
    
    def _load_yaml_settings(self):
        """Load settings from YAML file"""
        settings_file = Path("configs/settings.yaml")
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                self.settings = yaml.safe_load(f) or {}
            logger.debug("â YAML settings loaded")
        else:
            logger.warning("â ï¸ settings.yaml not found, using defaults")
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
        
        logger.info(f"ð Loaded {len(self.config['api_keys'])} API keys")
    
    def _validate_config(self):
        """Validate critical configuration values"""
        if not self.config.get('api_keys'):
            logger.warning("â ï¸ No API keys configured - some features may not work")
        
        # Validate port range
        port = self.config.get('port', 8000)
        if not (1024 <= port <= 65535):
            logger.warning(f"â ï¸ Invalid port {port}, using default 8000")
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
        self.config_manager = ConfigurationManager()
        self.components = {}
        self.is_initialized = False
        self.app = None
        
    async def initialize(self) -> bool:
        """Initialize the complete application"""
        try:
            logger.info("ð Initializing Shan_D_Superadvanced...")
            
            # Load configurations
            if not self.config_manager.load_configurations():
                return False
            
            # Initialize core components
            await self._initialize_core_components()
            
       
            # Initialize AI models
            await self._initialize_ai_models()
            
            # Setup integrations
            await self._setup_integrations()
            
            self.is_initialized = True
            logger.info("â Shan_D_Superadvanced initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"â Application initialization failed: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    async def _initialize_core_components(self):
        """Initialize core AI components"""
        logger.info("ð§  Initializing core AI components...")
        
        try:
            # Import and initialize core modules
            from src.core.emotion_engine import AdvancedEmotionEngine
            from src.core.memory_manager import AdvancedMemoryManager
            from src.core.learning_engine import ContinuousLearningEngine 
            from src.core.model_manager import AdvancedModelManager
            from src.core.conversation_flow import ShanDConversationFlow
            from src.core.multimodal_processor import MultimodalProcessor
            
            # Initialize components
            config = {'debug': True}  # Minimal configconfig = {'debug': True}  # Minimal config
            self.components['emotion_engine'] = AdvancedEmotionEngine()
            self.components['memory_manager'] = AdvancedMemoryManager()
            self.components['learning_engine'] = ContinuousLearningEngine()
            self.components['model_manager'] = AdvancedModelManager(config)
            self.components['conversation_flow'] = ShanDConversationFlow()
            self.components['multimodal_processor'] = MultimodalProcessor(config)
            
            # Initialize each component
            for name, component in self.components.items():
                if hasattr(component, 'initialize'):
                    await component.initialize()
                logger.debug(f"â {name} initialized")
            
            logger.info("â Core components initialized successfully")
            
        except ImportError as e:
            logger.error(f"â Failed to import core modules: {str(e)}")
            # Create mock components for graceful degradation
            self.components = {name: None for name in [
                'emotion_engine', 'memory_manager', 'learning_engine',
                'model_manager', 'conversation_flow', 'multimodal_processor'
            ]}
        except Exception as e:
            logger.error(f"â Core component initialization failed: {str(e)}")
            raise
    
    
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
        
        logger.info("â API routes configured")
    
    async def _initialize_ai_models(self):
        """Initialize AI models and validate API connections"""
        logger.info("ð¤ Initializing AI models...")
        
        try:
            model_manager = self.components.get('model_manager')
            if model_manager and hasattr(model_manager, 'initialize_models'):
                await model_manager.initialize_models(
                    self.config_manager.config.get('api_keys', {})
                )
                logger.info("â AI models initialized")
            else:
                logger.warning("â ï¸ Model manager not available")
                
        except Exception as e:
            logger.error(f"â AI model initialization failed: {str(e)}")
    
    async def _setup_integrations(self):
        """Setup external integrations (Telegram, etc.)"""
        logger.info("ð Setting up integrations...")
        
        try:
            # Setup Telegram bot if token is available
            telegram_token = self.config_manager.config.get('api_keys', {}).get('telegram')
            if telegram_token:
                # Import and setup telegram integration
                logger.info("â Telegram integration available")
            else:
                logger.info("â¹ï¸ Telegram integration not configured")
                
        except Exception as e:
            logger.error(f"â Integration setup failed: {str(e)}")
    
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
            logger.error("â No web application available to start")
            return False
        
        try:
            import uvicorn
            
            config = self.config_manager.config
            host = config.get('host', '0.0.0.0')
            port = config.get('port', 8000)
            
            logger.info(f"ð Starting Shan_D_Superadvanced server...")
            logger.info(f"ð Server available at http://{host}:{port}")
            logger.info(f"ð API documentation at http://{host}:{port}/docs")
            
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
            logger.error("â uvicorn not available, cannot start web server")
            return False
        except Exception as e:
            logger.error(f"â Failed to start server: {str(e)}")
            return False

async def main():
    """Main application entry point"""
    print("\n" + "="*80)
    print("ð SHAN_D_SUPERADVANCED - ADVANCED AI ASSISTANT ð")
    print("="*80)
    print("ð§  Features: Emotion Engine | Learning System | Memory Management")
    print("ð¤ Models: Multi-AI Support | Multimodal Processing")
    print("ð Interface: REST API | Telegram Bot | Web UI")
    print("="*80 + "\n")
    
    try:
        # Step 1: Validate directory structure
        logger.info("ð Starting application validation...")
        if not DirectoryStructureManager.validate_and_setup():
            logger.error("â Directory structure validation failed")
            return 1
        
        # Step 2: Initialize application
        app = ShanDApplication()
        if not await app.initialize():
            logger.error("â Application initialization failed")
            return 1
        
        # Step 3: Start server
        await app.start_server()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("ð Application stopped by user")
        return 0
    except Exception as e:
        logger.error(f"â Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return 1
    finally:
        logger.info("ð Application shutdown completed")

def run():
    """Synchronous entry point"""
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"â Critical failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    
    
    
    run()
