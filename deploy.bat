@echo off
REM Deployment script for Windows

echo 🚀 Starting deployment process...

REM Configuration
set IMAGE_NAME=your-dockerhub-username/stock-market-aggregator
set TAG=latest

REM Build the Docker image
echo 📦 Building Docker image...
docker build -t %IMAGE_NAME%:%TAG% .

REM Push to Docker Hub
echo ⬆️  Pushing to Docker Hub...
docker push %IMAGE_NAME%:%TAG%

echo ✅ Deployment completed successfully!
echo Image: %IMAGE_NAME%:%TAG%
echo.
echo To deploy on your servers, run:
echo docker pull %IMAGE_NAME%:%TAG%
echo docker-compose -f docker-compose.prod.yml up -d

pause