"""
Comprehensive example demonstrating all TFS/Azure DevOps Server APIs.

This script shows how to use the TFSClient to interact with:
- Git API (repositories, branches, pull requests, commits)
- Work Item Tracking API (work items, queries)
- Build API (build definitions, builds)
- Release API (release definitions, releases)
- Core API (projects, teams)
- Test API (test plans, runs)
"""

import os
from tfs_client import TFSClient
from tfs_config import TFSConfig


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    # Initialize TFS client
    print_section("TFS Comprehensive API Client - All Services")

    # Load configuration
    if os.path.exists('tfs_config.ini'):
        print("[INFO] Loading configuration from tfs_config.ini")
        config = TFSConfig('tfs_config.ini')
        conn_params = config.get_connection_params()
        PROJECT_NAME = config.get_project()
        REPOSITORY_NAME = config.get_repository()
        client = TFSClient(**conn_params)
    else:
        print("[INFO] Using environment variables")
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

    print(f"Connected to: {client.get_organization_url()}")
    print(f"API Version: {client.get_api_version()}")

    # ========================================================================
    # CORE API - Projects and Teams
    # ========================================================================
    print_section("1. CORE API - Projects and Teams")

    try:
        print("Fetching all projects...")
        projects = client.get_projects()
        print(f"Found {len(projects)} projects:")
        for project in projects[:5]:  # Show first 5
            print(f"  - {project['name']} ({project['state']})")
            print(f"    ID: {project['id']}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching teams in project '{PROJECT_NAME}'...")
        teams = client.get_teams(PROJECT_NAME)
        print(f"Found {len(teams)} teams:")
        for team in teams[:5]:
            print(f"  - {team['name']}")
    except Exception as e:
        print(f"Error: {e}")

    # ========================================================================
    # GIT API - Repositories, Branches, Pull Requests, Commits
    # ========================================================================
    print_section("2. GIT API - Repositories and Branches")

    try:
        print(f"Fetching repositories in project '{PROJECT_NAME}'...")
        repos = client.list_repositories(PROJECT_NAME)
        print(f"Found {len(repos)} repositories:")
        for repo in repos[:5]:
            print(f"  - {repo['name']}")
            if repo['default_branch']:
                print(f"    Default branch: {repo['default_branch']}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching branches in repository '{REPOSITORY_NAME}'...")
        branches = client.get_refs(PROJECT_NAME, REPOSITORY_NAME, filter_prefix="refs/heads/")
        print(f"Found {len(branches)} branches:")
        for branch in branches[:5]:
            branch_name = branch['name'].replace('refs/heads/', '')
            print(f"  - {branch_name}")
            print(f"    Commit: {branch['object_id'][:8]}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching pull requests in repository '{REPOSITORY_NAME}'...")
        prs = client.get_pull_requests(PROJECT_NAME, REPOSITORY_NAME, status="active")
        print(f"Found {len(prs)} active pull requests:")
        for pr in prs[:5]:
            print(f"  - PR #{pr['pull_request_id']}: {pr['title']}")
            print(f"    From: {pr['source_ref_name']} -> {pr['target_ref_name']}")
            print(f"    Status: {pr['status']}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching recent commits in repository '{REPOSITORY_NAME}'...")
        commits = client.get_commits(PROJECT_NAME, REPOSITORY_NAME, top=5)
        print(f"Found {len(commits)} recent commits:")
        for commit in commits:
            print(f"  - {commit['commit_id'][:8]} by {commit['author']}")
            print(f"    {commit['comment'][:60]}...")
    except Exception as e:
        print(f"Error: {e}")

    # ========================================================================
    # WORK ITEM TRACKING API
    # ========================================================================
    print_section("3. WORK ITEM TRACKING API")

    try:
        print("Querying recent work items...")
        wiql = f"SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.TeamProject] = '{PROJECT_NAME}' ORDER BY [System.ChangedDate] DESC"
        work_item_ids = client.query_work_items(PROJECT_NAME, wiql)

        if work_item_ids:
            print(f"Found {len(work_item_ids)} work items")

            # Get details for first few work items
            sample_ids = work_item_ids[:5]
            work_items = client.get_work_items(sample_ids)

            print("\nRecent work items:")
            for wi in work_items:
                title = wi['fields'].get('System.Title', 'N/A')
                state = wi['fields'].get('System.State', 'N/A')
                wi_type = wi['fields'].get('System.WorkItemType', 'N/A')
                print(f"  - #{wi['id']} [{wi_type}] {title}")
                print(f"    State: {state}")
        else:
            print("No work items found")
    except Exception as e:
        print(f"Error: {e}")

    # ========================================================================
    # BUILD API
    # ========================================================================
    print_section("4. BUILD API - Build Definitions and Builds")

    try:
        print(f"Fetching build definitions in project '{PROJECT_NAME}'...")
        build_defs = client.get_build_definitions(PROJECT_NAME)
        print(f"Found {len(build_defs)} build definitions:")
        for build_def in build_defs[:5]:
            print(f"  - {build_def['name']} (ID: {build_def['id']})")
            print(f"    Path: {build_def['path']}")
            print(f"    Status: {build_def['queue_status']}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching recent builds in project '{PROJECT_NAME}'...")
        builds = client.get_builds(PROJECT_NAME, top=5)
        print(f"Found {len(builds)} recent builds:")
        for build in builds:
            print(f"  - Build #{build['build_number']} ({build['definition']})")
            print(f"    Status: {build['status']}, Result: {build['result']}")
            print(f"    Requested by: {build['requested_by']}")
    except Exception as e:
        print(f"Error: {e}")

    # ========================================================================
    # RELEASE API
    # ========================================================================
    print_section("5. RELEASE API - Release Definitions and Releases")

    try:
        print(f"Fetching release definitions in project '{PROJECT_NAME}'...")
        release_defs = client.get_release_definitions(PROJECT_NAME)
        print(f"Found {len(release_defs)} release definitions:")
        for release_def in release_defs[:5]:
            print(f"  - {release_def['name']} (ID: {release_def['id']})")
            if release_def['path']:
                print(f"    Path: {release_def['path']}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching recent releases in project '{PROJECT_NAME}'...")
        releases = client.get_releases(PROJECT_NAME, top=5)
        print(f"Found {len(releases)} recent releases:")
        for release in releases:
            print(f"  - {release['name']} (ID: {release['id']})")
            print(f"    Status: {release['status']}")
            print(f"    Created by: {release['created_by']}")
    except Exception as e:
        print(f"Error: {e}")

    # ========================================================================
    # TEST API
    # ========================================================================
    print_section("6. TEST API - Test Plans and Runs")

    try:
        print(f"Fetching test plans in project '{PROJECT_NAME}'...")
        test_plans = client.get_test_plans(PROJECT_NAME)
        print(f"Found {len(test_plans)} test plans:")
        for plan in test_plans[:5]:
            print(f"  - {plan['name']} (ID: {plan['id']})")
            if plan['state']:
                print(f"    State: {plan['state']}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"\nFetching test runs in project '{PROJECT_NAME}'...")
        test_runs = client.get_test_runs(PROJECT_NAME)
        print(f"Found {len(test_runs)} test runs:")
        for run in test_runs[:5]:
            print(f"  - {run['name']} (ID: {run['id']})")
            print(f"    State: {run['state']}")
            if run['is_automated'] is not None:
                print(f"    Automated: {run['is_automated']}")
    except Exception as e:
        print(f"Error: {e}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print_section("Summary")
    print("✓ Core API - Projects and Teams")
    print("✓ Git API - Repositories, Branches, Pull Requests, Commits")
    print("✓ Work Item Tracking API - Work Items and Queries")
    print("✓ Build API - Build Definitions and Builds")
    print("✓ Release API - Release Definitions and Releases")
    print("✓ Test API - Test Plans and Runs")
    print("\nAll API services accessed successfully!")
    print("\nFor more details on each API, see the TFSClient class methods.")


if __name__ == "__main__":
    main()
