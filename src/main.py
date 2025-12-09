"""
KPI Report Generator - Phase 3 with HTML Reports

Console and HTML-based KPI reporting showing git release metrics from microservices.
"""

import argparse
import sys
from pathlib import Path
from src.git_analyzer import get_tags, count_commits_between, calculate_line_changes, fetch_repository
from src.config_manager import load_config
from src.report_generator import generate_html_report


def parse_arguments():
    """
    Parse command-line arguments.

    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog="kpi",
        description="""
KPI Report Generator - Phase 4: Data Visualization with Charts

Analyzes git repositories to generate professional KPI reports with:
  • Release history tracking (semantic versioning)
  • Commit counting between releases
  • Line change tracking (added/removed) with file exclusions
  • Professional HTML reports with embedded charts
  • Console output for quick checks
  • Matplotlib visualizations (project breakdowns, timelines, summaries)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kpi                                   # Console output (default)
  kpi --html                            # HTML report with charts
  kpi --html --period all               # HTML report for all time
  kpi --html --period 2025              # HTML report for year 2025
  kpi --html --period 2025-Q4           # HTML report for Q4 2025
  kpi --html --period 2025-11           # HTML report for November 2025
  kpi --html -o ./reports/monthly       # Custom output directory
  kpi --html --no-fetch                 # Skip git fetch (use local tags only)

Configuration:
  Edit config.yaml to customize:
    - projects_directory: Path to repositories
    - included_projects: Which repos to analyze
    - file_exclusions: Files to exclude from line counts
    - report_output: Default output directory

Output Formats:
  Console: Quick summary in terminal
  HTML:    Professional report with embedded charts (5 visualizations)
           - Summary metrics bar chart
           - Commits by service comparison
           - Lines added by service comparison
           - Net change by service comparison
           - Release activity timeline

Generated Charts:
  All charts saved as PNG files in reports/.charts/
  - Print/PDF friendly (static images, 150 DPI)
  - Consistent styling matching HTML theme
  - Top performers highlighted in green

For more information, see README.md or docs/ directory.
        """
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report with embedded charts instead of console output"
    )

    parser.add_argument(
        "--period",
        type=str,
        default="all",
        metavar="PERIOD",
        help="Reporting period: YYYY (e.g., 2025), YYYY-MM (e.g., 2025-11), YYYY-QN (e.g., 2025-Q4), or 'all' (default: all)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        metavar="DIR",
        help="Output directory for HTML reports (overrides config.yaml setting)"
    )

    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Skip git fetch (use local tags only, faster for offline use)"
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="KPI Report Generator v4.0.0 (Phase 4: Data Visualization)"
    )

    return parser.parse_args()


def collect_metrics_data(config, enable_fetch: bool = True, period: str = "all"):
    """
    Collect metrics from all configured projects.

    :param config: Configuration object
    :param enable_fetch: Whether to fetch latest tags from remote (default: True)
    :param period: Reporting period for filtering (default: "all")
    :return: List of project data dictionaries
    """
    projects_data = []

    #: Import period parsing function
    from src.report_generator import _parse_period_to_date_range

    #: Parse period to date range for filtering
    period_start, period_end = _parse_period_to_date_range(period)

    #: Build project paths from configuration
    project_paths = [
        config.projects_directory / project_name
        for project_name in config.included_projects
    ]

    total_projects = len(project_paths)

    for index, project_path in enumerate(project_paths, start=1):
        #: Print project progress header
        print(f"\n[{index}/{total_projects}] 🔄 Processing {project_path.name}...")
        #: Validate project exists and is a git repository
        if not project_path.exists():
            continue
        if not (project_path / ".git").exists():
            continue

        #: Fetch latest tags from remote (if enabled)
        if enable_fetch:
            print(f"       📡 Fetching updates...", end=" ", flush=True)
            success, msg = fetch_repository(project_path)
            print(f"{'✅' if success else '⚠️ '} {msg}")

        try:
            print(f"       📊 Analyzing metrics...", end=" ", flush=True)
            #: Get all tags
            tags = get_tags(project_path)
            if not tags:
                continue

            #: Collect release data (all releases)
            releases = []
            total_commits = 0
            total_lines_added = 0
            total_lines_removed = 0

            for i, (tag, date) in enumerate(tags):
                #: Filter by period if specified
                if period_start and period_end:
                    if not (period_start <= date <= period_end):
                        continue  # Skip releases outside period

                if i == 0:
                    #: First tag (newest) - collect unreleased commits from HEAD to this tag
                    unreleased_commits, unreleased_dates = count_commits_between(
                        project_path,
                        tag,
                        'HEAD',
                        return_dates=True
                    )
                    releases.append({
                        'version': tag,
                        'date': date.strftime('%Y-%m-%d'),
                        'commits': None,
                        'lines_added': None,
                        'lines_removed': None,
                        'unreleased_commits': unreleased_dates
                    })
                    continue

                #: Count commits and line changes
                prev_tag = tags[i-1][0]
                commits, commit_dates = count_commits_between(
                    project_path,
                    tag,
                    prev_tag,
                    return_dates=True
                )
                lines_added, lines_removed = calculate_line_changes(
                    project_path,
                    tag,
                    prev_tag,
                    config.file_exclusions
                )

                releases.append({
                    'version': tag,
                    'date': date.strftime('%Y-%m-%d'),
                    'commits': commits,
                    'commit_dates': commit_dates,
                    'lines_added': lines_added,
                    'lines_removed': lines_removed
                })

                total_commits += commits
                total_lines_added += lines_added
                total_lines_removed += lines_removed

            #: Build project summary
            projects_data.append({
                'name': project_path.name,
                'release_count': len(tags),  # All releases
                'total_commits': total_commits,
                'total_lines_added': total_lines_added,
                'total_lines_removed': total_lines_removed,
                'net_change': total_lines_added - total_lines_removed,
                'releases': releases
            })

            #: Print completion status
            print("✅")
            print(f"       ✅ Completed: {len(tags)} releases, "
                  f"{total_commits} commits, +{total_lines_added:,} lines")

        except Exception as e:
            print(f"\n       ⚠️  Error processing {project_path.name}: {e}")
            continue

    return projects_data


def generate_console_output(projects_data, config):
    """
    Generate console output from collected data.

    :param projects_data: List of project data dictionaries
    :param config: Configuration object
    """
    print("=" * 70)
    print("KPI Report Generator - Phase 3 Console Output")
    print("=" * 70)
    print()
    print(f"Configuration: config.yaml")
    print(f"Projects directory: {config.projects_directory}")
    print(f"Analyzed {len(projects_data)} projects")
    print()

    for project in projects_data:
        print(f"📦 {project['name']}")
        print("-" * 70)

        #: Show first 10 releases in console (all releases in HTML)
        display_releases = project['releases'][:10]
        for release in display_releases:
            if release['commits'] is None:
                #: Latest release
                print(f"  {release['version']:12} {release['date']} (latest)")
            else:
                #: Previous releases with metrics
                line_info = f"(+{release['lines_added']:,} / -{release['lines_removed']:,} lines)"
                print(f"  {release['version']:12} {release['date']} → {release['commits']:3d} commits  {line_info}")

        if len(project['releases']) > 10:
            print(f"  ... and {len(project['releases']) - 10} more releases")

        print()


def main():
    """
    Main entry point for KPI report generation.

    Supports both console and HTML output formats.
    """
    args = parse_arguments()

    #: Load configuration
    try:
        config = load_config("config.yaml")
    except FileNotFoundError:
        print("❌ Error: config.yaml not found")
        print("   Please create config.yaml in the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

    #: Show period filtering information
    if args.period != "all":
        from src.report_generator import _parse_period_to_date_range
        period_start, period_end = _parse_period_to_date_range(args.period)
        if period_start and period_end:
            print(f"\n📅 Filtering to period: {args.period}")
            print(f"   Date range: {period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}")

    #: Collect metrics from all projects
    projects_data = collect_metrics_data(config, enable_fetch=not args.no_fetch, period=args.period)

    if not projects_data:
        print("❌ No valid projects found to analyze")
        sys.exit(1)

    #: Generate output based on format
    if args.html:
        #: Determine output directory
        output_dir = Path(args.output) if args.output else config.report_output

        #: Generate HTML report
        output_path = generate_html_report(
            projects_data,
            output_dir,
            args.period,
            config
        )

        print(f"✅ HTML report generated: {output_path}")
        print(f"   Open in browser: file://{output_path.absolute()}")

    else:
        #: Generate console output
        generate_console_output(projects_data, config)


if __name__ == "__main__":
    main()
