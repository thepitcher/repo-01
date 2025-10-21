"""
Example usage of TFS Client to fetch branches and work items.
"""

import os
from tfs_client import TFSClient


def main():
    # Configuration - Update these values for your TFS environment
    TFS_URL = os.getenv('TFS_URL', 'http://tfs-server:8080/tfs/DefaultCollection')
    TFS_USERNAME = os.getenv('TFS_USERNAME')
    TFS_PASSWORD = os.getenv('TFS_PASSWORD')
    TFS_PAT = os.getenv('TFS_PAT')  # Personal Access Token
    PROJECT_NAME = os.getenv('TFS_PROJECT', 'YourProjectName')
    REPOSITORY_NAME = os.getenv('TFS_REPOSITORY', 'YourRepositoryName')

    # Initialize TFS client
    # Option 1: Using username and password (recommended)
    if TFS_USERNAME and TFS_PASSWORD:
        client = TFSClient(
            organization_url=TFS_URL,
            username=TFS_USERNAME,
            password=TFS_PASSWORD
        )
    # Option 2: Using Personal Access Token
    elif TFS_PAT:
        client = TFSClient(
            organization_url=TFS_URL,
            personal_access_token=TFS_PAT
        )
    # Option 3: Using default Windows credentials (for on-premise TFS)
    else:
        client = TFSClient(
            organization_url=TFS_URL,
            use_default_credentials=True
        )

    print("=" * 80)
    print("TFS Client Example Usage")
    print("=" * 80)

    # Example 1: List repositories in the project
    print("\n1. Listing repositories in project...")
    try:
        repositories = client.list_repositories(PROJECT_NAME)
        print(f"\nFound {len(repositories)} repositories:")
        for repo in repositories:
            print(f"  - {repo['name']} (ID: {repo['id']})")
            if repo['default_branch']:
                print(f"    Default branch: {repo['default_branch']}")
    except Exception as e:
        print(f"Error listing repositories: {e}")

    # Example 2: Get list of branches
    print(f"\n2. Fetching branches for repository '{REPOSITORY_NAME}'...")
    try:
        # Try using get_refs first (more reliable)
        branches = client.get_refs(
            project=PROJECT_NAME,
            repository=REPOSITORY_NAME,
            filter_prefix="refs/heads/"
        )

        print(f"\nFound {len(branches)} branches:")
        for branch in branches:
            # Remove refs/heads/ prefix for cleaner display
            branch_name = branch['name'].replace('refs/heads/', '')
            print(f"  - {branch_name}")
            print(f"    Object ID: {branch['object_id']}")
            if branch['creator']:
                print(f"    Creator: {branch['creator']}")
    except Exception as e:
        print(f"Error fetching branches: {e}")

    # Example 3: Get a specific work item
    print("\n3. Fetching work item by ID...")
    work_item_id = int(input("Enter work item ID (or press Enter to skip): ").strip() or "0")

    if work_item_id > 0:
        try:
            work_item = client.get_work_item(work_item_id)

            print(f"\nWork Item #{work_item['id']} (Rev {work_item['rev']}):")
            print(f"  URL: {work_item['url']}")
            print("\n  Fields:")

            # Display common fields
            fields = work_item.get('fields', {})
            for field_name, field_value in fields.items():
                # Show only important fields for readability
                if any(key in field_name for key in ['Title', 'State', 'Type', 'AssignedTo', 'CreatedBy']):
                    print(f"    {field_name}: {field_value}")

            # Display relations if any
            if 'relations' in work_item and work_item['relations']:
                print(f"\n  Relations ({len(work_item['relations'])}):")
                for rel in work_item['relations']:
                    print(f"    - {rel['rel']}: {rel['url']}")
        except Exception as e:
            print(f"Error fetching work item: {e}")

    # Example 4: Get multiple work items
    print("\n4. Fetching multiple work items...")
    work_item_ids_input = input("Enter work item IDs separated by commas (or press Enter to skip): ").strip()

    if work_item_ids_input:
        try:
            work_item_ids = [int(id.strip()) for id in work_item_ids_input.split(',')]
            work_items = client.get_work_items(work_item_ids)

            print(f"\nFetched {len(work_items)} work items:")
            for wi in work_items:
                fields = wi.get('fields', {})
                title = fields.get('System.Title', 'N/A')
                state = fields.get('System.State', 'N/A')
                work_item_type = fields.get('System.WorkItemType', 'N/A')

                print(f"\n  Work Item #{wi['id']}:")
                print(f"    Title: {title}")
                print(f"    Type: {work_item_type}")
                print(f"    State: {state}")
        except Exception as e:
            print(f"Error fetching work items: {e}")

    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)


if __name__ == "__main__":
    main()
