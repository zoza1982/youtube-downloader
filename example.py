#!/usr/bin/env python3
"""Example usage of YouTube Downloader"""

from ytd.cli import main
import sys

if __name__ == '__main__':
    # Example 1: Download a video
    print("Example 1: Downloading a video...")
    sys.argv = ['ytd', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '-o', './downloads']
    # main()  # Uncomment to actually download
    
    # Example 2: Download audio only
    print("\nExample 2: Downloading audio only...")
    sys.argv = ['ytd', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '-a', '--audio-format', 'mp3']
    # main()  # Uncomment to actually download
    
    # Example 3: List formats
    print("\nExample 3: Listing available formats...")
    sys.argv = ['ytd', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '--list-formats']
    # main()  # Uncomment to list formats
    
    print("\nTo run these examples, uncomment the main() calls in the script!")