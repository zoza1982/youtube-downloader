#!/usr/bin/env python3
"""
Utility to merge subtitle files (SRT/VTT) with video files using ffmpeg.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil
import json
try:
    from .ffmpeg_helper import ensure_ffmpeg, get_ffmpeg_command
except ImportError:
    from ffmpeg_helper import ensure_ffmpeg, get_ffmpeg_command


def check_ffmpeg():
    """Check if ffmpeg is installed"""
    return ensure_ffmpeg()


def get_video_info(video_path):
    """Get video information using ffprobe"""
    try:
        cmd = [
            get_ffmpeg_command().replace('ffmpeg', 'ffprobe'),
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception:
        return None


def merge_subtitles(video_path, subtitle_path, output_path=None, 
                   subtitle_track_name=None, soft_subs=True, 
                   subtitle_codec='mov_text', force=False):
    """
    Merge subtitle file with video file.
    
    Args:
        video_path: Path to video file
        subtitle_path: Path to subtitle file (SRT/VTT)
        output_path: Output file path (default: video_with_subs.ext)
        subtitle_track_name: Name for subtitle track (e.g., "English")
        soft_subs: If True, embeds as soft subtitles (can be turned on/off)
                  If False, burns subtitles into video (permanent)
        subtitle_codec: Subtitle codec to use (mov_text for MP4, srt for MKV)
        force: Overwrite output file if it exists
    """
    video_path = Path(video_path)
    subtitle_path = Path(subtitle_path)
    
    # Validate inputs
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}")
        return False
    
    if not subtitle_path.exists():
        print(f"Error: Subtitle file not found: {subtitle_path}")
        return False
    
    # Determine output path
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_with_subs{video_path.suffix}"
    else:
        output_path = Path(output_path)
    
    # Check if output exists
    if output_path.exists() and not force:
        print(f"Error: Output file already exists: {output_path}")
        print("Use --force to overwrite")
        return False
    
    # Auto-detect subtitle codec based on container
    if subtitle_codec == 'auto':
        if output_path.suffix.lower() == '.mp4':
            subtitle_codec = 'mov_text'
        elif output_path.suffix.lower() in ['.mkv', '.webm']:
            subtitle_codec = 'srt'
        else:
            subtitle_codec = 'mov_text'  # Default
    
    print(f"Merging subtitles...")
    print(f"  Video: {video_path.name}")
    print(f"  Subtitles: {subtitle_path.name}")
    print(f"  Output: {output_path.name}")
    print(f"  Mode: {'Soft subtitles (can be toggled)' if soft_subs else 'Hard subtitles (burned in)'}")
    
    if soft_subs:
        # Embed subtitles as a separate track (soft subs)
        cmd = [
            get_ffmpeg_command(),
            '-i', str(video_path),
            '-i', str(subtitle_path),
            '-c:v', 'copy',  # Copy video codec
            '-c:a', 'copy',  # Copy audio codec
            '-c:s', subtitle_codec,  # Subtitle codec
            '-map', '0:v',   # Map video from first input
            '-map', '0:a?',  # Map audio from first input (if exists)
            '-map', '1:0',   # Map first stream from second input (subtitle)
        ]
        
        # Add metadata for subtitle track
        if subtitle_track_name:
            cmd.extend(['-metadata:s:s:0', f'title={subtitle_track_name}'])
            cmd.extend(['-metadata:s:s:0', f'language={subtitle_track_name[:3].lower()}'])
        
        # Set default subtitle track
        cmd.extend(['-disposition:s:0', 'default'])
        
    else:
        # Burn subtitles into video (hard subs)
        # Use subtitles filter to burn them in
        subtitle_filter = f"subtitles='{str(subtitle_path).replace('\\', '\\\\').replace(':', '\\:')}'"
        
        cmd = [
            get_ffmpeg_command(),
            '-i', str(video_path),
            '-vf', subtitle_filter,
            '-c:a', 'copy',  # Copy audio codec
        ]
    
    # Add output file
    if force:
        cmd.extend(['-y'])  # Overwrite without asking
    
    cmd.append(str(output_path))
    
    # Execute ffmpeg
    try:
        print("\nRunning ffmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Successfully created: {output_path}")
            
            # Get file sizes for comparison
            original_size = video_path.stat().st_size / (1024 * 1024)  # MB
            output_size = output_path.stat().st_size / (1024 * 1024)  # MB
            
            print(f"\nFile sizes:")
            print(f"  Original: {original_size:.1f} MB")
            print(f"  Output: {output_size:.1f} MB")
            
            if soft_subs:
                print("\n💡 Tip: The subtitles are embedded as a soft track.")
                print("   Most players will show them automatically.")
                print("   You can turn them on/off in your video player.")
            else:
                print("\n💡 Note: The subtitles are permanently burned into the video.")
            
            return True
        else:
            print(f"\n❌ Error merging files:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\n❌ Error running ffmpeg: {e}")
        return False


def batch_merge(directory, pattern="*.mp4", soft_subs=True, force=False):
    """
    Merge all videos with matching subtitle files in a directory.
    
    Looks for subtitle files with the same base name as videos.
    E.g., video.mp4 + video.en.srt or video.srt
    """
    directory = Path(directory)
    if not directory.exists():
        print(f"Error: Directory not found: {directory}")
        return
    
    videos = list(directory.glob(pattern))
    if not videos:
        print(f"No videos found matching pattern: {pattern}")
        return
    
    print(f"Found {len(videos)} video(s) in {directory}")
    
    merged_count = 0
    for video_file in videos:
        base_name = video_file.stem
        
        # Look for matching subtitle files
        subtitle_patterns = [
            f"{base_name}.*.srt",
            f"{base_name}.*.vtt",
            f"{base_name}.srt",
            f"{base_name}.vtt",
        ]
        
        subtitle_file = None
        for pattern in subtitle_patterns:
            matches = list(directory.glob(pattern))
            if matches:
                subtitle_file = matches[0]
                break
        
        if subtitle_file:
            print(f"\n{'='*60}")
            print(f"Processing: {video_file.name}")
            print(f"Found subtitle: {subtitle_file.name}")
            
            output_path = directory / f"{base_name}_merged{video_file.suffix}"
            
            if merge_subtitles(video_file, subtitle_file, output_path, 
                             soft_subs=soft_subs, force=force):
                merged_count += 1
        else:
            print(f"\nSkipping {video_file.name} - no matching subtitle found")
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully merged {merged_count} video(s)")


def main():
    parser = argparse.ArgumentParser(
        description='Merge subtitle files (SRT/VTT) with video files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge single video with subtitles (soft subs)
  %(prog)s video.mp4 subtitles.srt
  
  # Merge with custom output name
  %(prog)s video.mp4 subtitles.vtt -o output.mp4
  
  # Burn subtitles into video (hard subs)
  %(prog)s video.mp4 subtitles.srt --hard-subs
  
  # Batch merge all videos in directory
  %(prog)s --batch downloads/
  
  # Merge with subtitle track name
  %(prog)s video.mp4 english.srt --subtitle-name "English"
        """
    )
    
    # Positional arguments for single file mode
    parser.add_argument('video', nargs='?', help='Video file path')
    parser.add_argument('subtitle', nargs='?', help='Subtitle file path (SRT/VTT)')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-f', '--force', action='store_true',
                       help='Overwrite output file if it exists')
    
    # Subtitle options
    parser.add_argument('--hard-subs', action='store_true',
                       help='Burn subtitles into video (permanent)')
    parser.add_argument('--subtitle-name', help='Name for subtitle track (e.g., "English")')
    parser.add_argument('--subtitle-codec', default='auto',
                       choices=['auto', 'mov_text', 'srt', 'ass'],
                       help='Subtitle codec (auto-detected by default)')
    
    # Batch mode
    parser.add_argument('--batch', metavar='DIR',
                       help='Batch process all videos in directory')
    parser.add_argument('--pattern', default='*.mp4',
                       help='File pattern for batch mode (default: *.mp4)')
    
    args = parser.parse_args()
    
    # Check ffmpeg
    if not check_ffmpeg():
        return 1
    
    # Batch mode
    if args.batch:
        batch_merge(args.batch, args.pattern, 
                   soft_subs=not args.hard_subs, force=args.force)
        return 0
    
    # Single file mode
    if not args.video or not args.subtitle:
        parser.print_help()
        return 1
    
    success = merge_subtitles(
        args.video,
        args.subtitle,
        args.output,
        args.subtitle_name,
        soft_subs=not args.hard_subs,
        subtitle_codec=args.subtitle_codec,
        force=args.force
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())