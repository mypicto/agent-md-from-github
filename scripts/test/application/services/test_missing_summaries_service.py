"""
Tests for MissingSummariesService.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock
from scripts.src.application.services.missing_summaries_service import MissingSummariesService
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.infrastructure.pull_request_file_set import PullRequestFileSet


class TestMissingSummariesService:
    """Test cases for MissingSummariesService."""

    def test_list_missing_summaries_サマリファイルが存在する場合_空リストが返される(self):
        """Test list_missing_summaries returns empty list when summary files exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            # Mock repository
            mock_repo = Mock()
            directory_path = output_directory / "test_owner" / "test_repo" / "2023-01-01"
            file_set = PullRequestFileSet(directory_path, 123)
            # Create summary file
            summary_file = file_set.get_summary_file_path()
            summary_file.parent.mkdir(parents=True, exist_ok=True)
            summary_file.touch()
            mock_repo.find_pull_request_file_sets.return_value = [file_set]
            service = MissingSummariesService(mock_repo)
            result = service.list_missing_summaries(repo_id, output_directory)
            assert result == []

    def test_list_missing_summaries_サマリファイルが存在しない場合_コメントファイルパスが返される(self):
        """Test list_missing_summaries returns comment file paths when summary files do not exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            # Mock repository
            mock_repo = Mock()
            directory_path = output_directory / "test_owner" / "test_repo" / "2023-01-01"
            file_set = PullRequestFileSet(directory_path, 123)
            mock_repo.find_pull_request_file_sets.return_value = [file_set]
            service = MissingSummariesService(mock_repo)
            result = service.list_missing_summaries(repo_id, output_directory)
            expected = [file_set.get_comments_file_path()]
            assert result == expected

    def test_list_missing_summaries_複数のファイルセットがある場合_欠如のみが返される(self):
        """Test list_missing_summaries returns only missing summaries when multiple file sets exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            # Mock repository
            mock_repo = Mock()
            directory_path1 = output_directory / "test_owner" / "test_repo" / "2023-01-01"
            file_set1 = PullRequestFileSet(directory_path1, 123)
            # Create summary for file_set1
            summary_file1 = file_set1.get_summary_file_path()
            summary_file1.parent.mkdir(parents=True, exist_ok=True)
            summary_file1.touch()
            directory_path2 = output_directory / "test_owner" / "test_repo" / "2023-01-02"
            file_set2 = PullRequestFileSet(directory_path2, 456)
            # Do not create summary for file_set2
            mock_repo.find_pull_request_file_sets.return_value = [file_set1, file_set2]
            service = MissingSummariesService(mock_repo)
            result = service.list_missing_summaries(repo_id, output_directory)
            expected = [file_set2.get_comments_file_path()]
            assert result == expected