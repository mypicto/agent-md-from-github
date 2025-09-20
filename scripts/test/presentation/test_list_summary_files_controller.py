"""
Tests for ListSummaryFilesController.
"""

import pytest
from unittest.mock import Mock, patch
from argparse import Namespace

from scripts.src.presentation.list_summary_files_controller import ListSummaryFilesController
from scripts.src.application.services.list_summary_files_service import ListSummaryFilesService
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestListSummaryFilesController:
    """Test cases for ListSummaryFilesController."""

    @pytest.fixture
    def controller(self):
        """Create the controller."""
        return ListSummaryFilesController()

    @pytest.fixture
    def mock_service(self):
        """Create a mock service."""
        return Mock(spec=ListSummaryFilesService)

    @patch("scripts.src.presentation.list_summary_files_controller.ServiceFactory")
    def test_run_有効な引数_ファイルパスを出力する(self, mock_factory, controller, mock_service, capsys):
        """Test running with valid arguments."""
        # Setup mocks
        mock_factory.create_list_summary_files_service.return_value = mock_service
        mock_service.list_summary_files.return_value = [
            "workspace/summaries/PR-1.yml",
            "workspace/summaries/PR-2.yml"
        ]

        # Mock argument parsing and workspace config
        with patch.object(controller._parser, 'parse_args', return_value=Namespace(
            priority=["high", "middle"]
        )), \
             patch('scripts.src.presentation.list_summary_files_controller.WorkspaceConfig') as mock_workspace:
            mock_repo_id = Mock()
            mock_workspace.return_value.get_repository_identifier.return_value = mock_repo_id
            
            controller.run()

        # Verify service was called correctly
        mock_factory.create_list_summary_files_service.assert_called_once()
        mock_service.list_summary_files.assert_called_once_with(mock_repo_id, ["high", "middle"])

        # Verify output
        captured = capsys.readouterr()
        assert "PR-1.yml" in captured.out
        assert "PR-2.yml" in captured.out

    @patch("scripts.src.presentation.list_summary_files_controller.ServiceFactory")
    def test_run_優先度フィルタなし_全てのファイルを返す(self, mock_factory, controller, mock_service, capsys):
        """Test running without priority filter."""
        # Setup mocks
        mock_factory.create_list_summary_files_service.return_value = mock_service
        mock_service.list_summary_files.return_value = [
            "pullrequests/test-owner/test-repo/summaries/PR-1.yml"
        ]

        # Mock argument parsing
        with patch.object(controller._parser, 'parse_args', return_value=Namespace(
            priority=None
        )), \
             patch('scripts.src.presentation.list_summary_files_controller.WorkspaceConfig') as mock_workspace:
            mock_repo_id = Mock()
            mock_workspace.return_value.get_repository_identifier.return_value = mock_repo_id
            
            controller.run()

        # Verify service was called with empty priority list
        mock_service.list_summary_files.assert_called_once_with(mock_repo_id, [])

    def test_run_workspace設定なし_エラーを出力して終了する(self, controller, capsys):
        """Test running when workspace config is not found."""
        # Mock argument parsing
        with patch.object(controller._parser, 'parse_args', return_value=Namespace(
            priority=["high"]
        )), \
             patch('scripts.src.presentation.list_summary_files_controller.WorkspaceConfig') as mock_workspace:
            mock_workspace.return_value.get_repository_identifier.side_effect = FileNotFoundError("Workspace configuration file not found")
            
            with pytest.raises(SystemExit):
                controller.run()

        # Verify error output
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    @patch("scripts.src.presentation.list_summary_files_controller.ServiceFactory")
    def test_run_サービス例外発生_エラーを出力して終了する(self, mock_factory, controller, mock_service, capsys):
        """Test running when service raises an exception."""
        # Setup mocks
        mock_factory.create_list_summary_files_service.return_value = mock_service
        mock_service.list_summary_files.side_effect = Exception("Service error")

        # Mock argument parsing
        with patch.object(controller._parser, 'parse_args', return_value=Namespace(
            priority=["high"]
        )), \
             patch('scripts.src.presentation.list_summary_files_controller.WorkspaceConfig') as mock_workspace:
            mock_repo_id = Mock()
            mock_workspace.return_value.get_repository_identifier.return_value = mock_repo_id
            
            with pytest.raises(SystemExit):
                controller.run()

        # Verify error output
        captured = capsys.readouterr()
        assert "Unexpected error:" in captured.err

    def test_argument_parser_setup_パーサーが正しく設定されている(self, controller):
        """Test that argument parser is properly configured."""
        parser = controller._parser

        # Check priority argument
        priority_action = next(action for action in parser._actions if action.dest == 'priority')
        assert type(priority_action).__name__ == '_AppendAction'
        assert priority_action.choices == ['high', 'middle', 'low']
        assert priority_action.help == "Priority level to filter by (can be specified multiple times)"
        priority_action = next(action for action in parser._actions if action.dest == 'priority')
        assert priority_action.choices == ["high", "middle", "low"]
        assert priority_action.help == "Priority level to filter by (can be specified multiple times)"