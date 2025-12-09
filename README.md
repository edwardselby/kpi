# KPI Report Generator

**Phase 4: Data Visualization with Charts**

A git metrics extraction tool that generates professional KPI reports from multiple microservice repositories. Analyzes release history, commit counts, and line changes with **console output, HTML reports, and embedded data visualizations**.

---

## Current Status: Phase 4 Complete ✅

**Implemented Features:**
- ✅ Git tag parsing (semantic versioning)
- ✅ Commit counting between releases
- ✅ Line change tracking (added/removed) with file exclusions
- ✅ YAML configuration for project management
- ✅ Console-based reporting for multiple microservices
- ✅ Professional HTML reports with Jinja2 templates
- ✅ CLI arguments for output format and period selection
- ✅ Print/PDF-ready HTML with embedded CSS
- ✅ **Matplotlib-based charts and visualizations** 🆕
- ✅ **Project breakdown bar charts** 🆕
- ✅ **Release timeline visualization** 🆕
- ✅ **Summary metrics charts** 🆕
- ✅ 74% test coverage (100% on chart_generator.py)
- ✅ Handles 334+ tags across repositories

**Example Usage:**
This tool works with any collection of git repositories using semantic versioning.
Configure your repositories in `config.yaml` or `config.local.yaml` to get started.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Git repositories to analyze
- Virtual environment (recommended)

### Installation

```bash
# Navigate to project
cd /path/to/your/kpi-report-generator

# Activate virtual environment
source .venv/bin/activate

# Install package in development mode (enables 'kpi' command)
pip install -e .
```

**What this does:**
- Installs all dependencies from requirements.txt
- Creates a `kpi` console command (no need for `python -m src.main`)
- Package is installed in "editable" mode (changes take effect immediately)

### Configuration

The tool uses a hierarchical configuration system:
1. **config.local.yaml** (if exists) - Your private organization configuration
2. **config.yaml** (fallback) - Public template with generic examples

#### Option 1: Use config.local.yaml (Recommended for Organizations)

```bash
# Copy the template
cp config.yaml config.local.yaml

# Edit with your organization's services
nano config.local.yaml

# config.local.yaml is gitignored - safe for private data
kpi --html
```

#### Option 2: Edit config.yaml directly

Edit `config.yaml` to specify which projects to analyze:

```yaml
# Path to directory containing repositories
projects_directory: ./projects

# Projects to include (whitelist)
included_projects:
  - api-gateway-service
  - user-service
  - payment-service

# Files to exclude from line counts
file_exclusions:
  - "*.lock"
  - "*.min.js"
  - "node_modules/*"
  - "dist/*"
```

### Usage

#### Console Output (Default)

```bash
# Generate console report (using kpi command)
kpi

# Or use the module path (if not installed)
python -m src.main
```

**Sample Console Output:**

```
======================================================================
KPI Report Generator - Phase 2 with Line Metrics
======================================================================

Configuration: config.yaml
Projects directory: /Users/edward/PycharmProjects
Analyzing 3 projects...

📦 api-gateway-service
----------------------------------------------------------------------
  2.1.0        2025-12-02 (latest)
  2.0.5        2025-10-23 →  45 commits  (+8,234 / -342 lines)
  2.0.4        2025-10-23 →   3 commits  (+512 / -28 lines)
  2.0.0        2025-10-15 →  12 commits  (+2,145 / -623 lines)

📦 user-service
----------------------------------------------------------------------
  3.2.1        2025-11-15 (latest)
  3.2.0        2025-10-22 →  18 commits  (+1,432 / -156 lines)
  3.1.2        2025-10-01 →   5 commits  (+234 / -12 lines)
  3.1.0        2025-09-25 →  22 commits  (+3,156 / -892 lines)
```

#### HTML Output 🆕

```bash
# Generate HTML report for all time
kpi --html

# Generate HTML report for specific period
kpi --html --period 2025-11

# Specify custom output directory
kpi --html -o ./custom-reports

# Get help
kpi --help

# Check version
kpi --version
```

**Output:**
```
✅ HTML report generated: reports/kpi-report-all.html
   Open in browser: file:///path/to/kpi-report-generator/reports/kpi-report-all.html
```

**HTML Report Features:**
- 📊 **Summary Cards**: Total releases, commits, lines added/removed
- 📊 **Visual Charts**: 6 embedded charts showing activity, volume, and comparisons
- 📋 **Per-Service Breakdown**: Tabular view with metrics for each service
- 📜 **Complete Release History**: All releases with dates and metrics
- 🎨 **Professional Styling**: Gradient headers, card layouts, responsive tables
- 🖨️ **Print-Ready**: Optimized for PDF export with page breaks
- 🔗 **No External Dependencies**: All CSS and charts embedded in single HTML file

**To View:**
```bash
# Open in default browser (macOS)
open reports/kpi-report-all.html

# Open in default browser (Linux)
xdg-open reports/kpi-report-all.html

# Or navigate directly in any browser
```

**To Print/Export as PDF:**
1. Open HTML report in browser
2. File → Print (or Cmd/Ctrl+P)
3. Select "Save as PDF" as destination
4. Report layout automatically optimized for print

---

## Testing

The test suite includes both fast unit tests (with mocks) and slower integration tests (with real operations).

### Quick Unit Tests (Default - ~1 second)

```bash
# Run unit tests only (default behavior)
pytest tests/

# With verbose output
pytest tests/ -v
```

Unit tests use mocks to avoid slow operations like git commands and matplotlib rendering. They verify logic and behavior without actual I/O.

### Full Integration Tests (Slow - ~3 minutes)

```bash
# Run integration tests that use real git/matplotlib operations
pytest tests/ -m integration -v
```

Integration tests verify actual file creation, git operations, and chart rendering.

### All Tests

```bash
# Run both unit and integration tests
pytest tests/ -m "" -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=term --cov-report=html -m ""

# View HTML coverage report
open htmlcov/index.html
```

### Test Results

- ✅ 33 tests passing
- ✅ 74% overall coverage
- ✅ 100% coverage on chart_generator.py (visualization) 🆕
- ✅ 89% coverage on git_analyzer.py (core logic)
- ✅ 88% coverage on config_manager.py
- ✅ All edge cases handled

---

## Project Structure

```
kpi-report-generator/
├── config.yaml              # Project configuration
├── src/
│   ├── __init__.py
│   ├── git_analyzer.py      # Core git operations + line counting
│   ├── config_manager.py    # YAML configuration loading
│   ├── chart_generator.py   # 🆕 Matplotlib chart generation
│   ├── report_generator.py  # HTML report generation with charts
│   └── main.py              # Console/HTML output orchestration
├── templates/               # Jinja2 templates
│   └── report.html          # Professional HTML report template
├── reports/                 # Generated HTML reports
│   ├── kpi-report-all.html  # Example HTML output (all releases)
│   └── .charts/             # Generated chart images (6 total)
│       ├── release-activity-all.png           # Release activity (Releases + Commits)
│       ├── code-volume-all.png                # Code volume (Lines ± Net Change)
│       ├── project-total_commits-all.png      # Commits by service
│       ├── project-total_lines_added-all.png  # Lines added by service
│       ├── project-net_change-all.png         # Net change by service
│       └── timeline-all.png                   # Release timeline
├── tests/
│   ├── __init__.py
│   ├── test_git_analyzer.py        # Git operations tests
│   ├── test_git_analyzer_phase2.py # Line counting tests
│   ├── test_config_manager.py      # Config tests
│   ├── test_chart_generator.py     # 🆕 Chart generation tests
│   ├── test_integration.py         # Integration tests
│   └── fixtures/
│       └── sample_repo/            # Test git repository
├── docs/                    # Complete MVP documentation
├── requirements.txt         # Updated dependencies (includes matplotlib)
└── README.md
```

---

## New Features in Phase 2

### 1. Line Change Tracking

Track lines added and removed for each release:

```python
from src.git_analyzer import calculate_line_changes

added, removed = calculate_line_changes(
    repo_path,
    "9.0.2",
    "9.2.5",
    ["*.lock", "*.min.js", "node_modules/*"]
)
# Returns: (13221, 485)
```

**Key Features:**
- Excludes unwanted files (lock files, minified JS, node_modules, etc.)
- Handles binary files gracefully
- Formatted output with thousands separators
- Filters per-project via configuration

### 2. YAML Configuration

Centralized configuration for all settings:

```yaml
projects_directory: /Users/edward/PycharmProjects
included_projects:
  - project-1
  - project-2
file_exclusions:
  - "*.lock"
  - "node_modules/*"
valid_branches:
  - main
  - dev
```

**Benefits:**
- No hardcoded paths in code
- Easy to add/remove projects
- Configurable exclusion patterns
- Supports multiple environments

### 3. File Exclusion System

Smart filtering to exclude irrelevant files:

```python
# Exclude patterns support:
- Wildcards: *.lock, *.min.js
- Directories: node_modules/*, dist/*
- Specific files: package-lock.json
```

**Default Exclusions:**
- `*.lock` - Lock files
- `*.min.js`, `*.min.css` - Minified files
- `node_modules/*` - Dependencies
- `dist/*`, `build/*` - Build artifacts
- `migrations/*` - Database migrations

---

## New Features in Phase 3

### 1. HTML Report Generation

Generate professional, print-ready HTML reports:

```bash
python -m src.main --html --period all
```

**Features:**
- **Jinja2 Templating**: Flexible, maintainable template system
- **Embedded CSS**: No external dependencies, works offline
- **Responsive Design**: Adapts to different screen sizes
- **Print Optimization**: Page breaks, optimized layouts for PDF export
- **Professional Styling**: Gradient headers, card layouts, hover effects

### 2. CLI Arguments

Control output format and period via command-line:

```bash
# Console output (default)
python -m src.main

# HTML report for all time
python -m src.main --html

# HTML report for specific period
python -m src.main --html --period 2025-11

# Custom output directory
python -m src.main --html --output ./reports
```

**Available Arguments:**
- `--html` - Generate HTML report instead of console output
- `--period PERIOD` - Reporting period: YYYY-MM, YYYY-QN, or 'all' (default: all)
- `--output DIR` - Output directory for HTML reports (overrides config)

### 3. Professional Template Design

**Template Components:**

1. **Header Section**
   - Gradient background (purple/blue)
   - Report title and metadata
   - Period and generation date

2. **Summary Cards**
   - Total releases across all services
   - Total commits
   - Lines added (formatted with commas)
   - Lines removed (formatted with commas)
   - Responsive grid layout

3. **Per-Service Breakdown Table**
   - Service name
   - Release count (last 5)
   - Total commits
   - Lines added/removed
   - Net change calculation

4. **Detailed Release History**
   - Separate table per service
   - Version, date, commits, lines changed
   - Hover effects for better readability

5. **Footer**
   - Generator information
   - Timestamp

**Template Location:** `templates/report.html`

### 4. Report Data Pipeline

**Data Flow:**
```
Git Repos → collect_metrics_data() → projects_data
                                         ↓
                           generate_html_report()
                                         ↓
                           _prepare_report_data()  [Calculate totals]
                                         ↓
                           _render_template()      [Jinja2]
                                         ↓
                           _save_report()          [Write HTML]
                                         ↓
                           reports/kpi-report-{period}.html
```

**Key Functions in `report_generator.py`:**

1. **`generate_html_report()`** - Main entry point
2. **`_prepare_report_data()`** - Aggregate totals, format dates
3. **`_render_template()`** - Load and render Jinja2 template
4. **`_save_report()`** - Write HTML to file with proper naming

---

## New Features in Phase 4

### 1. Data Visualization with Matplotlib

Generate professional static charts embedded in HTML reports:

```bash
python -m src.main --html
# Charts automatically generated and embedded in HTML
```

**Chart Types:**

1. **Release Activity Chart** - Bar chart showing total releases and commits (comparable scale)
2. **Code Volume Chart** - Bar chart showing lines added, removed, and net change (comparable scale)
3. **Project Breakdown Charts** - Horizontal bar charts comparing services by metric (commits, lines, net change)
4. **Release Timeline** - Timeline showing release activity over time grouped by month

**Key Features:**
- **Static PNG Images**: Print/PDF-friendly, no JavaScript required
- **Consistent Styling**: Matches HTML report color scheme
- **High DPI (150)**: Professional quality for presentations
- **Automatic Sorting**: Projects ranked by metric value
- **Top Performer Highlighting**: Best-performing service highlighted in green

### 2. Chart Generator Module

**File:** `src/chart_generator.py`

Core functions:

```python
def generate_project_breakdown_chart(projects, metric, period, output_path):
    """Creates horizontal bar chart comparing services."""

def generate_timeline_chart(timeline_data, period, output_path):
    """Creates timeline showing releases over time."""

def generate_summary_comparison_chart(summary_data, period, output_path):
    """Creates bar chart showing summary metrics."""
```

**Styling Configuration:**
- Seaborn darkgrid theme
- 10x6 figure size (150 DPI)
- Color palette matching HTML report
- Value labels on all bars

### 3. Integrated Chart Generation

Charts are generated automatically when creating HTML reports:

**Data Flow:**
```
1. Collect metrics → projects_data
2. Call report_generator.py
   ↓
3. _prepare_report_data() - Calculate totals
   ↓
4. _generate_all_charts() - Create 5 PNG files
   ↓
5. _render_template() - Embed chart paths
   ↓
6. HTML report with embedded <img> tags
```

**Chart Storage:**
- Location: `reports/.charts/`
- Format: PNG (high quality, 150 DPI)
- Naming: `{chart-type}-{period}.png`
- Size: ~35-45 KB per chart

### 4. HTML Template Integration

Charts are embedded as images in the HTML template:

```html
<section id="charts">
    <h2>Visual Analytics</h2>

    <!-- Summary Chart -->
    <img src=".charts/summary-all.png" alt="Summary Metrics">

    <!-- Project Breakdowns (Grid Layout) -->
    <div class="charts-grid">
        <img src=".charts/project-total_commits-all.png">
        <img src=".charts/project-total_lines_added-all.png">
        <img src=".charts/project-net_change-all.png">
    </div>

    <!-- Timeline -->
    <img src=".charts/timeline-all.png">
</section>
```

**CSS Features:**
- Responsive grid layout for breakdowns
- Print optimization (no page breaks in charts)
- Centered alignment with padding
- Shadow effects for depth

---

## Technical Details

### Core Functions

**`git_analyzer.py`:**

1. **`get_tags(repo_path: Path) -> List[Tuple[str, datetime]]`**
   - Extracts semantic version tags
   - Sorts chronologically (newest first)

2. **`count_commits_between(repo_path: Path, from_tag: str, to_tag: str) -> int`**
   - Counts commits in git range

3. **`calculate_line_changes(repo_path: Path, from_tag: str, to_tag: str, exclusions: List[str]) -> Tuple[int, int]`** 🆕
   - Calculates lines added/removed
   - Applies file exclusion patterns
   - Returns (lines_added, lines_removed)

4. **`should_exclude_file(filepath: str, patterns: List[str]) -> bool`** 🆕
   - Matches file against exclusion patterns
   - Supports wildcards and directories

**`config_manager.py`:**

1. **`load_config(path: str = "config.yaml") -> Config`**
   - Loads and validates YAML configuration
   - Returns typed Config object
   - Raises errors for missing/invalid config

**`report_generator.py`:**

1. **`generate_html_report(projects_data, output_dir, period) -> Path`**
   - Main entry point for HTML generation
   - Orchestrates data preparation, chart generation, rendering, and saving
   - Returns path to generated HTML file

2. **`_prepare_report_data(projects_data, period) -> Dict`**
   - Calculates aggregate totals across all projects
   - Formats period for display (e.g., "2025-11" → "November 2025")
   - Generates timestamps and metadata

3. **`_generate_all_charts(projects_data, report_data, period, output_dir) -> Dict`** 🆕
   - Creates all charts for the report
   - Returns dict mapping chart names to relative paths
   - Generates 5 charts: summary, 3 breakdowns, timeline

4. **`_render_template(report_data, chart_paths) -> str`**
   - Sets up Jinja2 environment
   - Loads report.html template
   - Renders with data and chart paths, returns HTML string

5. **`_save_report(html_content, output_dir, period) -> Path`**
   - Creates output directory if needed
   - Generates filename (e.g., "kpi-report-all.html")
   - Writes HTML file and returns path

**`chart_generator.py`:** 🆕

1. **`generate_project_breakdown_chart(projects, metric, period, output_path) -> Path`**
   - Creates horizontal bar chart comparing services
   - Sorts by metric value (descending)
   - Highlights top performer in green
   - Returns path to saved PNG file

2. **`generate_timeline_chart(timeline_data, period, output_path) -> Path`**
   - Creates timeline bar chart showing releases over time
   - Groups releases by month
   - Handles empty data gracefully
   - Returns path to saved PNG file

3. **`generate_summary_comparison_chart(summary_data, period, output_path) -> Path`**
   - Creates bar chart with 4 summary metrics
   - Color-coded bars (releases, commits, added, removed)
   - Value labels with thousands separators
   - Returns path to saved PNG file

4. **`setup_chart_style()`**
   - Applies consistent styling to all charts
   - Sets figure size, DPI, fonts, colors
   - Called automatically by chart generation functions

---

## Performance

**Benchmarks:**
- 3 repositories with 334 tags: **~4 seconds**
- Line change calculation adds minimal overhead
- File exclusions improve accuracy without speed penalty

---

## Known Limitations

Phase 3 intentionally excludes:

1. ⚠️ **No Changelog Parsing** - Git metrics only (future enhancement)
2. ⚠️ **Limited Display** - Shows last 5 releases only
3. ⚠️ **No Charts/Visualizations** - Tables only (Phase 4)
4. ⚠️ **No Period Filtering** - Period parameter defined but not yet filtering data
5. ⚠️ **No Trend Analysis** - Snapshot metrics only

These will be addressed in future phases.

---

## Validation

### Manual Verification

Confirm line counts by comparing with git:

```bash
# Check line changes manually
cd /path/to/repo
git diff --numstat 9.0.2 9.2.5 | awk '{added+=$1; removed+=$2} END {print "Added:", added, "Removed:", removed}'

# Compare with script output
python -m src.main
```

**Result:** Line counts match git exactly ✅

**Example verification:**
```
Git command:    Added: 13221  Removed: 485
Script output:  (+13,221 / -485 lines)
✅ Match!
```

---

## Dependencies

```txt
GitPython==3.1.40     # Git repository operations
pytest==7.4.3         # Testing framework
pytest-cov==4.1.0     # Coverage reporting
PyYAML==6.0.3         # YAML configuration
python-dateutil==2.9  # Date parsing utilities
Jinja2==3.1.6         # HTML template rendering
matplotlib==3.10.7    # 🆕 Chart generation and visualization
```

---

## Next Steps: Phase 5 and Beyond

With Phase 4 complete, future enhancements could include:

- 📋 **Changelog Parser** - Extract structured data from CHANGELOG.md for change type analysis
- 🔍 **Project Scanner** - Automatic discovery and validation of repositories
- 📅 **Period Filtering** - Implement actual date range filtering (currently parameter exists but not enforced)
- 📈 **Trend Analysis** - Velocity metrics, release cadence, growth trends over time
- 🎯 **Interactive Charts** - Add Chart.js or D3.js for interactive visualizations
- 🔄 **Automated Scheduling** - Cron jobs for regular report generation
- 📧 **Email Integration** - Automated report distribution to stakeholders
- 🎨 **Custom Themes** - Configurable color schemes and branding
- 💾 **Export Formats** - CSV, JSON, Markdown export options
- 📊 **Dashboards** - Real-time metrics dashboard with auto-refresh
- 🔔 **Alerts** - Notifications for unusual patterns (high churn, low activity, etc.)

See `docs/` directory for complete specifications.

---

## Development Timeline

**Phase 1 (Complete):** Git tag parsing, commit counting - 5 hours
**Phase 2 (Complete):** Line metrics, configuration - 3 hours
**Phase 3 (Complete):** HTML reports, CLI arguments, templates - 2 hours
**Phase 4 (Complete):** Data visualization with matplotlib charts - 2 hours

**Total:** ~12 hours over 3-4 days

---

## Success Criteria ✅

Phase 4 is complete when:

- [x] Load configuration from YAML file
- [x] Calculate lines added/removed with exclusions
- [x] Display enhanced metrics in console output
- [x] Generate professional HTML reports with Jinja2
- [x] Support CLI arguments for output format
- [x] Embed CSS for offline/PDF compatibility
- [x] Implement dual output modes (console/HTML)
- [x] **Generate matplotlib charts automatically** 🆕
- [x] **Create project breakdown visualizations** 🆕
- [x] **Create release timeline charts** 🆕
- [x] **Embed charts in HTML reports** 🆕
- [x] **Charts are print/PDF-friendly (static PNG)** 🆕
- [x] File exclusion patterns filter correctly
- [x] All tests pass (33/33)
- [x] Test coverage ≥70% (achieved 74%)
- [x] Manual validation matches git diff
- [x] Performance acceptable (<10s for 3 repos + charts)

**Status: ✅ All criteria met**

---

## Usage Examples

### Basic Console Report

```bash
# Generate console output (default)
kpi
```

Shows last 5 releases for each configured project with commits and line changes.

### HTML Report Generation 🆕

```bash
# Generate HTML report for all time
kpi --html

# Generate for specific month
kpi --html --period 2025-11

# Generate for specific quarter
kpi --html --period 2025-Q4

# Custom output directory
kpi --html -o ./monthly-reports
```

### View HTML Report

```bash
# Open generated report in browser
open reports/kpi-report-all.html

# Or get the file path from output
python -m src.main --html
# Output shows: file:///path/to/reports/kpi-report-all.html
```

### Export to PDF

```bash
# Generate HTML report
python -m src.main --html

# Open in browser
open reports/kpi-report-all.html

# Then: File → Print → Save as PDF
# Layout automatically optimized for print
```

### Custom Configuration

```bash
# Edit config.yaml to add/remove projects
nano config.yaml

# Run with updated config
kpi              # Console
kpi --html       # HTML
```

### Verify Line Counts

```bash
# Manual verification
cd ../your-microservice-repo
git diff --numstat <old-tag> <new-tag> | head -10

# Compare with script output
cd ~/path/to/kpi-report-generator
kpi | grep -A 5 "your-microservice"
```

---

## Troubleshooting

### Config File Not Found

```
❌ Error: config.yaml not found
```

**Solution:** Create `config.yaml` in project root with required fields.

### No Projects Found

```
⚠️  SKIP: project-name (not found at /path/to/repo)
```

**Solution:** Verify `projects_directory` path in config.yaml is correct.

### Import Errors

```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:** Install dependencies: `pip install -r requirements.txt`

---

## License

Internal tool for development metrics reporting.

---

## Contact

For documentation, refer to `docs/` directory for complete specifications.
