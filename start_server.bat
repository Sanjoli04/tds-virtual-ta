@echo off
echo Starting VirtualTA Knowledge Base Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create a .env file with your API_KEY
    echo Example: API_KEY=your_api_key_here
    echo.
)

REM Start the server
echo Starting server...
python deploy.py

pause 