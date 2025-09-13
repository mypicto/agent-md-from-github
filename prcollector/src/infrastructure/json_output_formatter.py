"""
JSON output formatter implementation.
"""

import json
from typing import Dict

from ..domain.pull_request_metadata import PullRequestMetadata
from ..domain.review_comment import ReviewComment


class JsonOutputFormatter:
    """JSON format output formatter."""
    
    def format_comments(self, pr_metadata: PullRequestMetadata) -> str:
        """Format review comments as JSON."""
        comments_data = {
            "pr_number": pr_metadata.number,
            "closed_at_iso": pr_metadata.closed_at.isoformat(),
            "merged": pr_metadata.is_merged,
            "review_comments": [
                self._format_review_comment(comment) 
                for comment in pr_metadata.review_comments
            ]
        }
        
        return json.dumps(comments_data, indent=2, ensure_ascii=False)
    
    def format_diff_excerpt(self, pr_metadata: PullRequestMetadata) -> str:
        """Format diff excerpt as markdown."""
        diff_parts = [
            f"# PR #{pr_metadata.number}: {pr_metadata.title}",
            f"# Closed at: {pr_metadata.closed_at}",
            f"# Merged: {pr_metadata.is_merged}",
            ""
        ]
        
        # Group comments by file path
        comments_by_file = self._group_comments_by_file(pr_metadata.review_comments)
        
        # For each file with comments, extract relevant diff sections
        for file_path, file_comments in comments_by_file.items():
            diff_parts.extend([
                f"## File: {file_path}",
                ""
            ])
            
            for comment in file_comments:
                diff_parts.extend([
                    f"### Comment by {comment.author} at position {comment.position}",
                    f"Comment: {comment.body}",
                    "",
                    "```diff",
                    comment.diff_context,
                    "```",
                    ""
                ])
        
        return "\n".join(diff_parts)
    
    def _format_review_comment(self, comment: ReviewComment) -> Dict:
        """Format a single review comment."""
        return {
            "id": comment.comment_id,
            "path": comment.file_path,
            "original_position": comment.position,
            "commit_id": comment.commit_id,
            "user": comment.author,
            "created_at": comment.created_at.isoformat(),
            "body": comment.body,
            "context_patch_excerpt": comment.diff_context
        }
    
    def _group_comments_by_file(self, comments: list[ReviewComment]) -> Dict[str, list[ReviewComment]]:
        """Group comments by file path."""
        comments_by_file = {}
        for comment in comments:
            file_path = comment.file_path
            if file_path not in comments_by_file:
                comments_by_file[file_path] = []
            comments_by_file[file_path].append(comment)
        return comments_by_file