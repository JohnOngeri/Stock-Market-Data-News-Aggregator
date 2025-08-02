#!/bin/bash

# Simple systemd deployment script for Stock Market Aggregator
# No Docker required - uses systemd services

echo "🚀 Stock Market Aggregator - Simple Systemd Deployment"
echo "====================================================="

APP_NAME="stock-market-app"
APP_DIR="/opt/stock-market-aggregator"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"

# Step 1: Install dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nginx

# Step 2: Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Step 3: Copy application files
echo "📋 Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Step 4: Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Step 5: Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Stock Market Data Aggregator
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:8080 app:app
Restart=always
RestartSec=3
EnvironmentFile=$APP_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

# Step 6: Enable and start service
echo "🔄 Starting service..."
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME

# Step 7: Check status
echo "✅ Checking service status..."
sudo systemctl status $APP_NAME --no-pager

echo "🎉 Deployment complete!"
echo "Service running on port 8080"
echo "Check status: sudo systemctl status $APP_NAME"
echo "View logs: sudo journalctl -u $APP_NAME -f"