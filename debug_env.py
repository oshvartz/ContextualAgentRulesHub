"""
Debug script to test environment variable handling.
"""

import os
import re

def test_env_vars():
    """Test setting and reading environment variables with colons."""
    print("Testing environment variable handling...")
    
    # Test setting variables with colons
    test_vars = [
        ("RulesLoaderOptions:0:SourceType", "YamlFile"),
        ("RulesLoaderOptions:0:Path", "./rules"),
        ("AGENT_RULES_VALIDATION", "true")
    ]
    
    print("\nSetting test variables:")
    for key, value in test_vars:
        os.environ[key] = value
        print(f"  Set: {key} = {value}")
    
    print("\nReading back variables:")
    for key, expected_value in test_vars:
        actual_value = os.environ.get(key)
        print(f"  {key} = {actual_value} (expected: {expected_value})")
        if actual_value != expected_value:
            print(f"    ERROR: Mismatch!")
    
    print("\nAll environment variables containing 'RulesLoader':")
    for key in os.environ.keys():
        if "RulesLoader" in key:
            print(f"  {key} = {os.environ[key]}")
    
    print("\nAll environment variables starting with 'RulesLoaderOptions':")
    for key in os.environ.keys():
        if key.startswith("RulesLoaderOptions"):
            print(f"  {key} = {os.environ[key]}")
    
    print("\nRegex pattern test:")
    pattern = re.compile(r'^RulesLoaderOptions:(\d+):')
    count = 0
    for key in os.environ.keys():
        match = pattern.match(key)
        if match:
            print(f"  Found match: {key} -> index {match.group(1)}")
            count += 1
    print(f"  Total matches: {count}")

if __name__ == "__main__":
    test_env_vars()
