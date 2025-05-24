# ContextualAgentRulesHub

A Python-based data model system for managing and retrieving agent rules from multiple sources with support for language-specific filtering and tag-based categorization.

## Overview

ContextualAgentRulesHub provides a flexible system for storing and retrieving agent rules that can be used by AI agents to follow context-specific guidelines. The system supports multiple source types and provides efficient querying capabilities.

## Features

- **Multi-Source Support**: Extensible architecture supporting File, Database, Git Repository, and API sources
- **YAML-Based Storage**: Human-readable rule storage with metadata and content separation
- **Efficient Indexing**: Fast lookups by language, tags, and content search
- **Lazy Loading**: Rule content is loaded only when needed for optimal performance
- **Flexible Querying**: Support for complex queries combining language, tags, and text search
- **Tag-Based Organization**: Flexible categorization system with AND/OR logic support

## Project Structure

```
ContextualAgentRulesHub/
├── src/                          # Core implementation
│   ├── models/                   # Data models
│   │   ├── rule.py              # Rule entity model
│   │   ├── source.py            # Source configuration model
│   │   └── rule_index.py        # Rule indexing system
│   ├── sources/                  # Source implementations
│   │   ├── base.py              # Abstract source interface
│   │   └── file_source.py       # YAML file source implementation
│   └── repository/               # Repository layer
│       └── rule_repository.py   # Main repository class
├── rules/                        # Example rule storage
│   ├── index.yaml               # Rule metadata index
│   ├── python-pep8-standards.yaml
│   ├── python-testing-guide.yaml
│   └── git-workflow-guide.yaml
├── requirements.txt              # Python dependencies
├── simple_demo.py               # Demonstration script
└── README.md                    # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ContextualAgentRulesHub
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Running the Demo

```bash
python simple_demo.py
```

This will demonstrate:
- Loading rules from YAML files
- Filtering by language and tags
- Content retrieval
- Metadata indexing

### Basic Usage

```python
from src.models.source import create_file_source
from src.sources.file_source import FileSource
from src.repository.rule_repository import RuleRepository

# Create a file source
source_config = create_file_source(
    directory_path="rules",
    index_file="index.yaml",
    content_format="yaml"
)

# Initialize the source and repository
file_source = FileSource(source_config)
repository = RuleRepository([file_source])

# Discover and index rules
repository.discover_rules()

# Query rules
python_rules = repository.get_rules_by_language("python")
testing_rules = repository.get_rules_by_tag("testing")
best_practices = repository.get_rules_by_tags_any(["best-practices", "standards"])

# Get rule content
content = repository.get_rule_content("python-pep8-standards")
```

## Rule Format

### Index File (`rules/index.yaml`)

```yaml
rules:
  - id: python-pep8-standards
    description: "Python PEP8 coding standards and formatting guidelines"
    language: python
    tags: [coding-standards, pep8, formatting, best-practices]
    content_file: python-pep8-standards.yaml
```

### Rule Content File (`rules/python-pep8-standards.yaml`)

```yaml
id: python-pep8-standards
description: "Python PEP8 coding standards and formatting guidelines"
language: python
tags:
  - coding-standards
  - pep8
  - formatting
  - best-practices
rule: |
  # Python PEP8 Standards Guide
  
  ## Indentation
  - Use 4 spaces per indentation level
  - Never mix tabs and spaces
  
  ## Line Length
  - Limit all lines to a maximum of 79 characters
  
  [... detailed rule content ...]
```

## Core Components

### Data Models

- **Rule**: Contains metadata (ID, description, language, tags) and content
- **Source**: Defines storage configuration for different source types
- **RuleIndex**: Provides efficient indexing and querying capabilities

### Source Types

- **FileSource**: Reads rules from YAML files with index-based metadata
- **DatabaseSource**: (Future) Database-backed rule storage
- **GitSource**: (Future) Git repository-based rule storage
- **APISource**: (Future) API-based rule retrieval

### Repository Features

- **Multi-source aggregation**: Combine rules from multiple sources
- **Lazy loading**: Content loaded only when requested
- **Efficient querying**: Index-based lookups for fast performance
- **Flexible filtering**: Language, tags, and text-based search

## API Reference

### RuleRepository

#### Query Methods
- `get_all_rules()` - Get all rules
- `get_rules_by_language(language)` - Filter by programming language
- `get_rules_by_tag(tag)` - Filter by single tag
- `get_rules_by_tags_any(tags)` - Filter by any of multiple tags (OR logic)
- `get_rules_by_tags_all(tags)` - Filter by all tags (AND logic)
- `search_rules(query)` - Text search in descriptions
- `get_rules_by_criteria()` - Complex multi-criteria queries

#### Content Methods
- `get_rule(rule_id)` - Get rule metadata
- `get_rule_content(rule_id)` - Get rule content with lazy loading

#### Management Methods
- `discover_rules()` - Scan and index all rules from sources
- `add_source(source)` - Add new rule source
- `refresh()` - Reload all rules from sources
- `get_repository_stats()` - Get statistics about the repository

## Extending the System

### Adding New Source Types

1. **Implement the RuleSource interface**:
   ```python
   from src.sources.base import RuleSource
   
   class CustomSource(RuleSource):
       def load_rules_metadata(self) -> List[Rule]:
           # Implementation
           pass
       
       def load_rule_content(self, rule_id: str) -> str:
           # Implementation
           pass
       
       def validate_source(self) -> bool:
           # Implementation
           pass
   ```

2. **Register with the repository**:
   ```python
   custom_source = CustomSource(config)
   repository.add_source(custom_source)
   ```

### Adding New Rule Types

Simply add new YAML files following the established format:

1. Add metadata to `rules/index.yaml`
2. Create content file `rules/your-rule-id.yaml`
3. Use appropriate language and tags for categorization

## Example Rules Included

1. **python-pep8-standards**: Python coding standards and formatting
2. **python-testing-guide**: Python testing best practices with pytest
3. **git-workflow-guide**: Git workflow and branching strategies

## Requirements

- Python 3.8+
- PyYAML 6.0+

## Phase 1 Implementation Status

✅ **Completed Features:**
- Core data models (Rule, Source, RuleIndex)
- File source implementation with YAML support
- Rule repository with multi-source support
- Efficient indexing and querying system
- Example rules and demonstration script
- Comprehensive documentation

🔄 **Future Phases:**
- Database source implementation
- Git repository source implementation
- API source implementation
- MCP server integration
- Advanced validation and error handling
- Performance optimization
- Testing framework

## Contributing

1. Follow Python PEP8 standards (see included rule for details)
2. Add tests for new functionality
3. Update documentation for API changes
4. Use descriptive commit messages

## License

[License information to be added]
