#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test script for Contextual Agent Rules Hub MCP Server using @modelcontextprotocol/inspector
    
.DESCRIPTION
    This script tests the MCP server using the official MCP inspector tool.
    It starts the server and launches the inspector interface for interactive testing.
    
.PARAMETER Port
    The port to run the inspector on (default: 3000)
    
.PARAMETER ServerScript
    Path to the MCP server script (default: ./mcp-server/run_server.py)
    
.EXAMPLE
    .\test-mcp-inspector.ps1
    
.EXAMPLE
    .\test-mcp-inspector.ps1 -Port 3001 -ServerScript "./mcp-server//run_server.py"
#>

param(
    [Parameter(Mandatory=$false)]
    [int]$Port = 3000,
    
    [Parameter(Mandatory=$false)]
    [string]$ServerScript = "./mcp-server//run_server.py"
)

# Script configuration
$ErrorActionPreference = "Stop"
$InformationPreference = "Continue"

# Colors for output
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Checking prerequisites..." $ColorInfo
    
    # Check if Node.js is available
    try {
        $nodeVersion = node --version
        Write-ColorOutput "✅ Node.js found: $nodeVersion" $ColorSuccess
    }
    catch {
        Write-ColorOutput "❌ Node.js not found. Please install Node.js first." $ColorError
        exit 1
    }
    
    # Check if npx is available
    try {
        $npxVersion = npx --version
        Write-ColorOutput "✅ npx found: $npxVersion" $ColorSuccess
    }
    catch {
        Write-ColorOutput "❌ npx not found. Please ensure Node.js is properly installed." $ColorError
        exit 1
    }
    
    # Check if Python is available
    try {
        $pythonVersion = python --version
        Write-ColorOutput "✅ Python found: $pythonVersion" $ColorSuccess
    }
    catch {
        Write-ColorOutput "❌ Python not found. Please install Python first." $ColorError
        exit 1
    }
    
    # Check if server script exists
    if (-not (Test-Path $ServerScript)) {
        Write-ColorOutput "❌ MCP server script not found at: $ServerScript" $ColorError
        exit 1
    }
    Write-ColorOutput "✅ MCP server script found: $ServerScript" $ColorSuccess
    
    Write-ColorOutput "✅ All prerequisites met!" $ColorSuccess
    Write-Host ""
}

function Install-MCPInspector {
    Write-ColorOutput "📦 Checking MCP Inspector..." $ColorInfo
    
    # Check if @modelcontextprotocol/inspector is available
    try {
        # Try to get help from the inspector to see if it's available
        $inspectorHelp = npx @modelcontextprotocol/inspector --help 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ MCP Inspector is available" $ColorSuccess
        } else {
            Write-ColorOutput "⚠️ MCP Inspector not found, will be installed automatically by npx" $ColorWarning
        }
    }
    catch {
        Write-ColorOutput "⚠️ MCP Inspector will be installed automatically by npx" $ColorWarning
    }
    Write-Host ""
}

function Test-MCPServer {
    Write-ColorOutput "🧪 Testing MCP Server availability..." $ColorInfo
    
    # Test if the server script can be imported/validated
    try {
        $testResult = python -c "
import sys
import os
from pathlib import Path

# Add paths like the run_server.py does
current_dir = Path('$($ServerScript)').parent
repo_root = current_dir.parent if current_dir.name == 'mcp-server' else current_dir
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(current_dir / 'src'))

try:
    # Set up environment like run_server.py
    os.environ['RulesLoaderOptions:0:SourceType'] = 'YamlFile'
    os.environ['RulesLoaderOptions:0:Path'] = str(repo_root / 'rules')
    os.environ['AGENT_RULES_VALIDATION'] = 'true'
    os.environ['AGENT_RULES_LOG_LEVEL'] = 'INFO'
    
    # Try to import the main module
    from main import mcp
    print('SUCCESS: MCP server module loaded successfully')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
"
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ MCP server module validated successfully" $ColorSuccess
        } else {
            Write-ColorOutput "❌ MCP server validation failed:" $ColorError
            Write-ColorOutput $testResult $ColorError
            exit 1
        }
    }
    catch {
        Write-ColorOutput "❌ Failed to validate MCP server: $_" $ColorError
        exit 1
    }
    Write-Host ""
}

function Start-MCPInspector {
    Write-ColorOutput "🚀 Starting MCP Inspector on port $Port..." $ColorInfo
    Write-ColorOutput "Server script: $ServerScript" $ColorInfo
    Write-Host ""
    
    Write-ColorOutput "🌐 Inspector will be available at: http://localhost:$Port" $ColorSuccess
    Write-ColorOutput "📋 The inspector will allow you to:" $ColorInfo
    Write-ColorOutput "   • View available tools and their schemas" $ColorInfo
    Write-ColorOutput "   • Test tool invocations interactively" $ColorInfo
    Write-ColorOutput "   • Inspect server responses and error handling" $ColorInfo
    Write-ColorOutput "   • Validate MCP protocol compliance" $ColorInfo
    Write-Host ""
    
    Write-ColorOutput "⚠️ Press Ctrl+C to stop the inspector" $ColorWarning
    Write-Host ""
    
    try {
        # Start the MCP inspector
        # The inspector expects the server command as arguments
        npx @modelcontextprotocol/inspector python "`"$ServerScript`"" --port $Port
    }
    catch {
        Write-ColorOutput "❌ Failed to start MCP Inspector: $_" $ColorError
        exit 1
    }
}

function Show-Usage {
    Write-ColorOutput "🔧 MCP Inspector Test Script" $ColorInfo
    Write-ColorOutput "This script will:" $ColorInfo
    Write-ColorOutput "1. Check prerequisites (Node.js, Python, MCP server)" $ColorInfo
    Write-ColorOutput "2. Validate the MCP server can be loaded" $ColorInfo
    Write-ColorOutput "3. Start the MCP Inspector web interface" $ColorInfo
    Write-Host ""
    Write-ColorOutput "Available tools to test:" $ColorInfo
    Write-ColorOutput "• GetAllRulesMetadata - Get metadata for all rules" $ColorInfo
    Write-ColorOutput "• GetRuleContentById - Get content of a specific rule" $ColorInfo
    Write-Host ""
}

# Main execution
try {
    Write-Host ""
    Write-ColorOutput "🧪 Contextual Agent Rules Hub - MCP Inspector Test" $ColorInfo
    Write-ColorOutput ("=" * 60) $ColorInfo
    Write-Host ""
    
    Show-Usage
    Test-Prerequisites
    Install-MCPInspector
    Test-MCPServer
    Start-MCPInspector
}
catch {
    Write-ColorOutput "❌ Script failed: $_" $ColorError
    exit 1
}
finally {
    Write-Host ""
    Write-ColorOutput "🏁 Test script completed" $ColorInfo
}
