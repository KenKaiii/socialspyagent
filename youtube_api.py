"""
YouTube Data API Module for SocialSpyAgent.

This module provides functions to interact with the YouTube Data API
to fetch information about YouTube channels and videos.
"""

import json
import datetime
from typing import Dict, List, Optional, Any
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from tqdm import tqdm
from base_api import BaseAPI

class YouTubeAPI(BaseAPI):
    """Class to interact with the YouTube Data API."""

    def __init__(self):
        """
        Initialize the YouTube API client.

        Raises:
            ValueError: If the Google API key is not found in environment variables.
        """
        # Initialize the base API with the Google API key
        super().__init__(
            api_key_env_var="GOOGLE_API_KEY",
            base_url="https://www.googleapis.com/youtube/v3",
            host=None
        )

        # Build the YouTube API client
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.api_key
        )

    def get_channel_id(self, username: str) -> Optional[str]:
        """
        Get the channel ID for a given YouTube username.

        Args:
            username: The YouTube username or channel name.

        Returns:
            The channel ID if found, None otherwise.

        Raises:
            HttpError: If there's an error with the API request.
        """
        try:
            # First try to search for the channel
            search_response = self.youtube.search().list(
                q=username,
                type="channel",
                part="id,snippet",
                maxResults=1
            ).execute()

            if search_response.get("items"):
                return search_response["items"][0]["id"]["channelId"]

            # If not found, try to get by username
            channels_response = self.youtube.channels().list(
                forUsername=username,
                part="id"
            ).execute()

            if channels_response.get("items"):
                return channels_response["items"][0]["id"]

            return None

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return None

    def get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a YouTube channel.

        Args:
            channel_id: The YouTube channel ID.

        Returns:
            A dictionary containing channel information if found, None otherwise.

        Raises:
            HttpError: If there's an error with the API request.
        """
        try:
            channel_response = self.youtube.channels().list(
                id=channel_id,
                part="snippet,statistics,contentDetails"
            ).execute()

            if not channel_response.get("items"):
                return None

            channel_data = channel_response["items"][0]

            return {
                "id": channel_data["id"],
                "title": channel_data["snippet"]["title"],
                "description": channel_data["snippet"]["description"],
                "customUrl": channel_data["snippet"].get("customUrl"),
                "publishedAt": channel_data["snippet"]["publishedAt"],
                "thumbnails": channel_data["snippet"]["thumbnails"],
                "country": channel_data["snippet"].get("country"),
                "viewCount": channel_data["statistics"].get("viewCount"),
                "subscriberCount": channel_data["statistics"].get("subscriberCount"),
                "videoCount": channel_data["statistics"].get("videoCount"),
                "uploadsPlaylistId": channel_data["contentDetails"]["relatedPlaylists"]["uploads"]
            }

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return None

    def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 10,
        published_after: Optional[datetime.datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get videos from a YouTube channel.

        Args:
            channel_id: The YouTube channel ID.
            max_results: Maximum number of videos to return (capped at 50).
            published_after: Only return videos published after this date.

        Returns:
            A list of dictionaries containing video information.

        Raises:
            HttpError: If there's an error with the API request.
        """
        try:
            # Ensure max_results doesn't exceed 50 to avoid pagination
            max_results = min(50, max_results)

            # First get the channel information including title and uploads playlist ID
            channel_response = self.youtube.channels().list(
                id=channel_id,
                part="snippet,contentDetails",
                fields="items(snippet(title),contentDetails(relatedPlaylists(uploads)))"  # Request title and uploads playlist
            ).execute()

            if not channel_response.get("items"):
                print(f"No channel found with ID: {channel_id}")
                return []

            channel_title = channel_response["items"][0]["snippet"]["title"]
            uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            # Get videos from the uploads playlist in a single request
            playlist_response = self.youtube.playlistItems().list(
                playlistId=uploads_playlist_id,
                part="contentDetails",
                maxResults=max_results,
                fields="items(contentDetails(videoId))"  # Only request video IDs
            ).execute()

            if not playlist_response.get("items"):
                print(f"No videos found in channel: {channel_id}")
                return []

            # Extract video IDs
            video_ids = [item["contentDetails"]["videoId"] for item in playlist_response.get("items", [])]

            # Get video details in a single request
            video_response = self.youtube.videos().list(
                id=','.join(video_ids),
                part="snippet,statistics",  # Only request the parts we need
                maxResults=max_results
            ).execute()

            # Process video details
            videos = []
            for video_data in video_response.get("items", []):
                # Check publication date if needed
                if published_after:
                    # Parse the video publication date
                    video_published_at = datetime.datetime.strptime(
                        video_data["snippet"]["publishedAt"],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )

                    # Make the video_published_at timezone-aware by adding UTC timezone
                    video_published_at = video_published_at.replace(tzinfo=datetime.timezone.utc)

                    # Now compare the timezone-aware datetimes
                    if video_published_at < published_after:
                        continue

                # Get view count and convert to integer
                view_count = video_data["statistics"].get("viewCount", "0")
                view_count = int(view_count) if view_count.isdigit() else 0

                # Create video URL
                video_url = f"https://www.youtube.com/watch?v={video_data['id']}"

                videos.append({
                    "channelTitle": channel_title,
                    "title": video_data["snippet"]["title"],
                    "viewCount": view_count,
                    "likeCount": int(video_data["statistics"].get("likeCount", "0")) if video_data["statistics"].get("likeCount", "").isdigit() else 0,
                    "commentCount": int(video_data["statistics"].get("commentCount", "0")) if video_data["statistics"].get("commentCount", "").isdigit() else 0,
                    "publishedAt": video_data["snippet"]["publishedAt"],
                    "url": video_url
                })

            return videos

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []

    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Get comments for a YouTube video.

        Args:
            video_id: The YouTube video ID.
            max_results: Maximum number of comments to return.

        Returns:
            A list of dictionaries containing comment information.

        Raises:
            HttpError: If there's an error with the API request.
        """
        try:
            comments = []
            next_page_token = None

            with tqdm(total=max_results, desc="Fetching comments") as pbar:
                while len(comments) < max_results:
                    comments_response = self.youtube.commentThreads().list(
                        videoId=video_id,
                        part="snippet",
                        maxResults=min(100, max_results - len(comments)),
                        pageToken=next_page_token
                    ).execute()

                    if not comments_response.get("items"):
                        break

                    for item in comments_response["items"]:
                        comment = item["snippet"]["topLevelComment"]["snippet"]

                        comments.append({
                            "id": item["id"],
                            "authorDisplayName": comment["authorDisplayName"],
                            "authorProfileImageUrl": comment["authorProfileImageUrl"],
                            "authorChannelUrl": comment["authorChannelUrl"],
                            "textDisplay": comment["textDisplay"],
                            "textOriginal": comment["textOriginal"],
                            "likeCount": comment["likeCount"],
                            "publishedAt": comment["publishedAt"],
                            "updatedAt": comment["updatedAt"]
                        })

                        pbar.update(1)

                        if len(comments) >= max_results:
                            break

                    next_page_token = comments_response.get("nextPageToken")
                    if not next_page_token:
                        break

            return comments

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []

    def search_videos(self, query: str, max_results: int = 50, published_after: Optional[datetime.datetime] = None) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos based on a query.

        Args:
            query: The search query.
            max_results: Maximum number of videos to return (capped at 50).
            published_after: Only return videos published after this date.

        Returns:
            A list of dictionaries containing video information.

        Raises:
            HttpError: If there's an error with the API request.
        """
        try:
            # Ensure max_results doesn't exceed 50 to avoid pagination
            max_results = min(50, max_results)

            # Set up published_after parameter if provided
            published_after_str = None
            if published_after:
                published_after_str = published_after.strftime('%Y-%m-%dT%H:%M:%SZ')

            # Set up search parameters
            search_params = {
                'q': query,
                'type': 'video',
                'part': 'snippet',
                'maxResults': max_results,
                'order': 'relevance',
                'fields': 'items(id(videoId),snippet(channelTitle))'  # Request video IDs and channel titles
            }

            if published_after_str:
                search_params['publishedAfter'] = published_after_str

            # Make a single search request
            search_response = self.youtube.search().list(**search_params).execute()

            if not search_response.get("items"):
                print("No videos found matching the search criteria.")
                return []

            # Extract video IDs and channel titles
            search_items = search_response.get("items", [])
            video_ids = [item["id"]["videoId"] for item in search_items]

            # Create a mapping of video IDs to channel titles
            channel_titles = {item["id"]["videoId"]: item["snippet"]["channelTitle"]
                             for item in search_items if "snippet" in item and "channelTitle" in item["snippet"]}

            # Make a single request to get video details
            video_response = self.youtube.videos().list(
                id=','.join(video_ids),
                part="snippet,statistics",  # Only request the parts we need
                maxResults=max_results
            ).execute()

            # Process video details
            videos = []
            for video_data in video_response.get("items", []):
                # Get view count and convert to integer
                view_count = video_data["statistics"].get("viewCount", "0")
                view_count = int(view_count) if view_count.isdigit() else 0

                # Create video URL
                video_url = f"https://www.youtube.com/watch?v={video_data['id']}"

                # Get channel title from mapping or from video data
                channel_title = channel_titles.get(video_data['id'], video_data["snippet"].get("channelTitle", "Unknown Channel"))

                videos.append({
                    "channelTitle": channel_title,
                    "title": video_data["snippet"]["title"],
                    "viewCount": view_count,
                    "likeCount": int(video_data["statistics"].get("likeCount", "0")) if video_data["statistics"].get("likeCount", "").isdigit() else 0,
                    "commentCount": int(video_data["statistics"].get("commentCount", "0")) if video_data["statistics"].get("commentCount", "").isdigit() else 0,
                    "publishedAt": video_data["snippet"]["publishedAt"],
                    "url": video_url
                })

            return videos

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []


def main():
    """Main function to demonstrate the YouTube API functionality."""
    # Load config
    with open("config.json", "r") as f:
        config = json.load(f)

    youtube_accounts = config.get("youtube_accounts", [])

    if not youtube_accounts:
        print("No YouTube accounts found in config.json")
        return

    try:
        # Initialize YouTube API
        youtube_api = YouTubeAPI()

        for account in youtube_accounts:
            print(f"\nProcessing YouTube account: {account}")

            # Get channel ID
            channel_id = youtube_api.get_channel_id(account)
            if not channel_id:
                print(f"Could not find channel ID for {account}")
                continue

            print(f"Channel ID: {channel_id}")

            # Get channel info
            channel_info = youtube_api.get_channel_info(channel_id)
            if not channel_info:
                print(f"Could not get channel info for {account}")
                continue

            print(f"Channel: {channel_info['title']}")
            print(f"Subscribers: {channel_info.get('subscriberCount', 'N/A')}")
            print(f"Videos: {channel_info.get('videoCount', 'N/A')}")

            # Get recent videos
            print("\nFetching recent videos...")
            videos = youtube_api.get_channel_videos(
                channel_id,
                max_results=5,
                published_after=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)
            )

            for i, video in enumerate(videos, 1):
                print(f"\nVideo {i}:")
                print(f"Title: {video['title']}")
                print(f"URL: {video['url']}")
                print(f"Published: {video['publishedAt']}")
                print(f"Views: {video['viewCount']}")
                print(f"Likes: {video['likeCount']}")
                print(f"Comments: {video['commentCount']}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
