"""
Priority filter for filtering review summaries by priority.
"""

from typing import List

from .review_summary import ReviewSummary


class PriorityFilter:
    """Filter for review summaries based on priority levels."""

    @staticmethod
    def filter_by_priorities(
        summaries: List[ReviewSummary],
        priorities: List[str]
    ) -> List[ReviewSummary]:
        """Filter summaries by the specified priority levels.

        Args:
            summaries: List of review summaries to filter
            priorities: List of priority levels to include (e.g., ['high', 'middle'])

        Returns:
            Filtered list of review summaries
        """
        if not priorities:
            return summaries

        return [
            summary for summary in summaries
            if summary.priority in priorities
        ]