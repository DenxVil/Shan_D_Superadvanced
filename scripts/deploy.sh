#!/bin/bash
# Shan-D Deployment Script
# Created by: ◉Ɗєиνιℓ

echo "🚀 Deploying Shan-D Ultra-Human AI Assistant..."

# Pull latest changes
git pull origin main

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t shan-d-ai:latest .

# Stop existing container
echo "🛑 Stopping existing container..."
docker stop shan-d-ai 2>/dev/null || true
docker rm shan-d-ai 2>/dev/null || true

# Start new container
echo "▶️ Starting new container..."
docker run -d \
    --name shan-d-ai \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    --restart unless-stopped \
    shan-d-ai:latest

echo "✅ Deployment complete!"
echo "🏷️ Powered by ◉Ɗєиνιℓ Advanced AI Technology"
