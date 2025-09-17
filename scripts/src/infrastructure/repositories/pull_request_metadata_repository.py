"""
PullRequestMetadata repository implementation for JSON persistence.
"""

import json
from dataclasses import asdict
from pathlib import Path

from ...domain.interfaces.pull_request_metadata_repository_interface import PullRequestMetadataRepositoryInterface
from ...domain.pull_request_basic_info import PullRequestBasicInfo
from ...domain.pull_request_metadata import PullRequestMetadata


class PullRequestMetadataRepository(PullRequestMetadataRepositoryInterface):
    """Repository for persisting PullRequestMetadata to JSON files."""

    def save(self, pr_metadata: PullRequestMetadata, output_directory: Path) -> None:
        """Save PullRequestMetadata to JSON file.

        Args:
            pr_metadata: The PR metadata to save
            output_directory: Base output directory
        """
        # Create directory structure: output_directory / org / repo / date / PR-number-metadata.json
        date_str = pr_metadata.closed_at.strftime("%Y-%m-%d")
        repo_path = output_directory / pr_metadata.repository_id.owner / pr_metadata.repository_id.name / date_str
        repo_path.mkdir(parents=True, exist_ok=True)

        file_path = repo_path / f"PR-{pr_metadata.number}-metadata.json"

        # Convert to dict and handle datetime serialization
        data = asdict(pr_metadata)
        data["closed_at"] = pr_metadata.closed_at.isoformat()

        # Serialize review_comments with datetime handling
        data["review_comments"] = [
            {
                **asdict(comment),
                "created_at": comment.created_at.isoformat()
            }
            for comment in pr_metadata.review_comments
        ]

        # Serialize repository_id
        data["repository_id"] = asdict(pr_metadata.repository_id)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def exists(self, basic_info: PullRequestBasicInfo, output_directory: Path) -> bool:
        """Check if PR metadata file already exists.

        Args:
            basic_info: Basic PR info
            output_directory: Base output directory

        Returns:
            True if file exists
        """
        date_str = basic_info.closed_at.strftime("%Y-%m-%d")
        file_path = output_directory / basic_info.repository_id.owner / basic_info.repository_id.name / date_str / f"PR-{basic_info.number}-metadata.json"
        return file_path.exists()