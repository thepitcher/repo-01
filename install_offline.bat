@echo off
REM Offline installation script for TFS Python Client
REM Compatible with Azure DevOps Server 2020 Update 1.1

echo ======================================================================
echo TFS Python Client - Offline Installation
echo Azure DevOps Server 2020 Update 1.1 Compatible
echo ======================================================================
echo.

REM Check if lib folder exists
if not exist "lib" (
    echo Error: lib folder not found!
    echo Please ensure you are running this script from the project root directory.
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo Using Python:
python --version
echo.

REM Step 1: Install build tools
echo Step 1/2: Installing build tools (pip, setuptools, wheel)...
python -m pip install --no-index --find-links=lib --upgrade pip setuptools wheel

if errorlevel 1 (
    echo Failed to install build tools
    exit /b 1
)
echo Build tools installed successfully
echo.

REM Step 2: Install dependencies
echo Step 2/2: Installing TFS client dependencies...
python -m pip install --no-index --find-links=lib -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies
    exit /b 1
)
echo Dependencies installed successfully
echo.

echo ======================================================================
echo Installation completed successfully!
echo ======================================================================
echo.

REM Verify installation
echo Verifying installation...
python -c "import azure.devops; print('Azure DevOps SDK version:', azure.devops.version.VERSION)" 2>nul

if errorlevel 1 (
    echo Warning: Could not verify installation
    echo Please check if the installation completed correctly.
) else (
    echo Installation verified
    echo.
    echo You can now use the TFS client. See README.md for usage examples.
)

echo.
pause
