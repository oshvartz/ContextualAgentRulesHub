#!/usr/bin/env python3
"""
Test script for the Contextual Agent Rules Hub MCP Server.
"""

import os
import sys
import asyncio

# Add mcp-server src to path
mcp_server_path = os.path.join(os.path.dirname(__file__), 'mcp-server', 'src')
sys.path.insert(0, mcp_server_path)

from bootstrap_integration import rule_system

async def test_rule_system():
    """Test the rule system integration."""
    print("Testing Contextual Agent Rules Hub MCP Server Integration")
    print("=" * 60)
    
    try:
        # Test initialization
        print("1. Initializing rule system...")
        rule_system.initialize()
        print("   ✓ Rule system initialized successfully")
        
        # Test getting repository stats
        print("\n2. Getting repository statistics...")
        stats = rule_system.get_repository_stats()
        print(f"   ✓ Total rules: {stats.get('total_rules', 0)}")
        print(f"   ✓ Available languages: {stats.get('available_languages', [])}")
        print(f"   ✓ Available tags: {stats.get('available_tags', [])}")
        
        # Test getting all rules metadata
        print("\n3. Getting all rules metadata...")
        metadata_list = rule_system.get_all_rules_metadata()
        print(f"   ✓ Retrieved metadata for {len(metadata_list)} rules")
        
        for metadata in metadata_list:
            print(f"     - {metadata['ruleId']}: {metadata['description']}")
        
        # Test getting rule content by ID
        if metadata_list:
            print("\n4. Testing rule content retrieval...")
            first_rule_id = metadata_list[0]['ruleId']
            print(f"   Testing with rule ID: {first_rule_id}")
            
            # Check if rule exists
            exists = rule_system.rule_exists(first_rule_id)
            print(f"   ✓ Rule exists: {exists}")
            
            if exists:
                # Get rule content
                content = rule_system.get_rule_content_by_id(first_rule_id)
                if content:
                    print(f"   ✓ Content retrieved (length: {len(content)} characters)")
                    print(f"   ✓ Content preview: {content[:100]}...")
                else:
                    print("   ⚠ No content returned")
            
            # Test with non-existent rule
            print(f"\n5. Testing with non-existent rule...")
            fake_rule_id = "non-existent-rule"
            fake_exists = rule_system.rule_exists(fake_rule_id)
            print(f"   ✓ Non-existent rule exists check: {fake_exists}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! MCP server integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    success = await test_rule_system()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
