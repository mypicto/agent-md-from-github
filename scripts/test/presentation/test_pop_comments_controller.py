"""
Test for PopCommentsController.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from scripts.src.presentation.pop_comments_controller import PopCommentsController


class TestPopCommentsController(unittest.TestCase):
    """Test cases for PopCommentsController."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.controller = PopCommentsController()
    
    @patch('scripts.src.presentation.pop_comments_controller.ServiceFactory')
    def test_run_正常系_欠落PRあり(self, mock_factory):
        """正常系: 欠落PRがある場合のテスト"""
        # Arrange
        with patch('scripts.src.presentation.pop_comments_controller.WorkspaceConfig') as mock_workspace:
            mock_service = MagicMock()
            mock_service.get_next_missing_comments_markdown.return_value = "# PR Comments\n\nSome comments..."
            mock_factory.create_pop_comments_service.return_value = mock_service
            mock_repo_id = MagicMock()
            mock_workspace.return_value.get_repository_identifier.return_value = mock_repo_id
            
            # Act
            with patch('builtins.print') as mock_print:
                self.controller.run([])
            
            # Assert
            mock_print.assert_called_once_with("# PR Comments\n\nSome comments...")
    
    @patch('scripts.src.presentation.pop_comments_controller.ServiceFactory')
    def test_run_正常系_欠落PRなし(self, mock_factory):
        """正常系: 欠落PRがない場合のテスト"""
        # Arrange
        with patch('scripts.src.presentation.pop_comments_controller.WorkspaceConfig') as mock_workspace:
            mock_service = MagicMock()
            mock_service.get_next_missing_comments_markdown.return_value = "No missing summaries found."
            mock_factory.create_pop_comments_service.return_value = mock_service
            mock_repo_id = MagicMock()
            mock_workspace.return_value.get_repository_identifier.return_value = mock_repo_id
            
            # Act
            with patch('builtins.print') as mock_print:
                self.controller.run([])
            
            # Assert
            mock_print.assert_called_once_with("No missing summaries found.")
    
    def test_run_異常系_workspace設定なし(self):
        """異常系: workspace.ymlが存在しない場合のテスト"""
        # Act & Assert
        with patch('scripts.src.presentation.pop_comments_controller.WorkspaceConfig') as mock_workspace:
            mock_workspace.return_value.get_repository_identifier.side_effect = FileNotFoundError("Workspace configuration file not found")
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with self.assertRaises(SystemExit):
                    self.controller.run([])
            
            # Assert
            self.assertIn("Error:", mock_stderr.getvalue())