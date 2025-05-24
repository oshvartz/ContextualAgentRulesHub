"""
YAML loader for loading agent rules from YAML files.
"""

import os
import yaml
from pathlib import Path
from typing import List, Optional
from ..models.agent_rule import AgentRule
from ..models.rule_content_source import YamlFileContentSource, ContentLoadError
from ..repository.agent_rule_repository import AgentRuleRepository

class YamlRuleLoader:
    """
    Loader for agent rules from YAML files.
    
    Scans a directory for YAML files and loads rule metadata,
    creating AgentRule objects with YamlFileContentSource.
    """
    
    def __init__(self, rules_directory: str):
        """
        Initialize YAML rule loader.
        
        Args:
            rules_directory: Path to directory containing YAML rule files
        """
        self.rules_directory = Path(rules_directory)
    
    def load_rules_to_repository(self, repository: AgentRuleRepository) -> int:
        """
        Load all YAML rules from directory into the repository.
        
        Args:
            repository: AgentRuleRepository to populate
            
        Returns:
            Number of rules successfully loaded
            
        Raises:
            FileNotFoundError: If rules directory doesn't exist
            ValueError: If duplicate rule IDs are found
        """
        if not self.rules_directory.exists():
            raise FileNotFoundError(f"Rules directory not found: {self.rules_directory}")
        
        if not self.rules_directory.is_dir():
            raise ValueError(f"Rules path is not a directory: {self.rules_directory}")
        
        loaded_count = 0
        yaml_files = self._find_yaml_files()
        
        for yaml_file in yaml_files:
            try:
                rule = self._load_rule_from_file(yaml_file)
                if rule:
                    repository.add_rule(rule)
                    loaded_count += 1
                    print(f"Loaded rule: {rule.rule_id}")
            except Exception as e:
                print(f"Warning: Failed to load rule from {yaml_file}: {e}")
                continue
        
        return loaded_count
    
    def load_rules(self) -> List[AgentRule]:
        """
        Load all YAML rules from directory.
        
        Returns:
            List of AgentRule objects
            
        Raises:
            FileNotFoundError: If rules directory doesn't exist
        """
        repository = AgentRuleRepository()
        self.load_rules_to_repository(repository)
        return repository.get_all_rules()
    
    def _find_yaml_files(self) -> List[Path]:
        """
        Find all YAML files in the rules directory.
        
        Returns:
            List of Path objects for YAML files
        """
        yaml_extensions = ['.yaml', '.yml']
        yaml_files = []
        
        for file_path in self.rules_directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in yaml_extensions:
                yaml_files.append(file_path)
        
        return sorted(yaml_files)
    
    def _load_rule_from_file(self, yaml_file: Path) -> Optional[AgentRule]:
        """
        Load a single rule from a YAML file.
        
        Args:
            yaml_file: Path to YAML file
            
        Returns:
            AgentRule object or None if file is invalid
            
        Raises:
            ContentLoadError: If YAML file cannot be parsed
            ValueError: If required fields are missing
        """
        try:
            with open(yaml_file, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if not isinstance(data, dict):
                raise ValueError(f"Invalid YAML structure in {yaml_file}")
            
            # Extract metadata
            rule_id = data.get('id')
            if not rule_id:
                raise ValueError(f"Missing 'id' field in {yaml_file}")
            
            description = data.get('description', '')
            if not description:
                raise ValueError(f"Missing 'description' field in {yaml_file}")
            
            language = data.get('language')
            # Convert null/None to None
            if language == 'null' or language is None:
                language = None
            
            tags = data.get('tags', [])
            if not isinstance(tags, list):
                raise ValueError(f"'tags' must be a list in {yaml_file}")
            
            # Ensure 'rule' field exists (even if we don't load content now)
            if 'rule' not in data:
                raise ValueError(f"Missing 'rule' field in {yaml_file}")
            
            # Create content source
            content_source = YamlFileContentSource(str(yaml_file))
            
            # Create AgentRule
            rule = AgentRule(
                rule_id=rule_id,
                description=description,
                language=language,
                tags=tags,
                content_source=content_source
            )
            
            return rule
            
        except yaml.YAMLError as e:
            raise ContentLoadError(f"YAML parsing error in {yaml_file}: {e}")
        except IOError as e:
            raise ContentLoadError(f"File read error for {yaml_file}: {e}")
    
    def validate_yaml_file(self, yaml_file: Path) -> dict:
        """
        Validate a single YAML file without loading it into repository.
        
        Args:
            yaml_file: Path to YAML file to validate
            
        Returns:
            Dictionary with validation results
        """
        result = {
            "file": str(yaml_file),
            "valid": False,
            "errors": [],
            "rule_id": None
        }
        
        try:
            rule = self._load_rule_from_file(yaml_file)
            if rule:
                result["valid"] = True
                result["rule_id"] = rule.rule_id
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    def validate_all_files(self) -> dict:
        """
        Validate all YAML files in the directory.
        
        Returns:
            Dictionary with validation results for all files
        """
        if not self.rules_directory.exists():
            return {
                "directory_exists": False,
                "error": f"Directory not found: {self.rules_directory}"
            }
        
        yaml_files = self._find_yaml_files()
        results = {
            "directory_exists": True,
            "total_files": len(yaml_files),
            "valid_files": 0,
            "invalid_files": 0,
            "files": []
        }
        
        for yaml_file in yaml_files:
            file_result = self.validate_yaml_file(yaml_file)
            results["files"].append(file_result)
            
            if file_result["valid"]:
                results["valid_files"] += 1
            else:
                results["invalid_files"] += 1
        
        return results
    
    def get_loader_info(self) -> dict:
        """
        Get information about this loader.
        
        Returns:
            Dictionary with loader information
        """
        return {
            "loader_type": "YamlRuleLoader",
            "rules_directory": str(self.rules_directory),
            "directory_exists": self.rules_directory.exists(),
            "supported_extensions": [".yaml", ".yml"]
        }
    
    def __str__(self) -> str:
        """String representation of the loader."""
        return f"YamlRuleLoader({self.rules_directory})"
    
    def __repr__(self) -> str:
        """Developer representation of the loader."""
        return f"YamlRuleLoader(rules_directory='{self.rules_directory}')"
