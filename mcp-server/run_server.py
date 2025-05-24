#!/usr/bin/env python3
"""
Startup script for Contextual Agent Rules Hub MCP Server.
"""

import os
import sys
from pathlib import Path

# Set up environment variables for the rule system (only if not already set)
current_dir = Path(__file__).parent
repo_root = current_dir.parent
rules_path = repo_root / "rules"

# Only set environment variables if they're not already configured
# This allows MCP configuration to override these defaults
if "RulesLoaderOptions:0:SourceType" not in os.environ:
    os.environ["RulesLoaderOptions:0:SourceType"] = "YamlFile"
if "RulesLoaderOptions:0:Path" not in os.environ:
    os.environ["RulesLoaderOptions:0:Path"] = str(rules_path)
if "AGENT_RULES_VALIDATION" not in os.environ:
    os.environ["AGENT_RULES_VALIDATION"] = "true"
if "AGENT_RULES_LOG_LEVEL" not in os.environ:
    os.environ["AGENT_RULES_LOG_LEVEL"] = "INFO"

# Add repo root to path so we can import the src modules
sys.path.insert(0, str(repo_root))

# Add mcp-server src to path
sys.path.insert(0, str(current_dir / "src"))

# Import and run the server - direct import to avoid asyncio conflict
from main import mcp

if __name__ == "__main__":
    # Use FastMCP's built-in sync run method
    mcp.run()
