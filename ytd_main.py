#!/usr/bin/env python3
"""
Standalone entry point for PyInstaller
This avoids relative import issues
"""

import sys
import os

# Handle Windows encoding issues early
if sys.platform.startswith('win'):
    try:
        # Set UTF-8 encoding for better Unicode support on Windows
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
        # Also set console code page to UTF-8 if possible
        os.system('chcp 65001 >nul 2>&1')
    except:
        # If that fails, the safe_print function will handle it
        pass

# Add the parent directory to sys.path so we can import ytd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ytd.cli import main

if __name__ == "__main__":
    sys.exit(main())