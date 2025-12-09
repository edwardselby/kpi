"""
Narrative generation engine for executive summaries.

Analyzes project activity patterns and generates natural language
summaries with business and technical insights.
"""

from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter


def generate_executive_summary(
    projects_data: List[Dict[str, Any]],
    report_data: Dict[str, Any],
    config: Any
) -> Dict[str, Any]:
    """
    Generate executive summary from project data.

    Main entry point for narrative generation. Analyzes category
    distribution, development focus, velocity metrics, and top
    performers to create comprehensive summary.

    :param projects_data: List of project dictionaries with metrics
    :type projects_data: List[Dict[str, Any]]
    :param report_data: Report totals and metadata
    :type report_data: Dict[str, Any]
    :param config: Configuration object with service metadata
    :type config: Any
    :return: Dict with narrative sections
    :rtype: Dict[str, Any]

    :Example:

    >>> projects = [{'name': 'svc-a', 'total_commits': 10, ...}]
    >>> report = {'total_commits': 10, 'period_display': 'November 2025'}
    >>> summary = generate_executive_summary(projects, report, config)
    >>> summary['has_summary']
    True
    """
    #: Handle empty or low-activity case
    if not projects_data or report_data['total_commits'] == 0:
        return _generate_minimal_summary(report_data['period_display'])

    #: Analyze activity patterns (Phase 1 functions)
    category_stats = _analyze_category_distribution(projects_data, config)
    focus_insights = _identify_development_focus(
        category_stats, projects_data, config
    )
    velocity = _calculate_velocity_metrics(report_data)
    top_performers = _identify_top_performers(projects_data, category_stats)

    #: Phase 2 analysis
    api_analysis = _analyze_api_distribution(projects_data, config)
    layer_analysis = _analyze_service_layers(projects_data, config)
    concentration = _detect_concentration_risks(projects_data, category_stats)
    recommendations = _generate_simple_recommendations(
        concentration, api_analysis, layer_analysis, velocity
    )

    #: NEW Phase 3 analysis - Dynamic multi-point sections
    multiple_focuses = _identify_multiple_focuses(
        category_stats, layer_analysis, projects_data, config
    )
    dynamic_highlights = _generate_dynamic_highlights(
        projects_data, category_stats, velocity, config
    )
    velocity_breakdown = _break_down_velocity_metrics(velocity, report_data)

    #: Generate balanced narrative with Phase 3 enhancements
    narrative = _generate_balanced_narrative(
        category_stats,
        focus_insights,
        velocity,
        top_performers,
        report_data['period_display'],
        api_analysis,
        layer_analysis,
        concentration,
        recommendations,
        multiple_focuses,     # NEW Phase 3
        dynamic_highlights,   # NEW Phase 3
        velocity_breakdown    # NEW Phase 3
    )

    return narrative


def _analyze_category_distribution(
    projects_data: List[Dict[str, Any]],
    config: Any
) -> Dict[str, Any]:
    """
    Analyze distribution of activity across service categories.

    Groups projects by category and calculates commit/line totals
    and percentages for each category.

    :param projects_data: List of project data dictionaries
    :type projects_data: List[Dict[str, Any]]
    :param config: Configuration with service metadata
    :type config: Any
    :return: Category statistics dictionary
    :rtype: Dict[str, Any]

    :Example:

    >>> stats = _analyze_category_distribution(projects, config)
    >>> stats['categories']['Core Infrastructure']['commits']
    28
    >>> stats['categories']['Core Infrastructure']['percentage']
    75.7
    """
    #: Initialize category accumulators
    category_data = defaultdict(lambda: {
        'commits': 0,
        'lines_added': 0,
        'lines_removed': 0,
        'projects': []
    })

    total_commits = 0
    total_lines_added = 0

    #: Aggregate metrics by category
    for project in projects_data:
        project_name = project['name']

        #: Get category from metadata
        if project_name in config.service_metadata:
            metadata = config.service_metadata[project_name]
            category = metadata.category

            commits = project.get('total_commits', 0)
            lines_added = project.get('total_lines_added', 0)
            lines_removed = project.get('total_lines_removed', 0)

            category_data[category]['commits'] += commits
            category_data[category]['lines_added'] += lines_added
            category_data[category]['lines_removed'] += lines_removed
            category_data[category]['projects'].append(project_name)

            total_commits += commits
            total_lines_added += lines_added

    #: Calculate percentages and sort by commits
    categories_with_pct = {}
    for category, data in category_data.items():
        pct = (data['commits'] / total_commits * 100) if total_commits > 0 else 0
        categories_with_pct[category] = {
            **data,
            'percentage': round(pct, 1)
        }

    #: Sort categories by commit count
    sorted_categories = sorted(
        categories_with_pct.items(),
        key=lambda x: x[1]['commits'],
        reverse=True
    )

    return {
        'categories': dict(sorted_categories),
        'total_commits': total_commits,
        'total_lines_added': total_lines_added,
        'top_category': sorted_categories[0] if sorted_categories else None
    }


def _identify_development_focus(
    category_stats: Dict[str, Any],
    projects_data: List[Dict[str, Any]],
    config: Any
) -> Dict[str, Any]:
    """
    Identify development focus areas using tags and churn analysis.

    Aggregates tags from top active categories, calculates code
    churn rate, and determines work type (new features vs refactoring).

    :param category_stats: Category distribution statistics
    :type category_stats: Dict[str, Any]
    :param projects_data: List of project data
    :type projects_data: List[Dict[str, Any]]
    :param config: Configuration with tag descriptions
    :type config: Any
    :return: Focus insights dictionary
    :rtype: Dict[str, Any]

    :Example:

    >>> focus = _identify_development_focus(cat_stats, projects, config)
    >>> focus['work_type']
    'new_features'
    >>> focus['top_tags']
    ['orchestration', 'data_processing']
    """
    #: Collect tags from top 2-3 categories
    tag_counts = Counter()
    top_categories = list(category_stats['categories'].keys())[:3]

    for project in projects_data:
        project_name = project['name']
        if project_name in config.service_metadata:
            metadata = config.service_metadata[project_name]
            if metadata.category in top_categories:
                commits = project.get('total_commits', 0)
                for tag in metadata.tags:
                    tag_counts[tag] += commits

    #: Get top 3 tags
    top_tags = [tag for tag, _ in tag_counts.most_common(3)]

    #: Calculate churn rate
    total_added = category_stats['total_lines_added']
    total_removed = sum(
        cat['lines_removed']
        for cat in category_stats['categories'].values()
    )

    churn_rate = (total_removed / total_added * 100) if total_added > 0 else 0

    #: Determine work type based on churn
    if churn_rate < 15:
        work_type = 'new_features'
    elif churn_rate < 40:
        work_type = 'mixed'
    else:
        work_type = 'refactoring'

    #: Calculate commit/release ratio (if available)
    total_commits = category_stats['total_commits']
    avg_commits_per_release = 0
    total_releases = 0

    for project in projects_data:
        total_releases += project.get('release_count', 0)

    if total_releases > 0:
        avg_commits_per_release = total_commits / total_releases

    #: Determine release pattern
    if avg_commits_per_release < 1.5:
        release_pattern = 'major'
    elif avg_commits_per_release < 3.0:
        release_pattern = 'moderate'
    else:
        release_pattern = 'incremental'

    return {
        'top_tags': top_tags,
        'churn_rate': round(churn_rate, 1),
        'work_type': work_type,
        'release_pattern': release_pattern
    }


def _calculate_velocity_metrics(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate velocity and productivity metrics.

    Computes average commits per release, average lines per commit,
    churn rate, work type classification, and net change interpretation.

    :param report_data: Report totals dictionary
    :type report_data: Dict[str, Any]
    :return: Velocity metrics dictionary
    :rtype: Dict[str, Any]

    :Example:

    >>> velocity = _calculate_velocity_metrics(report_data)
    >>> velocity['avg_commits_per_release']
    1.9
    >>> velocity['growth_type']
    'expansion'
    >>> velocity['churn_rate']
    15.2
    """
    total_releases = report_data['total_releases']
    total_commits = report_data['total_commits']
    total_lines_added = report_data['total_lines_added']
    total_lines_removed = report_data['total_lines_removed']
    net_change = total_lines_added - total_lines_removed

    #: Average commits per release
    avg_commits_per_release = (
        total_commits / total_releases if total_releases > 0 else 0
    )

    #: Average lines per commit
    avg_lines_per_commit = (
        (total_lines_added + total_lines_removed) / total_commits
        if total_commits > 0 else 0
    )

    #: Calculate churn rate (percentage of lines removed vs added)
    churn_rate = (total_lines_removed / total_lines_added * 100) if total_lines_added > 0 else 0

    #: Classify work type based on churn rate
    if churn_rate < 15:
        work_type = 'new_features'
    elif churn_rate > 40:
        work_type = 'refactoring'
    else:
        work_type = 'mixed'

    #: Determine growth type
    if net_change > 1000:
        growth_type = 'expansion'
    elif net_change > 0:
        growth_type = 'growth'
    elif net_change < -1000:
        growth_type = 'consolidation'
    else:
        growth_type = 'maintenance'

    #: Determine release pattern
    if avg_commits_per_release < 1.5:
        release_pattern = 'major'
    elif avg_commits_per_release < 3:
        release_pattern = 'moderate'
    else:
        release_pattern = 'incremental'

    return {
        'avg_commits_per_release': round(avg_commits_per_release, 1),
        'avg_lines_per_commit': round(avg_lines_per_commit, 1),
        'net_change': net_change,
        'growth_type': growth_type,
        'churn_rate': round(churn_rate, 1),      # NEW
        'work_type': work_type,                   # NEW
        'release_pattern': release_pattern        # NEW
    }


def _identify_top_performers(
    projects_data: List[Dict[str, Any]],
    category_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Identify top performing projects by various metrics.

    Finds projects with highest commits, highest net change,
    and leaders within each category.

    :param projects_data: List of project data
    :type projects_data: List[Dict[str, Any]]
    :param category_stats: Category distribution stats
    :type category_stats: Dict[str, Any]
    :return: Top performers dictionary
    :rtype: Dict[str, Any]

    :Example:

    >>> performers = _identify_top_performers(projects, cat_stats)
    >>> performers['top_by_commits']['name']
    'api-gateway-service'
    """
    if not projects_data:
        return {'top_by_commits': None, 'top_by_growth': None}

    #: Sort by commits
    by_commits = sorted(
        projects_data,
        key=lambda p: p.get('total_commits', 0),
        reverse=True
    )

    #: Sort by net change
    by_growth = sorted(
        projects_data,
        key=lambda p: p.get('net_change', 0),
        reverse=True
    )

    return {
        'top_by_commits': by_commits[0] if by_commits else None,
        'top_by_growth': by_growth[0] if by_growth else None
    }


def _analyze_api_distribution(
    projects_data: List[Dict[str, Any]],
    config: Any
) -> Dict[str, Any]:
    """
    Analyze distribution of API vs non-API services.

    Identifies which services have API functionality and calculates
    what percentage of commit activity is API-related.

    :param projects_data: List of project data dictionaries
    :type projects_data: List[Dict[str, Any]]
    :param config: Configuration with service metadata
    :type config: Any
    :return: API distribution analysis
    :rtype: Dict[str, Any]
    """
    api_services = []
    api_commits = 0
    total_commits = 0

    for project in projects_data:
        project_name = project['name']
        commits = project.get('total_commits', 0)
        total_commits += commits

        #: Check if service has API tag
        if project_name in config.service_metadata:
            tags = config.service_metadata[project_name].tags
            if 'API' in tags:
                api_services.append(project_name)
                api_commits += commits

    api_percentage = (api_commits / total_commits * 100) if total_commits > 0 else 0

    return {
        'api_service_count': len(api_services),
        'api_commit_percentage': api_percentage,
        'api_services': api_services,
        'total_commits': total_commits,
        'api_commits': api_commits
    }


def _analyze_service_layers(
    projects_data: List[Dict[str, Any]],
    config: Any
) -> Dict[str, Any]:
    """
    Analyze activity distribution across service layers.

    Uses tag_groups.service_layers to categorize services into
    data layer, presentation layer, business layer, and infrastructure layer.

    :param projects_data: List of project data dictionaries
    :type projects_data: List[Dict[str, Any]]
    :param config: Configuration with tag_groups
    :type config: Any
    :return: Layer distribution analysis
    :rtype: Dict[str, Any]
    """
    from collections import defaultdict

    layer_commits = defaultdict(int)
    total_commits = sum(p.get('total_commits', 0) for p in projects_data)

    #: Get layer definitions from config
    service_layers = config.tag_groups.get('service_layers', {})

    for project in projects_data:
        project_name = project['name']
        commits = project.get('total_commits', 0)

        if project_name in config.service_metadata:
            project_tags = set(config.service_metadata[project_name].tags)

            #: Assign to layer based on tag match
            for layer_name, layer_tags in service_layers.items():
                if any(tag in project_tags for tag in layer_tags):
                    layer_commits[layer_name] += commits
                    break  # Assign to first matching layer

    #: Calculate percentages
    layer_distribution = {}
    for layer_name in service_layers.keys():
        commits = layer_commits.get(layer_name, 0)
        percentage = (commits / total_commits * 100) if total_commits > 0 else 0
        layer_distribution[layer_name] = {
            'commits': commits,
            'percentage': percentage
        }

    return {
        'layer_distribution': layer_distribution,
        'total_commits': total_commits
    }


def _detect_concentration_risks(
    projects_data: List[Dict[str, Any]],
    category_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Detect concentration risks from single service dominance.

    Identifies if development is too concentrated in one service
    and counts dormant services with no activity.

    :param projects_data: List of project data dictionaries
    :type projects_data: List[Dict[str, Any]]
    :param category_stats: Category distribution statistics
    :type category_stats: Dict[str, Any]
    :return: Concentration risk analysis
    :rtype: Dict[str, Any]
    """
    total_commits = sum(p.get('total_commits', 0) for p in projects_data)

    #: Find service with most commits
    top_service = None
    top_commits = 0
    for project in projects_data:
        commits = project.get('total_commits', 0)
        if commits > top_commits:
            top_commits = commits
            top_service = project['name']

    concentration_percentage = (top_commits / total_commits * 100) if total_commits > 0 else 0

    #: Count dormant services (0 commits)
    dormant_count = sum(1 for p in projects_data if p.get('total_commits', 0) == 0)
    total_services = len(projects_data)
    dormant_percentage = (dormant_count / total_services * 100) if total_services > 0 else 0

    return {
        'has_concentration': concentration_percentage > 70,
        'top_service': top_service,
        'concentration_percentage': concentration_percentage,
        'dormant_count': dormant_count,
        'dormant_percentage': dormant_percentage,
        'total_services': total_services
    }


def _get_top_tags_for_category(
    projects_data: List[Dict[str, Any]],
    category_name: str,
    config: Any
) -> List[str]:
    """
    Extract top 2-3 tags for services in a category.

    :param projects_data: List of project data
    :type projects_data: List[Dict[str, Any]]
    :param category_name: Category to analyze
    :type category_name: str
    :param config: Config object with metadata
    :return: List of top tags
    :rtype: List[str]
    """
    from collections import Counter

    tags = []
    for project in projects_data:
        project_name = project['name']
        if project_name in config.service_metadata:
            metadata = config.service_metadata[project_name]
            if metadata.category == category_name and project.get('total_commits', 0) > 0:
                tags.extend(metadata.tags)

    #: Count tag frequencies and return top 3
    if tags:
        tag_counts = Counter(tags)
        return [tag for tag, _ in tag_counts.most_common(3)]
    return []


def _get_dominant_layer_for_category(
    projects_data: List[Dict[str, Any]],
    category_name: str,
    config: Any
) -> str:
    """
    Find dominant service layer for a category.

    :param projects_data: List of project data
    :type projects_data: List[Dict[str, Any]]
    :param category_name: Category to analyze
    :type category_name: str
    :param config: Config object with metadata
    :return: Dominant layer name (title cased)
    :rtype: str
    """
    from collections import defaultdict

    layer_commits = defaultdict(int)
    service_layers = config.tag_groups.get('service_layers', {})

    #: Aggregate commits by layer for this category
    for project in projects_data:
        project_name = project['name']
        commits = project.get('total_commits', 0)

        if project_name in config.service_metadata:
            metadata = config.service_metadata[project_name]
            if metadata.category == category_name and commits > 0:
                project_tags = set(metadata.tags)

                #: Find matching layer
                for layer_name, layer_tags in service_layers.items():
                    if any(tag in project_tags for tag in layer_tags):
                        layer_commits[layer_name] += commits
                        break

    #: Return dominant layer
    if layer_commits:
        dominant = max(layer_commits.items(), key=lambda x: x[1])[0]
        return dominant.replace('_', ' ').title()
    return "Unknown Layer"


def _identify_multiple_focuses(
    category_stats: Dict[str, Any],
    layer_analysis: Dict[str, Any],
    projects_data: List[Dict[str, Any]],
    config: Any
) -> Dict[str, Any]:
    """
    Identify top 3 development focuses by category AND layer.

    Returns dynamic list of 1-3 focuses based on distribution:
    - Always: Primary focus (highest %)
    - If 2nd > 10%: Secondary focus
    - If 3rd > 5%: Tertiary focus

    :param category_stats: Category distribution from Phase 1
    :type category_stats: Dict[str, Any]
    :param layer_analysis: Service layer distribution from Phase 2
    :type layer_analysis: Dict[str, Any]
    :param projects_data: List of project data
    :type projects_data: List[Dict[str, Any]]
    :param config: Config object with metadata
    :return: Dict with focus hierarchy
    :rtype: Dict[str, Any]
    """
    #: Sort categories by commit count
    categories_sorted = sorted(
        category_stats['categories'].items(),
        key=lambda x: x[1]['commits'],
        reverse=True
    )

    #: Build focus list based on thresholds
    focuses = []

    #: Primary focus (always include)
    if categories_sorted:
        cat_name, cat_data = categories_sorted[0]

        #: Get dominant layer globally (not just for this category)
        layer_dist = layer_analysis['layer_distribution']
        dominant_layer = max(layer_dist.items(), key=lambda x: x[1]['commits'])

        #: Get top tags for this category
        top_tags = _get_top_tags_for_category(projects_data, cat_name, config)

        focuses.append({
            'level': 'Primary',
            'category': cat_name,
            'percentage': cat_data['percentage'],
            'layer': dominant_layer[0].replace('_', ' ').title(),
            'tags': top_tags
        })

    #: Secondary focus (if > 10%)
    if len(categories_sorted) > 1:
        cat_name, cat_data = categories_sorted[1]
        if cat_data['percentage'] > 10:
            layer = _get_dominant_layer_for_category(projects_data, cat_name, config)
            top_tags = _get_top_tags_for_category(projects_data, cat_name, config)

            focuses.append({
                'level': 'Secondary',
                'category': cat_name,
                'percentage': cat_data['percentage'],
                'layer': layer,
                'tags': top_tags
            })

    #: Tertiary focus (if > 5%)
    if len(categories_sorted) > 2:
        cat_name, cat_data = categories_sorted[2]
        if cat_data['percentage'] > 5:
            layer = _get_dominant_layer_for_category(projects_data, cat_name, config)
            top_tags = _get_top_tags_for_category(projects_data, cat_name, config)

            focuses.append({
                'level': 'Tertiary',
                'category': cat_name,
                'percentage': cat_data['percentage'],
                'layer': layer,
                'tags': top_tags
            })

    return {
        'focuses': focuses,
        'focus_count': len(focuses)
    }


def _get_service_capability(service_name: str, config: Any) -> str:
    """
    Extract primary capability from service metadata.

    :param service_name: Service name
    :type service_name: str
    :param config: Config object
    :return: Primary capability/tag
    :rtype: str
    """
    if service_name in config.service_metadata:
        tags = config.service_metadata[service_name].tags
        if tags:
            return tags[0]  # Primary tag as capability
    return "development"


def _generate_dynamic_highlights(
    projects_data: List[Dict[str, Any]],
    category_stats: Dict[str, Any],
    velocity: Dict[str, Any],
    config: Any
) -> List[Dict[str, str]]:
    """
    Generate 3-5 dynamic highlights based on data patterns.

    Selection criteria (pick most interesting):
    1. Always: Top performer by commits
    2. If growth_rate > 30%: Fastest growing service (not already highlighted)
    3. If lines/commit > 200: High-output standout
    4. If release ratio varies significantly: Release velocity leader (not already highlighted)
    5. If churn_rate exceptional: Refactoring vs greenfield insight

    Returns max 5 highlights with balanced pairs. Avoids highlighting
    the same service multiple times.

    :param projects_data: List of project data
    :type projects_data: List[Dict[str, Any]]
    :param category_stats: Category distribution
    :type category_stats: Dict[str, Any]
    :param velocity: Velocity metrics
    :type velocity: Dict[str, Any]
    :param config: Config object
    :return: List of highlight dicts with positive + cautionary
    :rtype: List[Dict[str, str]]
    """
    highlights = []
    highlighted_services = set()  # Track services already highlighted
    total_commits = sum(p.get('total_commits', 0) for p in projects_data)

    #: 1. Top performer (ALWAYS include)
    top_project = max(projects_data, key=lambda p: p.get('total_commits', 0))
    if top_project.get('total_commits', 0) > 0:
        commits = top_project['total_commits']
        lines = top_project.get('total_lines_added', 0)
        service_name = top_project['name']
        highlighted_services.add(service_name)  # Track it

        #: Get service capability from config
        capability = _get_service_capability(service_name, config)

        positive = (
            f"{service_name} led with {commits} commits "
            f"(+{lines:,} lines), demonstrating significant {capability} expansion"
        )

        concentration_pct = (commits / total_commits * 100) if total_commits > 0 else 0
        cautionary = (
            f"This concentration ({concentration_pct:.1f}% of activity) creates "
            f"efficiency but presents an opportunity to distribute knowledge "
            f"across the team to build redundancy"
        )

        highlights.append({'positive': positive, 'cautionary': cautionary})

    #: 2. Fastest growing (if growth > 30% and not already highlighted)
    for project in projects_data:
        service_name = project['name']
        if service_name in highlighted_services:
            continue  # Skip already highlighted services

        lines_added = project.get('total_lines_added', 0)
        lines_removed = project.get('total_lines_removed', 0)
        net_change = project.get('net_change', 0)

        #: Calculate growth rate (simplified - based on lines_removed as proxy for previous size)
        if lines_added > 0 and lines_removed > 0:
            previous_size = lines_added - net_change  # Rough estimate
            if previous_size > 0:
                growth_rate = (net_change / previous_size) * 100

                if growth_rate > 30 and len(highlights) < 5:
                    highlighted_services.add(service_name)  # Track it
                    positive = (
                        f"{service_name} saw fastest growth rate "
                        f"({growth_rate:.1f}% increase in codebase size)"
                    )
                    cautionary = (
                        "Rapid expansion may benefit from refactoring allocation "
                        "to maintain long-term code quality"
                    )
                    highlights.append({'positive': positive, 'cautionary': cautionary})
                    break

    #: 3. High velocity standout (if lines/commit > 200)
    avg_lines_per_commit = velocity.get('avg_lines_per_commit', 0)
    if avg_lines_per_commit > 200 and len(highlights) < 5:
        positive = (
            f"High development output with {avg_lines_per_commit:.0f} lines per commit "
            f"indicates substantial feature development"
        )
        cautionary = (
            "Large commit sizes may benefit from breaking down changes "
            "for easier code review and reduced integration risk"
        )
        highlights.append({'positive': positive, 'cautionary': cautionary})

    #: 4. Release velocity leader (if commits/release ratio varies and not already highlighted)
    release_projects = [p for p in projects_data
                        if p.get('release_count', 0) > 0
                        and p['name'] not in highlighted_services]  # Filter out already highlighted
    if release_projects and len(highlights) < 5:
        ratios = [
            (p['name'], p['total_commits'] / p['release_count'])
            for p in release_projects
        ]
        ratios.sort(key=lambda x: x[1], reverse=True)

        if ratios and ratios[0][1] > 3:  # High commits per release
            service_name, ratio = ratios[0]
            highlighted_services.add(service_name)  # Track it
            positive = (
                f"{service_name} maintained high release velocity "
                f"({ratio:.1f} commits per release) demonstrating agile delivery"
            )
            cautionary = (
                "Frequent releases demonstrate agility; consider batch testing "
                "strategies for integration validation"
            )
            highlights.append({'positive': positive, 'cautionary': cautionary})

    #: 5. Churn insight (if already not covered by other highlights)
    churn_rate = velocity.get('churn_rate', 0)
    if churn_rate < 10 and len(highlights) < 5:
        net_change = velocity.get('net_change', 0)
        positive = (
            f"Low churn rate ({churn_rate:.1f}%) with substantial growth "
            f"(+{net_change:,} lines) indicates stable feature addition"
        )
        cautionary = (
            "Minimal refactoring presents an opportunity to allocate 15-20% "
            "capacity for technical debt reduction in future sprints"
        )
        highlights.append({'positive': positive, 'cautionary': cautionary})

    return highlights[:5]  # Max 5 highlights


def _break_down_velocity_metrics(
    velocity: Dict[str, Any],
    report_data: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Break down velocity into 3-4 distinct metrics.

    Always include:
    1. Commit rate (commits per release)
    2. Code output velocity (lines per commit)
    3. Churn analysis (refactoring vs greenfield)

    Optional (if data available):
    4. Release cadence (frequency patterns)

    :param velocity: Velocity metrics from Phase 1
    :type velocity: Dict[str, Any]
    :param report_data: Report data with releases
    :type report_data: Dict[str, Any]
    :return: List of velocity insights with balance points
    :rtype: List[Dict[str, str]]
    """
    metrics = []

    #: 1. Commit rate (ALWAYS)
    avg_commits = velocity.get('avg_commits_per_release', 0)
    total_commits = report_data.get('total_commits', 0)
    total_releases = report_data.get('total_releases', 0)

    observation = (
        f"Commit Rate: {total_commits} commits across {total_releases} releases "
        f"({avg_commits:.1f}:1 ratio) shows "
        f"{'continuous delivery' if avg_commits < 2 else 'batched development'}"
    )

    balance = (
        "Frequent releases demonstrate agility; consider batch strategies for integration testing"
        if avg_commits < 2
        else "Batched releases enable thorough testing; monitor for delivery delays"
    )

    metrics.append({'observation': observation, 'balance_point': balance})

    #: 2. Code output velocity (ALWAYS)
    avg_lines = velocity.get('avg_lines_per_commit', 0)
    net_change = velocity.get('net_change', 0)

    observation = (
        f"Code Growth: +{net_change:,} net lines ({avg_lines:.0f} lines/commit) "
        f"indicates {'substantial' if avg_lines > 100 else 'incremental'} feature development"
    )

    balance = (
        "High growth rate shows productivity; 15-20% refactoring allocation recommended"
        if avg_lines > 100
        else "Incremental changes enable stable evolution; monitor velocity for capacity signals"
    )

    metrics.append({'observation': observation, 'balance_point': balance})

    #: 3. Churn analysis (ALWAYS)
    churn_rate = velocity.get('churn_rate', 0)
    work_type = velocity.get('work_type', 'unknown')

    observation = (
        f"Code Churn: {churn_rate:.1f}% modification rate indicates "
        f"{work_type.replace('_', ' ')} development focus"
    )

    if work_type == 'new_features':
        balance = "New feature focus is positive; technical debt reduction opportunities exist"
    elif work_type == 'refactoring':
        balance = "Refactoring investment strengthens foundation; monitor for feature delivery balance"
    else:
        balance = "Balanced approach between features and refactoring maintains sustainable velocity"

    metrics.append({'observation': observation, 'balance_point': balance})

    #: 4. Release cadence (OPTIONAL - if release data rich enough)
    release_pattern = velocity.get('release_pattern', '')
    if release_pattern and len(metrics) < 4:
        observation = (
            f"Release Cadence: {release_pattern.replace('_', ' ').title()} release pattern "
            f"maintained throughout period"
        )
        balance = (
            "Consistent pace is sustainable; monitor for velocity degradation signals"
        )
        metrics.append({'observation': observation, 'balance_point': balance})

    return metrics  # Return 3-4 metrics


def _generate_simple_recommendations(
    concentration: Dict[str, Any],
    api_analysis: Dict[str, Any],
    layer_analysis: Dict[str, Any],
    velocity: Dict[str, Any]
) -> List[str]:
    """
    Generate simple pattern-based recommendations.

    Uses basic rules to identify areas for consideration based on
    detected patterns. Maximum 3 recommendations, constructive tone.

    :param concentration: Concentration risk data
    :type concentration: Dict[str, Any]
    :param api_analysis: API distribution data
    :type api_analysis: Dict[str, Any]
    :param layer_analysis: Service layer data
    :type layer_analysis: Dict[str, Any]
    :param velocity: Velocity metrics
    :type velocity: Dict[str, Any]
    :return: List of recommendations (max 3)
    :rtype: List[str]
    """
    recommendations = []

    #: Rule 1: Concentration > 70% suggests knowledge distribution
    if concentration.get('has_concentration', False):
        recommendations.append(
            "Consider distributing development efforts across additional services "
            "to build team-wide knowledge and reduce dependency on single components"
        )

    #: Rule 2: High dormant percentage suggests maintenance needed
    if concentration.get('dormant_percentage', 0) > 60:
        recommendations.append(
            "Opportunity to schedule maintenance sprints for inactive services "
            "to address technical debt and dependency updates"
        )

    #: Rule 3: Low churn suggests refactoring opportunity
    churn_rate = velocity.get('churn_rate', 0)
    if churn_rate < 10:
        recommendations.append(
            "Consider allocating 15-20% of capacity to refactoring efforts "
            "for long-term maintainability and architectural improvements"
        )

    #: Return max 3 recommendations
    return recommendations[:3]


def _generate_balanced_narrative(
    category_stats: Dict[str, Any],
    focus_insights: Dict[str, Any],
    velocity: Dict[str, Any],
    top_performers: Dict[str, Any],
    period_display: str,
    api_analysis: Dict[str, Any],
    layer_analysis: Dict[str, Any],
    concentration: Dict[str, Any],
    recommendations: List[str],
    multiple_focuses: Dict[str, Any],           # NEW - Phase 3
    dynamic_highlights: List[Dict[str, str]],   # NEW - Phase 3
    velocity_breakdown: List[Dict[str, str]]    # NEW - Phase 3
) -> Dict[str, Any]:
    """
    Generate balanced narrative with dynamic multi-point sections (Phase 3).

    Creates balanced business and technical narrative pairing each positive
    observation with a constructive cautionary note. Phase 3 enhancement:
    returns lists for development_focus (1-3 points), technical_highlights
    (3-5 points), and development_velocity (3-4 points).

    :param category_stats: Category distribution
    :type category_stats: Dict[str, Any]
    :param focus_insights: Development focus insights
    :type focus_insights: Dict[str, Any]
    :param velocity: Velocity metrics
    :type velocity: Dict[str, Any]
    :param top_performers: Top performing projects
    :type top_performers: Dict[str, Any]
    :param period_display: Human-readable period
    :type period_display: str
    :param api_analysis: API distribution data
    :type api_analysis: Dict[str, Any]
    :param layer_analysis: Service layer data
    :type layer_analysis: Dict[str, Any]
    :param concentration: Concentration risk data
    :type concentration: Dict[str, Any]
    :param recommendations: List of recommendations
    :type recommendations: List[str]
    :param multiple_focuses: Multiple focus hierarchy (Phase 3)
    :type multiple_focuses: Dict[str, Any]
    :param dynamic_highlights: Dynamic highlights list (Phase 3)
    :type dynamic_highlights: List[Dict[str, str]]
    :param velocity_breakdown: Velocity metrics breakdown (Phase 3)
    :type velocity_breakdown: List[Dict[str, str]]
    :return: Balanced narrative dictionary
    :rtype: Dict[str, Any]
    """
    categories = category_stats['categories']
    total_commits = category_stats['total_commits']
    total_lines = category_stats['total_lines_added']

    #: Determine period characterization
    if velocity['growth_type'] == 'expansion':
        if len(categories) == 1:
            period_summary = "Focused Growth Period"
        else:
            period_summary = "Broad Expansion Period"
    elif velocity['growth_type'] == 'consolidation':
        period_summary = "Optimization Period"
    else:
        period_summary = "Steady Development Period"

    #: Activity Breakdown - Balanced (Observation + Trade-off)
    activity_observation = ""
    activity_balance = ""

    if category_stats['top_category']:
        top_cat_name, top_cat_data = category_stats['top_category']
        top_pct = top_cat_data['percentage']

        activity_observation = (
            f"During {period_display}, development concentrated on "
            f"{top_cat_name} ({top_pct:.1f}% of commits), with "
            f"{len(top_cat_data['projects'])} active service(s) "
            f"delivering {total_commits} commits and {total_lines:,} lines added."
        )

        #: Balanced consideration - dormant services
        if concentration['dormant_count'] > 0:
            activity_balance = (
                f"While this focus strengthens {top_cat_name} capabilities, "
                f"{concentration['dormant_count']} service(s) "
                f"({concentration['dormant_percentage']:.0f}% of portfolio) remained inactive, "
                f"presenting an opportunity to address maintenance needs in future sprints."
            )
        else:
            activity_balance = (
                f"This concentrated effort enables deep expertise development, though "
                f"distributing work across more services could build broader team knowledge."
            )

    #: PHASE 3: Development Focus - Now multi-point (1-3 focuses)
    development_focus_points = []
    for focus in multiple_focuses['focuses']:
        level = focus['level']
        category = focus['category']
        percentage = focus['percentage']
        layer = focus['layer']
        tags = focus['tags']

        observation = (
            f"{level} investment in {category} ({percentage:.1f}% of activity) "
            f"focusing on {layer} with {', '.join(tags[:2]) if len(tags) >= 2 else (tags[0] if tags else 'core development')}"
        )

        #: Generate appropriate balance point based on level
        if level == 'Primary':
            balance = (
                f"This concentration enables rapid {layer.lower()} improvements. "
                f"However, limited activity in other areas may benefit from "
                f"increased allocation for balanced portfolio development"
            )
        elif level == 'Secondary':
            balance = (
                f"Secondary focus provides diversification. Consider opportunities "
                f"to strengthen this area with dedicated sprint allocation"
            )
        else:  # Tertiary
            balance = (
                f"Tertiary focus indicates emerging priority. Monitor for potential "
                f"escalation needs in upcoming planning cycles"
            )

        development_focus_points.append({
            'observation': observation,
            'balance_point': balance
        })

    return {
        'has_summary': True,
        'period_summary': period_summary,
        'activity_breakdown': {
            'observation': activity_observation,
            'balance_point': activity_balance
        },
        'development_focus': development_focus_points,      # CHANGED to list (Phase 3)
        'technical_highlights': dynamic_highlights,         # CHANGED to use Phase 3 data
        'development_velocity': velocity_breakdown,         # CHANGED to list (Phase 3)
        'recommendations': recommendations
    }


def _generate_minimal_summary(period_display: str) -> Dict[str, Any]:
    """
    Generate minimal summary for periods with no activity.

    :param period_display: Human-readable period
    :type period_display: str
    :return: Minimal summary dictionary
    :rtype: Dict[str, Any]

    :Example:

    >>> summary = _generate_minimal_summary("November 2025")
    >>> summary['has_summary']
    True
    >>> 'No significant' in summary['activity_breakdown']
    True
    """
    return {
        'has_summary': True,
        'period_summary': "Maintenance Period",
        'activity_breakdown': (
            f"No significant development activity was recorded during "
            f"{period_display}, suggesting reduced development intensity or "
            f"team focus elsewhere."
        ),
        'development_focus': (
            "This period showed minimal code changes, which may indicate "
            "planning phases, resource allocation to other initiatives, "
            "or preparation for upcoming development cycles."
        ),
        'technical_highlights': [
            "Limited development activity across all services",
            "Period may represent planning or stabilization phase"
        ],
        'velocity_metrics': (
            "No measurable velocity metrics available for this period."
        )
    }
