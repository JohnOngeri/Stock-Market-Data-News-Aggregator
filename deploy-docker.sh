#!/bin/bash

# Docker Hub Deployment Script
# This script builds the Docker image, pushes it to Docker Hub,
# and deploys the application locally using the load balancer setup.
set -e

# --- Configuration ---
# Your Docker Hub username. Can be set as an environment variable.
DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME:-"your-username"}
IMAGE_NAME="stock-market-aggregator"
TAG=${TAG:-"latest"}
FULL_IMAGE_NAME="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${TAG}"

# --- Pre-flight Checks ---
echo "Starting Docker deployment process..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Validate Docker Hub username
if [ "${DOCKER_HUB_USERNAME}" == "your-username" ]; then
    echo "Error: Please set your DOCKER_HUB_USERNAME environment variable or edit this script."
    echo "Example: export DOCKER_HUB_USERNAME=myusername"
    exit 1
fi

# --- Docker Hub Login ---
echo "Please log in to Docker Hub..."
docker login -u "${DOCKER_HUB_USERNAME}"

# --- Build and Push ---
echo "Building Docker image: ${FULL_IMAGE_NAME}"
docker build -t "${FULL_IMAGE_NAME}" .

echo "Pushing image to Docker Hub..."
docker push "${FULL_IMAGE_NAME}"

echo "Image pushed successfully to Docker Hub!"
echo "Image: ${FULL_IMAGE_NAME}"

# --- Deploy with Load Balancer ---
echo "Deploying services with the load balancer..."

# Export the username so docker-compose can use it
export DOCKER_HUB_USERNAME

# Stop any running services to ensure a clean slate
echo "Stopping existing services..."
docker-compose -f docker-compose.loadbalancer.yml down

# Pull the newly pushed image to ensure we're using the latest version
echo "Pulling latest image from Docker Hub..."
docker-compose -f docker-compose.loadbalancer.yml pull

# Start the services in detached mode
echo "Starting services..."
docker-compose -f docker-compose.loadbalancer.yml up -d

echo ""
echo "Deployment complete!"
echo "Application should be available at: http://localhost"