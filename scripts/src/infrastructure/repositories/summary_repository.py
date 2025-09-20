"""
Repository for managing PR summaries.
"""

from pathlib import Path
from typing import Optional
from ruamel.yaml import YAML

from ...domain.interfaces.summary_repository_interface import SummaryRepositoryInterface
from ...domain.pull_request_metadata import PullRequestMetadata
from ...domain.review_summary import ReviewSummary
from ...domain.repository_identifier import RepositoryIdentifier


class SummaryRepository(SummaryRepositoryInterface):
    """Repository for managing PR summaries."""

    def __init__(self, base_directory: str = "pullrequests"):
        self._base_directory = Path(base_directory)
        self._yaml = YAML()
        self._yaml.default_style = '|'
        self._yaml.allow_unicode = True
        self._yaml.default_flow_style = False

    def _get_summary_path(self, repository_id: RepositoryIdentifier, pr_number: int, base_directory: Path) -> Path:
        """Generate the summary file path."""
        summaries_dir = base_directory / "summaries"
        return summaries_dir / f"PR-{pr_number}.yml"

    def exists_summary(self, metadata: PullRequestMetadata, output_directory: Path) -> bool:
        """Check if summary file exists for the given PR metadata."""
        summary_path = self._get_summary_path(metadata.repository_id, metadata.number, output_directory)
        return summary_path.exists()

    def save(self, summary: ReviewSummary) -> None:
        """Save a review summary to file."""
        summaries_dir = self._base_directory / "summaries"
        summaries_dir.mkdir(parents=True, exist_ok=True)

        file_path = summaries_dir / f"PR-{summary.pr_number}.yml"

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
            self._yaml.dump(data, f)

    def get(self, repository_id: RepositoryIdentifier, pr_number: int) -> Optional[ReviewSummary]:
        """Get a review summary by repository and PR number."""
        summary_path = self._get_summary_path(repository_id, pr_number, self._base_directory)
        if not summary_path.exists():
            return None

        with open(summary_path, 'r', encoding='utf-8') as f:
            data = self._yaml.load(f)

        return ReviewSummary(
            repository_id=repository_id,
            pr_number=data["pr_number"],
            priority=data["priority"],
            summary=data["summary"]
        )