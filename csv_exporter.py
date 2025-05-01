"""
CSV export functionality for SocialSpyAgent.

This module provides functions to export data from various social media platforms to CSV format.
"""

import csv
import os
from typing import List, Dict, Any, Optional


def clean_text_for_csv(text: str) -> str:
    """
    Clean text for CSV export to prevent formatting issues.

    Args:
        text: The text to clean.

    Returns:
        Cleaned text suitable for CSV export.
    """
    if not text:
        return ""

    # Replace newlines with spaces
    text = text.replace('\n', ' ').replace('\r', ' ')

    # Replace problematic characters
    text = text.replace('\u2019', "'")  # Smart quotes
    text = text.replace('\u2018', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2026', '...')  # Ellipsis
    text = text.replace('\u2013', '-')  # En dash
    text = text.replace('\u2014', '-')  # Em dash

    # Remove emojis and other special characters that might cause issues
    text = ''.join(c for c in text if ord(c) < 65536)

    return text


def export_data_to_csv(data: List[Dict[str, Any]], filename: str, field_mapping: Dict[str, Any], output_dir: str = "Output CSV") -> str:
    """
    Generic function to export data to CSV.

    Args:
        data: List of dictionaries containing the data to export
        filename: Base filename to save (without path)
        field_mapping: Dictionary mapping CSV field names to data field names or transformation functions
        output_dir: Directory to save the CSV file

    Returns:
        Path to the saved CSV file
    """
    if not data:
        return ""

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the full filepath
    filepath = os.path.join(output_dir, filename)

    # Define CSV headers based on the field mapping
    fieldnames = list(field_mapping.keys())

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in data:
            # Create a row dictionary with cleaned text
            row = {}
            for csv_field, field_info in field_mapping.items():
                if isinstance(field_info, dict):
                    # Handle complex field mapping with transformations
                    field_name = field_info.get("field", "")
                    transform_func = field_info.get("transform")
                    default = field_info.get("default", "")

                    # Get the value from the data
                    value = item.get(field_name, default)

                    # Apply transformation if provided
                    if transform_func and callable(transform_func):
                        value = transform_func(value, item)
                    elif isinstance(value, str):
                        value = clean_text_for_csv(value)

                    row[csv_field] = value
                else:
                    # Simple field mapping (string)
                    value = item.get(field_info, "")
                    if isinstance(value, str):
                        value = clean_text_for_csv(value)
                    row[csv_field] = value

            writer.writerow(row)

    return filepath


def export_youtube_data_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Export YouTube data to CSV format.

    Args:
        data: List of YouTube video dictionaries.
        filename: Base filename to save (without path).

    Returns:
        Path to the saved CSV file.
    """
    # Define field mapping for YouTube data
    field_mapping = {
        'Channel': 'channelTitle',
        'Title': 'title',
        'Views': 'viewCount',
        'Likes': 'likeCount',
        'Comments': 'commentCount',
        'Engagement Rate (%)': {
            "field": "viewCount",
            "transform": lambda _, item: calculate_youtube_engagement(item)
        },
        'Published Date': {
            "field": "publishedAt",
            "transform": lambda date, _: date.split('T')[0] if date and 'T' in date else date
        },
        'URL': 'url'
    }

    return export_data_to_csv(data, filename, field_mapping)


def calculate_youtube_engagement(video: Dict[str, Any]) -> float:
    """Calculate engagement rate for YouTube videos."""
    view_count = video.get('viewCount', 0)
    like_count = video.get('likeCount', 0)
    comment_count = video.get('commentCount', 0)

    engagement_rate = 0
    if view_count > 0:
        engagement = like_count + comment_count
        engagement_rate = round((engagement / view_count) * 100, 2)

    return engagement_rate


def export_instagram_data_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Export Instagram data to CSV format.

    Args:
        data: List of Instagram reel dictionaries.
        filename: Base filename to save (without path).

    Returns:
        Path to the saved CSV file.
    """
    # Define field mapping for Instagram data
    field_mapping = {
        'Username': 'username',
        'Caption': 'caption',
        'Views': 'view_count',
        'Likes': 'like_count',
        'Comments': 'comment_count',
        'Engagement Rate (%)': 'engagement_rate',
        'Upload Date': 'upload_date',
        'URL': 'url'
    }

    return export_data_to_csv(data, filename, field_mapping)


def export_tiktok_data_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Export TikTok data to CSV format.

    Args:
        data: List of TikTok video dictionaries.
        filename: Base filename to save (without path).

    Returns:
        Path to the saved CSV file.
    """
    # Define field mapping for TikTok data
    field_mapping = {
        'Username': 'username',
        'Caption': 'caption',
        'Views': 'views',
        'Likes': 'likes',
        'Comments': 'comments',
        'Shares': 'shares',
        'Engagement Rate (%)': 'engagement_rate',
        'Upload Date': 'upload_date',
        'URL': 'url'
    }

    return export_data_to_csv(data, filename, field_mapping)


def json_to_csv(json_filepath: str, platform: str) -> Optional[str]:
    """
    Convert a JSON file to CSV format.

    Args:
        json_filepath: Path to the JSON file.
        platform: The platform name ('youtube', 'instagram', or 'tiktok').

    Returns:
        Path to the created CSV file or None if conversion failed.
    """
    import json

    # Get just the filename without path
    filename = os.path.basename(json_filepath).replace('.json', '.csv')

    try:
        # Read JSON data
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Export to CSV based on platform
        if platform.lower() == 'youtube':
            return export_youtube_data_to_csv(data, filename)
        elif platform.lower() == 'instagram':
            return export_instagram_data_to_csv(data, filename)
        elif platform.lower() == 'tiktok':
            return export_tiktok_data_to_csv(data, filename)
        else:
            return None
    except Exception as e:
        print(f"Error converting JSON to CSV: {str(e)}")
        return None
