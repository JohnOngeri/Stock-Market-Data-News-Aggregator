#!/bin/bash

echo "Starting Stock Market Data & News Aggregator"
echo "============================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys"
    echo ""
    read -p "Press Enter to continue..."
    exit 1
fi

# Start the application
echo "Starting Flask application..."
echo "Application will be available at http://localhost:8080"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py