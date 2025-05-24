"""
Specific source configuration implementations.
"""

import os
from pathlib import Path
from .bootstrap_configuration import SourceConfiguration

class YamlFileSourceConfig(SourceConfiguration):
    """
    Configuration for YAML file-based rule sources.
    """
    
    def __init__(self, properties: dict):
        super().__init__("YamlFile", properties)
        self.path = properties.get("Path")
    
    def validate(self) -> None:
        """
        Validate YAML file source configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.path:
            raise ValueError("YamlFile source requires 'Path' property")
        
        # Convert to Path object for validation
        path_obj = Path(self.path)
        
        # Check if path exists
        if not path_obj.exists():
            raise ValueError(f"Path does not exist: {self.path}")
        
        # Check if path is a directory
        if not path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {self.path}")
        
        # Check if directory is readable
        if not os.access(self.path, os.R_OK):
            raise ValueError(f"Directory is not readable: {self.path}")
    
    def get_path(self) -> str:
        """Get the configured path."""
        return self.path
    
    def get_path_object(self) -> Path:
        """Get the configured path as a Path object."""
        return Path(self.path)
    
    def __str__(self) -> str:
        return f"YamlFile(path='{self.path}')"
    
    def __repr__(self) -> str:
        return f"YamlFileSourceConfig(path='{self.path}')"

# Future source configurations can be added here:
# class DatabaseSourceConfig(SourceConfiguration):
#     def __init__(self, properties: dict):
#         super().__init__("Database", properties)
#         self.connection_string = properties.get("ConnectionString")
#         self.table_name = properties.get("TableName", "agent_rules")
#
# class GitRepositorySourceConfig(SourceConfiguration):
#     def __init__(self, properties: dict):
#         super().__init__("GitRepository", properties)
#         self.repo_url = properties.get("RepoUrl")
#         self.branch = properties.get("Branch", "main")
#         self.rules_path = properties.get("RulesPath", "rules/")
