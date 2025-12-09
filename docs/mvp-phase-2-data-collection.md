# Phase 2: Complete Data Collection

## Purpose

Build comprehensive data collection layer with all metrics: changelog parsing, line counts, file exclusions, configuration management, and cross-project aggregation.

## Duration

3-4 days

## Dependencies

- Phase 1 complete (git tag parsing and commit counting working)
- Phase 0 findings documented (edge cases known)

---

## Goals

- [x] YAML configuration management
- [x] Full changelog parsing (Keep a Changelog format)
- [x] Line count metrics with file exclusions
- [x] Project scanning and validation
- [x] Comprehensive warning system
- [x] Data aggregation across projects
- [x] Period filtering (month, quarter, all)
- [x] 90%+ test coverage

---

## Enhanced Project Structure

```
kpi-reporter/
├── config.yaml              # NEW: Configuration file
├── src/
│   ├── __init__.py
│   ├── main.py              # ENHANCED: Use config, show aggregates
│   ├── git_analyzer.py      # ENHANCED: Add line counts
│   ├── config_manager.py    # NEW: YAML loading
│   ├── project_scanner.py   # NEW: Project discovery
│   ├── changelog_parser.py  # NEW: Changelog parsing
│   └── data_aggregator.py   # NEW: Cross-project metrics
├── tests/
│   ├── test_config_manager.py
│   ├── test_project_scanner.py
│   ├── test_changelog_parser.py
│   ├── test_git_analyzer.py         # ENHANCED
│   ├── test_data_aggregator.py
│   └── fixtures/
│       ├── sample_config.yaml
│       ├── sample_changelog.md
│       └── sample_repo/
└── requirements.txt         # UPDATED: Add PyYAML
```

---

## Implementation Tasks

### Task 2.1: Configuration Manager

**File:** `src/config_manager.py`

**Implementation:** See Task 1 document (`docs/task-1-data-collection.md`) for complete specification.

**Key points:**
- Load `config.yaml` using PyYAML
- Validate required fields
- Provide typed Config dataclass
- Handle missing files gracefully

**Test coverage:**
- Valid config loading
- Missing file error
- Invalid YAML error
- Missing required fields

**Success criteria:**
- Can load sample config
- Validation catches errors
- Clear error messages

---

### Task 2.2: Changelog Parser

**File:** `src/changelog_parser.py`

**Implementation:** See Task 1 document for complete specification.

**Core functionality:**

```python
@dataclass
class ChangelogEntry:
    description: str
    change_type: str  # Added, Fixed, Changed, Removed
    tickets: List[str]

@dataclass
class ChangelogRelease:
    version: str
    date: Optional[datetime]
    entries: List[ChangelogEntry]

def parse_changelog(project_path: Path) -> Optional[ProjectChangelog]:
    """Parse CHANGELOG.md following Keep a Changelog format."""
    pass

def extract_ticket_references(text: str) -> List[str]:
    """Extract IDT-*, SODA-*, GSWP-* patterns."""
    pass
```

**Edge cases to handle:**
- Missing dates: `## [1.2.3]` (no date)
- Unreleased section: `## [Unreleased]`
- Malformed entries
- Multiple ticket references per line
- Various change type headers

**Test coverage:**
- Standard changelog format
- Missing sections
- Malformed dates
- Ticket extraction (multiple patterns)
- Edge cases from Phase 0 audit

**Success criteria:**
- Parses fixture changelog correctly
- Extracts all change types
- Identifies all ticket references
- Handles edge cases with warnings

---

### Task 2.3: Enhanced Git Analyzer (Line Counts)

**File:** `src/git_analyzer.py` (ENHANCED)

**Add line count calculation:**

```python
def calculate_diff_metrics(
    repo: git.Repo,
    from_ref: str,
    to_ref: str,
    exclusions: List[str]
) -> Tuple[int, int, int]:
    """
    Calculate lines added, removed, and files changed.

    Applies exclusion patterns to filter unwanted files.

    :return: (lines_added, lines_removed, files_changed)
    """
    diff = repo.git.diff(
        from_ref, to_ref,
        numstat=True
    )

    lines_added = 0
    lines_removed = 0
    files_changed = 0

    for line in diff.split('\n'):
        if not line.strip():
            continue

        parts = line.split('\t')
        if len(parts) < 3:
            continue

        added, removed, filepath = parts

        # Apply exclusions
        if should_exclude_file(filepath, exclusions):
            continue

        try:
            lines_added += int(added) if added != '-' else 0
            lines_removed += int(removed) if removed != '-' else 0
            files_changed += 1
        except ValueError:
            # Binary files show '-' for added/removed
            files_changed += 1

    return lines_added, lines_removed, files_changed


def should_exclude_file(filepath: str, exclusion_patterns: List[str]) -> bool:
    """
    Check if file matches any exclusion pattern.

    Supports:
    - Wildcards: *.lock
    - Directory patterns: node_modules/*
    - Specific files: package-lock.json
    """
    import fnmatch

    for pattern in exclusion_patterns:
        if fnmatch.fnmatch(filepath, pattern):
            return True
        if fnmatch.fnmatch(filepath.split('/')[-1], pattern):
            return True

    return False
```

**Test coverage:**
- Line count calculation
- File exclusion matching
- Binary file handling
- Multiple exclusion patterns
- Edge cases (no changes, massive changes)

**Success criteria:**
- Accurate line counts
- Exclusions filter correctly
- Binary files don't break parsing
- Performance acceptable (large diffs)

---

### Task 2.4: Project Scanner

**File:** `src/project_scanner.py`

**Implementation:** See Task 1 document for complete specification.

**Core functionality:**

```python
@dataclass
class ProjectInfo:
    name: str
    path: Path
    current_branch: str
    has_tags: bool
    has_changelog: bool
    is_valid_branch: bool
    warnings: List[str]

def scan_projects(config: Config) -> List[ProjectInfo]:
    """
    Scan projects directory for whitelisted projects.

    Validates each project and collects warnings.
    """
    pass
```

**Validation checks:**
- Is git repository
- Has tags
- Has CHANGELOG.md
- On valid branch (main/dev)

**Test coverage:**
- Valid projects
- Missing directories
- Non-git directories
- Invalid branch states
- Missing changelogs

**Success criteria:**
- Discovers all whitelisted projects
- Collects all warnings
- Skips invalid projects gracefully

---

### Task 2.5: Data Aggregator

**File:** `src/data_aggregator.py`

**Implementation:** See Task 1 document for complete specification.

**Core functionality:**

```python
@dataclass
class AggregatedMetrics:
    period: str
    total_releases: int
    total_commits: int
    total_lines_added: int
    total_lines_removed: int
    date_range: Tuple[datetime, datetime]
    projects: List[ProjectMetrics]
    change_type_distribution: Dict[str, int]

def aggregate_metrics(
    changelogs: List[ProjectChangelog],
    git_metrics: List[ProjectGitMetrics],
    period: str
) -> AggregatedMetrics:
    """Aggregate metrics across all projects for period."""
    pass

def filter_by_period(
    metrics: List[TagMetrics],
    period: str
) -> List[TagMetrics]:
    """
    Filter metrics to time period.

    Supported periods:
    - "2025-11" - Specific month
    - "2025-Q4" - Quarter (Oct-Dec)
    - "all" - All time
    """
    pass
```

**Test coverage:**
- Month filtering
- Quarter filtering
- All-time aggregation
- Empty datasets
- Cross-project totals
- Change type distribution

**Success criteria:**
- Correct period filtering
- Accurate aggregation
- Handles empty data
- Performance with 20+ projects

---

### Task 2.6: Enhanced Main Script

**File:** `src/main.py` (ENHANCED)

**Updates:**
- Load configuration from YAML
- Use project scanner
- Parse changelogs and git metrics
- Aggregate across projects
- Display comprehensive console output

**Sample output:**

```
============================================================
KPI Report Generator - Data Collection Phase
============================================================

Configuration loaded: config.yaml
  Projects directory: ../PyProjects
  Whitelisted projects: 8
  File exclusions: 6 patterns

Scanning projects...
  ✓ feed-orchestrator
  ✓ betslip-service
  ✓ odds-engine
  ⚠️  legacy-service (not on valid branch: feature/update)
  ✓ payment-service
  ✓ auth-service
  ✓ notification-service
  ⚠️  new-service (no git tags found)

Found 8 projects (6 valid, 2 with warnings)

Parsing changelogs...
  ✓ feed-orchestrator: 47 releases
  ✓ betslip-service: 30 releases
  ⚠️  odds-engine: CHANGELOG.md missing date in v2.3.1
  ...

Analyzing git repositories...
  ✓ feed-orchestrator: 47 tags analyzed
  ✓ betslip-service: 30 tags analyzed
  ...

Aggregating metrics for period: 2025-11
============================================================

SUMMARY METRICS (November 2025)
------------------------------------------------------------
Total Releases:      23
Total Commits:       156
Lines Added:         8,453
Lines Removed:       3,210
Net Lines Changed:   5,243

CHANGE TYPE DISTRIBUTION
------------------------------------------------------------
Fixed:               45 (38%)
Added:               35 (30%)
Changed:             25 (21%)
Removed:             13 (11%)

TICKET REFERENCES
------------------------------------------------------------
Total tickets:       72
IDT tickets:         45
SODA tickets:        18
GSWP tickets:        9

PER-PROJECT BREAKDOWN
------------------------------------------------------------
Project                 Releases  Commits  Lines+    Lines-
feed-orchestrator            5       47    3,200     1,100
betslip-service              2       12      800       200
odds-engine                  3       25    1,500       450
payment-service              4       31    1,800       720
auth-service                 3       18      650       340
notification-service         6       23    1,503       400

⚠️  WARNINGS (3)
------------------------------------------------------------
  - legacy-service not on valid branch (currently: feature/update)
  - new-service has no git tags
  - odds-engine CHANGELOG.md malformed date in v2.3.1
```

**Success criteria:**
- Loads config correctly
- Scans all projects
- Parses changelogs and git data
- Aggregates accurately
- Displays warnings clearly
- Performance <30s for 8 projects

---

## Configuration File

**File:** `config.yaml`

**Based on Phase 0 findings:**

```yaml
# KPI Report Generator Configuration

# Path to directory containing all project repositories
projects_directory: ../PyProjects

# Whitelist of projects to include (by directory name)
included_projects:
  - feed-orchestrator
  - betslip-service
  - odds-engine
  - payment-service
  - auth-service
  - notification-service
  - legacy-service    # Will warn: not on valid branch
  - new-service       # Will warn: no tags

# Files/patterns to exclude from line count metrics
file_exclusions:
  - "*.lock"
  - "package-lock.json"
  - "yarn.lock"
  - "*.min.js"
  - "*.min.css"
  - "*.generated.*"
  - "node_modules/*"
  - "migrations/*"

# Output directory for generated reports
report_output: ./reports

# Valid branches (warn if project is not on one of these)
valid_branches:
  - main
  - dev
```

---

## Testing Strategy

### Unit Tests (Per Component)

```bash
pytest tests/test_config_manager.py -v
pytest tests/test_changelog_parser.py -v
pytest tests/test_git_analyzer.py -v
pytest tests/test_project_scanner.py -v
pytest tests/test_data_aggregator.py -v
```

**Target: 90%+ coverage per module**

### Integration Tests

```bash
pytest tests/test_integration.py -v
```

**Scenarios:**
- Full pipeline with fixture data
- Multiple projects with mixed states
- Period filtering
- Error handling

### Manual Validation

```bash
# Run against real projects
python -m src.main

# Verify specific metrics
cd ../PyProjects/feed-orchestrator
git diff --numstat 9.2.5 9.2.6 | awk '{added+=$1; removed+=$2} END {print "Added:", added, "Removed:", removed}'

# Compare with script output
```

---

## Exit Criteria

Before proceeding to Phase 3:

- [ ] All 5 new components implemented
- [ ] Configuration loaded from YAML
- [ ] Changelog parsing works with real changelogs
- [ ] Line counts match manual verification
- [ ] File exclusions filter correctly
- [ ] Project scanner finds all projects
- [ ] Warning system captures all edge cases
- [ ] Data aggregator calculates correct totals
- [ ] Period filtering works (month, quarter, all)
- [ ] Test coverage >90%
- [ ] Performance acceptable (<30s for 8 projects)
- [ ] Console output is comprehensive and clear
- [ ] All Phase 0 edge cases handled

---

## Common Issues & Solutions

### Issue: YAML parsing errors

**Solution:**
```python
try:
    config = yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f"Error parsing config: {e}")
    sys.exit(1)
```

### Issue: Changelog date parsing fails

**Solution:**
```python
# Support multiple date formats
from dateutil import parser
try:
    date = parser.parse(date_string)
except:
    warnings.append(f"Could not parse date: {date_string}")
    date = None
```

### Issue: Line counts way too high

**Solution:**
```python
# Check exclusions are working
print(f"Excluded: {excluded_files}")
print(f"Included: {included_files}")

# Verify exclusion patterns
for pattern in exclusions:
    print(f"Pattern {pattern} matches: {matched_files}")
```

### Issue: Performance slow with large repos

**Solution:**
```python
# Cache git operations
@lru_cache(maxsize=128)
def get_diff_for_range(repo_path, from_ref, to_ref):
    ...

# Or process projects in parallel
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(analyze_project, projects)
```

---

## Demo Checklist

At end of Phase 2, you should be able to:

- [ ] Run `python -m src.main`
- [ ] Show configuration being loaded
- [ ] Display metrics for all projects
- [ ] Show aggregated totals
- [ ] Explain changelog parsing
- [ ] Demonstrate file exclusions working
- [ ] Show warning system catching issues
- [ ] Filter by different periods
- [ ] Run test suite and show coverage

**Demo script:**

```
"Phase 2 adds comprehensive data collection. Everything is now
configurable via config.yaml - no more hardcoded values.

Running the script... [execute]

Notice it's loading configuration, scanning 8 projects, and parsing
both changelogs and git history.

The summary shows aggregated metrics across all projects for November.
We processed 156 commits and changed over 11,000 lines of code.

The change type distribution shows most work was bug fixes (38%),
which aligns with this being a maintenance sprint.

Down here you can see per-project breakdowns and warnings for
projects with issues like missing tags or wrong branches.

Next phase adds HTML reports and charts for management presentation."
```

---

## Next Phase

**Phase 3: Basic Reporting**

Adds:
- HTML template (tables only)
- Jinja2 rendering
- File output
- CLI interface
- Professional presentation

---

## Time Box

**Maximum time:** 4 days

If implementation takes longer:
1. Reduce test coverage target (80% acceptable)
2. Skip period filtering (add in Phase 3)
3. Simplify changelog parsing (basic version info only)

The goal is **functional data collection**, not perfect parsing.
