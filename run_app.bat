@echo off
setlocal

echo ===== SocialSpyAgent Launcher =====
echo By Ken Kai does AI - https://www.youtube.com/@kenkaidoesai
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    goto :end
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    goto :end
)
echo Virtual environment activated successfully.

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
