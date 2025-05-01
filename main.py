"""
SocialSpyAgent - Social Media Data Scraper

This script provides a command-line interface to scrape data from various
social media platforms including YouTube, Instagram, and TikTok.
"""

import os
import sys
import signal
import argparse
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from terminal_ui import exit_screen, print_title, print_subtitle, print_warning

# Import handlers
from config_handler import check_api_keys, load_config
from platform_handler import search_platform, process_platform_accounts
from menu_handler import interactive_menu

# Load environment variables
load_dotenv()

def ctrl_c_handler(sig, frame):  # pylint: disable=unused-argument
    """
    Handle CTRL+C signal by showing exit screen and exiting.

    Args:
        sig: Signal number (unused but required by signal handler interface)
        frame: Current stack frame (unused but required by signal handler interface)
    """
    print("\n")  # Add some space after the ^C
    exit_screen()
    sys.exit(0)

def main():
    """Main function to run the SocialSpyAgent."""
    # Set up signal handler for CTRL+C
    signal.signal(signal.SIGINT, ctrl_c_handler)

    parser = argparse.ArgumentParser(description="SocialSpyAgent - Social Media Data Scraper")
    parser.add_argument("--platform", choices=["youtube", "instagram", "tiktok", "all"],
                        default=None, help="Social media platform to scrape")
    parser.add_argument("--output", default="Output JSON", help="Output directory for scraped data")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--query", help="Search query for YouTube (requires --platform youtube)")
    parser.add_argument("--timeframe", type=int, choices=[1, 2, 3, 4], default=4,
                       help="Time frame: 1=24h, 2=7d, 3=30d, 4=all")

    args = parser.parse_args()

    # Check if required API keys are set
    check_api_keys()

    # Run in interactive mode if specified or if no platform is specified
    if args.interactive or args.platform is None:
        interactive_menu()
        return

    # Load configuration
    config = load_config()

    # Create output directories if they don't exist
    os.makedirs(args.output, exist_ok=True)
    os.makedirs("Output CSV", exist_ok=True)
    os.makedirs("Output Spy", exist_ok=True)

    # If query is provided, do a search based on platform
    if args.query:
        if args.platform == "youtube":
            print_title(f"YouTube Search: {args.query}")
            search_platform("youtube", args.query, args.timeframe, args.output)
            return
        elif args.platform == "instagram":
            print_title(f"Instagram Search: {args.query}")
            search_platform("instagram", args.query, args.output)
            return
        elif args.platform == "tiktok":
            print_title(f"TikTok Search: {args.query}")
            search_platform("tiktok", args.query, args.output)
            return
        elif args.platform == "all":
            print_title(f"Social Media Search: {args.query}")
            search_platform("youtube", args.query, args.timeframe, args.output)
            search_platform("instagram", args.query, args.output)
            search_platform("tiktok", args.query, args.output)
            return

    # Process accounts based on selected platform
    if args.platform in ["youtube", "all"]:
        youtube_accounts = config.get("youtube_accounts", [])
        if youtube_accounts:
            print_title(f"YouTube Competitor Analysis")
            process_platform_accounts("youtube", youtube_accounts, args.timeframe, args.output)
        else:
            print_warning("No YouTube accounts found in config.json")

    if args.platform in ["instagram", "all"]:
        instagram_accounts = config.get("instagram_accounts", [])
        if instagram_accounts:
            print_title(f"Instagram Competitor Analysis")
            process_platform_accounts("instagram", instagram_accounts, args.output)
        else:
            print_warning("No Instagram accounts found in config.json")

    if args.platform in ["tiktok", "all"]:
        tiktok_accounts = config.get("tiktok_accounts", [])
        if tiktok_accounts:
            print_title(f"TikTok Competitor Analysis")
            process_platform_accounts("tiktok", tiktok_accounts, args.output)
        else:
            print_warning("No TikTok accounts found in config.json")

    print_subtitle("SocialSpyAgent completed")

if __name__ == "__main__":
    main()
