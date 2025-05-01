#!/bin/bash
# SocialSpyAgent Setup Script for Mac/Linux
# This script sets up the environment for SocialSpyAgent

# Function to print colored text
print_colored() {
    echo -e "\033[1;36m$1\033[0m"  # Cyan bold text
}

print_success() {
    echo -e "\033[1;32m✅ $1\033[0m"  # Green bold text with checkmark
}

print_info() {
    echo -e "\033[1;34mℹ️  $1\033[0m"  # Blue bold text with info symbol
}

print_warning() {
    echo -e "\033[1;33m⚠️  $1\033[0m"  # Yellow bold text with warning symbol
}

print_error() {
    echo -e "\033[1;31m❌ $1\033[0m"  # Red bold text with X symbol
}

# Print ASCII art banner
echo ""
echo -e "\033[1;36m"
cat << "EOF"
  _____             _       _  _____              _                       _
 / ____|           (_)     | |/ ____|            / \                     | |
| (___   ___   ___ _  __ _| | (___  _ __  _   _ / _ \ __ _  ___ _ __ ___| |_
 \___ \ / _ \ / __| |/ _` | |\___ \| '_ \| | | / ___ \ / _` |/ _ \ '_ \/ __|
 ____) | (_) | (__| | (_| | |____) | |_) | |_| / /   \ \ (_| |  __/ | | \__ \
|_____/ \___/ \___|_|\__,_|_|_____/| .__/ \__, \_/     \_\__, |\___|_| |_|___/
                                   | |     __/ |          __/ |
                                   |_|    |___/          |___/
EOF
echo -e "\033[0m"
echo ""

# Print welcome message
echo -e "\033[1;35m===== Setting up SocialSpyAgent =====\033[0m"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_warning "Python 3 is not installed. Attempting to install..."

    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        print_info "Detected macOS. Attempting to install Python using Homebrew..."

        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            print_info "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            if [ $? -ne 0 ]; then
                print_error "Failed to install Homebrew. Please install Python 3 manually."
                exit 1
            fi
            print_success "Homebrew installed successfully."
        fi

        # Install Python using Homebrew
        print_info "Installing Python 3 using Homebrew..."
        brew install python
        if [ $? -ne 0 ]; then
            print_error "Failed to install Python 3. Please install Python 3 manually."
            exit 1
        fi
        print_success "Python 3 installed successfully."

    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        print_info "Detected Linux. Attempting to install Python..."

        # Try apt (Debian/Ubuntu)
        if command -v apt &> /dev/null; then
            print_info "Using apt package manager..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            if [ $? -ne 0 ]; then
                print_error "Failed to install Python 3 using apt. Please install Python 3 manually."
                exit 1
            fi
        # Try yum (RHEL/CentOS/Fedora)
        elif command -v yum &> /dev/null; then
            print_info "Using yum package manager..."
            sudo yum install -y python3 python3-pip
            if [ $? -ne 0 ]; then
                print_error "Failed to install Python 3 using yum. Please install Python 3 manually."
                exit 1
            fi
        # Try dnf (newer Fedora)
        elif command -v dnf &> /dev/null; then
            print_info "Using dnf package manager..."
            sudo dnf install -y python3 python3-pip
            if [ $? -ne 0 ]; then
                print_error "Failed to install Python 3 using dnf. Please install Python 3 manually."
                exit 1
            fi
        # Try pacman (Arch Linux)
        elif command -v pacman &> /dev/null; then
            print_info "Using pacman package manager..."
            sudo pacman -Sy python python-pip
            if [ $? -ne 0 ]; then
                print_error "Failed to install Python 3 using pacman. Please install Python 3 manually."
                exit 1
            fi
        else
            print_error "Could not determine package manager. Please install Python 3 manually."
            exit 1
        fi

        print_success "Python 3 installed successfully."
    else
        print_error "Unsupported operating system. Please install Python 3 manually."
        exit 1
    fi

    # Verify Python installation
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 installation failed. Please install Python 3 manually."
        exit 1
    fi

    print_success "Python 3 is now installed and available."
fi

# Create virtual environment
print_colored "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment. Please make sure venv module is available."
    exit 1
fi
print_success "Virtual environment created successfully."

# Activate virtual environment
print_colored "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment."
    exit 1
fi
print_success "Virtual environment activated successfully."

# Install dependencies
print_colored "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies."
    exit 1
fi
print_success "Dependencies installed successfully."

# Create .env file from template
print_colored "Creating .env file from template..."
if [ ! -f .env ]; then
    cp .env.template .env
    print_success ".env file created. Please update it with your API keys."
else
    print_info ".env file already exists."
fi

# Print setup instructions
echo ""
echo -e "\033[1;35m===== Setup Instructions =====\033[0m"
echo ""
print_info "1. You need to obtain the following API keys:"
echo "   - Google API Key: https://console.cloud.google.com/"
echo "   - RapidAPI Key: https://rapidapi.com/"
echo ""
print_info "2. Update the .env file with your API keys."
echo ""
print_info "3. Run the following command to start using SocialSpyAgent:"
echo "   source venv/bin/activate"
echo ""
echo -e "\033[1;35m===== Setup Complete =====\033[0m"

# Make the script executable
chmod +x setup.sh

# Pause before exit
read -p "Press Enter to exit..."
