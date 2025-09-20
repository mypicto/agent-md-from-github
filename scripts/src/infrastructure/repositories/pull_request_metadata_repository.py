"""
PullRequestMetadata repository implementation for JSON persistence.
"""

import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from ...domain.interfaces.pull_request_metadata_repository_interface import PullRequestMetadataRepositoryInterface
from ...domain.pull_request_basic_info import PullRequestBasicInfo
from ...domain.pull_request_metadata import PullRequestMetadata
from ...domain.repository_identifier import RepositoryIdentifier


class PullRequestMetadataRepository(PullRequestMetadataRepositoryInterface):
    """Repository for persisting PullRequestMetadata to JSON files."""

    def save(self, pr_metadata: PullRequestMetadata, output_directory: Path) -> None:
        """Save PullRequestMetadata to JSON file.

        Args:
            pr_metadata: The PR metadata to save
            output_directory: Base output directory
        """
        # Create directory structure: output_directory / date / PR-number.json
        date_str = pr_metadata.closed_at.strftime("%Y-%m-%d")
        repo_path = output_directory / date_str
        repo_path.mkdir(parents=True, exist_ok=True)

        file_path = repo_path / f"PR-{pr_metadata.number}.json"

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
        file_path = output_directory / date_str / f"PR-{basic_info.number}.json"
        return file_path.exists()

    def find_all_by_repository(self, output_directory: Path, repository_id: RepositoryIdentifier) -> List[PullRequestMetadata]:
        """Find all PullRequestMetadata for the given repository.

        Args:
            output_directory: Base output directory
            repository_id: Repository identifier

        Returns:
            List of PullRequestMetadata
        """
        if not output_directory.exists():
            return []

        metadata_list = []
        for json_file in output_directory.rglob("PR-*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Deserialize
                from datetime import datetime
                from ...domain.review_comment import ReviewComment

                metadata = PullRequestMetadata(
                    number=data["number"],
                    title=data["title"],
                    closed_at=datetime.fromisoformat(data["closed_at"]),
                    is_merged=data["is_merged"],
                    review_comments=[
                        ReviewComment(
                            comment_id=comment["comment_id"],
                            file_path=comment["file_path"],
                            position=comment.get("position"),
                            commit_id=comment["commit_id"],
                            author=comment["author"],
                            created_at=datetime.fromisoformat(comment["created_at"]),
                            body=comment["body"],
                            diff_context=comment["diff_context"]
                        )
                        for comment in data["review_comments"]
                    ],
                    repository_id=RepositoryIdentifier(
                        owner=data["repository_id"]["owner"],
                        name=data["repository_id"]["name"]
                    )
                )

                # Filter by repository_id
                if metadata.repository_id == repository_id:
                    metadata_list.append(metadata)
            except (json.JSONDecodeError, KeyError, ValueError):
                # Skip invalid files
                continue

        return metadata_list

    def find_by_pr_number(self, output_directory: Path, repository_id: RepositoryIdentifier, pr_number: int) -> Optional[PullRequestMetadata]:
        """Find a specific PullRequestMetadata by PR number.

        Args:
            output_directory: Base output directory
            repository_id: Repository identifier
            pr_number: Pull request number

        Returns:
            PullRequestMetadata if found, None otherwise
        """
        all_metadata = self.find_all_by_repository(output_directory, repository_id)
        for metadata in all_metadata:
            if metadata.number == pr_number:
                return metadata
        return None