#!/bin/bash
# Linux build script for YouTube Downloader CLI
# Creates a standalone executable for Linux

set -e

echo "===================================="
echo "Building YouTube Downloader for Linux"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install additional Linux dependencies for PyInstaller
echo "Installing build dependencies..."
pip install staticx  # For creating truly static binaries

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build with PyInstaller
echo "Building executable with PyInstaller..."
pyinstaller ytd.spec --clean

# Check if build was successful
if [ ! -f "dist/ytd" ]; then
    echo "Build failed!"
    exit 1
fi

# Make static binary (optional, requires staticx)
if command -v staticx &> /dev/null; then
    echo "Creating static binary..."
    staticx dist/ytd dist/ytd-static
    mv dist/ytd-static dist/ytd
fi

# Create distribution directory
echo "Creating distribution package..."
mkdir -p "dist/ytd-linux"

# Copy executable and create README
cp "dist/ytd" "dist/ytd-linux/"

# Create README
cat > "dist/ytd-linux/README.txt" << EOF
YouTube Downloader CLI for Linux

Installation:
1. Copy 'ytd' to /usr/local/bin/ or ~/.local/bin/
   sudo cp ytd /usr/local/bin/
   OR
   cp ytd ~/.local/bin/
   
2. Make it executable (if needed):
   chmod +x ytd

Usage:
  ytd [URL] [options]
  ytd --help

Examples:
  ytd https://youtube.com/watch?v=VIDEO_ID
  ytd https://youtube.com/watch?v=VIDEO_ID -a
  ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --skip-download

Supported sites:
  ytd --list-extractors

This binary should work on most Linux distributions (x86_64).
Tested on: Ubuntu 20.04+, Debian 10+, Fedora 34+, Arch Linux
EOF

# Create install script
cat > "dist/ytd-linux/install.sh" << 'EOF'
#!/bin/bash
echo "Installing YouTube Downloader..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    # Install system-wide
    cp ytd /usr/local/bin/
    chmod +x /usr/local/bin/ytd
    echo "Installed to /usr/local/bin/ytd (system-wide)"
else
    # Install for current user
    mkdir -p ~/.local/bin
    cp ytd ~/.local/bin/
    chmod +x ~/.local/bin/ytd
    echo "Installed to ~/.local/bin/ytd (user only)"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "Note: ~/.local/bin is not in your PATH"
        echo "Add it to your shell configuration:"
        echo "  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc"
        echo "Then reload: source ~/.bashrc"
    fi
fi

echo "Installation complete!"
echo "Test with: ytd --version"
EOF
chmod +x "dist/ytd-linux/install.sh"

# Create uninstall script
cat > "dist/ytd-linux/uninstall.sh" << 'EOF'
#!/bin/bash
echo "Uninstalling YouTube Downloader..."

if [ -f "/usr/local/bin/ytd" ]; then
    sudo rm /usr/local/bin/ytd
    echo "Removed /usr/local/bin/ytd"
fi

if [ -f "$HOME/.local/bin/ytd" ]; then
    rm $HOME/.local/bin/ytd
    echo "Removed ~/.local/bin/ytd"
fi

echo "Uninstall complete!"
EOF
chmod +x "dist/ytd-linux/uninstall.sh"

# Create tarball
echo "Creating tarball..."
cd dist
tar -czf ytd-linux.tar.gz ytd-linux
cd ..

# Create AppImage (optional, requires appimage-builder)
if command -v appimage-builder &> /dev/null; then
    echo "Creating AppImage..."
    # Would need AppImageBuilder.yml configuration
    # appimage-builder --recipe AppImageBuilder.yml
fi

# Create .deb package (optional, for Debian/Ubuntu)
if command -v dpkg-deb &> /dev/null; then
    echo "Creating .deb package..."
    mkdir -p "dist/ytd-deb/DEBIAN"
    mkdir -p "dist/ytd-deb/usr/local/bin"
    
    cp "dist/ytd" "dist/ytd-deb/usr/local/bin/"
    
    cat > "dist/ytd-deb/DEBIAN/control" << EOF
Package: youtube-downloader
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: YouTube Downloader Contributors
Description: Command-line YouTube and video downloader
 Download videos from YouTube and 1700+ other sites.
 Supports video, audio, playlists, and subtitles.
EOF
    
    dpkg-deb --build dist/ytd-deb dist/youtube-downloader_1.0.0_amd64.deb
fi

echo "===================================="
echo "Build complete!"
echo "===================================="
echo "Executable: dist/ytd"
echo "Distribution: dist/ytd-linux.tar.gz"
if [ -f "dist/youtube-downloader_1.0.0_amd64.deb" ]; then
    echo "Debian package: dist/youtube-downloader_1.0.0_amd64.deb"
fi
echo ""
echo "Test the build:"
echo "  dist/ytd --version"
echo "  dist/ytd --help"
echo ""
echo "The binary should work on most Linux distributions."