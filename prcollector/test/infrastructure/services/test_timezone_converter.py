"""
Tests for TimezoneConverter.
"""

from datetime import datetime
import pytz
from prcollector.src.infrastructure.services.timezone_converter import TimezoneConverter


class TestTimezoneConverter:
    """Test cases for TimezoneConverter."""

    def test___init___デフォルトタイムゾーン_正しく初期化される(self):
        """Test __init__ initializes with default timezone."""
        converter = TimezoneConverter()
        assert converter._target_timezone == pytz.timezone("Asia/Tokyo")

    def test___init___指定タイムゾーン_正しく初期化される(self):
        """Test __init__ initializes with specified timezone."""
        converter = TimezoneConverter("UTC")
        assert converter._target_timezone == pytz.timezone("UTC")

    def test_convert_to_target_timezone_UTC日時_ターゲットタイムゾーンに変換される(self):
        """Test convert_to_target_timezone converts UTC datetime to target timezone."""
        converter = TimezoneConverter("Asia/Tokyo")
        utc_time = datetime(2023, 1, 1, 0, 0, 0)
        utc_time = pytz.UTC.localize(utc_time)

        result = converter.convert_to_target_timezone(utc_time)

        # Tokyo is UTC+9, so 00:00 UTC should be 09:00 Tokyo
        assert result.hour == 9
        assert result.tzinfo.zone == "Asia/Tokyo"

    def test_convert_to_target_timezone_タイムゾーンなし_UTCと仮定して変換される(self):
        """Test convert_to_target_timezone assumes UTC for naive datetime."""
        converter = TimezoneConverter("Asia/Tokyo")
        naive_time = datetime(2023, 1, 1, 0, 0, 0)

        result = converter.convert_to_target_timezone(naive_time)
        
        assert result.hour == 9  # UTC+9
        assert result.tzinfo.zone == "Asia/Tokyo"

    def test_localize_date_range_日付範囲_ローカライズされた範囲が返される(self):
        """Test localize_date_range returns localized date range."""
        converter = TimezoneConverter("Asia/Tokyo")
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 2)

        start_localized, end_localized = converter.localize_date_range(start_date, end_date)
        
        assert start_localized.tzinfo.zone == "Asia/Tokyo"
        assert end_localized.tzinfo.zone == "Asia/Tokyo"
        assert start_localized.hour == 0
        assert start_localized.minute == 0
        assert end_localized.hour == 23
        assert end_localized.minute == 59