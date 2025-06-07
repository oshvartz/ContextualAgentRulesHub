#!/usr/bin/env python3
"""
Contextual Agent Rules Hub MCP Server

A Model Context Protocol server that exposes the Agent Rules repository
with tools for accessing rule metadata and content.
"""

import logging
import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from bootstrap_integration import rule_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("cotextual-agent-rules-hub")

@mcp.tool()
async def GetAllRulesMetadata(contextFilter: Optional[str] = None) -> str:
    """Get metadata for all non-core rules in the index. Optionally filter by context. Core rules are excluded."""
    try:
        # Initialize rule system if needed
        rule_system.initialize()
        
        # Get all rules metadata with optional context filter
        metadata_list = rule_system.get_all_rules_metadata(context_filter=contextFilter)
        
        # Return as JSON string
        return json.dumps(metadata_list, indent=2)
        
    except Exception as e:
        logger.error(f"Error in GetAllRulesMetadata: {e}")
        return f"Error retrieving rules metadata: {str(e)}"

@mcp.tool()
async def GetRuleContentById(ruleId: str) -> str:
    """Get the content of a specific rule by its ID."""
    try:
        # Validate arguments
        if not ruleId or not ruleId.strip():
            return "ruleId must be a non-empty string"
        
        # Initialize rule system if needed
        rule_system.initialize()
        
        # Check if rule exists
        if not rule_system.rule_exists(ruleId):
            return f"Rule with ID '{ruleId}' not found"
        
        # Get rule content
        content = rule_system.get_rule_content_by_id(ruleId)
        
        if content is None:
            return f"No content available for rule '{ruleId}'"
        
        return content
        
    except Exception as e:
        logger.error(f"Error in GetRuleContentById: {e}")
        return f"Error retrieving rule content: {str(e)}"

@mcp.tool()
async def GetAllContexts() -> str:
    """Get all available contexts. Returns empty list if no contexts exist."""
    try:
        # Initialize rule system if needed
        rule_system.initialize()
        
        # Get all available contexts
        contexts = rule_system.get_available_contexts()
        
        # Return as JSON string
        return json.dumps(contexts, indent=2)
        
    except Exception as e:
        logger.error(f"Error in GetAllContexts: {e}")
        return f"Error retrieving contexts: {str(e)}"

@mcp.tool()
async def GetCoreRulesContent() -> str:
    """Get content for all core rules in the index. Returns a list of strings."""
    try:
        rule_system.initialize()
        content_list = rule_system.get_core_rules_content()
        return json.dumps(content_list, indent=2) # Return as a JSON array of strings
    except Exception as e:
        logger.error(f"Error in GetCoreRulesContent: {e}")
        return f"Error retrieving core rules content: {str(e)}"

# Initialize rule system when module is loaded
try:
    logger.info("Initializing Contextual Agent Rules Hub MCP Server")
    rule_system.initialize()
    stats = rule_system.get_repository_stats()
    logger.info(f"Rule system initialized: {stats.get('total_rules', 0)} rules loaded")
except Exception as e:
    logger.error(f"Failed to initialize rule system: {e}")
    # Continue anyway - tools will handle initialization
