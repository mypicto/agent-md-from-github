"""
Tests for TimezoneConverterInterface.
"""

import pytest
from prcollector.src.domain.interfaces.timezone_converter_interface import TimezoneConverterInterface


class TestTimezoneConverterInterface:
    """Test cases for TimezoneConverterInterface."""

    def test_interface_定義_プロトコルとして定義されている(self):
        """Test that TimezoneConverterInterface is defined as a protocol."""
        assert hasattr(TimezoneConverterInterface, 'convert_to_target_timezone')
        assert hasattr(TimezoneConverterInterface, 'localize_date_range')