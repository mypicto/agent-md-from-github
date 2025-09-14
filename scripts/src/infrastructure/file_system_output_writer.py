"""
File system output writer implementation.
"""

from pathlib import Path

from ..domain.pull_request_metadata import PullRequestMetadata
from ..domain.pull_request_basic_info import PullRequestBasicInfo
from .pull_request_file_path_resolver import PullRequestFilePathResolver


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
        # Get directory and file paths
        fileResolver = PullRequestFilePathResolver(output_directory, pr_metadata.repository_id, pr_metadata.closed_at, pr_metadata.number)
        
        # Create directory if it doesn't exist
        pr_directory = fileResolver.get_pr_directory()
        pr_directory.mkdir(parents=True, exist_ok=True)
        
        # Write files
        comments_file = fileResolver.get_comments_file_path()
        self._write_text_file(comments_file, comments_content)
        diff_file = fileResolver.get_diff_file_path()
        self._write_text_file(diff_file, diff_content)
    
    def file_exists_from_basic_info(self, basic_info: PullRequestBasicInfo, output_directory: Path) -> bool:
        """Check if PR files already exist using basic info."""
        fileResolver = PullRequestFilePathResolver(output_directory, basic_info.repository_id, basic_info.closed_at, basic_info.number)
        return fileResolver.file_exists()

    def _write_text_file(self, file_path: Path, content: str) -> None:
        """Write text content to file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)