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
