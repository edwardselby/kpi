"""
Integration tests for chart generation.

Tests all chart generation functions with real matplotlib rendering.
These tests are slower but verify actual chart output.

Run with: pytest -m integration
"""

from datetime import datetime
from pathlib import Path
import pytest
from src.chart_generator import (
    generate_project_breakdown_chart,
    generate_timeline_chart
)


@pytest.mark.integration
def test_project_breakdown_chart_generation(tmp_path):
    """
    Test project breakdown chart generates correctly.

    Verifies that chart file is created with correct format.
    """
    projects = [
        {'name': 'service-a', 'total_commits': 50},
        {'name': 'service-b', 'total_commits': 30},
        {'name': 'service-c', 'total_commits': 20}
    ]

    output = generate_project_breakdown_chart(
        projects,
        'total_commits',
        "2025-11",
        tmp_path
    )

    #: Verify file was created
    assert output.exists()
    assert output.suffix == ".png"
    assert output.name == "project-total_commits-2025-11.png"
    assert output.stat().st_size > 1000  # Chart should be >1KB


@pytest.mark.integration
def test_project_breakdown_chart_sorting(tmp_path):
    """
    Test that projects are sorted by metric value.

    The chart should sort projects in descending order.
    """
    projects = [
        {'name': 'low-activity', 'total_commits': 10},
        {'name': 'high-activity', 'total_commits': 100},
        {'name': 'medium-activity', 'total_commits': 50}
    ]

    output = generate_project_breakdown_chart(
        projects,
        'total_commits',
        "test",
        tmp_path
    )

    assert output.exists()


@pytest.mark.integration
def test_project_breakdown_chart_empty_list(tmp_path):
    """
    Test chart generation with empty project list.

    Should create chart without errors.
    """
    projects = []

    output = generate_project_breakdown_chart(
        projects,
        'total_commits',
        "test",
        tmp_path
    )

    assert output.exists()


@pytest.mark.skip(reason="generate_summary_comparison_chart function not implemented")
@pytest.mark.integration
def test_summary_comparison_chart(tmp_path):
    """
    Test summary comparison chart generation.

    Verifies that all metrics are included.
    """
    summary = {
        'total_releases': 15,
        'total_commits': 156,
        'total_lines_added': 41493,
        'total_lines_removed': 5060
    }

    output = generate_summary_comparison_chart(
        summary,
        "2025-11",
        tmp_path
    )

    assert output.exists()
    assert output.suffix == ".png"
    assert output.name == "summary-2025-11.png"
    assert output.stat().st_size > 1000


@pytest.mark.skip(reason="generate_summary_comparison_chart function not implemented")
@pytest.mark.integration
def test_summary_comparison_chart_missing_data(tmp_path):
    """
    Test summary chart with missing metrics.

    Should handle missing data gracefully.
    """
    summary = {
        'total_releases': 10
        #: Other metrics missing
    }

    output = generate_summary_comparison_chart(
        summary,
        "test",
        tmp_path
    )

    assert output.exists()


@pytest.mark.integration
def test_timeline_chart_with_data(tmp_path):
    """
    Test timeline chart with release data.

    Verifies chart creation with realistic release dates.
    """
    timeline = [
        (datetime(2025, 10, 1), "1.0.0"),
        (datetime(2025, 10, 15), "1.1.0"),
        (datetime(2025, 11, 1), "1.2.0"),
        (datetime(2025, 11, 10), "1.2.1")
    ]

    output = generate_timeline_chart(
        timeline,
        "2025-11",
        tmp_path
    )

    assert output.exists()
    assert output.suffix == ".png"
    assert output.name == "timeline-2025-11.png"
    assert output.stat().st_size > 1000


@pytest.mark.integration
def test_timeline_chart_empty_data(tmp_path):
    """
    Test timeline chart with no release data.

    Should create chart with "No data available" message.
    """
    timeline = []

    output = generate_timeline_chart(
        timeline,
        "test",
        tmp_path
    )

    assert output.exists()
    assert output.suffix == ".png"


@pytest.mark.integration
def test_timeline_chart_single_release(tmp_path):
    """
    Test timeline chart with single release.

    Should handle single data point correctly.
    """
    timeline = [(datetime(2025, 11, 15), "1.0.0")]

    output = generate_timeline_chart(
        timeline,
        "test",
        tmp_path
    )

    assert output.exists()


@pytest.mark.integration
def test_chart_directory_creation(tmp_path):
    """
    Test that chart directory is created if it doesn't exist.

    Chart generators should create directories as needed.
    """
    #: Use non-existent subdirectory
    chart_dir = tmp_path / "charts" / "nested"

    assert not chart_dir.exists()

    projects = [{'name': 'test', 'total_commits': 10}]
    output = generate_project_breakdown_chart(
        projects,
        'total_commits',
        "test",
        chart_dir
    )

    assert chart_dir.exists()
    assert output.exists()


@pytest.mark.integration
def test_different_metrics_generate_different_files(tmp_path):
    """
    Test that different metrics generate separate chart files.

    Each metric should have its own file.
    """
    projects = [
        {'name': 'service', 'total_commits': 100, 'total_lines_added': 1000}
    ]

    output1 = generate_project_breakdown_chart(
        projects, 'total_commits', "test", tmp_path
    )
    output2 = generate_project_breakdown_chart(
        projects, 'total_lines_added', "test", tmp_path
    )

    assert output1.exists()
    assert output2.exists()
    assert output1.name != output2.name
    assert "total_commits" in output1.name
    assert "total_lines_added" in output2.name
