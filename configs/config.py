"""
Configuration for Shan-D Ultra-Enhanced AI Assistant
Created by: ◉Ɗєиνιℓ 
"""
import os
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables
load_dotenv()

class Config:
    """Enhanced configuration class with advanced settings"""
    # Add this to your existing config.py


    
    def __init__(self):
        # Core Bot Settings
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        
        # AI Model Configuration
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
        self.GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        
        # Database Settings
        self.DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///shan_d.db')
        self.REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        # Enhanced AI Settings
        self.MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '50'))
        self.LEARNING_ENABLED = os.getenv('LEARNING_ENABLED', 'True').lower() == 'true'
        self.USER_ANALYSIS_ENABLED = os.getenv('USER_ANALYSIS_ENABLED', 'True').lower() == 'true'
        
        # Security & Admin
        self.ADMIN_USER_IDS = [int(x) for x in os.getenv('ADMIN_USER_IDS', '').split(',') if x]
        self.ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
        
        # Performance Settings
        self.MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', '10'))
        self.RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', '30'))
        
        # Logging & Monitoring
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'True').lower() == 'true'
        
        # Language & Cultural Settings
        self.DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
        self.SUPPORTED_LANGUAGES = ['en', 'hi', 'mr', 'ta', 'te', 'bn']
        self.CULTURAL_CONTEXT = os.getenv('CULTURAL_CONTEXT', 'indian')
        
        # Storage Settings
        self.DATA_RETENTION_DAYS = int(os.getenv('DATA_RETENTION_DAYS', '90'))
        self.BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'True').lower() == 'true'
        
    def get_branding_info(self) -> Dict:
        """Get branding information"""
        return {
            'ai_name': 'Shan-D',
            'creator': '◉Ɗєиνιℓ ',
            'version': '4.0.0 Ultra-Human Enhanced',
            'trademark': '◉Ɗєиνιℓ Advanced AI Technology'
        }
    
    def validate_config(self) -> bool:
        """Validate critical configuration settings"""
        if not self.TELEGRAM_TOKEN:
            return False
        return True
    # Add this to your existing config.py

WEB_CONFIG = {
    'host': '0.0.0.0',
    'port': 8080,
    'secret_key': 'your-secret-key-change-this-in-production',
    'cors_origins': ['*'],
    'max_request_size': 16 * 1024 * 1024,  # 16MB
    'websocket_heartbeat': 30,
    'static_files': True
}

def get_web_config():
    """Get web application configuration"""
    return WEB_CONFIG
