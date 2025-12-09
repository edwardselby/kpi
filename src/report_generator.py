"""
HTML report generation for KPI metrics.

Transforms collected git metrics into professional HTML reports using Jinja2
with embedded matplotlib charts.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.chart_generator import (
    generate_project_breakdown_chart,
    generate_timeline_chart,
    generate_release_activity_chart,
    generate_code_volume_chart,
    generate_commit_timeline_chart
)
from src.narrative_generator import generate_executive_summary


def _parse_period_to_date_range(period: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Parse period string to date range.

    Converts period specifications into start and end datetime objects
    for filtering releases and commits by time period.

    :param period: Period string ("all", "YYYY", "YYYY-MM", "YYYY-QN")
    :type period: str
    :return: Tuple of (start_date, end_date) or (None, None) for "all"
    :rtype: Tuple[Optional[datetime], Optional[datetime]]

    :Example:

    >>> _parse_period_to_date_range("2025")
    (datetime(2025, 1, 1, 0, 0), datetime(2025, 12, 31, 23, 59, 59))
    >>> _parse_period_to_date_range("2025-11")
    (datetime(2025, 11, 1, 0, 0), datetime(2025, 11, 30, 23, 59, 59))
    >>> _parse_period_to_date_range("2025-Q4")
    (datetime(2025, 10, 1, 0, 0), datetime(2025, 12, 31, 23, 59, 59))
    >>> _parse_period_to_date_range("all")
    (None, None)
    """
    from calendar import monthrange

    if period == "all":
        return None, None

    #: Quarterly format: YYYY-QN
    if "-Q" in period:
        try:
            year, quarter = period.split("-Q")
            year = int(year)
            quarter = int(quarter)

            #: Map quarter to month range
            quarter_months = {
                1: (1, 3),   # Q1: Jan-Mar
                2: (4, 6),   # Q2: Apr-Jun
                3: (7, 9),   # Q3: Jul-Sep
                4: (10, 12)  # Q4: Oct-Dec
            }

            if quarter not in quarter_months:
                print(f"⚠️  Warning: Invalid quarter '{quarter}' in period '{period}', showing all data")
                return None, None

            start_month, end_month = quarter_months[quarter]
            start_date = datetime(year, start_month, 1)

            #: Get last day of end month
            last_day = monthrange(year, end_month)[1]
            end_date = datetime(year, end_month, last_day, 23, 59, 59)

            return start_date, end_date
        except (ValueError, IndexError) as e:
            print(f"⚠️  Warning: Invalid period format '{period}', showing all data")
            return None, None

    #: Yearly format: YYYY (e.g., "2025")
    if len(period) == 4 and period.isdigit():
        try:
            year = int(period)
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31, 23, 59, 59)
            return start_date, end_date
        except ValueError:
            print(f"⚠️  Warning: Invalid year '{period}', showing all data")
            return None, None

    #: Monthly format: YYYY-MM
    try:
        year, month = period.split("-")
        year, month = int(year), int(month)

        if not (1 <= month <= 12):
            print(f"⚠️  Warning: Invalid month '{month}' in period '{period}', showing all data")
            return None, None

        start_date = datetime(year, month, 1)
        last_day = monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)

        return start_date, end_date
    except (ValueError, IndexError):
        #: Invalid format - return None (no filtering)
        print(f"⚠️  Warning: Invalid period format '{period}', showing all data")
        return None, None


def _generate_all_charts(
    projects_data: List[Dict[str, Any]],
    report_data: Dict[str, Any],
    period: str,
    output_dir: Path
) -> Dict[str, str]:
    """
    Generate all charts for the report.

    Creates project breakdown charts, timeline chart, and summary chart.
    Returns dict mapping chart names to relative paths for HTML embedding.

    :param projects_data: List of project data dictionaries
    :type projects_data: List[Dict[str, Any]]
    :param report_data: Prepared report data with totals
    :type report_data: Dict[str, Any]
    :param period: Period identifier
    :type period: str
    :param output_dir: Output directory for HTML report
    :type output_dir: Path
    :return: Dict mapping chart names to relative file paths
    :rtype: Dict[str, str]
    """
    #: Create charts subdirectory
    chart_dir = output_dir / ".charts"
    chart_dir.mkdir(parents=True, exist_ok=True)

    chart_paths = {}

    #: 1. Release Activity chart (Releases + Commits)
    activity_data = {
        'total_releases': report_data['total_releases'],
        'total_commits': report_data['total_commits']
    }

    path = generate_release_activity_chart(activity_data, period, chart_dir)
    chart_paths['release_activity'] = f".charts/{path.name}"

    #: 2. Code Volume chart (Lines Added/Removed + Net Change)
    volume_data = {
        'total_lines_added': report_data['total_lines_added'],
        'total_lines_removed': report_data['total_lines_removed']
    }

    path = generate_code_volume_chart(volume_data, period, chart_dir)
    chart_paths['code_volume'] = f".charts/{path.name}"

    #: 3. Project breakdown charts (commits and lines added)
    if projects_data:
        #: Commits breakdown
        path = generate_project_breakdown_chart(
            projects_data,
            'total_commits',
            period,
            chart_dir
        )
        chart_paths['project_commits'] = f".charts/{path.name}"

        #: Lines added breakdown
        path = generate_project_breakdown_chart(
            projects_data,
            'total_lines_added',
            period,
            chart_dir
        )
        chart_paths['project_lines_added'] = f".charts/{path.name}"

        #: Net change breakdown
        path = generate_project_breakdown_chart(
            projects_data,
            'net_change',
            period,
            chart_dir
        )
        chart_paths['project_net_change'] = f".charts/{path.name}"

    #: 4. Release timeline chart
    #: Collect all releases with dates
    timeline_data = []
    for project in projects_data:
        for release in project.get('releases', []):
            if release.get('date'):
                #: Parse date string to datetime
                date_str = release['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                timeline_data.append((date_obj, release['version']))

    if timeline_data:
        path = generate_timeline_chart(timeline_data, period, chart_dir)
        chart_paths['timeline'] = f".charts/{path.name}"

    #: 5. Commit timeline chart
    #: Note: Uses actual commit dates (when commits were made)
    #: not release dates (when tags were created) for accurate timeline
    #: Filter to match the date range of releases being shown

    #: Find earliest and latest release dates
    release_dates = []
    for project in projects_data:
        for release in project.get('releases', []):
            if release.get('date'):
                date_obj = datetime.strptime(release['date'], '%Y-%m-%d')
                release_dates.append(date_obj)

    if release_dates:
        earliest_release = min(release_dates)
        latest_release = max(release_dates)
    else:
        earliest_release = datetime.now()
        latest_release = datetime.now()

    commit_timeline_data = []
    for project in projects_data:
        #: Collect commits from releases (between tags)
        for release in project.get('releases', []):
            #: Use individual commit dates (not release tag date)
            for commit_date in release.get('commit_dates', []):
                #: Only include commits within release date range
                if earliest_release <= commit_date <= latest_release:
                    commit_timeline_data.append((commit_date, 1))

        #: Also collect commits after most recent tag (unreleased commits)
        if project.get('releases'):
            most_recent_release = project['releases'][0]  # First release is newest
            if most_recent_release.get('unreleased_commits'):
                for commit_date in most_recent_release['unreleased_commits']:
                    if earliest_release <= commit_date <= latest_release:
                        commit_timeline_data.append((commit_date, 1))

    if commit_timeline_data:
        path = generate_commit_timeline_chart(commit_timeline_data, period, chart_dir)
        chart_paths['commit_timeline'] = f".charts/{path.name}"

    return chart_paths


def _filter_active_projects(projects_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter out projects with no meaningful activity.

    Excludes projects where all metrics are zero (no commits, no line changes).
    This prevents empty/inactive projects from cluttering charts and tables.

    :param projects_data: List of all project data dictionaries
    :type projects_data: List[Dict[str, Any]]
    :return: Filtered list containing only projects with activity
    :rtype: List[Dict[str, Any]]

    :Example:

    >>> projects = [
    ...     {'name': 'active', 'total_commits': 10, 'total_lines_added': 100, 'total_lines_removed': 50},
    ...     {'name': 'inactive', 'total_commits': 0, 'total_lines_added': 0, 'total_lines_removed': 0}
    ... ]
    >>> _filter_active_projects(projects)
    [{'name': 'active', 'total_commits': 10, ...}]
    """
    active_projects = []

    for project in projects_data:
        #: Include project if it has any activity
        has_commits = project.get('total_commits', 0) > 0
        has_lines_added = project.get('total_lines_added', 0) > 0
        has_lines_removed = project.get('total_lines_removed', 0) > 0

        if has_commits or has_lines_added or has_lines_removed:
            active_projects.append(project)

    return active_projects


def generate_html_report(
    projects_data: List[Dict[str, Any]],
    output_dir: Path,
    period: str = "all",
    config: Any = None
) -> Path:
    """
    Generate HTML report from project data.

    :param projects_data: List of project dictionaries with metrics
    :type projects_data: List[Dict[str, Any]]
    :param output_dir: Directory to save report
    :type output_dir: Path
    :param period: Report period (e.g., "2025-11", "all")
    :type period: str
    :return: Path to generated HTML file
    :rtype: Path

    :Example:

    >>> projects = [
    ...     {
    ...         'name': 'api-gateway-service',
    ...         'releases': [...],
    ...         'total_commits': 67,
    ...         'total_lines_added': 13221,
    ...         'total_lines_removed': 485
    ...     }
    ... ]
    >>> path = generate_html_report(projects, Path('reports'))
    >>> path.exists()
    True
    """
    #: Filter out projects with no activity
    active_projects = _filter_active_projects(projects_data)

    #: Show filtering summary if projects were excluded
    if len(active_projects) < len(projects_data):
        excluded_count = len(projects_data) - len(active_projects)
        excluded_names = [p['name'] for p in projects_data if p not in active_projects]
        print(f"\n📊 Report Filtering:")
        print(f"   Excluded {excluded_count} project(s) with no activity: {', '.join(excluded_names)}")
        print(f"   Showing {len(active_projects)} active project(s)")

    #: Prepare data for template (use filtered projects)
    report_data = _prepare_report_data(active_projects, period, config)

    #: Generate charts (only for active projects)
    chart_paths = _generate_all_charts(active_projects, report_data, period, output_dir)

    #: Load and render template with charts
    html_content = _render_template(report_data, chart_paths)

    #: Save to file
    output_path = _save_report(html_content, output_dir, period)

    return output_path


def _prepare_report_data(
    projects_data: List[Dict[str, Any]],
    period: str,
    config: Any = None
) -> Dict[str, Any]:
    """
    Transform raw project data into template-ready format.

    Calculates aggregated totals and formats data for display.

    :param projects_data: Raw project data
    :param period: Report period
    :return: Template-ready data dictionary
    """
    #: Calculate aggregate totals
    total_releases = sum(p.get('release_count', 0) for p in projects_data)
    total_commits = sum(p.get('total_commits', 0) for p in projects_data)
    total_lines_added = sum(p.get('total_lines_added', 0) for p in projects_data)
    total_lines_removed = sum(p.get('total_lines_removed', 0) for p in projects_data)

    #: Format period for display
    period_display = _format_period_display(period)

    #: Generate timestamps
    now = datetime.now()
    generation_date = now.strftime("%B %d, %Y")
    generation_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    #: Generate executive summary if config provided
    executive_summary = {'has_summary': False}
    if config:
        try:
            executive_summary = generate_executive_summary(
                projects_data,
                {
                    'total_releases': total_releases,
                    'total_commits': total_commits,
                    'total_lines_added': total_lines_added,
                    'total_lines_removed': total_lines_removed,
                    'period_display': period_display
                },
                config
            )
        except Exception as e:
            print(f"⚠️  Warning: Could not generate executive summary: {e}")

    return {
        'period': period,
        'period_display': period_display,
        'generation_date': generation_date,
        'generation_timestamp': generation_timestamp,
        'total_releases': total_releases,
        'total_commits': total_commits,
        'total_lines_added': total_lines_added,
        'total_lines_removed': total_lines_removed,
        'projects': projects_data,
        'warnings': [],  # Placeholder for future warning system
        'executive_summary': executive_summary
    }


def _format_period_display(period: str) -> str:
    """
    Convert period code to human-readable format.

    :param period: Period code (e.g., "2025-11", "all")
    :return: Human-readable period string

    :Example:

    >>> _format_period_display("2025-11")
    'November 2025'
    >>> _format_period_display("all")
    'All Time'
    """
    if period == "all":
        return "All Time"

    if period.startswith("Q"):
        return period  # "Q4 2025"

    #: Month format: 2025-11
    try:
        date = datetime.strptime(period, "%Y-%m")
        return date.strftime("%B %Y")
    except:
        return period


def _render_template(
    report_data: Dict[str, Any],
    chart_paths: Dict[str, str]
) -> str:
    """
    Load Jinja2 template and render with data and charts.

    :param report_data: Template data dictionary
    :param chart_paths: Dict mapping chart names to relative paths
    :return: Rendered HTML string
    """
    #: Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )

    #: Load template
    template = env.get_template('report.html')

    #: Render with data and charts
    return template.render(**report_data, charts=chart_paths)


def _save_report(
    html_content: str,
    output_dir: Path,
    period: str
) -> Path:
    """
    Save HTML content to file with proper naming.

    Creates output directory if it doesn't exist.

    :param html_content: Rendered HTML string
    :param output_dir: Output directory
    :param period: Report period (for filename)
    :return: Path to saved file
    """
    #: Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    #: Generate filename
    filename = f"kpi-report-{period}.html"
    output_path = output_dir / filename

    #: Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path
