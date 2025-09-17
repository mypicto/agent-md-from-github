"""
Tests for PRReviewCollectionService.
"""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
from scripts.src.application.services.pr_review_collection_service import PRReviewCollectionService
from scripts.src.domain.date_range import DateRange
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.pull_request_basic_info import PullRequestBasicInfo
from scripts.src.domain.review_comment import ReviewComment


class TestPRReviewCollectionService:
    """Test cases for PRReviewCollectionService."""

    def test___init___初期化_サービスが正しく初期化される(self):
        """Test __init__ initializes the service correctly."""
        mock_github = MagicMock()
        mock_formatter = MagicMock()
        mock_writer = MagicMock()
        mock_filter = MagicMock()

        service = PRReviewCollectionService(
            github_repository=mock_github,
            output_formatter=mock_formatter,
            output_writer=mock_writer,
            comment_filter=mock_filter
        )

        assert service._github_repository == mock_github
        assert service._output_formatter == mock_formatter
        assert service._output_writer == mock_writer
        assert service._comment_filter == mock_filter

    def test_collect_review_comments_正常実行_レビューコメントが収集される(self):
        """Test collect_review_comments executes successfully."""
        mock_github = MagicMock()
        mock_formatter = MagicMock()
        mock_writer = MagicMock()
        mock_filter = MagicMock()

        service = PRReviewCollectionService(
            github_repository=mock_github,
            output_formatter=mock_formatter,
            output_writer=mock_writer,
            comment_filter=mock_filter
        )

        repo_id = RepositoryIdentifier(owner="test", name="repo")
        date_range = DateRange(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2)
        )
        output_dir = Path("test_dir")

        # Mock PR metadata with comments
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=1,
            commit_id="abc",
            author="user",
            created_at=datetime.now(),
            body="comment",
            diff_context="diff"
        )
        pr_metadata = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime.now(),
            is_merged=True,
            review_comments=[comment],
            repository_id=repo_id
        )

        # Mock basic info
        basic_info = PullRequestBasicInfo(
            number=1,
            title="Test PR",
            closed_at=datetime.now(),
            is_merged=True,
            repository_id=repo_id
        )

        mock_github.find_closed_prs_basic_info.return_value = [basic_info]
        mock_github.get_full_pr_metadata.return_value = pr_metadata
        mock_writer.exists_file_from_basic_info.return_value = False  # File doesn't exist
        mock_writer.exists_file.return_value = False  # For _process_single_pr
        mock_formatter.format_comments.return_value = "comments"
        mock_formatter.format_diff_excerpt.return_value = "diff"

        service.collect_review_comments(repo_id, date_range, output_dir)

        mock_github.find_closed_prs_basic_info.assert_called_once_with(repo_id, date_range)
        mock_github.get_full_pr_metadata.assert_called_once_with(1, repo_id)
        mock_writer.write_pr_data.assert_called_once()

    def test_collect_review_comments_例外発生_PRReviewCollectionErrorが発生する(self):
        """Test collect_review_comments raises PRReviewCollectionError on exception."""
        mock_github = MagicMock()
        mock_formatter = MagicMock()
        mock_writer = MagicMock()
        mock_filter = MagicMock()

        service = PRReviewCollectionService(
            github_repository=mock_github,
            output_formatter=mock_formatter,
            output_writer=mock_writer,
            comment_filter=mock_filter
        )

        repo_id = RepositoryIdentifier(owner="test", name="repo")
        date_range = DateRange(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2)
        )
        output_dir = Path("test_dir")

        mock_github.find_closed_prs_basic_info.side_effect = Exception("Test error")

        from scripts.src.application.exceptions.pr_review_collection_error import PRReviewCollectionError
        with pytest.raises(PRReviewCollectionError):
            service.collect_review_comments(repo_id, date_range, output_dir)

    def test__process_single_pr_正常処理_Trueが返される(self):
        """Test _process_single_pr returns True on successful processing."""
        mock_github = MagicMock()
        mock_formatter = MagicMock()
        mock_writer = MagicMock()
        mock_filter = MagicMock()

        service = PRReviewCollectionService(
            github_repository=mock_github,
            output_formatter=mock_formatter,
            output_writer=mock_writer,
            comment_filter=mock_filter
        )

        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=1,
            commit_id="abc",
            author="user",
            created_at=datetime.now(),
            body="comment",
            diff_context="diff"
        )
        repo_id = RepositoryIdentifier(owner="test", name="repo")
        pr_metadata = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime.now(),
            is_merged=True,
            review_comments=[comment],
            repository_id=repo_id
        )
        output_dir = Path("test_dir")

        mock_formatter.format_comments.return_value = "comments"
        mock_formatter.format_diff_excerpt.return_value = "diff"

        result = service._process_single_pr(pr_metadata, output_dir)
        assert result is True