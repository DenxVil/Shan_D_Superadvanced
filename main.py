#!/usr/bin/env python3
"""
Enhanced Main Application Entry Point
Addresses directory structure issues and provides robust startup sequence
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import traceback
from datetime import datetime

# Configure logging first
def setup_logging():
    """Setup comprehensive logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Setup file handler
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

# Initialize logging
logger = setup_logging()

class DirectoryManager:
    """Manages application directory structure"""
    
    REQUIRED_DIRECTORIES = [
        "data",
        "config", 
        "logs",
        "temp",
        "uploads",
        "models",
        "cache",
        "static",
        "templates"
    ]
    
    REQUIRED_FILES = [
        "config/app_config.py",
        "config/settings.json"
    ]
    
    @classmethod
    def ensure_directory_structure(cls) -> bool:
        """
        Ensure all required directories and files exist
        Returns True if successful, False otherwise
        """
        logger.info("🔍 Starting directory structure verification...")
        
        try:
            # Get application root directory
            app_root = Path.cwd()
            logger.info(f"Application root: {app_root}")
            
            # Create required directories
            for dir_name in cls.REQUIRED_DIRECTORIES:
                dir_path = app_root / dir_name
                dir_path.mkdir(exist_ok=True)
                logger.debug(f"✅ Directory ensured: {dir_path}")
            
            # Create required files with default content
            cls._create_default_files(app_root)
            
            # Verify permissions
            cls._verify_permissions(app_root)
            
            logger.info("✅ Directory structure verification completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Directory structure check failed: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    @classmethod
    def _create_default_files(cls, app_root: Path):
        """Create required files with default content"""
        
        # Create default app config
        config_file = app_root / "config" / "app_config.py"
        if not config_file.exists():
            config_content = '''"""
Application Configuration
"""
import os
from pathlib import Path

# Application settings
APP_NAME = "Shan_D_Superadvance"
VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Database Configuration (if needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
'''
            config_file.write_text(config_content)
            logger.info(f"✅ Created default config: {config_file}")
        
        # Create default settings
        settings_file = app_root / "config" / "settings.json"
        if not settings_file.exists():
            settings_content = '''{
    "app": {
        "name": "Shan_D_Superadvance",
        "version": "1.0.0",
        "environment": "production"
    },
    "features": {
        "ai_chat": true,
        "file_processing": true,
        "web_interface": true
    },
    "limits": {
        "max_file_size": 10485760,
        "max_requests_per_minute": 60
    }
}'''
            settings_file.write_text(settings_content)
            logger.info(f"✅ Created default settings: {settings_file}")
    
    @classmethod
    def _verify_permissions(cls, app_root: Path):
        """Verify read/write permissions for critical directories"""
        critical_dirs = ["data", "logs", "temp", "cache"]
        
        for dir_name in critical_dirs:
            dir_path = app_root / dir_name
            
            # Test write permission
            test_file = dir_path / ".permission_test"
            try:
                test_file.write_text("test")
                test_file.unlink()
                logger.debug(f"✅ Write permission verified: {dir_path}")
            except Exception as e:
                raise PermissionError(f"No write permission for {dir_path}: {e}")

class ApplicationCore:
    """Main application core management"""
    
    def __init__(self):
        self.app = None
        self.config = None
        self.is_running = False
        
    async def initialize(self) -> bool:
        """Initialize the application"""
        try:
            logger.info("🚀 Initializing Shan_D_Superadvance application...")
            
            # Load configuration
            await self._load_configuration()
            
            # Initialize components
            await self._initialize_components()
            
            # Setup routes and services
            await self._setup_services()
            
            logger.info("✅ Application initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Application initialization failed: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    async def _load_configuration(self):
        """Load application configuration"""
        try:
            # Import config after ensuring directory structure
            sys.path.append(str(Path.cwd()))
            from config.app_config import *
            
            self.config = {
                'app_name': globals().get('APP_NAME', 'Shan_D_Superadvance'),
                'version': globals().get('VERSION', '1.0.0'),
                'debug': globals().get('DEBUG', False),
                'host': globals().get('HOST', '0.0.0.0'),
                'port': globals().get('PORT', 8000)
            }
            
            logger.info(f"✅ Configuration loaded: {self.config['app_name']} v{self.config['version']}")
            
        except ImportError as e:
            logger.warning(f"Could not import config, using defaults: {e}")
            self.config = {
                'app_name': 'Shan_D_Superadvance',
                'version': '1.0.0',
                'debug': False,
                'host': '0.0.0.0',
                'port': 8000
            }
    
    async def _initialize_components(self):
        """Initialize application components"""
        logger.info("🔧 Initializing application components...")
        
        # Initialize FastAPI if available
        try:
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            
            self.app = FastAPI(
                title=self.config['app_name'],
                version=self.config['version'],
                debug=self.config['debug']
            )
            
            # Add CORS middleware
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            logger.info("✅ FastAPI application initialized")
            
        except ImportError:
            logger.warning("FastAPI not available, skipping web interface")
    
    async def _setup_services(self):
        """Setup application services and routes"""
        if self.app:
            # Health check endpoint
            @self.app.get("/health")
            async def health_check():
                return {
                    "status": "healthy",
                    "app": self.config['app_name'],
                    "version": self.config['version'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Root endpoint
            @self.app.get("/")
            async def root():
                return {
                    "message": f"Welcome to {self.config['app_name']}",
                    "version": self.config['version'],
                    "docs": "/docs"
                }
            
            logger.info("✅ Basic routes configured")
    
    async def start(self):
        """Start the application"""
        if not self.app:
            logger.error("❌ No application instance available to start")
            return False
        
        try:
            import uvicorn
            
            logger.info(f"🌟 Starting {self.config['app_name']} server...")
            logger.info(f"🌐 Server will be available at http://{self.config['host']}:{self.config['port']}")
            logger.info(f"📚 API documentation at http://{self.config['host']}:{self.config['port']}/docs")
            
            self.is_running = True
            
            # Start server
            config = uvicorn.Config(
                self.app,
                host=self.config['host'],
                port=self.config['port'],
                log_level="info" if not self.config['debug'] else "debug"
            )
            server = uvicorn.Server(config)
            await server.serve()
            
        except ImportError:
            logger.error("❌ uvicorn not available, cannot start web server")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to start server: {str(e)}")
            return False

async def main():
    """Main application entry point"""
    logger.info("🌟 ====================================================================== 🌟")
    logger.info("🚀 Starting Shan_D_Superadvance Application")
    logger.info("🌟 ====================================================================== 🌟")
    
    try:
        # Step 1: Ensure directory structure
        if not DirectoryManager.ensure_directory_structure():
            logger.error("❌ Failed to create required directory structure")
            return 1
        
        # Step 2: Initialize application
        app_core = ApplicationCore()
        if not await app_core.initialize():
            logger.error("❌ Failed to initialize application")
            return 1
        
        # Step 3: Start application
        await app_core.start()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return 1

def run_sync():
    """Synchronous wrapper for the main async function"""
    try:
        return asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Failed to run application: {str(e)}")
        return 1

if __name__ == "__main__":
    # Print startup banner
    print("\n" + "="*70)
    print("🌟 SHAN_D_SUPERADVANCE - ENHANCED STARTUP 🌟")
    print("="*70 + "\n")
    
    exit_code = run_sync()
    
    if exit_code == 0:
        logger.info("✅ Application completed successfully")
    else:
        logger.error(f"❌ Application exited with code: {exit_code}")
    
    sys.exit(exit_code)
