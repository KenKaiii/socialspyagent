"""
Instagram API Module for SocialSpyAgent.

This module provides functions to interact with the Instagram API
via RapidAPI to fetch information about Instagram users and reels.
"""

from typing import Dict, List, Any
import requests
from base_api import BaseAPI

class InstagramAPI(BaseAPI):
    """Class to interact with the Instagram API via RapidAPI."""

    def __init__(self):
        """
        Initialize the Instagram API client.

        Raises:
            ValueError: If the RapidAPI key is not found in environment variables.
        """
        super().__init__(
            api_key_env_var="RAPIDAPI_KEY",
            base_url="https://instagram360.p.rapidapi.com",
            host="instagram360.p.rapidapi.com"
        )

    def get_user_reels(self, username: str) -> Dict[str, Any]:
        """
        Get reels for a specific Instagram user.

        Args:
            username: The Instagram username.

        Returns:
            A dictionary containing the user's reels data.

        Raises:
            requests.RequestException: If there's an error with the API request.
        """
        url = f"{self.base_url}/userreels/"
        querystring = {"username_or_id": username}

        try:
            response = requests.get(url, headers=self.headers, params=querystring)

            # Check if we got a successful response
            if response.status_code == 200:
                return response.json()
            else:
                return self.handle_api_error(response)

        except requests.RequestException as e:
            return {"error": str(e)}

    def search_reels(self, keyword: str) -> Dict[str, Any]:
        """
        Search for reels using a keyword.

        Args:
            keyword: The search keyword.

        Returns:
            A dictionary containing the search results.

        Raises:
            requests.RequestException: If there's an error with the API request.
        """
        url = f"{self.base_url}/searchreels/"
        querystring = {"keyword": keyword}

        try:
            response = requests.get(url, headers=self.headers, params=querystring)

            # Check if we got a successful response
            if response.status_code == 200:
                return response.json()
            else:
                return self.handle_api_error(response)

        except requests.RequestException as e:

            return {"error": str(e)}

    def extract_reel_data(self, reel: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data from Instagram reel API response.

        Args:
            reel: Raw reel data from the API response

        Returns:
            Dictionary with extracted data
        """
        # Initialize with default values
        extracted_data = {
            "username": "",
            "caption": "",
            "view_count": 0,
            "like_count": 0,
            "share_count": 0,
            "comment_count": 0,
            "url": "",
            "upload_date": "",
            "engagement_rate": 0.0
        }

        # Extract username
        if "user" in reel and "username" in reel["user"]:
            extracted_data["username"] = reel["user"]["username"]

        # Extract caption
        if "caption" in reel and reel["caption"] is not None and "text" in reel["caption"]:
            extracted_data["caption"] = reel["caption"]["text"]

        # Extract view count (could be in different fields)
        if "play_count" in reel:
            extracted_data["view_count"] = reel["play_count"]
        elif "ig_play_count" in reel:
            extracted_data["view_count"] = reel["ig_play_count"]

        # Extract like count
        if "like_count" in reel:
            extracted_data["like_count"] = reel["like_count"]

        # Extract share count
        if "reshare_count" in reel:
            extracted_data["share_count"] = reel["reshare_count"]
        elif "share_count" in reel:
            extracted_data["share_count"] = reel["share_count"]

        # Extract comment count
        if "comment_count" in reel:
            extracted_data["comment_count"] = reel["comment_count"]

        # Construct URL from code
        if "code" in reel:
            extracted_data["url"] = f"https://www.instagram.com/reel/{reel['code']}/"

        # Extract upload date
        if "taken_at_date" in reel:
            extracted_data["upload_date"] = reel["taken_at_date"]

        # Calculate engagement rate
        # Formula: (likes + comments + shares) / views * 100
        if extracted_data["view_count"] > 0:
            engagement = (
                extracted_data["like_count"] +
                extracted_data["comment_count"] +
                extracted_data["share_count"]
            )
            extracted_data["engagement_rate"] = round((engagement / extracted_data["view_count"]) * 100, 2)

        return extracted_data

    def process_user_reels(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the userreels API response and extract relevant data.

        Args:
            response_data: Raw API response data

        Returns:
            List of dictionaries with extracted data
        """
        extracted_reels = []

        # Check if there's an error
        if "error" in response_data:
            return extracted_reels

        # Check if the response has the expected structure
        if "data" in response_data and "items" in response_data["data"]:
            reels = response_data["data"]["items"]

            for reel in reels:
                extracted_reel = self.extract_reel_data(reel)
                extracted_reels.append(extracted_reel)

        return extracted_reels

    def process_search_reels(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the searchreels API response and extract relevant data.

        Args:
            response_data: Raw API response data

        Returns:
            List of dictionaries with extracted data
        """
        extracted_reels = []

        # Check if there's an error
        if "error" in response_data:
            return extracted_reels

        # Check if the response has the expected structure
        if "data" in response_data and "items" in response_data["data"]:
            reels = response_data["data"]["items"]

            for reel in reels:
                extracted_reel = self.extract_reel_data(reel)
                extracted_reels.append(extracted_reel)

        return extracted_reels

    def get_formatted_user_reels(self, username: str) -> List[Dict[str, Any]]:
        """
        Get and format reels for a specific Instagram user.

        Args:
            username: The Instagram username.

        Returns:
            List of dictionaries with formatted reel data.
        """
        response_data = self.get_user_reels(username)
        return self.process_user_reels(response_data)

    def get_formatted_search_reels(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search and format reels using a keyword.

        Args:
            keyword: The search keyword.

        Returns:
            List of dictionaries with formatted reel data.
        """
        response_data = self.search_reels(keyword)
        return self.process_search_reels(response_data)

    # Using save_data_to_json from BaseAPI
