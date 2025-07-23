# Building YouTube Downloader

This document explains how to build YouTube Downloader binaries for different platforms.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- git

### Platform-specific requirements

**Windows:**
- Visual Studio Build Tools or MinGW
- Windows 10 or higher

**macOS:**
- Xcode Command Line Tools
- macOS 10.15 or higher

**Linux:**
- GCC or Clang
- patchelf (for creating portable binaries)

## Quick Build

The easiest way to build is using the provided scripts:

```bash
# Build for current platform
./build_all.sh current

# Build for specific platform (if on that platform)
./build_all.sh windows
./build_all.sh macos
./build_all.sh linux
```

## Manual Build Steps

### 1. Set up environment

```bash
# Clone repository
git clone https://github.com/zoza1982/youtube-downloader.git
cd youtube-downloader

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Build with PyInstaller

```bash
# Build using spec file
pyinstaller ytd.spec --clean

# Or build manually
pyinstaller --onefile \
    --name ytd \
    --add-data "ytd:ytd" \
    --hidden-import yt_dlp.extractor \
    --collect-submodules yt_dlp.extractor \
    ytd/cli.py
```

### 3. Test the build

```bash
# Test executable
dist/ytd --version
dist/ytd --help
dist/ytd --list-extractors
```

## Build Output

Builds are created in the `dist/` directory:

- **Windows**: `ytd.exe`
- **macOS**: `ytd` (Unix executable)
- **Linux**: `ytd` (Unix executable)

## Creating Distributions

### Windows Distribution

```batch
:: Create distribution folder
mkdir dist\ytd-windows
copy dist\ytd.exe dist\ytd-windows\

:: Create ZIP
cd dist
powershell Compress-Archive -Path ytd-windows -DestinationPath ytd-windows.zip
```

### macOS Distribution

```bash
# Create distribution folder
mkdir -p dist/ytd-macos
cp dist/ytd dist/ytd-macos/

# Create ZIP
cd dist
zip -r ytd-macos.zip ytd-macos

# Create DMG (optional)
hdiutil create -volname "YouTube Downloader" -srcfolder ytd-macos -ov -format UDZO ytd-macos.dmg
```

### Linux Distribution

```bash
# Create distribution folder
mkdir -p dist/ytd-linux
cp dist/ytd dist/ytd-linux/

# Create tarball
cd dist
tar -czf ytd-linux.tar.gz ytd-linux

# Create .deb package (optional)
# See build_scripts/build_linux.sh for details
```

## Automated Builds

GitHub Actions automatically builds binaries when:
- A new version tag is pushed (e.g., `v1.0.0`)
- Manually triggered via Actions tab

To create a new release:

```bash
# Tag a new version
git tag v1.0.0
git push origin v1.0.0

# This triggers the release workflow which:
# 1. Builds binaries for all platforms
# 2. Creates a GitHub release
# 3. Uploads all artifacts
```

## Build Optimization

### Reducing Binary Size

1. **Use UPX compression** (enabled by default in spec file)
2. **Exclude unnecessary modules** in spec file
3. **Use `--onefile` mode** for single executable

### Improving Startup Time

1. **Avoid `--onefile` mode** if startup time is critical
2. **Use `--onedir` mode** for faster startup
3. **Pre-compile Python files** with `-O` flag

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure all hidden imports are specified in spec file
- Use `--collect-submodules yt_dlp.extractor`

**Large binary size:**
- Check for unnecessary included modules
- Enable UPX compression
- Strip debug symbols on Unix platforms

**Antivirus false positives:**
- Sign binaries (Windows/macOS)
- Submit to antivirus vendors for whitelisting
- Use `--windowed` mode to reduce false positives

**FFmpeg not found:**
- The binary includes ffmpeg auto-download functionality
- Users can install system ffmpeg for better performance

### Platform-specific Issues

**Windows:**
- May need to install Visual C++ Redistributables
- Use `--no-console` for GUI applications only

**macOS:**
- First run may be slow due to code signing verification
- May need to allow in System Preferences > Security & Privacy

**Linux:**
- Use `staticx` for truly portable binaries
- Test on older distributions for compatibility

## Security Considerations

1. **Code Signing** (recommended for distribution):
   - Windows: Use SignTool with code signing certificate
   - macOS: Use codesign with Apple Developer ID
   - Linux: Use GPG signatures for packages

2. **Reproducible Builds**:
   - Use specific dependency versions
   - Document build environment
   - Use deterministic build flags

3. **Binary Verification**:
   - Provide SHA256 checksums
   - Sign releases with GPG
   - Use GitHub's built-in attestation

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Packaging Guide](https://packaging.python.org/)