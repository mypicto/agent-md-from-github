"""
Test for ReviewSummary value object.
"""

import pytest
from scripts.src.domain.review_summary import ReviewSummary
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestReviewSummary:
    """Test cases for ReviewSummary."""

    def test_ReviewSummary_インスタンス化_属性が正しく設定される(self):
        # Arrange
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        
        # Act
        summary = ReviewSummary(
            repository_id=repo_id,
            pr_number=123,
            priority="high",
            summary="Test summary"
        )
        
        # Assert
        assert summary.repository_id == repo_id
        assert summary.pr_number == 123
        assert summary.priority == "high"
        assert summary.summary == "Test summary"
    
    def test_ReviewSummary_バリデーション_pr_numberが0以下の場合_ValueErrorが発生する(self):
        # Arrange
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        
        # Act & Assert
        with pytest.raises(ValueError, match="PR number must be positive"):
            ReviewSummary(
                repository_id=repo_id,
                pr_number=0,
                priority="high",
                summary="Test summary"
            )
    
    def test_ReviewSummary_バリデーション_priorityが無効な場合_ValueErrorが発生する(self):
        # Arrange
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Priority must be"):
            ReviewSummary(
                repository_id=repo_id,
                pr_number=123,
                priority="invalid",
                summary="Test summary"
            )
    
    def test_ReviewSummary_バリデーション_summaryが空の場合_ValueErrorが発生する(self):
        # Arrange
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Summary must not be empty"):
            ReviewSummary(
                repository_id=repo_id,
                pr_number=123,
                priority="high",
                summary=""
            )