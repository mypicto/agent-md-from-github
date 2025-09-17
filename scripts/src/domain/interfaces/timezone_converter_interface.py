"""
Interface for timezone conversion operations.
"""

from datetime import datetime
from typing import Protocol


class TimezoneConverterInterface(Protocol):
    """Interface for timezone conversion operations."""
    
    def convert_to_target_timezone(self, utc_datetime: datetime) -> datetime:
        """Convert UTC datetime to target timezone."""
        ...
    
    def localize_date_range(self, start_date: datetime, end_date: datetime) -> tuple[datetime, datetime]:
        """Localize date range to target timezone."""
        ...