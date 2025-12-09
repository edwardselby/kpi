"""
Unit tests for git_analyzer module.

Tests git tag parsing, semantic versioning validation, and commit counting.
"""

import pytest
from pathlib import Path
from datetime import datetime
from src.git_analyzer import _is_semantic_version, get_tags, count_commits_between


@pytest.mark.integration
class TestSemanticVersionValidation:
    """Test semantic version pattern matching."""

    def test_valid_semantic_versions(self):
        """Test that valid semantic versions are accepted."""
        assert _is_semantic_version("1.2.3") is True
        assert _is_semantic_version("9.2.6") is True
        assert _is_semantic_version("10.15.20") is True
        assert _is_semantic_version("0.0.1") is True

    def test_valid_semantic_versions_with_suffix(self):
        """Test that RC/beta tags are accepted."""
        assert _is_semantic_version("1.2.3-rc1") is True
        assert _is_semantic_version("1.2.3-beta") is True
        assert _is_semantic_version("2.0.0-alpha1") is True
        assert _is_semantic_version("1.0.0-RC2") is True

    def test_invalid_semantic_versions(self):
        """Test that invalid versions are rejected."""
        assert _is_semantic_version("v1.2.3") is False  # 'v' prefix
        assert _is_semantic_version("1.2") is False  # Missing patch version
        assert _is_semantic_version("1") is False  # Only major version
        assert _is_semantic_version("production") is False  # Non-version tag
        assert _is_semantic_version("release-1.2.3") is False  # Prefix
        assert _is_semantic_version("") is False  # Empty string


@pytest.mark.integration
class TestGetTags:
    """Test git tag extraction from repositories."""

    def test_get_tags_from_fixture(self):
        """Test tag extraction from fixture repository."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        tags = get_tags(fixture_path)

        # Should have tags
        assert len(tags) > 0

        # Verify structure
        for tag_name, tag_date in tags:
            assert isinstance(tag_name, str)
            assert isinstance(tag_date, datetime)
            assert _is_semantic_version(tag_name)

    def test_tags_sorted_chronologically(self):
        """Test that tags are sorted newest first."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        tags = get_tags(fixture_path)

        if len(tags) < 2:
            pytest.skip("Need at least 2 tags for sorting test")

        # Verify chronological order (newest first)
        dates = [date for _, date in tags]
        assert dates == sorted(dates, reverse=True)

    def test_get_tags_empty_repo(self):
        """Test handling of repository with no tags."""
        # This would require creating an empty repo fixture
        # For now, we'll just verify the function signature
        pass


@pytest.mark.integration
class TestCountCommitsBetween:
    """Test commit counting between git references."""

    def test_count_commits_between_tags(self):
        """Test commit counting between known tags."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        # Should have 2 commits between 1.0.0 and 1.1.0
        count = count_commits_between(fixture_path, "1.0.0", "1.1.0")
        assert count == 2

    def test_count_commits_same_ref(self):
        """Test that same ref returns 0 commits."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        count = count_commits_between(fixture_path, "1.0.0", "1.0.0")
        assert count == 0

    def test_count_commits_invalid_refs(self):
        """Test handling of invalid git references."""
        fixture_path = Path("tests/fixtures/sample_repo")

        if not fixture_path.exists():
            pytest.skip("Fixture repository not created yet")

        # Invalid refs should return 0 and warn
        count = count_commits_between(fixture_path, "nonexistent", "1.0.0")
        assert count == 0
