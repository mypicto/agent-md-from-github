"""
Test for ReviewSummaryController.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import os

from scripts.src.presentation.review_summary_controller import ReviewSummaryController
from scripts.src.application.exceptions.pr_review_collection_error import PRReviewCollectionError


class TestReviewSummaryController:
    """Test cases for ReviewSummaryController."""

    def test_run_正常なファイル_サービスが呼ばれ結果が出力される(self):
        # Arrange
        controller = ReviewSummaryController()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write("Test summary content")
            temp_file_path = temp_file.name
        
        try:
            with patch('scripts.src.infrastructure.service_factory.ServiceFactory.create_review_summary_service') as mock_create:
                mock_service = Mock()
                mock_create.return_value = mock_service
                
                with patch('builtins.print') as mock_print:
                    # Act
                    controller.run(["--repo", "owner/repo", "--pr", "123", "--priority", "high", "--file", temp_file_path])
                    
                    # Assert
                    mock_create.assert_called_once()
                    mock_service.set_summary.assert_called_once()
                    args, kwargs = mock_service.set_summary.call_args
                    assert kwargs['summary'] == "Test summary content"
                    mock_print.assert_called_once_with("Successfully saved summary for PR #123 in owner/repo")
        finally:
            os.unlink(temp_file_path)

    def test_run_ファイル不存在_エラーメッセージが出力され終了(self):
        # Arrange
        controller = ReviewSummaryController()
        
        with patch('builtins.print') as mock_print, \
             patch('sys.exit') as mock_exit:
            # Act
            controller.run(["--repo", "owner/repo", "--pr", "123", "--priority", "high", "--file", "/nonexistent/file.md"])
            
            # Assert
            mock_print.assert_called_once_with("Error: File not found: /nonexistent/file.md", file=mock_print.call_args[1]['file'])
            mock_exit.assert_called_once_with(1)

    def test_run_PRReviewCollectionError_エラーメッセージが出力され終了(self):
        # Arrange
        controller = ReviewSummaryController()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write("Test summary content")
            temp_file_path = temp_file.name
        
        try:
            with patch('scripts.src.infrastructure.service_factory.ServiceFactory.create_review_summary_service') as mock_create:
                mock_service = Mock()
                mock_service.set_summary.side_effect = PRReviewCollectionError("PR not found")
                mock_create.return_value = mock_service
                
                with patch('builtins.print') as mock_print, \
                     patch('sys.exit') as mock_exit:
                    # Act
                    controller.run(["--repo", "owner/repo", "--pr", "123", "--priority", "high", "--file", temp_file_path])
                    
                    # Assert
                    mock_print.assert_called_once_with("Error: PR not found", file=mock_print.call_args[1]['file'])
                    mock_exit.assert_called_once_with(1)
        finally:
            os.unlink(temp_file_path)