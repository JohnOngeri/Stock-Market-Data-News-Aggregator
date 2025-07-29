@echo off
echo Starting Stock Market Data ^& News Aggregator
echo ============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys
    echo.
    pause
    exit /b 1
)

REM Start the application
echo Starting Flask application...
echo Application will be available at http://localhost:8080
echo Press Ctrl+C to stop the server
echo.
python app.py