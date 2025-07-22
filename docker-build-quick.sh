#!/bin/bash
# Quick build script for testing

echo "Building YouTube Downloader Docker image..."
docker build -t youtube-downloader:latest .
echo "Done! Run with: docker run -v \$(pwd)/downloads:/downloads youtube-downloader:latest --help"