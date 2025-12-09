"""
Unit tests for git_analyzer module with mocks.

Fast tests that mock git operations for quick feedback.
These run by default (pytest without -m integration).
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from src.git_analyzer import (
    _is_semantic_version,
    get_tags,
    count_commits_between,
    calculate_line_changes,
    should_exclude_file
)


@pytest.mark.unit
class TestSemanticVersionValidationUnit:
    """Fast unit tests for semantic version validation (no mocks needed - pure logic)."""

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
        """Test that invalid semantic versions are rejected."""
        assert _is_semantic_version("1.2") is False
        assert _is_semantic_version("v1.2.3") is False
        assert _is_semantic_version("1.2.3.4") is False
        assert _is_semantic_version("abc") is False
        assert _is_semantic_version("release-1.2.3") is False
        assert _is_semantic_version("") is False


@pytest.mark.unit
class TestGetTagsUnit:
    """Fast unit tests for git tag extraction using mocks."""

    @patch('src.git_analyzer.git.Repo')
    def test_get_tags_with_mock_repo(self, mock_repo_class):
        """Test tag extraction with mocked repository."""
        # Create mock tags
        mock_tag1 = Mock()
        mock_tag1.name = '1.2.3'
        mock_tag1.commit.committed_date = 1700000000

        mock_tag2 = Mock()
        mock_tag2.name = '2.0.0'
        mock_tag2.commit.committed_date = 1700100000

        mock_tag3 = Mock()
        mock_tag3.name = 'invalid'  # Should be filtered out
        mock_tag3.commit.committed_date = 1700050000

        # Setup mock repo
        mock_repo = Mock()
        mock_repo.tags = [mock_tag1, mock_tag2, mock_tag3]
        mock_repo_class.return_value = mock_repo

        # Call function
        tags = get_tags(Path('/fake/path'))

        # Verify results (sorted by date, newest first, invalid filtered)
        assert len(tags) == 2
        assert tags[0][0] == '2.0.0'  # Newest
        assert tags[1][0] == '1.2.3'
        assert isinstance(tags[0][1], datetime)

    @patch('src.git_analyzer.git.Repo')
    def test_get_tags_empty_repo(self, mock_repo_class):
        """Test tag extraction from repository with no tags."""
        mock_repo = Mock()
        mock_repo.tags = []
        mock_repo_class.return_value = mock_repo

        tags = get_tags(Path('/fake/path'))

        assert tags == []


@pytest.mark.unit
class TestCountCommitsBetweenUnit:
    """Fast unit tests for commit counting using mocks."""

    @patch('src.git_analyzer.git.Repo')
    def test_count_commits_between_tags(self, mock_repo_class):
        """Test commit counting with mocked git log."""
        # Setup mock repo
        mock_repo = Mock()
        mock_repo.iter_commits.return_value = [Mock(), Mock(), Mock()]  # 3 commits
        mock_repo_class.return_value = mock_repo

        # Call function
        count = count_commits_between(Path('/fake/path'), 'v1.0.0', 'v1.1.0')

        # Verify count and that correct git range was used
        assert count == 3
        mock_repo.iter_commits.assert_called_once_with('v1.0.0..v1.1.0')

    @patch('src.git_analyzer.git.Repo')
    def test_count_commits_same_ref(self, mock_repo_class):
        """Test commit counting when refs are the same."""
        mock_repo = Mock()
        mock_repo.iter_commits.return_value = []
        mock_repo_class.return_value = mock_repo

        count = count_commits_between(Path('/fake/path'), 'v1.0.0', 'v1.0.0')

        assert count == 0


@pytest.mark.unit
class TestFileExclusionUnit:
    """Fast unit tests for file exclusion logic (no mocks needed - pure logic)."""

    def test_exclude_lock_files(self):
        """Test that lock files are excluded."""
        patterns = ["*.lock", "package-lock.json"]

        assert should_exclude_file("yarn.lock", patterns) is True
        assert should_exclude_file("package-lock.json", patterns) is True
        assert should_exclude_file("src/main.js", patterns) is False

    def test_exclude_specific_files(self):
        """Test exclusion of specific files."""
        patterns = ["*.min.js", "*.min.css"]

        assert should_exclude_file("app.min.js", patterns) is True
        assert should_exclude_file("style.min.css", patterns) is True
        assert should_exclude_file("app.js", patterns) is False

    def test_exclude_directory_patterns(self):
        """Test directory pattern matching."""
        patterns = ["node_modules/*", "dist/*"]

        assert should_exclude_file("node_modules/package/file.js", patterns) is True
        assert should_exclude_file("dist/bundle.js", patterns) is True
        assert should_exclude_file("src/index.js", patterns) is False

    def test_do_not_exclude_normal_files(self):
        """Test that normal files pass through."""
        patterns = ["*.lock", "*.min.js"]

        assert should_exclude_file("src/main.py", patterns) is False
        assert should_exclude_file("README.md", patterns) is False
        assert should_exclude_file("tests/test_foo.py", patterns) is False


@pytest.mark.unit
class TestLineChangesUnit:
    """Fast unit tests for line change calculations using mocks."""

    @patch('src.git_analyzer.git.Repo')
    def test_calculate_line_changes_with_mock(self, mock_repo_class):
        """Test line change calculation with mocked git diff."""
        # Setup mock repo
        mock_repo = Mock()

        # Mock diff output (format: added\tremoved\tfilename)
        mock_diff_output = """10\t2\tsrc/main.py
5\t3\tsrc/utils.py
0\t10\tsrc/old.py"""

        mock_repo.git.diff.return_value = mock_diff_output
        mock_repo_class.return_value = mock_repo

        # Call function
        added, removed = calculate_line_changes(
            Path('/fake/path'),
            'v1.0.0',
            'v1.1.0',
            []
        )

        # Verify line counts and git diff was called correctly
        assert added == 15  # 10 + 5 + 0
        assert removed == 15  # 2 + 3 + 10
        # Verify git diff was called with correct arguments
        mock_repo.git.diff.assert_called_once_with('v1.0.0', 'v1.1.0', numstat=True)

    @patch('src.git_analyzer.git.Repo')
    def test_calculate_line_changes_with_exclusions(self, mock_repo_class):
        """Test line changes with file exclusions."""
        mock_repo = Mock()

        # Include files that should be excluded
        mock_diff_output = """10\t2\tsrc/main.py
5\t3\tpackage-lock.json
100\t50\tnode_modules/pkg/index.js"""

        mock_repo.git.diff.return_value = mock_diff_output
        mock_repo_class.return_value = mock_repo

        # Call with exclusions
        added, removed = calculate_line_changes(
            Path('/fake/path'),
            'v1.0.0',
            'v1.1.0',
            ["package-lock.json", "node_modules/*"]
        )

        # Only src/main.py should be counted
        assert added == 10
        assert removed == 2
        # Verify git diff was called with correct arguments
        mock_repo.git.diff.assert_called_once_with('v1.0.0', 'v1.1.0', numstat=True)

    @patch('src.git_analyzer.git.Repo')
    def test_calculate_line_changes_binary_files(self, mock_repo_class):
        """Test that binary files are handled correctly."""
        mock_repo = Mock()

        # Binary files show as "-\t-"
        mock_diff_output = """10\t2\tsrc/main.py
-\t-\timage.png
5\t3\tREADME.md"""

        mock_repo.git.diff.return_value = mock_diff_output
        mock_repo_class.return_value = mock_repo

        added, removed = calculate_line_changes(
            Path('/fake/path'),
            'v1.0.0',
            'v1.1.0',
            []
        )

        # Binary file should be skipped
        assert added == 15  # 10 + 5
        assert removed == 5  # 2 + 3
        # Verify git diff was called with correct arguments
        mock_repo.git.diff.assert_called_once_with('v1.0.0', 'v1.1.0', numstat=True)
