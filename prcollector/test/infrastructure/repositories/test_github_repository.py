"""
Tests for GitHubRepository.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from github.GithubException import GithubException
from prcollector.src.infrastructure.repositories.github_repository import GitHubRepository
from prcollector.src.domain.date_range import DateRange
from prcollector.src.domain.repository_identifier import RepositoryIdentifier


class TestGitHubRepository:
    """Test cases for GitHubRepository."""

    def test___init___初期化_リポジトリが正しく初期化される(self):
        """Test __init__ initializes the repository correctly."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        assert repo._github == mock_github
        assert repo._timezone_converter == mock_converter

    def test_find_closed_pull_requests_in_range_正常検索_PRメタデータが返される(self):
        """Test find_closed_pull_requests_in_range returns PR metadata."""
        mock_github = MagicMock()
        mock_converter = MagicMock()
        mock_repo = MagicMock()
        mock_pr = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        repo_id = RepositoryIdentifier(owner="test", name="repo")
        mock_date_range = MagicMock()
        mock_date_range.contains.return_value = True

        mock_github.get_repo.return_value = mock_repo
        mock_repo.get_pulls.return_value = [mock_pr]
        mock_pr.closed_at = datetime(2023, 1, 1, 12, 0, 0)
        mock_pr.number = 1
        mock_pr.title = "Test PR"
        mock_pr.merged = True
        mock_converter.convert_to_target_timezone.return_value = datetime(2023, 1, 1, 12, 0, 0)

        with patch.object(repo, '_convert_to_pr_metadata') as mock_convert:
            mock_convert.return_value = MagicMock()

            prs = list(repo.find_closed_pull_requests_in_range(repo_id, mock_date_range))

            assert len(prs) == 1
            mock_github.get_repo.assert_called_once_with("test/repo")
            mock_repo.get_pulls.assert_called_once()

    def test_find_closed_pull_requests_in_range_リポジトリアクセスエラー_GitHubApiErrorが発生する(self):
        """Test find_closed_pull_requests_in_range raises GitHubApiError on repo access error."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        repo_id = RepositoryIdentifier(owner="test", name="repo")
        date_range = DateRange(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2)
        )

        mock_github.get_repo.side_effect = GithubException("Access denied")

        from prcollector.src.application.exceptions.github_api_error import GitHubApiError
        with pytest.raises(GitHubApiError):
            list(repo.find_closed_pull_requests_in_range(repo_id, date_range))

    def test__convert_to_pr_metadata_正常変換_PRメタデータが作成される(self):
        """Test _convert_to_pr_metadata converts PR to metadata."""
        mock_github = MagicMock()
        mock_converter = MagicMock()

        repo = GitHubRepository(mock_github, mock_converter)

        mock_pr = MagicMock()
        mock_pr.number = 1
        mock_pr.title = "Test PR"
        mock_pr.merged = True

        closed_at = datetime(2023, 1, 1, 12, 0, 0)

        with patch.object(repo, '_extract_review_comments') as mock_extract:
            mock_extract.return_value = []

            metadata = repo._convert_to_pr_metadata(mock_pr, closed_at)

            assert metadata.number == 1
            assert metadata.title == "Test PR"
            assert metadata.is_merged is True
            assert metadata.closed_at == closed_at

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