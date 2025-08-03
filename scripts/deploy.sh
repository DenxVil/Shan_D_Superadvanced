#!/bin/bash
# Shan-D Deployment Script
# Created by: ◉Ɗєиνιℓ 🧑‍💻

echo "🌟 Deploying Shan-D Ultra-Human AI Assistant... 🤖"

# Set up environment
echo "📦 Setting up environment..."
python -m venv shan_d_env
source shan_d_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download language models
echo "🧠 Downloading language models..."
python -m spacy download en_core_web_sm

# Set up data directories
echo "📁 Creating data directories..."
mkdir -p data/users
mkdir -p data/learning
mkdir -p data/analytics
mkdir -p logs

# Check configuration
echo "⚙️ Checking configuration..."
if [ ! -f .env ]; then
    echo "❌ .env file not found! Please copy .env.example to .env and configure it."
    exit 1
fi

# Test the application
echo "🧪 Testing application..."
python -c "
import sys
sys.path.insert(0, 'src')
from configs.config import Config
config = Config()
if not config.validate_config():
    print('❌ Configuration validation failed!')
    sys.exit(1)
print('✅ Configuration is valid!')
"

echo "✅ Shan-D 👻 deployment completed successfully!"
echo "🚀 Run 'python main.py' to start the AI assistant"
echo "🏷️ Created by ◉Ɗєиνιℓ 🧑‍💻 Advanced AI Technology"
