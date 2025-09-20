"""
Filesystem-based workspace repository implementation.

This module provides a concrete implementation of the workspace repository
interface using the local filesystem for workspace operations.
"""

import shutil
import logging
from pathlib import Path
from typing import Optional

from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.workspace_path_calculator import WorkspacePathCalculator
from ...domain.workspace_config_generator import WorkspaceConfigGenerator
from ...domain.interfaces.workspace_repository_interface import WorkspaceRepositoryInterface


class FileSystemWorkspaceRepository(WorkspaceRepositoryInterface):
    """Filesystem-based implementation of workspace repository interface.
    
    This class implements workspace operations using the local filesystem,
    providing backup, restoration, clearing, and initialization capabilities.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize filesystem workspace repository.
        
        Args:
            logger: Optional logger for operation tracking
        """
        self._logger = logger or logging.getLogger(__name__)
        self._config_generator = WorkspaceConfigGenerator()

    def backup_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Backup current workspace to repository-specific location.
        
        Args:
            repository_identifier: Target repository identifier for backup
            
        Raises:
            OSError: If filesystem operations fail
            PermissionError: If insufficient permissions
        """
        workspace_dir = WorkspacePathCalculator.get_workspace_directory()
        backup_dir = WorkspacePathCalculator.get_backup_path(repository_identifier)
        
        if not workspace_dir.exists():
            self._logger.info("No workspace directory to backup")
            return
            
        # Remove existing backup if it exists
        if backup_dir.exists():
            self._logger.info(f"Removing existing backup at: {backup_dir}")
            shutil.rmtree(backup_dir)
        
        # Create backup directory structure
        backup_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy workspace to backup location
        self._logger.info(f"Copying workspace from {workspace_dir} to {backup_dir}")
        shutil.copytree(workspace_dir, backup_dir)
        
        self._logger.info(f"Workspace backed up to: {backup_dir}")

    def clear_workspace(self) -> None:
        """Clear current workspace directory contents.
        
        Raises:
            OSError: If filesystem operations fail
            PermissionError: If insufficient permissions
        """
        workspace_dir = WorkspacePathCalculator.get_workspace_directory()
        
        if not workspace_dir.exists():
            self._logger.info("No workspace directory to clear")
            return
            
        # Remove all contents of workspace directory
        for item in workspace_dir.iterdir():
            if item.is_file():
                item.unlink()
                self._logger.debug(f"Removed file: {item}")
            elif item.is_dir():
                shutil.rmtree(item)
                self._logger.debug(f"Removed directory: {item}")
                
        self._logger.info("Workspace directory cleared")

    def restore_workspace(self, repository_identifier: RepositoryIdentifier) -> bool:
        """Restore workspace from repository-specific backup location.
        
        Args:
            repository_identifier: Source repository identifier for restoration
            
        Returns:
            True if restoration was successful, False if backup doesn't exist
            
        Raises:
            OSError: If filesystem operations fail
            PermissionError: If insufficient permissions
        """
        backup_dir = WorkspacePathCalculator.get_backup_path(repository_identifier)
        workspace_dir = WorkspacePathCalculator.get_workspace_directory()
        
        if not backup_dir.exists():
            self._logger.info(f"No backup found at: {backup_dir}")
            return False
            
        # Ensure workspace directory exists
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy backup contents to workspace
        self._copy_directory_contents(backup_dir, workspace_dir)
        
        self._logger.info(f"Workspace restored from: {backup_dir}")
        return True

    def initialize_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Initialize new workspace for repository.
        
        Args:
            repository_identifier: Repository identifier for initialization
            
        Raises:
            OSError: If filesystem operations fail
            PermissionError: If insufficient permissions
        """
        workspace_dir = WorkspacePathCalculator.get_workspace_directory()
        config_path = WorkspacePathCalculator.get_workspace_config_path()
        
        # Create workspace directory structure
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (workspace_dir / "pullrequests").mkdir(exist_ok=True)
        (workspace_dir / "summaries").mkdir(exist_ok=True)
        (workspace_dir / "temp").mkdir(exist_ok=True)
        
        # Create workspace configuration file
        self._config_generator.create_workspace_config_file(
            repository_identifier, 
            config_path
        )
        
        self._logger.info(f"Initialized new workspace for: {repository_identifier.owner}/{repository_identifier.name}")

    def workspace_exists(self) -> bool:
        """Check if workspace directory exists.
        
        Returns:
            True if workspace exists, False otherwise
        """
        workspace_dir = WorkspacePathCalculator.get_workspace_directory()
        return workspace_dir.exists() and workspace_dir.is_dir()

    def backup_exists(self, repository_identifier: RepositoryIdentifier) -> bool:
        """Check if backup exists for repository.
        
        Args:
            repository_identifier: Repository identifier to check
            
        Returns:
            True if backup exists, False otherwise
        """
        backup_dir = WorkspacePathCalculator.get_backup_path(repository_identifier)
        return backup_dir.exists() and backup_dir.is_dir()

    def _copy_directory_contents(self, source_dir: Path, target_dir: Path) -> None:
        """Copy contents of source directory to target directory.
        
        Args:
            source_dir: Source directory path
            target_dir: Target directory path
            
        Raises:
            OSError: If filesystem operations fail
        """
        for item in source_dir.iterdir():
            target_item = target_dir / item.name
            
            if item.is_file():
                shutil.copy2(item, target_item)
                self._logger.debug(f"Copied file: {item} -> {target_item}")
            elif item.is_dir():
                shutil.copytree(item, target_item)
                self._logger.debug(f"Copied directory: {item} -> {target_item}")