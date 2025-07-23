# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for YouTube Downloader CLI
Builds a single executable binary for distribution
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Determine if we're building for Windows
is_windows = sys.platform.startswith('win')
is_macos = sys.platform == 'darwin'
is_linux = sys.platform.startswith('linux')

# Application metadata
APP_NAME = 'ytd'
APP_VERSION = '1.0.0'
APP_DESCRIPTION = 'YouTube Downloader CLI - Download videos from YouTube and 1700+ sites'

# Collect all yt-dlp extractors (needed for multi-site support)
hiddenimports = collect_submodules('yt_dlp.extractor') + collect_submodules('yt_dlp.downloader') + collect_submodules('yt_dlp.postprocessor') + [
    'yt_dlp',
    'yt_dlp.downloader',
    'yt_dlp.postprocessor',
    'yt_dlp.extractor.common',
    'yt_dlp.extractor.generic',
    'yt_dlp.utils',
    'yt_dlp.options',
    'yt_dlp.version',
    'yt_dlp.YoutubeDL',
    'certifi',
    'brotli',
    'mutagen',
    'websockets',
    'secretstorage',
    'validators',
    'tqdm',
    'colorama',
    'yaml',
]

# Data files to include
datas = collect_data_files('yt_dlp') + collect_data_files('certifi')

# Binary files to include (platform-specific)
binaries = []

# Platform-specific configurations
if is_windows:
    # Windows-specific settings
    console = True
    icon = 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None
    
elif is_macos:
    # macOS-specific settings
    console = True
    icon = 'assets/icon.icns' if os.path.exists('assets/icon.icns') else None
    
else:
    # Linux-specific settings
    console = True
    icon = None

# Analysis configuration
a = Analysis(
    ['ytd_main.py'],  # Use standalone entry point to avoid import issues
    pathex=[os.path.abspath('.')],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'pygame',
        'sphinx',
        'pytest',
        'mypy',
        'black',
        'flake8',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove unnecessary binaries to reduce size
a.binaries = [x for x in a.binaries if not x[0].startswith('api-ms-win')]

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

# Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=not is_windows,  # Strip symbols on Unix platforms
    upx=True,  # Use UPX compression if available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=console,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)

# Platform-specific post-processing
if is_macos:
    # Create macOS app bundle
    app = BUNDLE(
        exe,
        name=f'{APP_NAME}.app',
        icon=icon,
        bundle_identifier='com.github.youtube-downloader',
        info_plist={
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': 'YouTube Downloader',
            'CFBundleGetInfoString': APP_DESCRIPTION,
            'CFBundleIdentifier': 'com.github.youtube-downloader',
            'CFBundleVersion': APP_VERSION,
            'CFBundleShortVersionString': APP_VERSION,
            'NSHighResolutionCapable': True,
        },
    )