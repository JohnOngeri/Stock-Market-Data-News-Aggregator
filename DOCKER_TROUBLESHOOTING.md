# Docker Troubleshooting Guide

This guide will help you resolve common Docker issues with the Stock Market Data & News Aggregator application.

## 🔍 Quick Diagnosis

### Step 1: Check Docker Installation

```bash
# Check if Docker is installed and running
docker --version
docker info

# If Docker is not installed, install it:
# Windows: Download from https://www.docker.com/products/docker-desktop
# macOS: Download from https://www.docker.com/products/docker-desktop
# Linux: Follow instructions at https://docs.docker.com/engine/install/
```

### Step 2: Check Docker Service

```bash
# Check if Docker daemon is running
docker ps

# If you get an error, start Docker:
# Windows/macOS: Start Docker Desktop
# Linux: sudo systemctl start docker
```

## 🚨 Common Issues and Solutions

### Issue 1: "Docker command not found"

**Solution:**

```bash
# Install Docker
# Windows/macOS: Download Docker Desktop
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Logout and login again
```

### Issue 2: "Permission denied" when running Docker

**Solution:**

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Logout and login again, or run:
newgrp docker

# Or run Docker commands with sudo (not recommended for production)
sudo docker build -t stock-market-aggregator:v1 .
```

### Issue 3: "Port already in use"

**Solution:**

```bash
# Check what's using port 8080
netstat -tulpn | grep 8080
# or
lsof -i :8080

# Kill the process using the port
sudo kill -9 <PID>

# Or use a different port
docker run -p 8081:8080 stock-market-aggregator:v1
```

### Issue 4: "Build failed" during Docker build

**Solution:**

```bash
# Clean Docker cache
docker system prune -a

# Rebuild with no cache
docker build --no-cache -t stock-market-aggregator:v1 .

# Check if all files are present
ls -la
cat requirements.txt
```

### Issue 5: "Container exits immediately"

**Solution:**

```bash
# Check container logs
docker logs <container-name>

# Run container in interactive mode to debug
docker run -it --rm stock-market-aggregator:v1 /bin/bash

# Check if environment variables are set
docker run -it --rm -e ALPHA_VANTAGE_API_KEY=test -e NEWS_API_KEY=test stock-market-aggregator:v1
```

### Issue 6: "API key errors" in container

**Solution:**

```bash
# Create .env file with your API keys
echo "ALPHA_VANTAGE_API_KEY=your_actual_key" > .env
echo "NEWS_API_KEY=your_actual_key" >> .env

# Run with environment file
docker run -p 8080:8080 --env-file .env stock-market-aggregator:v1

# Or pass environment variables directly
docker run -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  stock-market-aggregator:v1
```

## 🔧 Step-by-Step Docker Setup

### Step 1: Prepare Your Environment

```bash
# Navigate to project directory
cd Stock-Market-Data-News-Aggregator

# Create .env file with your API keys
cat > .env << EOF
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
EOF
```

### Step 2: Build the Docker Image

```bash
# Build the image
docker build -t stock-market-aggregator:v1 .

# Verify the image was created
docker images | grep stock-market-aggregator
```

### Step 3: Test the Container

```bash
# Run the container
docker run -d --name stock-app \
  -p 8080:8080 \
  --env-file .env \
  stock-market-aggregator:v1

# Check if container is running
docker ps

# Check container logs
docker logs stock-app

# Test the application
curl http://localhost:8080
```

### Step 4: Troubleshoot if Issues Occur

```bash
# If container is not running, check logs
docker logs stock-app

# If you need to restart
docker stop stock-app
docker rm stock-app
docker run -d --name stock-app -p 8080:8080 --env-file .env stock-market-aggregator:v1
```

## 🐛 Debugging Commands

### Check Container Status

```bash
# List all containers
docker ps -a

# Check container logs
docker logs <container-name>

# Enter running container
docker exec -it <container-name> /bin/bash

# Check container resources
docker stats <container-name>
```

### Check Image Details

```bash
# List all images
docker images

# Inspect image
docker inspect stock-market-aggregator:v1

# Check image history
docker history stock-market-aggregator:v1
```

### Network Issues

```bash
# Check Docker networks
docker network ls

# Inspect network
docker network inspect bridge

# Test connectivity from container
docker exec <container-name> curl -I http://localhost:8080
```

## 🔄 Alternative Docker Approaches

### Option 1: Use Docker Compose

```bash
# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  stock-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ALPHA_VANTAGE_API_KEY=\${ALPHA_VANTAGE_API_KEY}
      - NEWS_API_KEY=\${NEWS_API_KEY}
    env_file:
      - .env
    restart: unless-stopped
EOF

# Run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 2: Development Mode

```bash
# Create a development Dockerfile
cat > Dockerfile.dev << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
EOF

# Build and run development version
docker build -f Dockerfile.dev -t stock-market-dev .
docker run -p 8080:8080 --env-file .env stock-market-dev
```

### Option 3: Simple Python Container

```bash
# Run with minimal setup
docker run -it --rm \
  -p 8080:8080 \
  -v $(pwd):/app \
  -w /app \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  -e NEWS_API_KEY=your_key \
  python:3.11-slim \
  bash -c "pip install -r requirements.txt && python app.py"
```

## 🧪 Testing Docker Setup

### Test Script

```bash
# Create a test script
cat > test_docker.sh << 'EOF'
#!/bin/bash

echo "Testing Docker setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

echo "✅ Docker is running"

# Build image
echo "Building Docker image..."
if docker build -t stock-market-aggregator:v1 .; then
    echo "✅ Image built successfully"
else
    echo "❌ Image build failed"
    exit 1
fi

# Run container
echo "Running container..."
docker run -d --name test-stock-app \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY=test \
  -e NEWS_API_KEY=test \
  stock-market-aggregator:v1

# Wait for container to start
sleep 5

# Test application
if curl -f http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Application is accessible"
else
    echo "❌ Application is not accessible"
    docker logs test-stock-app
fi

# Cleanup
docker stop test-stock-app
docker rm test-stock-app

echo "Test completed!"
EOF

# Make executable and run
chmod +x test_docker.sh
./test_docker.sh
```

## 🆘 Emergency Solutions

### If Nothing Works: Local Python Setup

```bash
# Fallback to local Python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

### If Docker Desktop Won't Start

1. **Windows**: Restart Docker Desktop, check Windows Subsystem for Linux
2. **macOS**: Restart Docker Desktop, check system resources
3. **Linux**: Restart Docker service: `sudo systemctl restart docker`

### If Build Fails Completely

```bash
# Use a simpler Dockerfile
cat > Dockerfile.simple << EOF
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
EOF

docker build -f Dockerfile.simple -t stock-market-simple .
docker run -p 8080:8080 --env-file .env stock-market-simple
```

## 📞 Getting Help

### Check System Requirements

- **Windows**: Windows 10/11 with WSL2
- **macOS**: macOS 10.15 or later
- **Linux**: Ubuntu 18.04+ or equivalent

### Common Error Messages

- `"Cannot connect to the Docker daemon"`: Docker service not running
- `"Port already in use"`: Another service using port 8080
- `"Build failed"`: Missing files or network issues
- `"Container exits"`: Environment variables or application errors

### Next Steps

1. Try the step-by-step setup above
2. Run the test script to diagnose issues
3. Check container logs for specific errors
4. Use the alternative approaches if needed
5. Fall back to local Python setup as last resort

---

**Need more help?** Check the container logs with `docker logs <container-name>` and share the error messages for specific assistance.
