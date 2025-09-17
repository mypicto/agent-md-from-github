"""
Tests for DeleteSummariesController.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from scripts.src.presentation.delete_summaries_controller import DeleteSummariesController


class TestDeleteSummariesController:
    """Test cases for DeleteSummariesController."""
    
    def test_run_リポジトリなし(self):
        """Test running without repository argument."""
        controller = DeleteSummariesController()
        
        mock_service = Mock()
        mock_service.delete_summaries.return_value = [Path("file1.md")]
        
        with patch('scripts.src.presentation.delete_summaries_controller.ServiceFactory') as mock_factory:
            mock_factory.create_delete_summaries_service.return_value = mock_service
            
            with patch('builtins.print'):
                controller.run(["--output-dir", "test"])
        
        mock_service.delete_summaries.assert_called_once_with(None, Path("test"))
    
    def test_run_リポジトリ指定(self):
        """Test running with repository argument."""
        controller = DeleteSummariesController()
        
        mock_service = Mock()
        mock_service.delete_summaries.return_value = [Path("file1.md")]
        
        with patch('scripts.src.presentation.delete_summaries_controller.ServiceFactory') as mock_factory:
            mock_factory.create_delete_summaries_service.return_value = mock_service
            
            with patch('builtins.print'):
                controller.run(["--repo", "owner/repo", "--output-dir", "test"])
        
        mock_service.delete_summaries.assert_called_once()
        args = mock_service.delete_summaries.call_args[0]
        assert args[0].owner == "owner"
        assert args[0].name == "repo"
        assert args[1] == Path("test")
    
    def test_run_出力結果(self, capsys):
        """Test output of deleted files."""
        controller = DeleteSummariesController()
        
        mock_service = Mock()
        mock_service.delete_summaries.return_value = [
            Path("pullrequests/owner/repo/PR-123-summary.md"),
            Path("pullrequests/owner/repo/PR-456-summary.md")
        ]
        
        with patch('scripts.src.presentation.delete_summaries_controller.ServiceFactory') as mock_factory:
            mock_factory.create_delete_summaries_service.return_value = mock_service
            
            controller.run([])
        
        captured = capsys.readouterr()
        assert "Deleted 2 summary files:" in captured.out
        assert "PR-123-summary.md" in captured.out
        assert "PR-456-summary.md" in captured.out
    
    def test_run_ファイルなし(self, capsys):
        """Test output when no files found."""
        controller = DeleteSummariesController()
        
        mock_service = Mock()
        mock_service.delete_summaries.return_value = []
        
        with patch('scripts.src.presentation.delete_summaries_controller.ServiceFactory') as mock_factory:
            mock_factory.create_delete_summaries_service.return_value = mock_service
            
            controller.run([])
        
        captured = capsys.readouterr()
        assert "No summary files found to delete." in captured.out