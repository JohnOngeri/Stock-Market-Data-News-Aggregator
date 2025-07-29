#!/bin/bash

# Deployment script for Stock Market Data & News Aggregator

set -e

echo "🚀 Starting deployment process..."

# Configuration
IMAGE_NAME="your-dockerhub-username/stock-market-aggregator"
TAG="latest"

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME:$TAG .

# Tag for Docker Hub
echo "🏷️  Tagging image for Docker Hub..."
docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:$TAG

# Push to Docker Hub
echo "⬆️  Pushing to Docker Hub..."
docker push $IMAGE_NAME:$TAG

echo "✅ Deployment completed successfully!"
echo "Image: $IMAGE_NAME:$TAG"
echo ""
echo "To deploy on your servers, run:"
echo "docker pull $IMAGE_NAME:$TAG"
echo "docker-compose -f docker-compose.prod.yml up -d"