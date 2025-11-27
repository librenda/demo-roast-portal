#!/bin/bash
# Quick start script for Akatos Pitch Roast Server

echo "🚀 Starting Akatos Pitch Roast Server..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo ""
python server.py

