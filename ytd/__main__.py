#!/usr/bin/env python3
"""
Allow running the package as a module: python -m ytd
"""

from .cli import main

if __name__ == "__main__":
    exit(main())