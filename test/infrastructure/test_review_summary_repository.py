"""
Tests for ReviewSummaryRepository.
"""

import yaml
import tempfile
from pathlib import Path
import pytest
from scripts.src.domain.review_summary import ReviewSummary
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.infrastructure.repositories.review_summary_repository import ReviewSummaryRepository


class TestReviewSummaryRepository:
    """Test cases for ReviewSummaryRepository."""
    
    def test_save_保存が成功する(self):
        """Test that save creates the correct JSON file."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = ReviewSummaryRepository(base_directory=temp_dir)
            repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
            summary = ReviewSummary(
                repository_id=repo_id,
                pr_number=123,
                priority="high",
                summary="Test summary"
            )
            
            # Act
            repo.save(summary)
            
            # Assert
            expected_path = Path(temp_dir) / "testowner" / "testrepo" / "summaries" / "PR-123.yml"
            assert expected_path.exists()
            
            with open(expected_path, 'r') as f:
                data = yaml.safe_load(f)
            
            assert data["repository_id"]["owner"] == "testowner"
            assert data["pr_number"] == 123
            assert data["priority"] == "high"
            assert data["summary"] == "Test summary"
    
    def test_get_存在する場合_ReviewSummaryが返される(self):
        """Test that get returns ReviewSummary when file exists."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = ReviewSummaryRepository(base_directory=temp_dir)
            repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
            
            # Create file manually
            summaries_dir = Path(temp_dir) / "testowner" / "testrepo" / "summaries"
            summaries_dir.mkdir(parents=True)
            file_path = summaries_dir / "PR-123.yml"
            data = {
                "repository_id": {"owner": "testowner", "name": "testrepo"},
                "pr_number": 123,
                "priority": "high",
                "summary": "Test summary"
            }
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            # Act
            result = repo.get(repo_id, 123)
            
            # Assert
            assert result is not None
            assert result.repository_id == repo_id
            assert result.pr_number == 123
            assert result.priority == "high"
            assert result.summary == "Test summary"
    
    def test_get_存在しない場合_Noneが返される(self):
        """Test that get returns None when file does not exist."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = ReviewSummaryRepository(base_directory=temp_dir)
            repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
            
            # Act
            result = repo.get(repo_id, 123)
            
            # Assert
            assert result is None