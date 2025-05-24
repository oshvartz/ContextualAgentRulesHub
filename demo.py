"""
Demo script showing the refactored AgentRule system in action.
"""

from src.models.agent_rule import AgentRule
from src.models.rule_content_source import YamlFileContentSource
from src.repository.agent_rule_repository import AgentRuleRepository
from src.loaders.yaml_loader import YamlRuleLoader

def main():
    print("=== AgentRule System Demo ===\n")
    
    # Create repository
    repository = AgentRuleRepository()
    
    # Create YAML loader
    loader = YamlRuleLoader("rules")
    
    print("1. Loading rules from YAML files...")
    try:
        loaded_count = loader.load_rules_to_repository(repository)
        print(f"   Successfully loaded {loaded_count} rules\n")
    except Exception as e:
        print(f"   Error loading rules: {e}\n")
        return
    
    # Show repository stats
    print("2. Repository Statistics:")
    stats = repository.get_repository_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # List all rules
    print("3. All Rules:")
    for rule in repository.get_all_rules():
        print(f"   - {rule.rule_id}: {rule.description}")
        print(f"     Language: {rule.language or 'None'}")
        print(f"     Tags: {', '.join(rule.tags)}")
        print()
    
    # Demonstrate on-demand content loading
    print("4. Loading rule content on-demand:")
    rule_id = "code-review-standards"
    rule = repository.get_rule(rule_id)
    
    if rule:
        print(f"   Rule: {rule.rule_id}")
        print(f"   Content Source: {rule.content_source}")
        
        try:
            content = rule.load_content()
            content_preview = content[:200] + "..." if len(content) > 200 else content
            print(f"   Content Preview: {content_preview}")
        except Exception as e:
            print(f"   Error loading content: {e}")
    else:
        print(f"   Rule '{rule_id}' not found")
    print()
    
    # Demonstrate filtering
    print("5. Filtering Examples:")
    
    # By tag
    review_rules = repository.get_rules_by_tag("code-review")
    print(f"   Rules with 'code-review' tag: {len(review_rules)}")
    for rule in review_rules:
        print(f"     - {rule.rule_id}")
    
    # By multiple tags
    best_practice_rules = repository.get_rules_by_tags_any(["best-practices", "collaboration"])
    print(f"   Rules with 'best-practices' OR 'collaboration' tags: {len(best_practice_rules)}")
    for rule in best_practice_rules:
        print(f"     - {rule.rule_id}")
    
    # Search by description
    search_results = repository.search_rules_by_description("review")
    print(f"   Rules containing 'review' in description: {len(search_results)}")
    for rule in search_results:
        print(f"     - {rule.rule_id}: {rule.description}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    main()
