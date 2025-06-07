# System Patterns: ContextualAgentRulesHub

## Architecture Overview
```
MCP Server (Python)
├── Rule Management System
│   ├── Rule Entity Models
│   ├── Source Abstraction Layer
│   └── Query/Retrieval Engine
├── File Source Implementation
│   ├── YAML File Reader
│   ├── Metadata Parser
│   └── Content Loader
└── MCP Protocol Interface
    ├── Tool Definitions
    ├── Resource Handlers
    └── Request/Response Processing
```

## Key Design Patterns

### Repository Pattern
- `RuleRepository` interface for rule storage abstraction
- `FileSource` implementation for YAML-based storage
- Extensible for future source types (database, API, etc.)

### Entity Model Pattern
- `AgentRule` entity with metadata (ID, description, language, tags, context, **is_core**)
- `RuleContentSource` for on-demand content loading.
- Clean separation between data and storage concerns

### Query Builder Pattern
- Flexible rule retrieval based on:
  - Programming language filtering
  - Tag-based categorization
  - Combined criteria queries
  - **is_core** filtering

## Component Relationships

### Core Entities
- **Rule**: Contains metadata and references to content source
- **Source**: Defines storage mechanism and location
- **RuleIndex**: Manages rule discovery and metadata

### Critical Implementation Paths
1. **Rule Discovery**: Scan file system → Parse metadata → Build index
2. **Rule Retrieval**: Query criteria → Filter rules → Load content
3. **MCP Integration**: Request handling → Rule lookup → Response formatting

## File Organization Patterns
```
rules/
├── {rule-id}.yaml          # Rule content files with optional 'is_core: true/false' (also supports 'coreRule' for backward compatibility)
# index.yaml is no longer the primary source of truth for metadata, 
# metadata is embedded in each rule file or loaded by AgentRulesBootstrapper.
└── sources/ # This structure is managed by AgentRulesBootstrapper via environment variables
    # Example: RulesLoaderOptions:0:SourceType=YamlFile
    #          RulesLoaderOptions:0:Path=c:/git/ContextualAgentRulesHub/rules
```

## MCP Tool Summary
- **GetAllRulesMetadata**: Get metadata for all non-core rules.
- **GetRuleContentById**: Get content of a specific rule by ID.
- **GetAllContexts**: Get all available contexts.
- **GetCoreRulesContent**: Get content for all core rules.

## Extensibility Points
- Source abstraction allows for new storage backends
- Tag system enables flexible categorization
- Language specification supports multi-language rules
- MCP protocol interface allows for various client integrations
