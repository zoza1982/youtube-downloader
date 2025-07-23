#!/usr/bin/env python3
"""
Standalone entry point for PyInstaller
This avoids relative import issues
"""

import sys
import os

# Add the parent directory to sys.path so we can import ytd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ytd.cli import main

if __name__ == "__main__":
    sys.exit(main())