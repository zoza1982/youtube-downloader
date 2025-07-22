#!/bin/bash
# Convenience script for running YouTube downloader with Docker/Podman

# Detect if we should use podman or docker
if command -v podman &> /dev/null; then
    DOCKER_CMD="podman"
    # Add :Z flag for SELinux if on Linux with podman
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        VOLUME_FLAGS=":Z"
    else
        VOLUME_FLAGS=""
    fi
else
    DOCKER_CMD="docker"
    VOLUME_FLAGS=""
fi

# Configuration
USE_LOCAL_BUILD=${USE_LOCAL_BUILD:-false}
LOCAL_IMAGE_NAME="youtube-downloader"
REMOTE_IMAGE_NAME="ghcr.io/zoza1982/youtube-downloader:latest"

# Create downloads directory if it doesn't exist
mkdir -p downloads

# Determine which image to use
if [ "$USE_LOCAL_BUILD" = "true" ]; then
    IMAGE_NAME=$LOCAL_IMAGE_NAME
    # Check if local image exists, build if not
    if ! $DOCKER_CMD image inspect $IMAGE_NAME &> /dev/null; then
        echo "Building YouTube downloader image locally..."
        $DOCKER_CMD build -t $IMAGE_NAME .
    fi
else
    # Use pre-built image from GitHub Container Registry
    IMAGE_NAME=$REMOTE_IMAGE_NAME
    echo "Using pre-built image from GitHub Container Registry..."
    echo "Pulling latest version (if needed)..."
    $DOCKER_CMD pull $IMAGE_NAME 2>/dev/null || true
fi

# Run the container
if [ $# -eq 0 ]; then
    # Interactive mode if no arguments
    echo "Starting YouTube downloader in interactive mode..."
    echo "Image: $IMAGE_NAME"
    echo ""
    $DOCKER_CMD run -it --rm \
        -v "$(pwd)/downloads:/downloads${VOLUME_FLAGS}" \
        $IMAGE_NAME
else
    # Pass all arguments to the container
    $DOCKER_CMD run --rm \
        -v "$(pwd)/downloads:/downloads${VOLUME_FLAGS}" \
        $IMAGE_NAME "$@"
fi