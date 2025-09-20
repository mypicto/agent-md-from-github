"""
Tests for ReviewSummaryService.
"""

import unittest
from pathlib import Path
from unittest.mock import Mock
from scripts.src.application.services.review_summary_service import ReviewSummaryService
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.application.exceptions.pr_review_collection_error import PRReviewCollectionError


class TestReviewSummaryService(unittest.TestCase):
    """Test cases for ReviewSummaryService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.review_summary_repo = Mock()
        self.pr_metadata_repo = Mock()
        self.service = ReviewSummaryService(self.review_summary_repo, self.pr_metadata_repo)
    
    def test_set_summary_PRが存在する場合_保存される(self):
        # Arrange
        from scripts.src.domain.pull_request_metadata import PullRequestMetadata
        from scripts.src.domain.review_comment import ReviewComment
        from datetime import datetime
        
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        
        # Mock PR metadata
        pr_metadata = PullRequestMetadata(
            number=123,
            title="Test PR",
            closed_at=datetime(2023, 1, 1),
            is_merged=True,
            review_comments=[],
            repository_id=repo_id
        )
        
        self.pr_metadata_repo.find_by_pr_number.return_value = pr_metadata
        
        # Act
        output_directory = Path("workspace")
        self.service.set_summary(repo_id, 123, "high", "Test summary", output_directory)
        
        # Assert
        self.review_summary_repo.save.assert_called_once()
        saved_summary = self.review_summary_repo.save.call_args[0][0]
        assert saved_summary.repository_id == repo_id
        assert saved_summary.pr_number == 123
        assert saved_summary.priority == "high"
        assert saved_summary.summary == "Test summary"
    
    def test_set_summary_PRが存在しない場合_PRReviewCollectionErrorが発生する(self):
        # Arrange
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        self.pr_metadata_repo.find_by_pr_number.return_value = None  # No PRs found
        
        # Act & Assert
        with self.assertRaises(PRReviewCollectionError):
            output_directory = Path("workspace")
            self.service.set_summary(repo_id, 123, "high", "Test summary", output_directory)
    
    def test_set_summary_メタデータ取得エラーの場合_PRReviewCollectionErrorが発生する(self):
        # Arrange
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        self.pr_metadata_repo.find_by_pr_number.side_effect = Exception("Repository error")
        
        # Act & Assert
        with self.assertRaises(PRReviewCollectionError):
            output_directory = Path("workspace")
            self.service.set_summary(repo_id, 123, "high", "Test summary", output_directory)