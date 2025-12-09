# Phase 3: Basic Reporting

## Purpose

Transform console output into professional HTML reports suitable for management presentation. Focus on clean tables and clear layout before adding visualizations.

## Duration

2-3 days

## Dependencies

- Phase 2 complete (data collection working)
- Jinja2 installed
- Sample data available for testing

---

## Goals

- [x] HTML template with professional styling
- [x] Summary metrics section (cards)
- [x] Per-project breakdown table
- [x] Warnings section
- [x] Print/PDF-friendly layout
- [x] Jinja2 template rendering
- [x] CLI interface with arguments
- [x] File output with naming convention

**Explicitly NOT in scope:**
- Charts (Phase 4)
- Interactive elements
- External CSS/JS dependencies

---

## Project Structure

```
kpi-reporter/
├── config.yaml
├── src/
│   ├── __init__.py
│   ├── main.py              # ENHANCED: CLI args
│   ├── report_generator.py  # NEW: Template rendering
│   ├── git_analyzer.py
│   ├── config_manager.py
│   ├── project_scanner.py
│   ├── changelog_parser.py
│   └── data_aggregator.py
├── templates/
│   └── report.html          # NEW: HTML template
├── reports/                 # NEW: Output directory
│   └── .gitkeep
├── tests/
│   └── test_report_generator.py  # NEW
└── requirements.txt         # UPDATED: Add Jinja2
```

---

## Implementation Tasks

### Task 3.1: HTML Template Design

**File:** `templates/report.html`

**Design principles:**
- Clean, professional appearance
- Print-friendly (proper page breaks)
- Embedded CSS (no external dependencies)
- Clear visual hierarchy
- Accessible (semantic HTML)

**Template structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KPI Report - {{ period_display }}</title>
    <style>
        /* Reset and base styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                         'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f7fa;
        }

        /* Print styles */
        @media print {
            body {
                background: white;
                max-width: 100%;
                padding: 20px;
            }
            .page-break { page-break-before: always; }
            .no-print { display: none; }
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .header .meta {
            font-size: 14px;
            opacity: 0.9;
        }

        /* Summary cards */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .summary-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }

        .summary-card h3 {
            font-size: 14px;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }

        .summary-card .value {
            font-size: 36px;
            font-weight: bold;
            color: #2c3e50;
        }

        /* Section headers */
        h2 {
            color: #2c3e50;
            font-size: 24px;
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        thead {
            background: #34495e;
            color: white;
        }

        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }

        tbody tr:hover {
            background: #f8f9fa;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        /* Right-align numeric columns */
        .numeric {
            text-align: right;
            font-variant-numeric: tabular-nums;
        }

        /* Warnings */
        .warnings {
            background: #fff3cd;
            border-left: 4px solid #f39c12;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }

        .warnings h3 {
            color: #856404;
            margin-bottom: 15px;
        }

        .warnings ul {
            margin-left: 20px;
        }

        .warnings li {
            margin: 8px 0;
            color: #856404;
        }

        /* Footer */
        .footer {
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            text-align: center;
            color: #7f8c8d;
            font-size: 13px;
        }

        /* Utility classes */
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }

        .badge-success { background: #d4edda; color: #155724; }
        .badge-warning { background: #fff3cd; color: #856404; }
        .badge-info { background: #d1ecf1; color: #0c5460; }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <h1>Development KPI Report</h1>
        <div class="meta">
            <strong>Period:</strong> {{ period_display }} |
            <strong>Generated:</strong> {{ generation_date }}
        </div>
    </div>

    <!-- Summary Section -->
    <section id="summary">
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
                <div class="value">{{ "{:,}".format(summary.total_lines_added) }}</div>
            </div>
            <div class="summary-card">
                <h3>Lines Removed</h3>
                <div class="value">{{ "{:,}".format(summary.total_lines_removed) }}</div>
            </div>
        </div>
    </section>

    <!-- Change Type Distribution -->
    <section id="change-types">
        <h2>Change Type Distribution</h2>
        <table>
            <thead>
                <tr>
                    <th>Type</th>
                    <th class="numeric">Count</th>
                    <th class="numeric">Percentage</th>
                </tr>
            </thead>
            <tbody>
                {% for type, count in change_distribution.items() %}
                <tr>
                    <td><span class="badge badge-info">{{ type }}</span></td>
                    <td class="numeric">{{ count }}</td>
                    <td class="numeric">{{ "%.1f"|format((count / total_changes * 100) if total_changes > 0 else 0) }}%</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </section>

    <!-- Per-Project Breakdown -->
    <section id="projects" class="page-break">
        <h2>Per-Service Breakdown</h2>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th class="numeric">Releases</th>
                    <th class="numeric">Commits</th>
                    <th class="numeric">Lines Added</th>
                    <th class="numeric">Lines Removed</th>
                    <th>Primary Change Type</th>
                </tr>
            </thead>
            <tbody>
                {% for project in projects %}
                <tr>
                    <td><strong>{{ project.name }}</strong></td>
                    <td class="numeric">{{ project.releases }}</td>
                    <td class="numeric">{{ project.commits }}</td>
                    <td class="numeric">{{ "{:,}".format(project.lines_added) }}</td>
                    <td class="numeric">{{ "{:,}".format(project.lines_removed) }}</td>
                    <td>
                        <span class="badge badge-success">{{ project.primary_change_type }}</span>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </section>

    <!-- Warnings Section -->
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

    <!-- Footer -->
    <footer class="footer">
        <p>Generated by KPI Report Generator v1.0.0</p>
        <p>{{ generation_timestamp }}</p>
    </footer>
</body>
</html>
```

**Test template:**
- Open in Chrome, Firefox, Safari
- Print preview (check page breaks)
- Verify responsive layout
- Check accessibility (semantic HTML)

**Success criteria:**
- Renders correctly in all browsers
- Print/PDF export works cleanly
- Professional appearance
- Clear visual hierarchy

---

### Task 3.2: Report Generator Implementation

**File:** `src/report_generator.py`

**See:** `docs/task-2-report-generation.md` for complete specification

**Core functionality:**

```python
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass


@dataclass
class ReportData:
    """Data structure for template rendering."""
    period: str
    period_display: str
    generation_date: str
    generation_timestamp: str
    summary: AggregatedMetrics
    projects: List[ProjectMetrics]
    change_distribution: Dict[str, int]
    total_changes: int
    warnings: List[str]


def generate_report(
    collected_data: CollectedData,
    period: str,
    output_dir: Path
) -> Path:
    """
    Generate HTML report from collected data.

    :param collected_data: Complete dataset from Phase 2
    :param period: Reporting period (e.g., "2025-11")
    :param output_dir: Directory for output file
    :return: Path to generated HTML file
    """
    # Prepare report data
    report_data = prepare_report_data(collected_data, period)

    # Load and render template
    html_content = render_template(report_data)

    # Save to file
    output_path = output_dir / f"kpi-report-{period}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path


def prepare_report_data(
    collected_data: CollectedData,
    period: str
) -> ReportData:
    """Transform collected data for template."""
    # Format period for display
    period_display = format_period_display(period)

    # Calculate total changes for percentages
    total_changes = sum(collected_data.aggregated.change_type_distribution.values())

    return ReportData(
        period=period,
        period_display=period_display,
        generation_date=datetime.now().strftime("%B %d, %Y"),
        generation_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        summary=collected_data.aggregated,
        projects=collected_data.aggregated.projects,
        change_distribution=collected_data.aggregated.change_type_distribution,
        total_changes=total_changes,
        warnings=collected_data.warnings
    )


def format_period_display(period: str) -> str:
    """
    Convert period code to human-readable format.

    Examples:
    - "2025-11" -> "November 2025"
    - "2025-Q4" -> "Q4 2025"
    - "all" -> "All Time"
    """
    if period == "all":
        return "All Time"

    if period.startswith("Q"):
        return period  # "Q4 2025"

    # Month format: 2025-11
    try:
        date = datetime.strptime(period, "%Y-%m")
        return date.strftime("%B %Y")
    except:
        return period


def render_template(report_data: ReportData) -> str:
    """Load Jinja2 template and render with data."""
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('report.html')

    return template.render(
        period_display=report_data.period_display,
        generation_date=report_data.generation_date,
        generation_timestamp=report_data.generation_timestamp,
        summary=report_data.summary,
        projects=report_data.projects,
        change_distribution=report_data.change_distribution,
        total_changes=report_data.total_changes,
        warnings=report_data.warnings
    )
```

**Test coverage:**
- Template rendering with complete data
- Template rendering with partial data
- Period formatting (month, quarter, all)
- File output creation
- Missing template error handling

**Success criteria:**
- Generates valid HTML
- All data populates correctly
- File saved to correct location
- No template errors

---

### Task 3.3: CLI Interface

**File:** `src/main.py` (ENHANCED)

**Add argument parsing:**

```python
import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# ... existing imports ...


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate KPI reports from microservice repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                    # Last month
  python -m src.main --period 2025-11   # Specific month
  python -m src.main --period 2025-Q4   # Quarter
  python -m src.main --period all       # All time
  python -m src.main --verbose          # Debug output
        """
    )

    parser.add_argument(
        "--period",
        type=str,
        default="last-month",
        help="Period: YYYY-MM, YYYY-QN, 'all', or 'last-month' (default)"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Config file path (default: config.yaml)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output directory (overrides config)"
    )

    return parser.parse_args()


def normalize_period(period: str) -> str:
    """Convert 'last-month' to YYYY-MM format."""
    if period == "last-month":
        # Get last complete month
        today = datetime.now()
        first_of_month = today.replace(day=1)
        last_month = first_of_month - timedelta(days=1)
        return last_month.strftime("%Y-%m")
    return period


def setup_logging(verbose: bool):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )


def main():
    """Main entry point."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger = logging.getLogger(__name__)

    try:
        # Load config
        config = load_config(args.config)

        # Override output dir if specified
        if args.output:
            config.report_output = Path(args.output)

        # Normalize period
        period = normalize_period(args.period)

        logger.info(f"Generating report for {period}")

        # Phase 2 data collection
        projects = scan_projects(config)
        changelogs = [parse_changelog(p.path) for p in projects]
        git_metrics = [analyze_repository(p.path, config.file_exclusions) for p in projects]
        aggregated = aggregate_metrics(changelogs, git_metrics, period)

        collected_data = CollectedData(
            config=config,
            projects=projects,
            changelogs=[c for c in changelogs if c],
            git_metrics=git_metrics,
            aggregated=aggregated,
            warnings=[w for p in projects for w in p.warnings]
        )

        # Phase 3 report generation
        report_path = generate_report(
            collected_data,
            period,
            config.report_output
        )

        logger.info(f"✓ Report generated: {report_path}")

        if collected_data.warnings:
            logger.warning(f"\n⚠️  {len(collected_data.warnings)} warnings:")
            for warning in collected_data.warnings:
                logger.warning(f"  - {warning}")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Test coverage:**
- Argument parsing (all combinations)
- Period normalization
- Config override
- Error handling
- Exit codes

**Success criteria:**
- All CLI options work
- Help text is clear
- Error messages are helpful
- Exit codes are correct

---

### Task 3.4: Integration Testing

**File:** `tests/test_report_generation_integration.py`

```python
"""Integration tests for report generation."""

import pytest
from pathlib import Path
import tempfile
from src.main import main
import sys


def test_full_report_generation(tmp_path, monkeypatch):
    """Test complete report generation pipeline."""
    # Mock sys.argv
    test_args = ["main.py", "--period", "all", "--output", str(tmp_path)]
    monkeypatch.setattr(sys, "argv", test_args)

    # Run main
    main()

    # Verify output exists
    report_file = tmp_path / "kpi-report-all.html"
    assert report_file.exists()

    # Verify HTML content
    html = report_file.read_text()
    assert "<!DOCTYPE html>" in html
    assert "Development KPI Report" in html
    assert "<table>" in html


def test_report_template_rendering():
    """Test template renders with sample data."""
    from src.report_generator import render_template, ReportData
    from src.data_aggregator import AggregatedMetrics, ProjectMetrics

    # Create sample data
    report_data = ReportData(
        period="2025-11",
        period_display="November 2025",
        generation_date="December 4, 2025",
        generation_timestamp="2025-12-04 10:30:00",
        summary=AggregatedMetrics(
            period="2025-11",
            total_releases=10,
            total_commits=50,
            total_lines_added=1000,
            total_lines_removed=500,
            date_range=(datetime(2025,11,1), datetime(2025,11,30)),
            projects=[],
            change_type_distribution={"Fixed": 20, "Added": 15}
        ),
        projects=[],
        change_distribution={"Fixed": 20, "Added": 15},
        total_changes=35,
        warnings=[]
    )

    html = render_template(report_data)

    assert "November 2025" in html
    assert "10" in html  # Total releases
    assert "1,000" in html  # Formatted line count
```

---

## Exit Criteria

Before proceeding to Phase 4:

- [ ] HTML template designed and tested
- [ ] Report generator creates valid HTML
- [ ] CLI interface works with all arguments
- [ ] Reports open correctly in browsers
- [ ] Print/PDF export works cleanly
- [ ] All data displays correctly
- [ ] Warnings section appears when needed
- [ ] File naming follows convention
- [ ] Integration tests pass
- [ ] Manual testing with real data successful

---

## Demo Checklist

At end of Phase 3:

- [ ] Run `python -m src.main --period 2025-11`
- [ ] Open generated HTML in browser
- [ ] Show summary metrics
- [ ] Show project breakdown table
- [ ] Print preview (show PDF readiness)
- [ ] Show warnings section
- [ ] Demonstrate CLI options
- [ ] Explain what Phase 4 will add

**Demo script:**

```
"Phase 3 transforms our data into professional HTML reports.

Running the generator... [execute]

This creates an HTML file that opens in any browser. Let me show you.

At the top we have the summary metrics - releases, commits, and lines
changed for the period.

Below that is the change type distribution showing what kind of work
was done - mostly bug fixes this month.

The per-service breakdown table shows which microservices had the
most activity. You can see feed-orchestrator had 5 releases.

This is print-ready - let me show you print preview. Notice the layout
stays clean and page breaks are in the right places.

Phase 4 will add charts to visualize this data, but even without
charts this report is ready to present to management."
```

---

## Next Phase

**Phase 4: Visualization**

Adds:
- Matplotlib chart generation
- Month-over-month comparison chart
- Project breakdown charts
- Change type pie chart
- Timeline visualization
- Chart integration into template

---

## Time Box

**Maximum time:** 3 days

If taking longer:
- Simplify template styling
- Skip responsive features
- Use basic table layouts
- Add fancy styling in Phase 4

The goal is **functional HTML reports**, not design perfection.
