"""
Chart generation for KPI reports using matplotlib.

All charts are static PNG images suitable for PDF export and HTML embedding.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server/CLI use

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

#: Apply seaborn style for professional appearance
plt.style.use('seaborn-v0_8-darkgrid')

#: Consistent styling across all charts
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

#: Color palette matching HTML report theme
COLOR_PALETTE = {
    "primary": "#2C3E50",      # Dark blue-gray
    "secondary": "#3498DB",    # Blue (matches HTML theme)
    "success": "#27AE60",      # Green
    "warning": "#F39C12",      # Orange
    "danger": "#E74C3C",       # Red
    "purple": "#9B59B6",       # Purple (matches HTML gradient)
    "teal": "#1ABC9C",         # Teal
}


def setup_chart_style():
    """
    Apply consistent styling to all charts.

    :Example:

    >>> setup_chart_style()
    >>> plt.plot([1, 2, 3])
    """
    plt.rcParams.update(CHART_STYLE)


def generate_project_breakdown_chart(
    projects: List[Dict[str, Any]],
    metric: str,
    period: str,
    output_path: Path
) -> Path:
    """
    Generate horizontal bar chart for project metrics.

    Projects sorted by metric value (highest first) with the top
    performer highlighted in green.

    :param projects: List of dicts with 'name' and metric keys
    :type projects: List[Dict[str, Any]]
    :param metric: Metric to visualize ('total_commits', 'total_lines_added', etc.)
    :type metric: str
    :param period: Period identifier for filename
    :type period: str
    :param output_path: Directory to save chart
    :type output_path: Path
    :return: Path to saved PNG file
    :rtype: Path

    :Example:

    >>> projects = [
    ...     {'name': 'service-a', 'total_commits': 50},
    ...     {'name': 'service-b', 'total_commits': 30}
    ... ]
    >>> path = generate_project_breakdown_chart(
    ...     projects, 'total_commits', 'all', Path('reports')
    ... )
    """
    setup_chart_style()

    #: Sort projects by metric value (descending)
    sorted_projects = sorted(
        projects,
        key=lambda p: p.get(metric, 0),
        reverse=True
    )

    names = [p['name'] for p in sorted_projects]
    values = [p.get(metric, 0) for p in sorted_projects]

    #: Create horizontal bar chart with dynamic height
    fig_height = max(6, len(names) * 0.5)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    bars = ax.barh(names, values, color=COLOR_PALETTE['secondary'])

    #: Highlight top performer in green
    if bars:
        bars[0].set_color(COLOR_PALETTE['success'])

    #: Format labels
    metric_label = metric.replace('_', ' ').replace('total ', '').title()
    ax.set_xlabel(metric_label)
    ax.set_ylabel('Service')
    ax.set_title(f'{metric_label} by Service')

    #: Add value labels on bars
    for i, (name, value) in enumerate(zip(names, values)):
        ax.text(
            value,
            i,
            f'  {value:,}',
            va='center',
            fontsize=9
        )

    plt.tight_layout()

    #: Save chart
    output_file = output_path / f"project-{metric}-{period}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return output_file


def generate_timeline_chart(
    timeline_data: List[Tuple[datetime, str]],
    period: str,
    output_path: Path
) -> Path:
    """
    Generate timeline chart showing releases over time.

    Each release is represented as a marker on the timeline,
    grouped by month.

    :param timeline_data: List of (date, version) tuples for releases
    :type timeline_data: List[Tuple[datetime, str]]
    :param period: Period identifier for filename
    :type period: str
    :param output_path: Directory to save chart
    :type output_path: Path
    :return: Path to saved PNG file
    :rtype: Path

    :Example:

    >>> from datetime import datetime
    >>> timeline = [
    ...     (datetime(2025, 11, 1), "1.0.0"),
    ...     (datetime(2025, 11, 15), "1.1.0")
    ... ]
    >>> path = generate_timeline_chart(timeline, 'all', Path('reports'))
    """
    setup_chart_style()

    if not timeline_data:
        #: Create empty chart with message
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(
            0.5, 0.5,
            'No release data available',
            ha='center',
            va='center',
            fontsize=14,
            color=COLOR_PALETTE['primary']
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    else:
        dates = [d for d, _ in timeline_data]
        versions = [v for _, v in timeline_data]

        #: Count releases per month for histogram
        from collections import Counter
        month_counts = Counter([d.strftime('%Y-%m') for d in dates])
        months = sorted(month_counts.keys())
        counts = [month_counts[m] for m in months]
        month_dates = [datetime.strptime(m, '%Y-%m') for m in months]

        fig, ax = plt.subplots(figsize=(12, 6))

        #: Bar chart showing releases per month
        #: Width of 25 days makes monthly bars more prominent
        ax.bar(
            month_dates,
            counts,
            width=25,
            color=COLOR_PALETTE['secondary'],
            alpha=0.7,
            edgecolor=COLOR_PALETTE['primary']
        )

        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Releases')
        ax.set_title('Release Activity Over Time')

        #: Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45, ha='right')

        #: Add grid for better readability
        ax.grid(True, alpha=0.3, axis='y')

        #: Add value labels on bars
        for date, count in zip(month_dates, counts):
            ax.text(
                date,
                count,
                str(count),
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.tight_layout()

    #: Save chart
    output_file = output_path / f"timeline-{period}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return output_file


def generate_commit_timeline_chart(
    commit_data: List[Tuple[datetime, int]],
    period: str,
    output_path: Path
) -> Path:
    """
    Generate timeline chart showing commits over time.

    Commits are aggregated by month to show development activity patterns.
    Complements the release timeline to reveal development intensity vs
    release frequency patterns.

    :param commit_data: List of (date, commit_count) tuples
    :type commit_data: List[Tuple[datetime, int]]
    :param period: Period identifier for filename
    :type period: str
    :param output_path: Directory to save chart
    :type output_path: Path
    :return: Path to saved PNG file
    :rtype: Path

    :Example:

    >>> from datetime import datetime
    >>> commits = [
    ...     (datetime(2025, 11, 1), 23),
    ...     (datetime(2025, 11, 15), 12),
    ...     (datetime(2025, 10, 1), 45)
    ... ]
    >>> path = generate_commit_timeline_chart(commits, 'all', Path('reports'))
    """
    setup_chart_style()

    if not commit_data:
        #: Create empty chart with message
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(
            0.5, 0.5,
            'No commit data available',
            ha='center',
            va='center',
            fontsize=14,
            color=COLOR_PALETTE['primary']
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    else:
        #: Aggregate commits by month (multiple releases in same month)
        from collections import defaultdict
        month_commits = defaultdict(int)
        for date, commits in commit_data:
            month_key = date.strftime('%Y-%m')
            month_commits[month_key] += commits

        #: Sort months chronologically
        months = sorted(month_commits.keys())
        month_dates = [datetime.strptime(m, '%Y-%m') for m in months]
        commit_counts = [month_commits[m] for m in months]

        #: Create bar chart - same size as release timeline for alignment
        fig, ax = plt.subplots(figsize=(12, 6))

        #: Use teal color to distinguish from release timeline (blue)
        #: Width of 25 days makes monthly bars more prominent
        ax.bar(
            month_dates,
            commit_counts,
            width=25,
            color=COLOR_PALETTE['teal'],
            alpha=0.7,
            edgecolor=COLOR_PALETTE['primary']
        )

        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Commits')
        ax.set_title('Commit Activity Over Time')

        #: Format x-axis identically to release timeline for vertical alignment
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45, ha='right')

        #: Add grid for better readability
        ax.grid(True, alpha=0.3, axis='y')

        #: Add value labels on bars
        for date, count in zip(month_dates, commit_counts):
            ax.text(
                date,
                count,
                str(count),
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.tight_layout()

    #: Save chart
    output_file = output_path / f"commit-timeline-{period}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return output_file


def generate_release_activity_chart(
    summary_data: Dict[str, int],
    period: str,
    output_path: Path
) -> Path:
    """
    Generate release activity chart showing releases and commits.

    Creates a bar chart showing total releases and commits
    (metrics with similar scale).

    :param summary_data: Dict with 'total_releases', 'total_commits'
    :type summary_data: Dict[str, int]
    :param period: Period identifier for filename
    :type period: str
    :param output_path: Directory to save chart
    :type output_path: Path
    :return: Path to saved PNG file
    :rtype: Path

    :Example:

    >>> summary = {'total_releases': 15, 'total_commits': 156}
    >>> path = generate_release_activity_chart(summary, 'all', Path('reports'))
    """
    setup_chart_style()

    #: Prepare data
    metrics = [
        ('Releases', summary_data.get('total_releases', 0)),
        ('Commits', summary_data.get('total_commits', 0))
    ]

    labels = [m[0] for m in metrics]
    values = [m[1] for m in metrics]

    #: Create bar chart (compact height for print layout)
    fig, ax = plt.subplots(figsize=(8, 4))

    colors = [COLOR_PALETTE['secondary'], COLOR_PALETTE['primary']]

    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', width=0.6)

    ax.set_ylabel('Count')
    ax.set_title('Release Activity')

    #: Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{value:,}',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold'
        )

    plt.tight_layout()

    #: Save chart
    output_file = output_path / f"release-activity-{period}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return output_file


def generate_code_volume_chart(
    summary_data: Dict[str, int],
    period: str,
    output_path: Path
) -> Path:
    """
    Generate code volume chart showing lines added, removed, and net change.

    Creates a bar chart showing lines added, lines removed, and net change
    (metrics with similar scale).

    :param summary_data: Dict with 'total_lines_added', 'total_lines_removed'
    :type summary_data: Dict[str, int]
    :param period: Period identifier for filename
    :type period: str
    :param output_path: Directory to save chart
    :type output_path: Path
    :return: Path to saved PNG file
    :rtype: Path

    :Example:

    >>> summary = {
    ...     'total_lines_added': 41493,
    ...     'total_lines_removed': 5060
    ... }
    >>> path = generate_code_volume_chart(summary, 'all', Path('reports'))
    """
    setup_chart_style()

    #: Calculate net change
    lines_added = summary_data.get('total_lines_added', 0)
    lines_removed = summary_data.get('total_lines_removed', 0)
    net_change = lines_added - lines_removed

    #: Prepare data
    metrics = [
        ('Lines Added', lines_added),
        ('Lines Removed', lines_removed),
        ('Net Change', net_change)
    ]

    labels = [m[0] for m in metrics]
    values = [m[1] for m in metrics]

    #: Create bar chart (compact height for print layout)
    fig, ax = plt.subplots(figsize=(9, 4))

    colors = [
        COLOR_PALETTE['success'],   # Green for added
        COLOR_PALETTE['danger'],     # Red for removed
        COLOR_PALETTE['secondary']   # Blue for net change
    ]

    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', width=0.6)

    ax.set_ylabel('Lines of Code')
    ax.set_title('Code Volume')

    #: Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{value:,}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    #: Add horizontal line at zero for reference
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

    plt.tight_layout()

    #: Save chart
    output_file = output_path / f"code-volume-{period}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return output_file
