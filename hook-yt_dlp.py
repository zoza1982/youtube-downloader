"""
PyInstaller hook for yt-dlp
Ensures all extractors and dependencies are included in the build
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all extractors
hiddenimports = collect_submodules('yt_dlp.extractor')

# Add other important submodules
hiddenimports += [
    'yt_dlp.downloader.common',
    'yt_dlp.downloader.dash',
    'yt_dlp.downloader.f4m',
    'yt_dlp.downloader.hls',
    'yt_dlp.downloader.http',
    'yt_dlp.downloader.rtmp',
    'yt_dlp.downloader.rtsp',
    'yt_dlp.downloader.ism',
    'yt_dlp.downloader.mhtml',
    'yt_dlp.downloader.niconico',
    'yt_dlp.downloader.websocket',
    'yt_dlp.downloader.youtube_live_chat',
    'yt_dlp.downloader.external',
    'yt_dlp.postprocessor.common',
    'yt_dlp.postprocessor.embedthumbnail',
    'yt_dlp.postprocessor.exec',
    'yt_dlp.postprocessor.ffmpeg',
    'yt_dlp.postprocessor.metadataparser',
    'yt_dlp.postprocessor.modify_chapters',
    'yt_dlp.postprocessor.movefilesafterdownload',
    'yt_dlp.postprocessor.sponskrub',
    'yt_dlp.postprocessor.sponsorblock',
    'yt_dlp.postprocessor.xattrpp',
]

# Collect data files (like certificates)
datas = collect_data_files('yt_dlp')