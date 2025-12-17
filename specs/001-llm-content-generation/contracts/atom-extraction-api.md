# Atom Extraction API Contract

**Version**: 1.0.0  
**Date**: December 15, 2025  
**Purpose**: Define contract for atom extraction from source content

## Function Signature

```python
def extract_atoms(
    source: Source,
    config: GenerationConfig,
    use_cache: bool = True
) -> AtomCollection:
    """
    Extract atoms from source content using LLM.
    
    Args:
        source: Source entity with content to extract from
        config: Generation configuration (model, temperature, prompts)
        use_cache: Whether to use cached results if available
        
    Returns:
        AtomCollection with extracted atoms
        
    Raises:
        ValueError: If source content is empty or invalid
        LLMError: If LLM API call fails after retries
        ValidationError: If LLM output doesn't match schema
    """
```

## Input Schema

### Source
```json
{
  "source_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "product_overview.txt",
  "file_path": "/path/to/product_overview.txt",
  "content_type": "text/plain",
  "content": "Our product offers three key features:\n1. Fast processing...",
  "metadata": {
    "file_size": 1024,
    "encoding": "utf-8"
  },
  "created_at": "2025-12-15T10:00:00Z"
}
```

### GenerationConfig
```json
{
  "model": "gpt-4-turbo",
  "temperature": 0.2,
  "max_tokens": 4000,
  "system_prompt": "You are an expert content analyst...",
  "user_prompt_template": "Extract atoms from the following content:\n\n{content}",
  "response_format": "json"
}
```

## Output Schema

### AtomCollection (Success)
```json
{
  "atoms": {
    "atom_001": {
      "atom_id": "atom_001",
      "type": "process",
      "title": "Product Setup",
      "steps": [
        {"order": 1, "text": "Install software", "dependencies": []},
        {"order": 2, "text": "Configure settings", "dependencies": [1]},
        {"order": 3, "text": "Run first scan", "dependencies": [2]}
      ],
      "source_ref": {
        "source_id": "550e8400-e29b-41d4-a716-446655440000",
        "file_path": "/path/to/product_overview.txt",
        "offset": 45,
        "length": 123,
        "line_number": 5
      },
      "created_at": "2025-12-15T10:01:30Z",
      "metadata": {
        "model": "gpt-4-turbo",
        "temperature": 0.2
      }
    },
    "atom_002": {
      "atom_id": "atom_002",
      "type": "comparison",
      "dimensions": ["speed", "accuracy", "cost"],
      "entities": {
        "Method A": {"speed": "fast", "accuracy": "high", "cost": "expensive"},
        "Method B": {"speed": "slow", "accuracy": "very high", "cost": "cheap"}
      },
      "source_ref": {
        "source_id": "550e8400-e29b-41d4-a716-446655440000",
        "file_path": "/path/to/product_overview.txt",
        "offset": 200,
        "length": 89,
        "line_number": 12
      },
      "created_at": "2025-12-15T10:01:30Z",
      "metadata": {
        "model": "gpt-4-turbo",
        "temperature": 0.2
      }
    }
  },
  "source_ids": ["550e8400-e29b-41d4-a716-446655440000"],
  "version": 1,
  "patch_history": []
}
```

## LLM Prompt Template

### System Prompt
```
You are an expert content analyst that extracts structured atoms from text.

Your task is to identify and extract:
1. **Statements**: Important facts, claims, or assertions
2. **Processes**: Step-by-step procedures with dependencies
3. **Comparisons**: Side-by-side evaluations across dimensions

**CRITICAL RULES**:
- Preserve relationships between content elements (don't create flat lists)
- Link atoms using related_to, contradicts, or dependencies fields
- Include precise source references (offset, length, line_number)
- Output ONLY valid JSON matching the schema below
- Extract atoms that are meaningful and self-contained

**Output Schema**:
{
  "atoms": {
    "atom_001": {
      "atom_id": "atom_XXX",
      "type": "statement" | "process" | "comparison",
      ...type-specific fields...
      "source_ref": {
        "source_id": "SOURCE_ID",
        "file_path": "FILE_PATH",
        "offset": INT,
        "length": INT,
        "line_number": INT
      }
    }
  }
}

**Type-Specific Schemas**:

Statement:
{
  "type": "statement",
  "text": "The extracted statement",
  "related_to": ["atom_id1", "atom_id2"],
  "contradicts": ["atom_id3"]
}

Process:
{
  "type": "process",
  "title": "Process name",
  "steps": [
    {"order": 1, "text": "Step description", "dependencies": []}
  ]
}

Comparison:
{
  "type": "comparison",
  "dimensions": ["dimension1", "dimension2"],
  "entities": {
    "Entity1": {"dimension1": "value", "dimension2": "value"},
    "Entity2": {"dimension1": "value", "dimension2": "value"}
  }
}
```

### User Prompt Template
```
Extract atoms from the following source content.

Source ID: {source_id}
File Path: {file_path}
Content Type: {content_type}

Content:
---
{content}
---

Output a JSON object with the atoms dictionary. Ensure all source_ref fields use the provided source_id and file_path.
```

## LLM Response Format

### Expected JSON Structure
```json
{
  "atoms": {
    "atom_001": {...},
    "atom_002": {...}
  }
}
```

### Post-Processing Steps
1. Validate JSON schema using Pydantic
2. Assign UUIDs to atoms if not provided
3. Verify source_ref integrity (offsets within content bounds)
4. Check relationship references (no dangling atom IDs)
5. Wrap in AtomCollection with metadata

## Error Responses

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Atom atom_001: source_ref offset 5000 exceeds content length 1024",
  "details": {
    "atom_id": "atom_001",
    "field": "source_ref.offset",
    "constraint": "offset + length <= content_length"
  }
}
```

### LLM Error
```json
{
  "error": "LLMError",
  "message": "Rate limit exceeded, retry after 30s",
  "details": {
    "status_code": 429,
    "retry_after": 30,
    "model": "gpt-4-turbo"
  }
}
```

## Caching Contract

### Cache Key Computation
```python
cache_key = SHA256(
    source.content + 
    config.system_prompt + 
    config.user_prompt_template + 
    config.model + 
    str(config.temperature)
).hexdigest()
```

### Cache Lookup
```python
if use_cache:
    cached = cache.get(cache_key)
    if cached:
        return AtomCollection.from_dict(cached["cached_data"])
```

### Cache Storage
```python
cache.set(
    cache_key=cache_key,
    data=atom_collection.to_dict(),
    metadata=CacheMetadata(
        model=config.model,
        temperature=config.temperature,
        created_at=datetime.now(),
        source_files=[source.file_path],
        prompt_template_hash=SHA256(config.system_prompt).hexdigest()
    )
)
```

## Example Usage

```python
from src.generation.atom import extract_atoms
from src.common.source import Source
from src.utils.generation_config import GenerationConfig

# Load source
source = Source(
    source_id="550e8400-e29b-41d4-a716-446655440000",
    name="overview.txt",
    file_path="/data/overview.txt",
    content_type="text/plain",
    content=Path("/data/overview.txt").read_text()
)

# Configure generation
config = GenerationConfig(
    model="gpt-4-turbo",
    temperature=0.2,
    max_tokens=4000,
    system_prompt=ATOM_EXTRACTION_SYSTEM_PROMPT,
    user_prompt_template=ATOM_EXTRACTION_USER_TEMPLATE
)

# Extract atoms
atoms = extract_atoms(source, config, use_cache=True)

# Access results
for atom_id, atom in atoms.atoms.items():
    print(f"{atom.type}: {atom.atom_id}")
```

## Performance Expectations

- **Cache hit**: <100ms
- **Cache miss (LLM call)**: <10s for 1000-word documents
- **Token usage**: ~1.5x input tokens (input + output)
- **Retry logic**: 3 attempts with exponential backoff (1s, 2s, 4s)

## Validation Rules

1. All atoms MUST have valid source_ref pointing to source
2. All relationship references (related_to, contradicts, dependencies) MUST point to existing atoms
3. Process steps MUST NOT have circular dependencies
4. Comparison entities MUST have values for all dimensions
5. Source_ref offset+length MUST NOT exceed content length
6. Atom IDs MUST be unique within collection
