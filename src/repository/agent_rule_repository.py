"""
Simple in-memory repository for AgentRule management.
"""

from typing import Dict, List, Optional
from ..models.agent_rule import AgentRule

class AgentRuleRepository:
    """
    Simple in-memory repository for storing and querying agent rules.
    
    Uses a dictionary mapping rule_id -> AgentRule for fast lookups.
    """
    
    def __init__(self):
        """Initialize empty repository."""
        self._rules: Dict[str, AgentRule] = {}
    
    def add_rule(self, rule: AgentRule) -> None:
        """
        Add a rule to the repository.
        
        Args:
            rule: AgentRule to add
            
        Raises:
            ValueError: If rule with same ID already exists
        """
        if rule.rule_id in self._rules:
            raise ValueError(f"Rule with ID '{rule.rule_id}' already exists")
        
        self._rules[rule.rule_id] = rule
    
    def update_rule(self, rule: AgentRule) -> None:
        """
        Update an existing rule in the repository.
        
        Args:
            rule: AgentRule to update
            
        Raises:
            ValueError: If rule doesn't exist
        """
        if rule.rule_id not in self._rules:
            raise ValueError(f"Rule with ID '{rule.rule_id}' not found")
        
        self._rules[rule.rule_id] = rule
    
    def remove_rule(self, rule_id: str) -> bool:
        """
        Remove a rule from the repository.
        
        Args:
            rule_id: ID of rule to remove
            
        Returns:
            True if rule was removed, False if not found
        """
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[AgentRule]:
        """
        Get a rule by its ID.
        
        Args:
            rule_id: Unique identifier of the rule
            
        Returns:
            AgentRule if found, None otherwise
        """
        return self._rules.get(rule_id)
    
    def get_rule_content(self, rule_id: str) -> Optional[str]:
        """
        Get the content of a rule by its ID.
        
        Args:
            rule_id: Unique identifier of the rule
            
        Returns:
            Rule content as string if found, None otherwise
            
        Raises:
            ContentLoadError: If there's an error loading the content
        """
        rule = self.get_rule(rule_id)
        if rule is None:
            return None
        
        return rule.load_content()
    
    def get_all_rules(self) -> List[AgentRule]:
        """Get all rules in the repository."""
        return list(self._rules.values())
    
    def get_all_rule_ids(self) -> List[str]:
        """Get all rule IDs in the repository."""
        return list(self._rules.keys())
    
    def get_rules_by_language(self, language: str) -> List[AgentRule]:
        """
        Get all rules for a specific language.
        
        Args:
            language: Programming language or domain
            
        Returns:
            List of rules matching the language
        """
        return [rule for rule in self._rules.values() 
                if rule.matches_language(language)]
    
    def get_rules_by_tag(self, tag: str) -> List[AgentRule]:
        """
        Get all rules with a specific tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of rules with the specified tag
        """
        return [rule for rule in self._rules.values() 
                if rule.has_tag(tag)]
    
    def get_rules_by_tags_any(self, tags: List[str]) -> List[AgentRule]:
        """
        Get all rules that have any of the specified tags.
        
        Args:
            tags: List of tags (OR logic)
            
        Returns:
            List of rules matching any of the tags
        """
        return [rule for rule in self._rules.values() 
                if rule.has_any_tag(tags)]
    
    def get_rules_by_tags_all(self, tags: List[str]) -> List[AgentRule]:
        """
        Get all rules that have all of the specified tags.
        
        Args:
            tags: List of tags (AND logic)
            
        Returns:
            List of rules matching all of the tags
        """
        return [rule for rule in self._rules.values() 
                if rule.has_all_tags(tags)]
    
    def search_rules_by_description(self, query: str) -> List[AgentRule]:
        """
        Search rules by description text (case-insensitive).
        
        Args:
            query: Search query string
            
        Returns:
            List of rules whose descriptions contain the query
        """
        query_lower = query.lower()
        return [rule for rule in self._rules.values() 
                if query_lower in rule.description.lower()]
    
    def get_rules_by_criteria(self,
                            language: Optional[str] = None,
                            tags: Optional[List[str]] = None,
                            tags_mode: str = "any",
                            description_query: Optional[str] = None,
                            context: Optional[str] = None,
                            is_core: Optional[bool] = None) -> List[AgentRule]:
        """
        Get rules by multiple criteria.
        
        Args:
            language: Filter by language (optional)
            tags: Filter by tags (optional)
            tags_mode: Either "any" or "all" for tag matching
            description_query: Search in descriptions (optional)
            context: Filter by context (optional):
                - If None: returns only rules without context
                - If provided: returns rules with no context OR matching context
            is_core: Filter by is_core status (True, False, or None for no filter) (optional)
            
        Returns:
            List of rules matching all specified criteria
        """
        rules = self.get_all_rules()
        
        # Filter by language
        if language:
            rules = [rule for rule in rules if rule.matches_language(language)]
        
        # Filter by tags
        if tags:
            if tags_mode.lower() == "all":
                rules = [rule for rule in rules if rule.has_all_tags(tags)]
            else:  # any
                rules = [rule for rule in rules if rule.has_any_tag(tags)]
        
        # Filter by description query
        if description_query:
            query_lower = description_query.lower()
            rules = [rule for rule in rules
                    if query_lower in rule.description.lower()]
        
        # Filter by context
        if context is not None:
            # If context filter is provided: include rules with no context OR matching context
            context_lower = context.lower()
            rules = [
                rule for rule in rules
                if rule.context is None or rule.context.lower() == context_lower
            ]
        else:
            # If no context filter is provided: return only rules without context
            rules = [rule for rule in rules if rule.context is None]

        # Filter by is_core status
        if is_core is not None:
            rules = [rule for rule in rules if rule.is_core == is_core]
        
        return rules
    
    def get_available_languages(self) -> List[str]:
        """Get list of all available languages (excluding None)."""
        languages = set()
        for rule in self._rules.values():
            if rule.language:
                languages.add(rule.language)
        return sorted(list(languages))
    
    def get_available_tags(self) -> List[str]:
        """Get list of all available tags."""
        tags = set()
        for rule in self._rules.values():
            tags.update(rule.tags)
        return sorted(list(tags))
    
    def get_available_contexts(self) -> List[str]:
        """Get list of all available contexts (excluding None)."""
        contexts = set()
        for rule in self._rules.values():
            if rule.context:
                contexts.add(rule.context)
        return sorted(list(contexts))
    
    def get_repository_stats(self) -> dict:
        """
        Get statistics about the repository.
        
        Returns:
            Dictionary with repository statistics
        """
        return {
            "total_rules": len(self._rules),
            "total_languages": len(self.get_available_languages()),
            "total_tags": len(self.get_available_tags()),
            "total_contexts": len(self.get_available_contexts()),
            "available_languages": self.get_available_languages(),
            "available_tags": self.get_available_tags(),
            "available_contexts": self.get_available_contexts()
        }
    
    def clear(self) -> None:
        """Clear all rules from the repository."""
        self._rules.clear()
    
    def rule_exists(self, rule_id: str) -> bool:
        """Check if a rule exists in the repository."""
        return rule_id in self._rules
    
    def __len__(self) -> int:
        """Get the number of rules in the repository."""
        return len(self._rules)
    
    def __contains__(self, rule_id: str) -> bool:
        """Check if a rule ID exists in the repository."""
        return rule_id in self._rules
    
    def __str__(self) -> str:
        """String representation of the repository."""
        return f"AgentRuleRepository({len(self._rules)} rules)"
    
    def __repr__(self) -> str:
        """Developer representation of the repository."""
        return f"AgentRuleRepository(rules={len(self._rules)})"
