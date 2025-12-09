"""
Configuration management for KPI Report Generator.

Loads and validates YAML configuration for project analysis.
"""

from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import yaml


@dataclass
class ServiceMetadata:
    """
    Metadata for a single service.

    :param category: Service category (e.g., "Core Infrastructure")
    :param tags: List of tags describing service function
    :param description: Human-readable service description
    """
    category: str
    tags: List[str]
    description: str


@dataclass
class Config:
    """
    Configuration data structure.

    :param projects_directory: Path to directory containing repositories
    :param included_projects: Whitelist of project directory names
    :param file_exclusions: Patterns to exclude from line counts
    :param report_output: Directory for generated reports
    :param valid_branches: Acceptable branch names (main, dev, etc.)
    :param service_metadata: Metadata for each service
    :param tag_descriptions: Human-readable tag descriptions
    :param category_priority: Category ordering for narrative
    :param tag_groups: Tag groupings for service layer analysis
    """
    projects_directory: Path
    included_projects: List[str]
    file_exclusions: List[str]
    report_output: Path
    valid_branches: List[str]
    service_metadata: Dict[str, ServiceMetadata]
    tag_descriptions: Dict[str, str]
    category_priority: List[str]
    tag_groups: Dict[str, Dict[str, List[str]]]


def _validate_service_metadata(data: dict) -> Dict[str, ServiceMetadata]:
    """
    Validate and parse service metadata.

    Ensures all included projects have complete metadata with valid
    tags and categories.

    :param data: Raw config dictionary
    :type data: dict
    :return: Validated service metadata dictionary
    :rtype: Dict[str, ServiceMetadata]
    :raises ValueError: If validation fails

    :Example:

    >>> data = {
    ...     'included_projects': ['service-a'],
    ...     'service_metadata': {
    ...         'service-a': {
    ...             'category': 'Core',
    ...             'tags': ['api'],
    ...             'description': 'Service A'
    ...         }
    ...     },
    ...     'tag_descriptions': {'api': 'API development'},
    ...     'category_priority': ['Core']
    ... }
    >>> metadata = _validate_service_metadata(data)
    >>> metadata['service-a'].category
    'Core'
    """
    included = set(data['included_projects'])
    metadata_keys = set(data.get('service_metadata', {}).keys())

    #: Check all included projects have metadata
    missing = included - metadata_keys
    if missing:
        raise ValueError(
            f"Missing service_metadata for: {', '.join(sorted(missing))}"
        )

    service_metadata = {}
    for service_name, meta in data['service_metadata'].items():
        #: Validate required fields present
        for field in ['category', 'tags', 'description']:
            if field not in meta:
                raise ValueError(
                    f"Service '{service_name}' missing '{field}'"
                )

        #: Validate tags are defined
        for tag in meta['tags']:
            if tag not in data['tag_descriptions']:
                raise ValueError(
                    f"Service '{service_name}' uses undefined tag '{tag}'"
                )

        #: Validate category is defined
        if meta['category'] not in data['category_priority']:
            raise ValueError(
                f"Service '{service_name}' uses undefined "
                f"category '{meta['category']}'"
            )

        service_metadata[service_name] = ServiceMetadata(
            category=meta['category'],
            tags=meta['tags'],
            description=meta['description']
        )

    return service_metadata


def load_config(config_path: str = "config.yaml") -> Config:
    """
    Load configuration from YAML file with local override support.

    Loading hierarchy:
    1. config.local.yaml (if exists) - private organization config
    2. config.yaml (fallback) - public template

    This allows maintaining private organization data while keeping
    the public repository generic.

    :param config_path: Path to config file (default: config.yaml)
    :type config_path: str
    :return: Validated configuration object
    :rtype: Config
    :raises FileNotFoundError: If config file doesn't exist
    :raises yaml.YAMLError: If YAML is malformed
    :raises KeyError: If required fields are missing

    :Example:

    >>> config = load_config("config.yaml")
    >>> config.projects_directory
    PosixPath('./projects')
    """
    #: Only use config hierarchy for default config.yaml
    #: If specific path provided, use it directly
    if config_path == "config.yaml":
        local_config_path = Path("config.local.yaml")
        if local_config_path.exists():
            config_file = local_config_path
            print(f"ℹ️  Using local configuration: {config_file}")
        else:
            config_file = Path(config_path)
            print(f"ℹ️  Using default configuration: {config_file}")
            print("   Create config.local.yaml for custom configuration.")
    else:
        #: Non-default path explicitly provided - use it directly
        config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML: {e}")

    #: Validate required fields
    required_fields = [
        'projects_directory',
        'included_projects',
        'file_exclusions',
        'report_output',
        'valid_branches',
        'service_metadata',
        'tag_descriptions',
        'category_priority',
        'tag_groups'
    ]

    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        raise ValueError(
            f"Missing required config fields: {', '.join(missing_fields)}"
        )

    #: Validate service metadata
    service_metadata = _validate_service_metadata(data)

    #: Convert string paths to Path objects and return config
    return Config(
        projects_directory=Path(data['projects_directory']),
        included_projects=data['included_projects'],
        file_exclusions=data['file_exclusions'],
        report_output=Path(data['report_output']),
        valid_branches=data['valid_branches'],
        service_metadata=service_metadata,
        tag_descriptions=data['tag_descriptions'],
        category_priority=data['category_priority'],
        tag_groups=data['tag_groups']
    )
