#!/usr/bin/env python3
"""Convert subtitle formats (VTT to SRT)"""

import re
import sys
from pathlib import Path


def vtt_to_srt(vtt_content: str) -> str:
    """Convert VTT subtitle format to SRT format"""
    # Remove WEBVTT header and metadata
    lines = vtt_content.split('\n')
    srt_lines = []
    subtitle_index = 1
    i = 0
    
    # Skip WEBVTT header and any metadata
    while i < len(lines) and not re.match(r'^\d{2}:\d{2}:', lines[i]):
        i += 1
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check if this is a timestamp line
        if ' --> ' in line:
            # Add subtitle index
            srt_lines.append(str(subtitle_index))
            
            # Convert timestamp format
            # VTT: 00:00:00.000 --> 00:00:02.000
            # SRT: 00:00:00,000 --> 00:00:02,000
            timestamp = line.replace('.', ',')
            
            # Remove position tags if present (align:start position:0%)
            timestamp = re.sub(r'\s*align:.*$', '', timestamp)
            timestamp = re.sub(r'\s*position:.*$', '', timestamp)
            
            srt_lines.append(timestamp)
            
            # Collect subtitle text
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip() and ' --> ' not in lines[i]:
                # Remove VTT tags like <c>, </c>, timestamps within text
                text = lines[i].strip()
                text = re.sub(r'<[^>]+>', '', text)  # Remove HTML-like tags
                text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)  # Remove inline timestamps
                if text:
                    text_lines.append(text)
                i += 1
            
            if text_lines:
                srt_lines.append('\n'.join(text_lines))
                srt_lines.append('')  # Empty line between subtitles
                subtitle_index += 1
        else:
            i += 1
    
    return '\n'.join(srt_lines)


def convert_file(vtt_path: Path, srt_path: Path = None) -> Path:
    """Convert VTT file to SRT file"""
    if srt_path is None:
        srt_path = vtt_path.with_suffix('.srt')
    
    try:
        # Read VTT content
        with open(vtt_path, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        # Convert to SRT
        srt_content = vtt_to_srt(vtt_content)
        
        # Write SRT file
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        return srt_path
    except Exception as e:
        print(f"Error converting {vtt_path}: {e}")
        return None


def batch_convert(directory: Path, pattern: str = "*.vtt") -> list:
    """Convert all VTT files in a directory to SRT"""
    converted_files = []
    
    for vtt_file in directory.glob(pattern):
        srt_file = convert_file(vtt_file)
        if srt_file:
            converted_files.append(srt_file)
            print(f"Converted: {vtt_file.name} → {srt_file.name}")
    
    return converted_files


def main():
    """Command-line interface for subtitle conversion"""
    if len(sys.argv) < 2:
        print("Usage: python convert_subtitles.py <vtt_file> [srt_file]")
        print("       python convert_subtitles.py --batch <directory>")
        sys.exit(1)
    
    if sys.argv[1] == '--batch' and len(sys.argv) >= 3:
        # Batch conversion
        directory = Path(sys.argv[2])
        if directory.is_dir():
            converted = batch_convert(directory)
            print(f"\nConverted {len(converted)} files")
        else:
            print(f"Error: {directory} is not a directory")
    else:
        # Single file conversion
        vtt_path = Path(sys.argv[1])
        if not vtt_path.exists():
            print(f"Error: {vtt_path} not found")
            sys.exit(1)
        
        srt_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        result = convert_file(vtt_path, srt_path)
        
        if result:
            print(f"Converted: {vtt_path} → {result}")
        else:
            print("Conversion failed")


if __name__ == "__main__":
    main()