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

    def test_exists_summary_要約ファイル存在_ファイルが存在する(self, repo, temp_dir, sample_metadata):
        """Test exists_summary returns True when file exists."""
        # Create the summary file
        summary_path = temp_dir / "summaries" / "PR-123.yml"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.touch()

        assert repo.exists_summary(sample_metadata, temp_dir) is True

    def test_exists_summary_要約ファイル不存在_ファイルが存在しない(self, repo, temp_dir, sample_metadata):
        """Test exists_summary returns False when file does not exist."""
        assert repo.exists_summary(sample_metadata, temp_dir) is False

    def test_save_ファイル作成_ファイルが作成される(self, repo, temp_dir, sample_summary):
        """Test save creates the summary file with correct content."""
        repo.save(sample_summary)

        summary_path = temp_dir / "summaries" / "PR-123.yml"
        assert summary_path.exists()

        # Check content
        from ruamel.yaml import YAML
        yaml = YAML()
        with open(summary_path, 'r') as f:
            data = yaml.load(f)

        assert data["repository_id"]["owner"] == "test-owner"
        assert data["repository_id"]["name"] == "test-repo"
        assert data["pr_number"] == 123
        assert data["priority"] == "high"
        assert data["summary"] == "Test summary content"

    def test_get_既存要約_要約が返される(self, repo, temp_dir, sample_summary):
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

    def test_get_不存在要約_Noneが返される(self, repo, sample_summary):
        """Test get returns None when file does not exist."""
        retrieved = repo.get(sample_summary.repository_id, sample_summary.pr_number)
        assert retrieved is None

    def test_save_特殊文字要約_リテラルブロックが使用される(self, repo, temp_dir):
        """Test that summary with special characters is saved in literal block format without quotes."""
        # Create summary with special characters that would normally trigger quotes
        summary_with_special_chars = ReviewSummary(
            repository_id=RepositoryIdentifier(owner="test-owner", name="test-repo"),
            pr_number=456,
            priority="high",
            summary="- **Category:** 設計\n  **What:** UseCaseでの入力バリデーションをJakarta Validatorに置き換え、`Validator`注入と`validate(param)`メソッドで制約違反を検出している。\n  **Why:** 入力制約をアノテーションで宣言することでバリデーションロジックを分離し一貫性を持たせ。"
        )
        
        repo.save(summary_with_special_chars)
        
        summary_path = temp_dir / "summaries" / "PR-456.yml"
        assert summary_path.exists()
        
        # Read the raw YAML content to check format
        with open(summary_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        # Check that summary field uses literal block format (starts with '"summary": |-')
        assert '"summary": |-' in yaml_content
        # Check that summary content is not quoted (no quotes around the multiline content)
        assert '"- **Category:**' not in yaml_content
        # Ensure the content preserves newlines and formatting
        assert '**Category:** 設計' in yaml_content
        assert '**What:** UseCaseでの入力バリデーション' in yaml_content