"""
Date range value object for filtering PRs.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DateRange:
    """Represents a date range for filtering PRs."""
    
    start_date: datetime
    end_date: datetime
    
    def __post_init__(self):
        """Validate date range."""
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")
    
    def contains(self, target_date: datetime) -> bool:
        """Check if a date falls within this range."""
        return self.start_date <= target_date <= self.end_date