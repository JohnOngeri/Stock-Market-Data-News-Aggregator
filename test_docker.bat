@echo off
REM Docker Test Script for Stock Market Data & News Aggregator (Windows)
REM This script will help diagnose and fix Docker issues

echo 🐳 Docker Troubleshooting Script
echo ================================
echo.

REM Step 1: Check if Docker is installed
echo Step 1: Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker is installed
    docker --version
) else (
    echo ❌ Docker is not installed
    echo.
    echo To install Docker:
    echo   Download Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Step 2: Check if Docker daemon is running
echo.
echo Step 2: Checking Docker daemon...
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker daemon is running
) else (
    echo ❌ Docker daemon is not running
    echo.
    echo To start Docker:
    echo   1. Start Docker Desktop
    echo   2. Wait for Docker to fully start
    echo   3. Try again
    pause
    exit /b 1
)

REM Step 3: Check if we're in the right directory
echo.
echo Step 3: Checking project files...
if exist "Dockerfile" (
    if exist "app.py" (
        if exist "requirements.txt" (
            echo ✅ All required files found
        ) else (
            echo ❌ Missing requirements.txt
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Missing app.py
        pause
        exit /b 1
    )
) else (
    echo ❌ Missing Dockerfile
    echo Make sure you're in the Stock-Market-Data-News-Aggregator directory
    pause
    exit /b 1
)

REM Step 4: Check if .env file exists
echo.
echo Step 4: Checking environment configuration...
if exist ".env" (
    echo ✅ .env file found
    findstr "ALPHA_VANTAGE_API_KEY" .env >nul 2>&1
    if %errorlevel% equ 0 (
        findstr "NEWS_API_KEY" .env >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ API keys configured in .env
        ) else (
            echo ⚠️  API keys not found in .env file
            echo Creating .env file with placeholder values...
            (
                echo ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
                echo NEWS_API_KEY=your_news_api_key_here
            ) > .env
            echo ✅ Created .env file with placeholder values
        )
    ) else (
        echo ⚠️  API keys not found in .env file
        echo Creating .env file with placeholder values...
        (
            echo ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
            echo NEWS_API_KEY=your_news_api_key_here
        ) > .env
        echo ✅ Created .env file with placeholder values
    )
) else (
    echo ⚠️  .env file not found
    echo Creating .env file...
    (
        echo ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
        echo NEWS_API_KEY=your_news_api_key_here
    ) > .env
    echo ✅ Created .env file with placeholder values
)

REM Step 5: Clean up any existing containers
echo.
echo Step 5: Cleaning up existing containers...
docker ps -a --format "table {{.Names}}" | findstr "stock-app" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Found existing stock-app container, removing...
    docker stop stock-app 2>nul
    docker rm stock-app 2>nul
    echo ✅ Cleaned up existing container
) else (
    echo ✅ No existing containers found
)

REM Step 6: Build Docker image
echo.
echo Step 6: Building Docker image...
docker build -t stock-market-aggregator:v1 .
if %errorlevel% equ 0 (
    echo ✅ Docker image built successfully
) else (
    echo ❌ Docker build failed
    echo.
    echo Trying to build with no cache...
    docker build --no-cache -t stock-market-aggregator:v1 .
    if %errorlevel% equ 0 (
        echo ✅ Docker image built successfully (no cache)
    ) else (
        echo ❌ Docker build still failed
        echo.
        echo Common build issues:
        echo   1. Check your internet connection
        echo   2. Make sure all files are present
        echo   3. Try: docker system prune -a
        pause
        exit /b 1
    )
)

REM Step 7: Run container
echo.
echo Step 7: Running container...
docker run -d --name stock-app -p 8080:8080 --env-file .env stock-market-aggregator:v1
if %errorlevel% equ 0 (
    echo ✅ Container started successfully
) else (
    echo ❌ Failed to start container
    echo.
    echo Checking container logs...
    docker logs stock-app
    pause
    exit /b 1
)

REM Step 8: Wait for container to be ready
echo.
echo Step 8: Waiting for application to start...
timeout /t 5 /nobreak >nul

REM Step 9: Check if container is running
echo.
echo Step 9: Checking container status...
docker ps | findstr "stock-app" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Container is running
) else (
    echo ❌ Container is not running
    echo.
    echo Container logs:
    docker logs stock-app
    pause
    exit /b 1
)

REM Step 10: Test application
echo.
echo Step 10: Testing application...
curl -f http://localhost:8080 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Application is accessible at http://localhost:8080
) else (
    echo ⚠️  Application not immediately accessible
    echo Waiting a bit more...
    timeout /t 10 /nobreak >nul
    curl -f http://localhost:8080 >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Application is now accessible at http://localhost:8080
    ) else (
        echo ❌ Application is not accessible
        echo.
        echo Container logs:
        docker logs stock-app
        echo.
        echo Trying to access with curl -v:
        curl -v http://localhost:8080
    )
)

REM Step 11: Show container info
echo.
echo Step 11: Container information...
for /f "tokens=1" %%i in ('docker ps -q --filter name^=stock-app') do set CONTAINER_ID=%%i
echo Container ID: %CONTAINER_ID%
echo Container logs: docker logs stock-app
echo Stop container: docker stop stock-app
echo Remove container: docker rm stock-app
echo Access application: http://localhost:8080

REM Step 12: Show helpful commands
echo.
echo 📋 Useful Commands:
echo ===================
echo View logs:          docker logs stock-app
echo Stop container:     docker stop stock-app
echo Start container:    docker start stock-app
echo Restart container:  docker restart stock-app
echo Remove container:   docker rm stock-app
echo Shell into container: docker exec -it stock-app /bin/bash
echo Test application:   curl http://localhost:8080
echo Open in browser:    http://localhost:8080

echo.
echo ✅ Docker setup completed successfully! 🎉
echo.
echo If you're still having issues, check the troubleshooting guide in DOCKER_TROUBLESHOOTING.md
pause 