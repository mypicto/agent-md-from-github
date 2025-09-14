"""
Tests for PullRequestFileSetRepository.
"""

import tempfile
from pathlib import Path
from scripts.src.infrastructure.repositories.pull_request_file_set_repository import PullRequestFileSetRepository
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestPullRequestFileSetRepository:
    """Test cases for PullRequestFileSetRepository."""

    def test_find_pull_request_file_sets_リポジトリが存在しない場合_空リストが返される(self):
        """Test find_pull_request_file_sets returns empty list when repository does not exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="nonexistent", name="repo")
            repository = PullRequestFileSetRepository()
            result = repository.find_pull_request_file_sets(output_directory, repo_id)
            assert result == []

    def test_find_pull_request_file_sets_コメントファイルが存在する場合_ファイルセットが返される(self):
        """Test find_pull_request_file_sets returns file sets when comment files exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            repo_dir = output_directory / repo_id.owner / repo_id.name / "2023-01-01"
            repo_dir.mkdir(parents=True, exist_ok=True)
            # Create comment file
            comment_file = repo_dir / "PR-123-comments.json"
            comment_file.touch()
            repository = PullRequestFileSetRepository()
            result = repository.find_pull_request_file_sets(output_directory, repo_id)
            assert len(result) == 1
            file_set = result[0]
            assert file_set.get_comments_file_path() == comment_file
            assert file_set.get_pr_directory() == repo_dir

    def test_find_pull_request_file_sets_複数のコメントファイルが存在する場合_全てのファイルセットが返される(self):
        """Test find_pull_request_file_sets returns all file sets when multiple comment files exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            repo_dir1 = output_directory / repo_id.owner / repo_id.name / "2023-01-01"
            repo_dir1.mkdir(parents=True, exist_ok=True)
            repo_dir2 = output_directory / repo_id.owner / repo_id.name / "2023-01-02"
            repo_dir2.mkdir(parents=True, exist_ok=True)
            # Create comment files
            comment_file1 = repo_dir1 / "PR-123-comments.json"
            comment_file1.touch()
            comment_file2 = repo_dir2 / "PR-456-comments.json"
            comment_file2.touch()
            repository = PullRequestFileSetRepository()
            result = repository.find_pull_request_file_sets(output_directory, repo_id)
            assert len(result) == 2
            pr_numbers = {fs._pr_number for fs in result}
            assert pr_numbers == {123, 456}