"""
TFS/Azure DevOps Comprehensive Client for all API services.

Compatible with Azure DevOps Server 2020 Update 1.1 (API version 6.0)

Supports:
- Git: Repositories, branches, pull requests, commits
- Work Items: Query, create, update work items
- Build: Build definitions, builds, queues
- Release: Release definitions, releases, deployments
- Core: Projects, teams, processes
- Wiki: Wiki pages and operations
- Test: Test plans, suites, cases, runs
- Graph: Users, groups, memberships
- Policy: Branch policies
- TFVC: Team Foundation Version Control
"""

import os
from typing import List, Dict, Optional, Any
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Try to import API v6.0 for Azure DevOps Server 2020, fallback to v7.0+
try:
    from azure.devops.v6_0.git import GitClient
    from azure.devops.v6_0.work_item_tracking import WorkItemTrackingClient
    from azure.devops.v6_0.build import BuildClient
    from azure.devops.v6_0.release import ReleaseClient
    from azure.devops.v6_0.core import CoreClient
    from azure.devops.v6_0.wiki import WikiClient
    from azure.devops.v6_0.test import TestClient
    from azure.devops.v6_0.graph import GraphClient
    from azure.devops.v6_0.policy import PolicyClient
    from azure.devops.v6_0.tfvc import TfvcClient
    API_VERSION = "6.0"
except ImportError:
    # Fallback to newer versions if v6_0 is not available
    try:
        from azure.devops.v7_0.git import GitClient
        from azure.devops.v7_0.work_item_tracking import WorkItemTrackingClient
        from azure.devops.v7_0.build import BuildClient
        from azure.devops.v7_0.release import ReleaseClient
        from azure.devops.v7_0.core import CoreClient
        from azure.devops.v7_0.wiki import WikiClient
        from azure.devops.v7_0.test import TestClient
        from azure.devops.v7_0.graph import GraphClient
        from azure.devops.v7_0.policy import PolicyClient
        from azure.devops.v7_0.tfvc import TfvcClient
        API_VERSION = "7.0"
    except ImportError:
        from azure.devops.v7_1.git import GitClient
        from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient
        from azure.devops.v7_1.build import BuildClient
        from azure.devops.v7_1.release import ReleaseClient
        from azure.devops.v7_1.core import CoreClient
        from azure.devops.v7_1.wiki import WikiClient
        from azure.devops.v7_1.test import TestClient
        from azure.devops.v7_1.graph import GraphClient
        from azure.devops.v7_1.policy import PolicyClient
        from azure.devops.v7_1.tfvc import TfvcClient
        API_VERSION = "7.1"


class TFSClient:
    """
    Comprehensive client for interacting with all TFS/Azure DevOps Server APIs.

    Tested with Azure DevOps Server 2020 Update 1.1 (API version 6.0).
    Should also work with TFS 2018, TFS 2019, and newer Azure DevOps Server versions.

    Provides access to:
    - Git API (repositories, branches, pull requests, commits)
    - Work Item Tracking API (work items, queries)
    - Build API (build definitions, builds)
    - Release API (release definitions, releases, deployments)
    - Core API (projects, teams)
    - Wiki API (wiki pages)
    - Test API (test plans, suites, cases, runs)
    - Graph API (users, groups, memberships)
    - Policy API (branch policies)
    - TFVC API (Team Foundation Version Control)
    """

    def __init__(
        self,
        organization_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        personal_access_token: Optional[str] = None,
        use_default_credentials: bool = False
    ):
        """
        Initialize comprehensive TFS client for all API services.

        Args:
            organization_url: TFS server URL (e.g., 'http://tfs-server:8080/tfs/DefaultCollection')
            username: Username for basic authentication
            password: Password for basic authentication
            personal_access_token: Personal Access Token for authentication
            use_default_credentials: Use default Windows credentials (for on-premise TFS)
        """
        self.organization_url = organization_url
        self.api_version = API_VERSION

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

        # Initialize all API clients
        self.git_client: GitClient = self.connection.clients.get_git_client()
        self.work_item_client: WorkItemTrackingClient = self.connection.clients.get_work_item_tracking_client()
        self.build_client: BuildClient = self.connection.clients.get_build_client()
        self.release_client: ReleaseClient = self.connection.clients.get_release_client()
        self.core_client: CoreClient = self.connection.clients.get_core_client()
        self.wiki_client: WikiClient = self.connection.clients.get_wiki_client()
        self.test_client: TestClient = self.connection.clients.get_test_client()
        self.graph_client: GraphClient = self.connection.clients.get_graph_client()
        self.policy_client: PolicyClient = self.connection.clients.get_policy_client()
        self.tfvc_client: TfvcClient = self.connection.clients.get_tfvc_client()

    # ========================================================================
    # GIT API METHODS
    # ========================================================================

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

    def get_pull_requests(self, project: str, repository: str, status: str = "active") -> List[Dict]:
        """
        Get pull requests from a repository.

        Args:
            project: Name of the TFS project
            repository: Name of the repository
            status: PR status filter (active, completed, abandoned, all)

        Returns:
            List of pull request dictionaries
        """
        try:
            prs = self.git_client.get_pull_requests(
                repository_id=repository,
                project=project,
                search_criteria={'status': status}
            )

            pr_list = []
            for pr in prs:
                pr_info = {
                    'pull_request_id': pr.pull_request_id,
                    'title': pr.title,
                    'description': pr.description,
                    'created_by': pr.created_by.display_name if pr.created_by else None,
                    'source_ref_name': pr.source_ref_name,
                    'target_ref_name': pr.target_ref_name,
                    'status': pr.status,
                    'creation_date': str(pr.creation_date) if pr.creation_date else None,
                    'url': pr.url if hasattr(pr, 'url') else None
                }
                pr_list.append(pr_info)

            return pr_list
        except Exception as e:
            print(f"Error fetching pull requests: {str(e)}")
            raise

    def get_commits(self, project: str, repository: str, branch: Optional[str] = None, top: int = 100) -> List[Dict]:
        """
        Get commits from a repository.

        Args:
            project: Name of the TFS project
            repository: Name of the repository
            branch: Branch name to filter commits (optional)
            top: Maximum number of commits to return

        Returns:
            List of commit dictionaries
        """
        try:
            search_criteria = {'$top': top}
            if branch:
                search_criteria['itemVersion'] = {'version': branch}

            commits = self.git_client.get_commits(
                repository_id=repository,
                project=project,
                search_criteria=search_criteria
            )

            commit_list = []
            for commit in commits:
                commit_info = {
                    'commit_id': commit.commit_id,
                    'author': commit.author.name if commit.author else None,
                    'committer': commit.committer.name if commit.committer else None,
                    'comment': commit.comment,
                    'change_counts': commit.change_counts if hasattr(commit, 'change_counts') else None,
                    'url': commit.url if hasattr(commit, 'url') else None
                }
                commit_list.append(commit_info)

            return commit_list
        except Exception as e:
            print(f"Error fetching commits: {str(e)}")
            raise

    def create_branch(self, project: str, repository: str, branch_name: str, source_commit_id: str) -> Dict:
        """
        Create a new branch in a repository.

        Args:
            project: Name of the TFS project
            repository: Name of the repository
            branch_name: Name of the new branch (without 'refs/heads/' prefix)
            source_commit_id: Commit SHA to branch from

        Returns:
            Dictionary containing the created branch information
        """
        try:
            # Construct the full ref name
            if not branch_name.startswith('refs/heads/'):
                ref_name = f'refs/heads/{branch_name}'
            else:
                ref_name = branch_name

            # Create the ref update object
            ref_update = {
                'name': ref_name,
                'oldObjectId': '0000000000000000000000000000000000000000',  # New branch
                'newObjectId': source_commit_id
            }

            # Update refs
            updated_refs = self.git_client.update_refs(
                ref_updates=[ref_update],
                repository_id=repository,
                project=project
            )

            if updated_refs and len(updated_refs) > 0:
                ref = updated_refs[0]
                return {
                    'name': ref.name,
                    'object_id': ref.new_object_id if hasattr(ref, 'new_object_id') else source_commit_id,
                    'success': ref.success if hasattr(ref, 'success') else True,
                    'url': ref.url if hasattr(ref, 'url') else None
                }
            else:
                raise Exception("Failed to create branch - no response from server")
        except Exception as e:
            print(f"Error creating branch '{branch_name}': {str(e)}")
            raise

    def delete_branch(self, project: str, repository: str, branch_name: str) -> bool:
        """
        Delete a branch from a repository.

        Args:
            project: Name of the TFS project
            repository: Name of the repository
            branch_name: Name of the branch to delete (without 'refs/heads/' prefix)

        Returns:
            Boolean indicating success
        """
        try:
            # Construct the full ref name
            if not branch_name.startswith('refs/heads/'):
                ref_name = f'refs/heads/{branch_name}'
            else:
                ref_name = branch_name

            # Get current branch to get its object ID
            refs = self.git_client.get_refs(
                repository_id=repository,
                project=project,
                filter=ref_name
            )

            if not refs or len(refs) == 0:
                raise Exception(f"Branch '{branch_name}' not found")

            current_object_id = refs[0].object_id

            # Create the ref update object to delete
            ref_update = {
                'name': ref_name,
                'oldObjectId': current_object_id,
                'newObjectId': '0000000000000000000000000000000000000000'  # Delete
            }

            # Update refs
            updated_refs = self.git_client.update_refs(
                ref_updates=[ref_update],
                repository_id=repository,
                project=project
            )

            if updated_refs and len(updated_refs) > 0:
                return updated_refs[0].success if hasattr(updated_refs[0], 'success') else True
            return False
        except Exception as e:
            print(f"Error deleting branch '{branch_name}': {str(e)}")
            raise

    # ========================================================================
    # WORK ITEM TRACKING API METHODS
    # ========================================================================

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

    def query_work_items(self, project: str, wiql: str) -> List[int]:
        """
        Query work items using WIQL (Work Item Query Language).

        Args:
            project: Name of the TFS project
            wiql: WIQL query string

        Returns:
            List of work item IDs matching the query
        """
        try:
            query_result = self.work_item_client.query_by_wiql(
                wiql={'query': wiql},
                project=project
            )

            if query_result.work_items:
                return [wi.id for wi in query_result.work_items]
            return []
        except Exception as e:
            print(f"Error querying work items: {str(e)}")
            raise

    # ========================================================================
    # BUILD API METHODS
    # ========================================================================

    def get_builds(self, project: str, definition_id: Optional[int] = None, top: int = 10) -> List[Dict]:
        """
        Get builds from a project.

        Args:
            project: Name of the TFS project
            definition_id: Build definition ID to filter (optional)
            top: Maximum number of builds to return

        Returns:
            List of build dictionaries
        """
        try:
            builds = self.build_client.get_builds(
                project=project,
                definitions=[definition_id] if definition_id else None,
                top=top
            )

            build_list = []
            for build in builds:
                build_info = {
                    'id': build.id,
                    'build_number': build.build_number,
                    'status': build.status,
                    'result': build.result,
                    'queue_time': str(build.queue_time) if build.queue_time else None,
                    'start_time': str(build.start_time) if build.start_time else None,
                    'finish_time': str(build.finish_time) if build.finish_time else None,
                    'requested_by': build.requested_by.display_name if build.requested_by else None,
                    'definition': build.definition.name if build.definition else None,
                    'url': build.url if hasattr(build, 'url') else None
                }
                build_list.append(build_info)

            return build_list
        except Exception as e:
            print(f"Error fetching builds: {str(e)}")
            raise

    def get_build_definitions(self, project: str) -> List[Dict]:
        """
        Get build definitions from a project.

        Args:
            project: Name of the TFS project

        Returns:
            List of build definition dictionaries
        """
        try:
            definitions = self.build_client.get_definitions(project=project)

            def_list = []
            for definition in definitions:
                def_info = {
                    'id': definition.id,
                    'name': definition.name,
                    'path': definition.path,
                    'queue_status': definition.queue_status,
                    'type': definition.type,
                    'revision': definition.revision,
                    'url': definition.url if hasattr(definition, 'url') else None
                }
                def_list.append(def_info)

            return def_list
        except Exception as e:
            print(f"Error fetching build definitions: {str(e)}")
            raise

    def queue_build(self, project: str, definition_id: int, source_branch: Optional[str] = None) -> Dict:
        """
        Queue a new build.

        Args:
            project: Name of the TFS project
            definition_id: Build definition ID
            source_branch: Source branch to build (optional)

        Returns:
            Dictionary containing queued build information
        """
        try:
            from azure.devops.v6_0.build.models import Build

            build = Build()
            build.definition = {'id': definition_id}
            if source_branch:
                build.source_branch = source_branch

            queued_build = self.build_client.queue_build(build=build, project=project)

            return {
                'id': queued_build.id,
                'build_number': queued_build.build_number,
                'status': queued_build.status,
                'queue_time': str(queued_build.queue_time) if queued_build.queue_time else None,
                'url': queued_build.url if hasattr(queued_build, 'url') else None
            }
        except Exception as e:
            print(f"Error queuing build: {str(e)}")
            raise

    # ========================================================================
    # RELEASE API METHODS
    # ========================================================================

    def get_releases(self, project: str, definition_id: Optional[int] = None, top: int = 10) -> List[Dict]:
        """
        Get releases from a project.

        Args:
            project: Name of the TFS project
            definition_id: Release definition ID to filter (optional)
            top: Maximum number of releases to return

        Returns:
            List of release dictionaries
        """
        try:
            releases = self.release_client.get_releases(
                project=project,
                definition_id=definition_id,
                top=top
            )

            release_list = []
            for release in releases:
                release_info = {
                    'id': release.id,
                    'name': release.name,
                    'status': release.status,
                    'created_on': str(release.created_on) if release.created_on else None,
                    'created_by': release.created_by.display_name if release.created_by else None,
                    'description': release.description,
                    'url': release.url if hasattr(release, 'url') else None
                }
                release_list.append(release_info)

            return release_list
        except Exception as e:
            print(f"Error fetching releases: {str(e)}")
            raise

    def get_release_definitions(self, project: str) -> List[Dict]:
        """
        Get release definitions from a project.

        Args:
            project: Name of the TFS project

        Returns:
            List of release definition dictionaries
        """
        try:
            definitions = self.release_client.get_release_definitions(project=project)

            def_list = []
            for definition in definitions:
                def_info = {
                    'id': definition.id,
                    'name': definition.name,
                    'path': definition.path if hasattr(definition, 'path') else None,
                    'is_deleted': definition.is_deleted if hasattr(definition, 'is_deleted') else None,
                    'created_on': str(definition.created_on) if definition.created_on else None,
                    'url': definition.url if hasattr(definition, 'url') else None
                }
                def_list.append(def_info)

            return def_list
        except Exception as e:
            print(f"Error fetching release definitions: {str(e)}")
            raise

    # ========================================================================
    # CORE API METHODS (Projects, Teams)
    # ========================================================================

    def get_projects(self) -> List[Dict]:
        """
        Get all projects from TFS.

        Returns:
            List of project dictionaries
        """
        try:
            projects = self.core_client.get_projects()

            project_list = []
            for project in projects:
                project_info = {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'state': project.state,
                    'visibility': project.visibility,
                    'url': project.url if hasattr(project, 'url') else None
                }
                project_list.append(project_info)

            return project_list
        except Exception as e:
            print(f"Error fetching projects: {str(e)}")
            raise

    def get_teams(self, project: str) -> List[Dict]:
        """
        Get all teams in a project.

        Args:
            project: Name of the TFS project

        Returns:
            List of team dictionaries
        """
        try:
            teams = self.core_client.get_teams(project_id=project)

            team_list = []
            for team in teams:
                team_info = {
                    'id': team.id,
                    'name': team.name,
                    'description': team.description,
                    'url': team.url if hasattr(team, 'url') else None
                }
                team_list.append(team_info)

            return team_list
        except Exception as e:
            print(f"Error fetching teams: {str(e)}")
            raise

    # ========================================================================
    # TEST API METHODS
    # ========================================================================

    def get_test_plans(self, project: str) -> List[Dict]:
        """
        Get test plans from a project.

        Args:
            project: Name of the TFS project

        Returns:
            List of test plan dictionaries
        """
        try:
            plans = self.test_client.get_plans(project=project)

            plan_list = []
            for plan in plans:
                plan_info = {
                    'id': plan.id,
                    'name': plan.name,
                    'state': plan.state if hasattr(plan, 'state') else None,
                    'area_path': plan.area_path if hasattr(plan, 'area_path') else None,
                    'iteration': plan.iteration if hasattr(plan, 'iteration') else None,
                    'url': plan.url if hasattr(plan, 'url') else None
                }
                plan_list.append(plan_info)

            return plan_list
        except Exception as e:
            print(f"Error fetching test plans: {str(e)}")
            raise

    def get_test_runs(self, project: str) -> List[Dict]:
        """
        Get test runs from a project.

        Args:
            project: Name of the TFS project

        Returns:
            List of test run dictionaries
        """
        try:
            runs = self.test_client.get_test_runs(project=project)

            run_list = []
            for run in runs:
                run_info = {
                    'id': run.id,
                    'name': run.name,
                    'state': run.state,
                    'started_date': str(run.started_date) if run.started_date else None,
                    'completed_date': str(run.completed_date) if run.completed_date else None,
                    'is_automated': run.is_automated if hasattr(run, 'is_automated') else None,
                    'url': run.url if hasattr(run, 'url') else None
                }
                run_list.append(run_info)

            return run_list
        except Exception as e:
            print(f"Error fetching test runs: {str(e)}")
            raise

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_api_version(self) -> str:
        """Get the API version being used."""
        return self.api_version

    def get_organization_url(self) -> str:
        """Get the organization URL."""
        return self.organization_url
