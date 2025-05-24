# Product Context: AgentRulesHub

## Purpose
AgentRulesHub serves as a foundational component for MCP servers to provide contextual rules to AI agents based on their current tasks. It enables dynamic rule retrieval that adapts to the specific needs of each task, improving agent performance and consistency.

## How It Works
1. Rules are stored with metadata including:
   - Unique identifier
   - Description
   - Optional language specification
   - Tags for categorization
2. Rules content is stored in YAML files, accessible through the FileSource implementation
3. The system can be queried to retrieve rules based on:
   - Programming language
   - Specific tags
   - Combinations of criteria

## User Experience Goals
- Simple and efficient rule retrieval
- Clear organization of rules through tags
- Easy extension for new rule sources
- Straightforward rule content management through YAML files
