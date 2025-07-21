"""Utility functions for YouTube Downloader"""

import logging
import re
import yaml
from pathlib import Path
from typing import Dict, Any
from argparse import Namespace


def setup_logger(verbose: bool = False, quiet: bool = False) -> logging.Logger:
    """Setup and configure logger"""
    logger = logging.getLogger('ytd')
    
    # Clear existing handlers
    logger.handlers.clear()
    
    if quiet:
        logger.setLevel(logging.ERROR)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Format based on verbosity
    if verbose:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
        return config
    except Exception as e:
        logging.error(f"Error loading config file: {str(e)}")
        return {}


def merge_options(config: Dict[str, Any], args: Namespace) -> Dict[str, Any]:
    """Merge command-line arguments with config file options"""
    # Convert args to dict
    args_dict = vars(args).copy()
    
    # Map config keys to argument names
    config_mapping = {
        'default_output': 'output',
        'default_format': 'format',
        'audio_format': 'audio_format',
        'subtitles': 'subtitles',
        'metadata': 'metadata',
        'concurrent_downloads': 'concurrent',
        'rate_limit': 'limit_rate',
    }
    
    # Start with config values
    options = {}
    for config_key, arg_key in config_mapping.items():
        if config_key in config:
            options[arg_key] = config[config_key]
    
    # Override with command-line arguments
    for key, value in args_dict.items():
        if value is not None:
            options[key] = value
    
    return options


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # Limit length
    max_length = 255
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        name = name[:max_length - len(ext) - 1]
        filename = f"{name}.{ext}" if ext else name
    
    return filename.strip()


def format_bytes(bytes: int) -> str:
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours}h {minutes}m {seconds}s"


def parse_playlist_items(items_spec: str) -> list:
    """Parse playlist items specification (e.g., "1-3,7,10-13")"""
    items = []
    parts = items_spec.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            items.extend(range(int(start), int(end) + 1))
        else:
            items.append(int(part))
    
    return sorted(set(items))


def get_default_config_path() -> Path:
    """Get default configuration file path"""
    config_dir = Path.home() / '.config' / 'ytd'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.yaml'


def create_default_config() -> None:
    """Create default configuration file"""
    default_config = {
        'default_output': '~/Videos/YouTube',
        'default_format': 'best',
        'audio_format': 'mp3',
        'subtitles': False,
        'metadata': True,
        'concurrent_downloads': 3,
        'rate_limit': None,
    }
    
    config_path = get_default_config_path()
    if not config_path.exists():
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        logging.info(f"Created default config at: {config_path}")