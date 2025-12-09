# Task 2: Report Generation & Presentation

## Overview

Implement the report generation and presentation layer for the KPI Report Generator. This task focuses on transforming collected metrics into visual, PDF-friendly HTML reports.

## Scope

This task covers:
- HTML report template design
- Chart generation (static, PDF-friendly)
- Report assembly and formatting
- CLI interface
- Output file management

## Components to Implement

### 1. Chart Generator (`src/chart_generator.py`)

**Purpose:** Generate static charts as images for embedding in HTML

**Responsibilities:**
- Create bar charts for metrics comparison
- Create pie charts for distribution
- Create timeline charts for historical trends
- Save charts as PNG images
- Use PDF-friendly styling (no interactivity)

**Dependencies:**
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, List, Tuple
```

**Key Methods:**

```python
def generate_summary_bar_chart(
    current: Dict[str, int],
    previous: Dict[str, int],
    output_path: Path
) -> Path:
    """
    Generate month-over-month comparison bar chart.

    Metrics: Releases, Commits, Lines Changed
    Shows current month vs previous month side-by-side.

    Returns: Path to saved PNG file
    """
    pass

def generate_project_breakdown_chart(
    projects: List[ProjectMetrics],
    metric: str,  # "releases", "commits", "lines_changed"
    output_path: Path
) -> Path:
    """
    Generate horizontal bar chart showing metric per project.

    Projects sorted by metric value (descending).

    Returns: Path to saved PNG file
    """
    pass

def generate_change_type_pie_chart(
    distribution: Dict[str, int],
    output_path: Path
) -> Path:
    """
    Generate pie chart showing change type distribution.

    Sections: Added, Fixed, Changed, Removed
    Colors: Consistent with project theme

    Returns: Path to saved PNG file
    """
    pass

def generate_timeline_chart(
    timeline_data: List[Tuple[datetime, int]],
    metric_name: str,
    output_path: Path
) -> Path:
    """
    Generate timeline bar chart showing metric over time.

    X-axis: Months
    Y-axis: Metric value

    Optional: Add secondary axis for lines changed

    Returns: Path to saved PNG file
    """
    pass
```

**Chart Styling:**
```python
# Consistent styling for all charts
CHART_STYLE = {
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 10,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.2
}

COLOR_PALETTE = {
    "primary": "#2C3E50",
    "secondary": "#3498DB",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "added": "#27AE60",
    "fixed": "#3498DB",
    "changed": "#F39C12",
    "removed": "#E74C3C"
}
```

---

### 2. HTML Template (`templates/report.html`)

**Purpose:** Static HTML template for rendering report data

**Requirements:**
- Clean, professional design
- Print/PDF friendly (no page breaks in wrong places)
- Embedded CSS (no external dependencies)
- Responsive layout
- Clear visual hierarchy

**Template Structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KPI Report - {{ period }}</title>
    <style>
        /* Embedded CSS for PDF compatibility */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Print-friendly styles */
        @media print {
            body { max-width: 100%; }
            .page-break { page-break-before: always; }
            img { max-width: 100%; }
        }

        /* Headers */
        h1 { color: #2C3E50; margin-bottom: 10px; }
        h2 { color: #34495E; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #3498DB; padding-bottom: 5px; }
        h3 { color: #34495E; margin-top: 20px; margin-bottom: 10px; }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498DB;
            color: white;
            font-weight: 600;
        }
        tr:hover { background-color: #f5f5f5; }

        /* Charts */
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        /* Summary cards */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .summary-card h3 { color: white; margin: 0; font-size: 14px; }
        .summary-card .value { font-size: 32px; font-weight: bold; margin: 10px 0; }

        /* Warnings */
        .warnings {
            background-color: #FFF3CD;
            border-left: 4px solid #F39C12;
            padding: 15px;
            margin: 20px 0;
        }
        .warnings h3 { color: #856404; margin-bottom: 10px; }
        .warnings ul { margin-left: 20px; }

        /* Footer */
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Development KPI Report</h1>
        <p><strong>Period:</strong> {{ period_display }}</p>
        <p><strong>Generated:</strong> {{ generation_date }}</p>
    </header>

    <!-- Summary Section -->
    <section id="summary">
        <h2>Executive Summary</h2>
        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Releases</h3>
                <div class="value">{{ summary.total_releases }}</div>
            </div>
            <div class="summary-card">
                <h3>Total Commits</h3>
                <div class="value">{{ summary.total_commits }}</div>
            </div>
            <div class="summary-card">
                <h3>Lines Added</h3>
                <div class="value">{{ summary.total_lines_added | format_number }}</div>
            </div>
            <div class="summary-card">
                <h3>Lines Removed</h3>
                <div class="value">{{ summary.total_lines_removed | format_number }}</div>
            </div>
        </div>
    </section>

    <!-- Month-over-Month Comparison -->
    <section id="mom-comparison" class="page-break">
        <h2>Month-over-Month Comparison</h2>
        <div class="chart-container">
            <img src="{{ charts.mom_comparison }}" alt="Month-over-Month Comparison">
        </div>
    </section>

    <!-- Per-Service Breakdown -->
    <section id="service-breakdown">
        <h2>Per-Service Breakdown</h2>

        <h3>Releases by Service</h3>
        <div class="chart-container">
            <img src="{{ charts.project_releases }}" alt="Releases by Service">
        </div>

        <h3>Detailed Metrics</h3>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Releases</th>
                    <th>Commits</th>
                    <th>Lines Added</th>
                    <th>Lines Removed</th>
                    <th>Primary Change Type</th>
                </tr>
            </thead>
            <tbody>
                {% for project in projects %}
                <tr>
                    <td><strong>{{ project.name }}</strong></td>
                    <td>{{ project.releases }}</td>
                    <td>{{ project.commits }}</td>
                    <td>{{ project.lines_added | format_number }}</td>
                    <td>{{ project.lines_removed | format_number }}</td>
                    <td>{{ project.primary_change_type }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </section>

    <!-- Timeline Chart -->
    <section id="timeline" class="page-break">
        <h2>Release Timeline</h2>
        <div class="chart-container">
            <img src="{{ charts.timeline }}" alt="Release Timeline">
        </div>
    </section>

    <!-- Change Type Distribution -->
    <section id="change-types">
        <h2>Change Type Distribution</h2>
        <div class="chart-container">
            <img src="{{ charts.change_types }}" alt="Change Type Distribution">
        </div>
    </section>

    <!-- Warnings (if any) -->
    {% if warnings %}
    <section id="warnings">
        <div class="warnings">
            <h3>⚠️ Warnings</h3>
            <ul>
                {% for warning in warnings %}
                <li>{{ warning }}</li>
                {% endfor %}
            </ul>
        </div>
    </section>
    {% endif %}

    <footer class="footer">
        <p>Generated by KPI Report Generator v1.0.0</p>
        <p>{{ generation_timestamp }}</p>
    </footer>
</body>
</html>
```

---

### 3. Report Generator (`src/report_generator.py`)

**Purpose:** Orchestrate report generation from collected data

**Responsibilities:**
- Load HTML template
- Generate all required charts
- Populate template with data
- Save HTML output file
- Clean up temporary chart files (optional)

**Data Model:**

```python
@dataclass
class ReportData:
    """Complete data for report generation."""
    period: str
    period_display: str  # Human-readable: "November 2025"
    generation_date: str
    generation_timestamp: str
    summary: AggregatedMetrics
    previous_summary: Optional[AggregatedMetrics]
    projects: List[ProjectMetrics]
    warnings: List[str]
    chart_paths: Dict[str, Path]  # Chart name -> file path
```

**Key Methods:**

```python
def generate_report(
    collected_data: CollectedData,
    period: str,
    output_dir: Path
) -> Path:
    """
    Generate complete HTML report from collected data.

    Steps:
    1. Prepare report data
    2. Generate all charts
    3. Load and populate template
    4. Save HTML file

    Returns: Path to generated HTML file
    """
    pass

def prepare_report_data(
    collected_data: CollectedData,
    period: str
) -> ReportData:
    """
    Transform collected data into report-ready format.

    - Calculate previous period for comparison
    - Format dates for display
    - Determine primary change types per project
    """
    pass

def generate_all_charts(
    report_data: ReportData,
    output_dir: Path
) -> Dict[str, str]:
    """
    Generate all charts and return paths for template.

    Charts generated:
    - Month-over-month comparison
    - Project breakdown (releases)
    - Project breakdown (commits)
    - Change type distribution
    - Timeline

    Returns: Dict mapping chart names to relative paths
    """
    pass

def populate_template(
    template_path: Path,
    report_data: ReportData
) -> str:
    """
    Load Jinja2 template and populate with data.

    Custom filters:
    - format_number: Add thousand separators
    - format_percentage: Format as percentage
    """
    pass

def save_report(
    html_content: str,
    output_path: Path
) -> Path:
    """
    Save HTML content to file.

    Creates output directory if doesn't exist.
    Returns: Path to saved file
    """
    pass
```

**Custom Template Filters:**

```python
def format_number(value: int) -> str:
    """Format number with thousand separators: 12345 -> 12,345"""
    return f"{value:,}"

def format_percentage(value: float) -> str:
    """Format float as percentage: 0.456 -> 45.6%"""
    return f"{value * 100:.1f}%"

def calculate_percentage(part: int, total: int) -> str:
    """Calculate and format percentage: (45, 100) -> "45.0%"  """
    if total == 0:
        return "0.0%"
    return format_percentage(part / total)
```

---

### 4. CLI Interface (`src/main.py`)

**Purpose:** Command-line interface for running the report generator

**Responsibilities:**
- Parse command-line arguments
- Orchestrate full pipeline
- Handle errors gracefully
- Display progress and results

**CLI Specification:**

```bash
# Default: last month
python -m src.main

# Specific month
python -m src.main --period 2025-11

# Specific quarter
python -m src.main --period 2025-Q4

# All time
python -m src.main --period all

# Custom config file
python -m src.main --config custom-config.yaml

# Verbose output
python -m src.main --verbose

# Keep temporary chart files
python -m src.main --keep-charts
```

**Implementation:**

```python
import argparse
import sys
from pathlib import Path
from datetime import datetime
import logging

from src.config_manager import load_config
from src.project_scanner import scan_projects
from src.changelog_parser import parse_changelog
from src.git_analyzer import analyze_repository
from src.data_aggregator import aggregate_metrics
from src.report_generator import generate_report

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate monthly KPI reports from microservice repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                    # Generate report for last month
  python -m src.main --period 2025-11   # Specific month
  python -m src.main --period 2025-Q4   # Specific quarter
  python -m src.main --period all       # All time
        """
    )

    parser.add_argument(
        "--period",
        type=str,
        default="last-month",
        help="Reporting period: YYYY-MM, YYYY-QN, 'all', or 'last-month' (default)"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--keep-charts",
        action="store_true",
        help="Keep temporary chart files after report generation"
    )

    return parser.parse_args()

def setup_logging(verbose: bool):
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def normalize_period(period: str) -> str:
    """
    Normalize period string to standard format.

    "last-month" -> "YYYY-MM" (calculated)
    """
    if period == "last-month":
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        return last_month.strftime("%Y-%m")
    return period

def main():
    """Main entry point for KPI report generation."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger = logging.getLogger(__name__)
    logger.info("Starting KPI report generation")

    try:
        # Load configuration
        logger.info(f"Loading configuration from {args.config}")
        config = load_config(args.config)

        # Normalize period
        period = normalize_period(args.period)
        logger.info(f"Generating report for period: {period}")

        # Scan projects
        logger.info(f"Scanning projects in {config.projects_directory}")
        projects = scan_projects(config)
        logger.info(f"Found {len(projects)} valid projects")

        if not projects:
            logger.error("No valid projects found. Check configuration.")
            sys.exit(1)

        # Collect changelog data
        logger.info("Parsing changelogs...")
        changelogs = []
        for project in projects:
            changelog = parse_changelog(project.path)
            if changelog:
                changelogs.append(changelog)
                logger.debug(f"  ✓ {project.name}: {len(changelog.releases)} releases")
            else:
                logger.warning(f"  ⚠ {project.name}: No changelog found")

        # Collect git metrics
        logger.info("Analyzing git repositories...")
        git_metrics = []
        for project in projects:
            metrics = analyze_repository(project.path, config.file_exclusions)
            git_metrics.append(metrics)
            logger.debug(f"  ✓ {project.name}: {len(metrics.tag_metrics)} tags analyzed")

        # Aggregate metrics
        logger.info("Aggregating metrics...")
        aggregated = aggregate_metrics(changelogs, git_metrics, period)
        logger.info(f"  Releases: {aggregated.total_releases}")
        logger.info(f"  Commits: {aggregated.total_commits}")
        logger.info(f"  Lines changed: {aggregated.total_lines_added + aggregated.total_lines_removed:,}")

        # Prepare collected data
        collected_data = CollectedData(
            config=config,
            projects=projects,
            changelogs=changelogs,
            git_metrics=git_metrics,
            aggregated=aggregated,
            warnings=[w for p in projects for w in p.warnings]
        )

        # Generate report
        logger.info("Generating report...")
        report_path = generate_report(
            collected_data,
            period,
            config.report_output
        )

        logger.info(f"✓ Report generated successfully: {report_path}")

        # Display warnings if any
        if collected_data.warnings:
            logger.warning(f"\n⚠️  {len(collected_data.warnings)} warnings encountered:")
            for warning in collected_data.warnings:
                logger.warning(f"  - {warning}")

        # Open report in browser (optional)
        if not args.keep_charts:
            logger.debug("Cleaning up temporary chart files...")
            # Cleanup logic here

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=args.verbose)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Implementation Requirements

### Testing Strategy

**Test Coverage Required:**

1. **Chart Generator**
   - Chart generation for valid data
   - Empty datasets
   - Single data point
   - Chart file saving
   - Style consistency

2. **Report Generator**
   - Template population with complete data
   - Template population with partial data
   - Missing charts handling
   - Output file creation
   - Custom filter functions

3. **CLI Interface**
   - Argument parsing (all options)
   - Period normalization
   - Error handling (missing config, no projects)
   - Logging output
   - Exit codes

### Error Handling

**Critical Errors (Exit):**
- Template file not found
- Output directory not writable
- Chart generation fails critically

**Warnings (Continue):**
- Individual chart generation fails (skip chart)
- Template rendering issues (fallback to plain text)

### Code Quality

- Type hints for all functions
- Docstrings following ReStructuredText format
- Clean separation of concerns
- No hardcoded paths or values
- Responsive error messages

### Dependencies

```txt
Jinja2>=3.1.2
matplotlib>=3.8.0
numpy>=1.24.0  # Required by matplotlib
```

---

## Output Specification

### File Naming Convention

```
reports/kpi-report-YYYY-MM.html
reports/kpi-report-YYYY-QN.html
reports/kpi-report-all-time.html
```

### Temporary Files

Charts generated during report creation:

```
reports/.charts/
├── mom-comparison-YYYY-MM.png
├── project-releases-YYYY-MM.png
├── project-commits-YYYY-MM.png
├── change-types-YYYY-MM.png
└── timeline-YYYY-MM.png
```

Option to keep or delete after report generation (`--keep-charts` flag).

---

## Directory Structure

```
src/
├── __init__.py
├── chart_generator.py     # Chart generation using matplotlib
├── report_generator.py    # Report assembly and HTML generation
└── main.py               # CLI interface and orchestration

templates/
└── report.html           # Jinja2 HTML template

reports/                  # Output directory (created automatically)
└── .charts/             # Temporary chart storage (optional)
```

---

## Testing Structure

```
tests/
├── __init__.py
├── test_chart_generator.py
├── test_report_generator.py
├── test_main.py
└── fixtures/
    ├── sample_template.html
    ├── sample_data.json
    └── expected_output.html
```

---

## Integration with Task 1

This task consumes the `CollectedData` structure from Task 1:

```python
@dataclass
class CollectedData:
    config: Config
    projects: List[ProjectInfo]
    changelogs: List[ProjectChangelog]
    git_metrics: List[ProjectGitMetrics]
    aggregated: AggregatedMetrics
    warnings: List[str]
```

Ensure data contracts match between tasks.

---

## Validation Checklist

Before considering Task 2 complete:

- [ ] All chart types generate correctly
- [ ] Charts are PDF-friendly (no interactivity)
- [ ] HTML template renders correctly in all browsers
- [ ] Print/PDF export works without page breaks in wrong places
- [ ] CLI interface handles all argument combinations
- [ ] Error messages are clear and actionable
- [ ] Test suite covers all components (90%+ coverage)
- [ ] Documentation complete for all public functions
- [ ] Sample report generated and reviewed
- [ ] Performance tested with large datasets

---

## Example Output

Sample command:

```bash
python -m src.main --period 2025-11
```

Expected output:

```
2025-12-04 10:30:15 - INFO - Starting KPI report generation
2025-12-04 10:30:15 - INFO - Loading configuration from config.yaml
2025-12-04 10:30:15 - INFO - Generating report for period: 2025-11
2025-12-04 10:30:15 - INFO - Scanning projects in ../PyProjects
2025-12-04 10:30:16 - INFO - Found 8 valid projects
2025-12-04 10:30:16 - INFO - Parsing changelogs...
2025-12-04 10:30:16 - INFO - Analyzing git repositories...
2025-12-04 10:30:18 - INFO - Aggregating metrics...
2025-12-04 10:30:18 - INFO -   Releases: 23
2025-12-04 10:30:18 - INFO -   Commits: 156
2025-12-04 10:30:18 - INFO -   Lines changed: 8,453
2025-12-04 10:30:18 - INFO - Generating report...
2025-12-04 10:30:22 - INFO - ✓ Report generated successfully: reports/kpi-report-2025-11.html

⚠️  3 warnings encountered:
  - Project 'legacy-service' not on valid branch (currently on 'feature/update')
  - Project 'new-service' has no git tags
  - Project 'auth-service' CHANGELOG.md has malformed date in version 2.3.1
```

Generated file:
```
reports/kpi-report-2025-11.html  (opens in browser)
```

---

## PDF Export Notes

While the HTML is PDF-friendly, actual PDF generation can be done externally:

**Using browser:**
```
Open report in Chrome/Firefox → Print → Save as PDF
```

**Using command line (optional future enhancement):**
```bash
# Using wkhtmltopdf
wkhtmltopdf reports/kpi-report-2025-11.html reports/kpi-report-2025-11.pdf

# Using weasyprint
weasyprint reports/kpi-report-2025-11.html reports/kpi-report-2025-11.pdf
```

This is **out of scope** for MVP but template is designed to support it.

---

## Notes for Implementation

1. **Chart Generation:** Use matplotlib's `Agg` backend for server-side rendering (no display required)
2. **Template Engine:** Jinja2 provides powerful template inheritance and custom filters
3. **Path Handling:** Use relative paths in HTML for portability
4. **Styling:** Embedded CSS ensures single-file portability
5. **Responsive Design:** Graceful degradation for smaller screens/print

---

## Future Enhancements (Out of Scope)

- Interactive charts (Chart.js/Plotly)
- Export to Excel/CSV
- Email delivery
- Scheduled runs
- Web dashboard
- Historical trend analysis
- Team member attribution
- CI/CD integration

---

## Dependencies on Task 1

Requires complete implementation of Task 1 data collection components. The `CollectedData` structure must be fully populated and validated before report generation.
