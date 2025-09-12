"""
Tests for GitHubRepositoryInterface.
"""

import pytest
from prcollector.src.domain.interfaces.github_repository_interface import GitHubRepositoryInterface


class TestGitHubRepositoryInterface:
    """Test cases for GitHubRepositoryInterface."""

    def test_interface_定義_プロトコルとして定義されている(self):
        """Test that GitHubRepositoryInterface is defined as a protocol."""
        assert hasattr(GitHubRepositoryInterface, 'find_closed_pull_requests_in_range')