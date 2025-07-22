# YouTube Downloader - Docker Quick Start Guide

## 🚀 Instant Setup (No Installation Required!)

Just run these commands - the image will be automatically pulled from GitHub Container Registry:

### Basic Usage

```bash
# Download a video
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ

# Download audio only (MP3)
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ -a

# Download with subtitles
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=dQw4w9WgXcQ -s --sub-langs en
```

### 💡 Make Your Life Easier - Create an Alias

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
alias ytd='docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest'
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use it like a native command:
```bash
ytd https://youtube.com/watch?v=dQw4w9WgXcQ
ytd https://youtube.com/watch?v=dQw4w9WgXcQ -a
ytd --help
```

## 📦 Available Images

- `ghcr.io/zoza1982/youtube-downloader:latest` - Standard image with all features
- `ghcr.io/zoza1982/youtube-downloader:alpine` - Smaller Alpine-based image
- `ghcr.io/zoza1982/youtube-downloader:main` - Latest development version

## 🎯 Common Use Cases

### Download Best Quality Video
```bash
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest \
  https://youtube.com/watch?v=VIDEO_ID -f best
```

### Download Audio for Podcasts
```bash
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest \
  https://youtube.com/watch?v=PODCAST_ID -a --audio-format mp3
```

### Download with Subtitles in Your Language
```bash
# List available subtitles
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest \
  https://youtube.com/watch?v=VIDEO_ID --list-subs

# Download with specific language subtitles (e.g., Croatian)
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest \
  https://youtube.com/watch?v=VIDEO_ID -s --sub-langs hr --convert-subs srt
```

### Download Entire Playlist
```bash
docker run --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest \
  https://youtube.com/playlist?list=PLAYLIST_ID -p
```

### Interactive Mode (Multiple Downloads)
```bash
docker run -it --rm -v $(pwd)/downloads:/downloads ghcr.io/zoza1982/youtube-downloader:latest
# Then use ytd commands inside the container
```

## 🛠️ Using Docker Compose

1. Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  ytd:
    image: ghcr.io/zoza1982/youtube-downloader:latest
    volumes:
      - ./downloads:/downloads
    stdin_open: true
    tty: true
```

2. Run commands:
```bash
# Interactive mode
docker-compose run --rm ytd

# Download a video
docker-compose run --rm ytd https://youtube.com/watch?v=VIDEO_ID

# Download audio
docker-compose run --rm ytd https://youtube.com/watch?v=VIDEO_ID -a
```

## 🐧 Podman Users

If you're using Podman, add the `:Z` flag for SELinux:

```bash
podman run --rm -v $(pwd)/downloads:/downloads:Z ghcr.io/zoza1982/youtube-downloader:latest https://youtube.com/watch?v=VIDEO_ID
```

Or use the provided script that auto-detects Podman:
```bash
./run-docker.sh https://youtube.com/watch?v=VIDEO_ID
```

## ❓ Troubleshooting

### Permission Denied
If you get permission errors, ensure the downloads directory has proper permissions:
```bash
mkdir -p downloads
chmod 755 downloads
```

### Cannot Pull Image
If you're behind a proxy or firewall:
```bash
# Try pulling explicitly
docker pull ghcr.io/zoza1982/youtube-downloader:latest

# Or use Docker Hub mirror (if available in your region)
```

### Out of Space
The images are relatively small:
- Standard image: ~200MB
- Alpine image: ~150MB

Clear Docker cache if needed:
```bash
docker system prune -a
```

## 📚 More Information

- Full documentation: https://github.com/zoza1982/youtube-downloader
- Report issues: https://github.com/zoza1982/youtube-downloader/issues
- All command options: `docker run --rm ghcr.io/zoza1982/youtube-downloader:latest --help`