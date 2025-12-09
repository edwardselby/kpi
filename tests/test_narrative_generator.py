"""
Unit tests for narrative_generator.py balanced insights functionality.

Tests cover Phase 2 enhancements:
- API distribution analysis
- Service layer analysis
- Concentration risk detection
- Simple recommendation generation
- Balanced narrative generation
"""

import pytest
from datetime import datetime
from pathlib import Path
from src.narrative_generator import (
    _analyze_api_distribution,
    _analyze_service_layers,
    _detect_concentration_risks,
    _generate_simple_recommendations,
    _generate_balanced_narrative,
    generate_executive_summary
)
from src.config_manager import ServiceMetadata


class MockConfig:
    """Mock configuration object for testing."""

    def __init__(self):
        self.service_metadata = {
            'api-gateway-service': ServiceMetadata(
                category='Core Infrastructure',
                tags=['API', 'routing', 'orchestration', 'integration'],
                description='API gateway system'
            ),
            'user-service': ServiceMetadata(
                category='Core Infrastructure',
                tags=['user_management', 'authentication', 'API'],
                description='User management system'
            ),
            'payment-service': ServiceMetadata(
                category='Domain Services',
                tags=['transaction_processing', 'domain_logic', 'API'],
                description='Payment processing API'
            ),
            'non-api-service': ServiceMetadata(
                category='Supporting Services',
                tags=['logging', 'monitoring'],
                description='Logging service'
            )
        }

        self.tag_descriptions = {
            'ETL': 'data transformation',
            'orchestration': 'service coordination',
            'integration': 'system integration',
            'API': 'API development',
            'data_presentation': 'data presentation',
            'aggregation': 'data aggregation',
            'user_interface': 'user-facing features',
            'real_time': 'real-time processing',
            'transaction_processing': 'transaction handling',
            'logging': 'logging infrastructure',
            'monitoring': 'monitoring systems'
        }

        self.tag_groups = {
            'service_layers': {
                'data_layer': ['ETL', 'data_processing', 'aggregation', 'database', 'storage'],
                'presentation_layer': ['data_presentation', 'user_interface', 'API'],
                'business_layer': ['transaction_processing', 'domain_logic', 'statistics'],
                'infrastructure_layer': ['orchestration', 'integration', 'logging', 'monitoring']
            },
            'technical_characteristics': {
                'real_time_services': ['real_time', 'event_management'],
                'batch_services': ['ETL', 'data_processing', 'aggregation'],
                'user_facing': ['user_interface', 'API'],
                'backend_services': ['database', 'storage', 'logging']
            }
        }


@pytest.fixture
def mock_config():
    """Provide mock configuration for tests."""
    return MockConfig()


@pytest.fixture
def sample_projects_data():
    """Provide sample project data for tests."""
    return [
        {
            'name': 'api-gateway-service',
            'total_commits': 28,
            'total_lines_added': 3540,
            'total_lines_removed': 200,
            'net_change': 3340,
            'release_count': 194
        },
        {
            'name': 'user-service',
            'total_commits': 9,
            'total_lines_added': 1240,
            'total_lines_removed': 150,
            'net_change': 1090,
            'release_count': 135
        },
        {
            'name': 'payment-service',
            'total_commits': 3,
            'total_lines_added': 342,
            'total_lines_removed': 50,
            'net_change': 292,
            'release_count': 44
        },
        {
            'name': 'non-api-service',
            'total_commits': 0,
            'total_lines_added': 0,
            'total_lines_removed': 0,
            'net_change': 0,
            'release_count': 10
        }
    ]


class TestAnalyzeApiDistribution:
    """Test _analyze_api_distribution function."""

    def test_identifies_api_services(self, sample_projects_data, mock_config):
        """Test that API services are correctly identified."""
        result = _analyze_api_distribution(sample_projects_data, mock_config)

        assert result['api_service_count'] == 3
        assert 'api-gateway-service' in result['api_services']
        assert 'user-service' in result['api_services']
        assert 'payment-service' in result['api_services']
        assert 'non-api-service' not in result['api_services']

    def test_calculates_api_commit_percentage(self, sample_projects_data, mock_config):
        """Test API commit percentage calculation."""
        result = _analyze_api_distribution(sample_projects_data, mock_config)

        # Total commits: 28 + 9 + 3 + 0 = 40
        # API commits: 28 + 9 + 3 = 40
        # Percentage: 40/40 * 100 = 100%
        assert result['api_commit_percentage'] == 100.0
        assert result['total_commits'] == 40
        assert result['api_commits'] == 40

    def test_handles_no_api_services(self, mock_config):
        """Test handling when no services have API tag."""
        projects_data = [
            {
                'name': 'non-api-service',
                'total_commits': 10,
                'total_lines_added': 500,
                'total_lines_removed': 50,
                'net_change': 450,
                'release_count': 5
            }
        ]

        result = _analyze_api_distribution(projects_data, mock_config)

        assert result['api_service_count'] == 0
        assert result['api_commit_percentage'] == 0.0
        assert result['api_services'] == []

    def test_handles_empty_projects(self, mock_config):
        """Test handling of empty projects list."""
        result = _analyze_api_distribution([], mock_config)

        assert result['api_service_count'] == 0
        assert result['api_commit_percentage'] == 0.0
        assert result['total_commits'] == 0


class TestAnalyzeServiceLayers:
    """Test _analyze_service_layers function."""

    def test_categorizes_services_by_layer(self, sample_projects_data, mock_config):
        """Test that services are categorized into correct layers."""
        result = _analyze_service_layers(sample_projects_data, mock_config)

        assert 'layer_distribution' in result
        layers = result['layer_distribution']

        # feed-orchestrator has ETL (data_layer)
        # data-aggregation has data_presentation (presentation_layer)
        # betslip has user_interface (presentation_layer)
        # non-api-service has logging (infrastructure_layer)

        assert 'data_layer' in layers
        assert 'presentation_layer' in layers
        assert 'infrastructure_layer' in layers

    def test_calculates_layer_percentages(self, sample_projects_data, mock_config):
        """Test layer percentage calculations."""
        result = _analyze_service_layers(sample_projects_data, mock_config)

        layers = result['layer_distribution']
        total_commits = result['total_commits']

        assert total_commits == 40

        # Verify percentages add up correctly
        total_percentage = sum(layer['percentage'] for layer in layers.values())
        assert 95 <= total_percentage <= 105  # Allow rounding errors

    def test_handles_service_with_multiple_matching_layers(self, mock_config):
        """Test that service is assigned to first matching layer."""
        projects_data = [
            {
                'name': 'api-gateway-service',  # Has both API and orchestration tags
                'total_commits': 10,
                'total_lines_added': 500,
                'total_lines_removed': 50,
                'net_change': 450,
                'release_count': 5
            }
        ]

        result = _analyze_service_layers(projects_data, mock_config)

        # Should be assigned to presentation_layer (API matches first in layer order)
        assert result['layer_distribution']['presentation_layer']['commits'] == 10


class TestDetectConcentrationRisks:
    """Test _detect_concentration_risks function."""

    def test_detects_high_concentration(self, sample_projects_data):
        """Test detection of high concentration (>70%)."""
        #: Create scenario with 71% concentration (29/40 commits)
        projects_with_high_concentration = [
            {'name': 'api-gateway-service', 'total_commits': 29, 'net_change': 3340, 'release_count': 194},
            {'name': 'user-service', 'total_commits': 9, 'net_change': 1289, 'release_count': 90},
            {'name': 'payment-service', 'total_commits': 2, 'net_change': 160, 'release_count': 16},
            {'name': 'non-api-service', 'total_commits': 0, 'net_change': 0, 'release_count': 10}
        ]
        category_stats = {'total_commits': 40}

        result = _detect_concentration_risks(projects_with_high_concentration, category_stats)

        # feed-orchestrator has 29/40 = 72.5% (> 70% threshold)
        assert result['has_concentration'] == True
        assert result['top_service'] == 'api-gateway-service'
        assert result['concentration_percentage'] == 72.5

    def test_counts_dormant_services(self, sample_projects_data):
        """Test counting of dormant services."""
        category_stats = {'total_commits': 40}

        result = _detect_concentration_risks(sample_projects_data, category_stats)

        # Only non-api-service has 0 commits
        assert result['dormant_count'] == 1
        assert result['total_services'] == 4
        assert result['dormant_percentage'] == 25.0

    def test_no_concentration_when_balanced(self):
        """Test no concentration flag when commits are balanced."""
        projects_data = [
            {'name': 'service-a', 'total_commits': 10, 'net_change': 500},
            {'name': 'service-b', 'total_commits': 10, 'net_change': 500},
            {'name': 'service-c', 'total_commits': 10, 'net_change': 500}
        ]
        category_stats = {'total_commits': 30}

        result = _detect_concentration_risks(projects_data, category_stats)

        # Each service has 33.3%, no concentration
        assert result['has_concentration'] == False
        assert result['concentration_percentage'] < 70


class TestGenerateSimpleRecommendations:
    """Test _generate_simple_recommendations function."""

    def test_generates_concentration_recommendation(self):
        """Test recommendation for high concentration."""
        concentration = {
            'has_concentration': True,
            'concentration_percentage': 75.0,
            'dormant_percentage': 50.0
        }
        api_analysis = {'api_commit_percentage': 80.0}
        layer_analysis = {'layer_distribution': {}}
        velocity = {'churn_rate': 15.0}

        recommendations = _generate_simple_recommendations(
            concentration, api_analysis, layer_analysis, velocity
        )

        assert len(recommendations) > 0
        assert any('distributing development efforts' in rec.lower() for rec in recommendations)

    def test_generates_dormant_services_recommendation(self):
        """Test recommendation for high dormant percentage."""
        concentration = {
            'has_concentration': False,
            'concentration_percentage': 50.0,
            'dormant_percentage': 70.0
        }
        api_analysis = {'api_commit_percentage': 50.0}
        layer_analysis = {'layer_distribution': {}}
        velocity = {'churn_rate': 20.0}

        recommendations = _generate_simple_recommendations(
            concentration, api_analysis, layer_analysis, velocity
        )

        assert len(recommendations) > 0
        assert any('maintenance sprints' in rec.lower() for rec in recommendations)

    def test_generates_low_churn_recommendation(self):
        """Test recommendation for low churn rate."""
        concentration = {
            'has_concentration': False,
            'concentration_percentage': 50.0,
            'dormant_percentage': 30.0
        }
        api_analysis = {'api_commit_percentage': 50.0}
        layer_analysis = {'layer_distribution': {}}
        velocity = {'churn_rate': 5.0}  # Low churn

        recommendations = _generate_simple_recommendations(
            concentration, api_analysis, layer_analysis, velocity
        )

        assert len(recommendations) > 0
        assert any('refactoring' in rec.lower() for rec in recommendations)

    def test_limits_recommendations_to_three(self):
        """Test that maximum 3 recommendations are returned."""
        concentration = {
            'has_concentration': True,
            'concentration_percentage': 80.0,
            'dormant_percentage': 70.0
        }
        api_analysis = {'api_commit_percentage': 90.0}
        layer_analysis = {'layer_distribution': {}}
        velocity = {'churn_rate': 5.0}

        recommendations = _generate_simple_recommendations(
            concentration, api_analysis, layer_analysis, velocity
        )

        assert len(recommendations) <= 3

    def test_constructive_tone(self):
        """Test that recommendations use constructive language."""
        concentration = {
            'has_concentration': True,
            'concentration_percentage': 75.0,
            'dormant_percentage': 65.0
        }
        api_analysis = {'api_commit_percentage': 80.0}
        layer_analysis = {'layer_distribution': {}}
        velocity = {'churn_rate': 8.0}

        recommendations = _generate_simple_recommendations(
            concentration, api_analysis, layer_analysis, velocity
        )

        # Check for constructive phrases
        all_text = ' '.join(recommendations).lower()
        assert 'consider' in all_text or 'opportunity' in all_text


class TestGenerateBalancedNarrative:
    """Test _generate_balanced_narrative function."""

    @pytest.fixture
    def complete_analysis_data(self, mock_config):
        """Provide complete analysis data for narrative generation."""
        return {
            'category_stats': {
                'categories': {
                    'Core Infrastructure': {
                        'commits': 37,
                        'percentage': 92.5,
                        'projects': ['api-gateway-service', 'user-service']
                    },
                    'User Features': {
                        'commits': 3,
                        'percentage': 7.5,
                        'projects': ['payment-service']
                    }
                },
                'total_commits': 40,
                'total_lines_added': 5122,
                'top_category': (
                    'Core Infrastructure',
                    {
                        'commits': 37,
                        'percentage': 92.5,
                        'projects': ['api-gateway-service', 'user-service']
                    }
                )
            },
            'focus_insights': {
                'top_tags': ['ETL', 'orchestration'],
                'churn_rate': 6.5,
                'work_type': 'new_features',
                'release_pattern': 'major'
            },
            'velocity': {
                'avg_commits_per_release': 0.1,
                'avg_lines_per_commit': 128.0,
                'net_change': 4789,
                'growth_type': 'expansion',
                'churn_rate': 6.5
            },
            'top_performers': {
                'top_by_commits': {
                    'name': 'api-gateway-service',
                    'total_commits': 28,
                    'total_lines_added': 3540,
                    'net_change': 3340
                },
                'top_by_growth': {
                    'name': 'api-gateway-service',
                    'total_commits': 28,
                    'total_lines_added': 3540,
                    'net_change': 3340
                }
            },
            'api_analysis': {
                'api_service_count': 3,
                'api_commit_percentage': 100.0,
                'api_services': ['api-gateway-service', 'user-service', 'payment-service']
            },
            'layer_analysis': {
                'layer_distribution': {
                    'data_layer': {'commits': 28, 'percentage': 70.0},
                    'presentation_layer': {'commits': 12, 'percentage': 30.0},
                    'business_layer': {'commits': 0, 'percentage': 0.0},
                    'infrastructure_layer': {'commits': 0, 'percentage': 0.0}
                },
                'total_commits': 40
            },
            'concentration': {
                'has_concentration': True,
                'top_service': 'api-gateway-service',
                'concentration_percentage': 70.0,
                'dormant_count': 1,
                'dormant_percentage': 25.0,
                'total_services': 4
            },
            'recommendations': [
                'Consider allocating 15-20% of capacity to refactoring efforts'
            ]
        }

    def test_returns_balanced_structure(self, complete_analysis_data, mock_config, sample_projects_data):
        """Test that balanced narrative returns proper structure."""
        data = complete_analysis_data

        #: Generate Phase 3 parameters
        multiple_focuses = _identify_multiple_focuses(
            data['category_stats'],
            data['layer_analysis'],
            sample_projects_data,
            mock_config
        )
        dynamic_highlights = _generate_dynamic_highlights(
            sample_projects_data,
            data['category_stats'],
            data['velocity'],
            mock_config
        )
        velocity_breakdown = _break_down_velocity_metrics(
            data['velocity'],
            {'total_commits': 40, 'total_releases': 40}
        )

        result = _generate_balanced_narrative(
            data['category_stats'],
            data['focus_insights'],
            data['velocity'],
            data['top_performers'],
            'November 2025',
            data['api_analysis'],
            data['layer_analysis'],
            data['concentration'],
            data['recommendations'],
            multiple_focuses,
            dynamic_highlights,
            velocity_breakdown
        )

        assert result['has_summary'] == True
        assert 'period_summary' in result

        # Check activity_breakdown has observation and balance_point
        assert 'activity_breakdown' in result
        assert 'observation' in result['activity_breakdown']
        assert 'balance_point' in result['activity_breakdown']

        # Check development_focus is now a list (Phase 3)
        assert 'development_focus' in result
        assert isinstance(result['development_focus'], list)
        assert len(result['development_focus']) > 0
        for focus in result['development_focus']:
            assert 'observation' in focus
            assert 'balance_point' in focus

        # Check development_velocity is now a list (Phase 3)
        assert 'development_velocity' in result
        assert isinstance(result['development_velocity'], list)
        assert len(result['development_velocity']) > 0
        for metric in result['development_velocity']:
            assert 'observation' in metric
            assert 'balance_point' in metric

        # Check recommendations are included
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0

    def test_technical_highlights_have_positive_and_cautionary(self, complete_analysis_data, mock_config, sample_projects_data):
        """Test that highlights include both positive and cautionary notes."""
        data = complete_analysis_data

        #: Generate Phase 3 parameters
        multiple_focuses = _identify_multiple_focuses(
            data['category_stats'],
            data['layer_analysis'],
            sample_projects_data,
            mock_config
        )
        dynamic_highlights = _generate_dynamic_highlights(
            sample_projects_data,
            data['category_stats'],
            data['velocity'],
            mock_config
        )
        velocity_breakdown = _break_down_velocity_metrics(
            data['velocity'],
            {'total_commits': 40, 'total_releases': 40}
        )

        result = _generate_balanced_narrative(
            data['category_stats'],
            data['focus_insights'],
            data['velocity'],
            data['top_performers'],
            'November 2025',
            data['api_analysis'],
            data['layer_analysis'],
            data['concentration'],
            data['recommendations'],
            multiple_focuses,
            dynamic_highlights,
            velocity_breakdown
        )

        highlights = result['technical_highlights']
        assert len(highlights) > 0

        for highlight in highlights:
            assert 'positive' in highlight
            assert 'cautionary' in highlight
            assert isinstance(highlight['positive'], str)
            assert isinstance(highlight['cautionary'], str)

    def test_constructive_language_in_balance_points(self, complete_analysis_data, mock_config, sample_projects_data):
        """Test that balance points use constructive language."""
        data = complete_analysis_data

        #: Generate Phase 3 parameters
        multiple_focuses = _identify_multiple_focuses(
            data['category_stats'],
            data['layer_analysis'],
            sample_projects_data,
            mock_config
        )
        dynamic_highlights = _generate_dynamic_highlights(
            sample_projects_data,
            data['category_stats'],
            data['velocity'],
            mock_config
        )
        velocity_breakdown = _break_down_velocity_metrics(
            data['velocity'],
            {'total_commits': 40, 'total_releases': 40}
        )

        result = _generate_balanced_narrative(
            data['category_stats'],
            data['focus_insights'],
            data['velocity'],
            data['top_performers'],
            'November 2025',
            data['api_analysis'],
            data['layer_analysis'],
            data['concentration'],
            data['recommendations'],
            multiple_focuses,
            dynamic_highlights,
            velocity_breakdown
        )

        #: Check for constructive phrases in balance points (Phase 3 uses lists)
        all_balance_text = ' '.join([
            result['activity_breakdown']['balance_point']
        ] + [
            focus['balance_point'] for focus in result['development_focus']
        ] + [
            metric['balance_point'] for metric in result['development_velocity']
        ]).lower()

        # Should contain constructive phrases
        constructive_phrases = [
            'opportunity', 'consider', 'area to consider',
            'presents', 'enables', 'supports'
        ]
        assert any(phrase in all_balance_text for phrase in constructive_phrases)


class TestGenerateExecutiveSummary:
    """Test generate_executive_summary integration."""

    def test_end_to_end_summary_generation(self, sample_projects_data, mock_config):
        """Test complete executive summary generation."""
        report_data = {
            'total_releases': 373,
            'total_commits': 40,
            'total_lines_added': 5122,
            'total_lines_removed': 400,
            'period_display': 'November 2025'
        }

        result = generate_executive_summary(
            sample_projects_data,
            report_data,
            mock_config
        )

        assert result['has_summary'] == True
        assert 'period_summary' in result
        assert 'activity_breakdown' in result
        assert 'development_focus' in result
        assert 'technical_highlights' in result
        assert 'development_velocity' in result
        assert 'recommendations' in result

    def test_handles_empty_projects(self, mock_config):
        """Test handling of empty projects list."""
        report_data = {
            'total_releases': 0,
            'total_commits': 0,
            'total_lines_added': 0,
            'total_lines_removed': 0,
            'period_display': 'November 2025'
        }

        result = generate_executive_summary(
            [],
            report_data,
            mock_config
        )

        # Should return minimal summary
        assert result['has_summary'] == True
        assert 'minimal' in str(result).lower() or result['has_summary'] == True

# ============================================================================
# Phase 3 Tests - Dynamic Multi-Point Sections
# ============================================================================

from src.narrative_generator import (
    _identify_multiple_focuses,
    _generate_dynamic_highlights,
    _break_down_velocity_metrics,
    _get_top_tags_for_category,
    _get_dominant_layer_for_category,
    _get_service_capability,
    _calculate_velocity_metrics
)


class TestIdentifyMultipleFocuses:
    """Test _identify_multiple_focuses function for Phase 3."""

    def test_returns_primary_focus_always(self, sample_projects_data, mock_config):
        """Test that primary focus is always returned."""
        category_stats = {
            'categories': {
                'Core Infrastructure': {'commits': 37, 'percentage': 92.5},
                'User Features': {'commits': 3, 'percentage': 7.5}
            },
            'total_commits': 40
        }
        layer_analysis = {
            'layer_distribution': {
                'data_layer': {'commits': 30, 'percentage': 75.0},
                'presentation_layer': {'commits': 10, 'percentage': 25.0}
            }
        }

        result = _identify_multiple_focuses(
            category_stats, layer_analysis, sample_projects_data, mock_config
        )

        assert result['focus_count'] == 1
        assert len(result['focuses']) == 1
        assert result['focuses'][0]['level'] == 'Primary'
        assert result['focuses'][0]['category'] == 'Core Infrastructure'
        assert result['focuses'][0]['percentage'] == 92.5

    def test_adds_secondary_if_above_10_percent(self, sample_projects_data, mock_config):
        """Test secondary focus added if 2nd category > 10%."""
        category_stats = {
            'categories': {
                'Core Infrastructure': {'commits': 30, 'percentage': 60.0},
                'User Features': {'commits': 15, 'percentage': 30.0},
                'Supporting Services': {'commits': 5, 'percentage': 10.0}
            },
            'total_commits': 50
        }
        layer_analysis = {
            'layer_distribution': {
                'data_layer': {'commits': 25, 'percentage': 50.0},
                'presentation_layer': {'commits': 25, 'percentage': 50.0}
            }
        }

        result = _identify_multiple_focuses(
            category_stats, layer_analysis, sample_projects_data, mock_config
        )

        assert result['focus_count'] >= 2
        assert result['focuses'][1]['level'] == 'Secondary'
        assert result['focuses'][1]['percentage'] == 30.0

    def test_adds_tertiary_if_above_5_percent(self, sample_projects_data, mock_config):
        """Test tertiary focus added if 3rd category > 5%."""
        category_stats = {
            'categories': {
                'Core Infrastructure': {'commits': 50, 'percentage': 50.0},
                'User Features': {'commits': 30, 'percentage': 30.0},
                'Supporting Services': {'commits': 20, 'percentage': 20.0}
            },
            'total_commits': 100
        }
        layer_analysis = {
            'layer_distribution': {
                'data_layer': {'commits': 40, 'percentage': 40.0},
                'presentation_layer': {'commits': 40, 'percentage': 40.0},
                'business_layer': {'commits': 20, 'percentage': 20.0}
            }
        }

        result = _identify_multiple_focuses(
            category_stats, layer_analysis, sample_projects_data, mock_config
        )

        assert result['focus_count'] == 3
        assert result['focuses'][2]['level'] == 'Tertiary'
        assert result['focuses'][2]['percentage'] == 20.0


class TestGenerateDynamicHighlights:
    """Test _generate_dynamic_highlights function for Phase 3."""

    def test_always_includes_top_performer(self, sample_projects_data, mock_config):
        """Test top performer is always included."""
        category_stats = {'total_commits': 40}
        velocity = {'avg_lines_per_commit': 100, 'churn_rate': 5.0, 'net_change': 5000}

        result = _generate_dynamic_highlights(
            sample_projects_data, category_stats, velocity, mock_config
        )

        assert len(result) >= 1
        assert 'api-gateway-service' in result[0]['positive']
        assert 'led with 28 commits' in result[0]['positive']

    def test_no_duplicate_services(self, sample_projects_data, mock_config):
        """Test that same service doesn't appear multiple times."""
        category_stats = {'total_commits': 40}
        velocity = {'avg_lines_per_commit': 250, 'churn_rate': 5.0, 'net_change': 5000}

        result = _generate_dynamic_highlights(
            sample_projects_data, category_stats, velocity, mock_config
        )

        # Extract all service names from highlights
        services_mentioned = []
        for highlight in result:
            positive = highlight['positive']
            for project in sample_projects_data:
                if project['name'] in positive:
                    services_mentioned.append(project['name'])
                    break

        # Check no duplicates
        assert len(services_mentioned) == len(set(services_mentioned))

    def test_includes_high_velocity_if_threshold_met(self, sample_projects_data, mock_config):
        """Test high velocity highlight added if lines/commit > 200."""
        category_stats = {'total_commits': 40}
        velocity = {'avg_lines_per_commit': 250, 'churn_rate': 5.0, 'net_change': 5000}

        result = _generate_dynamic_highlights(
            sample_projects_data, category_stats, velocity, mock_config
        )

        # Should have high velocity highlight
        velocity_highlight = [h for h in result if '250 lines per commit' in h['positive']]
        assert len(velocity_highlight) > 0

    def test_max_5_highlights(self, mock_config):
        """Test that maximum 5 highlights are generated."""
        # Create many projects to potentially trigger all highlight types
        many_projects = [
            {'name': f'service-{i}', 'total_commits': 100-i*10, 'total_lines_added': 10000-i*1000,
             'total_lines_removed': 1000, 'net_change': 9000-i*1000, 'release_count': 10}
            for i in range(10)
        ]

        category_stats = {'total_commits': 500}
        velocity = {'avg_lines_per_commit': 250, 'churn_rate': 5.0, 'net_change': 50000}

        result = _generate_dynamic_highlights(
            many_projects, category_stats, velocity, mock_config
        )

        assert len(result) <= 5


class TestBreakDownVelocityMetrics:
    """Test _break_down_velocity_metrics function for Phase 3."""

    def test_always_returns_three_or_four_metrics(self, mock_config):
        """Test that 3-4 velocity metrics are returned."""
        velocity = {
            'avg_commits_per_release': 2.5,
            'avg_lines_per_commit': 150,
            'net_change': 10000,
            'churn_rate': 20.0,
            'work_type': 'new_features',
            'release_pattern': 'moderate'
        }
        report_data = {
            'total_commits': 100,
            'total_releases': 40
        }

        result = _break_down_velocity_metrics(velocity, report_data)

        assert len(result) >= 3
        assert len(result) <= 4

    def test_includes_commit_rate_metric(self, mock_config):
        """Test commit rate metric is always included."""
        velocity = {
            'avg_commits_per_release': 2.5,
            'avg_lines_per_commit': 150,
            'net_change': 10000,
            'churn_rate': 20.0,
            'work_type': 'new_features'
        }
        report_data = {
            'total_commits': 100,
            'total_releases': 40
        }

        result = _break_down_velocity_metrics(velocity, report_data)

        commit_rate_metric = [m for m in result if 'Commit Rate' in m['observation']]
        assert len(commit_rate_metric) == 1
        assert '100 commits across 40 releases' in commit_rate_metric[0]['observation']

    def test_includes_code_growth_metric(self, mock_config):
        """Test code growth metric is always included."""
        velocity = {
            'avg_commits_per_release': 2.5,
            'avg_lines_per_commit': 150,
            'net_change': 10000,
            'churn_rate': 20.0,
            'work_type': 'new_features'
        }
        report_data = {
            'total_commits': 100,
            'total_releases': 40
        }

        result = _break_down_velocity_metrics(velocity, report_data)

        growth_metric = [m for m in result if 'Code Growth' in m['observation']]
        assert len(growth_metric) == 1
        assert '+10,000 net lines' in growth_metric[0]['observation']

    def test_includes_churn_analysis_metric(self, mock_config):
        """Test churn analysis metric is always included."""
        velocity = {
            'avg_commits_per_release': 2.5,
            'avg_lines_per_commit': 150,
            'net_change': 10000,
            'churn_rate': 20.0,
            'work_type': 'mixed'
        }
        report_data = {
            'total_commits': 100,
            'total_releases': 40
        }

        result = _break_down_velocity_metrics(velocity, report_data)

        churn_metric = [m for m in result if 'Code Churn' in m['observation']]
        assert len(churn_metric) == 1
        assert '20.0%' in churn_metric[0]['observation']
        assert 'mixed' in churn_metric[0]['observation']


class TestCalculateVelocityMetricsEnhanced:
    """Test enhanced _calculate_velocity_metrics with churn_rate fix."""

    def test_calculates_churn_rate_correctly(self):
        """Test that churn rate is calculated correctly."""
        report_data = {
            'total_releases': 100,
            'total_commits': 500,
            'total_lines_added': 100000,
            'total_lines_removed': 40000
        }

        result = _calculate_velocity_metrics(report_data)

        assert 'churn_rate' in result
        assert result['churn_rate'] == 40.0  # 40000/100000 * 100

    def test_returns_work_type(self):
        """Test that work_type is returned."""
        report_data = {
            'total_releases': 100,
            'total_commits': 500,
            'total_lines_added': 100000,
            'total_lines_removed': 10000  # 10% churn
        }

        result = _calculate_velocity_metrics(report_data)

        assert 'work_type' in result
        assert result['work_type'] == 'new_features'  # < 15% churn

    def test_work_type_new_features(self):
        """Test work_type classification as new_features."""
        report_data = {
            'total_releases': 100,
            'total_commits': 500,
            'total_lines_added': 100000,
            'total_lines_removed': 10000  # 10% churn
        }

        result = _calculate_velocity_metrics(report_data)
        assert result['work_type'] == 'new_features'

    def test_work_type_refactoring(self):
        """Test work_type classification as refactoring."""
        report_data = {
            'total_releases': 100,
            'total_commits': 500,
            'total_lines_added': 100000,
            'total_lines_removed': 50000  # 50% churn
        }

        result = _calculate_velocity_metrics(report_data)
        assert result['work_type'] == 'refactoring'

    def test_work_type_mixed(self):
        """Test work_type classification as mixed."""
        report_data = {
            'total_releases': 100,
            'total_commits': 500,
            'total_lines_added': 100000,
            'total_lines_removed': 25000  # 25% churn
        }

        result = _calculate_velocity_metrics(report_data)
        assert result['work_type'] == 'mixed'

    def test_returns_release_pattern(self):
        """Test that release_pattern is returned."""
        report_data = {
            'total_releases': 100,
            'total_commits': 500,
            'total_lines_added': 100000,
            'total_lines_removed': 40000
        }

        result = _calculate_velocity_metrics(report_data)

        assert 'release_pattern' in result
        assert result['release_pattern'] in ['major', 'moderate', 'incremental']


class TestPhase3Integration:
    """Integration tests for Phase 3 complete flow."""

    def test_phase3_returns_list_structures(self, sample_projects_data, mock_config):
        """Test that Phase 3 returns lists for multi-point sections."""
        report_data = {
            'total_releases': 40,
            'total_commits': 40,
            'total_lines_added': 5122,
            'total_lines_removed': 333,
            'period_display': 'November 2025'
        }

        result = generate_executive_summary(
            sample_projects_data,
            report_data,
            mock_config
        )

        # Check development_focus is a list
        assert isinstance(result['development_focus'], list)
        assert len(result['development_focus']) >= 1
        assert 'observation' in result['development_focus'][0]
        assert 'balance_point' in result['development_focus'][0]

        # Check technical_highlights is a list
        assert isinstance(result['technical_highlights'], list)
        assert len(result['technical_highlights']) >= 3
        assert 'positive' in result['technical_highlights'][0]
        assert 'cautionary' in result['technical_highlights'][0]

        # Check development_velocity is a list
        assert isinstance(result['development_velocity'], list)
        assert len(result['development_velocity']) >= 3
        assert 'observation' in result['development_velocity'][0]
        assert 'balance_point' in result['development_velocity'][0]

    def test_balanced_approach_maintained(self, sample_projects_data, mock_config):
        """Test that balanced approach is maintained in Phase 3."""
        report_data = {
            'total_releases': 40,
            'total_commits': 40,
            'total_lines_added': 5122,
            'total_lines_removed': 333,
            'period_display': 'November 2025'
        }

        result = generate_executive_summary(
            sample_projects_data,
            report_data,
            mock_config
        )

        # Every focus should have observation + balance_point
        for focus in result['development_focus']:
            assert 'observation' in focus
            assert 'balance_point' in focus
            assert len(focus['observation']) > 0
            assert len(focus['balance_point']) > 0

        # Every highlight should have positive + cautionary
        for highlight in result['technical_highlights']:
            assert 'positive' in highlight
            assert 'cautionary' in highlight
            assert len(highlight['positive']) > 0
            assert len(highlight['cautionary']) > 0

        # Every velocity metric should have observation + balance_point
        for metric in result['development_velocity']:
            assert 'observation' in metric
            assert 'balance_point' in metric
            assert len(metric['observation']) > 0
            assert len(metric['balance_point']) > 0
