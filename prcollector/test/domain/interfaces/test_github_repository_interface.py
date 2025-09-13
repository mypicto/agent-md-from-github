"""
Tests for GitHubRepositoryInterface.
"""

from prcollector.src.domain.interfaces.github_repository_interface import GitHubRepositoryInterface


class TestGitHubRepositoryInterface:
    """Test cases for GitHubRepositoryInterface."""

    def test_interface_定義_プロトコルとして定義されている(self):
        """Test that GitHubRepositoryInterface is defined as a protocol."""
        assert hasattr(GitHubRepositoryInterface, 'find_closed_prs_basic_info')
        assert hasattr(GitHubRepositoryInterface, 'get_full_pr_metadata')