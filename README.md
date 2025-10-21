# TFS Python Client

Python client for interacting with TFS (Team Foundation Server) / Azure DevOps Server to fetch branches and work items.

## Features

- Get list of branches from TFS repositories
- Fetch work items by ID
- List repositories in a project
- Support for both Personal Access Token (PAT) and Windows authentication

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The client can be configured using environment variables or by passing parameters directly to the `TFSClient` constructor.

### Environment Variables

Create a `.env` file or set the following environment variables:

```bash
TFS_URL=http://your-tfs-server:8080/tfs/DefaultCollection
TFS_PAT=your_personal_access_token
TFS_PROJECT=YourProjectName
TFS_REPOSITORY=YourRepositoryName
```

## Usage

### Basic Example

```python
from tfs_client import TFSClient

# Initialize client with Personal Access Token
client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    personal_access_token='your_pat_here'
)

# Or use default Windows credentials (on-premise TFS)
client = TFSClient(
    organization_url='http://tfs-server:8080/tfs/DefaultCollection',
    use_default_credentials=True
)

# Get branches
branches = client.get_refs(
    project='MyProject',
    repository='MyRepo',
    filter_prefix='refs/heads/'
)

for branch in branches:
    print(f"Branch: {branch['name']}")
    print(f"  Commit: {branch['object_id']}")

# Get work item by ID
work_item = client.get_work_item(work_item_id=123)
print(f"Work Item: {work_item['fields'].get('System.Title')}")
print(f"State: {work_item['fields'].get('System.State')}")
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

#### `__init__(organization_url, personal_access_token=None, use_default_credentials=False)`

Initialize the TFS client.

**Parameters:**
- `organization_url` (str): TFS server URL
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

### Personal Access Token (PAT)

1. Generate a PAT from your TFS/Azure DevOps Server
2. Grant required permissions (Code: Read, Work Items: Read)
3. Use it when initializing the client

### Windows Authentication

For on-premise TFS with Windows authentication, set `use_default_credentials=True`.

## Requirements

- Python 3.6+
- azure-devops >= 7.1.0
- TFS 2018+ or Azure DevOps Server

## License

MIT
