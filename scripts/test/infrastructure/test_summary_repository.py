"""
Unit tests for SummaryRepository.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_summary import ReviewSummary
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.infrastructure.repositories.summary_repository import SummaryRepository


class TestSummaryRepository:
    """Test cases for SummaryRepository."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp:
            yield Path(temp)

    @pytest.fixture
    def repo(self, temp_dir):
        """Create a SummaryRepository instance."""
        return SummaryRepository(base_directory=str(temp_dir))

    @pytest.fixture
    def sample_metadata(self):
        """Create sample PR metadata."""
        return PullRequestMetadata(
            number=123,
            title="Test PR",
            repository_id=RepositoryIdentifier(owner="test-owner", name="test-repo"),
            closed_at=None,
            is_merged=True,
            review_comments=[]
        )

    @pytest.fixture
    def sample_summary(self):
        """Create sample review summary."""
        return ReviewSummary(
            repository_id=RepositoryIdentifier(owner="test-owner", name="test-repo"),
            pr_number=123,
            priority="high",
            summary="Test summary content"
        )

    def test_exists_summary_file_exists(self, repo, temp_dir, sample_metadata):
        """Test exists_summary returns True when file exists."""
        # Create the summary file
        summary_path = temp_dir / "test-owner" / "test-repo" / "summaries" / "PR-123.yml"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.touch()

        assert repo.exists_summary(sample_metadata, temp_dir) is True

    def test_exists_summary_file_not_exists(self, repo, temp_dir, sample_metadata):
        """Test exists_summary returns False when file does not exist."""
        assert repo.exists_summary(sample_metadata, temp_dir) is False

    def test_save_creates_file(self, repo, temp_dir, sample_summary):
        """Test save creates the summary file with correct content."""
        repo.save(sample_summary)

        summary_path = temp_dir / "test-owner" / "test-repo" / "summaries" / "PR-123.yml"
        assert summary_path.exists()

        # Check content
        import yaml
        with open(summary_path, 'r') as f:
            data = yaml.safe_load(f)

        assert data["repository_id"]["owner"] == "test-owner"
        assert data["repository_id"]["name"] == "test-repo"
        assert data["pr_number"] == 123
        assert data["priority"] == "high"
        assert data["summary"] == "Test summary content"

    def test_get_existing_summary(self, repo, temp_dir, sample_summary):
        """Test get returns the summary when file exists."""
        # First save the summary
        repo.save(sample_summary)

        # Then retrieve it
        retrieved = repo.get(sample_summary.repository_id, sample_summary.pr_number)

        assert retrieved is not None
        assert retrieved.repository_id == sample_summary.repository_id
        assert retrieved.pr_number == sample_summary.pr_number
        assert retrieved.priority == sample_summary.priority
        assert retrieved.summary == sample_summary.summary

    def test_get_non_existing_summary(self, repo, sample_summary):
        """Test get returns None when file does not exist."""
        retrieved = repo.get(sample_summary.repository_id, sample_summary.pr_number)
        assert retrieved is None