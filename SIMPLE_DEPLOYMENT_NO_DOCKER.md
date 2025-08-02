# 🚀 Simple Deployment Guide (No Docker Required)

## 📋 Overview

This guide shows how to deploy your Stock Market Aggregator **without Docker** using simple Linux services and nginx load balancing.

## 🔧 Prerequisites

- Linux servers (Ubuntu/Debian recommended)
- Python 3.8+
- API keys (Alpha Vantage + NewsAPI)
- SSH access to servers

## 📝 Part 1: Local Development

### 1. Setup Environment
```bash
# Install dependencies
pip3 install -r requirements.txt

# Create .env file
echo "ALPHA_VANTAGE_API_KEY=your_key" > .env
echo "NEWS_API_KEY=your_key" >> .env

# Run locally
python3 app.py
```

## 🖥️ Part 2: Server Deployment

### Method 1: Ultra Simple (Recommended)

**On web-01 and web-02:**

```bash
# 1. Copy your project files
scp -r Stock-Market-Data-News-Aggregator/ user@server:/home/user/

# 2. SSH to server
ssh user@server

# 3. Run deployment script
cd Stock-Market-Data-News-Aggregator
chmod +x simple-deploy.sh
./simple-deploy.sh

# 4. Start the application
./start-app.sh
```

**That's it!** Your app is running on port 8080.

### Method 2: Systemd Service (More Robust)

**On web-01 and web-02:**

```bash
# 1. Copy files and run systemd deployment
chmod +x systemd-deploy.sh
sudo ./systemd-deploy.sh

# 2. Check service status
sudo systemctl status stock-market-app
```

## ⚖️ Part 3: Load Balancer Setup

**On lb-01 server:**

```bash
# 1. Copy load balancer script
scp load-balancer-setup.sh user@lb-01:/home/user/

# 2. SSH and run setup
ssh user@lb-01
chmod +x load-balancer-setup.sh
sudo ./load-balancer-setup.sh
```

## 🧪 Testing Your Deployment

### Test Individual Servers
```bash
curl http://172.20.0.11:8080  # web-01
curl http://172.20.0.12:8080  # web-02
```

### Test Load Balancer
```bash
# Test multiple requests to see round-robin
for i in {1..6}; do
  curl http://your-lb-ip
  echo "Request $i completed"
  sleep 1
done
```

### Test API Functionality
```bash
# Test stock data
curl -X POST http://your-lb-ip/get_stock_data \
  -H "Content-Type: application/json" \
  -d '{"symbols": "AAPL,MSFT"}'
```

## 🔧 Management Commands

### Start/Stop Application (Method 1)
```bash
./start-app.sh   # Start
./stop-app.sh    # Stop
```

### Start/Stop Application (Method 2)
```bash
sudo systemctl start stock-market-app    # Start
sudo systemctl stop stock-market-app     # Stop
sudo systemctl status stock-market-app   # Status
sudo journalctl -u stock-market-app -f   # View logs
```

### Load Balancer Management
```bash
sudo systemctl status nginx      # Check status
sudo systemctl reload nginx      # Reload config
sudo nginx -t                    # Test config
```

## 📊 Architecture Overview

```
Internet → Load Balancer (nginx) → Web Servers (gunicorn)
             (lb-01:80)              (web-01:8080, web-02:8080)
```

## 🔒 Security & Best Practices

### Environment Variables
```bash
# Create .env file on each server
ALPHA_VANTAGE_API_KEY=your_actual_key
NEWS_API_KEY=your_actual_key
PORT=8080
```

### Firewall Setup
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP (load balancer)
sudo ufw allow 8080  # App (internal only)
sudo ufw enable
```

## 🚨 Troubleshooting

### App Not Starting
```bash
# Check Python dependencies
pip3 list | grep -E "(flask|requests|gunicorn)"

# Check .env file
cat .env

# Check port availability
netstat -tlnp | grep 8080
```

### Load Balancer Issues
```bash
# Check nginx status
sudo systemctl status nginx

# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Test backend servers
curl http://172.20.0.11:8080
curl http://172.20.0.12:8080
```

### API Issues
```bash
# Test API keys
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY"
```

## 📋 Assignment Requirements Met

✅ **No Docker**: Simple Linux services instead  
✅ **Load Balancing**: Nginx round-robin  
✅ **Multi-Server**: Deployed on web-01 and web-02  
✅ **Easy Management**: Start/stop scripts  
✅ **Production Ready**: Systemd services with auto-restart  

## 🎯 Quick Commands Summary

### Deployment
```bash
# On web servers
./simple-deploy.sh && ./start-app.sh

# On load balancer
sudo ./load-balancer-setup.sh
```

### Testing
```bash
# Test everything
curl http://your-lb-ip
for i in {1..6}; do curl http://your-lb-ip; echo; done
```

### Management
```bash
# Check status
./stop-app.sh && ./start-app.sh  # Restart app
sudo systemctl reload nginx      # Reload load balancer
```

This approach is **much simpler than Docker** while still meeting all assignment requirements!