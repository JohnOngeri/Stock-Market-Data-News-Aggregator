#!/bin/bash

# Docker Test Script for Stock Market Data & News Aggregator
# This script will help diagnose and fix Docker issues

set -e  # Exit on any error

echo "🐳 Docker Troubleshooting Script"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [ "$status" = "ERROR" ]; then
        echo -e "${RED}❌ $message${NC}"
    else
        echo -e "${BLUE}ℹ️  $message${NC}"
    fi
}

# Step 1: Check if Docker is installed
echo "Step 1: Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_status "OK" "Docker is installed: $DOCKER_VERSION"
else
    print_status "ERROR" "Docker is not installed"
    echo ""
    echo "To install Docker:"
    echo "  Windows/macOS: Download Docker Desktop from https://www.docker.com/products/docker-desktop"
    echo "  Linux: sudo apt-get install docker.io docker-compose"
    exit 1
fi

# Step 2: Check if Docker daemon is running
echo ""
echo "Step 2: Checking Docker daemon..."
if docker info &> /dev/null; then
    print_status "OK" "Docker daemon is running"
else
    print_status "ERROR" "Docker daemon is not running"
    echo ""
    echo "To start Docker:"
    echo "  Windows/macOS: Start Docker Desktop"
    echo "  Linux: sudo systemctl start docker"
    exit 1
fi

# Step 3: Check if we're in the right directory
echo ""
echo "Step 3: Checking project files..."
if [ -f "Dockerfile" ] && [ -f "app.py" ] && [ -f "requirements.txt" ]; then
    print_status "OK" "All required files found"
else
    print_status "ERROR" "Missing required files (Dockerfile, app.py, requirements.txt)"
    echo "Make sure you're in the Stock-Market-Data-News-Aggregator directory"
    exit 1
fi

# Step 4: Check if .env file exists
echo ""
echo "Step 4: Checking environment configuration..."
if [ -f ".env" ]; then
    print_status "OK" ".env file found"
    # Check if API keys are set
    if grep -q "ALPHA_VANTAGE_API_KEY" .env && grep -q "NEWS_API_KEY" .env; then
        print_status "OK" "API keys configured in .env"
    else
        print_status "WARN" "API keys not found in .env file"
        echo "Creating .env file with placeholder values..."
        cat > .env << EOF
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
EOF
        print_status "OK" "Created .env file with placeholder values"
    fi
else
    print_status "WARN" ".env file not found"
    echo "Creating .env file..."
    cat > .env << EOF
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
EOF
    print_status "OK" "Created .env file with placeholder values"
fi

# Step 5: Clean up any existing containers
echo ""
echo "Step 5: Cleaning up existing containers..."
if docker ps -a --format "table {{.Names}}" | grep -q "stock-app"; then
    print_status "WARN" "Found existing stock-app container, removing..."
    docker stop stock-app 2>/dev/null || true
    docker rm stock-app 2>/dev/null || true
    print_status "OK" "Cleaned up existing container"
else
    print_status "OK" "No existing containers found"
fi

# Step 6: Build Docker image
echo ""
echo "Step 6: Building Docker image..."
if docker build -t stock-market-aggregator:v1 .; then
    print_status "OK" "Docker image built successfully"
else
    print_status "ERROR" "Docker build failed"
    echo ""
    echo "Trying to build with no cache..."
    if docker build --no-cache -t stock-market-aggregator:v1 .; then
        print_status "OK" "Docker image built successfully (no cache)"
    else
        print_status "ERROR" "Docker build still failed"
        echo ""
        echo "Common build issues:"
        echo "  1. Check your internet connection"
        echo "  2. Make sure all files are present"
        echo "  3. Try: docker system prune -a"
        exit 1
    fi
fi

# Step 7: Run container
echo ""
echo "Step 7: Running container..."
if docker run -d --name stock-app -p 8080:8080 --env-file .env stock-market-aggregator:v1; then
    print_status "OK" "Container started successfully"
else
    print_status "ERROR" "Failed to start container"
    echo ""
    echo "Checking container logs..."
    docker logs stock-app
    exit 1
fi

# Step 8: Wait for container to be ready
echo ""
echo "Step 8: Waiting for application to start..."
sleep 5

# Step 9: Check if container is running
echo ""
echo "Step 9: Checking container status..."
if docker ps | grep -q "stock-app"; then
    print_status "OK" "Container is running"
else
    print_status "ERROR" "Container is not running"
    echo ""
    echo "Container logs:"
    docker logs stock-app
    exit 1
fi

# Step 10: Test application
echo ""
echo "Step 10: Testing application..."
if curl -f http://localhost:8080 > /dev/null 2>&1; then
    print_status "OK" "Application is accessible at http://localhost:8080"
else
    print_status "WARN" "Application not immediately accessible"
    echo "Waiting a bit more..."
    sleep 10
    if curl -f http://localhost:8080 > /dev/null 2>&1; then
        print_status "OK" "Application is now accessible at http://localhost:8080"
    else
        print_status "ERROR" "Application is not accessible"
        echo ""
        echo "Container logs:"
        docker logs stock-app
        echo ""
        echo "Trying to access with curl -v:"
        curl -v http://localhost:8080 || true
    fi
fi

# Step 11: Show container info
echo ""
echo "Step 11: Container information..."
echo "Container ID: $(docker ps -q --filter name=stock-app)"
echo "Container logs: docker logs stock-app"
echo "Stop container: docker stop stock-app"
echo "Remove container: docker rm stock-app"
echo "Access application: http://localhost:8080"

# Step 12: Show helpful commands
echo ""
echo "📋 Useful Commands:"
echo "==================="
echo "View logs:          docker logs stock-app"
echo "Stop container:     docker stop stock-app"
echo "Start container:    docker start stock-app"
echo "Restart container:  docker restart stock-app"
echo "Remove container:   docker rm stock-app"
echo "Shell into container: docker exec -it stock-app /bin/bash"
echo "Test application:   curl http://localhost:8080"
echo "Open in browser:    http://localhost:8080"

echo ""
print_status "OK" "Docker setup completed successfully! 🎉"
echo ""
echo "If you're still having issues, check the troubleshooting guide in DOCKER_TROUBLESHOOTING.md" 