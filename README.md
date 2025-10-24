# TFS Python Client - Comprehensive API Support

Python client for interacting with **ALL** TFS (Team Foundation Server) / Azure DevOps Server APIs.

**Tested with Azure DevOps Server 2020 Update 1.1**

## Features

### Comprehensive API Coverage
This client provides full access to all major TFS/Azure DevOps Server APIs:

- **Git API**: Repositories, branches, pull requests, commits, refs
- **Work Item Tracking API**: Work items, queries (WIQL), relations
- **Build API**: Build definitions, builds, queuing builds
- **Release API**: Release definitions, releases, deployments
- **Core API**: Projects, teams, processes
- **Test API**: Test plans, test suites, test runs
- **Graph API**: Users, groups, memberships
- **Policy API**: Branch policies
- **TFVC API**: Team Foundation Version Control

### Additional Features
- **Flexible authentication: Choose username/password OR Personal Access Token (PAT)**
- Configuration file support for easy setup
- **Offline installation support** with bundled dependencies in `lib/` folder
- Compatible with Azure DevOps Server 2020 Update 1.1 (API version 6.0)
- Comprehensive error handling and logging
- Well-documented methods with type hints

## Installation

### Online Installation

Install dependencies from PyPI:

```bash
pip install -r requirements.txt
```

### Offline Installation

All required packages (including build tools) are included in the `lib/` folder for offline installation.

**Option 1: Use the installation script (Recommended)**

For Linux/Mac:
```bash
./install_offline.sh
```

For Windows:
```cmd
install_offline.bat
```

**Option 2: Manual installation**

**Step 1: Install build tools**
```bash
pip install --no-index --find-links=lib --upgrade pip setuptools wheel
```

**Step 2: Install dependencies**
```bash
pip install --no-index --find-links=lib -r requirements.txt
```

**Or as a single command:**
```bash
pip install --no-index --find-links=lib --upgrade pip setuptools wheel && \
pip install --no-index --find-links=lib -r requirements.txt
```

This is useful for:
- Air-gapped environments
- Systems without internet access
- Ensuring consistent package versions
- Corporate networks with restricted access

For troubleshooting and more details, see [lib/README.md](lib/README.md).

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

### API Usage Examples

#### Git API - Repositories, Branches, Pull Requests

```python
# List repositories
repos = client.list_repositories('MyProject')

# Get branches
branches = client.get_refs('MyProject', 'MyRepo', filter_prefix='refs/heads/')

# Create a new branch
new_branch = client.create_branch(
    project='MyProject',
    repository='MyRepo',
    branch_name='feature/new-feature',
    source_commit_id='abc123def456...'  # Commit SHA to branch from
)

# Delete a branch
success = client.delete_branch('MyProject', 'MyRepo', 'feature/old-feature')

# Get pull requests
prs = client.get_pull_requests('MyProject', 'MyRepo', status='active')

# Get commits
commits = client.get_commits('MyProject', 'MyRepo', branch='main', top=10)
```

#### Work Item Tracking API

```python
# Get a single work item
work_item = client.get_work_item(123)

# Get multiple work items
work_items = client.get_work_items([123, 456, 789])

# Query work items using WIQL
wiql = "SELECT [System.Id] FROM WorkItems WHERE [System.State] = 'Active'"
work_item_ids = client.query_work_items('MyProject', wiql)
```

#### Build API

```python
# Get build definitions
build_defs = client.get_build_definitions('MyProject')

# Get builds
builds = client.get_builds('MyProject', top=10)

# Queue a new build
queued_build = client.queue_build('MyProject', definition_id=42, source_branch='main')
```

#### Release API

```python
# Get release definitions
release_defs = client.get_release_definitions('MyProject')

# Get releases
releases = client.get_releases('MyProject', top=10)
```

#### Core API - Projects and Teams

```python
# Get all projects
projects = client.get_projects()

# Get teams in a project
teams = client.get_teams('MyProject')
```

#### Test API

```python
# Get test plans
test_plans = client.get_test_plans('MyProject')

# Get test runs
test_runs = client.get_test_runs('MyProject')
```

### Running the Example Scripts

**Basic example (branches and work items):**
```bash
python example_usage.py
```

**Branch management example (create/delete branches):**
```bash
python example_branch_operations.py
```

**Comprehensive example (all APIs):**
```bash
python example_all_apis.py
```

The comprehensive example demonstrates:
1. Core API - Projects and Teams
2. Git API - Repositories, Branches, Pull Requests, Commits
3. Work Item Tracking API - Work Items and Queries
4. Build API - Build Definitions and Builds
5. Release API - Release Definitions and Releases
6. Test API - Test Plans and Runs

## API Reference

### TFSClient

Comprehensive client providing access to all TFS/Azure DevOps Server APIs.

#### Initialization

```python
__init__(organization_url, username=None, password=None, personal_access_token=None, use_default_credentials=False)
```

**Parameters:**
- `organization_url` (str): TFS server URL
- `username` (str, optional): Username for basic authentication
- `password` (str, optional): Password for basic authentication
- `personal_access_token` (str, optional): Personal Access Token for authentication
- `use_default_credentials` (bool, optional): Use Windows default credentials

#### Git API Methods

- `list_repositories(project)` - List all repositories in a project
- `get_branches(project, repository)` - Get branches from a repository
- `get_refs(project, repository, filter_prefix)` - Get refs (branches/tags) with filtering
- `create_branch(project, repository, branch_name, source_commit_id)` - **Create a new branch**
- `delete_branch(project, repository, branch_name)` - **Delete a branch**
- `get_pull_requests(project, repository, status)` - Get pull requests
- `get_commits(project, repository, branch, top)` - Get commits from a repository

#### Work Item Tracking API Methods

- `get_work_item(work_item_id, expand)` - Get a single work item by ID
- `get_work_items(work_item_ids, expand)` - Get multiple work items by IDs
- `query_work_items(project, wiql)` - Query work items using WIQL

#### Build API Methods

- `get_build_definitions(project)` - Get build definitions
- `get_builds(project, definition_id, top)` - Get builds
- `queue_build(project, definition_id, source_branch)` - Queue a new build

#### Release API Methods

- `get_release_definitions(project)` - Get release definitions
- `get_releases(project, definition_id, top)` - Get releases

#### Core API Methods

- `get_projects()` - Get all projects
- `get_teams(project)` - Get all teams in a project

#### Test API Methods

- `get_test_plans(project)` - Get test plans
- `get_test_runs(project)` - Get test runs

#### Utility Methods

- `get_api_version()` - Get the API version being used
- `get_organization_url()` - Get the organization URL

### Complete API Documentation

For detailed documentation of all methods, parameters, and return types, see:
- **tfs_client.py** - Inline documentation with type hints
- **example_all_apis.py** - Comprehensive usage examples for all APIs

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
