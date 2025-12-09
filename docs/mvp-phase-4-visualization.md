# Phase 4: Visualization

## Purpose

Add professional charts and visualizations to enhance report presentation and make data insights immediately clear to management.

## Duration

3-4 days

## Dependencies

- Phase 3 complete (HTML reports working)
- Matplotlib installed
- Sample data available

---

## Goals

- [x] Chart generation using matplotlib
- [x] Month-over-month comparison bar chart
- [x] Per-project breakdown charts
- [x] Change type distribution pie chart
- [x] Release timeline chart
- [x] Consistent styling and color scheme
- [x] PDF-friendly static images
- [x] Chart integration into HTML template

---

## Project Structure

```
kpi-reporter/
├── config.yaml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── report_generator.py  # ENHANCED: Generate charts
│   ├── chart_generator.py   # NEW: Chart creation
│   ├── git_analyzer.py
│   ├── config_manager.py
│   ├── project_scanner.py
│   ├── changelog_parser.py
│   └── data_aggregator.py
├── templates/
│   └── report.html          # ENHANCED: Chart sections
├── reports/
│   ├── kpi-report-2025-11.html
│   └── .charts/             # NEW: Chart storage
│       ├── mom-comparison-2025-11.png
│       ├── project-releases-2025-11.png
│       ├── change-types-2025-11.png
│       └── timeline-2025-11.png
├── tests/
│   └── test_chart_generator.py  # NEW
└── requirements.txt         # UPDATED: Add matplotlib
```

---

## Implementation Tasks

### Task 4.1: Chart Generator Core

**File:** `src/chart_generator.py`

**See:** `docs/task-2-report-generation.md` for complete specification

**Setup and configuration:**

```python
"""
Chart generation for KPI reports using matplotlib.

All charts are static PNG images suitable for PDF export.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Consistent styling
plt.style.use('seaborn-v0_8-darkgrid')

CHART_STYLE = {
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
    "savefig.facecolor": "white"
}

COLOR_PALETTE = {
    "primary": "#2C3E50",
    "secondary": "#3498DB",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "purple": "#9B59B6",
    "teal": "#1ABC9C",
    # Change type colors
    "added": "#27AE60",
    "fixed": "#3498DB",
    "changed": "#F39C12",
    "removed": "#E74C3C"
}


def setup_chart_style():
    """Apply consistent styling to all charts."""
    plt.rcParams.update(CHART_STYLE)
```

**Success criteria:**
- Matplotlib configured correctly
- Non-interactive backend works
- Styling is consistent
- Colors are accessible

---

### Task 4.2: Month-over-Month Comparison Chart

**Function:**

```python
def generate_mom_comparison_chart(
    current_metrics: Dict[str, int],
    previous_metrics: Dict[str, int],
    period: str,
    output_path: Path
) -> Path:
    """
    Generate month-over-month comparison bar chart.

    Shows current period vs previous period for:
    - Releases
    - Commits
    - Lines changed (added + removed)

    :param current_metrics: Dict with 'releases', 'commits', 'lines_changed'
    :param previous_metrics: Same structure for previous period
    :param period: Period identifier for filename
    :param output_path: Directory to save chart
    :return: Path to saved PNG file
    """
    setup_chart_style()

    categories = ['Releases', 'Commits', 'Lines Changed']
    current_values = [
        current_metrics['releases'],
        current_metrics['commits'],
        current_metrics['lines_changed']
    ]
    previous_values = [
        previous_metrics['releases'],
        previous_metrics['commits'],
        previous_metrics['lines_changed']
    ]

    x = range(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(
        [i - width/2 for i in x],
        current_values,
        width,
        label='Current Period',
        color=COLOR_PALETTE['secondary']
    )

    bars2 = ax.bar(
        [i + width/2 for i in x],
        previous_values,
        width,
        label='Previous Period',
        color=COLOR_PALETTE['primary'],
        alpha=0.7
    )

    ax.set_xlabel('Metric')
    ax.set_ylabel('Count')
    ax.set_title('Month-over-Month Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height):,}',
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.tight_layout()

    # Save
    output_file = output_path / f"mom-comparison-{period}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return output_file
```

**Test:**
- Chart generates correctly
- Labels are readable
- Values match input
- File saves successfully

---

### Task 4.3: Project Breakdown Chart

**Function:**

```python
def generate_project_breakdown_chart(
    projects: List[Dict[str, any]],
    metric: str,
    period: str,
    output_path: Path
) -> Path:
    """
    Generate horizontal bar chart for project metrics.

    Projects sorted by metric value (highest first).

    :param projects: List of dicts with 'name' and metric keys
    :param metric: 'releases', 'commits', or 'lines_changed'
    :param period: Period identifier
    :param output_path: Save directory
    :return: Path to saved PNG
    """
    setup_chart_style()

    # Sort by metric (descending)
    sorted_projects = sorted(
        projects,
        key=lambda p: p[metric],
        reverse=True
    )

    names = [p['name'] for p in sorted_projects]
    values = [p[metric] for p in sorted_projects]

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, max(6, len(names) * 0.4)))

    bars = ax.barh(names, values, color=COLOR_PALETTE['secondary'])

    # Color top performer differently
    if bars:
        bars[0].set_color(COLOR_PALETTE['success'])

    ax.set_xlabel(metric.replace('_', ' ').title())
    ax.set_ylabel('Service')
    ax.set_title(f'{metric.replace("_", " ").title()} by Service')

    # Add value labels
    for i, (name, value) in enumerate(zip(names, values)):
        ax.text(
            value,
            i,
            f'  {value:,}',
            va='center',
            fontsize=9
        )

    plt.tight_layout()

    # Save
    output_file = output_path / f"project-{metric}-{period}.png"
    plt.savefig(output_file)
    plt.close()

    return output_file
```

---

### Task 4.4: Change Type Pie Chart

**Function:**

```python
def generate_change_type_pie_chart(
    distribution: Dict[str, int],
    period: str,
    output_path: Path
) -> Path:
    """
    Generate pie chart showing change type distribution.

    :param distribution: Dict mapping change types to counts
    :param period: Period identifier
    :param output_path: Save directory
    :return: Path to saved PNG
    """
    setup_chart_style()

    labels = list(distribution.keys())
    values = list(distribution.values())

    # Map change types to colors
    colors = [
        COLOR_PALETTE.get(label.lower(), COLOR_PALETTE['primary'])
        for label in labels
    ]

    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 11}
    )

    # Make percentage labels bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')

    ax.set_title('Change Type Distribution', pad=20)

    plt.tight_layout()

    # Save
    output_file = output_path / f"change-types-{period}.png"
    plt.savefig(output_file)
    plt.close()

    return output_file
```

---

### Task 4.5: Timeline Chart

**Function:**

```python
def generate_timeline_chart(
    timeline_data: List[Tuple[datetime, int]],
    metric_name: str,
    period: str,
    output_path: Path
) -> Path:
    """
    Generate timeline bar chart showing metric over time.

    :param timeline_data: List of (date, value) tuples
    :param metric_name: Name of metric being displayed
    :param period: Period identifier
    :param output_path: Save directory
    :return: Path to saved PNG
    """
    setup_chart_style()

    if not timeline_data:
        # Create empty chart with message
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No data available',
                ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    else:
        dates = [d for d, _ in timeline_data]
        values = [v for _, v in timeline_data]

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(dates, values, width=20, color=COLOR_PALETTE['secondary'])

        ax.set_xlabel('Date')
        ax.set_ylabel(metric_name)
        ax.set_title(f'{metric_name} Over Time')

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45, ha='right')

        # Add grid
        ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save
    output_file = output_path / f"timeline-{period}.png"
    plt.savefig(output_file)
    plt.close()

    return output_file
```

---

### Task 4.6: Integrate Charts into Report

**Update:** `src/report_generator.py`

**Add chart generation:**

```python
def generate_all_charts(
    report_data: ReportData,
    period: str,
    output_dir: Path
) -> Dict[str, str]:
    """
    Generate all charts for report.

    Returns dict mapping chart names to relative paths for HTML.
    """
    chart_dir = output_dir / ".charts"
    chart_dir.mkdir(exist_ok=True)

    chart_paths = {}

    # 1. Month-over-month comparison (if previous period available)
    if report_data.previous_summary:
        current = {
            'releases': report_data.summary.total_releases,
            'commits': report_data.summary.total_commits,
            'lines_changed': (report_data.summary.total_lines_added +
                            report_data.summary.total_lines_removed)
        }
        previous = {
            'releases': report_data.previous_summary.total_releases,
            'commits': report_data.previous_summary.total_commits,
            'lines_changed': (report_data.previous_summary.total_lines_added +
                             report_data.previous_summary.total_lines_removed)
        }

        path = generate_mom_comparison_chart(current, previous, period, chart_dir)
        chart_paths['mom_comparison'] = f".charts/{path.name}"

    # 2. Project breakdown (releases)
    projects_data = [
        {
            'name': p.name,
            'releases': p.releases,
            'commits': p.commits,
            'lines_changed': p.lines_added + p.lines_removed
        }
        for p in report_data.projects
    ]

    if projects_data:
        path = generate_project_breakdown_chart(
            projects_data, 'releases', period, chart_dir
        )
        chart_paths['project_releases'] = f".charts/{path.name}"

    # 3. Change type distribution
    if report_data.change_distribution:
        path = generate_change_type_pie_chart(
            report_data.change_distribution,
            period,
            chart_dir
        )
        chart_paths['change_types'] = f".charts/{path.name}"

    # 4. Timeline (optional - requires historical data)
    # Implementation depends on data structure

    return chart_paths


def generate_report(
    collected_data: CollectedData,
    period: str,
    output_dir: Path
) -> Path:
    """Generate complete report with charts."""
    # Prepare data
    report_data = prepare_report_data(collected_data, period)

    # Generate charts
    chart_paths = generate_all_charts(report_data, period, output_dir)

    # Render template with chart paths
    html_content = render_template(report_data, chart_paths)

    # Save
    output_path = output_dir / f"kpi-report-{period}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path
```

**Update template:** `templates/report.html`

**Add chart sections:**

```html
<!-- Month-over-Month Comparison -->
{% if charts.mom_comparison %}
<section id="mom-comparison" class="page-break">
    <h2>Month-over-Month Comparison</h2>
    <div class="chart-container">
        <img src="{{ charts.mom_comparison }}"
             alt="Month-over-Month Comparison"
             style="max-width: 100%; height: auto;">
    </div>
</section>
{% endif %}

<!-- Project Breakdown -->
{% if charts.project_releases %}
<section id="project-breakdown">
    <h2>Releases by Service</h2>
    <div class="chart-container">
        <img src="{{ charts.project_releases }}"
             alt="Releases by Service"
             style="max-width: 100%; height: auto;">
    </div>
</section>
{% endif %}

<!-- Change Type Distribution -->
{% if charts.change_types %}
<section id="change-distribution">
    <h2>Change Type Distribution</h2>
    <div class="chart-container">
        <img src="{{ charts.change_types }}"
             alt="Change Type Distribution"
             style="max-width: 100%; height: auto;">
    </div>
</section>
{% endif %}
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_chart_generator.py

def test_mom_comparison_chart_generation(tmp_path):
    """Test month-over-month chart generates correctly."""
    current = {'releases': 10, 'commits': 50, 'lines_changed': 1000}
    previous = {'releases': 8, 'commits': 40, 'lines_changed': 800}

    output = generate_mom_comparison_chart(
        current, previous, "2025-11", tmp_path
    )

    assert output.exists()
    assert output.suffix == ".png"


def test_project_breakdown_chart(tmp_path):
    """Test project breakdown chart generation."""
    projects = [
        {'name': 'service-a', 'releases': 5, 'commits': 20, 'lines_changed': 500},
        {'name': 'service-b', 'releases': 3, 'commits': 15, 'lines_changed': 300},
    ]

    output = generate_project_breakdown_chart(
        projects, 'releases', "2025-11", tmp_path
    )

    assert output.exists()


def test_change_type_pie_chart(tmp_path):
    """Test pie chart generation."""
    distribution = {
        'Fixed': 20,
        'Added': 15,
        'Changed': 10,
        'Removed': 5
    }

    output = generate_change_type_pie_chart(
        distribution, "2025-11", tmp_path
    )

    assert output.exists()
```

---

## Exit Criteria

- [ ] All chart types generate correctly
- [ ] Charts are PDF-friendly (static PNG)
- [ ] Consistent styling across all charts
- [ ] Charts integrate into HTML template
- [ ] Print/PDF export includes charts
- [ ] Performance acceptable (<30s total)
- [ ] Charts enhance understanding
- [ ] Tests pass for all chart types
- [ ] Manual validation with real data
- [ ] Ready for production use

---

## Final Demo

**Complete system demonstration:**

```bash
# Generate report
python -m src.main --period 2025-11

# Output shows:
✓ Configuration loaded
✓ 8 projects scanned
✓ Changelogs parsed
✓ Git metrics analyzed
✓ Generating charts...
  → Month-over-month comparison
  → Project breakdown
  → Change type distribution
  → Timeline
✓ Report generated: reports/kpi-report-2025-11.html
```

**Show in browser:**
- Professional layout
- Summary metrics
- Multiple charts
- Data tables
- Warnings section

**Export to PDF:**
- Print preview
- Clean page breaks
- All charts visible
- Professional appearance

---

## Project Complete ✅

MVP delivers:
- Automated KPI report generation
- Multi-project git and changelog analysis
- Professional HTML output
- Visual charts and tables
- PDF-ready format
- Configurable via YAML
- Command-line interface
- Comprehensive testing

**Ready for production use!**
