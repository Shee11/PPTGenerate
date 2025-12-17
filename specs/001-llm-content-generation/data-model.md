# Data Model: LLM-Based Content Generation System

**Branch**: `001-llm-content-generation`  
**Date**: December 15, 2025  
**Purpose**: Define entities, relationships, and validation rules

## Entity Definitions

### 1. Source

**Purpose**: Represents grounding content input for atom extraction

**Fields**:
- `source_id: str` - Unique identifier (UUID4)
- `name: str` - Display name or filename
- `file_path: str` - Absolute path to source file
- `content_type: Literal["text/plain", "text/vtt"]` - MIME type
- `content: str` - Raw content from file
- `metadata: dict[str, Any]` - Additional metadata (file size, encoding, timestamps)
- `created_at: datetime` - When source was loaded

**Relationships**:
- One Source → Many Atoms (one-to-many)

**Validation Rules**:
- `file_path` must exist and be readable
- `content_type` must match file extension (.txt → text/plain, .vtt → text/vtt)
- `content` must not be empty string
- `source_id` must be unique within session

**State Transitions**: N/A (immutable once loaded)

---

### 2. SourceReference

**Purpose**: Links atoms back to specific locations in source content

**Fields**:
- `source_id: str` - References Source.source_id
- `file_path: str` - Denormalized for convenience
- `offset: int` - Character offset in source content (0-indexed)
- `length: int` - Number of characters referenced
- `line_number: int | None` - Line number for text sources (1-indexed)

**Validation Rules**:
- `offset >= 0`
- `length > 0`
- `offset + length <= len(source.content)`
- `line_number >= 1` if provided

---

### 3. Atom

**Purpose**: Extracted content unit with preserved relationships

**Base Fields** (all atom types):
- `atom_id: str` - Unique identifier (UUID4)
- `type: Literal["statement", "process", "comparison"]` - Atom format type
- `source_ref: SourceReference` - Link to source location
- `created_at: datetime` - When atom was extracted
- `metadata: dict[str, Any]` - LLM generation metadata (model, temperature, etc.)

**Type-Specific Fields**:

#### Statement Atom
```python
class StatementAtom(Atom):
    type: Literal["statement"] = "statement"
    text: str  # The extracted statement
    related_to: list[str] = []  # atom_ids of related atoms
    contradicts: list[str] = []  # atom_ids of contradictory atoms
```

#### Process Atom
```python
class ProcessStep(BaseModel):
    order: int  # 1-indexed step number
    text: str  # Step description
    dependencies: list[int] = []  # Step orders this depends on

class ProcessAtom(Atom):
    type: Literal["process"] = "process"
    title: str  # Process name
    steps: list[ProcessStep]  # Ordered steps with dependencies
```

#### Comparison Atom
```python
class ComparisonAtom(Atom):
    type: Literal["comparison"] = "comparison"
    dimensions: list[str]  # What aspects are compared (e.g., ["cost", "performance"])
    entities: dict[str, dict[str, str]]  # Entity → dimension → value
    # Example: {"Option A": {"cost": "high", "performance": "fast"}}
```

**Relationships**:
- Many Atoms → One Source (many-to-one via source_ref)
- Atoms → Atoms (many-to-many via related_to, contradicts, dependencies)

**Validation Rules**:
- `atom_id` must be unique within AtomCollection
- `source_ref` must reference valid Source
- Related atom IDs (`related_to`, `contradicts`) must exist in collection
- Process steps must have valid dependency references (no cycles)
- Comparison entities must have values for all dimensions

---

### 4. AtomCollection

**Purpose**: PatchableCollection container for atoms

**Fields**:
- `atoms: dict[str, Atom]` - atom_id → Atom mapping
- `source_ids: list[str]` - Sources contributing atoms
- `version: int` - Incremented on each patch application
- `patch_history: list[dict]` - Audit log of applied patches

**Operations**:
- `apply_patch(patch: list[dict]) -> None` - Apply JSON Patch operations
- `get_by_source(source_id: str) -> list[Atom]` - Filter atoms by source
- `get_by_type(atom_type: str) -> list[Atom]` - Filter by type
- `to_dict() -> dict` - Serialize for LLM context
- `from_dict(data: dict) -> AtomCollection` - Deserialize from LLM output

**Validation Rules**:
- All atom IDs in patches must be valid (exist or being added)
- Patches must not create orphan references
- Version must increment monotonically

---

### 5. Slide

**Purpose**: Presentation slide with layout config and state

**Fields**:
- `slide_id: str` - Unique identifier (UUID4)
- `state: SlideState` - Enum: initial, draft, active
- `strategy: str` - Layout strategy name (e.g., "Bento.Standard")
- `widgets: dict[str, dict]` - Widget configs (matches existing schema)
- `header: dict | None` - Header widget config
- `footer: dict | None` - Footer widget config
- `parameters: dict[str, Any]` - Strategy-specific parameters
- `created_at: datetime` - When slide was initialized
- `updated_at: datetime` - Last modification timestamp

**Relationships**:
- Many Slides → One SlideCollection (contained by)

**State Transitions**:
```
initial → draft  (via state transition patch)
draft → active   (via content generation patch)
```

**Validation Rules**:
- `state` transitions must follow: initial → draft → active (no backwards)
- `strategy` must be valid layout strategy name
- `widgets` must conform to layout schema
- When `state == "active"`, widgets must have content (not empty)

---

### 6. SlideState (Enum)

```python
class SlideState(str, Enum):
    INITIAL = "initial"  # Slide created, no content
    DRAFT = "draft"      # State transition applied, awaiting content
    ACTIVE = "active"    # Content generated and applied
```

---

### 7. SlideCollection

**Purpose**: PatchableCollection container for slides (extends Content/Layout entity from spec)

**Fields**:
- `slides: list[Slide]` - Ordered list of slides
- `theme: dict | None` - Presentation theme config
- `version: int` - Incremented on each patch application
- `patch_history: list[dict]` - Audit log of applied patches

**Operations**:
- `apply_patch(patch: list[dict]) -> None` - Apply JSON Patch operations
- `get_by_state(state: SlideState) -> list[Slide]` - Filter by state
- `to_dict() -> dict` - Serialize for LLM context
- `from_dict(data: dict) -> SlideCollection` - Deserialize from LLM output

**Validation Rules**:
- Slide order must be preserved across patches
- All slide IDs in patches must be valid
- State transitions must be valid per Slide validation rules

---

### 8. PatchableCollection (Base Class)

**Purpose**: Abstract base class for collections supporting JSON Patch operations

**Abstract Methods**:
- `apply_patch(patch: list[dict]) -> None` - Apply JSON Patch (RFC 6902)
- `to_dict() -> dict` - Serialize to JSON-compatible dict
- `from_dict(cls, data: dict) -> Self` - Deserialize from dict

**Common Fields**:
- `version: int` - Patch application counter
- `patch_history: list[dict]` - Audit log (optional, for debugging)

**Validation**:
- Patches must conform to JSON Patch schema
- Operations must be valid for collection structure
- Apply must be atomic (all ops succeed or all fail)

---

### 9. GenerationCache

**Purpose**: Hash-indexed cache for LLM-generated content

**Fields**:
- `cache_key: str` - SHA256 hash (source_content + prompt + model_config)
- `cache_type: Literal["atoms", "layouts"]` - What's being cached
- `cached_data: dict` - Serialized AtomCollection or SlideCollection
- `metadata: CacheMetadata` - Generation metadata

**CacheMetadata Fields**:
- `model: str` - LLM model used (e.g., "gpt-4-turbo")
- `temperature: float` - Generation temperature
- `created_at: datetime` - Cache creation time
- `source_files: list[str]` - Source file paths
- `prompt_template_hash: str` - Hash of prompt template

**Operations**:
- `get(cache_key: str) -> dict | None` - Retrieve cached data
- `set(cache_key: str, data: dict, metadata: CacheMetadata) -> None` - Store in cache
- `invalidate(pattern: str) -> int` - Delete matching cache entries
- `compute_key(source: str, prompt: str, config: dict) -> str` - Generate cache key

**Validation Rules**:
- `cache_key` must be 64-char hex string (SHA256)
- `cached_data` must deserialize to valid collection
- Cache files stored at `.cache/{cache_type}/{cache_key[:2]}/{cache_key}.json`

---

### 10. GenerationConfig

**Purpose**: Configuration for LLM generation requests

**Fields**:
- `model: str` - Azure OpenAI deployment name
- `temperature: float` - 0.0-2.0, controls randomness
- `max_tokens: int` - Maximum response tokens
- `system_prompt: str` - System message for LLM
- `user_prompt_template: str` - Template for user messages
- `response_format: Literal["json", "text"]` - Expected output format

**Validation Rules**:
- `temperature` in range [0.0, 2.0]
- `max_tokens > 0`
- `system_prompt` and `user_prompt_template` not empty

---

## Entity Relationship Diagram (ERD)

```
Source (1) ─────< (n) Atom
                       ├─ StatementAtom
                       ├─ ProcessAtom
                       └─ ComparisonAtom
                              │
                              │ contained by
                              ▼
                      AtomCollection (extends PatchableCollection)


Slide ─────> SlideState (enum)
  │
  │ contained by
  ▼
SlideCollection (extends PatchableCollection)


PatchableCollection (abstract)
  ├─ AtomCollection
  └─ SlideCollection


GenerationCache
  ├─ atoms cache → AtomCollection
  └─ layouts cache → SlideCollection


Atom ──> SourceReference ──> Source
```

## Validation Summary

| Entity | Key Validations |
|--------|----------------|
| Source | File exists, content not empty, type matches extension |
| SourceReference | Valid offset/length, references existing source |
| Atom | Unique ID, valid source_ref, no orphan relationships |
| AtomCollection | Patch integrity, no dangling references |
| Slide | Valid state transitions (initial→draft→active), schema compliance |
| SlideCollection | Patch integrity, order preservation |
| PatchableCollection | Atomic patch application, JSON Patch schema compliance |
| GenerationCache | Valid SHA256 keys, deserializable data |
| GenerationConfig | Valid temperature/max_tokens ranges |

## State Transition Diagrams

### Slide State Machine
```
┌─────────┐
│ INITIAL │ (slide created)
└────┬────┘
     │ State transition patch applied
     │ {"op": "replace", "path": "/slides/0/state", "value": "draft"}
     ▼
 ┌───────┐
 │ DRAFT │ (awaiting content)
 └───┬───┘
     │ Content generation patch applied
     │ {"op": "replace", "path": "/slides/0/widgets/...", "value": {...}}
     ▼
 ┌────────┐
 │ ACTIVE │ (content complete)
 └────────┘
```

### Atom Extraction Flow
```
Source File → Load → Source Entity
                         │
                         │ LLM Extraction
                         ▼
                    JSON Patch (atoms)
                         │
                         │ Apply to collection
                         ▼
                   AtomCollection
                         │
                         │ Cache with hash key
                         ▼
                  GenerationCache
```

### Layout Generation Flow
```
AtomCollection → LLM Prompt → State Transition Patch
                                     │
                                     │ Apply
                                     ▼
                              SlideCollection (draft)
                                     │
                                     │ LLM Content Gen
                                     ▼
                              Content Generation Patch
                                     │
                                     │ Apply
                                     ▼
                              SlideCollection (active)
                                     │
                                     │ Cache with hash key
                                     ▼
                              GenerationCache
```
