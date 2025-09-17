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
        self.output_formatter = Mock()
        self.output_writer = Mock()
        self.comment_filter = AICommentFilter()
        
        self.service = PRReviewCollectionService(
            github_repository=self.github_repo,
            output_formatter=self.output_formatter,
            output_writer=self.output_writer,
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
    
    def test_process_single_pr_filters_comments(self):
        """Test that _process_single_pr filters comments before formatting."""
        # Mock the formatter and writer
        self.output_formatter.format_comments.return_value = '{"test": "data"}'
        self.output_formatter.format_diff_excerpt.return_value = "# Test diff"
        self.output_writer.write_pr_data.return_value = None
        
        # Process the PR
        result = self.service._process_single_pr(self.pr_metadata, self.output_dir)
        
        # Verify the result
        self.assertTrue(result)
        
        # Verify that formatter was called with filtered metadata
        self.assertEqual(self.output_formatter.format_comments.call_count, 1)
        self.assertEqual(self.output_formatter.format_diff_excerpt.call_count, 1)
        
        # Get the filtered metadata passed to formatter
        filtered_metadata = self.output_formatter.format_comments.call_args[0][0]
        
        # Verify that only human comment remains
        self.assertEqual(len(filtered_metadata.review_comments), 1)
        self.assertEqual(filtered_metadata.review_comments[0].author, "human")
        
        # Verify writer was called with filtered metadata
        self.assertEqual(self.output_writer.write_pr_data.call_count, 1)
        writer_metadata = self.output_writer.write_pr_data.call_args[0][0]
        self.assertEqual(len(writer_metadata.review_comments), 1)


if __name__ == "__main__":
    unittest.main()