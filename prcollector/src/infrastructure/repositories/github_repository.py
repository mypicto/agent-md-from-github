"""
GitHub API repository implementation.
"""

import logging
from datetime import datetime
from typing import Generator

from github import Github
from github.GithubException import GithubException

from ...domain.interfaces.github_repository_interface import GitHubRepositoryInterface
from ...domain.date_range import DateRange
from ...domain.pull_request_metadata import PullRequestMetadata
from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.review_comment import ReviewComment
from ..services.timezone_converter import TimezoneConverter
from ...application.exceptions.github_api_error import GitHubApiError


class GitHubRepository:
    """GitHub API repository implementation."""
    
    def __init__(self, github_client: Github, timezone_converter: TimezoneConverter):
        """Initialize GitHub repository.
        
        Args:
            github_client: Authenticated GitHub client
            timezone_converter: Timezone conversion service
        """
        self._github = github_client
        self._timezone_converter = timezone_converter
        self._logger = logging.getLogger("prcollector")
    
    def find_closed_pull_requests_in_range(
        self, 
        repo_id: RepositoryIdentifier, 
        date_range: DateRange
    ) -> Generator[PullRequestMetadata, None, None]:
        """Find closed PRs within the specified date range."""
        try:
            repo = self._github.get_repo(repo_id.to_string())
        except GithubException as e:
            raise GitHubApiError(f"Failed to access repository {repo_id.to_string()}: {e}")
        
        try:
            # Get all closed PRs (both merged and closed without merge)
            prs = repo.get_pulls(state='closed', sort='updated', direction='desc')
            
            self._logger.info("Starting PR search...")
            pr_count = 0
            
            for pr in prs:
                if pr.closed_at is None:
                    continue
                
                # Convert to target timezone
                closed_at_tz = self._timezone_converter.convert_to_target_timezone(pr.closed_at)
                
                if date_range.contains(closed_at_tz):
                    pr_count += 1
                    self._logger.debug(f"Found matching PR #{pr.number} (closed: {closed_at_tz.date()})")
                    pr_metadata = self._convert_to_pr_metadata(pr, closed_at_tz)
                    yield pr_metadata
                elif closed_at_tz < date_range.start_date:
                    # PRs are sorted by updated date in descending order
                    # If we hit a PR older than our range, we can stop
                    self._logger.debug(f"Reached PR #{pr.number} older than range, stopping search")
                    break
            
            self._logger.info(f"PR search completed. Found {pr_count} matching PRs.")
                    
        except GithubException as e:
            raise GitHubApiError(f"Error fetching PRs: {e}")
    
    def _convert_to_pr_metadata(self, pr, closed_at_tz: datetime) -> PullRequestMetadata:
        """Convert GitHub PR object to domain model."""
        review_comments = self._extract_review_comments(pr)
        
        return PullRequestMetadata(
            number=pr.number,
            title=pr.title,
            closed_at=closed_at_tz,
            is_merged=pr.merged,
            review_comments=review_comments
        )
    
    def _extract_review_comments(self, pr) -> list[ReviewComment]:
        """Extract review comments from PR."""
        comments = []
        
        try:
            # Get review comments (inline comments on code)
            review_comments = pr.get_review_comments()
            
            for comment in review_comments:
                created_at_tz = self._timezone_converter.convert_to_target_timezone(comment.created_at)
                diff_context = self._extract_diff_context(comment)
                
                review_comment = ReviewComment(
                    comment_id=comment.id,
                    file_path=comment.path,
                    position=comment.original_position,
                    commit_id=comment.commit_id,
                    author=comment.user.login,
                    created_at=created_at_tz,
                    body=comment.body,
                    diff_context=diff_context
                )
                comments.append(review_comment)
                
        except GithubException as e:
            self._logger.warning(f"Error fetching review comments: {e}")
        
        return comments
    
    def _extract_diff_context(self, comment) -> str:
        """Extract diff context from comment."""
        try:
            if hasattr(comment, 'diff_hunk') and comment.diff_hunk:
                return comment.diff_hunk
            else:
                return f"@@ Position: {comment.original_position} in {comment.path} @@"
        except Exception as e:
            self._logger.warning(f"Could not extract context patch: {e}")
            return f"@@ Position: {comment.original_position} in {comment.path} @@"