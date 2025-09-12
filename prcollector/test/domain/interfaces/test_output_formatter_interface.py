"""
Tests for OutputFormatterInterface.
"""

import pytest
from prcollector.src.domain.interfaces.output_formatter_interface import OutputFormatterInterface


class TestOutputFormatterInterface:
    """Test cases for OutputFormatterInterface."""

    def test_interface_定義_プロトコルとして定義されている(self):
        """Test that OutputFormatterInterface is defined as a protocol."""
        assert hasattr(OutputFormatterInterface, 'format_comments')
        assert hasattr(OutputFormatterInterface, 'format_diff_excerpt')