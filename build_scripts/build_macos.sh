#!/bin/bash
# macOS build script for YouTube Downloader CLI
# Creates a standalone executable for macOS

set -e

echo "===================================="
echo "Building YouTube Downloader for macOS"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
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

# Create distribution directory
echo "Creating distribution package..."
mkdir -p "dist/ytd-macos"

# Copy executable and create README
cp "dist/ytd" "dist/ytd-macos/"
if [ -d "dist/ytd.app" ]; then
    cp -r "dist/ytd.app" "dist/ytd-macos/"
fi

# Create README
cat > "dist/ytd-macos/README.txt" << EOF
YouTube Downloader CLI for macOS

Installation:
1. Copy 'ytd' to /usr/local/bin/ or add to your PATH
   sudo cp ytd /usr/local/bin/
   
2. Make it executable (if needed):
   chmod +x ytd

Usage:
  ytd [URL] [options]
  ytd --help

Examples:
  ytd https://youtube.com/watch?v=VIDEO_ID
  ytd https://youtube.com/watch?v=VIDEO_ID -a
  ytd https://youtube.com/watch?v=VIDEO_ID -s --sub-langs en --skip-download

Note: The first run may be slow as macOS verifies the binary.
If you see a security warning, go to System Preferences > Security & Privacy
and click "Open Anyway".
EOF

# Create install script
cat > "dist/ytd-macos/install.sh" << 'EOF'
#!/bin/bash
echo "Installing YouTube Downloader..."
if [ -w "/usr/local/bin" ]; then
    cp ytd /usr/local/bin/
    chmod +x /usr/local/bin/ytd
    echo "Installed to /usr/local/bin/ytd"
else
    echo "Installing to ~/bin/ (requires adding to PATH)"
    mkdir -p ~/bin
    cp ytd ~/bin/
    chmod +x ~/bin/ytd
    echo "Installed to ~/bin/ytd"
    echo "Add ~/bin to your PATH if not already done:"
    echo "  echo 'export PATH=\$HOME/bin:\$PATH' >> ~/.zshrc"
fi
echo "Installation complete!"
EOF
chmod +x "dist/ytd-macos/install.sh"

# Create ZIP file
echo "Creating ZIP archive..."
cd dist
zip -r ytd-macos.zip ytd-macos
cd ..

# Create DMG (optional, requires hdiutil)
if command -v hdiutil &> /dev/null; then
    echo "Creating DMG..."
    hdiutil create -volname "YouTube Downloader" -srcfolder "dist/ytd-macos" -ov -format UDZO "dist/ytd-macos.dmg"
fi

echo "===================================="
echo "Build complete!"
echo "===================================="
echo "Executable: dist/ytd"
echo "Distribution: dist/ytd-macos.zip"
if [ -f "dist/ytd-macos.dmg" ]; then
    echo "DMG: dist/ytd-macos.dmg"
fi
echo ""
echo "Test the build:"
echo "  dist/ytd --version"
echo "  dist/ytd --help"