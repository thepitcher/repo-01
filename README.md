# TFS Python Client

Python client for interacting with TFS (Team Foundation Server) / Azure DevOps Server to fetch branches and work items.

**Tested with Azure DevOps Server 2020 Update 1.1**

## Features

- Get list of branches from TFS repositories
- Fetch work items by ID
- List repositories in a project
- **Flexible authentication: Choose username/password OR Personal Access Token (PAT)**
- Configuration file support for easy setup
- Compatible with Azure DevOps Server 2020 Update 1.1 (API version 6.0)

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The client supports **three flexible configuration methods**. You can choose either **username/password** OR **personal access token** for authentication.

### Method 1: Configuration File (Recommended)

Create a `tfs_config.ini` file for easy configuration management. Choose one of the example files based on your authentication preference:

**For Username/Password Authentication:**
```bash
cp tfs_config_userpass.ini.example tfs_config.ini
# Edit tfs_config.ini with your credentials
```

**For Personal Access Token Authentication:**
```bash
cp tfs_config_pat.ini.example tfs_config.ini
# Edit tfs_config.ini with your PAT
```

Example configuration file structure:
```ini
[server]
url = http://tfs-server:8080/tfs/DefaultCollection

[auth]
# EITHER username/password (Option 1 - recommended)
username = your_username
password = your_password

# OR personal access token (Option 2)
# personal_access_token = your_pat_here

[project]
name = YourProjectName
repository = YourRepositoryName
```

### Method 2: Environment Variables

Create a `.env` file or set environment variables:

```bash
TFS_URL=http://your-tfs-server:8080/tfs/DefaultCollection

# EITHER username/password (Option 1 - recommended)
TFS_USERNAME=your_username
TFS_PASSWORD=your_password

# OR personal access token (Option 2)
# TFS_PAT=your_personal_access_token

# Project Configuration
TFS_PROJECT=YourProjectName
TFS_REPOSITORY=YourRepositoryName
```

### Method 3: Direct Parameters

Pass parameters directly when creating the client (see Usage section below).

## Usage

### Quick Start with Configuration File

```python
from tfs_client import TFSClient
from tfs_config import TFSConfig

# Load configuration from tfs_config.ini
config = TFSConfig('tfs_config.ini')
conn_params = config.get_connection_params()

# Create client (automatically uses username/password OR PAT from config)
client = TFSClient(**conn_params)

# Get branches
branches = client.get_refs(
    project=config.get_project(),
    repository=config.get_repository()
)

# Get work item
work_item = client.get_work_item(123)
```

### Authentication Options

The client accepts **EITHER** username/password **OR** personal access token:

#### Option 1: Username and Password (Recommended for Azure DevOps Server 2020)

```python
from tfs_client import TFSClient

client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    username='your_username',
    password='your_password'
)
```

#### Option 2: Personal Access Token

```python
from tfs_client import TFSClient

client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    personal_access_token='your_pat_here'
)
```

#### Option 3: Windows Default Credentials

```python
from tfs_client import TFSClient

client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    use_default_credentials=True
)
```

### Working with Branches and Work Items

```python
# Get list of branches
branches = client.get_refs(
    project='MyProject',
    repository='MyRepo',
    filter_prefix='refs/heads/'
)

for branch in branches:
    print(f"Branch: {branch['name']}")
    print(f"  Commit: {branch['object_id']}")

# Get a single work item by ID
work_item = client.get_work_item(work_item_id=123)
print(f"Work Item: {work_item['fields'].get('System.Title')}")
print(f"State: {work_item['fields'].get('System.State')}")

# Get multiple work items
work_items = client.get_work_items([123, 456, 789])
for wi in work_items:
    print(f"#{wi['id']}: {wi['fields'].get('System.Title')}")
```

### Running the Example Script

```bash
python example_usage.py
```

The example script demonstrates:
1. Listing repositories in a project
2. Fetching all branches in a repository
3. Getting a specific work item by ID
4. Fetching multiple work items

## API Reference

### TFSClient

#### `__init__(organization_url, username=None, password=None, personal_access_token=None, use_default_credentials=False)`

Initialize the TFS client.

**Parameters:**
- `organization_url` (str): TFS server URL
- `username` (str, optional): Username for basic authentication
- `password` (str, optional): Password for basic authentication
- `personal_access_token` (str, optional): Personal Access Token for authentication
- `use_default_credentials` (bool, optional): Use Windows default credentials

#### `get_branches(project, repository)`

Get list of branches from a repository.

**Parameters:**
- `project` (str): Project name
- `repository` (str): Repository name

**Returns:** List of branch dictionaries

#### `get_refs(project, repository, filter_prefix='refs/heads/')`

Get list of refs (branches/tags) from a repository.

**Parameters:**
- `project` (str): Project name
- `repository` (str): Repository name
- `filter_prefix` (str): Filter refs by prefix (default: 'refs/heads/' for branches)

**Returns:** List of ref dictionaries

#### `get_work_item(work_item_id, expand='All')`

Get a work item by ID.

**Parameters:**
- `work_item_id` (int): Work item ID
- `expand` (str): Level of detail ('None', 'Relations', 'Fields', 'Links', 'All')

**Returns:** Work item dictionary

#### `get_work_items(work_item_ids, expand='All')`

Get multiple work items by IDs.

**Parameters:**
- `work_item_ids` (List[int]): List of work item IDs
- `expand` (str): Level of detail ('None', 'Relations', 'Fields', 'Links', 'All')

**Returns:** List of work item dictionaries

#### `list_repositories(project)`

List all repositories in a project.

**Parameters:**
- `project` (str): Project name

**Returns:** List of repository dictionaries

## Authentication

**You can configure authentication using EITHER username/password OR personal access token.**

The client supports three authentication methods - choose the one that works best for your environment:

### 1. Username and Password (Recommended for Azure DevOps Server 2020)

Use your TFS username and password for basic authentication:

```python
client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    username='your_username',
    password='your_password'
)
```

**When to use:** This is the most straightforward method for on-premise Azure DevOps Server installations.

### 2. Personal Access Token (PAT)

Use a Personal Access Token instead of username/password:

1. Generate a PAT from your TFS/Azure DevOps Server
2. Grant required permissions (Code: Read, Work Items: Read)
3. Use it when initializing the client:

```python
client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    personal_access_token='your_pat'
)
```

**When to use:** Ideal for automation, CI/CD pipelines, or when you prefer token-based authentication.

### 3. Windows Authentication

For on-premise TFS with Windows authentication, set `use_default_credentials=True`:

```python
client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    use_default_credentials=True
)
```

**When to use:** For Windows domain environments where you want to use your current Windows credentials.

---

**Note:** The client automatically handles authentication based on which parameters you provide. If you provide both username/password and PAT, username/password will take precedence.

## Requirements

- Python 3.6+
- azure-devops >= 6.0.0b4, < 7.0.0 (for Azure DevOps Server 2020 Update 1.1 compatibility)

## Compatibility

This client is specifically designed and tested for:
- **Azure DevOps Server 2020 Update 1.1** (API version 6.0)

It should also work with:
- TFS 2018 and later
- TFS 2019
- Azure DevOps Server 2019
- Newer versions of Azure DevOps Server

**Note:** Azure DevOps Server 2020 Update 1.1 uses REST API version 6.0. The client uses the `azure-devops` Python SDK version 6.0.0 beta for compatibility.

## Version Information

- **Azure DevOps Server 2020 Update 1.1** → API version 6.0
- **Python SDK:** azure-devops 6.0.0b4

## License

MIT
