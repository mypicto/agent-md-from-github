"""
Tests for PRReviewCollectionService.
"""

import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.src.application.services.pr_review_collection_service import PRReviewCollectionService
from scripts.src.domain.date_range import DateRange
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_comment import ReviewComment
from scripts.src.infrastructure.filters.ai_comment_filter import AICommentFilter


class TestPRReviewCollectionService(unittest.TestCase):
    """Test cases for PRReviewCollectionService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.github_repo = Mock()
        self.pr_metadata_repo = Mock()
        self.comment_filter = AICommentFilter()
        
        self.service = PRReviewCollectionService(
            github_repository=self.github_repo,
            pr_metadata_repository=self.pr_metadata_repo,
            comment_filter=self.comment_filter
        )
        
        # Create test data
        self.repo_id = RepositoryIdentifier.from_string("owner/repo")
        self.date_range = DateRange(
            start_date=datetime(2025, 9, 1),
            end_date=datetime(2025, 9, 15)
        )
        self.output_dir = Path("/tmp/test")
        
        self.copilot_comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=1,
            commit_id="abc123",
            author="Copilot",
            created_at=datetime(2025, 9, 15),
            body="Copilot comment",
            diff_context="diff"
        )
        
        self.human_comment = ReviewComment(
            comment_id=2,
            file_path="test.py",
            position=2,
            commit_id="def456",
            author="human",
            created_at=datetime(2025, 9, 15),
            body="Human comment",
            diff_context="diff"
        )
        
        self.pr_metadata = PullRequestMetadata(
            number=123,
            title="Test PR",
            closed_at=datetime(2025, 9, 15),
            is_merged=True,
            review_comments=[self.copilot_comment, self.human_comment],
            repository_id=self.repo_id
        )


if __name__ == "__main__":
    unittest.main()