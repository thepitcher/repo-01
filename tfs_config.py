"""
Configuration utilities for TFS Client.

Supports loading configuration from file or environment variables.
"""

import os
import configparser
from typing import Optional, Dict


class TFSConfig:
    """Configuration manager for TFS Client with support for multiple authentication methods."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize TFS configuration.

        Args:
            config_file: Path to configuration file (INI format). If not provided,
                        will look for 'tfs_config.ini' in current directory or use environment variables.
        """
        self.config = configparser.ConfigParser()
        self.config_loaded = False

        # Try to load from config file
        if config_file and os.path.exists(config_file):
            self.config.read(config_file)
            self.config_loaded = True
        elif os.path.exists('tfs_config.ini'):
            self.config.read('tfs_config.ini')
            self.config_loaded = True

    def get_connection_params(self) -> Dict[str, Optional[str]]:
        """
        Get connection parameters from config file or environment variables.

        Returns:
            Dictionary with connection parameters including organization_url, username,
            password, and personal_access_token.
        """
        params = {}

        # Get organization URL
        if self.config_loaded and self.config.has_option('server', 'url'):
            params['organization_url'] = self.config.get('server', 'url')
        else:
            params['organization_url'] = os.getenv('TFS_URL', 'http://tfs-server:8080/tfs/DefaultCollection')

        # Get authentication parameters
        # Priority: Username/Password > Personal Access Token > Default Credentials
        if self.config_loaded:
            # Try username/password from config
            if self.config.has_option('auth', 'username') and self.config.has_option('auth', 'password'):
                params['username'] = self.config.get('auth', 'username')
                params['password'] = self.config.get('auth', 'password')
                params['personal_access_token'] = None
            # Try PAT from config
            elif self.config.has_option('auth', 'personal_access_token'):
                params['personal_access_token'] = self.config.get('auth', 'personal_access_token')
                params['username'] = None
                params['password'] = None
            # Use default credentials
            else:
                params['use_default_credentials'] = True
                params['username'] = None
                params['password'] = None
                params['personal_access_token'] = None
        else:
            # Try environment variables
            username = os.getenv('TFS_USERNAME')
            password = os.getenv('TFS_PASSWORD')
            pat = os.getenv('TFS_PAT')

            if username and password:
                params['username'] = username
                params['password'] = password
                params['personal_access_token'] = None
            elif pat:
                params['personal_access_token'] = pat
                params['username'] = None
                params['password'] = None
            else:
                params['use_default_credentials'] = True
                params['username'] = None
                params['password'] = None
                params['personal_access_token'] = None

        return params

    def get_project(self) -> str:
        """Get project name from config or environment."""
        if self.config_loaded and self.config.has_option('project', 'name'):
            return self.config.get('project', 'name')
        return os.getenv('TFS_PROJECT', 'YourProjectName')

    def get_repository(self) -> str:
        """Get repository name from config or environment."""
        if self.config_loaded and self.config.has_option('project', 'repository'):
            return self.config.get('project', 'repository')
        return os.getenv('TFS_REPOSITORY', 'YourRepositoryName')

    def get_auth_method(self) -> str:
        """
        Determine which authentication method is being used.

        Returns:
            One of: 'username_password', 'personal_access_token', 'default_credentials'
        """
        params = self.get_connection_params()

        if params.get('username') and params.get('password'):
            return 'username_password'
        elif params.get('personal_access_token'):
            return 'personal_access_token'
        else:
            return 'default_credentials'
