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
- `Rule` entity with metadata (ID, description, language, tags)
- `Source` entity for storage source information
- Clean separation between data and storage concerns

### Query Builder Pattern
- Flexible rule retrieval based on:
  - Programming language filtering
  - Tag-based categorization
  - Combined criteria queries

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
├── {rule-id}.yaml          # Rule content files
├── index.yaml              # Rule metadata index
└── sources/
    └── file-source.yaml    # Source configuration
```

## Extensibility Points
- Source abstraction allows for new storage backends
- Tag system enables flexible categorization
- Language specification supports multi-language rules
- MCP protocol interface allows for various client integrations
