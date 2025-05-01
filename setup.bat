@echo off

echo ===== SocialSpyAgent Setup =====
echo By Ken Kai does AI - https://www.youtube.com/@kenkaidoesai
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    echo Please make sure venv module is available.
    pause
    exit /b 1
)
echo Virtual environment created successfully.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated successfully.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed successfully.

REM Create .env file from template
echo Creating .env file from template...
if not exist .env (
    copy .env.template .env >nul
    echo .env file created. Please update it with your API keys.
) else (
    echo .env file already exists.
)

echo.
echo ===== Setup Instructions =====
echo.
echo 1. You need to obtain the following API keys:
echo    - Google API Key: https://console.cloud.google.com/
echo    - RapidAPI Key: https://rapidapi.com/
echo.
echo 2. Update the .env file with your API keys.
echo.
echo 3. Run the following command to start using SocialSpyAgent:
echo    venv\Scripts\activate.bat
echo.
echo ===== Setup Complete =====

pause
