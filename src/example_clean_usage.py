#!/usr/bin/env python3
"""
Example usage of the redesigned PR collector.

This demonstrates the clean architecture principles with proper 
class-to-file mapping and how different components can be composed and tested.
"""

import os
from datetime import datetime
from pathlib import Path

from src.domain import DateRange, RepositoryIdentifier
from src.infrastructure import ServiceFactory, TimezoneConverter
from src.presentation import CLIController


def example_direct_usage():
    """Example of using the service directly without CLI."""
    print("=== Direct Service Usage Example ===")
    
    # Get token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        return
    
    try:
        # Create service using factory
        service = ServiceFactory.create_pr_collection_service(
            github_token=token,
            timezone="Asia/Tokyo"
        )
        
        # Setup parameters using domain models
        repo_id = RepositoryIdentifier.from_string("microsoft/TypeScript")
        date_range = DateRange(
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 1, 7)
        )
        output_dir = Path("example_output")
        
        # Execute collection
        service.collect_review_comments(
            repository_id=repo_id,
            date_range=date_range,
            output_directory=output_dir
        )
        
        print("Collection completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")


def example_cli_usage():
    """Example of using the CLI interface."""
    print("\\n=== CLI Usage Example ===")
    
    # Create CLI controller
    cli = CLIController()
    
    # Example command-line arguments
    test_args = [
        "--repo", "owner/repo",
        "--from-date", "2024-01-01", 
        "--to-date", "2024-01-07",
        "--output-dir", "cli_output",
        "--timezone", "UTC",
        "--verbose"
    ]
    
    print("Would run with args:", " ".join(test_args))
    print("Note: This would require a valid GitHub token")


def example_custom_components():
    """Example of using custom components with dependency injection."""
    print("\\n=== Custom Components Example ===")
    
    # Create timezone converter
    converter = TimezoneConverter("UTC")
    
    # Test timezone conversion
    utc_time = datetime(2024, 1, 1, 12, 0, 0)
    tokyo_time = converter.convert_to_target_timezone(utc_time)
    
    print(f"UTC time: {utc_time}")
    print(f"Converted time: {tokyo_time}")
    
    # Test date range validation
    try:
        # This should work
        valid_range = DateRange(
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 1, 7)
        )
        print(f"Valid range: {valid_range}")
        
        # This should fail
        invalid_range = DateRange(
            start_date=datetime(2024, 1, 7),
            end_date=datetime(2024, 1, 1)
        )
        
    except ValueError as e:
        print(f"Expected validation error: {e}")


def show_architecture_benefits():
    """Show the benefits of the clean architecture."""
    print("\\n=== Architecture Benefits ===")
    
    benefits = [
        "✅ Single Responsibility: Each class has one clear purpose",
        "✅ Open/Closed: Easy to extend with new output formats",
        "✅ DRY: No code duplication across components",
        "✅ Law of Demeter: Minimal coupling between components", 
        "✅ KISS: Simple, focused interfaces",
        "✅ Testable: Each component can be tested in isolation",
        "✅ Flexible: Easy to swap implementations (Strategy pattern)",
        "✅ Domain-driven: Business logic separated from infrastructure",
        "✅ Class-to-File Mapping: Each class in its own file for better organization"
    ]
    
    for benefit in benefits:
        print(benefit)


def show_file_structure():
    """Show the new file structure."""
    print("\\n=== File Structure ===")
    
    structure = """
src/
├── domain/                     # Domain Layer
│   ├── __init__.py
│   ├── date_range.py          # DateRange value object
│   ├── repository_identifier.py # RepositoryIdentifier value object
│   ├── review_comment.py      # ReviewComment value object
│   └── pull_request_metadata.py # PullRequestMetadata value object
├── application/               # Application Layer
│   ├── __init__.py
│   └── pr_review_collection_service.py # Main business logic
├── infrastructure/            # Infrastructure Layer
│   ├── __init__.py
│   ├── timezone_converter.py # Timezone conversion service
│   ├── github_repository.py  # GitHub API implementation
│   ├── json_output_formatter.py # JSON formatting
│   ├── file_system_output_writer.py # File system output
│   └── service_factory.py    # Dependency injection
├── presentation/              # Presentation Layer
│   ├── __init__.py
│   └── cli_controller.py      # CLI interface
├── __init__.py               # Package initialization
├── main.py                   # Main entry point
└── example_clean_usage.py    # Usage examples
    """
    
    print(structure)


def main():
    """Run all examples."""
    print("GitHub PR Collector - Clean Architecture Examples")
    print("=" * 50)
    
    show_file_structure()
    example_direct_usage()
    example_cli_usage() 
    example_custom_components()
    show_architecture_benefits()
    
    print("\\n" + "=" * 50)
    print("For actual usage, run:")
    print("python src/main.py --repo 'owner/repo' --from-date '2024-01-01' --to-date '2024-01-07'")


if __name__ == "__main__":
    main()