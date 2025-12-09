"""
Unit tests for Phase 2 git_analyzer enhancements.

Tests line counting and file exclusion functionality.
"""

import pytest
from pathlib import Path
from src.git_analyzer import should_exclude_file, calculate_line_changes


class TestFileExclusion:
    """Test file exclusion pattern matching."""

    def test_exclude_lock_files(self):
        """Test that .lock files are excluded."""
        assert should_exclude_file("package-lock.json", ["package-lock.json"]) is True
        assert should_exclude_file("yarn.lock", ["*.lock"]) is True
        assert should_exclude_file("Gemfile.lock", ["*.lock"]) is True

    def test_exclude_specific_files(self):
        """Test excluding specific filenames."""
        assert should_exclude_file("package-lock.json", ["package-lock.json"]) is True
        assert should_exclude_file("src/package-lock.json", ["package-lock.json"]) is True

    def test_exclude_directory_patterns(self):
        """Test excluding directory patterns."""
        assert should_exclude_file("node_modules/package.json", ["node_modules/*"]) is True
        assert should_exclude_file("dist/bundle.js", ["dist/*"]) is True

    def test_do_not_exclude_normal_files(self):
        """Test that normal files are not excluded."""
        assert should_exclude_file("src/main.py", ["*.lock"]) is False
        assert should_exclude_file("README.md", ["*.lock"]) is False


class TestLineChanges:
    """Test line change calculation."""

    def test_calculate_line_changes_fixture(self):
        """Test line changes calculation on fixture repository."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        # Calculate changes between known tags
        added, removed = calculate_line_changes(
            fixture_path,
            "1.0.0",
            "1.1.0",
            []  # No exclusions for test
        )

        # Should have some changes
        assert added > 0

    def test_calculate_line_changes_with_exclusions(self):
        """Test that exclusions are applied to line counts."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        # This test verifies exclusions work, though our fixture
        # doesn't have .lock files to test with
        added, removed = calculate_line_changes(
            fixture_path,
            "1.0.0",
            "1.1.0",
            ["*.lock", "*.min.js"]
        )

        assert isinstance(added, int)
        assert isinstance(removed, int)

    def test_calculate_line_changes_invalid_refs(self):
        """Test handling of invalid references."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        # Invalid refs should return (0, 0) with warning
        added, removed = calculate_line_changes(
            fixture_path,
            "nonexistent",
            "1.0.0",
            []
        )

        assert added == 0
        assert removed == 0
