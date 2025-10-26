#!/usr/bin/env python3
"""
YouTube Video List Fetcher

This script queries the YouTube Data API to fetch a list of short videos
from a specific channel within the last year.

Dependencies managed with Poetry:
- google-api-python-client
- python-dotenv (for API key management)

Usage:
    poetry run python services/01_url_pull/main.py
    # or after poetry install:
    poetry run youtube-fetch

Setup:
    poetry install

Author: Generated for video_poc project
Date: October 26, 2025
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict
import json

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: google-api-python-client is not installed.")
    print("Install dependencies with: poetry install")
    sys.exit(1)

# Optional: Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


class YouTubeVideoFetcher:
    """Handles fetching video data from YouTube Data API."""
    
    def __init__(self, api_key: str):
        """Initialize the YouTube API client.
        
        Args:
            api_key (str): YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the YouTube Data API client."""
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            print("✓ YouTube API client initialized successfully")
        except Exception as e:
            print(f"Error initializing YouTube API client: {e}")
            sys.exit(1)
    
    def _get_date_range(self) -> tuple[str, str]:
        """Get the date range for the last year in RFC 3339 format.
        
        Returns:
            tuple: (published_after, published_before) in RFC 3339 format
        """
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        
        # Convert to RFC 3339 format (ISO 8601 with timezone)
        published_before = today.strftime('%Y-%m-%dT%H:%M:%SZ')
        published_after = one_year_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        return published_after, published_before
    
    def fetch_videos(self, channel_id: str, max_results_per_page: int = 50) -> List[Dict]:
        """Fetch all short videos from the specified channel within the last year.
        
        Args:
            channel_id (str): YouTube channel ID
            max_results_per_page (int): Maximum results per API call (default: 50)
            
        Returns:
            List[Dict]: List of video data dictionaries
        """
        published_after, published_before = self._get_date_range()
        
        print(f"Fetching videos from channel: {channel_id}")
        print(f"Date range: {published_after} to {published_before}")
        print("Looking for short videos (< 4 minutes)")
        print("-" * 60)
        
        all_videos = []
        next_page_token = None
        page_count = 0
        
        while True:
            try:
                page_count += 1
                print(f"Fetching page {page_count}...")
                
                # Build request parameters
                request_params = {
                    'part': 'snippet',
                    'channelId': channel_id,
                    'publishedAfter': published_after,
                    'publishedBefore': published_before,
                    'videoDuration': 'short',
                    'type': 'video',
                    'maxResults': max_results_per_page,
                    'order': 'date'  # Order by upload date (newest first)
                }
                
                # Add page token if available
                if next_page_token:
                    request_params['pageToken'] = next_page_token
                
                # Execute the API request
                response = self.youtube.search().list(**request_params).execute()
                
                # Process the response
                items = response.get('items', [])
                page_videos = self._process_video_items(items)
                all_videos.extend(page_videos)
                
                print(f"  Found {len(page_videos)} videos on this page")
                print(f"  Total videos so far: {len(all_videos)}")
                
                # Check if there are more pages
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            except HttpError as e:
                print(f"An HTTP error occurred: {e}")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
        
        print("-" * 60)
        print(f"✓ Completed! Total videos fetched: {len(all_videos)}")
        return all_videos
    
    def _process_video_items(self, items: List[Dict]) -> List[Dict]:
        """Process video items from API response.
        
        Args:
            items (List[Dict]): Raw video items from API response
            
        Returns:
            List[Dict]: Processed video data
        """
        processed_videos = []
        
        for item in items:
            video_data = {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'channel_title': item['snippet']['channelTitle'],
                'thumbnail_url': item['snippet']['thumbnails'].get('default', {}).get('url', ''),
                'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            processed_videos.append(video_data)
        
        return processed_videos
    
    def save_to_json(self, videos: List[Dict], filename: str = 'youtube_videos.json') -> None:
        """Save video data to JSON file.
        
        Args:
            videos (List[Dict]): List of video data
            filename (str): Output filename (default: 'youtube_videos.json')
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=2, ensure_ascii=False)
            print(f"✓ Video data saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON file: {e}")
    
    def print_video_summary(self, videos: List[Dict]) -> None:
        """Print a summary of fetched videos.
        
        Args:
            videos (List[Dict]): List of video data
        """
        if not videos:
            print("No videos found.")
            return
        
        print("\n" + "=" * 80)
        print("VIDEO SUMMARY")
        print("=" * 80)
        
        for i, video in enumerate(videos, 1):
            print(f"\n{i:3d}. {video['title']}")
            print(f"     Video ID: {video['video_id']}")
            print(f"     Published: {video['published_at']}")
            print(f"     URL: {video['video_url']}")
        
        print("\n" + "=" * 80)


def main():
    """Main function to execute the video fetching process."""
    
    # Configuration
    CHANNEL_ID = "UC-tE4p-L9f0-w1T1-v8a-qA"
    
    # Get API key from environment variable or prompt user
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("YouTube Data API key not found in environment variables.")
        print("Please set the YOUTUBE_API_KEY environment variable or enter it below.")
        api_key = input("Enter your YouTube Data API key: ").strip()
        
        if not api_key:
            print("Error: API key is required to proceed.")
            sys.exit(1)
    
    try:
        # Initialize the fetcher
        fetcher = YouTubeVideoFetcher(api_key)
        
        # Fetch videos
        videos = fetcher.fetch_videos(CHANNEL_ID)
        
        if videos:
            # Print summary
            fetcher.print_video_summary(videos)
            
            # Save to JSON file
            fetcher.save_to_json(videos)
            
            # Print final statistics
            print(f"\n✓ Successfully fetched {len(videos)} short videos from the channel")
            print("✓ Data saved to youtube_videos.json")
        else:
            print("No videos found matching the criteria.")
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()