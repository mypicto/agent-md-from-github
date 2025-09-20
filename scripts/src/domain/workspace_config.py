"""
Workspace configuration for repository settings.
"""

from ruamel.yaml import YAML
from pathlib import Path
from typing import Optional

from .repository_identifier import RepositoryIdentifier


class WorkspaceConfig:
    """Configuration class for workspace settings."""

    def __init__(self, workspace_path: Path = Path("workspace/workspace.yml")):
        """Initialize workspace config.

        Args:
            workspace_path: Path to workspace.yml file
        """
        self._workspace_path = workspace_path
        self._config: Optional[dict] = None

    def _load_config(self) -> dict:
        """Load configuration from workspace.yml.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If workspace.yml does not exist
            yaml.YAMLError: If YAML parsing fails
        """
        if self._config is None:
            if not self._workspace_path.exists():
                raise FileNotFoundError(f"Workspace configuration file not found: {self._workspace_path}")

            yaml_loader = YAML()
            with open(self._workspace_path, 'r', encoding='utf-8') as f:
                self._config = yaml_loader.load(f)

            if not isinstance(self._config, dict):
                raise ValueError("Invalid workspace configuration format")

        return self._config

    @property
    def organization(self) -> str:
        """Get organization name.

        Returns:
            Organization name

        Raises:
            KeyError: If organization is not found in config
        """
        config = self._load_config()
        return config['workspace']['organization']

    @property
    def repository(self) -> str:
        """Get repository name.

        Returns:
            Repository name

        Raises:
            KeyError: If repository is not found in config
        """
        config = self._load_config()
        return config['workspace']['repository']

    def get_repository_identifier(self) -> RepositoryIdentifier:
        """Get repository identifier from workspace config.

        Returns:
            RepositoryIdentifier instance
        """
        return RepositoryIdentifier(owner=self.organization, name=self.repository)