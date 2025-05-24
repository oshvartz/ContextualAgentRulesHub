"""
Demo script for Agent Rules Bootstrapper.

This script demonstrates how to use the Agent Rules Bootstrapper to load rules
from multiple sources using environment variable configuration.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.bootstrap.agent_rules_bootstrapper import AgentRulesBootstrapper
from src.config.environment_parser import EnvironmentConfigurationParser

def setup_demo_environment():
    """Setup environment variables for demo."""
    print("Setting up demo environment variables...")
    
    # Configure two YAML sources
    os.environ["RulesLoaderOptions:0:SourceType"] = "YamlFile"
    os.environ["RulesLoaderOptions:0:Path"] = "./rules"
    
    # Optional: Add a second source (uncomment if you have another rules directory)
    # os.environ["RulesLoaderOptions:1:SourceType"] = "YamlFile"
    # os.environ["RulesLoaderOptions:1:Path"] = "C:/git/some-other-rules"
    
    # Global configuration
    os.environ["AGENT_RULES_VALIDATION"] = "true"
    os.environ["AGENT_RULES_LOG_LEVEL"] = "INFO"
    
    print("Environment variables set:")
    for key, value in os.environ.items():
        if key.startswith("RulesLoaderOptions") or key.startswith("AGENT_RULES"):
            print(f"  {key} = {value}")
    
    # Debug: Print all environment variables that match the pattern
    print("\nDebug - All environment variables containing 'RulesLoader':")
    for key in os.environ.keys():
        if "RulesLoader" in key:
            print(f"  {key} = {os.environ[key]}")
    print()

def validate_environment():
    """Validate environment configuration."""
    print("Validating environment configuration...")
    
    parser = EnvironmentConfigurationParser()
    validation = parser.validate_environment()
    
    if validation["valid"]:
        print("✓ Environment configuration is valid")
        print(f"  Found {validation['sources_found']} source(s): {validation['indices']}")
    else:
        print("✗ Environment configuration has errors:")
        for error in validation["errors"]:
            print(f"    {error}")
        for warning in validation["warnings"]:
            print(f"    WARNING: {warning}")
    print()
    
    return validation["valid"]

def demo_bootstrapper():
    """Demonstrate the bootstrapper functionality."""
    print("Creating Agent Rules Bootstrapper...")
    
    try:
        # Create bootstrapper from environment
        bootstrapper = AgentRulesBootstrapper.from_environment()
        
        # Print configuration
        bootstrapper.print_configuration()
        
        # Validate sources before loading
        print("Validating sources...")
        validation = bootstrapper.validate_sources()
        if not validation["valid"]:
            print("Source validation failed:")
            for error in validation["errors"]:
                print(f"  {error}")
            return None
        print("✓ All sources validated successfully\n")
        
        # Bootstrap the repository
        print("Bootstrapping repository...")
        repository = bootstrapper.bootstrap()
        
        # Print results
        bootstrapper.print_results()
        
        # Show repository contents
        print("Repository contents:")
        stats = repository.get_repository_stats()
        print(f"  Total rules: {stats['total_rules']}")
        print(f"  Languages: {stats['available_languages']}")
        print(f"  Tags: {stats['available_tags']}")
        print()
        
        # Show some example queries
        demo_repository_queries(repository)
        
        return repository
        
    except Exception as e:
        print(f"Error creating bootstrapper: {e}")
        return None

def demo_repository_queries(repository):
    """Demonstrate repository query capabilities."""
    print("Demonstrating repository queries:")
    
    # Get all rules
    all_rules = repository.get_all_rules()
    print(f"  All rules: {len(all_rules)} rules")
    
    # Query by language
    csharp_rules = repository.get_rules_by_language("csharp")
    print(f"  C# rules: {len(csharp_rules)} rules")
    
    # Query by tag
    standards_rules = repository.get_rules_by_tag("coding-standards")
    print(f"  Coding standards rules: {len(standards_rules)} rules")
    
    # Show first rule details if available
    if all_rules:
        first_rule = all_rules[0]
        print(f"\nExample rule: {first_rule.rule_id}")
        print(f"  Description: {first_rule.description}")
        print(f"  Language: {first_rule.language}")
        print(f"  Tags: {first_rule.tags}")
        
        # Load content
        try:
            content = first_rule.load_content()
            content_preview = content[:200] + "..." if len(content) > 200 else content
            print(f"  Content preview: {content_preview}")
        except Exception as e:
            print(f"  Content load error: {e}")
    
    print()

def demo_parser_utilities():
    """Demonstrate parser utility functions."""
    print("Parser utility functions:")
    
    parser = EnvironmentConfigurationParser()
    
    # Show supported types
    supported_types = parser.get_supported_source_types()
    print(f"  Supported source types: {supported_types}")
    
    # Show example configuration
    print("\n  Example configuration:")
    parser.print_environment_example()

def main():
    """Main demo function."""
    print("Agent Rules Bootstrapper Demo")
    print("=" * 40)
    print()
    
    # Setup demo environment
    setup_demo_environment()
    
    # Validate environment
    if not validate_environment():
        print("Cannot continue with invalid environment")
        return
    
    # Show parser utilities
    demo_parser_utilities()
    print()
    
    # Demo the bootstrapper
    repository = demo_bootstrapper()
    
    if repository:
        print("Demo completed successfully!")
        print(f"Repository initialized with {len(repository)} rules")
    else:
        print("Demo failed - see errors above")

if __name__ == "__main__":
    main()
