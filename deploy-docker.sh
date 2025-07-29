#!/bin/bash

# Docker Hub Deployment Script
set -e

# Configuration
DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME:-"your-username"}
IMAGE_NAME="stock-market-aggregator"
TAG=${TAG:-"latest"}

echo "🚀 Starting Docker deployment process..."

# Build the image
echo "📦 Building Docker image..."
docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${TAG} .

# Tag for Docker Hub
echo "🏷️  Tagging image for Docker Hub..."
docker tag ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${TAG} ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${TAG}

# Push to Docker Hub
echo "⬆️  Pushing to Docker Hub..."
docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${TAG}

echo "✅ Image pushed successfully to Docker Hub!"
echo "📋 Image: ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${TAG}"

# Deploy with load balancer
echo "🔄 Deploying with load balancer..."
export DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME}
docker-compose -f docker-compose.loadbalancer.yml down
docker-compose -f docker-compose.loadbalancer.yml pull
docker-compose -f docker-compose.loadbalancer.yml up -d

echo "🎉 Deployment complete!"
echo "🌐 Application available at: http://localhost"