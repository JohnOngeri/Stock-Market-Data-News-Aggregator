# Docker Deployment Guide - Part Two A

This guide provides detailed instructions for deploying the Stock Market Data & News Aggregator application using Docker containers and Docker Hub, following the assignment requirements.

## Prerequisites

- Docker installed on your local machine
- Docker Hub account
- Access to the lab machines (Web01, Web02, Lb01)
- API keys for Alpha Vantage and NewsAPI.org

## Docker Hub Image Details

- **Repository**: `your-dockerhub-username/stock-market-aggregator`
- **Tags**: `v1`, `latest`
- **Image URL**: `https://hub.docker.com/r/your-dockerhub-username/stock-market-aggregator`

## Step 1: Build and Test Locally

### 1.1 Build the Docker Image

```bash
# Build the image with your Docker Hub username
docker build -t your-dockerhub-username/stock-market-aggregator:v1 .
```

### 1.2 Test the Image Locally

```bash
# Run the container locally with environment variables
docker run -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key" \
  -e NEWS_API_KEY="your_news_api_key" \
  your-dockerhub-username/stock-market-aggregator:v1
```

### 1.3 Verify Local Functionality

```bash
# Test the application
curl http://localhost:8080

# Test API endpoints
curl http://localhost:8080/api/stock/AAPL
curl http://localhost:8080/api/news
```

## Step 2: Push to Docker Hub

### 2.1 Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

### 2.2 Push the Image

```bash
# Push the v1 tag
docker push your-dockerhub-username/stock-market-aggregator:v1

# Tag as latest and push
docker tag your-dockerhub-username/stock-market-aggregator:v1 your-dockerhub-username/stock-market-aggregator:latest
docker push your-dockerhub-username/stock-market-aggregator:latest
```

### 2.3 Verify on Docker Hub

Visit `https://hub.docker.com/r/your-dockerhub-username/stock-market-aggregator` to confirm the image is available.

## Step 3: Deploy on Lab Machines

### 3.1 Deploy on Web01

```bash
# SSH into Web01
ssh user@web-01-ip

# Pull the image
docker pull your-dockerhub-username/stock-market-aggregator:v1

# Run the container
docker run -d --name app --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key" \
  -e NEWS_API_KEY="your_news_api_key" \
  your-dockerhub-username/stock-market-aggregator:v1

# Verify the container is running
docker ps

# Test the application
curl http://localhost:8080
```

### 3.2 Deploy on Web02

```bash
# SSH into Web02
ssh user@web-02-ip

# Pull the image
docker pull your-dockerhub-username/stock-market-aggregator:v1

# Run the container
docker run -d --name app --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key" \
  -e NEWS_API_KEY="your_news_api_key" \
  your-dockerhub-username/stock-market-aggregator:v1

# Verify the container is running
docker ps

# Test the application
curl http://localhost:8080
```

### 3.3 Verify Internal Connectivity

```bash
# From Web01, test Web02
curl http://web-02:8080

# From Web02, test Web01
curl http://web-01:8080
```

## Step 4: Configure Load Balancer (Lb01)

### 4.1 SSH into Lb01

```bash
ssh user@lb-01-ip
```

### 4.2 Update HAProxy Configuration

Edit the HAProxy configuration file:

```bash
# Edit the HAProxy config file
nano /etc/haproxy/haproxy.cfg
```

Add or update the backend section:

```haproxy
# Global settings
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:80
    default_backend webapps

backend webapps
    balance roundrobin
    server web01 172.20.0.11:8080 check
    server web02 172.20.0.12:8080 check
    option httpchk GET /
    http-check expect status 200
```

### 4.3 Reload HAProxy

```bash
# Reload HAProxy configuration
docker exec -it lb-01 sh -c 'haproxy -sf $(pidof haproxy) -f /etc/haproxy/haproxy.cfg'

# Or restart the HAProxy container
docker restart lb-01
```

### 4.4 Verify HAProxy Configuration

```bash
# Check HAProxy status
docker exec -it lb-01 haproxy -c -f /etc/haproxy/haproxy.cfg

# Check HAProxy stats (if available)
curl http://lb-01:8080/stats
```

## Step 5: Testing Load Balancing

### 5.1 Test End-to-End from Host

```bash
# Test multiple times to see round-robin in action
curl http://localhost
curl http://localhost
curl http://localhost
curl http://localhost
```

### 5.2 Verify Round-Robin Distribution

You should see responses alternating between Web01 and Web02. To verify this:

```bash
# Add a simple identifier to responses
# In your app.py, add a response header or modify the response to include server info
```

### 5.3 Monitor Load Balancer

```bash
# Check HAProxy logs
docker logs lb-01

# Check application logs
docker logs <web01-container-name>
docker logs <web02-container-name>
```

## Step 6: Security and Hardening

### 6.1 Environment Variables

Instead of hardcoding API keys, use environment variables:

```bash
# Create a .env file on each server
cat > .env << EOF
ALPHA_VANTAGE_API_KEY=your_actual_key
NEWS_API_KEY=your_actual_key
EOF

# Use the .env file
docker run -d --name app --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  your-dockerhub-username/stock-market-aggregator:v1
```

### 6.2 Docker Secrets (Optional)

For production environments, consider using Docker secrets:

```bash
# Create secrets
echo "your_alpha_vantage_key" | docker secret create alpha_vantage_key -
echo "your_news_api_key" | docker secret create news_api_key -

# Use secrets in docker-compose
version: '3.8'
services:
  app:
    image: your-dockerhub-username/stock-market-aggregator:v1
    secrets:
      - alpha_vantage_key
      - news_api_key
    environment:
      - ALPHA_VANTAGE_API_KEY_FILE=/run/secrets/alpha_vantage_key
      - NEWS_API_KEY_FILE=/run/secrets/news_api_key
```

## Step 7: Monitoring and Troubleshooting

### 7.1 Health Checks

The application includes health checks:

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check specific container health
docker inspect <container-name> | grep -A 10 "Health"
```

### 7.2 Logs

```bash
# View application logs
docker logs <container-name>

# Follow logs in real-time
docker logs -f <container-name>

# View HAProxy logs
docker logs lb-01
```

### 7.3 Common Issues and Solutions

#### Issue: Container won't start

```bash
# Check container logs
docker logs <container-name>

# Verify environment variables
docker exec <container-name> env | grep API
```

#### Issue: Load balancer not distributing traffic

```bash
# Check HAProxy configuration
docker exec -it lb-01 haproxy -c -f /etc/haproxy/haproxy.cfg

# Check backend servers
docker exec -it lb-01 haproxy -c -f /etc/haproxy/haproxy.cfg | grep -A 5 "backend"
```

#### Issue: API rate limiting

- Implement caching in the application
- Use multiple API keys
- Add retry logic with exponential backoff

## Step 8: Performance Optimization

### 8.1 Container Optimization

```bash
# Use resource limits
docker run -d --name app --restart unless-stopped \
  -p 8080:8080 \
  --memory="512m" \
  --cpus="0.5" \
  -e ALPHA_VANTAGE_API_KEY="your_key" \
  -e NEWS_API_KEY="your_key" \
  your-dockerhub-username/stock-market-aggregator:v1
```

### 8.2 Load Balancer Optimization

```haproxy
backend webapps
    balance roundrobin
    server web01 172.20.0.11:8080 check maxconn 100
    server web02 172.20.0.12:8080 check maxconn 100
    option httpchk GET /
    http-check expect status 200
    timeout connect 5s
    timeout server 30s
```

## Verification Checklist

- [ ] Docker image builds successfully
- [ ] Image pushed to Docker Hub
- [ ] Containers running on Web01 and Web02
- [ ] Applications accessible on both servers
- [ ] HAProxy configuration updated
- [ ] Load balancer distributing traffic
- [ ] Round-robin working correctly
- [ ] Health checks passing
- [ ] Logs showing successful requests
- [ ] Security measures implemented

## Demo Video Requirements

Record a 2-minute demo video showing:

1. **Local Application (30 seconds)**
   - Starting the application locally
   - Entering stock symbols (AAPL, MSFT, GOOGL)
   - Demonstrating sorting and filtering features
   - Showing news aggregation

2. **Load Balancer Testing (30 seconds)**
   - Accessing the application through the load balancer
   - Making multiple requests to show round-robin
   - Demonstrating that requests alternate between servers

3. **Key Features (60 seconds)**
   - Real-time stock data display
   - News search and filtering
   - Error handling for invalid symbols
   - Responsive design on different screen sizes

The video should demonstrate the application's practical value for investors and financial enthusiasts.
