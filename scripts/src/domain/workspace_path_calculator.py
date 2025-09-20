"""
Workspace path calculation for workspace management.

This module provides path calculation logic for workspace-related
operations including backup paths and configuration file paths.
"""

from pathlib import Path

from .repository_identifier import RepositoryIdentifier


class WorkspacePathCalculator:
    """Workspace path calculation specialized class.
    
    This class is responsible for calculating various paths
    related to workspace operations such as backup directories
    and configuration file locations.
    """

    # Default workspace directory
    _DEFAULT_WORKSPACE_DIR = Path("workspace")
    
    # Default workspaces backup directory
    _DEFAULT_WORKSPACES_DIR = Path("workspaces")
    
    # Default workspace configuration filename
    _DEFAULT_CONFIG_FILENAME = "workspace.yml"

    @staticmethod
    def get_backup_path(repository_identifier: RepositoryIdentifier) -> Path:
        """Calculate backup directory path for a repository.
        
        Args:
            repository_identifier: Repository identifier
            
        Returns:
            Path object representing backup directory
            
        Examples:
            >>> repo_id = RepositoryIdentifier(owner="owner", name="repo")
            >>> path = WorkspacePathCalculator.get_backup_path(repo_id)
            >>> str(path)
            'workspaces/owner/repo'
        """
        return (WorkspacePathCalculator._DEFAULT_WORKSPACES_DIR / 
                repository_identifier.owner / 
                repository_identifier.name)

    @staticmethod
    def get_workspace_directory() -> Path:
        """Get current workspace directory path.
        
        Returns:
            Path object representing current workspace directory
            
        Examples:
            >>> path = WorkspacePathCalculator.get_workspace_directory()
            >>> str(path)
            'workspace'
        """
        return WorkspacePathCalculator._DEFAULT_WORKSPACE_DIR

    @staticmethod
    def get_workspace_config_path() -> Path:
        """Get workspace configuration file path.
        
        Returns:
            Path object representing workspace.yml file path
            
        Examples:
            >>> path = WorkspacePathCalculator.get_workspace_config_path()
            >>> str(path)
            'workspace/workspace.yml'
        """
        return (WorkspacePathCalculator._DEFAULT_WORKSPACE_DIR / 
                WorkspacePathCalculator._DEFAULT_CONFIG_FILENAME)

    @staticmethod
    def get_workspaces_directory() -> Path:
        """Get workspaces backup directory path.
        
        Returns:
            Path object representing workspaces backup directory
            
        Examples:
            >>> path = WorkspacePathCalculator.get_workspaces_directory()
            >>> str(path)
            'workspaces'
        """
        return WorkspacePathCalculator._DEFAULT_WORKSPACES_DIR

    @staticmethod
    def get_repository_backup_config_path(repository_identifier: RepositoryIdentifier) -> Path:
        """Get backup workspace configuration file path for a repository.
        
        Args:
            repository_identifier: Repository identifier
            
        Returns:
            Path object representing backup workspace.yml file path
            
        Examples:
            >>> repo_id = RepositoryIdentifier(owner="owner", name="repo")
            >>> path = WorkspacePathCalculator.get_repository_backup_config_path(repo_id)
            >>> str(path)
            'workspaces/owner/repo/workspace.yml'
        """
        return (WorkspacePathCalculator.get_backup_path(repository_identifier) / 
                WorkspacePathCalculator._DEFAULT_CONFIG_FILENAME)