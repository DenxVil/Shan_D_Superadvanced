#Denvil


import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Load configuration from files and environment variables"""
    
    # Load environment variables
    load_dotenv('config/api_keys.env')
    
    # Load YAML configuration
    config_path = Path('config/settings.yaml')
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    
    # Override with environment variables
    config.update({
        'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
        'google_api_key': os.getenv('GOOGLE_API_KEY', ''),
        'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'max_concurrent_requests': int(os.getenv('MAX_CONCURRENT_REQUESTS', '50')),
        'request_timeout': int(os.getenv('REQUEST_TIMEOUT', '60')),
        'enable_reasoning_engine': os.getenv('ENABLE_REASONING_ENGINE', 'true').lower() == 'true',
        'enable_multimodal': os.getenv('ENABLE_MULTIMODAL', 'true').lower() == 'true',
        'enable_auto_fix': os.getenv('ENABLE_AUTO_FIX', 'true').lower() == 'true',
    })
    
    return config
