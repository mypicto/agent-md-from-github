"""
Tests for PriorityFilter.
"""

import pytest

from scripts.src.domain.priority_filter import PriorityFilter
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_summary import ReviewSummary


class TestPriorityFilter:
    """Test cases for PriorityFilter."""

    @pytest.fixture
    def sample_summaries(self):
        """Create sample review summaries for testing."""
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        return [
            ReviewSummary(
                repository_id=repo_id,
                pr_number=1,
                priority="high",
                summary="High priority summary"
            ),
            ReviewSummary(
                repository_id=repo_id,
                pr_number=2,
                priority="middle",
                summary="Middle priority summary"
            ),
            ReviewSummary(
                repository_id=repo_id,
                pr_number=3,
                priority="low",
                summary="Low priority summary"
            ),
            ReviewSummary(
                repository_id=repo_id,
                pr_number=4,
                priority="high",
                summary="Another high priority summary"
            )
        ]

    def test_filter_by_priorities_高優先度のみ_高優先度のサマリーのみを返す(self, sample_summaries):
        """Test filtering by high priority only."""
        result = PriorityFilter.filter_by_priorities(sample_summaries, ["high"])
        assert len(result) == 2
        assert all(summary.priority == "high" for summary in result)
        assert result[0].pr_number == 1
        assert result[1].pr_number == 4

    def test_filter_by_priorities_複数優先度_指定された優先度のサマリーを返す(self, sample_summaries):
        """Test filtering by multiple priorities."""
        result = PriorityFilter.filter_by_priorities(sample_summaries, ["high", "low"])
        assert len(result) == 3
        priorities = [summary.priority for summary in result]
        assert "high" in priorities
        assert "low" in priorities
        assert "middle" not in priorities

    def test_filter_by_priorities_優先度未指定_全てのサマリーを返す(self, sample_summaries):
        """Test filtering with empty priority list returns all summaries."""
        result = PriorityFilter.filter_by_priorities(sample_summaries, [])
        assert len(result) == 4
        assert result == sample_summaries

    def test_filter_by_priorities_一致なし_空のリストを返す(self, sample_summaries):
        """Test filtering with priorities that don't exist."""
        result = PriorityFilter.filter_by_priorities(sample_summaries, ["nonexistent"])
        assert len(result) == 0

    def test_filter_by_priorities_空の入力_空のリストを返す(self):
        """Test filtering with empty input list."""
        result = PriorityFilter.filter_by_priorities([], ["high"])
        assert len(result) == 0