"""
Workspace configuration file generation for workspace management.

This module provides configuration file generation logic for
workspace.yml files with proper structure and formatting.
"""

from pathlib import Path
from typing import Dict, Any

from ruamel.yaml import YAML

from .repository_identifier import RepositoryIdentifier


class WorkspaceConfigGenerator:
    """Workspace configuration file generation specialized class.
    
    This class is responsible for generating workspace.yml configuration
    files with the proper structure and formatting for repository settings.
    """

    @staticmethod
    def generate_config_content(repository_identifier: RepositoryIdentifier) -> Dict[str, Any]:
        """Generate workspace.yml configuration content.
        
        Args:
            repository_identifier: Repository identifier
            
        Returns:
            Dictionary containing workspace configuration structure
            
        Examples:
            >>> repo_id = RepositoryIdentifier(owner="owner", name="repo")
            >>> config = WorkspaceConfigGenerator.generate_config_content(repo_id)
            >>> config
            {'workspace': {'organization': 'owner', 'repository': 'repo'}}
        """
        return {
            'workspace': {
                'organization': repository_identifier.owner,
                'repository': repository_identifier.name
            }
        }

    def create_workspace_config_file(
        self, 
        repository_identifier: RepositoryIdentifier,
        workspace_path: Path
    ) -> None:
        """Create workspace.yml configuration file.
        
        Args:
            repository_identifier: Repository identifier
            workspace_path: Path to workspace.yml file
            
        Raises:
            OSError: If file creation fails
            PermissionError: If insufficient permissions to create file
            
        Examples:
            >>> generator = WorkspaceConfigGenerator()
            >>> repo_id = RepositoryIdentifier(owner="owner", name="repo")
            >>> generator.create_workspace_config_file(repo_id, Path("workspace/workspace.yml"))
        """
        # Generate configuration content
        config_content = self.generate_config_content(repository_identifier)
        
        # Ensure parent directory exists
        workspace_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create YAML writer with proper formatting
        yaml_writer = YAML()
        yaml_writer.default_flow_style = False
        yaml_writer.indent(mapping=2, sequence=4, offset=2)
        
        # Write configuration file
        with open(workspace_path, 'w', encoding='utf-8') as f:
            yaml_writer.dump(config_content, f)

    @staticmethod
    def validate_config_content(config_content: Dict[str, Any]) -> bool:
        """Validate workspace configuration content structure.
        
        Args:
            config_content: Configuration content to validate
            
        Returns:
            True if valid structure, False otherwise
            
        Examples:
            >>> config = {'workspace': {'organization': 'owner', 'repository': 'repo'}}
            >>> WorkspaceConfigGenerator.validate_config_content(config)
            True
            >>> invalid_config = {'invalid': 'structure'}
            >>> WorkspaceConfigGenerator.validate_config_content(invalid_config)
            False
        """
        try:
            # Check basic structure
            if not isinstance(config_content, dict):
                return False
                
            if 'workspace' not in config_content:
                return False
                
            workspace_config = config_content['workspace']
            if not isinstance(workspace_config, dict):
                return False
                
            # Check required fields
            required_fields = ['organization', 'repository']
            for field in required_fields:
                if field not in workspace_config:
                    return False
                if not isinstance(workspace_config[field], str):
                    return False
                if not workspace_config[field].strip():
                    return False
                    
            return True
            
        except (KeyError, TypeError, AttributeError):
            return False