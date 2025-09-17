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
            review_comments=[],
            repository_id=self.repo_id
        )
        
        self.metadata2 = PullRequestMetadata(
            number=456,
            title="Test PR 2",
            closed_at=datetime(2025, 9, 2),
            is_merged=False,
            review_comments=[],
            repository_id=self.repo_id
        )
    
    def test_list_missing_summaries_no_metadata(self):
        """Test listing missing summaries when no metadata exists."""
        self.pr_metadata_repo.find_all_by_repository.return_value = []
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [])
        self.pr_metadata_repo.find_all_by_repository.assert_called_once_with(self.output_dir, self.repo_id)
    
    def test_list_missing_summaries_all_have_summaries(self):
        """Test listing missing summaries when all have summaries."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]
        self.summary_repo.exists_summary.return_value = True
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)
    
    def test_list_missing_summaries_some_missing(self):
        """Test listing missing summaries when some are missing."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]
        
        def exists_summary_side_effect(metadata, output_dir):
            return metadata.number == 123  # Only PR 123 has summary
        
        self.summary_repo.exists_summary.side_effect = exists_summary_side_effect
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [456])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)
    
    def test_list_missing_summaries_all_missing(self):
        """Test listing missing summaries when all are missing."""
        self.pr_metadata_repo.find_all_by_repository.return_value = [self.metadata1, self.metadata2]
        self.summary_repo.exists_summary.return_value = False
        
        result = self.service.list_missing_summaries(self.repo_id, self.output_dir)
        
        self.assertEqual(result, [123, 456])
        self.assertEqual(self.summary_repo.exists_summary.call_count, 2)