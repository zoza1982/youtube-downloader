@echo off
:: Windows build script for YouTube Downloader CLI
:: Creates a standalone executable for Windows

echo ====================================
echo Building YouTube Downloader for Windows
echo ====================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install -r requirements-dev.txt

:: Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

:: Build with PyInstaller
echo Building executable with PyInstaller...
pyinstaller ytd.spec --clean

:: Check if build was successful
if not exist "dist\ytd.exe" (
    echo Build failed!
    exit /b 1
)

:: Create distribution directory
echo Creating distribution package...
if not exist "dist\ytd-windows" mkdir "dist\ytd-windows"

:: Copy executable and create README
copy "dist\ytd.exe" "dist\ytd-windows\"
echo YouTube Downloader CLI for Windows > "dist\ytd-windows\README.txt"
echo. >> "dist\ytd-windows\README.txt"
echo Usage: ytd.exe [URL] [options] >> "dist\ytd-windows\README.txt"
echo Run ytd.exe --help for more information >> "dist\ytd-windows\README.txt"

:: Create ZIP file
echo Creating ZIP archive...
cd dist
powershell -command "Compress-Archive -Path 'ytd-windows' -DestinationPath 'ytd-windows.zip'"
cd ..

echo ====================================
echo Build complete!
echo ====================================
echo Executable: dist\ytd.exe
echo Distribution: dist\ytd-windows.zip
echo.
echo Test the build:
echo   dist\ytd.exe --version
echo   dist\ytd.exe --help