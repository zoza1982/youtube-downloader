#!/bin/bash
set -e

# Check if running without arguments or with bash/sh
if [ $# -eq 0 ] || [ "$1" = "bash" ] || [ "$1" = "sh" ]; then
    echo "YouTube Downloader CLI - Docker Container"
    echo "========================================="
    echo ""
    echo "Usage examples:"
    echo "  ytd https://youtube.com/watch?v=VIDEO_ID"
    echo "  ytd https://youtube.com/watch?v=VIDEO_ID -a"
    echo "  ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en"
    echo ""
    echo "Downloads will be saved to /downloads (mounted from host)"
    echo ""
    
    if [ "$1" = "bash" ] || [ "$1" = "sh" ]; then
        exec "$@"
    else
        # Start interactive bash if no args
        exec bash
    fi
fi

# If first argument looks like a URL, run ytd
if [[ "$1" == http* ]] || [[ "$1" == *.youtube.com* ]]; then
    exec ytd "$@"
else
    # Otherwise, execute whatever command was provided
    exec "$@"
fi