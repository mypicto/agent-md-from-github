"""
Test for CommentsService.
"""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from scripts.src.application.services.comments_service import CommentsService
from scripts.src.application.exceptions.comments_service_error import CommentsServiceError
from scripts.src.domain.comment_thread import CommentThread
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_comment import ReviewComment
from scripts.src.presentation.markdown_formatter import MarkdownFormatter


class TestCommentsService:
    """Test cases for CommentsService."""

    def test_get_comments_markdown_PRが見つからない_エラーが発生する(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.find_all_by_repository.return_value = []
        mock_formatter = Mock()
        
        service = CommentsService(mock_repo, mock_formatter)
        repo_id = RepositoryIdentifier.from_string("owner/repo")
        output_dir = Path("/tmp")
        
        # Act & Assert
        with pytest.raises(CommentsServiceError, match="PR not found: 123"):
            service.get_comments_markdown(repo_id, "123", output_dir)

    def test_get_comments_markdown_コメントがある_正しいMarkdownが返される(self):
        # Arrange
        comment1 = ReviewComment(
            comment_id=1,
            file_path="file1.py",
            position=10,
            commit_id="abc",
            author="user1",
            created_at=datetime(2023, 1, 1, 10, 0),
            body="Comment 1",
            diff_context="+ line1"
        )
        comment2 = ReviewComment(
            comment_id=2,
            file_path="file1.py",
            position=10,
            commit_id="abc",
            author="user2",
            created_at=datetime(2023, 1, 1, 11, 0),
            body="Comment 2",
            diff_context="+ line2"
        )
        comment3 = ReviewComment(
            comment_id=3,
            file_path="file2.py",
            position=None,
            commit_id="def",
            author="user3",
            created_at=datetime(2023, 1, 1, 12, 0),
            body="Comment 3",
            diff_context=""
        )
        
        pr_metadata = PullRequestMetadata(
            number=123,
            title="Test PR",
            closed_at=datetime(2023, 1, 2),
            is_merged=True,
            review_comments=[comment1, comment2, comment3],
            repository_id=RepositoryIdentifier.from_string("owner/repo")
        )
        
        mock_repo = Mock()
        mock_repo.find_all_by_repository.return_value = [pr_metadata]
        mock_formatter = Mock()
        mock_formatter.format.return_value = "formatted markdown"
        
        service = CommentsService(mock_repo, mock_formatter)
        repo_id = RepositoryIdentifier.from_string("owner/repo")
        output_dir = Path("/tmp")
        
        # Act
        result = service.get_comments_markdown(repo_id, "123", output_dir)
        
        # Assert
        assert result == "formatted markdown"
        mock_formatter.format.assert_called_once()