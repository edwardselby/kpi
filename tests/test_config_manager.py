"""
Unit tests for config_manager module.

Tests configuration loading and validation.
"""

import pytest
from pathlib import Path
from src.config_manager import load_config, Config
import yaml


class TestConfigManager:
    """Test configuration loading and validation."""

    def test_load_valid_config(self):
        """Test loading valid configuration file."""
        config = load_config("config.yaml")

        assert isinstance(config, Config)
        assert isinstance(config.projects_directory, Path)
        assert isinstance(config.included_projects, list)
        assert len(config.included_projects) > 0
        assert isinstance(config.file_exclusions, list)
        assert isinstance(config.valid_branches, list)

    def test_config_has_required_fields(self):
        """Test that all required fields are present."""
        config = load_config("config.yaml")

        assert config.projects_directory is not None
        assert config.included_projects is not None
        assert config.file_exclusions is not None
        assert config.report_output is not None
        assert config.valid_branches is not None

    def test_load_nonexistent_config(self):
        """Test error when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yaml")

    def test_config_projects_are_strings(self):
        """Test that project names are strings."""
        config = load_config("config.yaml")

        for project in config.included_projects:
            assert isinstance(project, str)
            assert len(project) > 0

    def test_config_local_priority(self, tmp_path, monkeypatch):
        """Test that config.local.yaml takes priority over config.yaml."""
        # Change to test directory
        monkeypatch.chdir(tmp_path)

        # Create generic config.yaml
        config_yaml_data = {
            'projects_directory': './projects',
            'included_projects': ['generic-service'],
            'file_exclusions': ['*.lock'],
            'report_output': './reports',
            'valid_branches': ['main'],
            'service_metadata': {
                'generic-service': {
                    'category': 'Core Infrastructure',
                    'tags': ['API'],
                    'description': 'Generic service'
                }
            },
            'tag_descriptions': {'API': 'API development'},
            'category_priority': ['Core Infrastructure'],
            'tag_groups': {
                'service_layers': {
                    'presentation_layer': ['API']
                },
                'technical_characteristics': {
                    'user_facing': ['API']
                }
            }
        }

        # Create organization-specific config.local.yaml
        config_local_data = config_yaml_data.copy()
        config_local_data['included_projects'] = ['org-specific-service']
        config_local_data['projects_directory'] = '/org/projects'
        config_local_data['service_metadata'] = {
            'org-specific-service': {
                'category': 'Core Infrastructure',
                'tags': ['API'],
                'description': 'Organization service'
            }
        }

        # Write both configs
        with open('config.yaml', 'w') as f:
            yaml.dump(config_yaml_data, f)

        with open('config.local.yaml', 'w') as f:
            yaml.dump(config_local_data, f)

        # Load config - should prefer config.local.yaml
        config = load_config()

        assert config.included_projects == ['org-specific-service']
        assert str(config.projects_directory) == '/org/projects'

    def test_config_fallback_to_default(self, tmp_path, monkeypatch):
        """Test that config.yaml is used when config.local.yaml doesn't exist."""
        # Change to test directory
        monkeypatch.chdir(tmp_path)

        # Create only config.yaml (no config.local.yaml)
        config_yaml_data = {
            'projects_directory': './projects',
            'included_projects': ['generic-service'],
            'file_exclusions': ['*.lock'],
            'report_output': './reports',
            'valid_branches': ['main'],
            'service_metadata': {
                'generic-service': {
                    'category': 'Core Infrastructure',
                    'tags': ['API'],
                    'description': 'Generic service'
                }
            },
            'tag_descriptions': {'API': 'API development'},
            'category_priority': ['Core Infrastructure'],
            'tag_groups': {
                'service_layers': {
                    'presentation_layer': ['API']
                },
                'technical_characteristics': {
                    'user_facing': ['API']
                }
            }
        }

        with open('config.yaml', 'w') as f:
            yaml.dump(config_yaml_data, f)

        # Load config - should use config.yaml
        config = load_config()

        assert config.included_projects == ['generic-service']
        assert str(config.projects_directory) == 'projects'

    def test_config_local_gitignored(self):
        """Test that config.local.yaml is in .gitignore."""
        gitignore_path = Path('.gitignore')

        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_contents = f.read()

            assert 'config.local.yaml' in gitignore_contents, \
                "config.local.yaml should be in .gitignore to prevent accidental commits"
