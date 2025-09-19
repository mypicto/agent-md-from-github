"""
Application service for getting comments.
"""

from pathlib import Path
from typing import List

from ...domain.comment_thread import CommentThread
from ...domain.pull_request_metadata import PullRequestMetadata
from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.review_comment import ReviewComment
from ...domain.interfaces.pull_request_metadata_repository_interface import PullRequestMetadataRepositoryInterface
from ...presentation.markdown_formatter import MarkdownFormatter
from ..exceptions.comments_service_error import CommentsServiceError


class CommentsService:
    """Application service for getting comments markdown."""
    
    def __init__(
        self,
        pr_metadata_repository: PullRequestMetadataRepositoryInterface,
        markdown_formatter: MarkdownFormatter
    ):
        """Initialize comments service.
        
        Args:
            pr_metadata_repository: PR metadata repository
            markdown_formatter: Markdown formatter
        """
        self._pr_metadata_repository = pr_metadata_repository
        self._markdown_formatter = markdown_formatter
    
    def get_comments_markdown(
        self,
        repo_id: RepositoryIdentifier,
        pr_number: int,
        output_directory: Path
    ) -> str:
        """Get comments markdown for the specified PR.
        
        Args:
            repo_id: Repository identifier
            pr_number: PR number as string
            output_directory: Output directory
            
        Returns:
            Markdown formatted comments
            
        Raises:
            CommentsServiceError: If PR not found or other errors
        """
        # Find all metadata for the repository
        target_pr = self._pr_metadata_repository.find_by_pr_number(output_directory, repo_id, pr_number)
        if target_pr is None:
            raise CommentsServiceError(f"PR not found: {pr_number}")
        
        # Group comments into threads
        threads = self._group_comments_into_threads(target_pr.review_comments)
        
        # Sort threads by file_path
        threads.sort(key=lambda t: t.file_path)
        
        # Sort comments within each thread by created_at
        for thread in threads:
            thread.comments.sort(key=lambda c: c.created_at)
        
        # Format to markdown
        markdown = self._markdown_formatter.format(threads)
        
        return markdown
    
    def _group_comments_into_threads(self, comments: List[ReviewComment]) -> List[CommentThread]:
        """Group comments into threads by file_path and position."""
        from collections import defaultdict
        
        thread_dict = defaultdict(list)
        
        for comment in comments:
            key = (comment.file_path, comment.position)
            thread_dict[key].append(comment)
        
        threads = []
        for (file_path, position), comments_list in thread_dict.items():
            threads.append(CommentThread(
                file_path=file_path,
                position=position,
                comments=comments_list
            ))
        
        return threads