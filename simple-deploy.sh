#!/bin/bash

# Ultra-simple deployment script (no Docker)
# Just copy files and run with gunicorn

echo "🚀 Simple Deployment - No Docker Required"
echo "========================================"

# Configuration
DEPLOY_DIR="/opt/stock-market-app"
SERVICE_NAME="stock-app"

# Step 1: Create deployment directory
echo "📁 Creating deployment directory..."
sudo mkdir -p $DEPLOY_DIR
sudo chown $USER:$USER $DEPLOY_DIR

# Step 2: Copy files
echo "📋 Copying application files..."
cp -r . $DEPLOY_DIR/
cd $DEPLOY_DIR

# Step 3: Install Python dependencies
echo "🐍 Installing dependencies..."
pip3 install -r requirements.txt --user

# Step 4: Create simple start script
echo "📝 Creating start script..."
cat > start-app.sh << 'EOF'
#!/bin/bash
cd /opt/stock-market-app
export PYTHONPATH=/opt/stock-market-app
gunicorn --bind 0.0.0.0:8080 --daemon --pid app.pid app:app
echo "App started on port 8080"
EOF

chmod +x start-app.sh

# Step 5: Create stop script
cat > stop-app.sh << 'EOF'
#!/bin/bash
cd /opt/stock-market-app
if [ -f app.pid ]; then
    kill $(cat app.pid)
    rm app.pid
    echo "App stopped"
else
    echo "App not running"
fi
EOF

chmod +x stop-app.sh

echo "✅ Deployment complete!"
echo ""
echo "To start: ./start-app.sh"
echo "To stop:  ./stop-app.sh"
echo "App runs on: http://localhost:8080"