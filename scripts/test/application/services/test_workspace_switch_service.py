"""
Tests for WorkspaceSwitchService class.
"""

import pytest
import logging
from unittest.mock import Mock, patch

from scripts.src.application.services.workspace_switch_service import WorkspaceSwitchService
from scripts.src.application.exceptions.workspace_switch_error import WorkspaceSwitchError
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestWorkspaceSwitchService:
    """Test cases for WorkspaceSwitchService class."""

    def setup_method(self):
        """各テストメソッドの前に実行される準備処理."""
        self.mock_workspace_repository = Mock()
        self.mock_logger = Mock(spec=logging.Logger)
        self.service = WorkspaceSwitchService(
            self.mock_workspace_repository,
            self.mock_logger
        )

    def test_switch_workspace_success_restore_existing(self):
        """既存のワークスペースが存在する場合の切り替え成功をテストする."""
        # Setup mocks
        current_repo_id = RepositoryIdentifier(owner="current-owner", name="current-repo")
        target_repo_id = RepositoryIdentifier(owner="owner", name="repo")
        
        self.mock_workspace_repository.workspace_exists.return_value = True
        self.mock_workspace_repository.backup_exists.return_value = True
        self.mock_workspace_repository.restore_workspace.return_value = True
        
        # Mock current workspace config reading
        with patch.object(self.service, '_get_current_repository_identifier', return_value=current_repo_id):
            # Execute
            self.service.switch_workspace("owner/repo")
        
        # Verify calls
        self.mock_workspace_repository.workspace_exists.assert_called_once()
        self.mock_workspace_repository.backup_workspace.assert_called_once_with(current_repo_id)
        self.mock_workspace_repository.clear_workspace.assert_called_once()
        self.mock_workspace_repository.backup_exists.assert_called_once_with(target_repo_id)
        self.mock_workspace_repository.restore_workspace.assert_called_once_with(target_repo_id)
        self.mock_workspace_repository.initialize_workspace.assert_not_called()

    def test_switch_workspace_success_initialize_new(self):
        """新しいワークスペースの初期化による切り替え成功をテストする."""
        # Setup mocks
        current_repo_id = RepositoryIdentifier(owner="current-owner", name="current-repo")
        target_repo_id = RepositoryIdentifier(owner="my-org", name="my-project")
        
        self.mock_workspace_repository.workspace_exists.return_value = True
        self.mock_workspace_repository.backup_exists.return_value = False
        
        # Mock current workspace config reading
        with patch.object(self.service, '_get_current_repository_identifier', return_value=current_repo_id):
            # Execute
            self.service.switch_workspace("my-org/my-project")
        
        # Verify calls
        self.mock_workspace_repository.workspace_exists.assert_called_once()
        self.mock_workspace_repository.backup_workspace.assert_called_once_with(current_repo_id)
        self.mock_workspace_repository.clear_workspace.assert_called_once()
        self.mock_workspace_repository.backup_exists.assert_called_once_with(target_repo_id)
        self.mock_workspace_repository.restore_workspace.assert_not_called()
        self.mock_workspace_repository.initialize_workspace.assert_called_once_with(target_repo_id)

    def test_switch_workspace_no_existing_workspace(self):
        """既存のワークスペースが存在しない場合の切り替え成功をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = False
        self.mock_workspace_repository.backup_exists.return_value = False
        
        # Execute
        self.service.switch_workspace("owner/repo")
        
        # Verify calls
        self.mock_workspace_repository.workspace_exists.assert_called_once()
        self.mock_workspace_repository.backup_workspace.assert_not_called()
        self.mock_workspace_repository.clear_workspace.assert_called_once()
        self.mock_workspace_repository.backup_exists.assert_called_once()
        self.mock_workspace_repository.initialize_workspace.assert_called_once()

    def test_switch_workspace_invalid_repository_spec(self):
        """無効なリポジトリ仕様による切り替え失敗をテストする."""
        invalid_specs = [
            "invalid",
            "owner/",
            "/repo",
            "",
            "owner//repo"
        ]
        
        for spec in invalid_specs:
            with pytest.raises(WorkspaceSwitchError, match="Invalid repository specification"):
                self.service.switch_workspace(spec)

    def test_switch_workspace_backup_failure(self):
        """バックアップ失敗による切り替え失敗をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = True
        self.mock_workspace_repository.backup_workspace.side_effect = Exception("Backup failed")
        
        # Execute and verify
        with pytest.raises(WorkspaceSwitchError, match="Failed to switch workspace"):
            self.service.switch_workspace("owner/repo")

    def test_switch_workspace_clear_failure(self):
        """ワークスペースクリア失敗による切り替え失敗をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = False
        self.mock_workspace_repository.clear_workspace.side_effect = Exception("Clear failed")
        
        # Execute and verify
        with pytest.raises(WorkspaceSwitchError, match="Failed to switch workspace"):
            self.service.switch_workspace("owner/repo")

    def test_switch_workspace_restore_failure(self):
        """復元失敗による切り替え失敗をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = False
        self.mock_workspace_repository.backup_exists.return_value = True
        self.mock_workspace_repository.restore_workspace.side_effect = Exception("Restore failed")
        
        # Execute and verify
        with pytest.raises(WorkspaceSwitchError, match="Failed to switch workspace"):
            self.service.switch_workspace("owner/repo")

    def test_switch_workspace_restore_unsuccessful(self):
        """復元が非成功ステータスを返す場合の切り替え失敗をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = False
        self.mock_workspace_repository.backup_exists.return_value = True
        self.mock_workspace_repository.restore_workspace.return_value = False
        
        # Execute and verify
        with pytest.raises(WorkspaceSwitchError, match="Failed to switch workspace"):
            self.service.switch_workspace("owner/repo")

    def test_switch_workspace_initialization_failure(self):
        """初期化失敗による切り替え失敗をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = False
        self.mock_workspace_repository.backup_exists.return_value = False
        self.mock_workspace_repository.initialize_workspace.side_effect = Exception("Init failed")
        
        # Execute and verify
        with pytest.raises(WorkspaceSwitchError, match="Failed to switch workspace"):
            self.service.switch_workspace("owner/repo")

    def test_switch_workspace_logging(self):
        """ワークスペース切り替え処理のログ出力をテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = True
        self.mock_workspace_repository.backup_exists.return_value = True
        self.mock_workspace_repository.restore_workspace.return_value = True
        
        # Execute
        self.service.switch_workspace("owner/repo")
        
        # Verify logging calls
        self.mock_logger.info.assert_called()
        log_messages = [call.args[0] for call in self.mock_logger.info.call_args_list]
        
        assert any("Starting workspace switch" in msg for msg in log_messages)
        assert any("Successfully switched to workspace" in msg for msg in log_messages)

    def test_switch_workspace_without_logger(self):
        """ロガーなしでのワークスペース切り替えをテストする."""
        service_without_logger = WorkspaceSwitchService(self.mock_workspace_repository)
        
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = False
        self.mock_workspace_repository.backup_exists.return_value = False
        
        # Execute (should not raise exception)
        service_without_logger.switch_workspace("owner/repo")
        
        # Verify basic flow
        self.mock_workspace_repository.clear_workspace.assert_called_once()
        self.mock_workspace_repository.initialize_workspace.assert_called_once()

    def test_switch_workspace_with_invalid_current_config(self):
        """現在のワークスペース設定が無効な場合の切り替えをテストする."""
        # Setup mocks
        self.mock_workspace_repository.workspace_exists.return_value = True
        self.mock_workspace_repository.backup_exists.return_value = False
        
        # Mock invalid current workspace config reading
        with patch.object(self.service, '_get_current_repository_identifier', return_value=None):
            # Execute
            self.service.switch_workspace("owner/repo")
        
        # Verify calls - should skip backup but continue with other operations
        self.mock_workspace_repository.workspace_exists.assert_called_once()
        self.mock_workspace_repository.backup_workspace.assert_not_called()
        self.mock_workspace_repository.clear_workspace.assert_called_once()
        self.mock_workspace_repository.initialize_workspace.assert_called_once()