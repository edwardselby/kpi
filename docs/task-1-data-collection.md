# Task 1: Data Collection & Analysis

## Overview

Implement the backend data collection and analysis components for the KPI Report Generator. This task focuses on extracting, parsing, and aggregating metrics from multiple microservice repositories.

## Scope

This task covers:
- Configuration management
- Project discovery and validation
- Changelog parsing
- Git history analysis
- Data aggregation and structuring

## Components to Implement

### 1. Configuration Manager (`src/config_manager.py`)

**Purpose:** Load and validate configuration from `config.yaml`

**Responsibilities:**
- Load YAML configuration file
- Validate required fields
- Provide typed access to configuration values
- Handle configuration errors gracefully

**Configuration Schema:**
```python
@dataclass
class Config:
    projects_directory: Path
    included_projects: List[str]
    file_exclusions: List[str]
    report_output: Path
    valid_branches: List[str]
```

**Key Methods:**
```python
def load_config(config_path: str = "config.yaml") -> Config:
    """Load and validate configuration from YAML file."""
    pass

def validate_config(config: Config) -> List[str]:
    """Validate configuration and return list of warnings/errors."""
    pass
```

---

### 2. Project Scanner (`src/project_scanner.py`)

**Purpose:** Discover and validate project repositories

**Responsibilities:**
- Scan projects directory for whitelisted projects
- Validate each project is a git repository
- Check current branch against valid branches
- Verify presence of git tags
- Report warnings for invalid states

**Data Model:**
```python
@dataclass
class ProjectInfo:
    name: str
    path: Path
    current_branch: str
    has_tags: bool
    is_valid_branch: bool
    warnings: List[str]
```

**Key Methods:**
```python
def scan_projects(config: Config) -> List[ProjectInfo]:
    """
    Scan projects directory and return validated project information.

    Warnings generated for:
    - Projects not on valid branches
    - Projects without git tags
    - Missing CHANGELOG.md files
    """
    pass

def is_git_repository(path: Path) -> bool:
    """Check if directory is a valid git repository."""
    pass

def get_current_branch(repo_path: Path) -> str:
    """Get current branch name for repository."""
    pass

def has_git_tags(repo_path: Path) -> bool:
    """Check if repository has any git tags."""
    pass
```

**Error Handling:**
- Skip projects that don't exist
- Skip projects that aren't git repositories
- Warn but continue for invalid branch states
- Warn but continue for missing tags

---

### 3. Changelog Parser (`src/changelog_parser.py`)

**Purpose:** Extract structured data from CHANGELOG.md files

**Responsibilities:**
- Parse Keep a Changelog format
- Extract version, date, and change type information
- Identify ticket references (IDT-*, SODA-*, GSWP-*)
- Handle malformed changelogs gracefully

**Data Model:**
```python
@dataclass
class ChangelogEntry:
    description: str
    change_type: str  # Added, Fixed, Changed, Removed
    tickets: List[str]  # IDT-123, SODA-456, etc.

@dataclass
class ChangelogRelease:
    version: str
    date: Optional[datetime]
    entries: List[ChangelogEntry]

@dataclass
class ProjectChangelog:
    project_name: str
    releases: List[ChangelogRelease]
    parse_warnings: List[str]
```

**Key Methods:**
```python
def parse_changelog(project_path: Path) -> Optional[ProjectChangelog]:
    """
    Parse CHANGELOG.md file following Keep a Changelog format.

    Returns None if CHANGELOG.md doesn't exist.
    Warns and attempts partial parse if malformed.
    """
    pass

def extract_ticket_references(text: str) -> List[str]:
    """Extract ticket references matching patterns: IDT-\d+, SODA-\d+, GSWP-\d+"""
    pass

def parse_version_header(line: str) -> Tuple[str, Optional[datetime]]:
    """
    Parse version header line.
    Expected format: ## [1.2.3] - 2025-11-15
    """
    pass

def categorize_change_type(line: str) -> Optional[str]:
    """
    Identify change type from section header.
    Returns: 'Added', 'Fixed', 'Changed', 'Removed', or None
    """
    pass
```

**Changelog Format Reference:**
```markdown
## [1.2.3] - 2025-11-15

### Added
- IDT-123 New feature for user authentication

### Fixed
- SODA-456 Fixed bug in payment processing
- IDT-789 Corrected timezone handling
```

---

### 4. Git Analyzer (`src/git_analyzer.py`)

**Purpose:** Extract commit and line-change metrics from git history

**Responsibilities:**
- Analyze commits between tags
- Calculate line changes (added/removed) with exclusions
- Count files changed
- Aggregate metrics by time period

**Data Model:**
```python
@dataclass
class TagMetrics:
    tag_name: str
    tag_date: datetime
    previous_tag: Optional[str]
    commits_count: int
    lines_added: int
    lines_removed: int
    files_changed: int

@dataclass
class ProjectGitMetrics:
    project_name: str
    tag_metrics: List[TagMetrics]
    warnings: List[str]
```

**Key Methods:**
```python
def analyze_repository(project_path: Path, file_exclusions: List[str]) -> ProjectGitMetrics:
    """
    Analyze git repository and extract metrics for all tags.

    For each tag:
    - Count commits since previous tag
    - Calculate line changes excluding patterns
    - Count files modified
    """
    pass

def get_tags_chronological(repo_path: Path) -> List[Tuple[str, datetime]]:
    """
    Get all tags sorted chronologically.
    Parses semantic versions: 9.2.6, 9.2.6-rc1
    """
    pass

def calculate_diff_metrics(
    repo: git.Repo,
    from_ref: str,
    to_ref: str,
    exclusions: List[str]
) -> Tuple[int, int, int]:
    """
    Calculate lines added, removed, and files changed between refs.

    Returns: (lines_added, lines_removed, files_changed)
    Applies exclusion patterns to filter out unwanted files.
    """
    pass

def should_exclude_file(filepath: str, exclusion_patterns: List[str]) -> bool:
    """Check if file matches any exclusion pattern."""
    pass

def count_commits_between(repo: git.Repo, from_ref: str, to_ref: str) -> int:
    """Count commits between two references."""
    pass
```

**Tag Format Handling:**
- Semantic versioning: `9.2.6`
- Optional suffix: `9.2.6-rc1`
- No `v` prefix
- Sort chronologically by date, not version string

**File Exclusions:**
Apply patterns from config:
- `*.lock`
- `package-lock.json`
- `*.min.js`
- `*.min.css`
- `*.generated.*`
- `node_modules/*`
- `migrations/*`

---

### 5. Data Aggregator (`src/data_aggregator.py`)

**Purpose:** Combine and aggregate metrics across projects and time periods

**Responsibilities:**
- Merge changelog and git metrics
- Filter by time period
- Calculate aggregate statistics
- Prepare data structure for report generation

**Data Model:**
```python
@dataclass
class AggregatedMetrics:
    period: str  # "2025-11", "2025-Q4", "all"
    total_releases: int
    total_commits: int
    total_lines_added: int
    total_lines_removed: int
    date_range: Tuple[datetime, datetime]

    projects: List[ProjectMetrics]
    change_type_distribution: Dict[str, int]  # "Added": 45, "Fixed": 30, etc.

@dataclass
class ProjectMetrics:
    project_name: str
    releases: int
    commits: int
    lines_added: int
    lines_removed: int
    change_types: Dict[str, int]
```

**Key Methods:**
```python
def aggregate_metrics(
    changelogs: List[ProjectChangelog],
    git_metrics: List[ProjectGitMetrics],
    period: str
) -> AggregatedMetrics:
    """
    Combine and aggregate metrics for specified time period.

    Period formats:
    - "2025-11" - Specific month
    - "2025-Q4" - Quarter
    - "all" - All time
    """
    pass

def filter_by_period(
    metrics: List[TagMetrics],
    period: str
) -> List[TagMetrics]:
    """Filter metrics to specified time period."""
    pass

def calculate_change_type_distribution(
    changelogs: List[ProjectChangelog]
) -> Dict[str, int]:
    """Aggregate change types across all projects."""
    pass

def get_month_over_month_comparison(
    current_period: AggregatedMetrics,
    previous_period: AggregatedMetrics
) -> Dict[str, Tuple[int, int]]:
    """
    Compare current period vs previous period.

    Returns: {
        "releases": (current, previous),
        "commits": (current, previous),
        "lines_changed": (current, previous)
    }
    """
    pass
```

---

## Implementation Requirements

### Testing Strategy

**Test Coverage Required:**
1. **Configuration Manager**
   - Valid YAML parsing
   - Missing required fields
   - Invalid path values
   - Malformed YAML

2. **Project Scanner**
   - Valid git repositories
   - Non-git directories
   - Missing projects
   - Invalid branch states
   - Missing tags

3. **Changelog Parser**
   - Standard Keep a Changelog format
   - Missing sections
   - Malformed dates
   - Multiple ticket references
   - Various change types

4. **Git Analyzer**
   - Tag parsing and sorting
   - Diff calculation with exclusions
   - Commit counting
   - Edge case: single tag
   - Edge case: no tags

5. **Data Aggregator**
   - Period filtering (month, quarter, all)
   - Cross-project aggregation
   - Month-over-month comparison
   - Empty datasets

### Error Handling

**Critical Errors (Exit):**
- Config file not found
- Projects directory doesn't exist
- No valid projects found

**Warnings (Continue):**
- Project not on valid branch
- Missing CHANGELOG.md
- Malformed changelog entries
- No git tags in project
- Parse errors in individual entries

### Code Quality

- Type hints for all functions
- Docstrings following ReStructuredText format
- Comprehensive error messages
- Logging for debugging (use Python `logging` module)
- Modular, testable functions

### Dependencies

```txt
GitPython>=3.1.40
PyYAML>=6.0.1
python-dateutil>=2.8.2
```

---

## Output Specification

The data collection phase should produce structured data ready for report generation:

```python
@dataclass
class CollectedData:
    """Complete dataset for report generation."""
    config: Config
    projects: List[ProjectInfo]
    changelogs: List[ProjectChangelog]
    git_metrics: List[ProjectGitMetrics]
    aggregated: AggregatedMetrics
    warnings: List[str]  # All warnings encountered
```

This structure will be passed to Task 2 (Report Generation) components.

---

## Directory Structure

```
src/
├── __init__.py
├── config_manager.py      # Configuration loading and validation
├── project_scanner.py     # Project discovery and validation
├── changelog_parser.py    # CHANGELOG.md parsing
├── git_analyzer.py        # Git metrics extraction
└── data_aggregator.py     # Metric aggregation and filtering
```

---

## Testing Structure

```
tests/
├── __init__.py
├── test_config_manager.py
├── test_project_scanner.py
├── test_changelog_parser.py
├── test_git_analyzer.py
├── test_data_aggregator.py
└── fixtures/
    ├── sample_config.yaml
    ├── sample_changelog.md
    └── sample_repo/  # Mock git repository
```

---

## Validation Checklist

Before considering Task 1 complete:

- [ ] All five components implemented with type hints
- [ ] Comprehensive test suite (90%+ coverage)
- [ ] All critical errors handled with clear messages
- [ ] All warnings logged with actionable information
- [ ] Documentation for all public functions
- [ ] Sample test data created
- [ ] Integration test validating full data collection pipeline
- [ ] Code reviewed for security (path traversal, command injection)
- [ ] Performance tested with 20+ projects

---

## Example Usage

```python
from src.config_manager import load_config
from src.project_scanner import scan_projects
from src.changelog_parser import parse_changelog
from src.git_analyzer import analyze_repository
from src.data_aggregator import aggregate_metrics

# Load configuration
config = load_config("config.yaml")

# Scan projects
projects = scan_projects(config)

# Collect changelog data
changelogs = [
    parse_changelog(project.path)
    for project in projects
    if parse_changelog(project.path) is not None
]

# Collect git metrics
git_metrics = [
    analyze_repository(project.path, config.file_exclusions)
    for project in projects
]

# Aggregate for reporting period
aggregated = aggregate_metrics(changelogs, git_metrics, period="2025-11")

print(f"Total releases: {aggregated.total_releases}")
print(f"Total commits: {aggregated.total_commits}")
print(f"Lines changed: {aggregated.total_lines_added + aggregated.total_lines_removed}")
```

---

## Notes for Implementation

1. **Git Operations:** Use GitPython library for all git interactions
2. **Date Parsing:** Handle multiple date formats in changelogs gracefully
3. **Performance:** Lazy load git data to avoid memory issues with large repos
4. **Logging:** Use structured logging for debugging production issues
5. **Idempotency:** All parsing functions should be pure (no side effects)

---

## Dependencies on Task 2

Task 2 (Report Generation) will consume the `CollectedData` structure produced by this task. Ensure the data model is complete and well-documented.
