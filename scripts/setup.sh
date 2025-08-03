#!/bin/bash
# Shan-D Setup Script
# Created by: ◉Ɗєиνιℓ

echo "🌟 Setting up Shan-D Ultra-Human AI Assistant... 👻"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed 🙃"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/users
mkdir -p data/learning
mkdir -p data/analytics
mkdir -p logs

# Copy environment template
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
fi

echo "🎉 Setup complete! Run 'python main.py' to start Shan-D"
echo "🏷️ Created by ◉Ɗєиνιℓ Advanced AI Technology"
