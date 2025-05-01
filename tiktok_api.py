"""
TikTok API Module for SocialSpyAgent.

This module provides functions to interact with the TikTok API
via RapidAPI to fetch information about TikTok users and videos.
"""

import datetime
from typing import Dict, List, Any
import requests
from base_api import BaseAPI

class TikTokAPI(BaseAPI):
    """Class to interact with the TikTok API via RapidAPI."""

    def __init__(self):
        """
        Initialize the TikTok API client.

        Raises:
            ValueError: If the RapidAPI key is not found in environment variables.
        """
        super().__init__(
            api_key_env_var="RAPIDAPI_KEY",
            base_url="https://tiktok-api6.p.rapidapi.com",
            host="tiktok-api6.p.rapidapi.com"
        )

    def get_user_videos(self, username: str) -> Dict[str, Any]:
        """
        Get videos for a specific TikTok user.

        Args:
            username: The TikTok username.

        Returns:
            A dictionary containing the user's videos data.

        Raises:
            requests.RequestException: If there's an error with the API request.
        """
        url = f"{self.base_url}/user/videos"
        querystring = {"username": username}

        try:
            response = requests.get(url, headers=self.headers, params=querystring)

            # Check if we got a successful response
            if response.status_code == 200:
                return response.json()
            else:
                return self.handle_api_error(response)

        except requests.RequestException as e:
            return {"error": str(e)}

    def search_videos(self, query: str) -> Dict[str, Any]:
        """
        Search for TikTok videos using a query.

        Args:
            query: The search query.

        Returns:
            A dictionary containing the search results.

        Raises:
            requests.RequestException: If there's an error with the API request.
        """
        url = f"{self.base_url}/search/general/query"
        querystring = {"query": query}

        try:
            response = requests.get(url, headers=self.headers, params=querystring)

            # Check if we got a successful response
            if response.status_code == 200:
                return response.json()
            else:
                return self.handle_api_error(response)

        except requests.RequestException as e:
            return {"error": str(e)}

    def extract_video_data(self, video: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data from TikTok video API response.

        Args:
            video: Raw video data from the API response

        Returns:
            Dictionary with extracted data
        """
        # Initialize with default values for the fields we want to extract
        extracted_data = {
            "username": "",
            "caption": "",
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "views": 0,
            "url": "",
            "upload_date": "",
            "engagement_rate": 0.0
        }

        # Extract username (could be in different fields based on endpoint)
        if "author" in video and isinstance(video["author"], dict) and "uniqueId" in video["author"]:
            extracted_data["username"] = video["author"]["uniqueId"]
        elif "author" in video and isinstance(video["author"], dict) and "username" in video["author"]:
            extracted_data["username"] = video["author"]["username"]
        elif "author" in video and isinstance(video["author"], str):
            extracted_data["username"] = video["author"]
        elif "authorMeta" in video and "name" in video["authorMeta"]:
            extracted_data["username"] = video["authorMeta"]["name"]
        elif "username" in video:
            extracted_data["username"] = video["username"]

        # Extract caption/description
        if "description" in video:
            extracted_data["caption"] = video["description"]
        elif "desc" in video:
            extracted_data["caption"] = video["desc"]
        elif "text" in video:
            extracted_data["caption"] = video["text"]

        # Extract likes
        if "statistics" in video and "number_of_hearts" in video["statistics"]:
            extracted_data["likes"] = video["statistics"]["number_of_hearts"]
        elif "stats" in video and "diggCount" in video["stats"]:
            extracted_data["likes"] = video["stats"]["diggCount"]
        elif "stats" in video and "likes" in video["stats"]:
            extracted_data["likes"] = video["stats"]["likes"]
        elif "diggCount" in video:
            extracted_data["likes"] = video["diggCount"]
        elif "likes" in video:
            extracted_data["likes"] = video["likes"]

        # Extract comments
        if "statistics" in video and "number_of_comments" in video["statistics"]:
            extracted_data["comments"] = video["statistics"]["number_of_comments"]
        elif "stats" in video and "commentCount" in video["stats"]:
            extracted_data["comments"] = video["stats"]["commentCount"]
        elif "stats" in video and "comments" in video["stats"]:
            extracted_data["comments"] = video["stats"]["comments"]
        elif "commentCount" in video:
            extracted_data["comments"] = video["commentCount"]
        elif "comments" in video:
            extracted_data["comments"] = video["comments"]

        # Extract shares
        if "statistics" in video and "number_of_reposts" in video["statistics"]:
            extracted_data["shares"] = video["statistics"]["number_of_reposts"]
        elif "stats" in video and "shareCount" in video["stats"]:
            extracted_data["shares"] = video["stats"]["shareCount"]
        elif "stats" in video and "shares" in video["stats"]:
            extracted_data["shares"] = video["stats"]["shares"]
        elif "shareCount" in video:
            extracted_data["shares"] = video["shareCount"]
        elif "shares" in video:
            extracted_data["shares"] = video["shares"]

        # Extract views
        if "statistics" in video and "number_of_plays" in video["statistics"]:
            extracted_data["views"] = video["statistics"]["number_of_plays"]
        elif "stats" in video and "playCount" in video["stats"]:
            extracted_data["views"] = video["stats"]["playCount"]
        elif "stats" in video and "views" in video["stats"]:
            extracted_data["views"] = video["stats"]["views"]
        elif "playCount" in video:
            extracted_data["views"] = video["playCount"]
        elif "views" in video:
            extracted_data["views"] = video["views"]

        # Extract URL
        if "download_url" in video:
            extracted_data["url"] = video["download_url"]
        elif "video" in video and "playAddr" in video["video"]:
            extracted_data["url"] = video["video"]["playAddr"]
        elif "webVideoUrl" in video:
            extracted_data["url"] = video["webVideoUrl"]
        elif "shareUrl" in video:
            extracted_data["url"] = video["shareUrl"]
        elif "video_id" in video:
            # Construct URL from ID if direct URL not available
            extracted_data["url"] = f"https://www.tiktok.com/@{extracted_data['username']}/video/{video['video_id']}"
        elif "id" in video:
            # Construct URL from ID if direct URL not available
            extracted_data["url"] = f"https://www.tiktok.com/@{extracted_data['username']}/video/{video['id']}"

        # Extract upload date
        if "create_time" in video:
            # Convert timestamp to ISO format
            try:
                timestamp = int(video["create_time"])
                date_obj = datetime.datetime.fromtimestamp(timestamp)
                extracted_data["upload_date"] = date_obj.isoformat()
            except (ValueError, TypeError):
                pass
        elif "createTime" in video:
            # Convert timestamp to ISO format
            try:
                timestamp = int(video["createTime"])
                date_obj = datetime.datetime.fromtimestamp(timestamp)
                extracted_data["upload_date"] = date_obj.isoformat()
            except (ValueError, TypeError):
                pass
        elif "createTimeISO" in video:
            extracted_data["upload_date"] = video["createTimeISO"]

        # Calculate engagement rate
        # Formula: (likes + comments + shares) / views * 100
        if extracted_data["views"] > 0:
            engagement = (
                extracted_data["likes"] +
                extracted_data["comments"] +
                extracted_data["shares"]
            )
            extracted_data["engagement_rate"] = round((engagement / extracted_data["views"]) * 100, 2)

        return extracted_data

    def process_user_videos(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the user videos API response and extract relevant data.

        Args:
            response_data: Raw API response data

        Returns:
            List of dictionaries with extracted data
        """
        extracted_videos = []

        # Check if there's an error
        if "error" in response_data:
            return extracted_videos

        # Based on the actual API response structure
        if "videos" in response_data and isinstance(response_data["videos"], list):
            videos = response_data["videos"]
            for video in videos:
                # Add author information to the video object
                if "author" not in video and "author_name" in response_data:
                    video["author"] = response_data["author_name"]

                # Add username if available at the top level
                if "username" in response_data:
                    video["username"] = response_data["username"]

                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)
        elif "data" in response_data and isinstance(response_data["data"], list):
            videos = response_data["data"]
            for video in videos:
                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)
        elif "itemList" in response_data and isinstance(response_data["itemList"], list):
            videos = response_data["itemList"]
            for video in videos:
                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)

        return extracted_videos

    def process_search_videos(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the search videos API response and extract relevant data.

        Args:
            response_data: Raw API response data

        Returns:
            List of dictionaries with extracted data
        """
        extracted_videos = []

        # Check if there's an error
        if "error" in response_data:
            return extracted_videos

        # Based on the actual API response structure
        if "videos" in response_data and isinstance(response_data["videos"], list):
            videos = response_data["videos"]
            for video in videos:
                # Process author information if it exists
                if "author" in video and isinstance(video["author"], dict):
                    if "uniqueId" in video["author"]:
                        video["username"] = video["author"]["uniqueId"]

                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)
        elif "data" in response_data and "videos" in response_data["data"] and isinstance(response_data["data"]["videos"], list):
            videos = response_data["data"]["videos"]
            for video in videos:
                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)
        elif "data" in response_data and isinstance(response_data["data"], list):
            videos = response_data["data"]
            for video in videos:
                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)
        elif "itemList" in response_data and isinstance(response_data["itemList"], list):
            videos = response_data["itemList"]
            for video in videos:
                extracted_video = self.extract_video_data(video)
                extracted_videos.append(extracted_video)

        return extracted_videos

    def get_formatted_user_videos(self, username: str) -> List[Dict[str, Any]]:
        """
        Get and format videos for a specific TikTok user.

        Args:
            username: The TikTok username.

        Returns:
            List of dictionaries with formatted video data.
        """
        response_data = self.get_user_videos(username)
        return self.process_user_videos(response_data)

    def get_formatted_search_videos(self, query: str) -> List[Dict[str, Any]]:
        """
        Search and format TikTok videos using a query.

        Args:
            query: The search query.

        Returns:
            List of dictionaries with formatted video data.
        """
        response_data = self.search_videos(query)
        return self.process_search_videos(response_data)

    # Using save_data_to_json from BaseAPI


def main():
    """Main function to demonstrate the TikTok API functionality."""
    import os  # Import here for the demo function only

    try:
        # Initialize TikTok API
        tiktok_api = TikTokAPI()

        # Create output directory if it doesn't exist
        os.makedirs("Output JSON", exist_ok=True)

        # Example 1: Get user videos
        print("\nExample 1: Get user videos for 'mrbeast'")
        user_videos = tiktok_api.get_formatted_user_videos("mrbeast")
        if user_videos:
            print(f"Found {len(user_videos)} videos")
            filepath = tiktok_api.save_data_to_json(user_videos, "tiktok_mrbeast_videos")
            print(f"Data saved to {filepath}")

            # Display sample data
            if user_videos:
                print("\nSample video data:")
                sample = user_videos[0]
                for key, value in sample.items():
                    if key == "url":
                        print(f"  {key}: {value[:100]}...")  # Truncate long URLs
                    else:
                        print(f"  {key}: {value}")
        else:
            print("No videos found or API error occurred")

        # Example 2: Search videos
        print("\nExample 2: Search videos for 'mr beast'")
        search_videos = tiktok_api.get_formatted_search_videos("mr beast")
        if search_videos:
            print(f"Found {len(search_videos)} videos")
            filepath = tiktok_api.save_data_to_json(search_videos, "tiktok_search_mr_beast")
            print(f"Data saved to {filepath}")

            # Display sample data
            if search_videos:
                print("\nSample search result:")
                sample = search_videos[0]
                for key, value in sample.items():
                    if key == "url":
                        print(f"  {key}: {value[:100]}...")  # Truncate long URLs
                    else:
                        print(f"  {key}: {value}")
        else:
            print("No videos found or API error occurred")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
