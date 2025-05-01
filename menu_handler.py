"""
Menu Handler Module for SocialSpyAgent.

This module provides functions to handle the interactive menu
and user interactions.
"""

import os
from typing import Dict, List, Any

from terminal_ui import (
    welcome_screen, exit_screen, print_title, print_subtitle, print_panel,
    print_error, print_warning, print_info, print_success,
    get_user_choice, get_fancy_user_input,
    console, HIGHLIGHT_STYLE
)
from config_handler import load_config, check_api_keys, update_config_usernames, get_current_usernames, remove_config_usernames
from platform_handler import search_platform, process_platform_accounts
from sherlock_handler import spy_on_username

def interactive_menu():
    """Run the interactive menu for SocialSpyAgent."""
    # Display welcome screen
    welcome_screen()

    # Check if required API keys are set
    check_api_keys()

    # Load configuration
    config = load_config()

    # Create output directories
    os.makedirs("Output JSON", exist_ok=True)
    os.makedirs("Output CSV", exist_ok=True)
    os.makedirs("Output Spy", exist_ok=True)

    # Main menu
    main_options = [
        "Search by query",
        "Competitor Analysis",
        "Spy on username",
        "Manage usernames",
        "Exit (or press CTRL+C anytime)"
    ]

    while True:
        try:
            choice = get_user_choice("What would you like to do?", main_options)

            if choice == 1:  # Search by query
                handle_search_by_query()

            elif choice == 2:  # Competitor Analysis
                handle_competitor_analysis(config)

            elif choice == 3:  # Spy on username
                spy_on_username()

            elif choice == 4:  # Manage usernames
                handle_manage_usernames()
                # Reload config after potential changes
                config = load_config()

            elif choice == 5:  # Exit
                exit_screen()
                break

            print_subtitle("Operation completed")

        except KeyboardInterrupt:
            # Handle Ctrl+C within the menu loop
            print("\n")  # Add some space after the ^C
            print_panel("Operation cancelled by user", title="Interrupted")
            continue  # Return to the main menu

def handle_search_by_query():
    """Handle the 'Search by query' menu option."""
    # Get search query with fancy prompt
    query = get_fancy_user_input(
        "Enter your search query",
        "Type keywords to search across YouTube, Instagram, and TikTok.\nExamples: trending fashion, viral dance, product review",
        default="trending content"
    )
    if not query.strip():
        print_error("Search query cannot be empty.")
        return

    # Get time frame
    time_frame_options = [
        "Last 24 hours",
        "Last week (7 days)",
        "Last 30 days",
        "All time"
    ]

    time_frame = get_user_choice("Select time frame:", time_frame_options)

    # Search YouTube
    search_platform("youtube", query, time_frame, "Output JSON")

    # Search Instagram
    search_platform("instagram", query, "Output JSON")

    # Search TikTok
    search_platform("tiktok", query, "Output JSON")

def handle_competitor_analysis(config: Dict[str, List[str]]):
    """
    Handle the 'Competitor Analysis' menu option.

    Args:
        config: Configuration dictionary containing social media accounts
    """
    # Get time frame
    time_frame_options = [
        "Last 24 hours",
        "Last week (7 days)",
        "Last 30 days",
        "All time"
    ]

    time_frame = get_user_choice("Select time frame for competitor analysis:", time_frame_options)

    # Process YouTube accounts
    youtube_accounts = config.get("youtube_accounts", [])
    if youtube_accounts:
        process_platform_accounts("youtube", youtube_accounts, time_frame, "Output JSON")
    else:
        print_warning("No YouTube accounts found in config.json")

    # Process Instagram accounts
    instagram_accounts = config.get("instagram_accounts", [])
    if instagram_accounts:
        process_platform_accounts("instagram", instagram_accounts, "Output JSON")
    else:
        print_warning("No Instagram accounts found in config.json")

    # Process TikTok accounts
    tiktok_accounts = config.get("tiktok_accounts", [])
    if tiktok_accounts:
        process_platform_accounts("tiktok", tiktok_accounts, "Output JSON")
    else:
        print_warning("No TikTok accounts found in config.json")

def handle_manage_usernames():
    """Handle the 'Manage usernames' menu option."""
    # Platform selection menu
    platform_options = [
        "YouTube",
        "Instagram",
        "TikTok",
        "Back to main menu"
    ]

    while True:
        platform_choice = get_user_choice("Select platform to manage usernames:", platform_options)

        if platform_choice == 4:  # Back to main menu
            return

        # Map choice to platform name
        platform_map = {
            1: "youtube",
            2: "instagram",
            3: "tiktok"
        }

        platform = platform_map[platform_choice]

        # Show current usernames
        current_usernames = get_current_usernames(platform)

        if current_usernames:
            print_title(f"Current {platform.title()} usernames:")
            for i, username in enumerate(current_usernames, 1):
                print_info(f"{i}. {username}")

            # Ask what action to take
            action_options = [
                f"Add {platform.title()} usernames",
                f"Remove {platform.title()} usernames",
                "Back to platform selection"
            ]

            action_choice = get_user_choice(f"What would you like to do with {platform.title()} usernames?", action_options)

            if action_choice == 1:  # Add usernames
                handle_add_usernames(platform)
            elif action_choice == 2:  # Remove usernames
                handle_remove_usernames(platform, current_usernames)
            else:  # Back to platform selection
                continue
        else:
            print_warning(f"No {platform.title()} usernames found in config.json")

            # Only option is to add usernames
            print_info(f"You can add {platform.title()} usernames below.")
            handle_add_usernames(platform)

def handle_add_usernames(platform: str):
    """
    Handle adding usernames to a platform.

    Args:
        platform: The platform to add usernames to ('youtube', 'instagram', or 'tiktok')
    """
    # Get new usernames
    new_usernames_input = get_fancy_user_input(
        f"Enter {platform.title()} usernames to add",
        "Enter one or more usernames, separated by commas.\nLeave empty and press Enter to cancel.",
        default=""
    )

    if not new_usernames_input.strip():
        print_info("No usernames entered, returning to platform selection.")
        return

    # Split by comma and clean up
    new_usernames = [username.strip() for username in new_usernames_input.split(",") if username.strip()]

    if not new_usernames:
        print_error("No valid usernames entered.")
        return

    # Update config
    success = update_config_usernames(platform, new_usernames)

    if success:
        print_panel(
            f"Username configuration for {platform.title()} has been updated.",
            title="Configuration Updated"
        )
    else:
        print_error(f"Failed to update {platform.title()} usernames in config.json.")

def handle_remove_usernames(platform: str, current_usernames: List[str]):
    """
    Handle removing usernames from a platform.

    Args:
        platform: The platform to remove usernames from ('youtube', 'instagram', or 'tiktok')
        current_usernames: List of current usernames for the platform
    """
    if not current_usernames:
        print_warning(f"No {platform.title()} usernames to remove.")
        return

    # Create options for removal
    removal_options = current_usernames.copy()
    removal_options.append("Cancel removal")

    # Allow multiple selections
    print_subtitle(f"Select {platform.title()} usernames to remove:")
    print_info("Enter the numbers of the usernames to remove, separated by commas.")
    print_info("For example, to remove the first and third username, enter: 1,3")

    # Display usernames with numbers
    for i, username in enumerate(current_usernames, 1):
        print_info(f"{i}. {username}")

    print_info(f"{len(current_usernames) + 1}. Cancel removal")

    # Get user input for removal
    console.print("\nEnter numbers to remove (comma-separated): ", style=HIGHLIGHT_STYLE, end="")
    try:
        removal_input = input()

        if not removal_input.strip():
            print_info("No usernames selected for removal.")
            return

        # Parse input and validate
        try:
            # Split by comma and convert to integers
            selected_indices = [int(idx.strip()) for idx in removal_input.split(",") if idx.strip()]

            # Validate indices
            valid_indices = [idx for idx in selected_indices if 1 <= idx <= len(current_usernames)]

            if not valid_indices:
                print_error("No valid usernames selected for removal.")
                return

            # Get usernames to remove
            usernames_to_remove = [current_usernames[idx-1] for idx in valid_indices]

            # Confirm removal
            print_panel(
                f"You are about to remove the following usernames from {platform.title()}:\n" +
                "\n".join([f"- {username}" for username in usernames_to_remove]),
                title="Confirm Removal"
            )

            confirm_options = ["Yes, remove these usernames", "No, cancel removal"]
            confirm_choice = get_user_choice("Are you sure you want to remove these usernames?", confirm_options)

            if confirm_choice == 1:  # Confirm removal
                # Remove usernames
                success = remove_config_usernames(platform, usernames_to_remove)

                if success:
                    print_panel(
                        f"Username configuration for {platform.title()} has been updated.",
                        title="Configuration Updated"
                    )
                else:
                    print_error(f"Failed to update {platform.title()} usernames in config.json.")
            else:
                print_info("Username removal cancelled.")

        except ValueError:
            print_error("Invalid input. Please enter numbers separated by commas.")

    except KeyboardInterrupt:
        print("\n")  # Add some space after the ^C
        print_info("Username removal cancelled.")
        return
