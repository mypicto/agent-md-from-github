"""
Tests for OutputWriterInterface.
"""

import pytest
from prcollector.src.domain.interfaces.output_writer_interface import OutputWriterInterface


class TestOutputWriterInterface:
    """Test cases for OutputWriterInterface."""

    def test_interface_定義_プロトコルとして定義されている(self):
        """Test that OutputWriterInterface is defined as a protocol."""
        # This is a protocol/interface, so we mainly test that it exists
        assert hasattr(OutputWriterInterface, 'write_pr_data')
        assert hasattr(OutputWriterInterface, 'file_exists')