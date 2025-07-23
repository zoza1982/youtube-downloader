#!/usr/bin/env python3
"""
FFmpeg helper module for YouTube Downloader
Handles detection and automatic download of ffmpeg binaries
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
import tarfile
from pathlib import Path
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
import json
from tqdm import tqdm


class FFmpegHelper:
    """Helper class for managing FFmpeg installation"""
    
    # FFmpeg download URLs for different platforms
    FFMPEG_URLS = {
        'Windows': {
            'url': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
            'exe': 'ffmpeg.exe'
        },
        'Darwin': {  # macOS
            'url': 'https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip',
            'exe': 'ffmpeg'
        },
        'Linux': {
            'url': 'https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz',
            'exe': 'ffmpeg'
        }
    }
    
    def __init__(self):
        self.system = platform.system()
        self.app_dir = self._get_app_dir()
        self.ffmpeg_dir = self.app_dir / 'ffmpeg'
        self.ffmpeg_path = self._get_ffmpeg_path()
    
    def _get_app_dir(self) -> Path:
        """Get application directory for storing ffmpeg"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # Store in user's home directory since _MEIPASS is temporary
            home = Path.home()
            if self.system == 'Windows':
                return home / 'AppData' / 'Local' / 'ytd'
            elif self.system == 'Darwin':
                return home / 'Library' / 'Application Support' / 'ytd'
            else:  # Linux
                return home / '.local' / 'share' / 'ytd'
        else:
            # Running as script
            home = Path.home()
            if self.system == 'Windows':
                return home / 'AppData' / 'Local' / 'ytd'
            elif self.system == 'Darwin':
                return home / 'Library' / 'Application Support' / 'ytd'
            else:  # Linux
                return home / '.local' / 'share' / 'ytd'
    
    def _get_ffmpeg_path(self) -> Path:
        """Get the expected path for ffmpeg executable"""
        exe_name = self.FFMPEG_URLS[self.system]['exe']
        return self.ffmpeg_dir / exe_name
    
    def check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        # First check if it's in system PATH
        if shutil.which('ffmpeg'):
            return True
        
        # Check if we have a local copy
        if self.ffmpeg_path.exists():
            return True
        
        return False
    
    def get_ffmpeg_command(self) -> str:
        """Get the ffmpeg command to use"""
        # Prefer system ffmpeg if available
        system_ffmpeg = shutil.which('ffmpeg')
        if system_ffmpeg:
            return system_ffmpeg
        
        # Use local copy
        if self.ffmpeg_path.exists():
            return str(self.ffmpeg_path)
        
        return 'ffmpeg'  # Fallback
    
    def download_ffmpeg(self, progress_callback=None) -> bool:
        """Download and install ffmpeg for the current platform"""
        if self.system not in self.FFMPEG_URLS:
            print(f"Unsupported platform: {self.system}")
            return False
        
        print(f"Downloading FFmpeg for {self.system}...")
        
        # Create directories
        self.app_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_dir.mkdir(parents=True, exist_ok=True)
        
        # Download URL and info
        download_info = self.FFMPEG_URLS[self.system]
        url = download_info['url']
        
        # Download with progress
        temp_file = self.ffmpeg_dir / 'ffmpeg_temp.download'
        
        try:
            if progress_callback:
                self._download_with_progress(url, temp_file, progress_callback)
            else:
                self._download_with_tqdm(url, temp_file)
            
            # Extract based on file type
            print("Extracting FFmpeg...")
            if url.endswith('.zip'):
                self._extract_zip(temp_file)
            elif url.endswith('.tar.xz') or url.endswith('.tar.gz'):
                self._extract_tar(temp_file)
            else:
                # Direct binary download (macOS)
                shutil.move(temp_file, self.ffmpeg_path)
            
            # Make executable on Unix
            if self.system in ['Darwin', 'Linux']:
                os.chmod(self.ffmpeg_path, 0o755)
            
            # Clean up
            if temp_file.exists():
                temp_file.unlink()
            
            print(f"FFmpeg installed successfully to: {self.ffmpeg_path}")
            return True
            
        except Exception as e:
            print(f"Error downloading FFmpeg: {e}")
            if temp_file.exists():
                temp_file.unlink()
            return False
    
    def _download_with_tqdm(self, url: str, dest: Path):
        """Download file with tqdm progress bar"""
        response = urlopen(url)
        total_size = int(response.headers.get('Content-Length', 0))
        
        with open(dest, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading') as pbar:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    def _download_with_progress(self, url: str, dest: Path, callback):
        """Download file with custom progress callback"""
        def report_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100) if total_size > 0 else 0
            callback(percent, downloaded, total_size)
        
        urlretrieve(url, dest, reporthook=report_progress)
    
    def _extract_zip(self, zip_path: Path):
        """Extract zip file and find ffmpeg binary"""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find ffmpeg.exe in the zip
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith('ffmpeg.exe') or file_info.filename.endswith('ffmpeg'):
                    # Extract to temp location
                    temp_path = self.ffmpeg_dir / 'temp_extract'
                    zip_ref.extract(file_info, temp_path)
                    
                    # Move to final location
                    extracted_file = temp_path / file_info.filename
                    shutil.move(extracted_file, self.ffmpeg_path)
                    
                    # Clean up
                    shutil.rmtree(temp_path, ignore_errors=True)
                    break
    
    def _extract_tar(self, tar_path: Path):
        """Extract tar file and find ffmpeg binary"""
        with tarfile.open(tar_path, 'r:*') as tar_ref:
            # Find ffmpeg in the tar
            for member in tar_ref.getmembers():
                if member.name.endswith('ffmpeg') and not member.isdir():
                    # Extract directly to destination
                    member.name = 'ffmpeg'  # Rename to just 'ffmpeg'
                    tar_ref.extract(member, self.ffmpeg_dir)
                    break
    
    def ensure_ffmpeg(self) -> bool:
        """Ensure ffmpeg is available, download if necessary"""
        if self.check_ffmpeg():
            return True
        
        print("\nFFmpeg is required but not found.")
        print("Would you like to download it automatically? (y/n): ", end='')
        
        try:
            response = input().strip().lower()
            if response == 'y':
                return self.download_ffmpeg()
            else:
                print("\nPlease install FFmpeg manually:")
                print("  Windows: Download from https://ffmpeg.org/download.html")
                print("  macOS: brew install ffmpeg")
                print("  Linux: sudo apt install ffmpeg")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\nFFmpeg installation cancelled.")
            return False


# Convenience functions
def check_ffmpeg() -> bool:
    """Check if ffmpeg is available"""
    helper = FFmpegHelper()
    return helper.check_ffmpeg()


def get_ffmpeg_command() -> str:
    """Get the ffmpeg command to use"""
    helper = FFmpegHelper()
    return helper.get_ffmpeg_command()


def ensure_ffmpeg() -> bool:
    """Ensure ffmpeg is available, download if necessary"""
    helper = FFmpegHelper()
    return helper.ensure_ffmpeg()


if __name__ == "__main__":
    # Test the helper
    helper = FFmpegHelper()
    if helper.check_ffmpeg():
        print(f"FFmpeg found at: {helper.get_ffmpeg_command()}")
    else:
        print("FFmpeg not found.")
        if helper.ensure_ffmpeg():
            print(f"FFmpeg is now available at: {helper.get_ffmpeg_command()}")