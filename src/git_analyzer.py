"""
Git repository analysis for KPI metrics.

This module provides functions to extract git tags, count commits, and calculate
line changes between releases for development metrics reporting.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Union
import re
import git
import fnmatch


def _is_semantic_version(tag_name: str) -> bool:
    """
    Validate if tag name matches semantic versioning pattern.

    Accepts patterns:
    - X.Y.Z (e.g., "1.2.3", "9.2.6")
    - X.Y.Z-suffix (e.g., "1.2.3-rc1", "2.0.0-beta")

    Rejects:
    - Version with 'v' prefix (e.g., "v1.2.3")
    - Incomplete versions (e.g., "1.2")
    - Non-version tags (e.g., "production", "staging")

    :param tag_name: Tag name to validate
    :type tag_name: str
    :return: True if matches semantic version pattern
    :rtype: bool

    :Example:

    >>> _is_semantic_version("1.2.3")
    True
    >>> _is_semantic_version("1.2.3-rc1")
    True
    >>> _is_semantic_version("v1.2.3")
    False
    """
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
    return bool(re.match(pattern, tag_name))


def get_tags(repo_path: Path) -> List[Tuple[str, datetime]]:
    """
    Extract all semantic version tags from repository, sorted chronologically.

    Opens the git repository and extracts all tags that match semantic
    versioning pattern (X.Y.Z or X.Y.Z-suffix). Tags are sorted by commit
    date with newest first.

    :param repo_path: Absolute path to git repository
    :type repo_path: Path
    :return: List of (tag_name, tag_date) tuples, newest first
    :rtype: List[Tuple[str, datetime]]

    :Example:

    >>> tags = get_tags(Path("/path/to/repo"))
    >>> tags[0]
    ('9.2.6', datetime(2025, 11, 15, 10, 30, 0))
    """
    repo = git.Repo(repo_path)
    tags_with_dates = []

    for tag in repo.tags:
        try:
            #: Get commit date from tag's commit object
            commit = tag.commit
            tag_date = datetime.fromtimestamp(commit.committed_date)

            #: Filter to semantic versioning pattern only
            if _is_semantic_version(tag.name):
                tags_with_dates.append((tag.name, tag_date))

        except Exception as e:
            #: Skip problematic tags with warning
            print(f"⚠️  Warning: Could not parse tag {tag.name}: {e}")
            continue

    #: Sort by date (newest first) - important for correct ordering
    tags_with_dates.sort(key=lambda x: x[1], reverse=True)

    return tags_with_dates


def fetch_repository(repo_path: Path) -> Tuple[bool, str]:
    """
    Fetch latest tags and commits from remote.

    Non-destructive operation that updates remote-tracking branches
    and tags without modifying the working directory.

    :param repo_path: Absolute path to git repository
    :type repo_path: Path
    :return: Tuple of (success: bool, message: str)
    :rtype: Tuple[bool, str]

    :Example:

    >>> success, msg = fetch_repository(Path("/path/to/repo"))
    >>> if success:
    ...     print(f"Success: {msg}")
    Success: Fetched 2 new tags
    """
    try:
        repo = git.Repo(repo_path)

        #: Check if remote exists
        if not repo.remotes:
            return False, "No remote configured - using local tags"

        #: Fetch tags and commits from origin
        origin = repo.remotes.origin
        fetch_info = origin.fetch(tags=True, prune=True)

        #: Count new tags fetched
        new_tags = sum(1 for info in fetch_info if 'tag' in str(info.ref))

        if new_tags > 0:
            return True, f"Fetched {new_tags} new tag{'s' if new_tags != 1 else ''}"
        else:
            return True, "Already up to date"

    except git.exc.GitCommandError as e:
        #: Handle git command failures (network, auth, etc.)
        if "Connection" in str(e) or "timeout" in str(e).lower():
            return False, "Fetch failed (network timeout) - using local tags"
        elif "Authentication" in str(e) or "Permission" in str(e):
            return False, "Fetch failed (auth required) - using local tags"
        else:
            return False, "Fetch failed - using local tags"
    except Exception as e:
        #: Catch-all for unexpected errors
        return False, "Fetch failed - using local tags"


def count_commits_between(
    repo_path: Path,
    from_tag: str,
    to_tag: str,
    return_dates: bool = False
) -> Union[int, Tuple[int, List[datetime]]]:
    """
    Count commits between two git references, optionally returning dates.

    Uses git range syntax (from_tag..to_tag) to count commits. The range
    excludes from_tag and includes to_tag, following git conventions.

    :param repo_path: Absolute path to git repository
    :type repo_path: Path
    :param from_tag: Older tag (excluded from count)
    :type from_tag: str
    :param to_tag: Newer tag (included in count)
    :type to_tag: str
    :param return_dates: If True, return (count, dates) tuple
    :type return_dates: bool
    :return: Commit count, or (count, dates) if return_dates=True
    :rtype: Union[int, Tuple[int, List[datetime]]]

    :Example:

    >>> count = count_commits_between(
    ...     Path("/path/to/repo"),
    ...     "9.2.5",
    ...     "9.2.6"
    ... )
    >>> count
    23
    >>> count, dates = count_commits_between(
    ...     Path("/path/to/repo"),
    ...     "9.2.5",
    ...     "9.2.6",
    ...     return_dates=True
    ... )
    >>> len(dates)
    23
    """
    repo = git.Repo(repo_path)

    try:
        #: Use git range syntax: from_tag..to_tag
        #: This excludes from_tag, includes to_tag
        commits = list(repo.iter_commits(f"{from_tag}..{to_tag}"))

        if return_dates:
            #: Extract commit dates from commit objects
            commit_dates = [
                datetime.fromtimestamp(commit.committed_date)
                for commit in commits
            ]
            return len(commits), commit_dates
        else:
            return len(commits)

    except git.GitCommandError as e:
        #: Handle git errors gracefully - return 0 and warn
        print(f"⚠️  Warning: Could not count commits {from_tag}..{to_tag}: {e}")
        return (0, []) if return_dates else 0


def should_exclude_file(filepath: str, exclusion_patterns: List[str]) -> bool:
    """
    Check if file matches any exclusion pattern.

    Supports wildcards and directory patterns:
    - Wildcards: *.lock, *.min.js
    - Directory patterns: node_modules/*, dist/*
    - Specific files: package-lock.json

    :param filepath: File path to check
    :type filepath: str
    :param exclusion_patterns: List of glob patterns to exclude
    :type exclusion_patterns: List[str]
    :return: True if file should be excluded
    :rtype: bool

    :Example:

    >>> should_exclude_file("package-lock.json", ["*.lock", "package-lock.json"])
    True
    >>> should_exclude_file("src/main.py", ["*.lock"])
    False
    """
    for pattern in exclusion_patterns:
        #: Check full path match
        if fnmatch.fnmatch(filepath, pattern):
            return True
        #: Check filename only match
        if fnmatch.fnmatch(filepath.split('/')[-1], pattern):
            return True

    return False


def calculate_line_changes(
    repo_path: Path,
    from_tag: str,
    to_tag: str,
    exclusions: List[str]
) -> Tuple[int, int]:
    """
    Calculate lines added and removed between two tags.

    Applies file exclusion patterns to filter out generated files,
    dependencies, and other unwanted files from line counts.

    :param repo_path: Absolute path to git repository
    :type repo_path: Path
    :param from_tag: Older tag
    :type from_tag: str
    :param to_tag: Newer tag
    :type to_tag: str
    :param exclusions: List of file patterns to exclude
    :type exclusions: List[str]
    :return: Tuple of (lines_added, lines_removed)
    :rtype: Tuple[int, int]

    :Example:

    >>> added, removed = calculate_line_changes(
    ...     Path("/path/to/repo"),
    ...     "9.2.5",
    ...     "9.2.6",
    ...     ["*.lock", "*.min.js"]
    ... )
    >>> added, removed
    (3245, 1102)
    """
    repo = git.Repo(repo_path)

    try:
        #: Get diff with numstat (shows additions/deletions per file)
        diff_output = repo.git.diff(from_tag, to_tag, numstat=True)

        lines_added = 0
        lines_removed = 0

        for line in diff_output.split('\n'):
            if not line.strip():
                continue

            parts = line.split('\t')
            if len(parts) < 3:
                continue

            added_str, removed_str, filepath = parts

            #: Apply exclusions
            if should_exclude_file(filepath, exclusions):
                continue

            try:
                #: Binary files show '-' for added/removed
                if added_str != '-':
                    lines_added += int(added_str)
                if removed_str != '-':
                    lines_removed += int(removed_str)
            except ValueError:
                #: Skip lines that can't be parsed
                continue

        return lines_added, lines_removed

    except git.GitCommandError as e:
        print(f"⚠️  Warning: Could not calculate line changes {from_tag}..{to_tag}: {e}")
        return 0, 0
