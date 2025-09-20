"""
Service for listing summary files based on priority filter.
"""

import os
from pathlib import Path
from typing import List

from ...domain.priority_filter import PriorityFilter
from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.review_summary import ReviewSummary
from ...infrastructure.repositories.summary_repository import SummaryRepository


class ListSummaryFilesService:
    """Service for listing and filtering summary files."""

    def __init__(self, summary_repository: SummaryRepository):
        """Initialize the service with a summary repository.

        Args:
            summary_repository: Repository for accessing summary files
        """
        self._summary_repository = summary_repository

    def list_summary_files(
        self,
        repository_id: RepositoryIdentifier,
        priorities: List[str]
    ) -> List[str]:
        """List summary files filtered by priority.

        Args:
            repository_id: Repository identifier
            priorities: List of priorities to filter by (empty list means all)

        Returns:
            List of summary file paths matching the criteria
        """
        # Get the summaries directory path
        repo_dir = Path("pullrequests") / repository_id.owner / repository_id.name
        summaries_dir = repo_dir / "summaries"

        if not summaries_dir.exists():
            return []

        matching_files = []

        # Iterate through all yml files in the summaries directory
        for file_path in summaries_dir.glob("PR-*.yml"):
            # Extract PR number from filename
            filename = file_path.name
            if not filename.startswith("PR-") or not filename.endswith(".yml"):
                continue

            try:
                pr_number_str = filename[3:-4]  # Remove "PR-" and ".yml"
                pr_number = int(pr_number_str)
            except ValueError:
                continue

            # Load the summary
            summary = self._summary_repository.get(repository_id, pr_number)
            if summary is None:
                continue

            # Apply priority filter
            if not priorities or summary.priority in priorities:
                matching_files.append(str(file_path))

        return matching_files