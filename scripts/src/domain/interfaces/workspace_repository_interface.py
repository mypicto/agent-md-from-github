"""
Workspace repository interface for workspace management operations.

This module defines the abstract interface for workspace-related
operations that can be implemented by different storage backends.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from ..repository_identifier import RepositoryIdentifier


class WorkspaceRepositoryInterface(ABC):
    """Abstract interface for workspace operations.
    
    This interface defines the contract for workspace management operations
    including backup, restoration, clearing, and initialization. Different
    implementations can provide various storage backends (filesystem, cloud, etc.).
    """

    @abstractmethod
    def backup_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Backup current workspace to repository-specific location.
        
        Args:
            repository_identifier: Target repository identifier for backup
            
        Raises:
            WorkspaceBackupError: If backup operation fails
        """
        pass

    @abstractmethod
    def clear_workspace(self) -> None:
        """Clear current workspace directory contents.
        
        Removes all files and directories from the current workspace
        while preserving the workspace directory structure.
        
        Raises:
            WorkspaceClearError: If clear operation fails
        """
        pass

    @abstractmethod
    def restore_workspace(self, repository_identifier: RepositoryIdentifier) -> bool:
        """Restore workspace from repository-specific backup location.
        
        Args:
            repository_identifier: Source repository identifier for restoration
            
        Returns:
            True if restoration was successful, False if backup doesn't exist
            
        Raises:
            WorkspaceRestoreError: If restore operation fails
        """
        pass

    @abstractmethod
    def initialize_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Initialize new workspace for repository.
        
        Creates a new workspace structure with proper configuration
        for the specified repository.
        
        Args:
            repository_identifier: Repository identifier for initialization
            
        Raises:
            WorkspaceInitializationError: If initialization fails
        """
        pass

    @abstractmethod
    def workspace_exists(self) -> bool:
        """Check if workspace directory exists.
        
        Returns:
            True if workspace exists, False otherwise
        """
        pass

    @abstractmethod
    def backup_exists(self, repository_identifier: RepositoryIdentifier) -> bool:
        """Check if backup exists for repository.
        
        Args:
            repository_identifier: Repository identifier to check
            
        Returns:
            True if backup exists, False otherwise
        """
        pass