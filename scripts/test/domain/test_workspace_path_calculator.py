"""
Tests for WorkspacePathCalculator class.
"""

import pytest
from pathlib import Path

from scripts.src.domain.workspace_path_calculator import WorkspacePathCalculator
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestWorkspacePathCalculator:
    """Test cases for WorkspacePathCalculator class."""

    def test_get_backup_path_simple_repository(self):
        """シンプルなリポジトリのバックアップパスの計算をテストする."""
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        expected = Path("workspaces/owner/repo")
        result = WorkspacePathCalculator.get_backup_path(repo_id)
        
        assert result == expected
        assert str(result) == "workspaces/owner/repo"

    def test_get_backup_path_organization_repository(self):
        """組織リポジトリのバックアップパスの計算をテストする."""
        repo_id = RepositoryIdentifier(owner="my-org", name="my-project")
        expected = Path("workspaces/my-org/my-project")
        result = WorkspacePathCalculator.get_backup_path(repo_id)
        
        assert result == expected
        assert str(result) == "workspaces/my-org/my-project"

    def test_get_backup_path_special_characters(self):
        """特殊文字を含むリポジトリのバックアップパスの計算をテストする."""
        repo_id = RepositoryIdentifier(owner="user-name", name="repo_with.dots")
        expected = Path("workspaces/user-name/repo_with.dots")
        result = WorkspacePathCalculator.get_backup_path(repo_id)
        
        assert result == expected

    def test_get_workspace_directory(self):
        """ワークスペースディレクトリパスの取得をテストする."""
        expected = Path("workspace")
        result = WorkspacePathCalculator.get_workspace_directory()
        
        assert result == expected
        assert str(result) == "workspace"

    def test_get_workspace_config_path(self):
        """ワークスペース設定ファイルパスの取得をテストする."""
        expected = Path("workspace/workspace.yml")
        result = WorkspacePathCalculator.get_workspace_config_path()
        
        assert result == expected
        assert str(result) == "workspace/workspace.yml"

    def test_get_workspaces_directory(self):
        """ワークスペースバックアップディレクトリパスの取得をテストする."""
        expected = Path("workspaces")
        result = WorkspacePathCalculator.get_workspaces_directory()
        
        assert result == expected
        assert str(result) == "workspaces"

    def test_get_repository_backup_config_path(self):
        """リポジトリバックアップ設定ファイルパスの取得をテストする."""
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        expected = Path("workspaces/owner/repo/workspace.yml")
        result = WorkspacePathCalculator.get_repository_backup_config_path(repo_id)
        
        assert result == expected
        assert str(result) == "workspaces/owner/repo/workspace.yml"

    def test_paths_are_relative(self):
        """すべてのパスが相対パスであることをテストする."""
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        paths = [
            WorkspacePathCalculator.get_backup_path(repo_id),
            WorkspacePathCalculator.get_workspace_directory(),
            WorkspacePathCalculator.get_workspace_config_path(),
            WorkspacePathCalculator.get_workspaces_directory(),
            WorkspacePathCalculator.get_repository_backup_config_path(repo_id)
        ]
        
        for path in paths:
            assert not path.is_absolute(), f"Path should be relative: {path}"

    def test_path_consistency(self):
        """パス計算の一貫性をテストする."""
        repo_id = RepositoryIdentifier(owner="test-org", name="test-repo")
        
        backup_path = WorkspacePathCalculator.get_backup_path(repo_id)
        config_path = WorkspacePathCalculator.get_repository_backup_config_path(repo_id)
        
        # Config path should be backup path + workspace.yml
        expected_config = backup_path / "workspace.yml"
        assert config_path == expected_config