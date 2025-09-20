"""
Tests for FileSystemWorkspaceRepository class.
"""

import pytest
import tempfile
import shutil
import logging
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.src.infrastructure.repositories.filesystem_workspace_repository import FileSystemWorkspaceRepository
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestFileSystemWorkspaceRepository:
    """Test cases for FileSystemWorkspaceRepository class."""

    def setup_method(self):
        """各テストメソッドの前に実行される準備処理."""
        self.mock_logger = Mock(spec=logging.Logger)
        self.repository = FileSystemWorkspaceRepository(self.mock_logger)
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """各テストメソッドの後に実行される清理処理."""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def create_temp_workspace(self):
        """テスト用の一時ワークスペースを作成する."""
        workspace_dir = Path(self.temp_dir) / "workspace"
        workspace_dir.mkdir()
        
        # Create sample files
        (workspace_dir / "workspace.yml").write_text("test config")
        (workspace_dir / "pullrequests").mkdir()
        (workspace_dir / "summaries").mkdir()
        (workspace_dir / "pullrequests" / "test.json").write_text("test data")
        
        return workspace_dir

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_backup_workspace_success(self, mock_path_calc):
        """ワークスペースバックアップの成功をテストする."""
        workspace_dir = self.create_temp_workspace()
        backup_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        mock_path_calc.get_backup_path.return_value = backup_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute
        self.repository.backup_workspace(repo_id)
        
        # Verify backup exists
        assert backup_dir.exists()
        assert (backup_dir / "workspace.yml").exists()
        assert (backup_dir / "pullrequests").exists()
        assert (backup_dir / "summaries").exists()
        assert (backup_dir / "pullrequests" / "test.json").exists()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_backup_workspace_overwrite_existing(self, mock_path_calc):
        """既存のバックアップを上書きするワークスペースバックアップをテストする."""
        workspace_dir = self.create_temp_workspace()
        backup_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        
        # Create existing backup
        backup_dir.mkdir(parents=True)
        (backup_dir / "old_file.txt").write_text("old content")
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        mock_path_calc.get_backup_path.return_value = backup_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute
        self.repository.backup_workspace(repo_id)
        
        # Verify old backup is replaced
        assert backup_dir.exists()
        assert not (backup_dir / "old_file.txt").exists()
        assert (backup_dir / "workspace.yml").exists()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_backup_workspace_no_workspace(self, mock_path_calc):
        """ワークスペースが存在しない場合のバックアップをテストする."""
        nonexistent_dir = Path(self.temp_dir) / "nonexistent"
        backup_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        
        mock_path_calc.get_workspace_directory.return_value = nonexistent_dir
        mock_path_calc.get_backup_path.return_value = backup_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute (should not raise exception)
        self.repository.backup_workspace(repo_id)
        
        # Verify no backup created
        assert not backup_dir.exists()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_clear_workspace_success(self, mock_path_calc):
        """ワークスペースクリアの成功をテストする."""
        workspace_dir = self.create_temp_workspace()
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        
        # Verify initial state
        assert (workspace_dir / "workspace.yml").exists()
        assert (workspace_dir / "pullrequests").exists()
        
        # Execute
        self.repository.clear_workspace()
        
        # Verify contents cleared but directory exists
        assert workspace_dir.exists()
        assert not (workspace_dir / "workspace.yml").exists()
        assert not (workspace_dir / "pullrequests").exists()
        assert not (workspace_dir / "summaries").exists()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_clear_workspace_no_workspace(self, mock_path_calc):
        """ワークスペースが存在しない場合のクリアをテストする."""
        nonexistent_dir = Path(self.temp_dir) / "nonexistent"
        
        mock_path_calc.get_workspace_directory.return_value = nonexistent_dir
        
        # Execute (should not raise exception)
        self.repository.clear_workspace()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_restore_workspace_success(self, mock_path_calc):
        """ワークスペース復元の成功をテストする."""
        workspace_dir = Path(self.temp_dir) / "workspace"
        backup_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        
        # Create backup
        backup_dir.mkdir(parents=True)
        (backup_dir / "workspace.yml").write_text("backup config")
        (backup_dir / "pullrequests").mkdir()
        (backup_dir / "pullrequests" / "backup.json").write_text("backup data")
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        mock_path_calc.get_backup_path.return_value = backup_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute
        result = self.repository.restore_workspace(repo_id)
        
        # Verify success
        assert result is True
        assert workspace_dir.exists()
        assert (workspace_dir / "workspace.yml").exists()
        assert (workspace_dir / "pullrequests" / "backup.json").exists()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_restore_workspace_no_backup(self, mock_path_calc):
        """バックアップが存在しない場合の復元をテストする."""
        workspace_dir = Path(self.temp_dir) / "workspace"
        backup_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        mock_path_calc.get_backup_path.return_value = backup_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute
        result = self.repository.restore_workspace(repo_id)
        
        # Verify failure
        assert result is False

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_initialize_workspace_success(self, mock_path_calc):
        """ワークスペース初期化の成功をテストする."""
        workspace_dir = Path(self.temp_dir) / "workspace"
        config_path = workspace_dir / "workspace.yml"
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        mock_path_calc.get_workspace_config_path.return_value = config_path
        
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        
        # Execute
        self.repository.initialize_workspace(repo_id)
        
        # Verify workspace structure
        assert workspace_dir.exists()
        assert (workspace_dir / "pullrequests").exists()
        assert (workspace_dir / "summaries").exists()
        assert (workspace_dir / "temp").exists()
        assert config_path.exists()

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_workspace_exists_true(self, mock_path_calc):
        """ワークスペース存在確認（存在する場合）をテストする."""
        workspace_dir = self.create_temp_workspace()
        
        mock_path_calc.get_workspace_directory.return_value = workspace_dir
        
        # Execute
        result = self.repository.workspace_exists()
        
        # Verify
        assert result is True

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_workspace_exists_false(self, mock_path_calc):
        """ワークスペース存在確認（存在しない場合）をテストする."""
        nonexistent_dir = Path(self.temp_dir) / "nonexistent"
        
        mock_path_calc.get_workspace_directory.return_value = nonexistent_dir
        
        # Execute
        result = self.repository.workspace_exists()
        
        # Verify
        assert result is False

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_backup_exists_true(self, mock_path_calc):
        """バックアップ存在確認（存在する場合）をテストする."""
        backup_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        backup_dir.mkdir(parents=True)
        
        mock_path_calc.get_backup_path.return_value = backup_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute
        result = self.repository.backup_exists(repo_id)
        
        # Verify
        assert result is True

    @patch('scripts.src.infrastructure.repositories.filesystem_workspace_repository.WorkspacePathCalculator')
    def test_backup_exists_false(self, mock_path_calc):
        """バックアップ存在確認（存在しない場合）をテストする."""
        nonexistent_dir = Path(self.temp_dir) / "workspaces" / "owner" / "repo"
        
        mock_path_calc.get_backup_path.return_value = nonexistent_dir
        
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        # Execute
        result = self.repository.backup_exists(repo_id)
        
        # Verify
        assert result is False