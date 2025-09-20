"""
Repository identifier validation for workspace management.

This module provides validation logic for repository identifiers
following the owner/repository format required by GitHub.
"""

import re
from typing import Tuple

from .repository_identifier import RepositoryIdentifier


class RepositoryIdentifierValidator:
    """Repository identifier format validation specialized class.
    
    This class is responsible for validating and parsing repository
    identifiers in the format 'owner/repository' according to GitHub
    naming conventions.
    """

    # GitHub username/organization name pattern
    # - Must start with alphanumeric character
    # - Can contain hyphens but not consecutive hyphens
    # - Cannot start or end with hyphen
    # - Maximum 39 characters
    _OWNER_PATTERN = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,37}[a-zA-Z0-9])?$'
    
    # GitHub repository name pattern
    # - Must start with alphanumeric character
    # - Can contain hyphens, underscores, and dots
    # - Cannot start with dot
    # - Cannot end with hyphen
    # - Maximum 100 characters
    _REPOSITORY_PATTERN = r'^[a-zA-Z0-9][a-zA-Z0-9\-_.]*[a-zA-Z0-9._]$|^[a-zA-Z0-9]$'

    @staticmethod
    def validate_format(repository_spec: str) -> bool:
        """Validate repository identifier format.
        
        Args:
            repository_spec: Repository specification in 'owner/repository' format
            
        Returns:
            True if format is valid, False otherwise
            
        Examples:
            >>> RepositoryIdentifierValidator.validate_format("owner/repo")
            True
            >>> RepositoryIdentifierValidator.validate_format("invalid")
            False
        """
        if not repository_spec or not isinstance(repository_spec, str):
            return False
            
        parts = repository_spec.split('/')
        if len(parts) != 2:
            return False
            
        owner, repository = parts
        
        return (
            RepositoryIdentifierValidator._validate_owner(owner) and
            RepositoryIdentifierValidator._validate_repository_name(repository)
        )

    @staticmethod
    def parse_repository_spec(repository_spec: str) -> RepositoryIdentifier:
        """Parse repository specification string into RepositoryIdentifier object.
        
        Args:
            repository_spec: Repository specification in 'owner/repository' format
            
        Returns:
            RepositoryIdentifier object
            
        Raises:
            ValueError: If repository specification format is invalid
            
        Examples:
            >>> validator = RepositoryIdentifierValidator()
            >>> repo_id = validator.parse_repository_spec("owner/repo")
            >>> repo_id.owner
            'owner'
            >>> repo_id.name
            'repo'
        """
        if not RepositoryIdentifierValidator.validate_format(repository_spec):
            raise ValueError(f"Invalid repository specification format: {repository_spec}")
            
        owner, repository = repository_spec.split('/')
        return RepositoryIdentifier(owner=owner, name=repository)

    @staticmethod
    def _validate_owner(owner: str) -> bool:
        """Validate owner name according to GitHub username rules.
        
        Args:
            owner: Owner/organization name
            
        Returns:
            True if valid, False otherwise
        """
        if not owner or len(owner) > 39:
            return False
            
        return bool(re.match(RepositoryIdentifierValidator._OWNER_PATTERN, owner))

    @staticmethod
    def _validate_repository_name(repository: str) -> bool:
        """Validate repository name according to GitHub repository rules.
        
        Args:
            repository: Repository name
            
        Returns:
            True if valid, False otherwise
        """
        if not repository or len(repository) > 100:
            return False
            
        return bool(re.match(RepositoryIdentifierValidator._REPOSITORY_PATTERN, repository))