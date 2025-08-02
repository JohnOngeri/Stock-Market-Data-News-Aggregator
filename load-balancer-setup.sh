#!/bin/bash

# Simple load balancer setup using nginx
# No Docker required

echo "⚖️ Setting up Load Balancer with Nginx"
echo "====================================="

# Step 1: Install nginx
echo "📦 Installing nginx..."
sudo apt update
sudo apt install -y nginx

# Step 2: Create load balancer config
echo "⚙️ Creating load balancer configuration..."
sudo tee /etc/nginx/sites-available/stock-app-lb > /dev/null <<'EOF'
upstream stock_app_backend {
    server 172.20.0.11:8080;
    server 172.20.0.12:8080;
}

server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://stock_app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health check
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Step 3: Enable the site
echo "🔗 Enabling load balancer site..."
sudo ln -sf /etc/nginx/sites-available/stock-app-lb /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Step 4: Test and reload nginx
echo "🧪 Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Configuration valid, reloading nginx..."
    sudo systemctl reload nginx
    sudo systemctl enable nginx
    echo "🎉 Load balancer setup complete!"
    echo "Access your app at: http://your-server-ip"
else
    echo "❌ Nginx configuration error"
    exit 1
fi