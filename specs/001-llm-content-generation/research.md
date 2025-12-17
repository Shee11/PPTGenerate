# Research: LLM-Based Content Generation System

**Branch**: `001-llm-content-generation`  
**Date**: December 15, 2025  
**Purpose**: Resolve technical unknowns and establish best practices for implementation

## Research Tasks

### 1. Caching Backend Selection

**Decision**: Filesystem-based JSON caching in `.cache/` directories

**Rationale**:
- **Simplicity**: No external dependencies (redis/memcached) required - aligns with constitution principle VII (Simplicity and Clarity)
- **Cross-platform**: Works identically on Windows PowerShell and Unix bash
- **Version control friendly**: `.cache/` can be gitignored, no service management scripts needed
- **Sufficient performance**: <100ms read/write for JSON files under 1MB meets SC-001 (<10s total for atom extraction includes I/O)
- **Inspectable**: Cache contents are human-readable JSON, aiding debugging
- **Atomic writes**: Use temp file + rename pattern for safe concurrent access

**Alternatives considered**:
- Redis/Memcached: Rejected because it requires external service management, complicates cross-platform setup, and adds operational complexity for marginal performance gain in single-user CLI context
- SQLite: Rejected because it adds dependency and complexity vs simple JSON files; no need for query capabilities

**Implementation approach**:
- Hash key: `SHA256(source_content + prompt_template + model_config)` → 64-char hex string
- Cache structure: `.cache/atoms/{hash[:2]}/{hash}.json` (2-char prefix for directory sharding)
- Metadata: Include timestamp, model version, source file path in cached JSON
- Invalidation: Manual (delete `.cache/` directory) or TTL-based (optional enhancement)

---

### 2. Azure OpenAI Integration Best Practices

**Decision**: Singleton LLM client with connection pooling and retry logic

**Rationale**:
- **Token efficiency**: Authentication tokens are expensive to acquire; reuse across multiple API calls
- **Connection pooling**: Azure OpenAI SDK handles connection reuse automatically when client is long-lived
- **Retry logic**: Built-in exponential backoff for transient failures (429 rate limits, 503 service unavailable)
- **Configuration**: Load from `.env` file once at startup (AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION)

**Implementation approach**:
```python
# src/utils/llm_client.py
from openai import AzureOpenAI
from functools import lru_cache

@lru_cache(maxsize=1)
def get_llm_client() -> AzureOpenAI:
    """Singleton LLM client with connection pooling"""
    # Load from .env, return configured client
    # Client handles token management and retries internally
```

**Best practices**:
- System prompts: Define once per flow type (atom extraction vs layout generation)
- Temperature: 0.7 for creative content, 0.2 for structured extraction
- Max tokens: Calculated based on expected output size + 20% buffer
- Streaming: Not needed for batch generation (all content returned at once)
- Error handling: Catch `openai.RateLimitError`, `openai.APIError`, retry with backoff

**Alternatives considered**:
- Client per request: Rejected due to token acquisition overhead (~200-500ms per auth)
- LangChain/LlamaIndex: Rejected as over-engineering for simple prompt→response pattern

---

### 3. Patch-Based State Management Pattern

**Decision**: JSON Patch (RFC 6902) format with custom PatchableCollection base class

**Rationale**:
- **Standard format**: JSON Patch is well-defined spec with existing validators
- **LLM-friendly**: Simple structure LLMs can generate reliably:
  ```json
  [
    {"op": "add", "path": "/atoms/atom_001", "value": {...}},
    {"op": "replace", "path": "/slides/0/state", "value": "draft"}
  ]
  ```
- **Incremental updates**: Only transmit changes, not full collections (reduces token usage)
- **Validation**: Can validate patches before applying (fail fast on schema violations)
- **Rollback**: Store patch history for undo/debugging

**Implementation approach**:
```python
# src/common/patchable.py
class PatchableCollection:
    def apply_patch(self, patch: list[dict]) -> None:
        """Apply JSON Patch operations to collection"""
        # Validate patch schema
        # Apply operations in order
        # Update internal state
    
    def to_dict(self) -> dict:
        """Serialize for LLM context"""
        
    @classmethod
    from_dict(cls, data: dict):
        """Deserialize from LLM output"""
```

**Alternatives considered**:
- Full replacement: Rejected because it wastes tokens sending unchanged data and loses incremental progress
- Custom patch format: Rejected in favor of standard (JSON Patch) for better tooling/validation
- Event sourcing: Over-engineering for initial implementation; patches provide sufficient auditability

---

### 4. Relationship Preservation in Atom Extraction

**Decision**: Nested JSON structures with explicit relationship fields

**Rationale**:
- **LLM-compatible**: Modern LLMs (GPT-4, Claude) excel at generating nested JSON
- **Type-specific formats**:
  - **Statement atoms**: `{"type": "statement", "text": "...", "source_ref": {...}}`
  - **Process atoms**: `{"type": "process", "steps": [{"order": 1, "text": "...", "dependencies": []}], "source_ref": {...}}`
  - **Comparison atoms**: `{"type": "comparison", "dimensions": [...], "entities": {...}, "source_ref": {...}}`
- **Explicit relationships**: `dependencies`, `related_to`, `contradicts` fields link atoms
- **Source traceability**: Every atom has `source_ref: {file: str, offset: int, length: int}`

**Implementation approach**:
- Prompt engineering: Provide schema examples in system prompt
- Validation: Pydantic models for each atom type with relationship field validation
- Post-processing: Verify relationship integrity (no dangling references)

**Alternatives considered**:
- Graph database: Rejected as over-engineering; JSON nested structures sufficient
- Flat list with ID references: Rejected because it's harder for LLMs to generate correctly and relationships are less obvious

---

### 5. Two-Step Layout Generation State Management

**Decision**: Explicit state field on Slide model with validation

**Rationale**:
- **Clear state machine**: `initial → draft → active` (FR-019)
- **Patch-based transitions**:
  1. First LLM call generates state transition patch: `[{"op": "replace", "path": "/slides/0/state", "value": "draft"}]`
  2. Second LLM call generates content patch: `[{"op": "replace", "path": "/slides/0/widgets/cell_1", "value": {...}}]`
- **Progress visibility**: Users see draft state before waiting for full content
- **Retry-friendly**: If content generation fails, slides remain in draft state for retry
- **Validation**: State transitions validated before applying patches

**Implementation approach**:
```python
# src/common/slide.py
class SlideState(str, Enum):
    INITIAL = "initial"
    DRAFT = "draft"
    ACTIVE = "active"

class Slide(BaseModel):
    state: SlideState = SlideState.INITIAL
    # ... other fields
```

**Alternatives considered**:
- Single-step generation: Rejected per complexity justification (loses progress on failure)
- Status flags: Rejected in favor of explicit enum for type safety

---

### 6. CLI Context and Instruction Parameters

**Decision**: Add `--context` and `--user-instruction` flags to `uce-render` CLI

**Rationale**:
- **Separation of concerns**: Context (source files) separate from instructions (generation directives)
- **File-based input**: Supports large contexts that exceed command-line argument limits
- **Reusability**: Same context can be used with different instructions

**Implementation approach**:
```python
# cli/uce_render.py
@click.command()
@click.option('--context', type=click.Path(exists=True), help='Path to context file (source content)')
@click.option('--user-instruction', type=click.Path(exists=True), help='Path to instruction file')
def generate(context, user_instruction):
    # Read context and instruction files
    # Pass to generation flows
```

**File formats**:
- **Context**: Plain text, VTT, or JSON list of file paths
- **Instruction**: Plain text markdown or structured JSON

**Alternatives considered**:
- Inline arguments: Rejected due to shell escaping issues and length limits
- YAML config files: Rejected as over-engineering; simple paths sufficient

---

## Summary of Decisions

| Unknown | Decision | Impact |
|---------|----------|--------|
| Caching backend | Filesystem JSON | Simple, cross-platform, no external dependencies |
| LLM integration | Singleton Azure OpenAI client | Efficient token reuse, built-in retry logic |
| Patch format | JSON Patch (RFC 6902) | Standard, LLM-friendly, incremental updates |
| Relationship modeling | Nested JSON structures | LLM-compatible, explicit relationships |
| State management | Explicit enum with validation | Type-safe, clear state machine |
| CLI parameters | `--context` and `--user-instruction` flags | Separation of concerns, file-based input |

All technical unknowns resolved. Ready for Phase 1: Data Model and Contracts.
