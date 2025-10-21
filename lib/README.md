# Offline Installation Instructions

This folder contains all required Python packages for the TFS client, allowing for offline installation.

## Contents

This directory includes:
- `azure-devops-6.0.0b4.tar.gz` - Main Azure DevOps SDK for API v6.0
- All dependency wheel files (.whl)

## Installation from lib folder

### Option 1: Install all dependencies from lib folder

```bash
pip install --no-index --find-links=lib -r requirements.txt
```

### Option 2: Install individual packages

```bash
pip install --no-index --find-links=lib lib/azure-devops-6.0.0b4.tar.gz
```

## Package List

The following packages are included:

1. **azure-devops** (6.0.0b4) - Main SDK
2. **msrest** (0.6.21) - Microsoft REST API client
3. **certifi** - SSL certificate handling
4. **charset-normalizer** - Character encoding detection
5. **idna** - Internationalized domain names
6. **isodate** - ISO 8601 date/time handling
7. **oauthlib** - OAuth implementation
8. **requests** - HTTP library
9. **requests-oauthlib** - OAuth for requests
10. **urllib3** - HTTP client

## Notes

- The `azure-devops` package is provided as a source distribution (.tar.gz) as no pre-built wheel is available for version 6.0.0b4
- All dependencies are provided as wheels (.whl) for faster installation
- These packages are compatible with Azure DevOps Server 2020 Update 1.1 (API version 6.0)

## Verifying Installation

After installation, verify with:

```bash
python -c "import azure.devops; print(azure.devops.version.VERSION)"
```

This should output: `6.0.0b4`
