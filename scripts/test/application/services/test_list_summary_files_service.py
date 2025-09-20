"""
Tests for ListSummaryFilesService.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from scripts.src.application.services.list_summary_files_service import ListSummaryFilesService
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_summary import ReviewSummary
from scripts.src.infrastructure.repositories.summary_repository import SummaryRepository


class TestListSummaryFilesService:
    """Test cases for ListSummaryFilesService."""

    @pytest.fixture
    def mock_summary_repository(self):
        """Create a mock summary repository."""
        return Mock(spec=SummaryRepository)

    @pytest.fixture
    def service(self, mock_summary_repository):
        """Create the service with mock repository."""
        return ListSummaryFilesService(mock_summary_repository)

    @pytest.fixture
    def repo_id(self):
        """Create a test repository identifier."""
        return RepositoryIdentifier(owner="test-owner", name="test-repo")

    @pytest.fixture
    def sample_summaries(self, repo_id):
        """Create sample review summaries."""
        return [
            ReviewSummary(
                repository_id=repo_id,
                pr_number=1,
                priority="high",
                summary="High priority summary"
            ),
            ReviewSummary(
                repository_id=repo_id,
                pr_number=2,
                priority="middle",
                summary="Middle priority summary"
            ),
            ReviewSummary(
                repository_id=repo_id,
                pr_number=3,
                priority="low",
                summary="Low priority summary"
            )
        ]

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.glob")
    def test_list_summary_files_優先度フィルタあり_一致するファイルのみを返す(self, mock_glob, mock_exists, service, repo_id, sample_summaries):
        """Test listing summary files with priority filter."""
        # Setup mocks
        mock_exists.return_value = True
        mock_glob.return_value = [
            Path("pullrequests/test-owner/test-repo/summaries/PR-1.yml"),
            Path("pullrequests/test-owner/test-repo/summaries/PR-2.yml"),
            Path("pullrequests/test-owner/test-repo/summaries/PR-3.yml")
        ]

        # Configure repository mock
        service._summary_repository.get.side_effect = sample_summaries

        # Test filtering by high priority
        result = service.list_summary_files(repo_id, ["high"])

        assert len(result) == 1
        assert "PR-1.yml" in result[0]
        service._summary_repository.get.assert_any_call(repo_id, 1)

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.glob")
    def test_list_summary_files_優先度フィルタなし_全てのファイルを返す(self, mock_glob, mock_exists, service, repo_id, sample_summaries):
        """Test listing summary files without priority filter."""
        # Setup mocks
        mock_exists.return_value = True
        mock_glob.return_value = [
            Path("pullrequests/test-owner/test-repo/summaries/PR-1.yml"),
            Path("pullrequests/test-owner/test-repo/summaries/PR-2.yml"),
            Path("pullrequests/test-owner/test-repo/summaries/PR-3.yml")
        ]

        # Configure repository mock
        service._summary_repository.get.side_effect = sample_summaries

        # Test without priority filter (should return all)
        result = service.list_summary_files(repo_id, [])

        assert len(result) == 3
        assert all("PR-" in path for path in result)

    @patch("pathlib.Path.exists")
    def test_list_summary_files_ディレクトリなし_空のリストを返す(self, mock_exists, service, repo_id):
        """Test listing summary files when directory doesn't exist."""
        mock_exists.return_value = False

        result = service.list_summary_files(repo_id, [])

        assert result == []

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.glob")
    def test_list_summary_files_無効なファイル名_無視して処理する(self, mock_glob, mock_exists, service, repo_id):
        """Test handling of invalid filename formats."""
        # Setup mocks
        mock_exists.return_value = True
        mock_glob.return_value = [
            Path("pullrequests/test-owner/test-repo/summaries/invalid.yml"),
            Path("pullrequests/test-owner/test-repo/summaries/PR-1.yml")
        ]

        # Configure repository mock
        service._summary_repository.get.return_value = None

        result = service.list_summary_files(repo_id, [])

        # Should skip invalid files and files that can't be loaded
        assert len(result) == 0

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.glob")
    def test_list_summary_files_リポジトリがNoneを返す_ファイルをスキップする(self, mock_glob, mock_exists, service, repo_id):
        """Test when repository returns None for a summary."""
        # Setup mocks
        mock_exists.return_value = True
        mock_glob.return_value = [
            Path("pullrequests/test-owner/test-repo/summaries/PR-1.yml")
        ]

        # Configure repository mock to return None
        service._summary_repository.get.return_value = None

        result = service.list_summary_files(repo_id, [])

        assert len(result) == 0