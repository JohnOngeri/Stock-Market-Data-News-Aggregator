# 🚀 Simple Deployment Guide - Stock Market Data & News Aggregator

## 📋 Quick Overview

This guide provides a **simplified approach** to deploy your Stock Market Aggregator using Docker containers and load balancing.

## 🔧 Prerequisites

- Docker installed locally
- Docker Hub account
- API keys for Alpha Vantage and NewsAPI
- Access to lab servers (web-01, web-02, lb-01)

## 📦 Part 1: Local Setup & Testing

### 1. Get API Keys
```bash
# Get your free API keys:
# Alpha Vantage: https://www.alphavantage.co/support/#api-key
# NewsAPI: https://newsapi.org/register
```

### 2. Configure Environment
```bash
# Create .env file with your API keys
ALPHA_VANTAGE_API_KEY=your_actual_key_here
NEWS_API_KEY=your_actual_key_here
PORT=8080
```

### 3. Test Locally (Without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Test at http://localhost:8080
```

## 🐳 Part 2A: Docker Deployment (Simplified)

### Step 1: Build & Test Docker Image

```bash
# Replace 'yourusername' with your Docker Hub username
docker build -t yourusername/stock-market-aggregator:v1 .

# Test locally with Docker
docker run -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  yourusername/stock-market-aggregator:v1

# Verify: curl http://localhost:8080
```

### Step 2: Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push image
docker push yourusername/stock-market-aggregator:v1
```

### Step 3: Deploy on Lab Servers

**On web-01:**
```bash
ssh web-01
docker pull yourusername/stock-market-aggregator:v1
docker run -d --name app --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  yourusername/stock-market-aggregator:v1
```

**On web-02:**
```bash
ssh web-02
docker pull yourusername/stock-market-aggregator:v1
docker run -d --name app --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  yourusername/stock-market-aggregator:v1
```

### Step 4: Configure Load Balancer

**On lb-01:**
```bash
# Update HAProxy config
sudo nano /etc/haproxy/haproxy.cfg

# Add this backend section:
backend webapps
    balance roundrobin
    option httpchk GET /
    server web01 172.20.0.11:8080 check
    server web02 172.20.0.12:8080 check

# Reload HAProxy
sudo systemctl reload haproxy
# OR if using Docker:
docker exec -it lb-01 sh -c 'haproxy -sf $(pidof haproxy) -f /etc/haproxy/haproxy.cfg'
```

### Step 5: Test Load Balancing

```bash
# Test multiple requests to see round-robin
for i in {1..6}; do
  curl http://your-lb-ip
  echo "Request $i completed"
  sleep 1
done
```

## 🎯 Alternative: Even Simpler Approach

If Docker seems complex, here's a **non-Docker approach**:

### Deploy Directly on Servers

**On web-01 and web-02:**
```bash
# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip
git clone your-repo-url
cd Stock-Market-Data-News-Aggregator
pip3 install -r requirements.txt

# Create .env file with API keys
echo "ALPHA_VANTAGE_API_KEY=your_key" > .env
echo "NEWS_API_KEY=your_key" >> .env

# Run with gunicorn
gunicorn --bind 0.0.0.0:8080 app:app &
```

**Configure load balancer the same way as above.**

## 📊 Testing & Verification

### 1. Individual Server Test
```bash
curl http://172.20.0.11:8080  # web-01
curl http://172.20.0.12:8080  # web-02
```

### 2. Load Balancer Test
```bash
curl http://your-lb-ip
```

### 3. Functionality Test
```bash
# Test stock data endpoint
curl -X POST http://your-lb-ip/get_stock_data \
  -H "Content-Type: application/json" \
  -d '{"symbols": "AAPL,MSFT"}'
```

## 🔒 Security Best Practices

1. **Never commit API keys** to your repository
2. **Use environment variables** for sensitive data
3. **Use .gitignore** to exclude .env files
4. **Rotate API keys** regularly

## 📝 What to Include in Your README

```markdown
## Docker Hub Information
- **Repository**: https://hub.docker.com/r/yourusername/stock-market-aggregator
- **Image**: yourusername/stock-market-aggregator:v1
- **Build Command**: docker build -t yourusername/stock-market-aggregator:v1 .

## Deployment Commands
- **Web01/Web02**: docker run -d --name app --restart unless-stopped -p 8080:8080 -e ALPHA_VANTAGE_API_KEY=key -e NEWS_API_KEY=key yourusername/stock-market-aggregator:v1
- **Load Balancer**: Updated haproxy.cfg with backend servers

## Testing Evidence
- Screenshots of load balancer distributing requests
- Curl commands showing round-robin behavior
- Application functionality tests
```

## 🎬 Demo Video Checklist

Your 2-minute video should show:
1. **Local application** running (30 seconds)
2. **Docker build and run** (30 seconds)
3. **Load balancer** distributing requests (45 seconds)
4. **Key features** - stock data and news (15 seconds)

## 🚨 Common Issues & Solutions

### Issue: API Rate Limits
**Solution**: The app handles this gracefully with error messages

### Issue: Docker Build Fails
**Solution**: Check Dockerfile and ensure all files are present

### Issue: Load Balancer Not Working
**Solution**: Verify server IPs and ports in haproxy.cfg

### Issue: Environment Variables Not Working
**Solution**: Use -e flag with docker run or --env-file

## ✅ Final Checklist

- [ ] Application runs locally
- [ ] Docker image builds successfully
- [ ] Image pushed to Docker Hub
- [ ] Deployed on web-01 and web-02
- [ ] Load balancer configured
- [ ] Round-robin testing completed
- [ ] README updated with all details
- [ ] Demo video recorded
- [ ] API keys secured (not in repo)

This simplified approach removes complexity while meeting all assignment requirements!