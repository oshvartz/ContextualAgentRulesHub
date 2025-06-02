# Plan: Add `context` Parameter to AgentRule and MCP Server

This document outlines the plan to add an optional `context` string parameter to the `AgentRule` model. This will allow rules to be associated with a specific context (e.g., a project name like "GSA"). The MCP server's `GetAllRulesMetadata` tool will be updated to allow filtering by this context, with the following behavior:

- **No context filter**: Returns only rules without context (general rules)
- **With context filter**: Returns rules with no context OR rules matching the provided context

This ensures that general rules are always available, while context-specific rules are only returned when explicitly requested.

## 1. Modify `AgentRule` Dataclass

**File:** [`src/models/agent_rule.py`](src/models/agent_rule.py:10)

*   Add `context: Optional[str] = None` to the `@dataclass` definition.
*   Update the `__repr__` method to include the `context` field for better debugging/logging.

```python
from dataclasses import dataclass
from typing import List, Optional
from .rule_content_source import RuleContentSource

@dataclass
class AgentRule:
    # ... existing attributes ...
    context: Optional[str] = None # New attribute

    # ... existing methods ...

    def __repr__(self) -> str:
        return (f"AgentRule(rule_id='{self.rule_id}', description='{self.description}', "
                f"language='{self.language}', tags={self.tags}, context='{self.context}')") # Updated
```

## 2. Update `YamlRuleLoader`

**File:** [`src/loaders/yaml_loader.py`](src/loaders/yaml_loader.py:13)

*   In the `_load_rule_from_file()` method:
    *   After extracting `tags`, add logic to extract `context = data.get('context')`.
    *   Pass the extracted `context` to the `AgentRule` constructor.

```python
# In YamlRuleLoader._load_rule_from_file() method:
# ...
tags = data.get('tags', [])
if not isinstance(tags, list):
    raise ValueError(f"'tags' must be a list in {yaml_file}")

context = data.get('context') # Add this line

# Ensure 'rule' field exists (even if we don't load content now)
if 'rule' not in data:
    raise ValueError(f"Missing 'rule' field in {yaml_file}")

# Create content source
content_source = YamlFileContentSource(str(yaml_file))

# Create AgentRule
rule = AgentRule(
    rule_id=rule_id,
    description=description,
    language=language,
    tags=tags,
    content_source=content_source,
    context=context  # Add new parameter
)
# ...
```

## 3. Update `AgentRuleRepository`

**File:** [`src/repository/agent_rule_repository.py`](src/repository/agent_rule_repository.py:8)

*   Modify the `get_rules_by_criteria()` method:
    *   Add `context: Optional[str] = None` to its parameters.
    *   Update filtering logic to include rules where `rule.context is None` OR `rule.context` matches the provided `context` filter (case-insensitive).

```python
# In AgentRuleRepository.get_rules_by_criteria()
def get_rules_by_criteria(self,
                          language: Optional[str] = None,
                          tags: Optional[List[str]] = None,
                          tags_mode: str = "any",
                          description_query: Optional[str] = None,
                          context: Optional[str] = None) -> List[AgentRule]: # Added context
    rules = self.get_all_rules()

    # Filter by language
    if language:
        rules = [rule for rule in rules if rule.matches_language(language)]

    # Filter by tags
    if tags:
        if tags_mode.lower() == "all":
            rules = [rule for rule in rules if rule.has_all_tags(tags)]
        else:  # any
            rules = [rule for rule in rules if rule.has_any_tag(tags)]

    # Filter by description query
    if description_query:
        query_lower = description_query.lower()
        rules = [rule for rule in rules
                 if query_lower in rule.description.lower()]

    # Filter by context (NEW LOGIC)
    if context is not None:
        # If context filter is provided: include rules with no context OR matching context
        context_lower = context.lower()
        rules = [
            rule for rule in rules
            if rule.context is None or rule.context.lower() == context_lower
        ]
    else:
        # If no context filter is provided: return only rules without context
        rules = [rule for rule in rules if rule.context is None]

    return rules
```
*   **(Optional but Recommended)** Add `get_available_contexts(self) -> List[str]` and update `get_repository_stats()` to include context-related statistics.

## 4. Update `RuleSystemIntegration`

**File:** [`mcp-server/src/bootstrap_integration.py`](mcp-server/src/bootstrap_integration.py:20)

*   Modify the `get_all_rules_metadata()` method:
    *   Add an optional parameter `context_filter: Optional[str] = None`.
    *   If `context_filter` is provided, fetch rules using `self._repository.get_rules_by_criteria(context=context_filter)`. Otherwise, call `get_rules_by_criteria()` without the context argument (or pass `context=None`) to get all rules.
    *   Add `"context": rule.context` to the `metadata` dictionary created for each rule.

```python
# In RuleSystemIntegration class
def get_all_rules_metadata(self, context_filter: Optional[str] = None) -> List[Dict[str, Any]]: # Added context_filter
    if not self._initialized:
        self.initialize()

    if not self._repository:
        raise Exception("Repository not initialized")

    # Use get_rules_by_criteria, passing the context_filter
    # The repository's method now handles the "OR None" logic for context
    rules = self._repository.get_rules_by_criteria(context=context_filter)

    metadata_list = []
    for rule in rules:
        source_info = rule.get_content_source_info()
        metadata = {
            "ruleId": rule.rule_id,
            "description": rule.description,
            "language": rule.language,
            "tags": rule.tags,
            "context": rule.context, # Add this line
            "source": {
                "sourceType": source_info.get("type", "File") # Assuming 'type' key, adjust if needed
            }
        }
        metadata_list.append(metadata)
    return metadata_list
```

## 5. Update MCP Server Tools

**File:** [`mcp-server/src/main.py`](mcp-server/src/main.py:1)

*   Modify the `GetAllRulesMetadata` tool:
    *   Update its signature and input schema (as defined by `FastMCP`) to accept an optional `contextFilter: Optional[str]` parameter.
    *   Pass this `contextFilter` to `rule_system.get_all_rules_metadata(context_filter=contextFilter)`.

```python
# In mcp-server/src/main.py
@mcp.tool()
# The actual signature for FastMCP might involve type hints or a schema definition.
# This is a conceptual representation. Ensure the tool's input schema reflects
# an optional 'contextFilter' string argument.
async def GetAllRulesMetadata(contextFilter: Optional[str] = None) -> str: # Added contextFilter
    try:
        rule_system.initialize()
        # Pass the filter to the underlying system
        metadata_list = rule_system.get_all_rules_metadata(context_filter=contextFilter)
        return json.dumps(metadata_list, indent=2)
    except Exception as e:
        logger.error(f"Error in GetAllRulesMetadata: {e}")
        return f"Error retrieving rules metadata: {str(e)}"
```

## 6. Update Example YAML Rule Files

**Files:** e.g., in `rules/` directory.

*   For testing purposes, add the `context` key to one or more YAML files.
    Example:
    ```yaml
    id: code-review-standards
    description: "Code review guidelines and best practices"
    language: null
    context: general # New field
    tags:
      - code-review
      - best-practices
    rule: |
      # ... rule content ...
    ```
    Another example:
    ```yaml
    id: gsa-specific-rule
    description: "A rule specific to the GSA project"
    language: python
    context: GSA # New field
    tags:
      - gsa
      - python-gsa
    rule: |
      # ... rule content for GSA ...
    ```

## Mermaid Diagram of Changes

```mermaid
graph TD
    subgraph "Model Layer (Python Library)"
        A[AgentRule Class in src/models/agent_rule.py] -- Add context attribute & update repr --> A
    end

    subgraph "Data Loading Layer (Python Library)"
        B[YamlRuleLoader in src/loaders/yaml_loader.py] -- Read 'context' from YAML & pass to constructor --> B
        B -- Instantiates --> A
        C[YAML Rule Files in rules/] -- Add 'context' key --> C
    end

    subgraph "Repository Layer (Python Library)"
        D[AgentRuleRepository in src/repository/agent_rule_repository.py] -- Update get_rules_by_criteria() for context filtering (incl. None) --> D
    end

    subgraph "MCP Server Integration Layer (mcp-server/src)"
        E[RuleSystemIntegration in bootstrap_integration.py] -- Modify get_all_rules_metadata() to use updated repo filter & include context field --> E
        E -- Uses --> D
    end

    subgraph "MCP Server Tools Layer (mcp-server/src)"
        F[GetAllRulesMetadata Tool in main.py] -- Add contextFilter param to schema & call, pass to RuleSystemIntegration --> F
        F -- Uses --> E
    end

    C --> B