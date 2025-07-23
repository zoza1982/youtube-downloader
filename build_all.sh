#!/bin/bash
# Master build script for YouTube Downloader CLI
# Builds for all supported platforms

set -e

echo "========================================"
echo "YouTube Downloader Multi-Platform Builder"
echo "========================================"

# Detect current platform
PLATFORM=$(uname -s)
case "$PLATFORM" in
    Linux*)     CURRENT_OS="linux";;
    Darwin*)    CURRENT_OS="macos";;
    MINGW*|CYGWIN*|MSYS*) CURRENT_OS="windows";;
    *)          CURRENT_OS="unknown";;
esac

echo "Current platform: $CURRENT_OS"
echo ""

# Function to display usage
usage() {
    echo "Usage: $0 [platform]"
    echo ""
    echo "Platforms:"
    echo "  all      - Build for all platforms (requires cross-compilation setup)"
    echo "  current  - Build for current platform only"
    echo "  windows  - Build for Windows"
    echo "  macos    - Build for macOS"
    echo "  linux    - Build for Linux"
    echo ""
    echo "Examples:"
    echo "  $0 current    # Build for current platform"
    echo "  $0 all        # Build for all platforms"
    echo "  $0 linux      # Build for Linux only"
    exit 1
}

# Function to build for current platform
build_current() {
    echo "Building for current platform ($CURRENT_OS)..."
    case "$CURRENT_OS" in
        linux)
            bash build_scripts/build_linux.sh
            ;;
        macos)
            bash build_scripts/build_macos.sh
            ;;
        windows)
            cmd //c build_scripts\\build_windows.bat
            ;;
        *)
            echo "Error: Unknown platform"
            exit 1
            ;;
    esac
}

# Function to check if wine is installed (for cross-compiling to Windows)
check_wine() {
    if ! command -v wine &> /dev/null; then
        echo "Warning: Wine is not installed. Cannot cross-compile for Windows."
        echo "Install wine to enable Windows builds on Linux/macOS:"
        echo "  Ubuntu/Debian: sudo apt install wine wine64"
        echo "  macOS: brew install wine-stable"
        return 1
    fi
    return 0
}

# Parse arguments
if [ $# -eq 0 ]; then
    usage
fi

TARGET=$1

case "$TARGET" in
    current)
        build_current
        ;;
    
    all)
        echo "Building for all platforms..."
        echo "Note: Cross-compilation support is limited."
        echo "For best results, build on each target platform."
        echo ""
        
        # Always build for current platform
        build_current
        
        # Attempt cross-compilation if tools are available
        if [ "$CURRENT_OS" != "windows" ]; then
            if check_wine; then
                echo ""
                echo "Attempting Windows cross-compilation with Wine..."
                echo "Note: This is experimental and may not work properly."
                # Would need wine-pyinstaller setup
            fi
        fi
        
        echo ""
        echo "========================================"
        echo "Build Summary:"
        echo "========================================"
        echo "✓ $CURRENT_OS build complete"
        echo ""
        echo "For other platforms, please build natively on those systems"
        echo "or use GitHub Actions for automated multi-platform builds."
        ;;
    
    windows|macos|linux)
        if [ "$TARGET" = "$CURRENT_OS" ]; then
            build_current
        else
            echo "Cross-compilation from $CURRENT_OS to $TARGET is not directly supported."
            echo "Please build on the target platform or use GitHub Actions."
            echo ""
            echo "Alternatively, you can use Docker for Linux builds:"
            echo "  docker run -v \$(pwd):/app python:3.11 bash /app/build_scripts/build_linux.sh"
        fi
        ;;
    
    *)
        usage
        ;;
esac

# Summary
echo ""
echo "========================================"
echo "Build artifacts location: dist/"
echo "========================================"
ls -la dist/ 2>/dev/null || echo "No builds found"

# Create release notes template
if [ -d "dist" ]; then
    cat > "dist/RELEASE_NOTES.md" << EOF
# YouTube Downloader CLI - Release Notes

## Version 1.0.0

### Features
- Download videos from YouTube and 1700+ other sites
- Extract audio in various formats (MP3, M4A, OPUS, etc.)
- Download playlists with customizable selection
- Download and convert subtitles (VTT to SRT)
- Merge subtitles with videos
- Resume interrupted downloads
- Progress tracking with speed and ETA

### Installation

#### Windows
1. Download \`ytd-windows.zip\`
2. Extract to desired location
3. Add to PATH or run from extracted directory

#### macOS
1. Download \`ytd-macos.zip\`
2. Extract and run \`install.sh\`
3. Or manually copy \`ytd\` to \`/usr/local/bin/\`

#### Linux
1. Download \`ytd-linux.tar.gz\`
2. Extract and run \`install.sh\`
3. Or manually copy \`ytd\` to \`/usr/local/bin/\`

### Usage
\`\`\`bash
ytd https://youtube.com/watch?v=VIDEO_ID
ytd https://youtube.com/watch?v=VIDEO_ID -a
ytd --help
\`\`\`

### System Requirements
- No Python installation required
- FFmpeg recommended for full functionality
- 64-bit operating system

### Known Issues
- First run on macOS may be slow due to code signing verification
- Some antivirus software may flag the executable (false positive)
EOF
fi

echo ""
echo "Build process complete!"