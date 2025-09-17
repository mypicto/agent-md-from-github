"""
Markdown formatter for comment threads.
"""

from typing import List

from scripts.src.domain.comment_thread import CommentThread


class MarkdownFormatter:
    """Formatter for converting comment threads to markdown."""
    
    def format(self, threads: List[CommentThread]) -> str:
        """Format comment threads to markdown string.
        
        Args:
            threads: List of comment threads
            
        Returns:
            Markdown formatted string
        """
        lines = []
        for thread in threads:
            lines.append(f"## {thread.file_path}")
            lines.append("")
            
            # Add diff context if available (from first comment)
            if thread.comments and thread.comments[0].diff_context:
                lines.append("```diff")
                lines.append(thread.comments[0].diff_context)
                lines.append("```")
                lines.append("")
            
            # Add comments
            for comment in thread.comments:
                lines.append(f"- **{comment.author}**: {comment.body}")
            lines.append("")
        
        return "\n".join(lines)