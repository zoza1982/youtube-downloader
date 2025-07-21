#!/bin/bash
# Test script for YouTube Downloader CLI

echo "YouTube Downloader CLI Test Script"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}Error: Virtual environment not activated${NC}"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Check if ytd is installed
if ! command -v ytd &> /dev/null; then
    echo -e "${RED}Error: ytd command not found${NC}"
    echo "Please run: pip install -e ."
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo -e "${GREEN}✓ ytd command found${NC}"
echo ""

# Test 1: Version check
echo "Test 1: Version Check"
ytd --version
echo ""

# Test 2: Help display
echo "Test 2: Help Display (first 10 lines)"
ytd --help | head -10
echo "..."
echo ""

# Test 3: List formats (using a known video)
echo "Test 3: List Formats"
echo "Command: ytd https://www.youtube.com/watch?v=dQw4w9WgXcQ --list-formats"
echo "(This would list available formats for Rick Astley - Never Gonna Give You Up)"
echo ""

# Test 4: Dry run examples
echo "Test 4: Example Commands (not executed)"
echo "--------------------------------------"
echo ""

echo "Download video:"
echo "  ytd https://youtube.com/watch?v=VIDEO_ID"
echo ""

echo "Download audio only as MP3:"
echo "  ytd https://youtube.com/watch?v=VIDEO_ID -a"
echo ""

echo "Download to specific directory:"
echo "  ytd https://youtube.com/watch?v=VIDEO_ID -o ~/Downloads"
echo ""

echo "Download with subtitles:"
echo "  ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en,es"
echo ""

echo "Download playlist:"
echo "  ytd https://youtube.com/playlist?list=PLAYLIST_ID -p"
echo ""

echo -e "${GREEN}All tests completed!${NC}"
echo ""
echo "To actually download a video, run ytd with a real YouTube URL."