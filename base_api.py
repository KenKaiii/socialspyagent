"""
Base API Module for SocialSpyAgent.

This module provides a base class for all social media API clients.
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAPI:
    """Base class for all social media API clients."""
    
    def __init__(self, api_key_env_var: str, base_url: str, host: Optional[str] = None):
        """
        Initialize the API client with common parameters.
        
        Args:
            api_key_env_var: Environment variable name for the API key
            base_url: Base URL for the API
            host: Optional host name for the API
            
        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        self.api_key = os.getenv(api_key_env_var)
        if not self.api_key:
            raise ValueError(f"{api_key_env_var} not found. Please set it in .env file.")
        
        self.base_url = base_url
        self.headers = self._create_headers(host)
    
    def _create_headers(self, host: Optional[str] = None) -> Dict[str, str]:
        """
        Create headers for API requests.
        
        Args:
            host: Optional host name for the API
            
        Returns:
            Dictionary containing the headers for API requests
        """
        headers = {"x-rapidapi-key": self.api_key}
        if host:
            headers["x-rapidapi-host"] = host
        return headers
    
    def save_data_to_json(self, data: List[Dict[str, Any]], filename: str, output_dir: str = "Output JSON") -> str:
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
        
        # Create a timestamp for the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"{output_dir}/{filename}_{timestamp}.json"
        
        # Save the data to a JSON file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def handle_api_error(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API error responses.
        
        Args:
            response: The API response object
            
        Returns:
            Dictionary containing error information
        """
        error_info = ""
        try:
            error_info = response.json()
        except:
            error_info = response.text
        
        return {
            "error": f"API Error: {response.status_code}",
            "details": error_info
        }
