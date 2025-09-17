"""
File system implementation of review summary repository.
"""

import json
from pathlib import Path
from typing import Optional

from ...domain.review_summary import ReviewSummary
from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.interfaces.review_summary_repository_interface import ReviewSummaryRepositoryInterface


class ReviewSummaryRepository(ReviewSummaryRepositoryInterface):
    """File system based repository for review summaries."""
    
    def __init__(self, base_directory: str = "pullrequests"):
        """Initialize repository.
        
        Args:
            base_directory: Base directory for storing summaries
        """
        self._base_directory = Path(base_directory)
    
    def save(self, summary: ReviewSummary) -> None:
        """Save a review summary to file.
        
        Args:
            summary: The review summary to save
        """
        repo_dir = self._base_directory / summary.repository_id.owner / summary.repository_id.name
        summaries_dir = repo_dir / "summaries"
        summaries_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = summaries_dir / f"PR-{summary.pr_number}.json"
        
        data = {
            "repository_id": {
                "owner": summary.repository_id.owner,
                "name": summary.repository_id.name
            },
            "pr_number": summary.pr_number,
            "priority": summary.priority,
            "summary": summary.summary
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get(self, repository_id: RepositoryIdentifier, pr_number: int) -> Optional[ReviewSummary]:
        """Get a review summary from file.
        
        Args:
            repository_id: Repository identifier
            pr_number: PR number
            
        Returns:
            ReviewSummary if found, None otherwise
        """
        repo_dir = self._base_directory / repository_id.owner / repository_id.name
        summaries_dir = repo_dir / "summaries"
        file_path = summaries_dir / f"PR-{pr_number}.json"
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return ReviewSummary(
                repository_id=RepositoryIdentifier(
                    owner=data["repository_id"]["owner"],
                    name=data["repository_id"]["name"]
                ),
                pr_number=data["pr_number"],
                priority=data["priority"],
                summary=data["summary"]
            )
        except (json.JSONDecodeError, KeyError, ValueError):
            return None