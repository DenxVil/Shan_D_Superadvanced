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
import traceback
from pathlib import Path
from datetime import datetime
import signal
import json

# ◉Ɗєиνιℓ Trademark - Advanced AI Development

print("""
🌟 ══════════════════════════════════════════════════════════════════ 🌟
░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓███████▓▒░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
         ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
         ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░

🤖 Shan-D - Ultra-Enhanced Human-like AI Assistant
🧠 Advanced Learning + User Personalization + Self-Improvement
🏷️ Created by: ◉Ɗєиνιℓ
🎭 AI Name: Shan-D
📅 Version: 4.0.0 Ultra-Human Enhanced
🌍 Features: Complete User Analysis + Adaptive Learning

🌟 ══════════════════════════════════════════════════════════════════ 🌟
""")

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def log_detailed_error(error, context="General", additional_info=None):
    """Enhanced error logging with all details shown in console only"""
    error_details = {
        'timestamp': datetime.now().isoformat(),
        'context': context,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'traceback': traceback.format_exc(),
        'system_info': {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': os.getcwd(),
            'python_executable': sys.executable,
            'python_path': sys.path[:5],  # Show first 5 paths
            'environment_variables': {
                key: value for key, value in os.environ.items() 
                if any(keyword in key.upper() for keyword in ['TOKEN', 'API', 'KEY', 'PATH', 'HOME'])
            }
        }
    }
    
    if additional_info:
        error_details['additional_info'] = additional_info
    
    # Enhanced console output with full details
    print(f"\n" + "🚨" + "="*80)
    print(f"💥 COMPREHENSIVE ERROR ANALYSIS - {context.upper()}")
    print(f"🚨" + "="*80)
    
    print(f"\n⏰ **ERROR TIMESTAMP**")
    print(f"   📅 Date/Time: {error_details['timestamp']}")
    print(f"   🏷️ Context: {context}")
    
    print(f"\n🔥 **ERROR IDENTIFICATION**")
    print(f"   🏷️ Error Type: {error_details['error_type']}")
    print(f"   📝 Error Message: {error_details['error_message']}")
    print(f"   🎯 Error Class: {type(error).__module__}.{type(error).__name__}")
    
    if hasattr(error, 'args') and error.args:
        print(f"   📋 Error Arguments: {error.args}")
    
    print(f"\n🖥️ **SYSTEM ENVIRONMENT**")
    print(f"   🐍 Python Version: {error_details['system_info']['python_version']}")
    print(f"   💻 Platform: {error_details['system_info']['platform']}")
    print(f"   📂 Working Directory: {error_details['system_info']['working_directory']}")
    print(f"   🔧 Python Executable: {error_details['system_info']['python_executable']}")
    
    print(f"\n🛤️ **PYTHON PATH (First 5 entries)**")
    for i, path in enumerate(error_details['system_info']['python_path'], 1):
        print(f"   {i}. {path}")
    
    print(f"\n🔑 **RELEVANT ENVIRONMENT VARIABLES**")
    env_vars = error_details['system_info']['environment_variables']
    if env_vars:
        for key, value in env_vars.items():
            # Mask sensitive information
            if any(sensitive in key.upper() for sensitive in ['TOKEN', 'KEY', 'PASSWORD']):
                masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "*" * len(value)
                print(f"   🔐 {key}: {masked_value}")
            else:
                print(f"   📄 {key}: {value}")
    else:
        print(f"   ℹ️ No relevant environment variables found")
    
    if additional_info:
        print(f"\n🔍 **ADDITIONAL CONTEXT INFORMATION**")
        if isinstance(additional_info, dict):
            for key, value in additional_info.items():
                print(f"   📌 {key}:")
                if isinstance(value, (dict, list)):
                    for line in json.dumps(value, indent=6).split('\n'):
                        print(f"      {line}")
                else:
                    print(f"      {value}")
        else:
            print(f"   📝 {additional_info}")
    
    print(f"\n📚 **COMPLETE STACK TRACE**")
    print(f"{'─' * 80}")
    # Format the traceback for better readability
    traceback_lines = error_details['traceback'].split('\n')
    for i, line in enumerate(traceback_lines):
        if line.strip():
            if line.startswith('  File'):
                print(f"📁 {line}")
            elif line.startswith('    '):
                print(f"💻 {line}")
            elif 'Error:' in line or 'Exception:' in line:
                print(f"🔴 {line}")
            else:
                print(f"📄 {line}")
    print(f"{'─' * 80}")
    
    print(f"\n🎯 **ERROR RESOLUTION SUGGESTIONS**")
    error_type = type(error).__name__
    if error_type == "ImportError":
        print(f"   💡 1. Check if the module is installed: pip list | grep <module_name>")
        print(f"   💡 2. Verify module path is correct")
        print(f"   💡 3. Install missing package: pip install <package_name>")
        print(f"   💡 4. Check if virtual environment is activated")
    elif error_type == "ModuleNotFoundError":
        print(f"   💡 1. Install the missing module: pip install <module_name>")
        print(f"   💡 2. Check sys.path includes the module location")
        print(f"   💡 3. Verify spelling of module name")
    elif error_type == "AttributeError":
        print(f"   💡 1. Check if the attribute exists in the object")
        print(f"   💡 2. Verify object is properly initialized")
        print(f"   💡 3. Check for typos in attribute name")
    elif error_type == "SyntaxError":
        print(f"   💡 1. Check for missing brackets, quotes, or colons")
        print(f"   💡 2. Verify indentation is correct")
        print(f"   💡 3. Look for unclosed strings or comments")
    else:
        print(f"   💡 1. Check the error message for specific guidance")
        print(f"   💡 2. Verify all required dependencies are installed")
        print(f"   💡 3. Check file permissions and paths")
    
    print(f"\n📋 **DEBUGGING CHECKLIST**")
    print(f"   ☐ Verify all imports are correct")
    print(f"   ☐ Check file paths and permissions")
    print(f"   ☐ Ensure all dependencies are installed")
    print(f"   ☐ Validate configuration files")
    print(f"   ☐ Check environment variables")
    print(f"   ☐ Verify Python version compatibility")
    
    print(f"\n🚨" + "="*80)
    print(f"💥 END OF ERROR ANALYSIS - {context.upper()}")
    print(f"🚨" + "="*80 + "\n")

def check_import_dependencies():
    """Enhanced dependency checking with detailed console error reporting"""
    print("🔍 Checking import dependencies...")
    
    required_modules = [
        ('src.telegram.bot', 'ShanDBot'),
        ('configs.config', 'Config'),
        ('utils.helpers', ['setup_logging', 'check_dependencies']),
        ('core.shan_d_enhanced', 'EnhancedShanD'),
        ('core.command_processor', 'AdvancedCommandProcessor'),
        ('storage.user_data_manager', 'UserDataManager'),
        ('core.learning_engine', 'ContinuousLearningEngine')
    ]
    
    missing_modules = []
    import_errors = {}
    
    for module_info in required_modules:
        module_name = module_info[0]
        required_items = module_info[1] if isinstance(module_info[1], list) else [module_info[1]]
        
        try:
            print(f"   ✓ Checking {module_name}...")
            module = __import__(module_name, fromlist=required_items)
            
            for item in required_items:
                if not hasattr(module, item):
                    missing_modules.append(f"{module_name}.{item}")
                    print(f"   ❌ Missing: {module_name}.{item}")
                else:
                    print(f"   ✅ Found: {module_name}.{item}")
                    
        except ImportError as e:
            missing_modules.append(module_name)
            import_errors[module_name] = str(e)
            print(f"   ❌ Failed to import {module_name}: {e}")
        except Exception as e:
            import_errors[module_name] = f"Unexpected error: {str(e)}"
            print(f"   ⚠️ Unexpected error importing {module_name}: {e}")
    
    if missing_modules or import_errors:
        error_details = {
            'missing_modules': missing_modules,
            'import_errors': import_errors,
            'python_path': sys.path,
            'current_directory': os.getcwd(),
            'src_directory_exists': os.path.exists('src'),
            'directory_contents': os.listdir('.') if os.path.exists('.') else [],
            'src_contents': os.listdir('src') if os.path.exists('src') else 'src directory not found'
        }
        
        log_detailed_error(
            ImportError(f"Missing modules: {missing_modules}"),
            "Module Import Check",
            error_details
        )
        
        print("📦 Attempting to install requirements...")
        try:
            if os.path.exists('requirements.txt'):
                print("📋 Found requirements.txt, installing...")
                os.system("pip install -r requirements.txt")
                print("✅ Requirements installation completed")
            else:
                print("⚠️ No requirements.txt found")
                print("📋 Common packages you might need:")
                print("   pip install python-telegram-bot")
                print("   pip install aiohttp")
                print("   pip install asyncio")
        except Exception as install_error:
            log_detailed_error(install_error, "Requirements Installation")
        
        return False
    
    print("✅ All import dependencies satisfied")
    return True

# Enhanced import section with detailed error handling
try:
    if not check_import_dependencies():
        print("❌ Dependency check failed. Please check the error details above.")
        sys.exit(1)
    
    # Import all required modules
    from src.telegram.bot import ShanDBot
    from configs.config import Config
    from utils.helpers import setup_logging, check_dependencies
    from core.shan_d_enhanced import EnhancedShanD
    from core.command_processor import AdvancedCommandProcessor
    from storage.user_data_manager import UserDataManager
    from core.learning_engine import ContinuousLearningEngine
    
    print("✅ All modules imported successfully")
    
except ImportError as e:
    log_detailed_error(e, "Module Import", {
        'attempted_modules': [
            'src.telegram.bot', 'configs.config', 'utils.helpers',
            'core.shan_d_enhanced', 'core.command_processor',
            'storage.user_data_manager', 'core.learning_engine'
        ],
        'python_path': sys.path,
        'working_directory': os.getcwd(),
        'available_files': os.listdir('.') if os.path.exists('.') else []
    })
    sys.exit(1)
except Exception as e:
    log_detailed_error(e, "Unexpected Import Error")
    sys.exit(1)

# Setup enhanced logging with ◉Ɗєиνιℓ branding
try:
    logger = setup_logging()
    print("✅ Logging system initialized")
except Exception as e:
    log_detailed_error(e, "Logging Setup")
    # Continue without enhanced logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class UltraShanDApplication:
    """Ultra-enhanced application manager with complete learning capabilities"""
    
    def __init__(self):
        try:
            print("🚀 Initializing UltraShanDApplication...")
            self.config = Config()
            self.bot = None
            self.shan_d_brain = None
            self.command_processor = None
            self.user_data_manager = None
            self.learning_engine = None
            self.running = False
            
            # Setup signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            print("✅ UltraShanDApplication initialized successfully")
            
        except Exception as e:
            log_detailed_error(e, "Application Initialization", {
                'config_loaded': hasattr(self, 'config'),
                'available_attributes': dir(self),
                'config_type': type(self.config).__name__ if hasattr(self, 'config') else 'N/A'
            })
            raise

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        try:
            logger.info("🛑 Ultra-Human AI shutdown signal received...")
            self.running = False
        except Exception as e:
            log_detailed_error(e, "Signal Handler")

    async def startup_checks(self):
        """Perform comprehensive startup checks with detailed error reporting"""
        try:
            logger.info("🔍 Performing ultra-enhanced startup checks...")
            
            # Check dependencies with detailed reporting
            print("📋 Checking system dependencies...")
            if not check_dependencies():
                raise RuntimeError("❌ Missing required system dependencies")
            
            # Validate configuration with detailed checks
            print("🔧 Validating configuration...")
            config_issues = []
            
            if not hasattr(self.config, 'TELEGRAM_TOKEN') or not self.config.TELEGRAM_TOKEN:
                config_issues.append("TELEGRAM_TOKEN not found in environment or config")
            
            if not hasattr(self.config, 'get_branding_info'):
                config_issues.append("get_branding_info method missing from config")
            
            if config_issues:
                log_detailed_error(
                    RuntimeError("Configuration validation failed"),
                    "Configuration Check",
                    {
                        'issues': config_issues,
                        'config_attributes': dir(self.config),
                        'config_type': type(self.config).__name__,
                        'environment_vars': [k for k in os.environ.keys() if 'TOKEN' in k.upper()],
                        'config_dict': vars(self.config) if hasattr(self.config, '__dict__') else 'No __dict__ available'
                    }
                )
                raise RuntimeError(f"Configuration issues: {config_issues}")
            
            # Create data directories with error handling
            print("📁 Creating data directories...")
            directories = ["data/users", "data/learning", "data/analytics"]
            for directory in directories:
                try:
                    os.makedirs(directory, exist_ok=True)
                    print(f"   ✅ {directory}")
                except Exception as dir_error:
                    log_detailed_error(dir_error, f"Directory Creation - {directory}", {
                        'directory': directory,
                        'parent_exists': os.path.exists(os.path.dirname(directory)),
                        'permissions': oct(os.stat('.').st_mode)[-3:] if os.path.exists('.') else 'N/A'
                    })
                    raise
            
            # Initialize components with detailed error handling
            print("🧠 Initializing Ultra-Human AI components...")
            
            try:
                self.user_data_manager = UserDataManager()
                print("   ✅ UserDataManager initialized")
            except Exception as e:
                log_detailed_error(e, "UserDataManager Initialization", {
                    'UserDataManager_available': 'UserDataManager' in globals(),
                    'module_path': UserDataManager.__module__ if 'UserDataManager' in globals() else 'N/A'
                })
                raise
            
            try:
                self.learning_engine = ContinuousLearningEngine()
                print("   ✅ ContinuousLearningEngine initialized")
            except Exception as e:
                log_detailed_error(e, "ContinuousLearningEngine Initialization", {
                    'ContinuousLearningEngine_available': 'ContinuousLearningEngine' in globals(),
                    'module_path': ContinuousLearningEngine.__module__ if 'ContinuousLearningEngine' in globals() else 'N/A'
                })
                raise
            
            try:
                self.shan_d_brain = EnhancedShanD(
                    user_data_manager=self.user_data_manager,
                    learning_engine=self.learning_engine
                )
                print("   ✅ EnhancedShanD brain initialized")
            except Exception as e:
                log_detailed_error(e, "EnhancedShanD Initialization", {
                    'user_data_manager_type': type(self.user_data_manager).__name__,
                    'learning_engine_type': type(self.learning_engine).__name__,
                    'user_data_manager_methods': dir(self.user_data_manager),
                    'learning_engine_methods': dir(self.learning_engine)
                })
                raise
            
            try:
                self.command_processor = AdvancedCommandProcessor(self.shan_d_brain)
                print("   ✅ AdvancedCommandProcessor initialized")
            except Exception as e:
                log_detailed_error(e, "AdvancedCommandProcessor Initialization", {
                    'shan_d_brain_type': type(self.shan_d_brain).__name__,
                    'shan_d_brain_methods': dir(self.shan_d_brain)
                })
                raise
            
            logger.info("✅ All ultra-enhanced startup checks passed!")
            
        except Exception as e:
            log_detailed_error(e, "Startup Checks", {
                'completed_components': [
                    name for name in ['user_data_manager', 'learning_engine', 'shan_d_brain', 'command_processor']
                    if hasattr(self, name) and getattr(self, name) is not None
                ],
                'component_status': {
                    'user_data_manager': hasattr(self, 'user_data_manager'),
                    'learning_engine': hasattr(self, 'learning_engine'),
                    'shan_d_brain': hasattr(self, 'shan_d_brain'),
                    'command_processor': hasattr(self, 'command_processor')
                }
            })
            raise

    async def start(self):
        """Start the Ultra-Human Shan-D application with enhanced error handling"""
        try:
            await self.startup_checks()
            
            logger.info("🚀 Initializing Shan-D Ultra-Human AI Assistant...")
            logger.info("🏷️ Created by: ◉Ɗєиνιℓ - Advanced AI Development")
            
            # Display enhanced branding information with error handling
            try:
                branding = self.config.get_branding_info()
                logger.info(f"🤖 AI Name: {branding['ai_name']}")
                logger.info(f"📊 Version: {branding['version']}")
                logger.info(f"🌟 Technology: {branding['trademark']}")
            except Exception as branding_error:
                log_detailed_error(branding_error, "Branding Information", {
                    'config_methods': [method for method in dir(self.config) if not method.startswith('_')],
                    'config_type': type(self.config).__name__
                })
                logger.warning("⚠️ Could not load branding information, continuing...")
            
            logger.info("💬 Enhanced Capabilities:")
            logger.info(" 📈 Complete User Analysis & Story Generation")
            logger.info(" 🧠 Self-Improving from Every Conversation")
            logger.info(" 🎭 Adaptive Personalization for Each User")
            logger.info(" 🌍 Internet-Scale Knowledge Integration")
            logger.info(" 💝 Ultra-Human Emotional Intelligence")
            
            # Initialize enhanced bot with detailed error handling
            try:
                self.bot = ShanDBot(
                    self.shan_d_brain,
                    self.command_processor,
                    self.user_data_manager
                )
                logger.info("✅ ShanDBot initialized successfully")
            except Exception as bot_error:
                log_detailed_error(bot_error, "ShanDBot Initialization", {
                    'brain_available': self.shan_d_brain is not None,
                    'processor_available': self.command_processor is not None,
                    'data_manager_available': self.user_data_manager is not None,
                    'ShanDBot_signature': ShanDBot.__init__.__code__.co_varnames if hasattr(ShanDBot, '__init__') else 'N/A'
                })
                raise
            
            self.running = True
            
            # Start background learning tasks with error handling
            try:
                await self._start_background_learning()
            except Exception as bg_error:
                log_detailed_error(bg_error, "Background Learning Startup")
                logger.warning("⚠️ Background learning failed to start, continuing without it...")
            
            # Start the bot with error handling
            try:
                await self.bot.start()
                logger.info("✅ Shan-D Ultra-Human AI is now live and ready!")
            except Exception as start_error:
                log_detailed_error(start_error, "Bot Startup", {
                    'bot_type': type(self.bot).__name__,
                    'bot_methods': dir(self.bot)
                })
                raise
            
            logger.info("🌟 Advanced learning and personalization active!")
            logger.info("🎭 User analysis, self-improvement, and adaptation enabled!")
            
            # Keep running until signal received
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("👋 Shan-D Ultra-Human AI shutting down gracefully...")
        except Exception as e:
            log_detailed_error(e, "Application Startup", {
                'running_state': self.running,
                'bot_initialized': self.bot is not None,
                'components_status': {
                    'config': self.config is not None,
                    'brain': self.shan_d_brain is not None,
                    'processor': self.command_processor is not None,
                    'data_manager': self.user_data_manager is not None,
                    'learning_engine': self.learning_engine is not None
                }
            })
            raise
        finally:
            await self.cleanup()

    async def _start_background_learning(self):
        """Start background learning and analysis tasks with error handling"""
        try:
            logger.info("🎓 Starting background learning engine...")
            
            # Start continuous learning tasks with individual error handling
            tasks = []
            
            try:
                task1 = asyncio.create_task(self.learning_engine.continuous_learning_loop())
                tasks.append(('continuous_learning', task1))
            except Exception as e:
                log_detailed_error(e, "Continuous Learning Task Creation")
            
            try:
                task2 = asyncio.create_task(self.user_data_manager.periodic_user_analysis())
                tasks.append(('user_analysis', task2))
            except Exception as e:
                log_detailed_error(e, "User Analysis Task Creation")
            
            try:
                task3 = asyncio.create_task(self._performance_monitoring())
                tasks.append(('performance_monitoring', task3))
            except Exception as e:
                log_detailed_error(e, "Performance Monitoring Task Creation")
            
            logger.info(f"✅ Started {len(tasks)} background learning tasks")
            
        except Exception as e:
            log_detailed_error(e, "Background Learning Initialization")
            raise

    async def _performance_monitoring(self):
        """Monitor and log AI performance metrics with error handling"""
        while self.running:
            try:
                await asyncio.sleep(3600)  # Every hour
                analytics = await self.shan_d_brain.get_ultra_human_analytics()
                logger.info(f"📊 Performance: {analytics.get('human_like_percentage', 0):.1f}% human-like responses")
            except Exception as e:
                log_detailed_error(e, "Performance Monitoring")
                await asyncio.sleep(300)  # Wait 5 minutes before retry

    async def cleanup(self):
        """Cleanup resources on shutdown with detailed error handling"""
        logger.info("🧹 Cleaning up ultra-human AI resources...")
        
        cleanup_tasks = [
            ('bot_stop', self.bot.stop if self.bot else None),
            ('brain_save', self.shan_d_brain.emergency_save if self.shan_d_brain else None),
            ('user_data_save', self.user_data_manager.save_all_pending_data if self.user_data_manager else None),
            ('learning_save', self.learning_engine.save_learning_state if self.learning_engine else None)
        ]
        
        for task_name, task_func in cleanup_tasks:
            if task_func:
                try:
                    if asyncio.iscoroutinefunction(task_func):
                        await task_func()
                    else:
                        task_func()
                    logger.info(f"✅ {task_name} completed")
                except Exception as e:
                    log_detailed_error(e, f"Cleanup Task - {task_name}")
        
        logger.info("🏷️ Thank you for using ◉Ɗєиνιℓ Ultra-Human AI Technology")
        logger.info("👋 Shan-D Ultra-Human AI shutdown complete")

async def main():
    """Ultra-enhanced main entry point with comprehensive error handling"""
    try:
        print("🚀 Starting Shan-D Ultra-Human AI Application...")
        app = UltraShanDApplication()
        await app.start()
    except KeyboardInterrupt:
        print("\n👋 Ultra-Human AI says goodbye!")
    except Exception as e:
        log_detailed_error(e, "Main Application", {
            'command_line_args': sys.argv,
            'working_directory': os.getcwd(),
            'python_executable': sys.executable,
            'script_location': __file__
        })
        print(f"💥 Fatal error in Ultra-Human AI. Check error details above.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Ultra-Human AI says goodbye!")
    except Exception as e:
        log_detailed_error(e, "Application Entry Point")
        sys.exit(1) 
