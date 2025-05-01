"""
Configuration Handler Module for SocialSpyAgent.

This module provides functions to handle configuration operations
like loading config files, checking API keys, and updating configuration.
"""

import os
import sys
import json
from typing import Dict, List, Any, Union

from terminal_ui import print_info, print_error, print_warning, print_panel, print_success

def load_config() -> Dict[str, List[str]]:
    """
    Load configuration from config.json file.

    Returns:
        Dictionary containing social media account configurations.

    Raises:
        FileNotFoundError: If config.json is not found.
        json.JSONDecodeError: If config.json is not valid JSON.
    """
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            print_info(f"Configuration loaded successfully")
            return config
    except FileNotFoundError:
        print_error("config.json not found.")
        print_panel(
            "Please create a config.json file with your social media accounts.\n"
            "See README.md for instructions.",
            title="Configuration Error"
        )
        sys.exit(1)
    except json.JSONDecodeError:
        print_error("config.json is not valid JSON.")
        print_panel(
            "Please check your config.json file for syntax errors.",
            title="Configuration Error"
        )
        sys.exit(1)

def check_api_keys() -> None:
    """
    Check if required API keys are set in environment variables.

    Raises:
        SystemExit: If any required API key is missing.
    """
    missing_keys = []

    # Check Google API key for YouTube
    if not os.getenv("GOOGLE_API_KEY"):
        missing_keys.append("GOOGLE_API_KEY")

    # Check RapidAPI key for TikTok and Instagram
    if not os.getenv("RAPIDAPI_KEY"):
        missing_keys.append("RAPIDAPI_KEY")

    if missing_keys:
        print_error("The following API keys are missing from your .env file:")
        for key in missing_keys:
            print_error(f"  - {key}")
        print_panel(
            "Please update your .env file with the required API keys.\n"
            "See README.md for instructions on how to obtain these keys.",
            title="API Keys Required"
        )
        sys.exit(1)

def update_config_usernames(platform: str, new_usernames: List[str]) -> bool:
    """
    Update the config.json file with new usernames for the specified platform.

    Args:
        platform: The platform to update ('youtube', 'instagram', or 'tiktok')
        new_usernames: List of usernames to add

    Returns:
        bool: True if the update was successful, False otherwise
    """
    try:
        # Load current config
        config = load_config()

        # Get the key for the platform
        platform_key = f"{platform}_accounts"

        # Get current usernames for the platform
        current_usernames = config.get(platform_key, [])

        # Add new usernames, avoiding duplicates
        added_usernames = []
        for username in new_usernames:
            username = username.strip()
            if username and username not in current_usernames:
                current_usernames.append(username)
                added_usernames.append(username)

        # Update config
        config[platform_key] = current_usernames

        # Save updated config
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        # Print success message
        if added_usernames:
            print_success(f"Added {len(added_usernames)} new username(s) to {platform}: {', '.join(added_usernames)}")
        else:
            print_info("No new usernames were added (they may already exist in the config)")

        return True
    except Exception as e:
        print_error(f"Error updating config: {str(e)}")
        return False

def get_current_usernames(platform: str) -> List[str]:
    """
    Get the current usernames for the specified platform.

    Args:
        platform: The platform to get usernames for ('youtube', 'instagram', or 'tiktok')

    Returns:
        List of usernames for the specified platform
    """
    config = load_config()
    platform_key = f"{platform}_accounts"
    return config.get(platform_key, [])

def remove_config_usernames(platform: str, usernames_to_remove: List[str]) -> bool:
    """
    Remove usernames from the config.json file for the specified platform.

    Args:
        platform: The platform to update ('youtube', 'instagram', or 'tiktok')
        usernames_to_remove: List of usernames to remove

    Returns:
        bool: True if the update was successful, False otherwise
    """
    try:
        # Load current config
        config = load_config()

        # Get the key for the platform
        platform_key = f"{platform}_accounts"

        # Get current usernames for the platform
        current_usernames = config.get(platform_key, [])

        if not current_usernames:
            print_warning(f"No {platform} usernames found in config.json")
            return False

        # Remove usernames
        removed_usernames = []
        for username in usernames_to_remove:
            if username in current_usernames:
                current_usernames.remove(username)
                removed_usernames.append(username)

        # Update config
        config[platform_key] = current_usernames

        # Save updated config
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        # Print success message
        if removed_usernames:
            print_success(f"Removed {len(removed_usernames)} username(s) from {platform}: {', '.join(removed_usernames)}")
        else:
            print_info("No usernames were removed (they may not exist in the config)")

        return True
    except Exception as e:
        print_error(f"Error updating config: {str(e)}")
        return False
