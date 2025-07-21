#!/usr/bin/env python3
"""Demo script to show how to play videos with subtitles"""

import subprocess
import sys
from pathlib import Path
import platform


def find_video_subtitle_pairs(directory: Path) -> list:
    """Find video files with matching subtitle files"""
    pairs = []
    
    # Common video extensions
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}
    subtitle_extensions = {'.vtt', '.srt', '.ass', '.ssa'}
    
    for video_file in directory.iterdir():
        if video_file.suffix.lower() in video_extensions:
            # Look for matching subtitle files
            base_name = video_file.stem
            subtitles = []
            
            for sub_file in directory.iterdir():
                if sub_file.suffix.lower() in subtitle_extensions:
                    if sub_file.stem.startswith(base_name):
                        subtitles.append(sub_file)
            
            if subtitles:
                pairs.append((video_file, subtitles))
    
    return pairs


def play_with_vlc(video_path: Path, subtitle_path: Path = None):
    """Play video with VLC"""
    cmd = ['vlc', str(video_path)]
    
    if subtitle_path:
        cmd.extend(['--sub-file', str(subtitle_path)])
    
    print(f"Playing: {video_path.name}")
    if subtitle_path:
        print(f"With subtitles: {subtitle_path.name}")
    
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print("VLC not found. Please install VLC media player.")
        print("Download from: https://www.videolan.org/vlc/")


def play_with_mpv(video_path: Path, subtitle_path: Path = None):
    """Play video with MPV"""
    cmd = ['mpv', str(video_path)]
    
    if subtitle_path:
        cmd.extend(['--sub-file', str(subtitle_path)])
    
    print(f"Playing: {video_path.name}")
    if subtitle_path:
        print(f"With subtitles: {subtitle_path.name}")
    
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print("MPV not found. Please install MPV player.")
        print("Download from: https://mpv.io/")


def open_with_default_player(video_path: Path):
    """Open video with system default player"""
    system = platform.system()
    
    print(f"Opening with default player: {video_path.name}")
    print("Note: Subtitles should auto-load if they have matching names")
    
    try:
        if system == 'Darwin':  # macOS
            subprocess.run(['open', str(video_path)])
        elif system == 'Windows':
            subprocess.run(['start', '', str(video_path)], shell=True)
        else:  # Linux
            subprocess.run(['xdg-open', str(video_path)])
    except Exception as e:
        print(f"Error opening file: {e}")


def main():
    """Interactive demo for playing videos with subtitles"""
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
    else:
        directory = Path('downloads')
    
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return
    
    # Find video-subtitle pairs
    pairs = find_video_subtitle_pairs(directory)
    
    if not pairs:
        print(f"No videos with subtitles found in {directory}")
        return
    
    print(f"\nFound {len(pairs)} video(s) with subtitles:\n")
    
    for i, (video, subs) in enumerate(pairs, 1):
        print(f"{i}. {video.name}")
        for sub in subs:
            lang_code = sub.stem.replace(video.stem, '').strip('.')
            print(f"   - {sub.name} ({lang_code})")
    
    print("\nHow to play:")
    print("1. VLC will auto-load subtitles with matching names")
    print("2. Or manually load: Subtitle → Add Subtitle File")
    print("3. For SRT conversion, use: --convert-subs srt")
    
    # Show example commands
    if pairs:
        video, subs = pairs[0]
        print(f"\nExample VLC command:")
        print(f"vlc \"{video}\" --sub-file \"{subs[0]}\"")


if __name__ == "__main__":
    main()