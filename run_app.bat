@echo off
setlocal

:: Set colors
set CYAN=36
set GREEN=32
set RED=31
set YELLOW=33
set RESET=0

:: Function to print colored text
call :print_colored "SocialSpyAgent Launcher" %CYAN%
echo.

:: Check if virtual environment exists
if not exist venv (
    call :print_colored "Virtual environment not found. Setting up..." %YELLOW%
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        call :print_error "Failed to create virtual environment. Please make sure Python is installed."
        goto :end
    )
    call :print_success "Virtual environment created successfully."
)

:: Activate virtual environment
call :print_colored "Activating virtual environment..." %CYAN%
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    call :print_error "Failed to activate virtual environment."
    goto :end
)
call :print_success "Virtual environment activated successfully."

:: Check if requirements are installed
call :print_colored "Checking dependencies..." %CYAN%
pip show sherlock-project >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :print_colored "Installing dependencies..." %YELLOW%
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        call :print_error "Failed to install dependencies."
        goto :end
    )
    call :print_success "Dependencies installed successfully."
) else (
    call :print_success "Dependencies already installed."
)

:: Run the application
call :print_colored "Starting SocialSpyAgent..." %CYAN%
python main.py --interactive
if %ERRORLEVEL% NEQ 0 (
    call :print_error "Application exited with an error."
) else (
    call :print_success "Application closed successfully."
)

goto :end

:print_colored
echo [%~2m%~1[0m
exit /b

:print_success
echo [%GREEN%m[✓] %~1[0m
exit /b

:print_error
echo [%RED%m[✗] %~1[0m
exit /b

:end
endlocal
