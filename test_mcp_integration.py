#!/usr/bin/env python3
"""
Simple test for the MCP server integration.
"""

import os
import sys
from pathlib import Path

# Set up environment variables for the rule system
os.environ["RulesLoaderOptions:0:SourceType"] = "YamlFile"
os.environ["RulesLoaderOptions:0:Path"] = "./rules"
os.environ["AGENT_RULES_VALIDATION"] = "true"
os.environ["AGENT_RULES_LOG_LEVEL"] = "INFO"

# Add repo root to path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

def test_direct_imports():
    """Test importing the rule system directly."""
    print("Testing direct imports...")
    try:
        from src.bootstrap.agent_rules_bootstrapper import AgentRulesBootstrapper
        from src.repository.agent_rule_repository import AgentRuleRepository
        print("✓ Direct imports successful")
        
        # Test bootstrapper creation
        bootstrapper = AgentRulesBootstrapper.from_environment()
        print("✓ Bootstrapper created from environment")
        
        # Test repository bootstrap
        repository = bootstrapper.bootstrap()
        print("✓ Repository bootstrapped")
        
        # Test repository queries
        stats = repository.get_repository_stats()
        print(f"✓ Repository stats: {stats['total_rules']} rules loaded")
        
        # Test getting all rules
        rules = repository.get_all_rules()
        print(f"✓ Retrieved {len(rules)} rules")
        
        # Test getting rule content if rules exist
        if rules:
            first_rule = rules[0]
            content = first_rule.load_content()
            print(f"✓ Content loaded for rule '{first_rule.rule_id}' (length: {len(content)})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_integration():
    """Test the MCP integration layer."""
    print("\nTesting MCP integration layer...")
    try:
        # Add MCP server path
        mcp_path = repo_root / 'mcp-server' / 'src'
        sys.path.insert(0, str(mcp_path))
        
        from bootstrap_integration import rule_system
        print("✓ MCP integration import successful")
        
        # Test initialization
        rule_system.initialize()
        print("✓ Rule system initialized")
        
        # Test metadata retrieval
        metadata = rule_system.get_all_rules_metadata()
        print(f"✓ Retrieved metadata for {len(metadata)} rules")
        
        # Test content retrieval if rules exist
        if metadata:
            first_rule_id = metadata[0]['ruleId']
            content = rule_system.get_rule_content_by_id(first_rule_id)
            print(f"✓ Content retrieved for rule '{first_rule_id}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("MCP Server Integration Test")
    print("=" * 40)
    
    success1 = test_direct_imports()
    success2 = test_mcp_integration()
    
    if success1 and success2:
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
