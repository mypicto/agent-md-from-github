"""
File system output writer implementation.
"""

from pathlib import Path

from ..domain.pull_request_metadata import PullRequestMetadata
from ..domain.pull_request_basic_info import PullRequestBasicInfo
from .pull_request_file_set import PullRequestFileSet


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
        fileSet = PullRequestFileSet.create_with_metadata(output_directory, pr_metadata)
        
        # Create directory if it doesn't exist
        pr_directory = fileSet.get_pr_directory()
        pr_directory.mkdir(parents=True, exist_ok=True)
        
        # Write files
        comments_file = fileSet.get_comments_file_path()
        self._write_text_file(comments_file, comments_content)
        diff_file = fileSet.get_diff_file_path()
        self._write_text_file(diff_file, diff_content)
    
    def exists_file_from_basic_info(self, basic_info: PullRequestBasicInfo, output_directory: Path) -> bool:
        """Check if PR files already exist using basic info."""
        fileSet = PullRequestFileSet.create_with_basic_info(output_directory, basic_info)
        return fileSet.exists_file()

    def _write_text_file(self, file_path: Path, content: str) -> None:
        """Write text content to file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)