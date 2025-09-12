#!/usr/bin/env python3
"""
GitHub Pull Request Review Comments Collector

This script collects review comments and related diff excerpts 
from closed pull requests in a specified GitHub repository within a date range.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pytz
from github import Github


class PRCollector:
    """Collects PR review comments and related diffs from GitHub repository."""
    
    def __init__(self, token: str, timezone: str = "Asia/Tokyo"):
        """
        Initialize the collector.
        
        Args:
            token: GitHub personal access token
            timezone: Timezone for date filtering (default: Asia/Tokyo)
        """
        self.github = Github(token)
        self.timezone = pytz.timezone(timezone)
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger("prcollector")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def collect_prs(
        self, 
        repo_name: str, 
        date_from: datetime, 
        date_to: datetime,
        output_dir: str = "pullrequests"
    ) -> None:
        """
        Collect PR review comments and diffs for the specified period.
        
        Args:
            repo_name: Repository name in format "owner/repo"
            date_from: Start date (inclusive)
            date_to: End date (inclusive)
            output_dir: Output directory for results
        """
        self.logger.info(f"Starting collection for {repo_name}")
        self.logger.info(f"Period: {date_from.date()} to {date_to.date()}")
        
        try:
            repo = self.github.get_repo(repo_name)
        except Exception as e:
            self.logger.error(f"Failed to access repository {repo_name}: {e}")
            return
            
        # Convert dates to timezone-aware datetime objects
        date_from_tz = self.timezone.localize(date_from.replace(hour=0, minute=0, second=0))
        date_to_tz = self.timezone.localize(date_to.replace(hour=23, minute=59, second=59))
        
        self.logger.info(f"Searching for PRs closed between {date_from_tz} and {date_to_tz}")
        
        # Get closed PRs within the date range
        closed_prs = self._get_closed_prs_in_period(repo, date_from_tz, date_to_tz)
        
        self.logger.info(f"Found {len(closed_prs)} PRs closed in the specified period")
        
        for pr in closed_prs:
            self._process_pr(pr, output_dir)
            
        self.logger.info("Collection completed")
    
    def _get_closed_prs_in_period(
        self, 
        repo, 
        date_from: datetime, 
        date_to: datetime
    ) -> List:
        """
        Get all PRs closed within the specified period.
        
        Args:
            repo: GitHub repository object
            date_from: Start datetime (timezone-aware)
            date_to: End datetime (timezone-aware)
            
        Returns:
            List of PullRequest objects
        """
        closed_prs = []
        
        try:
            # Get all closed PRs (both merged and closed without merge)
            prs = repo.get_pulls(state='closed', sort='updated', direction='desc')
            
            for pr in prs:
                if pr.closed_at is None:
                    continue
                    
                # Convert to timezone-aware datetime
                closed_at_tz = pr.closed_at.replace(tzinfo=pytz.UTC).astimezone(self.timezone)
                
                if date_from <= closed_at_tz <= date_to:
                    closed_prs.append(pr)
                elif closed_at_tz < date_from:
                    # PRs are sorted by updated date in descending order
                    # If we hit a PR older than our range, we can stop
                    break
                    
        except Exception as e:
            self.logger.error(f"Error fetching PRs: {e}")
            
        return closed_prs
    
    def _process_pr(self, pr, output_dir: str) -> None:
        """
        Process a single PR to extract review comments and diffs.
        
        Args:
            pr: PullRequest object
            output_dir: Output directory
        """
        closed_at_tz = pr.closed_at.replace(tzinfo=pytz.UTC).astimezone(self.timezone)
        date_folder = closed_at_tz.strftime("%Y-%m-%d")
        
        # Create output directory structure
        output_path = Path(output_dir) / date_folder
        output_path.mkdir(parents=True, exist_ok=True)
        
        comments_file = output_path / f"PR-{pr.number}-comments.json"
        diff_file = output_path / f"PR-{pr.number}-diff.patch"
        
        # Skip if comments file already exists (idempotency)
        if comments_file.exists():
            self.logger.info(f"Skipping PR #{pr.number} - comments file already exists")
            return
            
        self.logger.info(f"Processing PR #{pr.number}: {pr.title}")
        
        try:
            # Get review comments (inline comments only)
            review_comments = self._get_review_comments(pr)
            
            if not review_comments:
                self.logger.info(f"No review comments found for PR #{pr.number}")
                return
                
            # Prepare comments data
            comments_data = {
                "pr_number": pr.number,
                "closed_at_iso": closed_at_tz.isoformat(),
                "merged": pr.merged,
                "review_comments": review_comments
            }
            
            # Save comments to JSON file
            with open(comments_file, 'w', encoding='utf-8') as f:
                json.dump(comments_data, f, indent=2, ensure_ascii=False)
                
            # Generate and save diff excerpt
            diff_excerpt = self._generate_diff_excerpt(pr, review_comments)
            with open(diff_file, 'w', encoding='utf-8') as f:
                f.write(diff_excerpt)
                
            self.logger.info(f"Saved PR #{pr.number} data ({len(review_comments)} comments)")
            
        except Exception as e:
            self.logger.error(f"Error processing PR #{pr.number}: {e}")
    
    def _get_review_comments(self, pr) -> List[Dict]:
        """
        Get review comments (inline comments) for a PR.
        
        Args:
            pr: PullRequest object
            
        Returns:
            List of review comment dictionaries
        """
        comments = []
        
        try:
            # Get review comments (inline comments on code)
            review_comments = pr.get_review_comments()
            
            for comment in review_comments:
                comment_data = {
                    "id": comment.id,
                    "path": comment.path,
                    "original_position": comment.original_position,
                    "commit_id": comment.commit_id,
                    "user": comment.user.login,
                    "created_at": comment.created_at.replace(tzinfo=pytz.UTC).astimezone(self.timezone).isoformat(),
                    "body": comment.body,
                    "context_patch_excerpt": self._extract_context_patch(comment)
                }
                comments.append(comment_data)
                
        except Exception as e:
            self.logger.error(f"Error fetching review comments: {e}")
            
        return comments
    
    def _extract_context_patch(self, comment) -> str:
        """
        Extract context patch around the comment position.
        
        Args:
            comment: PullRequestReviewComment object
            
        Returns:
            Patch excerpt string
        """
        try:
            if hasattr(comment, 'diff_hunk') and comment.diff_hunk:
                return comment.diff_hunk
            else:
                return f"@@ Position: {comment.original_position} in {comment.path} @@"
        except Exception as e:
            self.logger.warning(f"Could not extract context patch: {e}")
            return f"@@ Position: {comment.original_position} in {comment.path} @@"
    
    def _generate_diff_excerpt(self, pr, review_comments: List[Dict]) -> str:
        """
        Generate diff excerpt for lines with review comments (±3 lines context).
        
        Args:
            pr: PullRequest object
            review_comments: List of review comment dictionaries
            
        Returns:
            Diff excerpt string
        """
        diff_parts = []
        
        try:
            # Get the full diff for the PR
            diff_parts.append(f"# PR #{pr.number}: {pr.title}")
            diff_parts.append(f"# Closed at: {pr.closed_at}")
            diff_parts.append(f"# Merged: {pr.merged}")
            diff_parts.append("")
            
            # Group comments by file path
            comments_by_file = {}
            for comment in review_comments:
                file_path = comment["path"]
                if file_path not in comments_by_file:
                    comments_by_file[file_path] = []
                comments_by_file[file_path].append(comment)
            
            # For each file with comments, extract relevant diff sections
            for file_path, file_comments in comments_by_file.items():
                diff_parts.append(f"## File: {file_path}")
                diff_parts.append("")
                
                for comment in file_comments:
                    diff_parts.append(f"### Comment by {comment['user']} at position {comment['original_position']}")
                    diff_parts.append(f"Comment: {comment['body']}")
                    diff_parts.append("")
                    diff_parts.append("```diff")
                    diff_parts.append(comment["context_patch_excerpt"])
                    diff_parts.append("```")
                    diff_parts.append("")
                    
        except Exception as e:
            self.logger.error(f"Error generating diff excerpt: {e}")
            diff_parts.append(f"Error generating diff: {e}")
            
        return "\n".join(diff_parts)


def parse_date(date_str: str) -> datetime:
    """
    Parse date string in YYYY-MM-DD format.
    
    Args:
        date_str: Date string
        
    Returns:
        datetime object
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Collect GitHub PR review comments and diffs for a specified period"
    )
    parser.add_argument(
        "--repo", 
        required=True, 
        help="Repository name in format 'owner/repo'"
    )
    parser.add_argument(
        "--from-date", 
        type=parse_date, 
        required=True,
        help="Start date (inclusive) in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--to-date", 
        type=parse_date, 
        required=True,
        help="End date (inclusive) in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--output-dir", 
        default="pullrequests",
        help="Output directory (default: pullrequests)"
    )
    parser.add_argument(
        "--timezone", 
        default="Asia/Tokyo",
        help="Timezone for date filtering (default: Asia/Tokyo)"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_TOKEN environment variable)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger("prcollector").setLevel(logging.DEBUG)
    
    # Get GitHub token
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GitHub token not provided. Use --token or set GITHUB_TOKEN environment variable.")
        sys.exit(1)
    
    # Validate date range
    if args.from_date > args.to_date:
        print("Error: from-date must be before or equal to to-date")
        sys.exit(1)
    
    # Initialize collector and run
    try:
        collector = PRCollector(token, args.timezone)
        collector.collect_prs(
            args.repo, 
            args.from_date, 
            args.to_date, 
            args.output_dir
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()