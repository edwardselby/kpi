# KPI Report Generator

A domain-agnostic tool for generating professional KPI reports from git repository metrics. Analyze release history, commit counts, and line changes across multiple microservice repositories with console output, HTML reports, and embedded data visualizations.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Features

- 📊 **Git Metrics Analysis** - Extract semantic version tags, count commits, and track line changes between releases
- 📈 **Data Visualization** - Generate professional charts with matplotlib (activity, volume, comparisons, timelines)
- 📄 **HTML Reports** - Professional, print-ready HTML reports with embedded CSS and charts
- ⚙️ **Flexible Configuration** - YAML-based configuration with support for private organization data
- 🎯 **File Exclusions** - Smart filtering to exclude lock files, minified assets, and dependencies
- ⚡ **Fast Testing** - Comprehensive test suite with mocked unit tests (~1s) and integration tests
- 🔧 **CLI Interface** - Command-line arguments for output format and period selection

---

## Quick Start

### Prerequisites

- Python 3.10+
- Git repositories with semantic versioning tags
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/edwardselby/kpi.git
cd kpi

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in development mode
pip install -e .
```

This installs all dependencies and creates a `kpi` console command.

### Configuration

The tool uses a hierarchical configuration system:

1. **config.local.yaml** (if exists) - Your private organization configuration
2. **config.yaml** (fallback) - Public template with generic examples

#### Option 1: Private Configuration (Recommended)

```bash
# Copy the template
cp config.yaml config.local.yaml

# Edit with your organization's services
nano config.local.yaml
```

The `config.local.yaml` file is gitignored and safe for private data.

#### Option 2: Edit Public Template

```yaml
# config.yaml
projects_directory: ./projects

included_projects:
  - api-gateway-service
  - user-service
  - payment-service

file_exclusions:
  - "*.lock"
  - "*.min.js"
  - "node_modules/*"
  - "dist/*"
```

### Basic Usage

```bash
# Console output (default)
kpi

# Generate HTML report
kpi --html

# Generate report for specific period
kpi --html --period 2025-11

# Get help
kpi --help
```

---

## Usage

### Console Output

Generate a text-based report to your terminal:

```bash
kpi
```

**Sample Output:**

```
======================================================================
KPI Report Generator
======================================================================

Configuration: config.yaml
Projects directory: /Users/username/projects
Analyzing 3 projects...

📦 api-gateway-service
----------------------------------------------------------------------
  2.1.0        2025-12-02 (latest)
  2.0.5        2025-10-23 →  45 commits  (+8,234 / -342 lines)
  2.0.4        2025-10-23 →   3 commits  (+512 / -28 lines)
  2.0.0        2025-10-15 →  12 commits  (+2,145 / -623 lines)
```

### HTML Reports

Generate professional HTML reports with embedded visualizations:

```bash
# All-time report
kpi --html

# Specific month
kpi --html --period 2025-11

# Specific quarter
kpi --html --period 2025-Q4

# Custom output directory
kpi --html -o ./reports
```

**Output:**
```
✅ HTML report generated: reports/kpi-report-all.html
   Open in browser: file:///path/to/kpi-report-generator/reports/kpi-report-all.html
```

**HTML Report Features:**
- 📊 Summary cards (total releases, commits, lines added/removed)
- 📈 Visual charts (6 embedded matplotlib visualizations)
- 📋 Per-service breakdown tables
- 📜 Complete release history
- 🎨 Professional styling with gradient headers
- 🖨️ Print-ready with optimized page breaks
- 🔗 No external dependencies (all CSS and charts embedded)

### Viewing Reports

```bash
# macOS
open reports/kpi-report-all.html

# Linux
xdg-open reports/kpi-report-all.html

# Windows
start reports/kpi-report-all.html
```

### Export to PDF

1. Open HTML report in browser
2. File → Print (or Cmd/Ctrl+P)
3. Select "Save as PDF"
4. Layout automatically optimized for print

---

## Configuration

### Configuration File Structure

```yaml
# Path to directory containing repositories
projects_directory: /path/to/repos

# Projects to analyze (whitelist)
included_projects:
  - project-1
  - project-2

# Files to exclude from line counts
file_exclusions:
  - "*.lock"
  - "*.min.js"
  - "*.min.css"
  - "node_modules/*"
  - "dist/*"
  - "build/*"
  - "migrations/*"
  - "package-lock.json"

# Valid git branches for analysis
valid_branches:
  - main
  - master
  - dev

# Optional: Service metadata for enhanced reporting
service_metadata:
  api-gateway-service:
    category: "Core Infrastructure"
    tags: ["API", "routing", "orchestration"]
    description: "Central API gateway for request routing"
```

### File Exclusion Patterns

The tool supports flexible exclusion patterns:

- **Wildcards**: `*.lock`, `*.min.js`
- **Directories**: `node_modules/*`, `dist/*`
- **Specific files**: `package-lock.json`

### Configuration Hierarchy

The configuration loader checks files in this order:

1. `config.local.yaml` (if exists) - Private organization config
2. `config.yaml` (fallback) - Public template

This allows you to keep private organization data in `config.local.yaml` (gitignored) while maintaining a generic public template.

---

## Testing

The test suite includes fast unit tests with mocks and slower integration tests with real operations.

### Quick Unit Tests (Default)

```bash
# Run unit tests only (~1 second)
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=term
```

Unit tests use mocks to avoid slow operations like git commands and matplotlib rendering.

### Integration Tests

```bash
# Run integration tests with real git/matplotlib operations (~3 minutes)
pytest tests/ -m integration -v
```

### All Tests

```bash
# Run both unit and integration tests
pytest tests/ -m "" -v

# With HTML coverage report
pytest tests/ --cov=src --cov-report=html -m ""
open htmlcov/index.html
```

### Test Coverage

- ✅ 33 tests passing
- ✅ 74% overall coverage
- ✅ 100% coverage on chart_generator.py
- ✅ 89% coverage on git_analyzer.py
- ✅ 88% coverage on config_manager.py

---

## Project Structure

```
kpi-report-generator/
├── config.yaml              # Configuration template
├── config.local.yaml        # Private config (gitignored)
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point and orchestration
│   ├── git_analyzer.py      # Git operations and metrics
│   ├── config_manager.py    # Configuration loading
│   ├── chart_generator.py   # Matplotlib chart generation
│   ├── report_generator.py  # HTML report generation
│   └── narrative_generator.py # Text narrative generation
├── templates/
│   └── report.html          # Jinja2 HTML template
├── reports/                 # Generated reports (gitignored)
│   ├── kpi-report-*.html    # HTML output files
│   └── .charts/             # Generated chart images
│       ├── release-activity-*.png
│       ├── code-volume-*.png
│       ├── project-total_commits-*.png
│       ├── project-total_lines_added-*.png
│       ├── project-net_change-*.png
│       └── timeline-*.png
├── tests/
│   ├── test_git_analyzer.py
│   ├── test_git_analyzer_unit.py
│   ├── test_chart_generator.py
│   ├── test_chart_generator_unit.py
│   ├── test_config_manager.py
│   ├── test_report_generator.py
│   ├── test_narrative_generator.py
│   ├── test_integration.py
│   └── fixtures/
│       └── sample_repo/     # Test git repository
├── docs/                    # Development documentation
├── requirements.txt         # Python dependencies
├── setup.py                 # Package configuration
├── pytest.ini               # Test configuration
└── README.md
```

---

## API Reference

### Core Functions

#### git_analyzer.py

```python
def get_tags(repo_path: Path) -> List[Tuple[str, datetime]]:
    """Extract semantic version tags from repository."""

def count_commits_between(repo_path: Path, from_tag: str, to_tag: str) -> int:
    """Count commits between two git tags."""

def calculate_line_changes(
    repo_path: Path,
    from_tag: str,
    to_tag: str,
    exclusions: List[str]
) -> Tuple[int, int]:
    """Calculate lines added and removed between tags."""

def should_exclude_file(filepath: str, patterns: List[str]) -> bool:
    """Check if file matches exclusion patterns."""
```

#### chart_generator.py

```python
def generate_project_breakdown_chart(
    projects: List[Dict],
    metric: str,
    period: str,
    output_path: Path
) -> Path:
    """Create horizontal bar chart comparing services."""

def generate_timeline_chart(
    timeline_data: List[Tuple],
    period: str,
    output_path: Path
) -> Path:
    """Create timeline showing releases over time."""

def generate_summary_comparison_chart(
    summary_data: Dict,
    period: str,
    output_path: Path
) -> Path:
    """Create bar chart with summary metrics."""
```

#### report_generator.py

```python
def generate_html_report(
    projects_data: List[Dict],
    output_dir: Path,
    period: str = "all"
) -> Path:
    """Generate HTML report with embedded charts."""
```

#### config_manager.py

```python
def load_config(path: str = "config.yaml") -> Config:
    """Load configuration with local override support."""
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
matplotlib==3.10.7    # Chart generation and visualization
```

---

## Performance

**Benchmarks:**
- 3 repositories with 334 tags: ~4 seconds
- Chart generation adds ~1-2 seconds
- HTML rendering: < 1 second
- Total end-to-end: < 10 seconds

---

## Use Cases

### E-commerce Platform

```yaml
included_projects:
  - product-catalog-service
  - shopping-cart-service
  - payment-gateway-service
  - order-fulfillment-service
```

### SaaS Application

```yaml
included_projects:
  - user-auth-service
  - subscription-management-service
  - billing-service
  - analytics-dashboard-service
```

### Fintech Application

```yaml
included_projects:
  - account-service
  - transaction-processor-service
  - risk-assessment-service
  - compliance-reporting-service
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

**Solution:** Verify `projects_directory` path in config.yaml points to the correct location.

### Import Errors

```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:** Install dependencies: `pip install -r requirements.txt`

### Permission Errors

```
PermissionError: [Errno 13] Permission denied
```

**Solution:** Ensure you have read access to git repositories and write access to the output directory.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Ensure all tests pass (`pytest tests/ -m ""`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/kpi.git
cd kpi

# Install in development mode with test dependencies
pip install -e .
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## License

MIT License - see LICENSE file for details.

---

## Support

- **Issues**: https://github.com/edwardselby/kpi/issues
- **Documentation**: See `docs/` directory for detailed specifications

---

## Acknowledgments

Built with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
