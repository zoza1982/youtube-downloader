"""Setup configuration for YouTube Downloader"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from VERSION file
version_path = Path(__file__).parent / "VERSION"
version = "1.0.0"
if version_path.exists():
    version = version_path.read_text().strip()

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [line.strip() for line in requirements_path.read_text().splitlines() 
                   if line.strip() and not line.startswith('#')]

setup(
    name="youtube-downloader-cli",
    version=version,
    author="YouTube Downloader Contributors",
    author_email="",
    description="A powerful command-line YouTube video downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtube-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ytd=ytd.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)