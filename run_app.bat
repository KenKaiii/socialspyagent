@echo off
setlocal

echo ===== SocialSpyAgent Launcher =====
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Setting up...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. Please make sure Python is installed.
        goto :end
    )
    echo Virtual environment created successfully.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    goto :end
)
echo Virtual environment activated successfully.

REM Check if requirements are installed
echo Checking dependencies...
echo Installing/updating all dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    goto :end
)
echo Dependencies installed successfully.

REM Run the application
echo Starting SocialSpyAgent...
python main.py --interactive
if %ERRORLEVEL% NEQ 0 (
    echo Application exited with an error.
) else (
    echo Application closed successfully.
)

:end
echo.
echo Press any key to exit...
pause >nul
endlocal
