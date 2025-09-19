"""
Test for CommentsController.
"""

from unittest.mock import Mock, patch

from scripts.src.presentation.comments_controller import CommentsController
from scripts.src.application.exceptions.comments_service_error import CommentsServiceError


class TestCommentsController:
    """Test cases for CommentsController."""

    def test_run_正常な引数_サービスが呼ばれ結果が出力される(self):
        # Arrange
        controller = CommentsController()
        
        with patch('scripts.src.infrastructure.service_factory.ServiceFactory.create_comments_service') as mock_create:
            mock_service = Mock()
            mock_service.get_comments_markdown.return_value = "markdown content"
            mock_create.return_value = mock_service
            
            with patch('builtins.print') as mock_print:
                # Act
                controller.run(["--repo", "owner/repo", "--pr", "PR-123"])
                
                # Assert
                mock_create.assert_called_once()
                mock_service.get_comments_markdown.assert_called_once()
                mock_print.assert_called_once_with("markdown content")

    def test_run_CommentsServiceError_エラーメッセージが出力され終了(self):
        # Arrange
        controller = CommentsController()
        
        with patch('scripts.src.infrastructure.service_factory.ServiceFactory.create_comments_service') as mock_create:
            mock_service = Mock()
            mock_service.get_comments_markdown.side_effect = CommentsServiceError("PR not found")
            mock_create.return_value = mock_service
            
            with patch('builtins.print') as mock_print, \
                 patch('sys.exit') as mock_exit:
                # Act
                controller.run(["--repo", "owner/repo", "--pr", "PR-123"])
                
                # Assert
                mock_print.assert_called_once()
                args, kwargs = mock_print.call_args
                assert "Error:" in args[0]
                assert kwargs['file'] is not None  # stderr
                mock_exit.assert_called_once_with(1)

    def test_run_予期せぬエラー_エラーメッセージが出力され終了(self):
        # Arrange
        controller = CommentsController()
        
        with patch('scripts.src.infrastructure.service_factory.ServiceFactory.create_comments_service') as mock_create:
            mock_service = Mock()
            mock_service.get_comments_markdown.side_effect = Exception("unexpected")
            mock_create.return_value = mock_service
            
            with patch('builtins.print') as mock_print, \
                 patch('sys.exit') as mock_exit:
                # Act
                controller.run(["--repo", "owner/repo", "--pr", "PR-123"])
                
                # Assert
                mock_print.assert_called_once()
                args, kwargs = mock_print.call_args
                assert "Unexpected error:" in args[0]
                assert kwargs['file'] is not None  # stderr
                mock_exit.assert_called_once_with(1)

    def test_run_無効なPR形式_エラーメッセージが出力され終了(self):
        # Arrange
        controller = CommentsController()
        
        with patch('builtins.print') as mock_print, \
             patch('sys.exit') as mock_exit:
            # Act
            controller.run(["--repo", "owner/repo", "--pr", "invalid"])
            
            # Assert
            mock_print.assert_called_once()
            args, kwargs = mock_print.call_args
            assert "Error:" in args[0]
            assert "PR number must be in format" in args[0]
            assert kwargs['file'] is not None  # stderr
            mock_exit.assert_called_once_with(1)