"""
Tests for MissingSummariesService.
"""

import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from scripts.src.application.services.missing_summaries_service import MissingSummariesService
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_comment import ReviewComment


class TestMissingSummariesService(unittest.TestCase):
    """Test cases for MissingSummariesService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pr_metadata_repo = Mock()
        self.summary_repo = Mock()
        
        self.service = MissingSummariesService(
            pr_metadata_repository=self.pr_metadata_repo,
            summary_repository=self.summary_repo
        )
        
        # Create test data
        self.repo_id = RepositoryIdentifier.from_string("owner/repo")
        self.output_dir = Path("/tmp/test")
        
        self.metadata1 = PullRequestMetadata(
            number=123,
            title="Test PR 1",
            closed_at=datetime(2025, 9, 1),
            is_merged=True,
            review_comments=[ReviewComment(
                comment_id=1,
                file_path="file1.py",
                position=1,
                commit_id="abc123",
                author="user1",
                created_at=datetime(2025, 9, 1),
                body="comment1",
                diff_context="diff1"
            )],  # 1 comment
            repository_id=self.repo_id
        )
        
        self.metadata2 = PullRequestMetadata(
            number=456,
            title="Test PR 2",
            closed_at=datetime(2025, 9, 2),
            is_merged=False,
            review_comments=[ReviewComment(
                comment_id=2,
                file_path="file2.py",
                position=2,
                commit_id="def456",
                author="user2",
                created_at=datetime(2025, 9, 2),
                body="comment2",
                diff_context="diff2"
            ), ReviewComment(
                comment_id=3,
                file_path="file3.py",
                position=3,
                commit_id="ghi789",
                author="user3",
                created_at=datetime(2025, 9, 2),
                body="comment3",
                diff_context="diff3"
            )],  # 2 comments
            repository_id=self.repo_id
        )
        
        self.metadata_no_comments = PullRequestMetadata(
            number=789,
            title="Test PR No Comments",
            closed_at=datetime(2025, 9, 3),
            is_merged=True,
            review_comments=[],  # No comments
            repository_id=self.repo_id
        )
    
    def test_list_missing_summaries_メタデータなし_空リストが返される(self):
        """Test listing missing summaries when no metadata exists."""
        self.pr_metadata_repo.find_all_by_repository.return_value = []
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [])
        self.pr_metadata_repo.find_all_by_repository.assert_called_once_with(self.output_dir, self.repo_id)
    
    def test_list_missing_summaries_すべて要約あり_空リストが返される(self):
        """Test listing missing summaries when all have summaries."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]
        self.summary_repo.exists_summary.return_value = True
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)
    
    def test_list_missing_summaries_一部欠落_欠落PRが返される(self):
        """Test listing missing summaries when some are missing."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]
        
        def exists_summary_side_effect(metadata, output_dir):
            return metadata.number == 123  # Only PR 123 has summary
        
        self.summary_repo.exists_summary.side_effect = exists_summary_side_effect
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [456])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)
    
    def test_list_missing_summaries_すべて欠落_すべてPRが返される(self):
        """Test listing missing summaries when all are missing."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]
        self.summary_repo.exists_summary.return_value = False
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [456, 123])  # Sorted by comment count desc
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)
    
    def test_list_missing_summaries_レビューコメントゼロ除外(self):
        """Test that PRs with no review comments are filtered out."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata_no_comments, self.metadata1]
        self.summary_repo.exists_summary.return_value = False  # Both missing summaries
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        # Should filter out metadata_no_comments (0 comments), keep metadata1 (1 comment)
        self.assertEqual(result, [123])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 1)  # Only called for filtered metadata
    
    def test_list_missing_summaries_レビューコメント件数降順ソート(self):
        """Test that results are sorted by review comment count in descending order."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]  # 1 and 2 comments
        self.summary_repo.exists_summary.return_value = False  # Both missing summaries
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        # Should sort by comment count desc: metadata2 (2 comments), metadata1 (1 comment)
        self.assertEqual(result, [456, 123])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)