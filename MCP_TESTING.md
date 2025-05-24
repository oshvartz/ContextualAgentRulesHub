# MCP Server Testing Guide

This guide explains how to test the Contextual Agent Rules Hub MCP Server using the official MCP Inspector tool.

## Overview

The MCP Inspector (`@modelcontextprotocol/inspector`) is the official testing tool for Model Context Protocol servers. It provides a web-based interface to:

- View available tools and their schemas
- Test tool invocations interactively
- Inspect server responses and error handling
- Validate MCP protocol compliance

## Prerequisites

Before running the tests, ensure you have:

1. **Node.js** (v16 or higher) - For running the MCP Inspector
2. **Python** (v3.8 or higher) - For running the MCP server
3. **Python dependencies** - Install with `pip install -r mcp-server/requirements.txt`

## Available Test Scripts

### 1. PowerShell Script (Recommended)
```powershell
.\test-mcp-inspector.ps1
```

**Features:**
- Comprehensive prerequisite checking
- Server validation before testing
- Colored output for better readability
- Configurable port and server script path
- Detailed error handling

**Usage Examples:**
```powershell
# Default usage (port 3000)
.\test-mcp-inspector.ps1

# Custom port
.\test-mcp-inspector.ps1 -Port 3001

# Custom server script path
.\test-mcp-inspector.ps1 -ServerScript "./custom/path/server.py"
```

### 2. Batch File (Simple)
```cmd
test-mcp-inspector.bat
```

**Features:**
- Simple prerequisite checking
- Quick start for basic testing
- Windows-compatible batch commands

## Available Tools to Test

The MCP server exposes the following tools:

### GetAllRulesMetadata
- **Description:** Get metadata for all rules in the index
- **Parameters:** None
- **Returns:** JSON array of rule metadata objects

**Example Response:**
```json
[
  {
    "ruleId": "code-review-standards",
    "description": "Code review guidelines and best practices",
    "language": null,
    "tags": ["code-review", "best-practices", "collaboration"],
    "source": {"sourceType": "File"}
  }
]
```

### GetRuleContentById
- **Description:** Get the content of a specific rule by its ID
- **Parameters:** 
  - `ruleId` (string, required): The ID of the rule to retrieve
- **Returns:** Rule content as text

**Example Usage:**
```json
{
  "ruleId": "python-testing-guide"
}
```

## Testing Workflow

1. **Start the Inspector:**
   Run one of the test scripts to launch the MCP Inspector

2. **Access the Web Interface:**
   Open your browser to `http://localhost:3000` (or your specified port)

3. **Explore Available Tools:**
   The interface will show all available tools with their schemas

4. **Test GetAllRulesMetadata:**
   - Click on the `GetAllRulesMetadata` tool
   - Click "Invoke" (no parameters needed)
   - Verify the response contains rule metadata

5. **Test GetRuleContentById:**
   - Click on the `GetRuleContentById` tool
   - Enter a rule ID from the metadata response (e.g., "code-review-standards")
   - Click "Invoke"
   - Verify the response contains the rule content

## Expected Test Results

### Successful GetAllRulesMetadata Response:
- Status: Success
- Response: JSON array with rule objects
- Each rule should have: `ruleId`, `description`, `language`, `tags`, `source`

### Successful GetRuleContentById Response:
- Status: Success
- Response: Text content of the specified rule
- Content should be formatted (markdown, YAML, etc.)

### Error Cases to Test:
1. **Invalid Rule ID:**
   - Input: Non-existent rule ID (e.g., "invalid-rule")
   - Expected: Error message "Rule with ID 'invalid-rule' not found"

2. **Empty Rule ID:**
   - Input: Empty string or whitespace
   - Expected: Error message "ruleId must be a non-empty string"

## Troubleshooting

### Common Issues:

**1. "Node.js not found"**
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation

**2. "Python not found"**
- Install Python from https://python.org/
- Ensure Python is in your PATH

**3. "MCP server script not found"**
- Verify you're running the script from the project root directory
- Check that `mcp-server/run_server.py` exists

**4. "Failed to start MCP Inspector"**
- Check if port 3000 is already in use
- Try a different port: `.\test-mcp-inspector.ps1 -Port 3001`

**5. "Module import errors"**
- Install Python dependencies: `pip install -r mcp-server/requirements.txt`
- Verify Python path configuration

### Debug Mode:
For detailed debugging, you can run the server directly:
```bash
python mcp-server/run_server.py
```

## Manual Testing

If you prefer manual testing without the scripts:

```bash
# Install the inspector globally (optional)
npm install -g @modelcontextprotocol/inspector

# Run the inspector
npx @modelcontextprotocol/inspector python mcp-server/run_server.py
```

## Integration Testing

The project also includes integration tests:
- `test_mcp_server.py` - Basic server functionality
- `test_mcp_integration.py` - Full integration tests
- `direct_test.py` - Direct API testing

Run with:
```bash
python test_mcp_server.py
python test_mcp_integration.py
```

## Continuous Testing

For development, you can:
1. Keep the inspector running in one terminal
2. Make changes to the server code
3. Restart the inspector to test changes
4. The web interface will automatically reconnect

## Security Notes

- The MCP Inspector runs locally and doesn't expose your server to the internet
- The server only exposes read-only access to rule data
- No sensitive information should be included in rule content for testing
