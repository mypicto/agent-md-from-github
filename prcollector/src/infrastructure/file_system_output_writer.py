"""
File system output writer implementation.
"""

from pathlib import Path

from ..domain.pull_request_metadata import PullRequestMetadata
from ..domain.pull_request_basic_info import PullRequestBasicInfo


class FileSystemOutputWriter:
    """File system output writer."""
    
    def write_pr_data(
        self, 
        pr_metadata: PullRequestMetadata, 
        comments_content: str, 
        diff_content: str, 
        output_directory: Path
    ) -> None:
        """Write PR data to file system."""
        # Create date-based directory structure
        date_folder = pr_metadata.closed_at.strftime("%Y-%m-%d")
        output_path = output_directory / date_folder
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Define file paths
        comments_file = output_path / f"PR-{pr_metadata.number}-comments.json"
        diff_file = output_path / f"PR-{pr_metadata.number}-diff.patch"
        
        # Write files
        self._write_text_file(comments_file, comments_content)
        self._write_text_file(diff_file, diff_content)
    
    def file_exists_from_basic_info(self, basic_info: PullRequestBasicInfo, output_directory: Path) -> bool:
        """Check if PR files already exist using basic info."""
        date_folder = basic_info.closed_at.strftime("%Y-%m-%d")
        output_path = output_directory / date_folder
        comments_file = output_path / f"PR-{basic_info.number}-comments.json"
        return comments_file.exists()
    
    def _write_text_file(self, file_path: Path, content: str) -> None:
        """Write text content to file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)