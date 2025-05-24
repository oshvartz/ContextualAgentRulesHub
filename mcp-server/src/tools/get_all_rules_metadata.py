"""
GetAllRulesMetadata tool implementation.
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from ..bootstrap_integration import rule_system

# Tool definition
GET_ALL_RULES_METADATA_TOOL = Tool(
    name="GetAllRulesMetadata",
    description="Gets the metadata for all rules in the index.",
    inputSchema={
        "type": "object",
        "properties": {},
        "title": "GetAllRulesMetadata",
        "description": "Gets the metadata for all rules in the index."
    }
)

async def handle_get_all_rules_metadata(arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle the GetAllRulesMetadata tool call.
    
    Args:
        arguments: Tool arguments (empty for this tool)
        
    Returns:
        List of TextContent with rules metadata
        
    Raises:
        Exception: If there's an error retrieving metadata
    """
    try:
        # Get all rules metadata from the rule system
        metadata_list = rule_system.get_all_rules_metadata()
        
        # Return as JSON string
        import json
        result = json.dumps(metadata_list, indent=2)
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        # Return error information
        error_msg = f"Error retrieving rules metadata: {str(e)}"
        return [TextContent(type="text", text=error_msg)]
