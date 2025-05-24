"""
Rule content source for on-demand loading of rule content.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from typing import Optional


class RuleContentSource(ABC):
    """
    Abstract base class for rule content sources.
    
    Provides interface for loading rule content on-demand from various sources.
    """
    
    @abstractmethod
    def load_content(self) -> str:
        """
        Load the rule content from the source.
        
        Returns:
            Rule content as string
            
        Raises:
            ContentLoadError: If content cannot be loaded
        """
        pass
    
    @abstractmethod
    def get_source_info(self) -> dict:
        """
        Get information about this content source.
        
        Returns:
            Dictionary with source information
        """
        pass


class YamlFileContentSource(RuleContentSource):
    """
    Content source for YAML files.
    
    Loads rule content from a YAML file's 'rule' field.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize YAML file content source.
        
        Args:
            file_path: Path to the YAML file containing the rule
        """
        self.file_path = Path(file_path)
    
    def load_content(self) -> str:
        """
        Load rule content from YAML file.
        
        Returns:
            Rule content from the 'rule' field in the YAML file
            
        Raises:
            ContentLoadError: If file cannot be read or parsed
        """
        try:
            if not self.file_path.exists():
                raise ContentLoadError(f"YAML file not found: {self.file_path}")
            
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if not isinstance(data, dict):
                raise ContentLoadError(f"Invalid YAML structure in {self.file_path}")
            
            rule_content = data.get('rule')
            if rule_content is None:
                raise ContentLoadError(f"No 'rule' field found in {self.file_path}")
            
            return str(rule_content)
            
        except yaml.YAMLError as e:
            raise ContentLoadError(f"YAML parsing error in {self.file_path}: {e}")
        except IOError as e:
            raise ContentLoadError(f"File read error for {self.file_path}: {e}")
    
    def get_source_info(self) -> dict:
        """Get information about this YAML file source."""
        return {
            "source_type": "YamlFile",
            "file_path": str(self.file_path),
            "exists": self.file_path.exists()
        }
    
    def __str__(self) -> str:
        """String representation of the source."""
        return f"YamlFileContentSource({self.file_path})"
    
    def __repr__(self) -> str:
        """Developer representation of the source."""
        return f"YamlFileContentSource(file_path='{self.file_path}')"


class ContentLoadError(Exception):
    """Exception raised when rule content cannot be loaded."""
    pass
