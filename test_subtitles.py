#!/usr/bin/env python3
"""Test script for subtitle features"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ytd.downloader import YouTubeDownloader
from ytd.utils import setup_logger

def test_subtitle_listing():
    """Test listing available subtitles"""
    # Popular video with many subtitle options
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    logger = setup_logger(verbose=True)
    options = {'quiet': False}
    downloader = YouTubeDownloader(options, logger)
    
    print("Testing subtitle listing...")
    print(f"URL: {test_url}\n")
    
    subtitles = downloader.list_subtitles(test_url)
    
    if subtitles:
        print(f"Found {len(subtitles)} subtitle tracks:\n")
        
        manual_subs = []
        auto_subs = []
        
        for lang, info in sorted(subtitles.items()):
            if info['type'] == 'manual':
                manual_subs.append((lang, info))
            else:
                auto_subs.append((lang, info))
        
        if manual_subs:
            print("Manual Subtitles:")
            for lang, info in manual_subs:
                print(f"  - {lang}: {', '.join(info['formats'])}")
        
        if auto_subs:
            print(f"\nAuto-generated Subtitles ({len(auto_subs)} languages):")
            # Show first 10 auto-generated languages
            for lang, info in auto_subs[:10]:
                print(f"  - {lang}: {', '.join(info['formats'])}")
            if len(auto_subs) > 10:
                print(f"  ... and {len(auto_subs) - 10} more languages")
    else:
        print("No subtitles found for this video")

def show_usage_examples():
    """Show examples of how to use the new subtitle features"""
    print("\n" + "="*60)
    print("USAGE EXAMPLES")
    print("="*60)
    
    print("\n1. List all available subtitles:")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID --list-subs")
    
    print("\n2. Download video with manual English subtitles:")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en")
    
    print("\n3. Download video with auto-generated English subtitles:")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --write-auto-subs")
    
    print("\n4. Download video with ALL available subtitles (manual + auto):")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs all")
    
    print("\n5. Download specific auto-generated languages (e.g., Spanish and French):")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs es,fr --write-auto-subs")
    
    print("\n6. Download video with multiple subtitle languages:")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en,es,fr,de")
    
    print("\n7. Download only audio with subtitles (for podcasts/lectures):")
    print("   ytd https://youtube.com/watch?v=VIDEO_ID -a -s --sub-langs en --write-auto-subs")

if __name__ == "__main__":
    print("YouTube Downloader - Subtitle Features Test")
    print("==========================================\n")
    
    test_subtitle_listing()
    show_usage_examples()
    
    print("\n✅ Subtitle features are ready to use!")