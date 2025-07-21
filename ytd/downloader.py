"""Core downloader module using yt-dlp"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import yt_dlp
from tqdm import tqdm
from .convert_subtitles import convert_file


class YouTubeDownloader:
    """YouTube video downloader using yt-dlp"""
    
    def __init__(self, options: Dict[str, Any], logger: Optional[logging.Logger] = None):
        """Initialize downloader with options and logger"""
        self.options = options
        self.logger = logger or logging.getLogger(__name__)
        self.output_dir = Path(options.get('output', '.')).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Progress bar
        self.pbar = None
        self.last_percentage = 0
        
    def _get_ydl_opts(self, additional_opts: Optional[Dict] = None) -> Dict:
        """Get yt-dlp options based on configuration"""
        opts = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'logger': self.logger,
            'quiet': self.options.get('quiet', False),
            'no_warnings': self.options.get('quiet', False),
            'ignoreerrors': True,  # Continue on download errors
            'continuedl': True,  # Resume downloads
            'noprogress': self.options.get('no_progress', False),
        }
        
        # Format selection
        format_spec = self.options.get('format', 'best')
        if self.options.get('audio_only'):
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.options.get('audio_format', 'mp3'),
                'preferredquality': '192',
            }]
        else:
            opts['format'] = format_spec
        
        # Subtitles
        if self.options.get('subtitles'):
            opts['writesubtitles'] = True
            # Always try to get auto-generated subtitles as fallback
            opts['writeautomaticsub'] = True
            
            # Handle subtitle languages
            sub_langs = self.options.get('sub_langs', 'en')
            if sub_langs.lower() == 'all':
                # Download all available subtitles
                opts['subtitleslangs'] = ['all']
            else:
                # Download specific languages
                opts['subtitleslangs'] = sub_langs.split(',')
        
        # Metadata and thumbnail
        if self.options.get('metadata'):
            opts['addmetadata'] = True
        if self.options.get('thumbnail'):
            opts['writethumbnail'] = True
            opts['postprocessors'] = opts.get('postprocessors', []) + [{
                'key': 'FFmpegEmbedSubtitle',
            }, {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }, {
                'key': 'EmbedThumbnail',
            }]
        
        # Rate limiting
        if self.options.get('limit_rate'):
            opts['ratelimit'] = self._parse_rate_limit(self.options['limit_rate'])
        
        # Concurrent downloads
        if self.options.get('concurrent'):
            opts['concurrent_fragment_downloads'] = self.options['concurrent']
        
        # Archive file
        if self.options.get('archive'):
            opts['download_archive'] = self.options['archive']
        
        # Cookies
        if self.options.get('cookies'):
            opts['cookiefile'] = self.options['cookies']
        
        # Custom filename
        if self.options.get('filename'):
            opts['outtmpl'] = str(self.output_dir / self.options['filename'])
        
        # Playlist options
        if self.options.get('playlist_items'):
            opts['playlist_items'] = self.options['playlist_items']
        
        # Skip download option (useful for subtitles only)
        if self.options.get('skip_download'):
            opts['skip_download'] = True
        
        # Subtitle format preference
        if self.options.get('subtitles'):
            # Prefer VTT format by default (better support for styling)
            opts['subtitlesformat'] = 'vtt/srt/best'
        
        # Merge additional options
        if additional_opts:
            opts.update(additional_opts)
        
        return opts
    
    def _parse_rate_limit(self, rate: str) -> int:
        """Parse rate limit string to bytes"""
        rate = rate.upper()
        multipliers = {'K': 1024, 'M': 1024 * 1024}
        
        for suffix, multiplier in multipliers.items():
            if rate.endswith(suffix):
                return int(float(rate[:-1]) * multiplier)
        
        return int(rate)
    
    def _progress_hook(self, d: Dict) -> None:
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            if not self.options.get('no_progress') and not self.options.get('quiet'):
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    percentage = (downloaded / total) * 100
                    
                    # Create progress bar if not exists
                    if self.pbar is None:
                        self.pbar = tqdm(
                            total=100,
                            desc=d.get('filename', 'Downloading').split('/')[-1][:50],
                            unit='%',
                            ncols=80
                        )
                    
                    # Update progress
                    progress = percentage - self.last_percentage
                    if progress > 0:
                        self.pbar.update(progress)
                        self.last_percentage = percentage
                    
                    # Add speed and ETA info
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    if speed and eta:
                        self.pbar.set_postfix({
                            'speed': f"{speed/1024/1024:.1f}MB/s",
                            'eta': f"{eta}s"
                        })
        
        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.update(100 - self.last_percentage)
                self.pbar.close()
                self.pbar = None
                self.last_percentage = 0
            self.logger.info(f"Download finished: {d.get('filename', 'Unknown')}")
    
    def _handle_subtitle_conversion(self) -> None:
        """Convert downloaded subtitles if requested"""
        convert_format = self.options.get('convert_subs', 'keep')
        if convert_format == 'keep':
            return
        
        # Find downloaded subtitle files
        for subtitle_file in self.output_dir.glob('*.vtt'):
            if convert_format == 'srt':
                try:
                    srt_file = convert_file(subtitle_file)
                    if srt_file:
                        self.logger.info(f"Converted subtitle: {subtitle_file.name} → {srt_file.name}")
                        # Optionally remove the original VTT file
                        # subtitle_file.unlink()
                except Exception as e:
                    self.logger.error(f"Failed to convert {subtitle_file}: {e}")
    
    def download_video(self, url: str) -> bool:
        """Download a single video"""
        try:
            opts = self._get_ydl_opts()
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                self.logger.info(f"Downloading video: {url}")
                ydl.download([url])
            
            # Handle subtitle conversion if requested
            if self.options.get('subtitles'):
                self._handle_subtitle_conversion()
            
            return True
        except Exception as e:
            self.logger.error(f"Error downloading video: {str(e)}")
            return False
    
    def download_playlist(self, url: str) -> bool:
        """Download entire playlist"""
        try:
            opts = self._get_ydl_opts({
                'playlistreverse': False,
                'playlistrandom': False,
            })
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                self.logger.info(f"Downloading playlist: {url}")
                ydl.download([url])
            
            # Handle subtitle conversion if requested
            if self.options.get('subtitles'):
                self._handle_subtitle_conversion()
            
            return True
        except Exception as e:
            self.logger.error(f"Error downloading playlist: {str(e)}")
            return False
    
    def download_audio(self, url: str) -> bool:
        """Download audio only"""
        try:
            # Audio-only option is already handled in _get_ydl_opts
            opts = self._get_ydl_opts()
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                self.logger.info(f"Downloading audio: {url}")
                ydl.download([url])
            
            # Handle subtitle conversion if requested
            if self.options.get('subtitles'):
                self._handle_subtitle_conversion()
            
            return True
        except Exception as e:
            self.logger.error(f"Error downloading audio: {str(e)}")
            return False
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """Get video information without downloading"""
        try:
            opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            self.logger.error(f"Error getting video info: {str(e)}")
            return None
    
    def list_formats(self, url: str) -> List[str]:
        """List available formats for a video"""
        try:
            opts = {
                'quiet': True,
                'no_warnings': True,
                'listformats': True,
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                if 'formats' in info:
                    for f in info['formats']:
                        format_str = f"{f.get('format_id', 'N/A')} - "
                        format_str += f"{f.get('ext', 'N/A')} "
                        
                        if f.get('height'):
                            format_str += f"{f['height']}p "
                        
                        if f.get('filesize'):
                            size_mb = f['filesize'] / 1024 / 1024
                            format_str += f"({size_mb:.1f}MB) "
                        
                        if f.get('tbr'):
                            format_str += f"[{f['tbr']:.0f}k] "
                        
                        format_str += f.get('format_note', '')
                        formats.append(format_str.strip())
                
                return formats
        except Exception as e:
            self.logger.error(f"Error listing formats: {str(e)}")
            return []
    
    def list_subtitles(self, url: str) -> Dict[str, Dict[str, Any]]:
        """List all available subtitles including auto-generated ones"""
        try:
            opts = {
                'quiet': True,
                'no_warnings': True,
                'listsubtitles': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                subtitles = {}
                
                # Manual subtitles
                if 'subtitles' in info and info['subtitles']:
                    for lang, sub_info in info['subtitles'].items():
                        subtitles[lang] = {
                            'name': sub_info[0].get('name', lang),
                            'type': 'manual',
                            'formats': [s.get('ext', 'unknown') for s in sub_info]
                        }
                
                # Auto-generated subtitles
                if 'automatic_captions' in info and info['automatic_captions']:
                    for lang, sub_info in info['automatic_captions'].items():
                        subtitles[f"{lang} (auto)"] = {
                            'name': sub_info[0].get('name', lang),
                            'type': 'auto-generated',
                            'lang_code': lang,
                            'formats': [s.get('ext', 'unknown') for s in sub_info]
                        }
                
                return subtitles
        except Exception as e:
            self.logger.error(f"Error listing subtitles: {str(e)}")
            return {}
    
    def update(self) -> bool:
        """Update yt-dlp to the latest version"""
        try:
            # Try to update using pip
            result = subprocess.run(
                ['pip', 'install', '--upgrade', 'yt-dlp'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("yt-dlp updated successfully")
                return True
            else:
                self.logger.error(f"Failed to update yt-dlp: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"Error updating yt-dlp: {str(e)}")
            return False