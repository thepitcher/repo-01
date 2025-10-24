"""
Example demonstrating Git branch operations (create, list, delete).
"""

from tfs_client import TFSClient
from tfs_config import TFSConfig
import os


def main():
    # Initialize client
    if os.path.exists('tfs_config.ini'):
        config = TFSConfig('tfs_config.ini')
        conn_params = config.get_connection_params()
        PROJECT_NAME = config.get_project()
        REPOSITORY_NAME = config.get_repository()
        client = TFSClient(**conn_params)
    else:
        TFS_URL = os.getenv('TFS_URL', 'http://tfs-server:8080/tfs/DefaultCollection')
        TFS_USERNAME = os.getenv('TFS_USERNAME')
        TFS_PASSWORD = os.getenv('TFS_PASSWORD')
        PROJECT_NAME = os.getenv('TFS_PROJECT', 'YourProjectName')
        REPOSITORY_NAME = os.getenv('TFS_REPOSITORY', 'YourRepositoryName')

        client = TFSClient(
            organization_url=TFS_URL,
            username=TFS_USERNAME,
            password=TFS_PASSWORD
        )

    print("=" * 80)
    print("Git Branch Management Example")
    print("=" * 80)
    print(f"\nProject: {PROJECT_NAME}")
    print(f"Repository: {REPOSITORY_NAME}")

    # ========================================================================
    # Step 1: List existing branches
    # ========================================================================
    print("\n[Step 1] Listing existing branches...")
    try:
        branches = client.get_refs(PROJECT_NAME, REPOSITORY_NAME, filter_prefix='refs/heads/')
        print(f"Found {len(branches)} branches:")
        for branch in branches[:10]:  # Show first 10
            branch_name = branch['name'].replace('refs/heads/', '')
            print(f"  - {branch_name}")
            print(f"    Commit: {branch['object_id'][:8]}")
    except Exception as e:
        print(f"Error: {e}")
        return

    # ========================================================================
    # Step 2: Get a source commit to branch from
    # ========================================================================
    print("\n[Step 2] Getting latest commit from main/master branch...")
    try:
        # Try to get commits from main or master branch
        source_branch = None
        for branch in branches:
            branch_name = branch['name'].replace('refs/heads/', '')
            if branch_name in ['main', 'master']:
                source_branch = branch_name
                source_commit_id = branch['object_id']
                print(f"Using branch: {source_branch}")
                print(f"Source commit: {source_commit_id}")
                break

        if not source_branch:
            # Use the first branch
            source_branch = branches[0]['name'].replace('refs/heads/', '')
            source_commit_id = branches[0]['object_id']
            print(f"Using first available branch: {source_branch}")
            print(f"Source commit: {source_commit_id}")

    except Exception as e:
        print(f"Error: {e}")
        return

    # ========================================================================
    # Step 3: Create a new branch
    # ========================================================================
    new_branch_name = input("\n[Step 3] Enter new branch name (or press Enter to skip): ").strip()

    if new_branch_name:
        print(f"\nCreating branch '{new_branch_name}' from commit {source_commit_id[:8]}...")
        try:
            result = client.create_branch(
                project=PROJECT_NAME,
                repository=REPOSITORY_NAME,
                branch_name=new_branch_name,
                source_commit_id=source_commit_id
            )

            print(f"✓ Branch created successfully!")
            print(f"  Name: {result['name']}")
            print(f"  Commit: {result['object_id']}")
            print(f"  Success: {result['success']}")

            # Verify by listing branches again
            print("\nVerifying - listing branches again...")
            branches = client.get_refs(PROJECT_NAME, REPOSITORY_NAME, filter_prefix='refs/heads/')
            for branch in branches:
                branch_name = branch['name'].replace('refs/heads/', '')
                if branch_name == new_branch_name:
                    print(f"  ✓ Found new branch: {branch_name}")
                    break

        except Exception as e:
            print(f"✗ Error creating branch: {e}")

        # ========================================================================
        # Step 4: Delete the branch (optional)
        # ========================================================================
        delete_confirm = input(f"\n[Step 4] Delete branch '{new_branch_name}'? (yes/no): ").strip().lower()

        if delete_confirm == 'yes':
            print(f"\nDeleting branch '{new_branch_name}'...")
            try:
                success = client.delete_branch(
                    project=PROJECT_NAME,
                    repository=REPOSITORY_NAME,
                    branch_name=new_branch_name
                )

                if success:
                    print(f"✓ Branch deleted successfully!")

                    # Verify deletion
                    print("\nVerifying - listing branches again...")
                    branches = client.get_refs(PROJECT_NAME, REPOSITORY_NAME, filter_prefix='refs/heads/')
                    found = False
                    for branch in branches:
                        branch_name = branch['name'].replace('refs/heads/', '')
                        if branch_name == new_branch_name:
                            found = True
                            break

                    if not found:
                        print(f"  ✓ Branch '{new_branch_name}' no longer exists")
                    else:
                        print(f"  ⚠ Branch '{new_branch_name}' still exists")
                else:
                    print(f"✗ Failed to delete branch")

            except Exception as e:
                print(f"✗ Error deleting branch: {e}")
    else:
        print("\nSkipping branch creation.")

    print("\n" + "=" * 80)
    print("Branch Management Example Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
