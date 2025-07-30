@echo off
echo 🐳 Simple Docker Runner for Stock Market App
echo ============================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file with test keys...
    (
        echo ALPHA_VANTAGE_API_KEY=test_key
        echo NEWS_API_KEY=test_key
    ) > .env
    echo ✅ Created .env file
)

REM Stop and remove existing containers
echo Cleaning up existing containers...
docker stop stock-app-simple 2>nul
docker rm stock-app-simple 2>nul

REM Build and run with simple Dockerfile
echo Building and running application...
docker build -f Dockerfile.simple -t stock-app-simple .
if %errorlevel% neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo ✅ Build successful

REM Run the container
docker run -d --name stock-app-simple -p 8080:8080 --env-file .env stock-app-simple
if %errorlevel% neq 0 (
    echo ❌ Failed to start container
    echo Container logs:
    docker logs stock-app-simple
    pause
    exit /b 1
)

echo ✅ Container started successfully

REM Wait for application to start
echo Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Test the application
echo Testing application...
curl -f http://localhost:8080 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Application is running at http://localhost:8080
    echo.
    echo 🎉 Success! Open your browser and go to:
    echo    http://localhost:8080
) else (
    echo ⚠️  Application might still be starting...
    echo Container logs:
    docker logs stock-app-simple
    echo.
    echo Try accessing: http://localhost:8080
)

echo.
echo 📋 Useful commands:
echo   View logs:    docker logs stock-app-simple
echo   Stop app:     docker stop stock-app-simple
echo   Remove app:   docker rm stock-app-simple
echo   Restart:      docker restart stock-app-simple

pause 