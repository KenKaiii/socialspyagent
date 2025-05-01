"""
Platform Handler Module for SocialSpyAgent.

This module provides generic functions to handle operations across different social media platforms.
"""

import os
import json
from typing import List, Dict, Any
import datetime

from youtube_api import YouTubeAPI
from instagram_api import InstagramAPI
from tiktok_api import TikTokAPI
from csv_exporter import export_youtube_data_to_csv, export_instagram_data_to_csv, export_tiktok_data_to_csv
from terminal_ui import (
    print_title, print_subtitle, print_info, print_success, print_warning, print_error,
    display_youtube_videos, display_instagram_reels, display_tiktok_videos,
    run_with_spinner
)

def get_time_frame_info(time_frame: int) -> Dict[str, Any]:
    """
    Get time frame information based on the time frame code.

    Args:
        time_frame: Time frame code (1: last 24 hours, 2: last week, 3: last 30 days, 4: all time)

    Returns:
        Dictionary containing published_after, time_frame_str, and time_frame_display
    """
    now = datetime.datetime.now(datetime.timezone.utc)

    if time_frame == 1:  # Last 24 hours
        return {
            "published_after": now - datetime.timedelta(days=1),
            "time_frame_str": "24h",
            "time_frame_display": "Last 24 hours"
        }
    elif time_frame == 2:  # Last week
        return {
            "published_after": now - datetime.timedelta(days=7),
            "time_frame_str": "7d",
            "time_frame_display": "Last 7 days"
        }
    elif time_frame == 3:  # Last 30 days
        return {
            "published_after": now - datetime.timedelta(days=30),
            "time_frame_str": "30d",
            "time_frame_display": "Last 30 days"
        }
    else:  # All time
        return {
            "published_after": None,
            "time_frame_str": "all",
            "time_frame_display": "All time"
        }

def save_data_to_json(data: List[Dict[str, Any]], filename: str, output_dir: str = "Output JSON") -> str:
    """
    Save data to a JSON file.

    Args:
        data: The data to save
        filename: The name of the file to save to
        output_dir: Directory to save the file in

    Returns:
        The path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the full filepath
    filepath = os.path.join(output_dir, filename)

    # Save the data to a JSON file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filepath

def sanitize_query(query: str) -> str:
    """
    Sanitize a query string for use in filenames.

    Args:
        query: The query string to sanitize

    Returns:
        Sanitized query string
    """
    return query.replace(" ", "_").replace("/", "_").replace("\\", "_")

def search_platform(platform: str, query: str, time_frame: int = 4, output_dir: str = "Output JSON") -> None:
    """
    Generic function to search a platform and save results.

    Args:
        platform: Platform name ('youtube', 'instagram', or 'tiktok')
        query: Search query
        time_frame: Time frame code (1: last 24 hours, 2: last week, 3: last 30 days, 4: all time)
        output_dir: Directory to save output files
    """
    try:
        # Initialize the appropriate API client
        if platform == "youtube":
            api = YouTubeAPI()
            time_frame_info = get_time_frame_info(time_frame)
            published_after = time_frame_info["published_after"]
            time_frame_display = time_frame_info["time_frame_display"]
            time_frame_str = time_frame_info["time_frame_str"]

            print_title(f"YouTube Search: {query}")
            print_info(f"Time frame: {time_frame_display}")

            # Search for videos with spinner animation
            results = run_with_spinner(
                api.search_videos,
                f"Searching YouTube for '{query}'...",
                "youtube",  # Platform-specific styling
                query=query,
                max_results=50,
                published_after=published_after
            )

            if not results:
                print_warning(f"No videos found for query: {query}")
                return

            # Save results to JSON
            query_safe = sanitize_query(query)
            filename = f"youtube_search_{query_safe}_{time_frame_str}.json"
            json_file = save_data_to_json(results, filename, output_dir)

            # Export to CSV
            csv_filename = filename.replace('.json', '.csv')
            csv_file = export_youtube_data_to_csv(results, csv_filename)

            # Display success messages
            print_success(f"Found {len(results)} videos")
            print_info(f"JSON saved to {json_file}")
            print_info(f"CSV saved to {csv_file}")

            # Display results in a table
            display_youtube_videos(
                results,
                f"YouTube Search Results: {query} ({time_frame_display})"
            )

        elif platform == "instagram":
            api = InstagramAPI()

            print_title(f"Instagram Search: {query}")

            # Search for reels with spinner animation
            results = run_with_spinner(
                api.get_formatted_search_reels,
                f"Searching Instagram for '{query}'...",
                "instagram",  # Platform-specific styling
                query
            )

            if not results:
                print_warning(f"No reels found for query: {query}")
                return

            # Save results to JSON
            query_safe = sanitize_query(query)
            filename = f"instagram_search_{query_safe}.json"
            json_file = save_data_to_json(results, filename, output_dir)

            # Export to CSV
            csv_filename = filename.replace('.json', '.csv')
            csv_file = export_instagram_data_to_csv(results, csv_filename)

            # Display success messages
            print_success(f"Found {len(results)} reels")
            print_info(f"JSON saved to {json_file}")
            print_info(f"CSV saved to {csv_file}")

            # Display results in a table
            display_instagram_reels(
                results,
                f"Instagram Search Results: {query}"
            )

        elif platform == "tiktok":
            api = TikTokAPI()

            print_title(f"TikTok Search: {query}")

            # Search for videos with spinner animation
            results = run_with_spinner(
                api.get_formatted_search_videos,
                f"Searching TikTok for '{query}'...",
                "tiktok",  # Platform-specific styling
                query
            )

            if not results:
                print_warning(f"No videos found for query: {query}")
                return

            # Save results to JSON
            query_safe = sanitize_query(query)
            filename = f"tiktok_search_{query_safe}.json"
            json_file = save_data_to_json(results, filename, output_dir)

            # Export to CSV
            csv_filename = filename.replace('.json', '.csv')
            csv_file = export_tiktok_data_to_csv(results, csv_filename)

            # Display success messages
            print_success(f"Found {len(results)} videos")
            print_info(f"JSON saved to {json_file}")
            print_info(f"CSV saved to {csv_file}")

            # Display results in a table
            display_tiktok_videos(
                results,
                f"TikTok Search Results: {query}"
            )

        else:
            print_error(f"Unsupported platform: {platform}")

    except Exception as e:
        print_error(f"Error searching {platform}: {str(e)}")
        raise

def process_platform_accounts(platform: str, accounts: List[str], time_frame: int = 4, output_dir: str = "Output JSON") -> None:
    """
    Generic function to process accounts for a specific platform.

    Args:
        platform: Platform name ('youtube', 'instagram', or 'tiktok')
        accounts: List of account names
        time_frame: Time frame code (1: last 24 hours, 2: last week, 3: last 30 days, 4: all time)
        output_dir: Directory to save output files
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get time frame information
        time_frame_info = get_time_frame_info(time_frame)
        published_after = time_frame_info["published_after"]
        time_frame_display = time_frame_info["time_frame_display"]

        if platform == "youtube":
            api = YouTubeAPI()

            print_title(f"YouTube Competitor Analysis ({time_frame_display})")
            print_info(f"Processing {len(accounts)} YouTube accounts")

            for account in accounts:
                print_subtitle(f"Processing YouTube account: {account}")

                # Get channel ID with spinner animation
                channel_id = run_with_spinner(
                    api.get_channel_id,
                    f"Finding channel ID for {account}...",
                    "youtube",  # Platform-specific styling
                    account
                )
                if not channel_id:
                    print_error(f"Could not find channel ID for {account}")
                    continue

                # Get channel info with spinner animation
                channel_info = run_with_spinner(
                    api.get_channel_info,
                    f"Fetching channel info for {account}...",
                    "youtube",  # Platform-specific styling
                    channel_id
                )
                if not channel_info:
                    print_error(f"Could not get channel info for {account}")
                    continue

                # Display channel info in a panel
                from terminal_ui import print_panel
                channel_panel_text = (
                    f"Channel: {channel_info['title']}\n"
                    f"Subscribers: {int(channel_info.get('subscriberCount', 0)):,}\n"
                    f"Total Videos: {int(channel_info.get('videoCount', 0)):,}\n"
                    f"Total Views: {int(channel_info.get('viewCount', 0)):,}\n"
                    f"Created: {channel_info['publishedAt'].split('T')[0]}"
                )
                print_panel(channel_panel_text, title=f"Channel Info: {account}")

                # Save channel info to JSON
                filename = f"youtube_{account}_channel.json"
                json_file = save_data_to_json(channel_info, filename, output_dir)
                print_info(f"Channel info saved to {json_file}")

                # Get recent videos with spinner animation
                videos = run_with_spinner(
                    api.get_channel_videos,
                    f"Fetching videos for {account}...",
                    "youtube",  # Platform-specific styling
                    channel_id,
                    max_results=50,
                    published_after=published_after
                )

                if not videos:
                    print_warning(f"No videos found for {account} in the selected time frame")
                    continue

                # Save videos info to JSON
                filename = f"youtube_{account}_videos.json"
                json_file = save_data_to_json(videos, filename, output_dir)

                # Export to CSV
                csv_filename = filename.replace('.json', '.csv')
                csv_file = export_youtube_data_to_csv(videos, csv_filename)

                print_success(f"Found {len(videos)} videos")
                print_info(f"JSON saved to {json_file}")
                print_info(f"CSV saved to {csv_file}")

                # Display videos in a table
                display_youtube_videos(
                    videos,
                    f"Videos from {account} ({time_frame_display})"
                )

        elif platform == "instagram":
            api = InstagramAPI()

            print_title(f"Instagram Competitor Analysis")
            print_info(f"Processing {len(accounts)} Instagram accounts")

            for account in accounts:
                print_subtitle(f"Processing Instagram account: {account}")

                # Get user reels with spinner animation
                reels = run_with_spinner(
                    api.get_formatted_user_reels,
                    f"Fetching reels for {account}...",
                    "instagram",  # Platform-specific styling
                    account
                )

                if not reels:
                    print_warning(f"No reels found for {account}")
                    continue

                # Save reels info to JSON
                filename = f"instagram_{account}_reels.json"
                json_file = save_data_to_json(reels, filename, output_dir)

                # Export to CSV
                csv_filename = filename.replace('.json', '.csv')
                csv_file = export_instagram_data_to_csv(reels, csv_filename)

                print_success(f"Found {len(reels)} reels")
                print_info(f"JSON saved to {json_file}")
                print_info(f"CSV saved to {csv_file}")

                # Display reels in a table
                display_instagram_reels(
                    reels,
                    f"Reels from {account}"
                )

        elif platform == "tiktok":
            api = TikTokAPI()

            print_title(f"TikTok Competitor Analysis")
            print_info(f"Processing {len(accounts)} TikTok accounts")

            # Add a 2-second delay between API requests to avoid rate limits
            import time
            for i, account in enumerate(accounts):
                if i > 0:
                    print_info("Waiting 2 seconds before next request to avoid rate limits...")
                    time.sleep(2)

                print_subtitle(f"Processing TikTok account: {account}")

                # Get user videos with spinner animation
                videos = run_with_spinner(
                    api.get_formatted_user_videos,
                    f"Fetching videos for {account}...",
                    "tiktok",  # Platform-specific styling
                    account
                )

                if not videos:
                    print_warning(f"No videos found for {account}")
                    continue

                # Save videos info to JSON
                filename = f"tiktok_{account}_videos.json"
                json_file = save_data_to_json(videos, filename, output_dir)

                # Export to CSV
                csv_filename = filename.replace('.json', '.csv')
                csv_file = export_tiktok_data_to_csv(videos, csv_filename)

                print_success(f"Found {len(videos)} videos")
                print_info(f"JSON saved to {json_file}")
                print_info(f"CSV saved to {csv_file}")

                # Display videos in a table
                display_tiktok_videos(
                    videos,
                    f"Videos from {account}"
                )

        else:
            print_error(f"Unsupported platform: {platform}")

    except Exception as e:
        print_error(f"Error processing {platform} accounts: {str(e)}")
        raise
