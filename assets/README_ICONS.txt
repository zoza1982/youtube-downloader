
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
