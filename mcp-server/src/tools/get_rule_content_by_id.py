"""
GetRuleContentById tool implementation.
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from ..bootstrap_integration import rule_system

# Tool definition
GET_RULE_CONTENT_BY_ID_TOOL = Tool(
    name="GetRuleContentById",
    description="Gets the content of a specific rule by its ID.",
    inputSchema={
        "type": "object",
        "properties": {
            "ruleId": {
                "type": "string",
                "description": "The unique identifier of the rule"
            }
        },
        "title": "GetRuleContentById",
        "description": "Gets the content of a specific rule by its ID.",
        "required": ["ruleId"]
    }
)

async def handle_get_rule_content_by_id(arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle the GetRuleContentById tool call.
    
    Args:
        arguments: Tool arguments containing ruleId
        
    Returns:
        List of TextContent with rule content
        
    Raises:
        Exception: If there's an error retrieving content
    """
    try:
        # Validate arguments
        if "ruleId" not in arguments:
            error_msg = "Missing required parameter: ruleId"
            return [TextContent(type="text", text=error_msg)]
        
        rule_id = arguments["ruleId"]
        
        if not isinstance(rule_id, str) or not rule_id.strip():
            error_msg = "ruleId must be a non-empty string"
            return [TextContent(type="text", text=error_msg)]
        
        # Check if rule exists
        if not rule_system.rule_exists(rule_id):
            error_msg = f"Rule with ID '{rule_id}' not found"
            return [TextContent(type="text", text=error_msg)]
        
        # Get rule content
        content = rule_system.get_rule_content_by_id(rule_id)
        
        if content is None:
            error_msg = f"No content available for rule '{rule_id}'"
            return [TextContent(type="text", text=error_msg)]
        
        return [TextContent(type="text", text=content)]
        
    except Exception as e:
        # Return error information
        error_msg = f"Error retrieving rule content: {str(e)}"
        return [TextContent(type="text", text=error_msg)]
