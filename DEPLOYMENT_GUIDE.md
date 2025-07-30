# Deployment Guide - Stock Market Data & News Aggregator

This guide provides comprehensive instructions for deploying the Stock Market Data & News Aggregator application in various environments, including local development, Docker containers, and production with load balancing.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment with Load Balancing](#production-deployment-with-load-balancing)
5. [Testing and Verification](#testing-and-verification)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)

## 🔧 Prerequisites

### Required Software
- **Python 3.8+** - For local development
- **Docker** - For containerized deployment
- **Git** - For version control
- **API Keys**:
  - [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)
  - [NewsAPI.org API Key](https://newsapi.org/register)

### System Requirements
- **Minimum RAM**: 2GB
- **Minimum Storage**: 1GB free space
- **Network**: Internet connection for API calls

## 🏠 Local Development Setup

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd Stock-Market-Data-News-Aggregator
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the root directory:
```env
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
NEWS_API_KEY=your_news_api_key_here
PORT=8080
```

### Step 4: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:8080`

### Step 5: Run Tests
```bash
# Run all tests
python test_app.py

# Run specific test file
python simple_test.py
```

## 🐳 Docker Deployment

### Local Docker Build and Run

#### Step 1: Build the Docker Image
```bash
# Build the image
docker build -t stock-market-aggregator:v1 .

# Verify the image was created
docker images | grep stock-market-aggregator
```

#### Step 2: Run the Container
```bash
# Run with environment variables
docker run -d \
  --name stock-app \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  stock-market-aggregator:v1

# Or run with .env file
docker run -d \
  --name stock-app \
  -p 8080:8080 \
  --env-file .env \
  stock-market-aggregator:v1
```

#### Step 3: Verify the Container
```bash
# Check container status
docker ps

# View container logs
docker logs stock-app

# Test the application
curl http://localhost:8080
```

#### Step 4: Stop and Clean Up
```bash
# Stop the container
docker stop stock-app

# Remove the container
docker rm stock-app
```

### Docker Hub Deployment

#### Step 1: Tag for Docker Hub
```bash
# Login to Docker Hub
docker login

# Tag the image with your Docker Hub username
docker tag stock-market-aggregator:v1 <your-dockerhub-username>/stock-market-aggregator:v1
```

#### Step 2: Push to Docker Hub
```bash
# Push the image
docker push <your-dockerhub-username>/stock-market-aggregator:v1

# Verify the push
docker search <your-dockerhub-username>/stock-market-aggregator
```

#### Step 3: Pull and Run from Docker Hub
```bash
# Pull the image
docker pull <your-dockerhub-username>/stock-market-aggregator:v1

# Run the container
docker run -d \
  --name stock-app \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  <your-dockerhub-username>/stock-market-aggregator:v1
```

## 🌐 Production Deployment with Load Balancing

### Lab Environment Setup

This deployment uses the lab infrastructure with three servers:
- **Web01**: Application server 1
- **Web02**: Application server 2  
- **Lb01**: Load balancer (HAProxy)

### Step 1: Deploy on Web01

```bash
# SSH into Web01
ssh web-01

# Pull the Docker image
docker pull <your-dockerhub-username>/stock-market-aggregator:v1

# Run the application container
docker run -d \
  --name stock-app-1 \
  --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  <your-dockerhub-username>/stock-market-aggregator:v1

# Verify the container is running
docker ps

# Test the application
curl http://localhost:8080
```

### Step 2: Deploy on Web02

```bash
# SSH into Web02
ssh web-02

# Pull the Docker image
docker pull <your-dockerhub-username>/stock-market-aggregator:v1

# Run the application container
docker run -d \
  --name stock-app-2 \
  --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  <your-dockerhub-username>/stock-market-aggregator:v1

# Verify the container is running
docker ps

# Test the application
curl http://localhost:8080
```

### Step 3: Configure Load Balancer (Lb01)

```bash
# SSH into Lb01
ssh lb-01

# Edit HAProxy configuration
sudo nano /etc/haproxy/haproxy.cfg
```

Add or update the backend configuration:
```haproxy
backend webapps
    balance roundrobin
    server web01 172.20.0.11:8080 check
    server web02 172.20.0.12:8080 check
```

Reload HAProxy:
```bash
# Reload HAProxy configuration
docker exec -it lb-01 sh -c 'haproxy -sf $(pidof haproxy) -f /etc/haproxy/haproxy.cfg'

# Verify HAProxy is running
docker exec -it lb-01 sh -c 'haproxy -c -f /etc/haproxy/haproxy.cfg'
```

### Step 4: Test Load Balancing

```bash
# Test from your local machine
for i in {1..10}; do
  curl -s http://localhost | grep "Server:" || echo "Request $i completed"
  sleep 1
done

# Test individual servers
curl http://web-01:8080
curl http://web-02:8080
```

## 🧪 Testing and Verification

### Application Testing

#### 1. Basic Functionality Test
```bash
# Test home page
curl http://localhost:8080

# Test API endpoints
curl http://localhost:8080/api/stock/AAPL
curl http://localhost:8080/api/news
```

#### 2. Load Balancing Verification
```bash
# Test multiple requests to verify round-robin
for i in {1..6}; do
  echo "Request $i:"
  curl -s http://localhost | head -n 1
  sleep 1
done
```

#### 3. Health Check Verification
```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check application health
curl -f http://localhost:8080/ || echo "Health check failed"
```

### Performance Testing

#### 1. Load Testing
```bash
# Install Apache Bench (if available)
sudo apt-get install apache2-utils

# Run load test
ab -n 100 -c 10 http://localhost:8080/
```

#### 2. Stress Testing
```bash
# Test with multiple concurrent users
for i in {1..50}; do
  curl -s http://localhost:8080 > /dev/null &
done
wait
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Container Won't Start
```bash
# Check container logs
docker logs <container-name>

# Check if port is already in use
netstat -tulpn | grep 8080

# Remove conflicting container
docker rm -f <container-name>
```

#### 2. API Key Issues
```bash
# Verify environment variables
docker exec <container-name> env | grep API_KEY

# Check application logs for API errors
docker logs <container-name> | grep -i "api\|error"
```

#### 3. Load Balancer Issues
```bash
# Check HAProxy status
docker exec -it lb-01 sh -c 'haproxy -c -f /etc/haproxy/haproxy.cfg'

# Check HAProxy logs
docker logs lb-01

# Verify backend servers
docker exec -it lb-01 sh -c 'haproxy -c -f /etc/haproxy/haproxy.cfg' | grep backend
```

#### 4. Network Connectivity Issues
```bash
# Test connectivity between servers
ping web-01
ping web-02
ping lb-01

# Test port connectivity
telnet web-01 8080
telnet web-02 8080
```

### Debugging Commands

#### Container Debugging
```bash
# Enter container shell
docker exec -it <container-name> /bin/bash

# Check running processes
docker exec <container-name> ps aux

# Check network connectivity
docker exec <container-name> curl -I http://localhost:8080
```

#### Application Debugging
```bash
# View real-time logs
docker logs -f <container-name>

# Check application configuration
docker exec <container-name> env

# Test API endpoints from within container
docker exec <container-name> curl http://localhost:8080/api/stock/AAPL
```

## 🔒 Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use Docker secrets in production
- Rotate API keys regularly

### Network Security
- Use HTTPS in production
- Implement rate limiting
- Configure firewall rules

### Container Security
- Run containers as non-root user
- Keep base images updated
- Scan images for vulnerabilities

### API Security
- Validate all user inputs
- Implement request rate limiting
- Monitor API usage

## 📊 Monitoring and Logging

### Application Monitoring
```bash
# Monitor container resource usage
docker stats

# Monitor application logs
docker logs -f <container-name>

# Check application health
curl -f http://localhost:8080/health
```

### Load Balancer Monitoring
```bash
# Check HAProxy statistics
curl http://lb-01:8080/stats

# Monitor backend health
docker exec -it lb-01 sh -c 'haproxy -c -f /etc/haproxy/haproxy.cfg'
```

## 🔄 Maintenance and Updates

### Updating the Application
```bash
# Pull latest image
docker pull <your-dockerhub-username>/stock-market-aggregator:v1

# Stop old container
docker stop <container-name>

# Remove old container
docker rm <container-name>

# Start new container
docker run -d \
  --name <container-name> \
  --restart unless-stopped \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  <your-dockerhub-username>/stock-market-aggregator:v1
```

### Backup and Recovery
```bash
# Backup container configuration
docker inspect <container-name> > backup.json

# Backup environment variables
docker exec <container-name> env > env_backup.txt

# Restore from backup
docker run -d \
  --name <container-name> \
  --env-file env_backup.txt \
  <image-name>
```

## 📝 Deployment Checklist

### Pre-Deployment
- [ ] API keys obtained and configured
- [ ] Docker images built and tested
- [ ] Environment variables set
- [ ] Network connectivity verified
- [ ] Security configurations applied

### Deployment
- [ ] Containers deployed on Web01 and Web02
- [ ] Load balancer configured
- [ ] Health checks passing
- [ ] Application accessible via load balancer
- [ ] Round-robin load balancing verified

### Post-Deployment
- [ ] Performance testing completed
- [ ] Security testing performed
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team notified of deployment

## 📞 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review container logs: `docker logs <container-name>`
3. Verify network connectivity
4. Check API key configuration
5. Contact the development team

---

**Note**: This deployment guide assumes you have the necessary permissions and access to the lab infrastructure. Adjust commands and configurations according to your specific environment and requirements.
