"""
Workspace switching service for application layer.

This module provides the main use case service for workspace switching
operations, orchestrating domain objects and repository interfaces.
"""

import logging
from typing import Optional

from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.repository_identifier_validator import RepositoryIdentifierValidator
from ...domain.workspace_config import WorkspaceConfig
from ...domain.workspace_path_calculator import WorkspacePathCalculator
from ...domain.interfaces.workspace_repository_interface import WorkspaceRepositoryInterface
from ..exceptions.workspace_switch_error import WorkspaceSwitchError


class WorkspaceSwitchService:
    """Workspace switching use case service.
    
    This service orchestrates workspace switching operations by coordinating
    between domain objects and infrastructure implementations following
    Clean Architecture principles.
    """

    def __init__(
        self,
        workspace_repository: WorkspaceRepositoryInterface,
        logger: Optional[logging.Logger] = None
    ):
        """Initialize workspace switch service.
        
        Args:
            workspace_repository: Workspace repository implementation
            logger: Optional logger for operation tracking
        """
        self._workspace_repository = workspace_repository
        self._logger = logger or logging.getLogger(__name__)

    def switch_workspace(self, repository_spec: str) -> None:
        """Switch workspace to specified repository.
        
        This method performs the complete workspace switching operation:
        1. Validate repository specification format
        2. Parse repository identifier
        3. Backup current workspace (if exists)
        4. Clear current workspace
        5. Restore target repository workspace or initialize new one
        
        Args:
            repository_spec: Repository specification in 'owner/repository' format
            
        Raises:
            WorkspaceSwitchError: If any step of the switching process fails
            
        Examples:
            >>> service = WorkspaceSwitchService(workspace_repo)
            >>> service.switch_workspace("owner/repository")
        """
        try:
            self._logger.info(f"Starting workspace switch to: {repository_spec}")
            
            # Step 1: Validate and parse repository specification
            repository_identifier = self._validate_and_parse_repository(repository_spec)
            self._logger.info(f"Validated repository: {repository_identifier.owner}/{repository_identifier.name}")
            
            # Step 2: Backup current workspace if it exists
            if self._workspace_repository.workspace_exists():
                current_repository_identifier = self._get_current_repository_identifier()
                if current_repository_identifier:
                    self._backup_current_workspace(current_repository_identifier)
                else:
                    self._logger.warning("Current workspace exists but has no valid configuration - skipping backup")
            else:
                self._logger.info("No existing workspace to backup")
            
            # Step 3: Clear current workspace
            self._clear_current_workspace()
            
            # Step 4: Restore or initialize target workspace
            if self._workspace_repository.backup_exists(repository_identifier):
                self._restore_target_workspace(repository_identifier)
            else:
                self._initialize_new_workspace(repository_identifier)
                
            self._logger.info(f"Successfully switched to workspace: {repository_spec}")
            
        except Exception as e:
            error_msg = f"Failed to switch workspace to {repository_spec}: {str(e)}"
            self._logger.error(error_msg)
            raise WorkspaceSwitchError(error_msg) from e

    def _get_current_repository_identifier(self) -> Optional[RepositoryIdentifier]:
        """Get current workspace repository identifier.
        
        Returns:
            Current repository identifier if workspace config exists, None otherwise
        """
        try:
            config_path = WorkspacePathCalculator.get_workspace_config_path()
            if not config_path.exists():
                self._logger.debug("Workspace config file does not exist")
                return None
                
            workspace_config = WorkspaceConfig(config_path)
            return workspace_config.get_repository_identifier()
            
        except Exception as e:
            self._logger.warning(f"Failed to read current workspace config: {str(e)}")
            return None

    def _validate_and_parse_repository(self, repository_spec: str) -> RepositoryIdentifier:
        """Validate and parse repository specification.
        
        Args:
            repository_spec: Repository specification string
            
        Returns:
            Parsed repository identifier
            
        Raises:
            WorkspaceSwitchError: If validation fails
        """
        try:
            return RepositoryIdentifierValidator.parse_repository_spec(repository_spec)
        except ValueError as e:
            raise WorkspaceSwitchError(f"Invalid repository specification: {str(e)}") from e

    def _backup_current_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Backup current workspace.
        
        Args:
            repository_identifier: Repository identifier for backup naming
            
        Raises:
            WorkspaceSwitchError: If backup fails
        """
        try:
            self._logger.info("Backing up current workspace...")
            self._workspace_repository.backup_workspace(repository_identifier)
            self._logger.info("Current workspace backed up successfully")
        except Exception as e:
            raise WorkspaceSwitchError(f"Failed to backup current workspace: {str(e)}") from e

    def _clear_current_workspace(self) -> None:
        """Clear current workspace.
        
        Raises:
            WorkspaceSwitchError: If clearing fails
        """
        try:
            self._logger.info("Clearing current workspace...")
            self._workspace_repository.clear_workspace()
            self._logger.info("Current workspace cleared successfully")
        except Exception as e:
            raise WorkspaceSwitchError(f"Failed to clear current workspace: {str(e)}") from e

    def _restore_target_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Restore target workspace from backup.
        
        Args:
            repository_identifier: Repository identifier for restoration
            
        Raises:
            WorkspaceSwitchError: If restoration fails
        """
        try:
            self._logger.info(f"Restoring workspace for {repository_identifier.owner}/{repository_identifier.name}...")
            success = self._workspace_repository.restore_workspace(repository_identifier)
            if not success:
                raise WorkspaceSwitchError("Restoration returned unsuccessful status")
            self._logger.info("Target workspace restored successfully")
        except Exception as e:
            raise WorkspaceSwitchError(f"Failed to restore target workspace: {str(e)}") from e

    def _initialize_new_workspace(self, repository_identifier: RepositoryIdentifier) -> None:
        """Initialize new workspace.
        
        Args:
            repository_identifier: Repository identifier for initialization
            
        Raises:
            WorkspaceSwitchError: If initialization fails
        """
        try:
            self._logger.info(f"Initializing new workspace for {repository_identifier.owner}/{repository_identifier.name}...")
            self._workspace_repository.initialize_workspace(repository_identifier)
            self._logger.info("New workspace initialized successfully")
        except Exception as e:
            raise WorkspaceSwitchError(f"Failed to initialize new workspace: {str(e)}") from e