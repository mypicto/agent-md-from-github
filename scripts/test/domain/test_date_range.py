"""
Tests for DateRange.
"""

import pytest
from datetime import datetime
from scripts.src.domain.date_range import DateRange


class TestDateRange:
    """Test cases for DateRange."""

    def test___post_init___有効な日付範囲_正常に初期化される(self):
        """Test __post_init__ validates correctly for valid date range."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 2)
        date_range = DateRange(start_date=start, end_date=end)
        assert date_range.start_date == start
        assert date_range.end_date == end

    def test___post_init___無効な日付範囲_ValueErrorが発生する(self):
        """Test __post_init__ raises ValueError for invalid date range."""
        start = datetime(2023, 1, 2)
        end = datetime(2023, 1, 1)
        with pytest.raises(ValueError):
            DateRange(start_date=start, end_date=end)

    def test_contains_範囲内の日付_Trueが返される(self):
        """Test contains returns True for date within range."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 3)
        date_range = DateRange(start_date=start, end_date=end)
        target = datetime(2023, 1, 2)
        assert date_range.contains(target) is True

    def test_contains_範囲外の日付_Falseが返される(self):
        """Test contains returns False for date outside range."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 3)
        date_range = DateRange(start_date=start, end_date=end)
        target = datetime(2023, 1, 4)
        assert date_range.contains(target) is False