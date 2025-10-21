#!/bin/bash
# Offline installation script for TFS Python Client
# Compatible with Azure DevOps Server 2020 Update 1.1

set -e  # Exit on error

echo "======================================================================"
echo "TFS Python Client - Offline Installation"
echo "Azure DevOps Server 2020 Update 1.1 Compatible"
echo "======================================================================"
echo ""

# Check if lib folder exists
if [ ! -d "lib" ]; then
    echo "Error: lib folder not found!"
    echo "Please ensure you are running this script from the project root directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "Using Python: $($PYTHON_CMD --version)"
echo ""

# Step 1: Install build tools
echo "Step 1/2: Installing build tools (pip, setuptools, wheel)..."
$PYTHON_CMD -m pip install --no-index --find-links=lib --upgrade pip setuptools wheel

if [ $? -eq 0 ]; then
    echo "✓ Build tools installed successfully"
else
    echo "✗ Failed to install build tools"
    exit 1
fi

echo ""

# Step 2: Install dependencies
echo "Step 2/2: Installing TFS client dependencies..."
$PYTHON_CMD -m pip install --no-index --find-links=lib -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Installation completed successfully!"
echo "======================================================================"
echo ""

# Verify installation
echo "Verifying installation..."
$PYTHON_CMD -c "import azure.devops; print('Azure DevOps SDK version:', azure.devops.version.VERSION)" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Installation verified"
    echo ""
    echo "You can now use the TFS client. See README.md for usage examples."
else
    echo "⚠ Warning: Could not verify installation"
    echo "Please check if the installation completed correctly."
fi

echo ""
