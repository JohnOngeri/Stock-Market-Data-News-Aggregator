@echo off
REM Docker Hub Deployment Script for Windows
setlocal enabledelayedexpansion

REM Configuration
if "%DOCKER_HUB_USERNAME%"=="" set DOCKER_HUB_USERNAME=your-username
set IMAGE_NAME=stock-market-aggregator
if "%TAG%"=="" set TAG=latest

echo Starting Docker deployment process...

REM Build the image
echo Building Docker image...
docker build -t %DOCKER_HUB_USERNAME%/%IMAGE_NAME%:%TAG% .
if errorlevel 1 goto error

REM Push to Docker Hub
echo Pushing to Docker Hub...
docker push %DOCKER_HUB_USERNAME%/%IMAGE_NAME%:%TAG%
if errorlevel 1 goto error

echo Image pushed successfully to Docker Hub!
echo Image: %DOCKER_HUB_USERNAME%/%IMAGE_NAME%:%TAG%

REM Deploy with load balancer
echo Deploying with load balancer...
docker-compose -f docker-compose.loadbalancer.yml down
docker-compose -f docker-compose.loadbalancer.yml pull
docker-compose -f docker-compose.loadbalancer.yml up -d
if errorlevel 1 goto error

echo Deployment complete!
echo Application available at: http://localhost
goto end

:error
echo Deployment failed!
exit /b 1

:end