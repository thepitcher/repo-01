# Offline Installation Instructions

This folder contains all required Python packages for the TFS client, allowing for offline installation in air-gapped environments.

## Contents

This directory includes:
- `azure-devops-6.0.0b4.tar.gz` - Main Azure DevOps SDK for API v6.0
- Build tools (setuptools, wheel, pip)
- All dependency wheel files (.whl)

**Total size:** ~4.9 MB

## Installation from lib folder

### Step 1: Upgrade pip and install build tools (required)

First, ensure you have the latest pip, setuptools, and wheel:

```bash
pip install --no-index --find-links=lib --upgrade pip setuptools wheel
```

### Step 2: Install all dependencies

```bash
pip install --no-index --find-links=lib -r requirements.txt
```

### Alternative: Single command installation

```bash
pip install --no-index --find-links=lib --upgrade pip setuptools wheel && \
pip install --no-index --find-links=lib -r requirements.txt
```

### Troubleshooting

If you get an error about setuptools, run:

```bash
pip install --no-index --find-links=lib setuptools>=40.8.0
pip install --no-index --find-links=lib -r requirements.txt
```

## Package List

The following packages are included:

### Build Tools:
1. **pip** (25.2) - Package installer
2. **setuptools** (80.9.0) - Build system
3. **wheel** (0.45.1) - Wheel package support

### Main Package:
4. **azure-devops** (6.0.0b4) - Main Azure DevOps SDK for API v6.0

### Dependencies:
5. **msrest** (0.6.21) - Microsoft REST API client
6. **certifi** (2025.10.5) - SSL certificate handling
7. **charset-normalizer** (3.4.4) - Character encoding detection
8. **idna** (3.11) - Internationalized domain names
9. **isodate** (0.7.2) - ISO 8601 date/time handling
10. **oauthlib** (3.3.1) - OAuth implementation
11. **requests** (2.32.5) - HTTP library
12. **requests-oauthlib** (2.0.0) - OAuth for requests
13. **urllib3** (2.5.0) - HTTP client

**Total: 13 packages**

## Notes

- The `azure-devops` package is provided as a source distribution (.tar.gz) as no pre-built wheel is available for version 6.0.0b4
- setuptools, wheel, and pip are included to handle the source distribution installation
- All other dependencies are provided as wheels (.whl) for faster installation
- These packages are compatible with Azure DevOps Server 2020 Update 1.1 (API version 6.0)

## Verifying Installation

After installation, verify with:

```bash
python -c "import azure.devops; print(azure.devops.version.VERSION)"
```

This should output: `6.0.0b4`

## System Requirements

- Python 3.6 or higher
- pip 20.0 or higher (included in lib folder)
