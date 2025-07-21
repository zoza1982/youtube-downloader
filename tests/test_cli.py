"""Tests for CLI module"""

import pytest
from unittest.mock import patch, MagicMock
from ytd.cli import create_parser, validate_url, main


class TestCLI:
    """Test CLI functionality"""
    
    def test_create_parser(self):
        """Test parser creation"""
        parser = create_parser()
        assert parser is not None
        
        # Test basic parsing
        args = parser.parse_args(['https://youtube.com/watch?v=test'])
        assert args.url == 'https://youtube.com/watch?v=test'
        assert args.output == '.'
        assert args.format == 'best'
        assert args.audio_only is False
    
    def test_parser_with_options(self):
        """Test parser with various options"""
        parser = create_parser()
        
        args = parser.parse_args([
            'https://youtube.com/watch?v=test',
            '-o', '~/Videos',
            '-f', '1080p',
            '-a',
            '--audio-format', 'mp3',
            '-v'
        ])
        
        assert args.output == '~/Videos'
        assert args.format == '1080p'
        assert args.audio_only is True
        assert args.audio_format == 'mp3'
        assert args.verbose is True
    
    def test_validate_url(self):
        """Test URL validation"""
        # Valid URLs
        assert validate_url('https://youtube.com/watch?v=test') is True
        assert validate_url('https://www.youtube.com/watch?v=test') is True
        assert validate_url('https://youtu.be/test') is True
        assert validate_url('https://youtube-nocookie.com/watch?v=test') is True
        
        # Invalid URLs
        assert validate_url('not-a-url') is False
        assert validate_url('https://example.com') is False
        assert validate_url('') is False
    
    @patch('ytd.cli.YouTubeDownloader')
    def test_main_success(self, mock_downloader):
        """Test successful main execution"""
        mock_instance = MagicMock()
        mock_instance.download_video.return_value = True
        mock_downloader.return_value = mock_instance
        
        with patch('sys.argv', ['ytd', 'https://youtube.com/watch?v=test']):
            result = main()
            assert result == 0
            mock_instance.download_video.assert_called_once()
    
    @patch('ytd.cli.YouTubeDownloader')
    def test_main_invalid_url(self, mock_downloader):
        """Test main with invalid URL"""
        with patch('sys.argv', ['ytd', 'not-a-url']):
            result = main()
            assert result == 1
            mock_downloader.assert_not_called()
    
    @patch('ytd.cli.YouTubeDownloader')
    def test_main_download_failure(self, mock_downloader):
        """Test main with download failure"""
        mock_instance = MagicMock()
        mock_instance.download_video.return_value = False
        mock_downloader.return_value = mock_instance
        
        with patch('sys.argv', ['ytd', 'https://youtube.com/watch?v=test']):
            result = main()
            assert result == 1