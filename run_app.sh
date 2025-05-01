#!/bin/bash

# Set colors
CYAN="\033[36m"
GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
RESET="\033[0m"

# Function to print colored text
print_colored() {
    echo -e "${!2}$1${RESET}"
}

print_success() {
    echo -e "${GREEN}[✓] $1${RESET}"
}

print_error() {
    echo -e "${RED}[✗] $1${RESET}"
}

# Display header
print_colored "===== SocialSpyAgent Launcher =====" "CYAN"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_colored "Virtual environment not found. Setting up..." "YELLOW"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment. Please make sure Python is installed."
        exit 1
    fi
    print_success "Virtual environment created successfully."
fi

# Activate virtual environment
print_colored "Activating virtual environment..." "CYAN"
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment."
    exit 1
fi
print_success "Virtual environment activated successfully."

# Check if requirements are installed
print_colored "Checking dependencies..." "CYAN"
print_colored "Installing/updating all dependencies..." "YELLOW"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies."
    exit 1
fi
print_success "Dependencies installed successfully."

# Run the application
print_colored "Starting SocialSpyAgent..." "CYAN"
python main.py --interactive
if [ $? -ne 0 ]; then
    print_error "Application exited with an error."
else
    print_success "Application closed successfully."
fi

# Pause before exit
echo
echo "Press Enter to exit..."
read
