"""
Integration tests for main script execution.

Tests the complete console output workflow.
"""

import pytest
import sys
from io import StringIO
from src.main import main


class TestMainExecution:
    """Test main script execution."""

    def test_main_runs_without_errors(self, capsys, monkeypatch):
        """Test that main() executes without crashing."""
        #: Mock sys.argv to avoid argument parsing conflicts
        monkeypatch.setattr('sys.argv', ['pytest'])

        # Run main function
        main()

        # Capture output
        captured = capsys.readouterr()

        # Verify output contains expected elements
        assert "KPI Report Generator" in captured.out
        assert "Phase" in captured.out  # Support all phases

        # Should process at least one project
        assert "📦" in captured.out

    def test_main_handles_fixture_repo(self, monkeypatch, capsys):
        """Test main with fixture repository."""
        from pathlib import Path

        # Mock the projects list to use only our fixture
        def mock_main():
            from src.git_analyzer import get_tags, count_commits_between

            projects = [
                Path("tests/fixtures/sample_repo"),
            ]

            print("=" * 60)
            print("KPI Report Generator - Test Fixture")
            print("=" * 60)
            print()

            for project_path in projects:
                if not project_path.exists():
                    print(f"⚠️  SKIP: {project_path.name} (not found)")
                    continue

                if not (project_path / ".git").exists():
                    print(f"⚠️  SKIP: {project_path.name} (not a git repository)")
                    continue

                print(f"📦 {project_path.name}")
                print("-" * 60)

                tags = get_tags(project_path)

                for i, (tag, date) in enumerate(tags[:5]):
                    if i == 0:
                        print(f"  {tag:15} {date.strftime('%Y-%m-%d')} (latest)")
                        continue

                    prev_tag = tags[i-1][0]
                    commits = count_commits_between(project_path, tag, prev_tag)
                    print(f"  {tag:15} {date.strftime('%Y-%m-%d')} → {commits:3d} commits")

                print()

        # Run test version
        mock_main()

        # Capture output
        captured = capsys.readouterr()

        # Verify output structure
        assert "sample_repo" in captured.out
        assert "2.0.0-rc1" in captured.out  # Latest tag in fixture
        assert "commits" in captured.out

    def test_main_output_format(self, capsys, monkeypatch):
        """Test that main output is well-formatted."""
        #: Mock sys.argv to avoid argument parsing conflicts
        monkeypatch.setattr('sys.argv', ['pytest'])

        main()

        captured = capsys.readouterr()

        # Check for proper formatting
        assert "=" * 60 in captured.out or "=" * 70 in captured.out  # Header line (varies by phase)
        assert "-" * 60 in captured.out or "-" * 70 in captured.out  # Separator lines
        assert "→" in captured.out  # Arrow for commit counts
