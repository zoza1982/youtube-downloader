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

# Set image name
IMAGE_NAME="youtube-downloader"

# Create downloads directory if it doesn't exist
mkdir -p downloads

# Check if image exists, build if not
if ! $DOCKER_CMD image inspect $IMAGE_NAME &> /dev/null; then
    echo "Building YouTube downloader image..."
    $DOCKER_CMD build -t $IMAGE_NAME .
fi

# Run the container
if [ $# -eq 0 ]; then
    # Interactive mode if no arguments
    echo "Starting YouTube downloader in interactive mode..."
    $DOCKER_CMD run -it --rm \
        -v "$(pwd)/downloads:/downloads${VOLUME_FLAGS}" \
        $IMAGE_NAME
else
    # Pass all arguments to the container
    $DOCKER_CMD run --rm \
        -v "$(pwd)/downloads:/downloads${VOLUME_FLAGS}" \
        $IMAGE_NAME "$@"
fi