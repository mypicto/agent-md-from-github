"""
Tests for PullRequestFileSet.
"""

import tempfile
from datetime import datetime
from pathlib import Path
from scripts.src.infrastructure.pull_request_file_set import PullRequestFileSet
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.pull_request_basic_info import PullRequestBasicInfo
from scripts.src.domain.review_comment import ReviewComment


class TestPullRequestFileSet:
    """Test cases for PullRequestFileSet."""

    def test_get_pr_directory_正常取得_正しいディレクトリパスが返される(self):
        """Test get_pr_directory returns correct directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            expected_path = output_directory / "test_owner" / "test_repo" / "2023-01-01"
            assert resolver.get_pr_directory() == expected_path

    def test_get_comments_file_path_正常取得_正しいコメントファイルパスが返される(self):
        """Test get_comments_file_path returns correct file path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            expected_path = output_directory / "test_owner" / "test_repo" / "2023-01-01" / "PR-123-comments.json"
            assert resolver.get_comments_file_path() == expected_path

    def test_exists_file_ファイルが存在する場合_Trueが返される(self):
        """Test exists_file returns True when file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            # Create the comments file
            comments_file = resolver.get_comments_file_path()
            comments_file.parent.mkdir(parents=True, exist_ok=True)
            comments_file.touch()
            assert resolver.exists_file() is True

    def test_exists_file_ファイルが存在しない場合_Falseが返される(self):
        """Test exists_file returns False when file does not exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            # Do not create the file
            assert resolver.exists_file() is False

    def test_create_with_metadata_正常作成_インスタンスが生成される(self):
        """Test create_with_metadata creates instance correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_metadata = PullRequestMetadata(
                number=123,
                title="Test PR",
                closed_at=closed_at,
                is_merged=True,
                review_comments=[],
                repository_id=repo_id
            )
            resolver = PullRequestFileSet.create_with_metadata(output_directory, pr_metadata)
            expected_directory = output_directory / "test_owner" / "test_repo" / "2023-01-01"
            assert resolver.get_pr_directory() == expected_directory
            assert resolver.get_comments_file_path() == expected_directory / "PR-123-comments.json"

    def test_create_with_basic_info_正常作成_インスタンスが生成される(self):
        """Test create_with_basic_info creates instance correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            basic_info = PullRequestBasicInfo(
                number=123,
                title="Test PR",
                closed_at=closed_at,
                is_merged=True,
                repository_id=repo_id
            )
            resolver = PullRequestFileSet.create_with_basic_info(output_directory, basic_info)
            expected_directory = output_directory / "test_owner" / "test_repo" / "2023-01-01"
            assert resolver.get_pr_directory() == expected_directory
            assert resolver.get_comments_file_path() == expected_directory / "PR-123-comments.json"

    def test_get_summary_file_path_正常取得_正しいサマリーファイルパスが返される(self):
        """Test get_summary_file_path returns correct file path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            expected_path = output_directory / "test_owner" / "test_repo" / "2023-01-01" / "PR-123-summary.md"
            assert resolver.get_summary_file_path() == expected_path

    def test_exists_summary_ファイルが存在する場合_Trueが返される(self):
        """Test exists_summary returns True when file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            # Create the summary file
            summary_file = resolver.get_summary_file_path()
            summary_file.parent.mkdir(parents=True, exist_ok=True)
            summary_file.touch()
            assert resolver.exists_summary() is True

    def test_exists_summary_ファイルが存在しない場合_Falseが返される(self):
        """Test exists_summary returns False when file does not exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            closed_at = datetime(2023, 1, 1)
            pr_number = 123
            directory_path = output_directory / repo_id.owner / repo_id.name / closed_at.strftime("%Y-%m-%d")
            resolver = PullRequestFileSet(directory_path, pr_number)
            # Do not create the file
            assert resolver.exists_summary() is False

    def test_get_comments_pattern_正常取得_正しいパターンが返される(self):
        """Test get_comments_pattern returns correct pattern."""
        pattern = PullRequestFileSet.get_comments_pattern()
        assert pattern == "PR-*-comments.json"

    def test_create_from_comments_file_path_正常作成_インスタンスが生成される(self):
        """Test create_from_comments_file_path creates instance correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / "test_owner" / "test_repo" / "2023-01-01" / "PR-123-comments.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
            resolver = PullRequestFileSet.create_from_comments_file_path(file_path)
            assert resolver.get_pr_directory() == file_path.parent
            assert resolver.get_comments_file_path() == file_path
            assert resolver.get_summary_file_path() == file_path.parent / "PR-123-summary.md"

    def test_create_from_comments_file_path_無効なファイル名_ValueErrorが発生(self):
        """Test create_from_comments_file_path raises ValueError for invalid filename."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / "invalid-file.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
            try:
                PullRequestFileSet.create_from_comments_file_path(file_path)
                assert False, "ValueError should be raised"
            except ValueError as e:
                assert "Invalid filename format" in str(e)