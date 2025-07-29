# Part Two A: Docker Containers + Docker Hub + Three-Lab-Container Setup

## Overview

This guide provides complete containerization and deployment instructions for a three-lab-container setup:

- **Web01**: Application server container
- **Web02**: Application server container (redundancy)
- **Lb01**: HAProxy load balancer container

## 1. Containerization with Dockerfile

### Current Dockerfile Analysis

The application uses a production-ready Dockerfile with:

- **Configurable Port**: Exposed on port 8080 (configurable via PORT environment variable)
- **Security**: Non-root user execution
- **Performance**: Gunicorn WSGI server with 4 workers
- **Health Checks**: Built-in container health monitoring

```dockerfile
# Key configurations in existing Dockerfile:
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

### Port Configuration

The application port is configurable through environment variables:

- Default: 8080
- Override: Set `PORT` environment variable

## 2. Local Build and Test Steps

### Step 1: Build the Docker Image

```bash
# Build with semantic tag
docker build -t stock-market-aggregator:v1 .
docker build -t stock-market-aggregator:latest .

# Verify image creation
docker images | grep stock-market-aggregator
```

### Step 2: Local Testing

```bash
# Create test environment file
echo "ALPHA_VANTAGE_API_KEY=your_alpha_key" > .env.test
echo "NEWS_API_KEY=your_news_key" >> .env.test

# Run container locally
docker run -d \
  --name test-app \
  -p 8080:8080 \
  --env-file .env.test \
  stock-market-aggregator:latest

# Verify container is running
docker ps | grep test-app
```

### Step 3: Verification with curl

```bash
# Test main endpoint
curl -f http://localhost:8080/
# Expected: HTML response with application interface

# Test API endpoints
curl -f http://localhost:8080/api/stock/AAPL
# Expected: JSON with stock data

curl -f http://localhost:8080/api/news
# Expected: JSON with news articles

# Test health endpoint (if container has health check)
docker inspect test-app | grep -A 5 "Health"

# Clean up test container
docker stop test-app && docker rm test-app
```

## 3. Docker Hub Publishing Process

### Step 1: Docker Hub Login

```bash
# Login to Docker Hub
docker login
# Enter your Docker Hub username and password
```

### Step 2: Tag Images with Semantic Versioning

```bash
# Replace 'yourusername' with your Docker Hub username
DOCKER_HUB_USERNAME="yourusername"

# Tag with semantic versions
docker tag stock-market-aggregator:latest $DOCKER_HUB_USERNAME/stock-market-aggregator:latest
docker tag stock-market-aggregator:v1 $DOCKER_HUB_USERNAME/stock-market-aggregator:v1
docker tag stock-market-aggregator:v1 $DOCKER_HUB_USERNAME/stock-market-aggregator:v1.0.0
```

### Step 3: Push to Docker Hub

```bash
# Push all tags
docker push $DOCKER_HUB_USERNAME/stock-market-aggregator:latest
docker push $DOCKER_HUB_USERNAME/stock-market-aggregator:v1
docker push $DOCKER_HUB_USERNAME/stock-market-aggregator:v1.0.0

# Verify push success
docker search $DOCKER_HUB_USERNAME/stock-market-aggregator
```

## 4. Three-Lab-Container Setup Deployment

### Prerequisites

- 3 lab machines: Web01, Web02, Lb01
- Docker installed on all machines
- Network connectivity between machines
- API keys for Alpha Vantage and NewsAPI

### Step 1: Deploy on Web01 Server

```bash
# SSH to Web01 machine
ssh user@web01

# Pull the image
docker pull $DOCKER_HUB_USERNAME/stock-market-aggregator:latest

# Create environment file
cat > .env << EOF
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
PORT=8080
FLASK_ENV=production
EOF

# Run container with specific configuration
docker run -d \
  --name stock-app-web01 \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  --memory=512m \
  --memory-reservation=256m \
  --health-cmd="curl -f http://localhost:8080/ || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  $DOCKER_HUB_USERNAME/stock-market-aggregator:latest

# Verify deployment
docker ps | grep stock-app-web01
curl -f http://localhost:8080/
```

### Step 2: Deploy on Web02 Server

```bash
# SSH to Web02 machine
ssh user@web02

# Pull the image
docker pull $DOCKER_HUB_USERNAME/stock-market-aggregator:latest

# Create environment file (same as Web01)
cat > .env << EOF
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
PORT=8080
FLASK_ENV=production
EOF

# Run container (identical to Web01)
docker run -d \
  --name stock-app-web02 \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  --memory=512m \
  --memory-reservation=256m \
  --health-cmd="curl -f http://localhost:8080/ || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  $DOCKER_HUB_USERNAME/stock-market-aggregator:latest

# Verify deployment
docker ps | grep stock-app-web02
curl -f http://localhost:8080/
```

### Step 3: Configure HAProxy Load Balancer (Lb01)

#### HAProxy Configuration File

```bash
# SSH to Lb01 machine
ssh user@lb01

# Create HAProxy configuration
sudo mkdir -p /etc/haproxy
sudo tee /etc/haproxy/haproxy.cfg > /dev/null << 'EOF'
global
    daemon
    maxconn 4096
    log stdout local0 info

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog
    option dontlognull
    option redispatch
    retries 3

frontend stock_app_frontend
    bind *:80
    default_backend stock_app_servers
    
    # Health check endpoint
    acl health_check path_beg /health
    use_backend health_backend if health_check

backend stock_app_servers
    balance roundrobin
    option httpchk GET /
    http-check expect status 200
    
    # Replace with actual IP addresses of Web01 and Web02
    server web01 <WEB01_IP>:8080 check inter 30s fall 3 rise 2
    server web02 <WEB02_IP>:8080 check inter 30s fall 3 rise 2

backend health_backend
    http-request return status 200 content-type text/plain string "HAProxy Health OK"

listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE
EOF
```

#### Deploy HAProxy Container

```bash
# Run HAProxy container
docker run -d \
  --name haproxy-lb01 \
  --restart unless-stopped \
  -p 80:80 \
  -p 8404:8404 \
  -v /etc/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  haproxy:2.8-alpine

# Verify HAProxy is running
docker ps | grep haproxy-lb01
docker logs haproxy-lb01
```

#### HAProxy Reload Command

```bash
# Reload HAProxy configuration without downtime
docker exec haproxy-lb01 haproxy -f /usr/local/etc/haproxy/haproxy.cfg -c
docker kill -s HUP haproxy-lb01

# Alternative: Restart container (brief downtime)
docker restart haproxy-lb01
```

## 5. End-to-End Testing and Verification

### Step 1: Basic Connectivity Tests

```bash
# From host machine, test individual servers
curl -f http://<WEB01_IP>:8080/
curl -f http://<WEB02_IP>:8080/

# Test load balancer
curl -f http://<LB01_IP>/
```

### Step 2: Load Balancing Verification

```bash
# Test traffic distribution (run from host machine)
echo "Testing load balancing distribution..."
for i in {1..20}; do
    response=$(curl -s http://<LB01_IP>/ | grep -o "Server: [^<]*" || echo "Response $i")
    echo "Request $i: $response"
    sleep 1
done

# Test with API endpoints
echo "Testing API load balancing..."
for i in {1..10}; do
    curl -s http://<LB01_IP>/api/stock/AAPL | jq '.symbol' || echo "API test $i failed"
    sleep 2
done
```

### Step 3: Failover Testing

```bash
# Stop Web01 and verify Web02 handles all traffic
ssh user@web01 "docker stop stock-app-web01"

echo "Testing failover to Web02..."
for i in {1..10}; do
    curl -f http://<LB01_IP>/ && echo "Request $i: SUCCESS" || echo "Request $i: FAILED"
    sleep 1
done

# Restart Web01
ssh user@web01 "docker start stock-app-web01"

# Wait for health check and test distribution resumes
sleep 60
echo "Testing restored load balancing..."
for i in {1..10}; do
    curl -s http://<LB01_IP>/ | grep -o "Server: [^<]*" || echo "Test $i"
    sleep 1
done
```

### Step 4: HAProxy Statistics Monitoring

```bash
# Access HAProxy stats page
curl http://<LB01_IP>:8404/stats

# Or open in browser: http://<LB01_IP>:8404/stats
```

## 6. Evidence Collection

### Required Screenshots/Logs

1. **Docker Build Output**:

   ```bash
   docker build -t stock-market-aggregator:v1 . 2>&1 | tee build.log
   ```

2. **Docker Hub Push Confirmation**:

   ```bash
   docker push $DOCKER_HUB_USERNAME/stock-market-aggregator:latest 2>&1 | tee push.log
   ```

3. **Container Status on All Servers**:

   ```bash
   # On each server
   docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" > container_status.log
   ```

4. **HAProxy Stats Page**: Screenshot of http://<LB01_IP>:8404/stats

5. **Load Balancing Evidence**:

   ```bash
   # Capture load balancing logs
   for i in {1..50}; do
       echo "$(date): $(curl -s http://<LB01_IP>/ | grep -o 'Server: [^<]*')"
   done > load_balance_test.log
   ```

6. **Failover Test Results**:

   ```bash
   # Document failover behavior
   echo "Failover test started: $(date)" > failover_test.log
   # Stop one server and test
   # Document results
   ```

## 7. Security Considerations

### Environment Variables Protection

```bash
# Secure .env file permissions
chmod 600 .env
chown root:root .env

# Use Docker secrets in production
echo "your_api_key" | docker secret create alpha_vantage_key -
echo "your_news_key" | docker secret create news_api_key -
```

### Network Security

```bash
# Create custom Docker network for container communication
docker network create --driver bridge stock-app-network

# Run containers with custom network
docker run -d --network stock-app-network --name stock-app-web01 ...
```

## 8. Monitoring and Maintenance

### Health Monitoring

```bash
# Check container health status
docker inspect stock-app-web01 | jq '.[0].State.Health'

# Monitor HAProxy backend status
curl -s http://<LB01_IP>:8404/stats | grep -E "(web01|web02)"
```

### Log Management

```bash
# Centralized logging
docker logs --follow stock-app-web01 > /var/log/stock-app-web01.log &
docker logs --follow stock-app-web02 > /var/log/stock-app-web02.log &
docker logs --follow haproxy-lb01 > /var/log/haproxy-lb01.log &
```

This deployment guide provides complete instructions for containerizing, publishing, and deploying the Stock Market Data & News Aggregator in a three-lab-container setup with HAProxy load balancing and comprehensive testing procedures.
