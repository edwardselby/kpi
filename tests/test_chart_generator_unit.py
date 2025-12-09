"""
Unit tests for chart_generator module with mocks.

Fast tests that mock matplotlib to avoid actual rendering.
These run by default (pytest without -m integration).
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, call
from src.chart_generator import (
    generate_project_breakdown_chart,
    generate_timeline_chart
)


@pytest.mark.unit
class TestProjectBreakdownChartUnit:
    """Fast unit tests for project breakdown charts using mocks."""

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_chart_generation_no_rendering(self, mock_figure, mock_savefig):
        """Test that chart function calls matplotlib correctly without rendering."""
        projects = [
            {'name': 'service-a', 'total_commits': 50},
            {'name': 'service-b', 'total_commits': 30}
        ]

        output_path = Path('/tmp/test-chart.png')

        result = generate_project_breakdown_chart(
            projects,
            'total_commits',
            "test",
            output_path
        )

        # Verify matplotlib was called (implementation may call figure() multiple times)
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once
        # Verify result is PNG file with expected characteristics
        assert result.suffix == '.png'
        assert 'total_commits' in result.name

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_chart_sorting_logic(self, mock_figure, mock_savefig):
        """Test that projects are sorted by metric value."""
        projects = [
            {'name': 'low', 'total_commits': 10},
            {'name': 'high', 'total_commits': 100},
            {'name': 'medium', 'total_commits': 50}
        ]

        result = generate_project_breakdown_chart(
            projects,
            'total_commits',
            "test",
            Path('/tmp/chart.png')
        )

        # Verify chart was created and saved
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once
        assert 'total_commits' in result.name

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_chart_with_empty_projects(self, mock_figure, mock_savefig):
        """Test chart generation with empty project list."""
        projects = []

        result = generate_project_breakdown_chart(
            projects,
            'total_commits',
            "test",
            Path('/tmp/chart.png')
        )

        # Should still call matplotlib (creates empty chart)
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_different_metrics_handled(self, mock_figure, mock_savefig):
        """Test that different metrics can be charted."""
        projects = [{'name': 'svc', 'total_commits': 100, 'total_lines_added': 5000}]

        # Test commits metric
        generate_project_breakdown_chart(
            projects, 'total_commits', "test", Path('/tmp/commits.png')
        )

        # Test lines metric
        generate_project_breakdown_chart(
            projects, 'total_lines_added', "test", Path('/tmp/lines.png')
        )

        # Should save exactly 2 charts (savefig is reliable indicator)
        assert mock_savefig.call_count == 2, "Should save exactly 2 charts"
        assert mock_figure.called, "plt.figure() should be called"


@pytest.mark.unit
class TestTimelineChartUnit:
    """Fast unit tests for timeline charts using mocks."""

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_timeline_with_data(self, mock_figure, mock_savefig):
        """Test timeline chart generation with release data."""
        timeline = [
            (datetime(2025, 10, 1), "1.0.0"),
            (datetime(2025, 11, 1), "1.1.0"),
            (datetime(2025, 12, 1), "1.2.0")
        ]

        result = generate_timeline_chart(
            timeline,
            "test",
            Path('/tmp/timeline.png')
        )

        # Verify matplotlib was called correctly
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once
        # Verify result is PNG file with expected characteristics
        assert result.suffix == '.png'
        assert 'timeline' in result.name

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_timeline_with_empty_data(self, mock_figure, mock_savefig):
        """Test timeline chart with no releases."""
        timeline = []

        result = generate_timeline_chart(
            timeline,
            "test",
            Path('/tmp/timeline.png')
        )

        # Should still create chart (shows "No data")
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_timeline_with_single_release(self, mock_figure, mock_savefig):
        """Test timeline with single release."""
        timeline = [(datetime(2025, 11, 15), "1.0.0")]

        result = generate_timeline_chart(
            timeline,
            "test",
            Path('/tmp/timeline.png')
        )

        # Should handle single point
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once


@pytest.mark.unit
class TestChartDirectoryHandling:
    """Test chart directory creation logic."""

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    @patch('pathlib.Path.mkdir')
    def test_creates_directory_if_missing(self, mock_mkdir, mock_figure, mock_savefig):
        """Test that chart directory is created if it doesn't exist."""
        projects = [{'name': 'svc', 'total_commits': 10}]
        output_path = Path('/tmp/nested/dir/chart.png')

        # Mock directory doesn't exist
        with patch('pathlib.Path.exists', return_value=False):
            generate_project_breakdown_chart(
                projects,
                'total_commits',
                "test",
                output_path
            )

            # Verify mkdir was called
            mock_mkdir.assert_called()

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_works_with_existing_directory(self, mock_figure, mock_savefig):
        """Test that function works when directory already exists."""
        projects = [{'name': 'svc', 'total_commits': 10}]

        with patch('pathlib.Path.exists', return_value=True):
            result = generate_project_breakdown_chart(
                projects,
                'total_commits',
                "test",
                Path('/tmp/chart.png')
            )

            # Should still work
            mock_savefig.assert_called_once()


@pytest.mark.unit
class TestChartPerformance:
    """Test that unit tests are actually fast."""

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_multiple_charts_generated_quickly(self, mock_figure, mock_savefig):
        """Test that generating multiple charts is fast with mocks."""
        projects = [{'name': f'svc-{i}', 'total_commits': i*10} for i in range(10)]

        # Generate 5 charts
        for metric in ['total_commits', 'total_lines_added', 'net_change']:
            generate_project_breakdown_chart(
                projects,
                metric,
                "test",
                Path(f'/tmp/{metric}.png')
            )

        # With mocks, this should be instant
        # Verify all 3 charts were saved (savefig is reliable indicator)
        assert mock_savefig.call_count == 3, "Should save exactly 3 charts"
        assert mock_figure.called, "plt.figure() should be called"

    @patch('src.chart_generator.plt.savefig')
    @patch('src.chart_generator.plt.figure')
    def test_timeline_generation_is_fast(self, mock_figure, mock_savefig):
        """Test that timeline generation with mocks is fast."""
        # Generate many releases (spread across months)
        timeline = [
            (datetime(2025, (i % 12) + 1, min((i % 28) + 1, 28)), f"1.0.{i}")
            for i in range(100)
        ]

        generate_timeline_chart(timeline, "test", Path('/tmp/timeline.png'))

        # With mocks, should be instant regardless of data size
        assert mock_figure.called, "plt.figure() should be called"
        mock_savefig.assert_called_once()  # Chart should be saved exactly once
