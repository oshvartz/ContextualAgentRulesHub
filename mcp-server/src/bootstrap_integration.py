"""
Bootstrap integration for connecting MCP server to existing rule system.
"""

import os
import sys
from typing import List, Dict, Any, Optional

# Add the parent src directory to Python path to import existing modules
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, repo_root)  # Add repo root instead of src

# Import from src package
from src.bootstrap.agent_rules_bootstrapper import AgentRulesBootstrapper
from src.repository.agent_rule_repository import AgentRuleRepository
from src.models.agent_rule import AgentRule


class RuleSystemIntegration:
    """
    Integration layer for connecting MCP server to existing rule system.
    """
    
    def __init__(self):
        """Initialize the integration with lazy loading."""
        self._repository: Optional[AgentRuleRepository] = None
        self._bootstrapper: Optional[AgentRulesBootstrapper] = None
        self._initialized = False
    
    def initialize(self) -> None:
        """
        Initialize the rule system by bootstrapping rules from environment configuration.
        
        Raises:
            Exception: If initialization fails
        """
        if self._initialized:
            return
        
        try:
            # Create bootstrapper from environment configuration
            self._bootstrapper = AgentRulesBootstrapper.from_environment()
            
            # Bootstrap repository with rules
            self._repository = self._bootstrapper.bootstrap()
            
            self._initialized = True
            
        except Exception as e:
            raise Exception(f"Failed to initialize rule system: {str(e)}")
    
    def get_all_rules_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all rules in the repository.
        
        Returns:
            List of rule metadata dictionaries
            
        Raises:
            Exception: If repository is not initialized
        """
        if not self._initialized:
            self.initialize()
        
        if not self._repository:
            raise Exception("Repository not initialized")
        
        rules = self._repository.get_all_rules()
        metadata_list = []
        
        for rule in rules:
            # Get source info from the rule's content source
            source_info = rule.get_content_source_info()
            
            metadata = {
                "ruleId": rule.rule_id,
                "description": rule.description,
                "language": rule.language,
                "tags": rule.tags,
                "source": {
                    "sourceType": source_info.get("type", "File")
                }
            }
            metadata_list.append(metadata)
        
        return metadata_list
    
    def get_rule_content_by_id(self, rule_id: str) -> Optional[str]:
        """
        Get the content of a specific rule by its ID.
        
        Args:
            rule_id: The unique identifier of the rule
            
        Returns:
            Rule content as string, or None if rule not found
            
        Raises:
            Exception: If repository is not initialized or content loading fails
        """
        if not self._initialized:
            self.initialize()
        
        if not self._repository:
            raise Exception("Repository not initialized")
        
        try:
            content = self._repository.get_rule_content(rule_id)
            return content
        except Exception as e:
            raise Exception(f"Failed to load content for rule '{rule_id}': {str(e)}")
    
    def get_repository_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the repository.
        
        Returns:
            Dictionary with repository statistics
        """
        if not self._initialized:
            self.initialize()
        
        if not self._repository:
            return {"total_rules": 0, "status": "not_initialized"}
        
        stats = self._repository.get_repository_stats()
        
        # Add bootstrap stats if available
        if self._bootstrapper and self._bootstrapper.get_bootstrap_stats():
            bootstrap_stats = self._bootstrapper.get_bootstrap_stats()
            stats.update({
                "bootstrap_success_rate": bootstrap_stats.get_success_rate(),
                "bootstrap_time_seconds": bootstrap_stats.total_time_seconds,
                "sources_loaded": bootstrap_stats.successful_sources,
                "sources_failed": bootstrap_stats.failed_sources
            })
        
        return stats
    
    def rule_exists(self, rule_id: str) -> bool:
        """
        Check if a rule exists in the repository.
        
        Args:
            rule_id: The unique identifier of the rule
            
        Returns:
            True if rule exists, False otherwise
        """
        if not self._initialized:
            self.initialize()
        
        if not self._repository:
            return False
        
        return self._repository.rule_exists(rule_id)


# Global instance for the MCP server
rule_system = RuleSystemIntegration()
