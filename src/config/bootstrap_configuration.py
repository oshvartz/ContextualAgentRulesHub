"""
Bootstrap configuration classes for Agent Rules Hub.
"""

from dataclasses import dataclass
from typing import Dict, List
from abc import ABC, abstractmethod

@dataclass
class SourceConfiguration(ABC):
    """
    Abstract base class for rule source configurations.
    """
    source_type: str
    properties: Dict[str, str]
    
    def __init__(self, source_type: str, properties: Dict[str, str]):
        self.source_type = source_type
        self.properties = properties
    
    @abstractmethod
    def validate(self) -> None:
        """
        Validate the source configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        pass
    
    def get_property(self, key: str, default: str = None) -> str:
        """
        Get a property value.
        
        Args:
            key: Property key
            default: Default value if key not found
            
        Returns:
            Property value or default
        """
        return self.properties.get(key, default)
    
    def __str__(self) -> str:
        return f"{self.source_type}({self.properties})"
    
    def __repr__(self) -> str:
        return f"SourceConfiguration(source_type='{self.source_type}', properties={self.properties})"

@dataclass
class BootstrapConfiguration:
    """
    Configuration for the Agent Rules Bootstrapper.
    """
    sources: List[SourceConfiguration]
    validation_enabled: bool = True
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.sources:
            raise ValueError("At least one source must be configured")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            raise ValueError(f"Invalid log level: {self.log_level}")
    
    def get_sources_by_type(self, source_type: str) -> List[SourceConfiguration]:
        """
        Get all sources of a specific type.
        
        Args:
            source_type: Type of source to filter by
            
        Returns:
            List of sources matching the type
        """
        return [source for source in self.sources if source.source_type == source_type]
    
    def get_source_types(self) -> List[str]:
        """
        Get list of all source types in configuration.
        
        Returns:
            List of unique source types
        """
        return list(set(source.source_type for source in self.sources))
    
    def validate_all_sources(self) -> List[str]:
        """
        Validate all source configurations.
        
        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []
        for i, source in enumerate(self.sources):
            try:
                source.validate()
            except ValueError as e:
                errors.append(f"Source {i} ({source.source_type}): {e}")
        
        return errors
    
    def __len__(self) -> int:
        """Return number of configured sources."""
        return len(self.sources)
    
    def __str__(self) -> str:
        return f"BootstrapConfiguration({len(self.sources)} sources, validation={self.validation_enabled})"
    
    def __repr__(self) -> str:
        return f"BootstrapConfiguration(sources={self.sources}, validation_enabled={self.validation_enabled}, log_level='{self.log_level}')"
