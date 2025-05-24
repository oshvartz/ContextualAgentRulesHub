"""
Environment variable parser for Agent Rules Hub configuration.
"""

import os
import re
import logging
from typing import Dict, List
from .bootstrap_configuration import BootstrapConfiguration, SourceConfiguration
from .source_configs import YamlFileSourceConfig

class EnvironmentConfigurationParser:
    """
    Parser for environment variables with indexed configuration pattern.
    
    Supports pattern like:
    RulesLoaderOptions:0:SourceType = YamlFile
    RulesLoaderOptions:0:Path = ./rules
    RulesLoaderOptions:1:SourceType = YamlFile
    RulesLoaderOptions:1:Path = c:/git/rules
    """
    
    ENV_PREFIX = "RulesLoaderOptions"
    
    # Registry of supported source types
    SOURCE_TYPE_REGISTRY = {
        "YamlFile": YamlFileSourceConfig,
        # Future: "Database": DatabaseSourceConfig,
        # Future: "GitRepository": GitRepositorySourceConfig,
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_bootstrap_configuration(self) -> BootstrapConfiguration:
        """
        Parse complete bootstrap configuration from environment variables.
        
        Returns:
            BootstrapConfiguration with all parsed sources
            
        Raises:
            ValueError: If no valid sources found or configuration invalid
        """
        sources = self.parse_rules_loader_options()
        
        if not sources:
            raise ValueError("No valid rule sources found in environment variables")
        
        # Parse optional global settings
        validation_enabled = self._parse_bool_env("AGENT_RULES_VALIDATION", True)
        log_level = os.getenv("AGENT_RULES_LOG_LEVEL", "INFO").upper()
        
        return BootstrapConfiguration(
            sources=sources,
            validation_enabled=validation_enabled,
            log_level=log_level
        )
    
    def parse_rules_loader_options(self) -> List[SourceConfiguration]:
        """
        Parse indexed RulesLoaderOptions from environment variables.
        
        Returns:
            List of parsed source configurations
        """
        sources = []
        indices = self._extract_source_indices()
        
        self.logger.info(f"Found {len(indices)} source indices: {sorted(indices)}")
        
        for index in sorted(indices):
            try:
                source_config = self._parse_source_config(index)
                if source_config:
                    sources.append(source_config)
                    self.logger.info(f"Parsed source {index}: {source_config.source_type}")
            except Exception as e:
                self.logger.warning(f"Failed to parse source {index}: {e}")
                continue
        
        return sources
    
    def _extract_source_indices(self) -> List[int]:
        """
        Find all indices used in RulesLoaderOptions:X:* variables.
        
        Returns:
            List of unique indices found in environment variables
        """
        indices = set()
        
        # Due to Windows limitations with environment variable keys containing colons,
        # we need to probe for indices rather than iterate through all keys
        max_probe = 100  # Reasonable upper limit for number of sources
        
        for i in range(max_probe):
            # Check if this index has a SourceType defined
            source_type_key = f"{self.ENV_PREFIX}:{i}:SourceType"
            if source_type_key in os.environ:
                indices.add(i)
        
        return list(indices)
    
    def _parse_source_config(self, index: int) -> SourceConfiguration:
        """
        Parse configuration for a specific source index.
        
        Args:
            index: Source index to parse
            
        Returns:
            SourceConfiguration for the given index
            
        Raises:
            ValueError: If required configuration is missing or invalid
        """
        # Extract all properties for this index using direct access
        # (due to Windows limitations with iterating environment variables with colons)
        properties = {}
        prefix = f"{self.ENV_PREFIX}:{index}:"
        
        # Known property names for different source types
        potential_properties = ["SourceType", "Path", "ConnectionString", "TableName", "RepoUrl", "Branch", "RulesPath"]
        
        for prop_name in potential_properties:
            key = f"{prefix}{prop_name}"
            if key in os.environ:
                properties[prop_name] = os.environ[key]
        
        if not properties:
            raise ValueError(f"No properties found for source index {index}")
        
        source_type = properties.get("SourceType")
        if not source_type:
            raise ValueError(f"Missing SourceType for index {index}")
        
        return self._create_source_config(source_type, properties)
    
    def _create_source_config(self, source_type: str, properties: Dict[str, str]) -> SourceConfiguration:
        """
        Factory method to create appropriate source configuration.
        
        Args:
            source_type: Type of source (e.g., "YamlFile")
            properties: Dictionary of properties from environment variables
            
        Returns:
            Appropriate SourceConfiguration subclass instance
            
        Raises:
            ValueError: If source type is not supported
        """
        if source_type not in self.SOURCE_TYPE_REGISTRY:
            supported_types = list(self.SOURCE_TYPE_REGISTRY.keys())
            raise ValueError(f"Unsupported source type '{source_type}'. Supported types: {supported_types}")
        
        config_class = self.SOURCE_TYPE_REGISTRY[source_type]
        return config_class(properties)
    
    def _parse_bool_env(self, env_var: str, default: bool) -> bool:
        """
        Parse boolean environment variable.
        
        Args:
            env_var: Environment variable name
            default: Default value if not set
            
        Returns:
            Boolean value
        """
        value = os.getenv(env_var)
        if value is None:
            return default
        
        return value.lower() in ("true", "1", "yes", "on")
    
    def validate_environment(self) -> Dict[str, any]:
        """
        Validate environment configuration without parsing.
        
        Returns:
            Dictionary with validation results
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "sources_found": 0,
            "indices": []
        }
        
        try:
            indices = self._extract_source_indices()
            result["indices"] = sorted(indices)
            result["sources_found"] = len(indices)
            
            if not indices:
                result["valid"] = False
                result["errors"].append("No RulesLoaderOptions found in environment")
                return result
            
            for index in indices:
                try:
                    self._parse_source_config(index)
                except Exception as e:
                    result["warnings"].append(f"Source {index}: {e}")
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Environment validation failed: {e}")
        
        return result
    
    def get_supported_source_types(self) -> List[str]:
        """
        Get list of supported source types.
        
        Returns:
            List of supported source type names
        """
        return list(self.SOURCE_TYPE_REGISTRY.keys())
    
    def register_source_type(self, source_type: str, config_class: type) -> None:
        """
        Register a new source type.
        
        Args:
            source_type: Name of the source type
            config_class: Configuration class for the source type
        """
        self.SOURCE_TYPE_REGISTRY[source_type] = config_class
        self.logger.info(f"Registered source type: {source_type}")
    
    def print_environment_example(self) -> None:
        """Print example environment variable configuration."""
        print("Example environment configuration:")
        print()
        print("# First YAML source")
        print("RulesLoaderOptions:0:SourceType=YamlFile")
        print("RulesLoaderOptions:0:Path=./rules")
        print()
        print("# Second YAML source")
        print("RulesLoaderOptions:1:SourceType=YamlFile")
        print("RulesLoaderOptions:1:Path=c:/git/shared-rules")
        print()
        print("# Optional global settings")
        print("AGENT_RULES_VALIDATION=true")
        print("AGENT_RULES_LOG_LEVEL=INFO")
    
    def __str__(self) -> str:
        return f"EnvironmentConfigurationParser(supported_types={list(self.SOURCE_TYPE_REGISTRY.keys())})"
    
    def __repr__(self) -> str:
        return f"EnvironmentConfigurationParser(registry={self.SOURCE_TYPE_REGISTRY})"
