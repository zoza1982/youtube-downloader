#!/usr/bin/env python3
"""
Generate placeholder icons for YouTube Downloader
Creates simple icons for Windows (.ico) and macOS (.icns)
"""

import os
from pathlib import Path

# Create assets directory
assets_dir = Path(__file__).parent
assets_dir.mkdir(exist_ok=True)

# Icon information
ICON_INFO = """
YouTube Downloader Icons

To create proper icons for your application:

1. Windows Icon (.ico):
   - Create a 256x256 PNG image with your logo
   - Use an online converter or tool like ImageMagick:
     convert logo.png -resize 16x16 icon-16.png
     convert logo.png -resize 32x32 icon-32.png
     convert logo.png -resize 48x48 icon-48.png
     convert logo.png -resize 256x256 icon-256.png
     convert icon-16.png icon-32.png icon-48.png icon-256.png icon.ico

2. macOS Icon (.icns):
   - Create icons at these sizes: 16x16, 32x32, 128x128, 256x256, 512x512
   - Use iconutil on macOS:
     mkdir icon.iconset
     # Copy your PNG files to icon.iconset with names like:
     # icon_16x16.png, icon_32x32.png, icon_128x128.png, etc.
     iconutil -c icns icon.iconset

3. Recommended Design:
   - Simple, recognizable design
   - Works well at small sizes
   - High contrast
   - No thin lines that disappear when scaled down

4. Free Icon Resources:
   - FontAwesome icons
   - Material Design Icons
   - Flaticon (with attribution)
   - Icons8

5. Icon Generators:
   - https://www.favicon-generator.org/
   - https://icon.kitchen/
   - https://makeappicon.com/

For now, the build will work without icons, but adding them will make
your application look more professional.
"""

# Create placeholder files and info
info_file = assets_dir / "README_ICONS.txt"
info_file.write_text(ICON_INFO)

print("Icon information created in assets/README_ICONS.txt")
print("\nTo add icons to your builds:")
print("1. Create icon.ico for Windows")
print("2. Create icon.icns for macOS")
print("3. Place them in the assets/ directory")
print("\nThe PyInstaller spec file will automatically use them if present.")