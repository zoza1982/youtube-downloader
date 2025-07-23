# YouTube Downloader CLI

A powerful and user-friendly command-line tool for downloading videos from YouTube and 1700+ other video platforms using the robust yt-dlp library.

## 🚀 Quick Start with Docker

```bash
# Download a video (no installation required!)
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ

# Download audio as MP3
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ -a

# Download subtitles only (video and subtitles must be downloaded separately)
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ -s --sub-langs en --skip-download
```

**Pro tip**: Add this alias to your shell: `alias ytd='docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest'`

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Using pyenv](#using-pyenv-recommended)
  - [Using Docker/Podman](#using-dockerpodman)
- [Quick Start](#quick-start)
- [Command-Line Options](#command-line-options)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
  - [Subtitles](#subtitles)
  - [Playing Videos with Subtitles](#playing-videos-with-subtitles)
  - [Merging Subtitles with Videos](#merging-subtitles-with-videos)
- [Utilities](#utilities)
- [Quick Examples](#quick-examples)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [License](#license)

## Features

- 🌐 **1700+ Supported Sites**: Works with YouTube, Twitter/X, Facebook, Instagram, TikTok, and many more
- 📹 **Video Downloads**: Download videos in various qualities and formats
- 🎵 **Audio Extraction**: Extract audio in MP3, M4A, OPUS, and more formats
- 📑 **Playlist Support**: Download entire playlists with customizable selection
- 📝 **Subtitles**: Download manual and auto-generated subtitles in any language
- 🔄 **Subtitle Conversion**: Convert VTT to SRT format for better compatibility
- 🎬 **Subtitle Merging**: Embed subtitles into videos (soft or hard subs)
- 🎨 **Metadata & Thumbnails**: Preserve video metadata and embed thumbnails
- ⚡ **Concurrent Downloads**: Speed up downloads with parallel processing
- 📊 **Progress Tracking**: Visual progress bars with speed and ETA
- 🔄 **Resume Capability**: Continue interrupted downloads
- 🎯 **Format Selection**: Choose specific video quality/format
- 🔧 **Configurable**: Support for configuration files
- 🐳 **Docker/Podman Support**: Run in containers with easy deployment
- 🔒 **Security**: Runs as non-root user in containers

## Supported Sites

This tool supports **1700+ video platforms** including:

- **Video Platforms**: YouTube, Vimeo, Dailymotion, Twitch
- **Social Media**: Twitter/X, Facebook, Instagram, TikTok, Reddit
- **Music**: SoundCloud, Bandcamp, Mixcloud
- **Educational**: Coursera, Udemy, TED, Khan Academy
- **News**: BBC, CNN, NBC, Fox News
- **Adult Content**: pornhub, xvideos, and many others
- **And 1700+ more sites!**

To see all supported sites:
```bash
ytd --list-extractors
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- ffmpeg (for audio conversion and video/audio merging)

### Installing ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Using pyenv (Recommended)

1. **Install pyenv** (if not already installed):
   ```bash
   # macOS
   brew install pyenv
   
   # Linux
   curl https://pyenv.run | bash
   ```

2. **Install Python and create virtual environment:**
   ```bash
   # Install Python 3.11 (or any version >= 3.8)
   pyenv install 3.11.7
   
   # Clone the repository
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   
   # Set local Python version
   pyenv local 3.11.7
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install the package
   pip install -e .
   ```

### Using system Python

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Using pip (when published)

```bash
pip install youtube-downloader-cli
```

### Using Docker/Podman

The easiest way to use YouTube Downloader is with our pre-built Docker images from GitHub Container Registry.

#### Quick Start (No Build Required!)

```bash
# Pull the image (optional, docker run will do this automatically)
docker pull ghcr.io/zoza1982/youtube-downloader:latest

# Download a video
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ

# Download audio only (MP3)
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ -a

# Download subtitles only (video and subtitles must be downloaded separately)
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ -s --sub-langs en --skip-download

# Download 1080p with Croatian subtitles converted to SRT
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=VIDEO_ID -f best[height=1080] -s --sub-langs hr --convert-subs srt

# Interactive mode (for multiple downloads)
docker run -it --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest
# Then use ytd commands inside container
```

#### Using Alpine Version (Smaller Image)

```bash
# Use Alpine version for smaller download size
docker pull ghcr.io/zoza1982/youtube-downloader:alpine

# Run with Alpine image
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:alpine https://youtube.com/watch?v=VIDEO_ID
```

#### Create Alias for Easy Use

Add this to your `.bashrc` or `.zshrc`:

```bash
# YouTube Downloader alias
alias ytd='docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest'

# Then use it like a native command:
ytd https://youtube.com/watch?v=VIDEO_ID
ytd https://youtube.com/watch?v=VIDEO_ID -a --audio-format mp3
ytd --help
```

#### Build Your Own Image (Optional)

If you want to build the image yourself:

```bash
# Clone the repository
git clone https://github.com/zoza1982/youtube-downloader.git
cd youtube-downloader

# Build the image
docker build -t youtube-downloader .

# Or using docker-compose
docker-compose build
```

#### Run with docker-compose

```bash
# Simple download
YTD_URL="https://youtube.com/watch?v=VIDEO_ID" docker-compose run --rm ytd

# Download with arguments
YTD_URL="https://youtube.com/watch?v=VIDEO_ID" YTD_ARGS="-a --audio-format mp3" docker-compose run --rm ytd

# Interactive shell
docker-compose run --rm ytd bash

# Using the download profile
YTD_URL="https://youtube.com/watch?v=VIDEO_ID" docker-compose --profile download up
```

#### Podman-specific notes

Since you're using Podman aliased as docker, everything should work the same. For rootless podman:

```bash
# Pull from GitHub Container Registry
podman pull ghcr.io/zoza1982/youtube-downloader:latest

# Run with podman (note: podman runs rootless by default)
podman run --rm -v $(pwd)/downloads:/downloads:Z ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=VIDEO_ID

# The convenience script auto-detects podman
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID
```

The `:Z` flag is important for SELinux systems to properly handle volume permissions. The `run-docker.sh` script automatically adds this flag when using Podman on Linux.

#### Using the convenience script

A `run-docker.sh` script is provided for easier usage:

```bash
# Make it executable
chmod +x run-docker.sh

# Run in interactive mode
./run-docker.sh

# Download a video
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID

# Download with options
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID -a --audio-format mp3
```

The script automatically:
- Detects whether to use Docker or Podman
- Builds the image if needed
- Handles volume mounting with proper SELinux labels for Podman
- Provides interactive mode when run without arguments

#### Building a smaller image

An Alpine-based Dockerfile is also provided for a smaller image size:

```bash
# Build Alpine version (smaller size)
docker build -f Dockerfile.alpine -t youtube-downloader:alpine .

# Run Alpine version
docker run -v $(pwd)/downloads:/downloads youtube-downloader:alpine https://youtube.com/watch?v=VIDEO_ID
```

#### Volume mounts and permissions

The container runs as a non-root user (uid 1000) for security. Make sure your downloads directory has appropriate permissions:

```bash
# Create downloads directory with correct permissions
mkdir -p downloads
chmod 755 downloads

# For Podman on SELinux systems
chcon -t container_file_t downloads/
```

## Quick Start

### Basic Usage

Download a video:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID
```

Download audio only (MP3):
```bash
ytd https://youtube.com/watch?v=VIDEO_ID -a
```

Download a playlist:
```bash
ytd https://youtube.com/playlist?list=PLAYLIST_ID -p
```

### Common Examples

Download best quality video to specific directory:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID -f best -o ~/Videos
```

Download audio in M4A format:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID -a --audio-format m4a
```

Download with subtitles:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en,es
```

Download specific playlist items:
```bash
ytd https://youtube.com/playlist?list=PLAYLIST_ID -p --playlist-items "1-3,7,10-13"
```

List available formats:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID --list-formats
```

## Command-Line Options

### Basic Options
- `url`: YouTube video or playlist URL (required)
- `-h, --help`: Show help message

### Output Options
- `-o, --output PATH`: Output directory (default: current directory)
- `--filename TEMPLATE`: Custom filename template

### Format Options
- `-f, --format FORMAT`: Video format/quality (default: best)
- `-a, --audio-only`: Download audio only
- `--audio-format FORMAT`: Audio format (mp3, m4a, opus, vorbis, flac, wav)
- `--list-formats`: List all available formats
- `--list-subs`: List all available subtitles (including auto-generated)

### Download Options
- `-p, --playlist`: Download entire playlist
- `--playlist-items ITEMS`: Specific playlist items (e.g., "1-3,7,10-13")
- `-s, --subtitles`: Download subtitles
- `--sub-langs LANGS`: Subtitle languages (comma-separated, or "all" for all available)
- `--write-auto-subs`: Download auto-generated subtitles (deprecated - now included automatically)
- `--skip-download`: Skip downloading video/audio (useful for subtitles only)
- `--convert-subs FORMAT`: Convert subtitles to format (srt, vtt, keep)
- `-m, --metadata`: Embed metadata
- `--thumbnail`: Embed thumbnail
- `-r, --limit-rate RATE`: Limit download rate (e.g., 50K, 4M)
- `--concurrent N`: Number of concurrent downloads

### Other Options
- `-v, --verbose`: Enable verbose output
- `-q, --quiet`: Enable quiet mode
- `--config PATH`: Configuration file path
- `--update`: Update yt-dlp
- `--no-progress`: Disable progress bar
- `--archive FILE`: Track downloaded videos
- `--cookies FILE`: Cookies file path
- `--list-extractors`: List all supported video sites
- `--version`: Show version

## Configuration

Create a configuration file at `~/.config/ytd/config.yaml`:

```yaml
default_output: ~/Videos/YouTube
default_format: best
audio_format: mp3
subtitles: true
metadata: true
concurrent_downloads: 3
```

## Advanced Usage

### Subtitles

YouTube provides both manually created subtitles and auto-generated (automatic captions) subtitles. This tool supports both:

#### Listing Available Subtitles
```bash
# List all available subtitles for a video
ytd https://youtube.com/watch?v=VIDEO_ID --list-subs
```

#### Downloading Subtitles

**Important**: Due to YouTube rate limiting, video and subtitles must be downloaded separately.

```bash
# Step 1: Download the video
ytd https://youtube.com/watch?v=VIDEO_ID

# Step 2: Download subtitles separately
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --skip-download

# Download specific languages (comma-separated)
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en,es,fr,de --skip-download

# Download ALL available subtitles
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs all --skip-download

# Convert subtitles to SRT during download
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs hr --skip-download --convert-subs srt
```

**Note**: The tool now automatically downloads whatever subtitles are available (manual or auto-generated) for the requested languages. If manual subtitles aren't available, it will download auto-generated ones.

#### Auto-generated Subtitles
Auto-generated subtitles are created by YouTube's speech recognition technology. They're available in many languages and can be useful for:
- Videos without manual subtitles
- Language learning
- Accessibility
- Content in multiple languages

Note: Auto-generated subtitles may contain errors and lack proper punctuation.

### Playing Videos with Subtitles

Most video players will automatically load subtitles if they're in the same folder with matching names:
- Video: `video-title.mp4`
- Subtitle: `video-title.lang.vtt` or `video-title.lang.srt`

#### Supported Players

**VTT Format Support:**
- ✅ VLC Media Player (all platforms)
- ✅ MPV Player (all platforms)
- ✅ IINA (macOS)
- ✅ PotPlayer (Windows)
- ✅ Kodi
- ✅ Plex
- ❌ QuickTime (needs SRT)
- ❌ Windows Media Player (needs SRT)

#### Converting Subtitles to SRT

Some players require SRT format. You can convert during download:

```bash
# Download with automatic SRT conversion
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --convert-subs srt

# Convert existing VTT files to SRT
python -m ytd.convert_subtitles video.vtt

# Batch convert all VTT files in a directory
python -m ytd.convert_subtitles --batch downloads/
```

#### Loading Subtitles in VLC

**Automatic:** Keep files with matching names in same folder
**Manual:** Subtitle → Add Subtitle File... → Select .vtt or .srt
**Drag & Drop:** Drag subtitle file onto VLC window

### Merging Subtitles with Videos

You can permanently embed subtitles into video files using the merge utility:

```bash
# Merge as soft subtitles (can be turned on/off in player)
python merge_subtitles.py video.mp4 subtitles.srt
# Or using module syntax:
python -m ytd.merge_subtitles video.mp4 subtitles.srt

# Merge with custom output name
python merge_subtitles.py video.mp4 subtitles.vtt -o final_video.mp4

# Burn subtitles into video (permanent, always visible)
python merge_subtitles.py video.mp4 subtitles.srt --hard-subs

# Batch merge all videos in a directory with matching subtitles
python merge_subtitles.py --batch downloads/

# Add subtitle track with language name
python merge_subtitles.py video.mp4 croatian.srt --subtitle-name "Croatian"
```

**Soft vs Hard Subtitles:**
- **Soft subtitles**: Embedded as separate track, can be toggled on/off in players
- **Hard subtitles**: Permanently burned into video, always visible

**Note**: This requires ffmpeg to be installed on your system.

## Utilities

The project includes several utility scripts for working with downloaded content:

### Subtitle Converter (`convert_subtitles.py`)
Convert VTT subtitles to SRT format:
```bash
# Convert single file
python convert_subtitles.py video.en.vtt

# Batch convert directory
python -m ytd.convert_subtitles --batch downloads/
```

### Subtitle Merger (`merge_subtitles.py`)
Merge subtitles with videos using ffmpeg:
```bash
# Soft subtitles (toggleable)
python merge_subtitles.py video.mp4 subtitles.srt

# Hard subtitles (burned in)
python merge_subtitles.py video.mp4 subtitles.srt --hard-subs

# Batch merge directory
python merge_subtitles.py --batch downloads/
```

### Play Demo (`play_with_subtitles.py`)
Demo script showing how to play videos with subtitles:
```bash
python play_with_subtitles.py downloads/
```

### Docker Runner (`run-docker.sh`)
Convenience script for Docker/Podman:
```bash
# Interactive mode
./run-docker.sh

# Download video
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID
```

### Format Selection

YouTube videos are available in various formats. Use `--list-formats` to see available options:

```bash
ytd https://youtube.com/watch?v=VIDEO_ID --list-formats
```

Then download specific format:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID -f 137+140  # 1080p video + audio
```

### Rate Limiting

Limit download speed to avoid bandwidth issues:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID --limit-rate 1M  # 1 MB/s
```

### Archive File

Track downloaded videos to avoid re-downloading:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID --archive ~/downloaded.txt
```

### Using Cookies

For age-restricted or private videos:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID --cookies ~/cookies.txt
```

## Quick Examples

### Download a specific video quality
```bash
# List available formats first
ytd https://youtube.com/watch?v=dQw4w9WgXcQ --list-formats

# Download 1080p video (format codes may vary)
ytd https://youtube.com/watch?v=dQw4w9WgXcQ -f "137+140"

# Download best quality available
ytd https://youtube.com/watch?v=dQw4w9WgXcQ -f best
```

### Download audio for a podcast
```bash
# Download as MP3 with metadata
ytd https://youtube.com/watch?v=PODCAST_ID -a --audio-format mp3 -m

# Download entire podcast playlist as MP3
ytd https://youtube.com/playlist?list=PLAYLIST_ID -p -a --audio-format mp3
```

### Download with subtitles for language learning
```bash
# List all available subtitles for a video
ytd https://youtube.com/watch?v=VIDEO_ID --list-subs

# Download video first
ytd https://youtube.com/watch?v=VIDEO_ID

# Then download subtitles separately (due to rate limiting)
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --skip-download

# Download multiple language subtitles
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en,es,fr --skip-download

# Download ALL available subtitles
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs all --skip-download

# Download subtitles with automatic SRT conversion
ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --skip-download --convert-subs srt

# For playlists: download videos first, then subtitles
ytd https://youtube.com/playlist?list=PLAYLIST_ID -p
ytd https://youtube.com/playlist?list=PLAYLIST_ID -p -s --sub-langs en --skip-download
```

### Working with subtitles
```bash
# Convert VTT to SRT
python convert_subtitles.py video.en.vtt

# Batch convert all VTT files in downloads folder
python -m ytd.convert_subtitles --batch downloads/

# Merge subtitles with video (soft subs - can be toggled)
python merge_subtitles.py video.mp4 video.en.srt

# Burn subtitles into video (hard subs - permanent)
python merge_subtitles.py video.mp4 video.en.srt --hard-subs

# Batch merge all videos with matching subtitles
python merge_subtitles.py --batch downloads/
```

### Using Docker/Podman
```bash
# Quick download with pre-built image
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=VIDEO_ID

# Using the convenience script (auto-pulls from ghcr.io)
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID

# Download audio only
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID -a

# Download with Croatian subtitles as SRT
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID -s --sub-langs hr --convert-subs srt

# Interactive mode for multiple downloads
./run-docker.sh
# Then use ytd commands inside the container

# Using docker-compose (pulls from ghcr.io automatically)
docker-compose run --rm ytd https://youtube.com/watch?v=VIDEO_ID

# One-off download with docker-compose
YTD_URL="https://youtube.com/watch?v=VIDEO_ID" YTD_ARGS="-a" docker-compose run --rm ytd-download

# Use local build instead of pre-built image
USE_LOCAL_BUILD=true ./run-docker.sh https://youtube.com/watch?v=VIDEO_ID
```

### Batch download with archive
```bash
# First download - creates archive file
ytd https://youtube.com/watch?v=VIDEO1 --archive downloaded.txt

# Subsequent downloads - skips already downloaded videos
ytd https://youtube.com/watch?v=VIDEO2 --archive downloaded.txt
ytd https://youtube.com/playlist?list=PLAYLIST_ID -p --archive downloaded.txt
```

## Troubleshooting

### Common Issues

1. **"Video unavailable" error**
   - Try updating yt-dlp: `ytd --update`
   - Check if video is private or age-restricted

2. **Slow downloads**
   - Increase concurrent downloads: `--concurrent 5`
   - Check your internet connection

3. **Format not available**
   - List formats first: `--list-formats`
   - Choose available format or use `best`

4. **SSL Certificate errors**
   - Update certificates or use `--no-check-certificate` (not recommended)

5. **HTTP 429 Too Many Requests**
   - YouTube rate limiting prevents downloading video + subtitles together
   - The tool now enforces separate downloads:
     1. Download video: `ytd URL`
     2. Download subtitles: `ytd URL -s --sub-langs en --skip-download`

### Docker/Podman Issues

1. **Permission denied errors**
   - Ensure downloads directory has correct permissions: `chmod 755 downloads`
   - For Podman on SELinux: use `:Z` flag or run `chcon -t container_file_t downloads/`

2. **Build fails with network errors**
   - Check Docker/Podman proxy settings
   - Try building with `--no-cache` flag

3. **Container can't write to downloads**
   - Check UID mismatch: container runs as UID 1000
   - Solution: `chown 1000:1000 downloads` or adjust Dockerfile

4. **Podman-specific issues**
   - Use `podman machine start` if on macOS
   - For rootless mode, ensure subuid/subgid are configured

### Debug Mode

Enable verbose output for debugging:
```bash
ytd https://youtube.com/watch?v=VIDEO_ID -v

# In Docker
docker run -v $(pwd)/downloads:/downloads youtube-downloader URL -v
```

## Development

### Project Structure
```
youtube-downloader/
├── ytd/
│   ├── __init__.py         # Package metadata
│   ├── cli.py              # Command-line interface with argparse
│   ├── downloader.py       # Core download logic using yt-dlp
│   ├── utils.py            # Utility functions
│   ├── convert_subtitles.py # VTT to SRT converter
│   └── merge_subtitles.py  # Merge subtitles with videos
├── tests/
│   ├── __init__.py
│   └── test_cli.py         # Unit tests
├── .github/
│   └── workflows/
│       └── docker-publish.yml # GitHub Actions for Docker builds
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── setup.py               # Package configuration
├── README.md              # This file
├── example.py             # Usage examples
├── Dockerfile             # Standard Docker image
├── Dockerfile.alpine      # Smaller Alpine-based image
├── docker-compose.yml     # Docker Compose configuration
├── docker-entrypoint.sh   # Custom entrypoint script
├── run-docker.sh         # Convenience script for Docker/Podman
├── .dockerignore         # Docker build exclusions
├── .gitignore           # Git exclusions
├── convert_subtitles.py  # Standalone subtitle converter
├── merge_subtitles.py    # Standalone subtitle merger
└── play_with_subtitles.py # Demo for playing videos with subs
```

### Development Setup

1. **Clone and setup environment:**
   ```bash
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Install package in editable mode
   pip install -e .
   ```

2. **Verify installation:**
   ```bash
   # Check if ytd command is available
   which ytd
   
   # Check version
   ytd --version
   
   # View help
   ytd --help
   ```

### Running the Tool

After installation, you can use the `ytd` command from anywhere:

```bash
# Basic download
ytd https://youtube.com/watch?v=VIDEO_ID

# Download to specific directory
ytd https://youtube.com/watch?v=VIDEO_ID -o ~/Downloads

# Download audio only
ytd https://youtube.com/watch?v=VIDEO_ID -a

# Download with debug output
ytd https://youtube.com/watch?v=VIDEO_ID -v
```

### Testing

1. **Run all tests:**
   ```bash
   pytest
   ```

2. **Run tests with coverage:**
   ```bash
   pytest --cov=ytd --cov-report=term-missing
   ```

3. **Run specific test file:**
   ```bash
   pytest tests/test_cli.py -v
   ```

4. **Run tests and generate HTML coverage report:**
   ```bash
   pytest --cov=ytd --cov-report=html
   # Open htmlcov/index.html in browser
   ```

### Code Quality

1. **Run linter (flake8):**
   ```bash
   flake8 ytd/ --max-line-length=120
   ```

2. **Format code with black:**
   ```bash
   black ytd/ tests/
   ```

3. **Type checking with mypy:**
   ```bash
   mypy ytd/
   ```

4. **Run all quality checks:**
   ```bash
   # Create a simple script or use tox
   black ytd/ tests/ --check
   flake8 ytd/ tests/
   mypy ytd/
   pytest
   ```

### Building and Distribution

1. **Build package:**
   ```bash
   python setup.py sdist bdist_wheel
   ```

2. **Test installation locally:**
   ```bash
   pip install dist/youtube_downloader_cli-1.0.0-py3-none-any.whl
   ```

3. **Upload to TestPyPI (for testing):**
   ```bash
   twine upload --repository testpypi dist/*
   ```

4. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Check code quality (`black`, `flake8`, `mypy`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Tips

- Always work in a virtual environment
- Run tests before committing
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Requirements

### Python Dependencies
- **yt-dlp**: The core downloading engine
- **argparse**: Command-line argument parsing (built-in)
- **tqdm**: Progress bar display
- **colorama**: Cross-platform colored terminal output
- **PyYAML**: Configuration file support

### System Dependencies
- **Python 3.8+**: Required for running the application
- **ffmpeg**: Required for audio conversion, video merging, and subtitle embedding
- **git**: Required for some yt-dlp operations

### Optional Dependencies
- **Docker/Podman**: For containerized deployment
- **VLC/MPV**: For playing downloaded videos with subtitles

## Acknowledgments

- Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Inspired by the need for a simple, powerful YouTube downloader

## Disclaimer

This tool is for personal use only. Respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download.