@echo off
REM Simple deployment script for Stock Market Aggregator (Windows)

echo 🚀 Stock Market Aggregator - Simple Deployment
echo ==============================================

REM Configuration
set DOCKERHUB_USERNAME=your-dockerhub-username
set APP_NAME=stock-market-aggregator
set VERSION=v1
set IMAGE_NAME=%DOCKERHUB_USERNAME%/%APP_NAME%:%VERSION%

REM Step 1: Build the Docker image
echo 📦 Building Docker image...
docker build -t %IMAGE_NAME% .

if %errorlevel% neq 0 (
    echo ❌ Docker build failed
    exit /b 1
)
echo ✅ Docker image built successfully

REM Step 2: Test locally
echo 🧪 Testing locally...
docker run -d --name test-app -p 8080:8080 -e ALPHA_VANTAGE_API_KEY=%ALPHA_VANTAGE_API_KEY% -e NEWS_API_KEY=%NEWS_API_KEY% %IMAGE_NAME%

timeout /t 5 /nobreak > nul

REM Test if app is responding
curl -f http://localhost:8080 > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Local test passed
    docker stop test-app
    docker rm test-app
) else (
    echo ❌ Local test failed
    docker stop test-app
    docker rm test-app
    exit /b 1
)

REM Step 3: Push to Docker Hub
echo 📤 Pushing to Docker Hub...
docker login
docker push %IMAGE_NAME%

if %errorlevel% neq 0 (
    echo ❌ Push to Docker Hub failed
    exit /b 1
)

echo ✅ Image pushed to Docker Hub successfully
echo 🔗 Image available at: https://hub.docker.com/r/%DOCKERHUB_USERNAME%/%APP_NAME%

echo 🎉 Deployment preparation complete!
echo Next steps:
echo 1. SSH to web-01 and web-02
echo 2. Run: docker pull %IMAGE_NAME%
echo 3. Run: docker run -d --name app --restart unless-stopped -p 8080:8080 -e ALPHA_VANTAGE_API_KEY=your_key -e NEWS_API_KEY=your_key %IMAGE_NAME%
echo 4. Configure load balancer