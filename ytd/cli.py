#!/usr/bin/env python3
"""Command-line interface for YouTube Downloader"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import validators
from colorama import init, Fore, Style

from .downloader import YouTubeDownloader
from .utils import setup_logger, load_config, merge_options
from . import __version__

init(autoreset=True)  # Initialize colorama


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='ytd',
        description='Download YouTube videos and playlists with ease',
        epilog='Example: ytd https://youtube.com/watch?v=VIDEO_ID -f best -o ~/Videos'
    )
    
    # Positional argument
    parser.add_argument(
        'url',
        nargs='?',  # Make URL optional for commands like --list-extractors
        help='Video or playlist URL (supports 1700+ sites including YouTube)'
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '-o', '--output',
        type=str,
        default='.',
        help='Output directory (default: current directory)'
    )
    output_group.add_argument(
        '--filename',
        type=str,
        help='Output filename template (default: video title)'
    )
    
    # Format options
    format_group = parser.add_argument_group('Format Options')
    format_group.add_argument(
        '-f', '--format',
        type=str,
        default='best',
        help='Video format/quality (default: best). Use --list-formats to see available formats'
    )
    format_group.add_argument(
        '-a', '--audio-only',
        action='store_true',
        help='Download audio only'
    )
    format_group.add_argument(
        '--audio-format',
        type=str,
        default='mp3',
        choices=['mp3', 'm4a', 'opus', 'vorbis', 'flac', 'wav'],
        help='Audio format for audio-only downloads (default: mp3)'
    )
    format_group.add_argument(
        '--list-formats',
        action='store_true',
        help='List all available formats for the video'
    )
    format_group.add_argument(
        '--list-subs',
        action='store_true',
        help='List all available subtitles (including auto-generated)'
    )
    
    # Download options
    download_group = parser.add_argument_group('Download Options')
    download_group.add_argument(
        '-p', '--playlist',
        action='store_true',
        help='Download entire playlist'
    )
    download_group.add_argument(
        '--playlist-items',
        type=str,
        help='Playlist items to download (e.g., "1-3,7,10-13")'
    )
    download_group.add_argument(
        '-s', '--subtitles',
        action='store_true',
        help='Download subtitles'
    )
    download_group.add_argument(
        '--sub-langs',
        type=str,
        default='en',
        help='Subtitle languages (comma-separated, default: en). Use "all" for all available subtitles'
    )
    download_group.add_argument(
        '--write-auto-subs',
        action='store_true',
        help='Download auto-generated subtitles (deprecated - auto-subs are now included by default)'
    )
    download_group.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip downloading the video/audio file (useful for downloading subtitles only)'
    )
    download_group.add_argument(
        '--convert-subs',
        type=str,
        choices=['srt', 'vtt', 'keep'],
        default='keep',
        help='Convert subtitles to specified format (default: keep original)'
    )
    download_group.add_argument(
        '-m', '--metadata',
        action='store_true',
        help='Embed metadata in the file'
    )
    download_group.add_argument(
        '--thumbnail',
        action='store_true',
        help='Embed thumbnail in the file'
    )
    download_group.add_argument(
        '-r', '--limit-rate',
        type=str,
        help='Limit download rate (e.g., 50K, 4M)'
    )
    download_group.add_argument(
        '--concurrent',
        type=int,
        default=3,
        help='Number of concurrent fragment downloads (default: 3)'
    )
    
    # Other options
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    other_group.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Enable quiet mode (minimal output)'
    )
    other_group.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    other_group.add_argument(
        '--update',
        action='store_true',
        help='Update yt-dlp to the latest version'
    )
    other_group.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress bar'
    )
    other_group.add_argument(
        '--archive',
        type=str,
        help='Download archive file to track already downloaded videos'
    )
    other_group.add_argument(
        '--cookies',
        type=str,
        help='Path to cookies file'
    )
    other_group.add_argument(
        '--list-extractors',
        action='store_true',
        help='List all supported video sites/extractors'
    )
    other_group.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser


def validate_url(url: str) -> bool:
    """Validate URL - now supports all sites that yt-dlp supports"""
    # Just check if it's a valid URL format
    # yt-dlp will handle checking if the site is supported
    return validators.url(url)


def print_error(message: str) -> None:
    """Print error message in red"""
    print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message in green"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print info message in blue"""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def main() -> int:
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(verbose=args.verbose, quiet=args.quiet)
    
    # Handle list extractors request (doesn't need URL)
    if args.list_extractors:
        import yt_dlp
        print_info("Supported video sites/extractors:")
        print("\nYt-dlp supports 1700+ websites including:")
        
        # Show some popular examples
        popular_sites = [
            "YouTube", "YouTube Playlists", "YouTube Shorts",
            "Twitter/X", "Facebook", "Instagram", "TikTok",
            "Vimeo", "Dailymotion", "Twitch", "Reddit",
            "SoundCloud", "Bandcamp", "Mixcloud",
            "BBC", "CNN", "TED", "Coursera", "Udemy",
            "pornhub", "xvideos", "PeerTube instances",
            "And 1700+ more sites!"
        ]
        
        for site in popular_sites:
            print(f"  • {site}")
        
        print("\nFor a complete list, run:")
        print("  yt-dlp --list-extractors")
        print("\nFor details about a specific site:")
        print("  yt-dlp --extractor-descriptions")
        return 0
    
    # Check if URL is required (not needed for some commands)
    if not args.url:
        print_error("URL is required")
        parser.print_help()
        return 1
    
    # Validate URL
    if not validate_url(args.url):
        print_error("Invalid URL format")
        return 1
    
    # Load configuration
    config = {}
    if args.config:
        config_path = Path(args.config)
        if config_path.exists():
            config = load_config(config_path)
        else:
            print_error(f"Configuration file not found: {args.config}")
            return 1
    
    # Merge command-line options with config
    options = merge_options(config, args)
    
    try:
        # Create downloader instance
        downloader = YouTubeDownloader(options, logger)
        
        # Handle update request
        if args.update:
            print_info("Updating yt-dlp...")
            if downloader.update():
                print_success("yt-dlp updated successfully")
            else:
                print_error("Failed to update yt-dlp")
            return 0
        
        # Handle list formats request
        if args.list_formats:
            print_info(f"Fetching available formats for: {args.url}")
            formats = downloader.list_formats(args.url)
            if formats:
                print("\nAvailable formats:")
                for fmt in formats:
                    print(f"  {fmt}")
            return 0
        
        # Handle list subtitles request
        if args.list_subs:
            print_info(f"Fetching available subtitles for: {args.url}")
            subtitles = downloader.list_subtitles(args.url)
            if subtitles:
                print("\nAvailable subtitles:")
                print(f"{'Language':<25} {'Type':<15} {'Formats':<20}")
                print("-" * 60)
                for lang, info in sorted(subtitles.items()):
                    formats_str = ', '.join(info['formats'][:3])
                    if len(info['formats']) > 3:
                        formats_str += '...'
                    print(f"{lang:<25} {info['type']:<15} {formats_str:<20}")
                print(f"\nTotal: {len(subtitles)} subtitle tracks available")
            else:
                print("No subtitles available for this video")
            return 0
        
        # Perform download
        print_info(f"Starting download: {args.url}")
        
        if args.playlist:
            result = downloader.download_playlist(args.url)
        elif args.audio_only:
            result = downloader.download_audio(args.url)
        else:
            result = downloader.download_video(args.url)
        
        if result:
            print_success("Download completed successfully!")
            return 0
        else:
            print_error("Download failed")
            return 1
            
    except KeyboardInterrupt:
        print_error("\nDownload cancelled by user")
        return 130
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        if args.verbose:
            logger.exception("Full error details:")
        return 1


if __name__ == '__main__':
    sys.exit(main())