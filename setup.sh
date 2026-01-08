#!/bin/bash

# Terminal RPG - Setup Script
# For Linux/macOS

echo "🎮 Terminal RPG - Setup Script"
echo "================================"

# Check Python version
echo "📌 Checking Python version..."
python3 --version

if ! command -v python3.11 &> /dev/null
then
    echo "❌ Python 3.11+ required. Please install it first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -e ".[dev]"

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p src/{core,entities,systems,world,ui/{components,screens,themes},data,utils}
mkdir -p data/genres/cyberpunk/{locations,npcs,dialogues,enemies,items}
mkdir -p saves
mkdir -p logs
mkdir -p tests
mkdir -p docs

touch saves/.gitkeep
touch logs/.gitkeep

# Success message
echo ""
echo "✅ Setup complete!"
echo ""
echo "To start developing:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the game: python -m src.main"
echo ""
echo "Happy coding! 🚀"
