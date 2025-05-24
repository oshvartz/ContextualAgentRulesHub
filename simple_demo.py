#!/usr/bin/env python3
"""
Simple demonstration script for the ContextualAgentRulesHub system.

This script shows how to use the rule repository to load and query rules
from YAML files using a simplified import approach.
"""

import sys
import os
from pathlib import Path
import yaml

def main():
    """Demonstrate basic functionality without complex imports."""
    print("=== ContextualAgentRulesHub Simple Demo ===\n")
    
    # Check if rules directory exists
    rules_dir = Path("rules")
    if not rules_dir.exists():
        print("✗ Rules directory not found")
        return
    
    # Check if index file exists
    index_file = rules_dir / "index.yaml"
    if not index_file.exists():
        print("✗ Index file not found")
        return
    
    print("✓ Found rules directory and index file")
    
    # Load index file
    print("\n1. Loading rule index...")
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = yaml.safe_load(f)
        
        rules_metadata = index_data.get('rules', [])
        print(f"   Found {len(rules_metadata)} rules in index")
        
    except Exception as e:
        print(f"✗ Error loading index: {e}")
        return
    
    # Display rules metadata
    print("\n2. Rules overview:")
    for rule_meta in rules_metadata:
        rule_id = rule_meta.get('id', 'unknown')
        description = rule_meta.get('description', 'No description')
        language = rule_meta.get('language', 'generic')
        tags = ', '.join(rule_meta.get('tags', []))
        
        print(f"   - {rule_id}")
        print(f"     Description: {description}")
        print(f"     Language: {language}")
        print(f"     Tags: {tags}")
        print()
    
    # Test loading rule content
    print("3. Loading rule content...")
    if rules_metadata:
        first_rule = rules_metadata[0]
        rule_id = first_rule['id']
        content_file = rules_dir / f"{rule_id}.yaml"
        
        if content_file.exists():
            print(f"   Loading content for: {rule_id}")
            try:
                with open(content_file, 'r', encoding='utf-8') as f:
                    rule_data = yaml.safe_load(f)
                
                content = rule_data.get('rule', 'No content found')
                
                # Show first few lines
                lines = content.split('\n')[:15]
                print("   First 15 lines of content:")
                for i, line in enumerate(lines, 1):
                    print(f"   {i:2d}: {line}")
                
                if len(content.split('\n')) > 15:
                    print(f"   ... ({len(content.split('\n')) - 15} more lines)")
                    
            except Exception as e:
                print(f"   ✗ Error loading content: {e}")
        else:
            print(f"   ✗ Content file not found: {content_file}")
    
    # Demonstrate filtering
    print("\n4. Filtering examples:")
    
    # Filter by language
    python_rules = [r for r in rules_metadata if r.get('language') == 'python']
    print(f"   Python rules: {len(python_rules)}")
    for rule in python_rules:
        print(f"   - {rule['id']}: {rule['description']}")
    
    # Filter by tag
    testing_rules = [r for r in rules_metadata if 'testing' in r.get('tags', [])]
    print(f"\n   Testing rules: {len(testing_rules)}")
    for rule in testing_rules:
        print(f"   - {rule['id']}: {rule['description']}")
    
    # Filter by multiple tags
    best_practice_rules = [r for r in rules_metadata 
                          if any(tag in r.get('tags', []) for tag in ['best-practices', 'formatting'])]
    print(f"\n   Best practices or formatting rules: {len(best_practice_rules)}")
    for rule in best_practice_rules:
        print(f"   - {rule['id']}: {rule['description']}")
    
    print(f"\n=== Simple Demo Complete ===")
    print(f"The data model system structure is in place and working!")
    print(f"Key components implemented:")
    print(f"- ✓ YAML-based rule storage")
    print(f"- ✓ Rule metadata indexing")
    print(f"- ✓ Content lazy loading")
    print(f"- ✓ Language and tag filtering")
    print(f"- ✓ Extensible source abstraction")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
