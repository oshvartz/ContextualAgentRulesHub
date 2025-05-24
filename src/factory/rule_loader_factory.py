"""
Factory for creating rule loaders based on source configurations.
"""

import logging
from typing import Dict, Type, Union
from abc import ABC, abstractmethod

from ..config.bootstrap_configuration import SourceConfiguration
from ..config.source_configs import YamlFileSourceConfig
from ..loaders.yaml_loader import YamlRuleLoader
from ..repository.agent_rule_repository import AgentRuleRepository

class RuleLoader(ABC):
    """
    Abstract base class for rule loaders.
    """
    
    @abstractmethod
    def load_rules_to_repository(self, repository: AgentRuleRepository) -> int:
        """
        Load rules into the given repository.
        
        Args:
            repository: Repository to load rules into
            
        Returns:
            Number of rules loaded
        """
        pass

class RuleLoaderFactory:
    """
    Factory for creating rule loaders based on source configuration.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._loaders: Dict[str, Type[RuleLoader]] = {
            "YamlFile": YamlRuleLoader,
            # Future loaders can be registered here
        }
    
    def create_loader(self, source_config: SourceConfiguration) -> RuleLoader:
        """
        Create appropriate loader for source configuration.
        
        Args:
            source_config: Source configuration to create loader for
            
        Returns:
            Configured rule loader instance
            
        Raises:
            ValueError: If source type is not supported or configuration invalid
        """
        source_type = source_config.source_type
        
        if source_type not in self._loaders:
            supported_types = list(self._loaders.keys())
            raise ValueError(f"Unsupported source type '{source_type}'. Supported types: {supported_types}")
        
        loader_class = self._loaders[source_type]
        
        # Create loader based on source type
        if source_type == "YamlFile":
            return self._create_yaml_file_loader(source_config)
        
        # Future source types would be handled here
        
        raise ValueError(f"No factory method implemented for source type: {source_type}")
    
    def _create_yaml_file_loader(self, source_config: SourceConfiguration) -> YamlRuleLoader:
        """
        Create YAML file loader from configuration.
        
        Args:
            source_config: YamlFile source configuration
            
        Returns:
            Configured YamlRuleLoader
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not isinstance(source_config, YamlFileSourceConfig):
            raise ValueError(f"Expected YamlFileSourceConfig, got {type(source_config)}")
        
        # Validate the configuration
        source_config.validate()
        
        # Create loader with the configured path
        loader = YamlRuleLoader(source_config.get_path())
        
        self.logger.debug(f"Created YamlRuleLoader for path: {source_config.get_path()}")
        
        return loader
    
    def register_loader(self, source_type: str, loader_class: Type[RuleLoader]) -> None:
        """
        Register a new loader type.
        
        Args:
            source_type: Name of the source type
            loader_class: Loader class that implements RuleLoader interface
        """
        if not issubclass(loader_class, RuleLoader):
            raise ValueError(f"Loader class must inherit from RuleLoader")
        
        self._loaders[source_type] = loader_class
        self.logger.info(f"Registered loader type: {source_type} -> {loader_class.__name__}")
    
    def get_supported_types(self) -> list[str]:
        """
        Get list of supported source types.
        
        Returns:
            List of supported source type names
        """
        return list(self._loaders.keys())
    
    def is_supported(self, source_type: str) -> bool:
        """
        Check if a source type is supported.
        
        Args:
            source_type: Source type to check
            
        Returns:
            True if supported, False otherwise
        """
        return source_type in self._loaders
    
    def get_loader_info(self) -> Dict[str, str]:
        """
        Get information about registered loaders.
        
        Returns:
            Dictionary mapping source types to loader class names
        """
        return {
            source_type: loader_class.__name__ 
            for source_type, loader_class in self._loaders.items()
        }
    
    def __str__(self) -> str:
        return f"RuleLoaderFactory(supported_types={list(self._loaders.keys())})"
    
    def __repr__(self) -> str:
        return f"RuleLoaderFactory(loaders={self._loaders})"

# Make YamlRuleLoader compatible with the RuleLoader interface
# Note: YamlRuleLoader already has the required load_rules_to_repository method
