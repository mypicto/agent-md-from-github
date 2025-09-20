"""
Timezone conversion service implementation.
"""

from datetime import datetime

import pytz


class TimezoneConverter:
    """Timezone conversion service implementation."""
    
    def __init__(self, target_timezone: str = "UTC"):
        """Initialize timezone converter.
        
        Args:
            target_timezone: Target timezone name (default: UTC)
        """
        self._target_timezone = pytz.timezone(target_timezone)
    
    def convert_to_target_timezone(self, utc_datetime: datetime) -> datetime:
        """Convert UTC datetime to target timezone."""
        if utc_datetime.tzinfo is None:
            # Assume UTC if no timezone info
            utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
        elif utc_datetime.tzinfo != pytz.UTC:
            # Convert to UTC first if different timezone
            utc_datetime = utc_datetime.astimezone(pytz.UTC)
        
        return utc_datetime.astimezone(self._target_timezone)
    
    def localize_date_range(self, start_date: datetime, end_date: datetime) -> tuple[datetime, datetime]:
        """Localize date range to target timezone."""
        # Set start of day for start date
        start_localized = self._target_timezone.localize(
            start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        )
        
        # Set end of day for end date  
        end_localized = self._target_timezone.localize(
            end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        )
        
        return start_localized, end_localized