@echo off
setlocal enabledelayedexpansion

:: Set color codes
set "CYAN=36"
set "GREEN=32"
set "BLUE=34"
set "YELLOW=33"
set "RED=31"
set "MAGENTA=35"
set "WHITE=37"

:: Function to print colored text
call :print_colored "  _____             _       _  _____              _                       _   " %CYAN%
call :print_colored " / ____|           (_)     | |/ ____|            / \                     | |  " %CYAN%
call :print_colored "| (___   ___   ___ _  __ _| | (___  _ __  _   _ / _ \ __ _  ___ _ __ ___| |_ " %CYAN%
call :print_colored " \___ \ / _ \ / __| |/ _` | |\___ \| '_ \| | | / ___ \ / _` |/ _ \ '_ \/ __|" %CYAN%
call :print_colored " ____) | (_) | (__| | (_| | |____) | |_) | |_| / /   \ \ (_| |  __/ | | \__ \" %CYAN%
call :print_colored "|_____/ \___/ \___|_|\__,_|_|_____/| .__/ \__, \_/     \_\__, |\___|_| |_|___/" %CYAN%
call :print_colored "                                   | |     __/ |          __/ |              " %CYAN%
call :print_colored "                                   |_|    |___/          |___/               " %CYAN%
echo.

call :print_colored "===== Setting up SocialSpyAgent =====" %MAGENTA%
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :print_warning "Python is not installed or not in PATH. Attempting to download and install..."

    :: Create a temporary directory for Python installer
    mkdir temp_python_install 2>nul
    cd temp_python_install

    :: Download Python installer
    call :print_info "Downloading Python installer..."
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe' -OutFile 'python_installer.exe'}"
    if %ERRORLEVEL% NEQ 0 (
        call :print_error "Failed to download Python installer."
        cd ..
        rmdir /s /q temp_python_install 2>nul
        goto :end
    )

    :: Run Python installer with required options
    call :print_info "Installing Python (this may take a few minutes)..."
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if %ERRORLEVEL% NEQ 0 (
        call :print_error "Failed to install Python."
        cd ..
        rmdir /s /q temp_python_install 2>nul
        goto :end
    )

    :: Clean up
    cd ..
    rmdir /s /q temp_python_install 2>nul

    :: Refresh environment variables
    call :print_info "Refreshing environment variables..."
    call :refresh_env

    :: Verify Python installation
    python --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        call :print_error "Python installation failed or PATH was not updated. Please install Python manually."
        goto :end
    )

    call :print_success "Python installed successfully!"
)

:: Create virtual environment with spinner animation
call :print_colored "Creating virtual environment..." %CYAN%
echo [  ] Processing...
python -m venv venv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :print_error "Failed to create virtual environment. Please make sure venv module is available."
    goto :end
)
echo [✓] Virtual environment created successfully.

:: Activate virtual environment with spinner animation
call :print_colored "Activating virtual environment..." %CYAN%
echo [  ] Processing...
call venv\Scripts\activate.bat >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :print_error "Failed to activate virtual environment."
    goto :end
)
echo [✓] Virtual environment activated successfully.

:: Install dependencies with spinner animation
call :print_colored "Installing dependencies..." %CYAN%
echo [  ] This may take a few minutes...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    call :print_error "Failed to install dependencies."
    goto :end
)
echo [✓] Dependencies installed successfully.

:: Create .env file from template
call :print_colored "Creating .env file from template..." %CYAN%
if not exist .env (
    copy .env.template .env >nul
    call :print_success ".env file created. Please update it with your API keys."
) else (
    call :print_info ".env file already exists."
)

echo.
call :print_colored "===== Setup Instructions =====" %MAGENTA%
echo.
call :print_info "1. You need to obtain the following API keys:"
echo    - Google API Key: https://console.cloud.google.com/
echo    - RapidAPI Key: https://rapidapi.com/
echo.
call :print_info "2. Update the .env file with your API keys."
echo.
call :print_info "3. Run the following command to start using SocialSpyAgent:"
echo    venv\Scripts\activate.bat
echo.
call :print_colored "===== Setup Complete =====" %MAGENTA%

goto :end

:print_colored
echo [1;%~2m%~1[0m
exit /b

:print_success
echo [1;32m✅ %~1[0m
exit /b

:print_info
echo [1;34mℹ️ %~1[0m
exit /b

:print_warning
echo [1;33m⚠️ %~1[0m
exit /b

:print_error
echo [1;31m❌ %~1[0m
exit /b

:refresh_env
:: This function refreshes environment variables without restarting the script
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /ve') do set "PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /ve') do set "PATH=!PATH!;%%b"
exit /b

:end
pause
