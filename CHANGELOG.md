# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-21

### Added
- Initial release with core YouTube downloading functionality
- Command-line interface using argparse
- Video download support in multiple formats and qualities
- Audio extraction with format conversion (MP3, M4A, OPUS, etc.)
- Playlist download support with item selection
- Subtitle download support (manual and auto-generated)
- Subtitle listing with `--list-subs` option
- Subtitle-only download with `--skip-download` option
- Subtitle format conversion with `--convert-subs` option
- VTT to SRT converter utility (`convert_subtitles.py`)
- Subtitle merging utility (`merge_subtitles.py`) for embedding subtitles
- Play demo script (`play_with_subtitles.py`)
- Progress tracking with visual progress bars
- Resume capability for interrupted downloads
- Metadata and thumbnail embedding
- Configuration file support (YAML)
- Concurrent download support
- Archive file support to avoid re-downloads
- Cookie support for restricted videos
- Rate limiting option
- Docker/Podman support with multiple Dockerfiles
- Docker Compose configuration
- GitHub Actions workflow for Docker builds
- Convenience script for Docker/Podman usage (`run-docker.sh`)
- Comprehensive documentation and examples
- Unit tests with pytest

### Technical Details
- Built on yt-dlp library for robust YouTube support
- Runs as non-root user in containers for security
- Multi-stage Docker build for smaller images
- Alpine Linux variant available for minimal size
- Cross-platform support (Windows, macOS, Linux)
- Python 3.8+ compatibility

### Dependencies
- yt-dlp (core engine)
- ffmpeg (media processing)
- tqdm (progress bars)
- colorama (colored output)
- PyYAML (configuration)