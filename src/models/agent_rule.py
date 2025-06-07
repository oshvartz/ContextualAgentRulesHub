"""
Agent rule entity model for storing rule metadata.
"""

from dataclasses import dataclass
from typing import List, Optional
from .rule_content_source import RuleContentSource

@dataclass
class AgentRule:
    """
    Represents an agent rule with metadata and on-demand content loading.
    
    Attributes:
        rule_id: Unique identifier for the rule
        description: Human-readable description of the rule
        language: Optional programming language or domain the rule applies to
        tags: List of tags for categorization and filtering
        content_source: RuleContentSource for on-demand content loading
        context: Optional context the rule applies to (e.g., project name)
        is_core: Optional boolean indicating if this is a core rule, defaults to False
    """
    rule_id: str
    description: str
    language: Optional[str]
    tags: List[str]
    content_source: RuleContentSource
    context: Optional[str] = None
    is_core: Optional[bool] = False
    
    def __post_init__(self):
        """Validate rule data after initialization."""
        if not self.rule_id or not self.rule_id.strip():
            raise ValueError("Rule ID cannot be empty")
        
        if not self.description or not self.description.strip():
            raise ValueError("Rule description cannot be empty")
        
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list")
        
        # Ensure tags are strings and not empty
        self.tags = [tag.strip() for tag in self.tags if tag and tag.strip()]
        
        if self.content_source is None:
            raise ValueError("Content source cannot be None")
    
    def load_content(self) -> str:
        """
        Load the rule content on-demand from the content source.
        
        Returns:
            Rule content as string
            
        Raises:
            ContentLoadError: If content cannot be loaded
        """
        return self.content_source.load_content()
    
    def has_tag(self, tag: str) -> bool:
        """Check if the rule has a specific tag."""
        return tag.lower() in [t.lower() for t in self.tags]
    
    def has_any_tag(self, tags: List[str]) -> bool:
        """Check if the rule has any of the specified tags."""
        lower_tags = [t.lower() for t in self.tags]
        return any(tag.lower() in lower_tags for tag in tags)
    
    def has_all_tags(self, tags: List[str]) -> bool:
        """Check if the rule has all of the specified tags."""
        lower_tags = [t.lower() for t in self.tags]
        return all(tag.lower() in lower_tags for tag in tags)
    
    def matches_language(self, language: str) -> bool:
        """Check if the rule matches a specific language (case-insensitive)."""
        if not self.language:
            return False
        return self.language.lower() == language.lower()
    
    def get_content_source_info(self) -> dict:
        """Get information about the content source."""
        return self.content_source.get_source_info()
    
    def __str__(self) -> str:
        """String representation of the rule."""
        return f"AgentRule({self.rule_id}: {self.description})"
    
    def __repr__(self) -> str:
        """Developer representation of the rule."""
        return (f"AgentRule(rule_id='{self.rule_id}', description='{self.description}', "
                f"language='{self.language}', tags={self.tags}, context='{self.context}', "
                f"is_core={self.is_core})")
