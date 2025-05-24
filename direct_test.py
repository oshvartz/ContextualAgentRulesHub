"""
Direct test of environment variable access.
"""

import os

def direct_test():
    """Direct test of environment variable access."""
    print("Direct environment variable test...")
    
    # Set variables
    os.environ["RulesLoaderOptions:0:SourceType"] = "YamlFile"
    os.environ["RulesLoaderOptions:0:Path"] = "./rules"
    
    # Direct access
    print(f"Direct access test:")
    print(f"  os.environ['RulesLoaderOptions:0:SourceType'] = {os.environ.get('RulesLoaderOptions:0:SourceType', 'NOT_FOUND')}")
    print(f"  os.environ['RulesLoaderOptions:0:Path'] = {os.environ.get('RulesLoaderOptions:0:Path', 'NOT_FOUND')}")
    
    # Check if keys exist in environ
    target_key1 = "RulesLoaderOptions:0:SourceType"
    target_key2 = "RulesLoaderOptions:0:Path"
    
    print(f"\nKey existence test:")
    print(f"  '{target_key1}' in os.environ = {target_key1 in os.environ}")
    print(f"  '{target_key2}' in os.environ = {target_key2 in os.environ}")
    
    # Check keys() method
    print(f"\nKeys iteration test:")
    all_keys = list(os.environ.keys())
    print(f"  Total environment variables: {len(all_keys)}")
    
    found_rules_keys = []
    for key in all_keys:
        if "RulesLoader" in key:
            found_rules_keys.append(key)
    
    print(f"  Keys containing 'RulesLoader': {found_rules_keys}")
    
    # Alternative approach: check for the exact keys
    if target_key1 in all_keys:
        print(f"  Found {target_key1} in keys list")
    else:
        print(f"  {target_key1} NOT found in keys list")
    
    # Test with different approach - using items()
    print(f"\nUsing items() approach:")
    for key, value in os.environ.items():
        if "RulesLoader" in key:
            print(f"  Found: {key} = {value}")

if __name__ == "__main__":
    direct_test()
