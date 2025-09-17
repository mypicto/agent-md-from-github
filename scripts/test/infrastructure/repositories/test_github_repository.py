"""
Tests for GitHubRepository.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch
from scripts.src.infrastructure.repositories.github_repository import GitHubRepository


class TestGitHubRepository:
    """Test cases for GitHubRepository."""

    def test___init___初期化_リポジトリが正しく初期化される(self):
        """Test __init__ initializes the repository correctly."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        assert repo._github == mock_github
        assert repo._timezone_converter == mock_converter

    def test__extract_review_comments_正常抽出_コメントリストが返される(self):
        """Test _extract_review_comments extracts comments correctly."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        mock_pr = MagicMock()
        mock_comment = MagicMock()
        mock_comment.id = 1
        mock_comment.path = "test.py"
        mock_comment.original_position = 10
        mock_comment.commit_id = "abc123"
        mock_comment.user.login = "testuser"
        mock_comment.created_at = datetime(2023, 1, 1, 12, 0, 0)
        mock_comment.body = "Test comment"

        mock_pr.get_review_comments.return_value = [mock_comment]
        mock_converter.convert_to_target_timezone.return_value = datetime(2023, 1, 1, 12, 0, 0)

        with patch.object(repo, '_extract_diff_context') as mock_extract_diff:
            mock_extract_diff.return_value = "+ test line"

            comments = repo._extract_review_comments(mock_pr)

            assert len(comments) == 1
            assert comments[0].comment_id == 1
            assert comments[0].author == "testuser"

    def test__extract_diff_context_diff_hunkあり_diff_hunkが返される(self):
        """Test _extract_diff_context returns diff_hunk when available."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        mock_comment = MagicMock()
        mock_comment.diff_hunk = "+ test line"
        mock_comment.original_position = 10
        mock_comment.path = "test.py"

        result = repo._extract_diff_context(mock_comment)

        assert result == "+ test line"

    def test__extract_diff_context_diff_hunkなし_デフォルトコンテキストが返される(self):
        """Test _extract_diff_context returns default context when diff_hunk not available."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        mock_comment = MagicMock()
        mock_comment.diff_hunk = None
        mock_comment.original_position = 10
        mock_comment.path = "test.py"

        result = repo._extract_diff_context(mock_comment)

        assert "@@ Position: 10 in test.py @@" in result