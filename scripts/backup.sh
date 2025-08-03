#!/bin/bash
# Shan-D Backup Script
# Created by: ◉Ɗєиνιℓ 

echo "💾 Creating backup of Shan-D data..."

# Create backup directory
backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

# Backup user data
echo "📊 Backing up user data..."
cp -r data/ "$backup_dir/"

# Backup logs
echo "📝 Backing up logs..."
cp -r logs/ "$backup_dir/" 2>/dev/null || true

# Create archive
echo "📦 Creating archive..."
tar -czf "${backup_dir}.tar.gz" "$backup_dir"
rm -rf "$backup_dir"

echo "✅ Backup created: ${backup_dir}.tar.gz"
echo "🏷️ Secured by ◉Ɗєиνιℓ Advanced AI Technology"
