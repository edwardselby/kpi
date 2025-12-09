# Phase 1: Walking Skeleton (Core Data Flow)

## Purpose

Build the absolute minimum viable pipeline to prove git data extraction works. Console output only, hardcoded configuration, basic tag parsing and commit counting.

## Duration

1-2 days

## Philosophy

**"Make it work, then make it right, then make it fast"**

This phase focuses on **"make it work"** - prove the core concept functions before building infrastructure around it.

---

## Goals

- [x] Parse git tags from real repositories
- [x] Count commits between consecutive tags
- [x] Extract tag dates
- [x] Display results in readable console format
- [x] Hardcoded configuration (no YAML yet)
- [x] No changelog parsing (git only)
- [x] No HTML output (console only)

---

## Project Structure

```
kpi-reporter/
├── src/
│   ├── __init__.py
│   ├── main.py              # Simple orchestration (hardcoded)
│   └── git_analyzer.py      # Tag parsing + commit counting
├── tests/
│   ├── __init__.py
│   ├── test_git_analyzer.py
│   └── fixtures/
│       └── sample_repo/     # From Phase 0
├── requirements.txt
└── README.md
```

---

## Implementation Tasks

### Task 1.1: Project Setup

**Create basic structure:**

```bash
mkdir -p src tests/fixtures
touch src/__init__.py tests/__init__.py
touch src/main.py src/git_analyzer.py
touch tests/test_git_analyzer.py
```

**Create requirements.txt:**

```txt
GitPython==3.1.40
pytest==7.4.3
pytest-cov==4.1.0
```

**Install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Success Criteria:**
- Virtual environment created
- Dependencies installed
- Project structure ready

---

### Task 1.2: Implement Git Tag Parsing

**File:** `src/git_analyzer.py`

**Core function:**

```python
"""
Git repository analysis for KPI metrics.

This module extracts tag and commit information from git repositories.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
import git


def get_tags(repo_path: Path) -> List[Tuple[str, datetime]]:
    """
    Extract all tags from repository, sorted chronologically.

    Handles semantic versioning with or without 'v' prefix.
    Filters out non-version tags.

    :param repo_path: Path to git repository
    :type repo_path: Path
    :return: List of (tag_name, tag_date) tuples, newest first
    :rtype: List[Tuple[str, datetime]]

    :Example:

    >>> tags = get_tags(Path("../PyProjects/feed-orchestrator"))
    >>> tags[0]
    ('9.2.6', datetime(2025, 11, 15, 10, 30, 0))
    """
    repo = git.Repo(repo_path)

    tags_with_dates = []
    for tag in repo.tags:
        try:
            # Get tag commit date
            commit = tag.commit
            tag_date = datetime.fromtimestamp(commit.committed_date)

            # Normalize tag name (remove 'v' prefix if present)
            tag_name = tag.name
            if tag_name.startswith('v'):
                tag_name = tag_name[1:]

            # Filter to semantic versioning pattern
            # Accept: 9.2.6, 9.2.6-rc1
            if _is_semantic_version(tag_name):
                tags_with_dates.append((tag_name, tag_date))

        except Exception as e:
            # Skip problematic tags
            print(f"⚠️  Warning: Could not parse tag {tag.name}: {e}")
            continue

    # Sort by date (newest first)
    tags_with_dates.sort(key=lambda x: x[1], reverse=True)

    return tags_with_dates


def _is_semantic_version(tag_name: str) -> bool:
    """
    Check if tag matches semantic versioning pattern.

    Accepts: X.Y.Z or X.Y.Z-suffix

    :param tag_name: Tag name to validate
    :return: True if matches pattern
    """
    import re
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
    return bool(re.match(pattern, tag_name))
```

**Test implementation:**

```python
# tests/test_git_analyzer.py
import pytest
from pathlib import Path
from src.git_analyzer import get_tags, _is_semantic_version


def test_is_semantic_version():
    """Test semantic version pattern matching."""
    assert _is_semantic_version("1.2.3") is True
    assert _is_semantic_version("9.2.6") is True
    assert _is_semantic_version("1.2.3-rc1") is True
    assert _is_semantic_version("1.2.3-beta") is True

    assert _is_semantic_version("v1.2.3") is False
    assert _is_semantic_version("1.2") is False
    assert _is_semantic_version("release-1.2.3") is False
    assert _is_semantic_version("production") is False


def test_get_tags_with_fixture():
    """Test tag extraction from sample repository."""
    fixture_path = Path("tests/fixtures/sample_repo")

    if not fixture_path.exists():
        pytest.skip("Fixture repository not created yet")

    tags = get_tags(fixture_path)

    assert len(tags) > 0
    assert all(isinstance(tag, str) for tag, _ in tags)
    assert all(isinstance(date, datetime) for _, date in tags)

    # Verify chronological ordering (newest first)
    dates = [date for _, date in tags]
    assert dates == sorted(dates, reverse=True)
```

**Success Criteria:**
- Can parse tags from fixture repository
- Filters non-version tags
- Normalizes 'v' prefix
- Sorts chronologically
- Tests pass

---

### Task 1.3: Implement Commit Counting

**Add to:** `src/git_analyzer.py`

```python
def count_commits_between(
    repo_path: Path,
    from_ref: str,
    to_ref: str
) -> int:
    """
    Count commits between two git references.

    :param repo_path: Path to git repository
    :param from_ref: Starting reference (older)
    :param to_ref: Ending reference (newer)
    :return: Number of commits
    :rtype: int

    :Example:

    >>> count = count_commits_between(
    ...     Path("../PyProjects/feed-orchestrator"),
    ...     "9.2.5",
    ...     "9.2.6"
    ... )
    >>> count
    23
    """
    repo = git.Repo(repo_path)

    try:
        # Get commit range
        # Use .. syntax: from_ref..to_ref excludes from_ref, includes to_ref
        commits = list(repo.iter_commits(f"{from_ref}..{to_ref}"))
        return len(commits)

    except git.GitCommandError as e:
        print(f"⚠️  Warning: Could not count commits {from_ref}..{to_ref}: {e}")
        return 0
```

**Test implementation:**

```python
# tests/test_git_analyzer.py

def test_count_commits_between():
    """Test commit counting between tags."""
    fixture_path = Path("tests/fixtures/sample_repo")

    if not fixture_path.exists():
        pytest.skip("Fixture repository not created yet")

    # Should have commits between tags
    count = count_commits_between(fixture_path, "1.2.1", "1.2.2")
    assert count > 0

    # Same ref should be 0
    count = count_commits_between(fixture_path, "1.2.2", "1.2.2")
    assert count == 0


def test_count_commits_invalid_refs():
    """Test commit counting with invalid references."""
    fixture_path = Path("tests/fixtures/sample_repo")

    if not fixture_path.exists():
        pytest.skip("Fixture repository not created yet")

    # Invalid refs should return 0 and warn
    count = count_commits_between(fixture_path, "nonexistent", "1.2.2")
    assert count == 0
```

**Success Criteria:**
- Accurately counts commits between refs
- Handles invalid refs gracefully
- Returns 0 for same ref
- Tests pass

---

### Task 1.4: Create Console Output

**File:** `src/main.py`

```python
"""
KPI Report Generator - Phase 1 Walking Skeleton

Hardcoded console output to validate git data extraction.
"""

from pathlib import Path
from src.git_analyzer import get_tags, count_commits_between


def main():
    """
    Generate console report for hardcoded projects.

    Phase 1: Minimal viable output to prove concept.
    """
    # Hardcoded projects (from Phase 0 validation)
    projects = [
        Path("../PyProjects/feed-orchestrator"),
        Path("../PyProjects/betslip-service"),
        Path("../PyProjects/odds-engine"),
    ]

    print("=" * 60)
    print("KPI Report Generator - Phase 1 Walking Skeleton")
    print("=" * 60)
    print()

    for project_path in projects:
        if not project_path.exists():
            print(f"⚠️  SKIP: {project_path.name} (not found)")
            print()
            continue

        if not (project_path / ".git").exists():
            print(f"⚠️  SKIP: {project_path.name} (not a git repository)")
            print()
            continue

        print(f"📦 {project_path.name}")
        print("-" * 60)

        # Get tags
        tags = get_tags(project_path)

        if not tags:
            print("  ⚠️  No tags found")
            print()
            continue

        # Show last 5 releases
        for i, (tag, date) in enumerate(tags[:5]):
            if i == 0:
                # First tag (newest) - no previous to compare
                print(f"  {tag:15} {date.strftime('%Y-%m-%d')} (latest)")
                continue

            # Count commits since previous tag
            prev_tag = tags[i-1][0]
            commits = count_commits_between(project_path, tag, prev_tag)

            print(f"  {tag:15} {date.strftime('%Y-%m-%d')} → {commits:3d} commits")

        print()


if __name__ == "__main__":
    main()
```

**Expected output:**

```
============================================================
KPI Report Generator - Phase 1 Walking Skeleton
============================================================

📦 feed-orchestrator
------------------------------------------------------------
  9.2.6           2025-11-15 (latest)
  9.2.5           2025-10-12 →  23 commits
  9.2.4           2025-09-08 →  18 commits
  9.2.3           2025-08-15 →  15 commits
  9.2.2           2025-07-20 →  12 commits

📦 betslip-service
------------------------------------------------------------
  3.1.2           2025-11-20 (latest)
  3.1.1           2025-10-05 →  12 commits
  3.1.0           2025-09-10 →  25 commits
  3.0.9           2025-08-01 →   8 commits
  3.0.8           2025-07-15 →  10 commits

📦 odds-engine
------------------------------------------------------------
  2.4.5           2025-11-18 (latest)
  2.4.4           2025-10-22 →  15 commits
  2.4.3           2025-09-30 →  20 commits
  2.4.2           2025-09-05 →  11 commits
  2.4.1           2025-08-10 →   9 commits
```

**Success Criteria:**
- Runs without errors
- Shows tags for all valid projects
- Displays commit counts correctly
- Handles missing projects gracefully
- Output is readable and informative

---

### Task 1.5: Test with Real Repositories

**Manual testing:**

```bash
# Run the script
python -m src.main

# Verify output:
1. Do tag dates match git log?
   git log --tags --simplify-by-decoration --pretty="format:%ai %d"

2. Do commit counts match manual count?
   git log --oneline 9.2.5..9.2.6 | wc -l

3. Are projects handled correctly?
   - Existing projects show data
   - Missing projects show warning
   - Non-git directories show warning
```

**Create validation script:**

```python
# tests/test_integration.py
"""Integration tests against real repositories."""

import pytest
from pathlib import Path
from src.main import main
import sys
from io import StringIO


def test_main_execution():
    """Test that main() executes without errors."""
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        main()
        output = sys.stdout.getvalue()

        # Basic validation
        assert "KPI Report Generator" in output
        assert len(output) > 100  # Should have substantial output

    finally:
        sys.stdout = old_stdout


def test_real_repo_analysis():
    """Test analysis of a real repository (if available)."""
    project_path = Path("../PyProjects/feed-orchestrator")

    if not project_path.exists():
        pytest.skip("Real repository not available")

    from src.git_analyzer import get_tags, count_commits_between

    tags = get_tags(project_path)

    assert len(tags) > 0, "Should find tags in real repository"

    if len(tags) >= 2:
        # Test commit counting between real tags
        count = count_commits_between(project_path, tags[1][0], tags[0][0])
        assert count > 0, "Should find commits between consecutive tags"
```

**Success Criteria:**
- Script runs against real repositories
- Output matches manual verification
- Edge cases handled (missing projects, etc.)
- Integration tests pass

---

## Testing Strategy

### Unit Tests

```bash
pytest tests/test_git_analyzer.py -v
```

**Coverage:**
- Tag parsing
- Semantic version validation
- Commit counting
- Error handling

### Integration Tests

```bash
pytest tests/test_integration.py -v
```

**Coverage:**
- Full script execution
- Real repository analysis (if available)
- Output format validation

### Manual Validation

```bash
# Run against real repos
python -m src.main

# Verify specific project
cd ../PyProjects/feed-orchestrator
git log --oneline 9.2.5..9.2.6 | wc -l
# Compare with script output
```

---

## Exit Criteria

Before proceeding to Phase 2, verify:

- [ ] Can parse git tags from real repositories
- [ ] Accurately counts commits between tags
- [ ] Console output is clear and informative
- [ ] Handles edge cases (missing repos, no tags)
- [ ] All tests pass
- [ ] Code is clean and documented
- [ ] Validated against 2-3 real repositories
- [ ] Performance is acceptable (<5s for 3 repos)

---

## Known Limitations (Acceptable for Phase 1)

- **Hardcoded project list** - Will be config-driven in Phase 2
- **No changelog parsing** - Git data only
- **No line count metrics** - Just commit counts
- **No aggregation** - Shows per-project only
- **Console output only** - No HTML/PDF
- **No period filtering** - Shows all releases

These limitations are **intentional**. Phase 1 proves the core git integration works. Everything else builds on this foundation.

---

## Common Issues & Solutions

### Issue: GitPython not finding repository

**Symptom:** `InvalidGitRepositoryError`

**Solution:**
```python
# Verify path is correct
if not (repo_path / ".git").exists():
    print(f"Not a git repo: {repo_path}")
```

### Issue: Tags not sorted correctly

**Symptom:** Newest tag not first

**Solution:**
```python
# Sort by date, not version string
tags.sort(key=lambda x: x[1], reverse=True)
```

### Issue: Commit count is zero

**Symptom:** All commit counts show 0

**Solution:**
```python
# Check ref order (from older to newer)
commits = repo.iter_commits(f"{older_tag}..{newer_tag}")
```

### Issue: Non-version tags cause errors

**Symptom:** Parsing fails on `production` tag

**Solution:**
```python
# Filter with regex
if not _is_semantic_version(tag_name):
    continue
```

---

## Demo Checklist

At end of Phase 1, you should be able to:

- [ ] Run `python -m src.main`
- [ ] See output for multiple projects
- [ ] Show accurate commit counts
- [ ] Explain what each metric means
- [ ] Point to tests that validate correctness
- [ ] Discuss limitations and next steps

**Demo script:**

```
"This is Phase 1 - a walking skeleton that proves we can extract
git metrics from our microservices.

Running the script... [execute]

Here you can see we're analyzing 3 projects. For each release tag,
we're showing the date and commit count since the previous release.

For example, feed-orchestrator version 9.2.6 had 23 commits since 9.2.5.

The data comes directly from git - we're parsing tags and using
git log to count commits.

Next phase, we'll add changelog parsing, line counts, and configuration.
But this proves the core concept works."
```

---

## Next Phase

Once Phase 1 is complete and validated: **Phase 2 - Complete Data Collection**

Phase 2 adds:
- YAML configuration
- Changelog parsing
- Line count metrics
- File exclusions
- Warning system
- Data aggregation

---

## Time Box

**Maximum time:** 2 days

If git parsing takes longer than 2 days, that indicates either:
1. Assumption about git structure was wrong → revisit Phase 0
2. Technical complexity higher than expected → simplify scope
3. Getting stuck on details → move forward with working version

The goal is **working software**, not perfect code.
