"""
TFS/Azure DevOps Client for fetching branches and work items.
"""

import os
from typing import List, Dict, Optional
from azure.devops.connection import Connection
from azure.devops.v7_1.git import GitClient
from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient
from msrest.authentication import BasicAuthentication


class TFSClient:
    """Client for interacting with TFS/Azure DevOps Server."""

    def __init__(
        self,
        organization_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        personal_access_token: Optional[str] = None,
        use_default_credentials: bool = False
    ):
        """
        Initialize TFS client.

        Args:
            organization_url: TFS server URL (e.g., 'http://tfs-server:8080/tfs/DefaultCollection')
            username: Username for basic authentication
            password: Password for basic authentication
            personal_access_token: Personal Access Token for authentication
            use_default_credentials: Use default Windows credentials (for on-premise TFS)
        """
        self.organization_url = organization_url

        # Setup authentication
        if username and password:
            # Basic authentication with username and password
            credentials = BasicAuthentication(username, password)
        elif personal_access_token:
            # PAT authentication (empty username with PAT as password)
            credentials = BasicAuthentication('', personal_access_token)
        elif use_default_credentials:
            # For on-premise TFS with Windows authentication
            credentials = None  # Will use default credentials
        else:
            raise ValueError(
                "Authentication required: provide either username/password, "
                "personal_access_token, or set use_default_credentials=True"
            )

        # Create connection
        self.connection = Connection(
            base_url=organization_url,
            creds=credentials
        )

        # Get clients
        self.git_client: GitClient = self.connection.clients.get_git_client()
        self.work_item_client: WorkItemTrackingClient = self.connection.clients.get_work_item_tracking_client()

    def get_branches(self, project: str, repository: str) -> List[Dict]:
        """
        Get list of branches from a TFS repository.

        Args:
            project: Name of the TFS project
            repository: Name of the repository

        Returns:
            List of branch information dictionaries
        """
        try:
            branches = self.git_client.get_branches(
                repository_id=repository,
                project=project
            )

            branch_list = []
            for branch in branches:
                branch_info = {
                    'name': branch.name,
                    'object_id': branch.object_id,
                    'creator': branch.creator.display_name if branch.creator else None,
                    'url': branch.url if hasattr(branch, 'url') else None
                }
                branch_list.append(branch_info)

            return branch_list
        except Exception as e:
            print(f"Error fetching branches: {str(e)}")
            raise

    def get_refs(self, project: str, repository: str, filter_prefix: str = "refs/heads/") -> List[Dict]:
        """
        Get list of refs (branches/tags) from a TFS repository.

        Args:
            project: Name of the TFS project
            repository: Name of the repository
            filter_prefix: Filter refs by prefix (default: 'refs/heads/' for branches)

        Returns:
            List of ref information dictionaries
        """
        try:
            refs = self.git_client.get_refs(
                repository_id=repository,
                project=project,
                filter=filter_prefix
            )

            ref_list = []
            for ref in refs:
                ref_info = {
                    'name': ref.name,
                    'object_id': ref.object_id,
                    'creator': ref.creator.display_name if ref.creator else None,
                    'url': ref.url if hasattr(ref, 'url') else None
                }
                ref_list.append(ref_info)

            return ref_list
        except Exception as e:
            print(f"Error fetching refs: {str(e)}")
            raise

    def get_work_item(self, work_item_id: int, expand: str = "All") -> Dict:
        """
        Get work item by ID from TFS.

        Args:
            work_item_id: ID of the work item
            expand: Level of detail to return (None, Relations, Fields, Links, All)

        Returns:
            Dictionary containing work item information
        """
        try:
            work_item = self.work_item_client.get_work_item(
                id=work_item_id,
                expand=expand
            )

            work_item_info = {
                'id': work_item.id,
                'rev': work_item.rev,
                'fields': work_item.fields if work_item.fields else {},
                'url': work_item.url if hasattr(work_item, 'url') else None,
            }

            # Add relations if available
            if work_item.relations:
                work_item_info['relations'] = [
                    {
                        'rel': rel.rel,
                        'url': rel.url,
                        'attributes': rel.attributes if rel.attributes else {}
                    }
                    for rel in work_item.relations
                ]

            return work_item_info
        except Exception as e:
            print(f"Error fetching work item {work_item_id}: {str(e)}")
            raise

    def get_work_items(self, work_item_ids: List[int], expand: str = "All") -> List[Dict]:
        """
        Get multiple work items by IDs from TFS.

        Args:
            work_item_ids: List of work item IDs
            expand: Level of detail to return (None, Relations, Fields, Links, All)

        Returns:
            List of dictionaries containing work item information
        """
        try:
            work_items = self.work_item_client.get_work_items(
                ids=work_item_ids,
                expand=expand
            )

            work_items_list = []
            for work_item in work_items:
                work_item_info = {
                    'id': work_item.id,
                    'rev': work_item.rev,
                    'fields': work_item.fields if work_item.fields else {},
                    'url': work_item.url if hasattr(work_item, 'url') else None,
                }

                # Add relations if available
                if work_item.relations:
                    work_item_info['relations'] = [
                        {
                            'rel': rel.rel,
                            'url': rel.url,
                            'attributes': rel.attributes if rel.attributes else {}
                        }
                        for rel in work_item.relations
                    ]

                work_items_list.append(work_item_info)

            return work_items_list
        except Exception as e:
            print(f"Error fetching work items: {str(e)}")
            raise

    def list_repositories(self, project: str) -> List[Dict]:
        """
        List all repositories in a project.

        Args:
            project: Name of the TFS project

        Returns:
            List of repository information dictionaries
        """
        try:
            repositories = self.git_client.get_repositories(project=project)

            repo_list = []
            for repo in repositories:
                repo_info = {
                    'id': repo.id,
                    'name': repo.name,
                    'url': repo.url if hasattr(repo, 'url') else None,
                    'default_branch': repo.default_branch if hasattr(repo, 'default_branch') else None,
                    'size': repo.size if hasattr(repo, 'size') else None,
                }
                repo_list.append(repo_info)

            return repo_list
        except Exception as e:
            print(f"Error fetching repositories: {str(e)}")
            raise
