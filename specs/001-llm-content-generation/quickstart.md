# Quickstart: LLM-Based Content Generation

**Branch**: `001-llm-content-generation`  
**Date**: December 15, 2025  
**Audience**: Developers implementing or using the content generation system

## Overview

This feature enables automatic generation of presentation content from source materials using LLM-based extraction and layout generation. The system uses a two-flow architecture:

1. **Atom Extraction Flow**: Extracts structured atoms (statements, processes, comparisons) from source files
2. **Layout Generation Flow**: Generates presentation slides with proper layout strategies and widget content

Both flows use **patch-based updates** to maintain context and enable caching.

## Prerequisites

- Python 3.11+
- Azure OpenAI API access with GPT-4+ model
- `.env` file configured with Azure credentials

## Quick Start (5 minutes)

### 1. Configure Environment

Create/update `.env` file:
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 2. Prepare Source Content

Create `context.txt`:
```
Our product offers three key features:
1. Fast processing with 10x speed improvement
2. Advanced security using end-to-end encryption
3. User-friendly interface with drag-and-drop

Compared to competitors:
- We are faster but more expensive
- Competitor A is slower but cheaper
- Competitor B has similar speed at higher cost
```

### 3. Create Instruction File

Create `instruction.txt`:
```
Create a 3-slide presentation:
- Slide 1: Overview of key features using Bento.Standard
- Slide 2: Competitive comparison using Swiss.Asymmetry
- Slide 3: Summary with Data.KPI_Row
```

### 4. Generate Content

```bash
# From project root
uce-render generate --context context.txt --user-instruction instruction.txt --output presentation.json
```

### 5. Inspect Results

```bash
# View generated atoms
cat .cache/atoms/<hash>.json

# View generated slides
cat presentation.json
```

## Architecture Overview

```
┌─────────────┐
│ Source File │
└──────┬──────┘
       │
       │ 1. Load source
       ▼
┌─────────────────┐
│ Atom Extraction │ ← LLM Call (with caching)
└──────┬──────────┘
       │
       │ 2. Extract atoms as patches
       ▼
┌─────────────────┐
│ AtomCollection  │
└──────┬──────────┘
       │
       │ 3. Pass to layout generation
       ▼
┌──────────────────┐
│ Layout Generation│ ← LLM Call (two-step, with caching)
└──────┬───────────┘
       │
       │ 4a. State transition patch (draft)
       │ 4b. Content generation patch (active)
       ▼
┌──────────────────┐
│ SlideCollection  │
└──────┬───────────┘
       │
       │ 5. Render to HTML/JSON
       ▼
┌──────────────────┐
│ Output File      │
└──────────────────┘
```

## Core Concepts

### PatchableCollection

Base class for Atom and Slide collections that supports incremental updates via JSON Patch (RFC 6902).

**Why patches?**
- LLM outputs incremental changes, not full replacements
- Preserves context across multiple generation steps
- Enables undo/rollback via patch history
- Reduces token usage (only changes transmitted)

**Example patch**:
```json
[
  {"op": "add", "path": "/atoms/atom_001", "value": {...}},
  {"op": "replace", "path": "/slides/0/state", "value": "draft"}
]
```

### Atom Types

| Type | Purpose | Example Use Case |
|------|---------|-----------------|
| **Statement** | Important facts/claims | "Product achieves 99.9% uptime" |
| **Process** | Step-by-step procedures with dependencies | Installation instructions with order |
| **Comparison** | Multi-dimensional comparisons | Feature matrix, pricing tiers |

### Slide States

```
initial → draft → active
```

- **initial**: Slide created, no content
- **draft**: Layout strategy assigned, awaiting content
- **active**: Content populated, ready for rendering

### Caching Strategy

Caches use SHA256 hash keys computed from:
```
hash = SHA256(source_content + prompt + model_config)
```

**Cache locations**:
- Atoms: `.cache/atoms/{hash[:2]}/{hash}.json`
- Layouts: `.cache/layouts/{hash[:2]}/{hash}.json`

**Cache invalidation**: Delete `.cache/` directory or specific files

## Implementation Guide

### Directory Structure

```
src/
├── utils/
│   ├── llm_client.py         # Singleton Azure OpenAI client
│   └── generation_config.py  # Configuration models
├── common/
│   ├── patchable.py           # PatchableCollection base class
│   ├── source.py              # Source entity
│   ├── slide.py               # Slide entity with state enum
│   └── slides.py              # SlideCollection (extends patchable)
└── generation/
    ├── atom/
    │   ├── __init__.py
    │   ├── models.py          # Atom entity types
    │   ├── collection.py      # AtomCollection
    │   ├── extractor.py       # extract_atoms() function
    │   └── prompts.py         # LLM prompts for extraction
    └── content/
        ├── __init__.py
        ├── generator.py       # generate_layout() function
        └── prompts.py         # LLM prompts for layout

cli/
└── uce_render.py              # Add --context and --user-instruction flags
```

### Key Modules

#### 1. LLM Client (Reusable)

```python
# src/utils/llm_client.py
from openai import AzureOpenAI
from functools import lru_cache
import os

@lru_cache(maxsize=1)
def get_llm_client() -> AzureOpenAI:
    """Singleton client - called once, reused for all requests"""
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

def call_llm(system_prompt: str, user_prompt: str, config: GenerationConfig) -> dict:
    """Wrapper for LLM calls with retry logic"""
    client = get_llm_client()
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        response_format={"type": "json_object"} if config.response_format == "json" else None
    )
    return response.choices[0].message.content
```

#### 2. PatchableCollection Base Class

```python
# src/common/patchable.py
from abc import ABC, abstractmethod
from jsonpatch import JsonPatch

class PatchableCollection(ABC):
    version: int = 0
    patch_history: list[dict] = []
    
    def apply_patch(self, patch: list[dict]) -> None:
        """Apply JSON Patch operations"""
        # Validate patch schema
        patch_obj = JsonPatch(patch)
        
        # Convert to dict, apply, convert back
        data = self.to_dict()
        result = patch_obj.apply(data)
        self._update_from_dict(result)
        
        # Update metadata
        self.version += 1
        self.patch_history.append({"version": self.version, "patch": patch})
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize to dict for LLM context"""
        pass
    
    @abstractmethod
    def _update_from_dict(self, data: dict) -> None:
        """Update internal state from dict"""
        pass
```

#### 3. Atom Extraction

```python
# src/generation/atom/extractor.py
from src.utils.llm_client import call_llm
from src.utils.cache import GenerationCache

def extract_atoms(
    source: Source,
    config: GenerationConfig,
    use_cache: bool = True
) -> AtomCollection:
    # Check cache
    cache_key = compute_cache_key(source, config)
    if use_cache:
        cached = GenerationCache.get(cache_key)
        if cached:
            return AtomCollection.from_dict(cached["cached_data"])
    
    # Call LLM
    system_prompt = ATOM_EXTRACTION_SYSTEM_PROMPT
    user_prompt = ATOM_EXTRACTION_USER_TEMPLATE.format(
        source_id=source.source_id,
        file_path=source.file_path,
        content_type=source.content_type,
        content=source.content
    )
    
    response = call_llm(system_prompt, user_prompt, config)
    atoms_dict = json.loads(response)
    
    # Wrap in collection
    collection = AtomCollection.from_dict(atoms_dict)
    
    # Cache result
    GenerationCache.set(cache_key, collection.to_dict(), metadata={...})
    
    return collection
```

#### 4. Layout Generation (Two-Step)

```python
# src/generation/content/generator.py

def generate_layout(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    use_cache: bool = True
) -> SlideCollection:
    # Check cache
    cache_key = compute_cache_key(atoms, user_instruction, config)
    if use_cache:
        cached = GenerationCache.get(cache_key)
        if cached:
            return SlideCollection.from_dict(cached["cached_data"])
    
    # Step 1: State transition (initial → draft)
    state_patch = _generate_state_transition(atoms, user_instruction, config)
    collection = SlideCollection(slides=[], theme=None, version=0)
    collection.apply_patch(state_patch)
    
    # Step 2: Content generation (draft → active)
    content_patch = _generate_content(atoms, collection, user_instruction, config)
    collection.apply_patch(content_patch)
    
    # Cache result
    GenerationCache.set(cache_key, collection.to_dict(), metadata={...})
    
    return collection

def _generate_state_transition(atoms, instruction, config) -> list[dict]:
    """Step 1: Generate draft slides with strategies assigned"""
    system_prompt = STATE_TRANSITION_SYSTEM_PROMPT
    user_prompt = STATE_TRANSITION_USER_TEMPLATE.format(
        atoms=json.dumps(atoms.to_dict(), indent=2),
        instruction=instruction
    )
    response = call_llm(system_prompt, user_prompt, config)
    return json.loads(response)  # Returns JSON Patch

def _generate_content(atoms, draft_slides, instruction, config) -> list[dict]:
    """Step 2: Populate widget content and activate"""
    system_prompt = CONTENT_GENERATION_SYSTEM_PROMPT
    user_prompt = CONTENT_GENERATION_USER_TEMPLATE.format(
        draft_slides=json.dumps(draft_slides.to_dict(), indent=2),
        atoms=json.dumps(atoms.to_dict(), indent=2),
        instruction=instruction
    )
    response = call_llm(system_prompt, user_prompt, config)
    return json.loads(response)  # Returns JSON Patch
```

### CLI Integration

```python
# cli/uce_render.py
import click

@click.group()
def cli():
    """UCE Render CLI"""
    pass

@cli.command()
@click.option('--context', type=click.Path(exists=True), required=True,
              help='Path to source content file(s)')
@click.option('--user-instruction', type=click.Path(exists=True), required=True,
              help='Path to generation instruction file')
@click.option('--output', type=click.Path(), default='output.json',
              help='Output file path')
@click.option('--no-cache', is_flag=True, help='Disable caching')
def generate(context, user_instruction, output, no_cache):
    """Generate presentation from source content"""
    # Load source
    source = Source.from_file(context)
    
    # Load instruction
    instruction_text = Path(user_instruction).read_text()
    
    # Extract atoms
    atom_config = GenerationConfig.for_atom_extraction()
    atoms = extract_atoms(source, atom_config, use_cache=not no_cache)
    
    # Generate layout
    layout_config = GenerationConfig.for_layout_generation()
    slides = generate_layout(atoms, instruction_text, layout_config, use_cache=not no_cache)
    
    # Save output
    Path(output).write_text(json.dumps(slides.to_dict(), indent=2))
    
    click.echo(f"Generated {len(slides.slides)} slides → {output}")
```

## Testing Strategy

### Unit Tests (Per Entity)

```python
# tests/test_patchable.py
def test_apply_patch_adds_item():
    collection = AtomCollection(atoms={})
    patch = [{"op": "add", "path": "/atoms/atom_001", "value": {...}}]
    collection.apply_patch(patch)
    assert "atom_001" in collection.atoms
    assert collection.version == 1

# tests/test_state_transitions.py
def test_slide_state_progression():
    slide = Slide(state=SlideState.INITIAL)
    slide.state = SlideState.DRAFT  # Valid
    slide.state = SlideState.ACTIVE  # Valid
    
    with pytest.raises(StateTransitionError):
        slide.state = SlideState.INITIAL  # Invalid (backwards)
```

### Integration Tests (Flows)

```python
# tests/integration/test_atom_extraction.py
def test_extract_atoms_from_text_file(mock_llm):
    source = Source.from_file("tests/fixtures/sample.txt")
    config = GenerationConfig.for_atom_extraction()
    
    atoms = extract_atoms(source, config)
    
    assert len(atoms.atoms) > 0
    assert all(atom.source_ref.source_id == source.source_id for atom in atoms.atoms.values())

# tests/integration/test_layout_generation.py
def test_two_step_layout_generation(mock_llm, sample_atoms):
    instruction = "Create 3 slides"
    config = GenerationConfig.for_layout_generation()
    
    slides = generate_layout(sample_atoms, instruction, config)
    
    assert len(slides.slides) == 3
    assert all(slide.state == SlideState.ACTIVE for slide in slides.slides)
    assert all(slide.widgets for slide in slides.slides)  # Content populated
```

### Contract Tests (LLM Outputs)

```python
# tests/contract/test_llm_schema_compliance.py
def test_atom_extraction_output_schema(real_llm_call):
    """Verify LLM outputs valid atom JSON"""
    response = real_llm_call(ATOM_EXTRACTION_SYSTEM_PROMPT, sample_user_prompt)
    atoms_dict = json.loads(response)
    
    # Validate against Pydantic models
    AtomCollection.from_dict(atoms_dict)  # Should not raise

def test_layout_generation_uses_supported_widgets(real_llm_call):
    """Verify LLM only uses schema-compliant widgets"""
    response = real_llm_call(CONTENT_GENERATION_SYSTEM_PROMPT, sample_user_prompt)
    patch = json.loads(response)
    
    for op in patch:
        if "widgets" in op["path"]:
            widget = op["value"]
            assert widget["type"] in SUPPORTED_WIDGET_TYPES
```

## Next Steps

1. **Review API contracts**: See `contracts/atom-extraction-api.md` and `contracts/layout-generation-api.md`
2. **Implement data models**: Start with `src/common/patchable.py` and entities
3. **Create LLM utilities**: Build `src/utils/llm_client.py` with singleton pattern
4. **Implement atom extraction**: Follow `src/generation/atom/extractor.py` structure
5. **Implement layout generation**: Build two-step flow in `src/generation/content/generator.py`
6. **Add CLI commands**: Extend `cli/uce_render.py` with `--context` and `--user-instruction` flags
7. **Write tests**: Follow TDD - tests before implementation

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| **LLM generates invalid JSON** | Use `response_format={"type": "json_object"}` in API call |
| **Cache misses on identical inputs** | Ensure deterministic hash computation (sort dict keys) |
| **State transitions fail** | Validate state before applying patches, use Pydantic validators |
| **Token limits exceeded** | Chunk large sources, summarize atoms for layout generation |
| **Circular dependencies in processes** | Validate dependency graph in ProcessAtom post-processing |
| **Re-authenticating LLM client** | Use singleton pattern with `@lru_cache` decorator |

## References

- [API Contracts](./contracts/)
- [Data Model](./data-model.md)
- [Research Decisions](./research.md)
- [Feature Specification](./spec.md)
