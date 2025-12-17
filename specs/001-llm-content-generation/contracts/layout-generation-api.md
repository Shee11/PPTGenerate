# Layout Generation API Contract

**Version**: 1.0.0  
**Date**: December 15, 2025  
**Purpose**: Define contract for layout generation from atoms

## Function Signature

```python
def generate_layout(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    use_cache: bool = True
) -> SlideCollection:
    """
    Generate presentation layout from atoms using LLM (two-step process).
    
    Step 1: Generate state transition patch (initial → draft)
    Step 2: Generate content patch (populate widgets, draft → active)
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions (e.g., "Create 5 slides")
        config: Generation configuration (model, temperature, prompts)
        use_cache: Whether to use cached results if available
        
    Returns:
        SlideCollection with active slides and content
        
    Raises:
        ValueError: If atoms is empty or instruction invalid
        LLMError: If LLM API call fails after retries
        ValidationError: If LLM output doesn't match schema
        StateTransitionError: If slide state transitions are invalid
    """
```

## Input Schema

### AtomCollection
```json
{
  "atoms": {
    "atom_001": {
      "atom_id": "atom_001",
      "type": "process",
      "title": "Setup Process",
      "steps": [...]
    },
    "atom_002": {
      "atom_id": "atom_002",
      "type": "comparison",
      "dimensions": ["speed", "accuracy"],
      "entities": {...}
    }
  },
  "source_ids": ["550e8400-..."],
  "version": 1
}
```

### User Instruction (text)
```
Create a 10-slide presentation about the product.
- Start with overview using Bento.Standard layout
- Show comparison data using Swiss.Asymmetry
- Include process steps with Focus.Solar_System
- Use cyber-tech theme with neon colors
```

### GenerationConfig
```json
{
  "model": "gpt-4-turbo",
  "temperature": 0.7,
  "max_tokens": 8000,
  "system_prompt": "You are a presentation designer...",
  "user_prompt_template": "Generate slides from these atoms:\n{atoms}\n\nInstructions: {instruction}",
  "response_format": "json"
}
```

## Output Schema

### SlideCollection (Final State - Active)
```json
{
  "slides": [
    {
      "slide_id": "slide_001",
      "state": "active",
      "strategy": "Bento.Standard",
      "widgets": {
        "cell_1": {
          "type": "Type.Display",
          "parameters": {"text": "NEURAL NETWORK ALPHA"},
          "preset": {"surface": "Elevated", "shape": "Rounded"}
        },
        "cell_2": {
          "type": "Type.Heading",
          "parameters": {"text": "System Overview", "level": 2}
        }
      },
      "header": {
        "type": "Type.Body",
        "parameters": {"text": "CLASSIFIED | NEXUS PROTOCOL"}
      },
      "footer": {
        "type": "Type.Body",
        "parameters": {"text": "NODE-001 | UPLINK ACTIVE"}
      },
      "created_at": "2025-12-15T10:05:00Z",
      "updated_at": "2025-12-15T10:05:15Z"
    }
  ],
  "theme": {
    "primary_color": "#00ff9f",
    "background_color": "#0a0e27",
    "typography": {...}
  },
  "version": 2,
  "patch_history": [
    {"op": "replace", "path": "/slides/0/state", "value": "draft"},
    {"op": "replace", "path": "/slides/0/widgets", "value": {...}}
  ]
}
```

## Two-Step Generation Process

### Step 1: State Transition Patch

**Purpose**: Initialize slides in draft state

**LLM Prompt** (system + user):
```
System: You are a presentation structure designer. Generate JSON Patch operations to initialize slides.

Output a JSON Patch array that:
1. Creates slide entries with strategy assignments
2. Sets all slides to "draft" state
3. Does NOT populate widget content yet

User: Create {N} slides based on these atoms and instructions:

Atoms: {atom_summary}
Instructions: {user_instruction}

Output JSON Patch operations to initialize slides.
```

**Expected Output**:
```json
[
  {
    "op": "add",
    "path": "/slides/0",
    "value": {
      "slide_id": "slide_001",
      "state": "draft",
      "strategy": "Bento.Standard",
      "widgets": {},
      "created_at": "2025-12-15T10:05:00Z"
    }
  },
  {
    "op": "add",
    "path": "/slides/1",
    "value": {
      "slide_id": "slide_002",
      "state": "draft",
      "strategy": "Swiss.Asymmetry",
      "widgets": {},
      "created_at": "2025-12-15T10:05:00Z"
    }
  }
]
```

**Application**:
```python
slide_collection = SlideCollection(slides=[], theme=None, version=0)
slide_collection.apply_patch(state_transition_patch)
# Result: slides in draft state, no content yet
```

---

### Step 2: Content Generation Patch

**Purpose**: Populate widget content and activate slides

**LLM Prompt** (system + user):
```
System: You are a presentation content generator. Generate JSON Patch operations to populate slide content.

You MUST:
1. Use ONLY supported widget types and attributes from the layout schema
2. Match content to the assigned strategy for each slide
3. Fill all required widget slots for each strategy
4. Set slide state to "active" after populating content
5. Ensure text content is derived from provided atoms

Supported Widget Types:
- Type.Display, Type.Heading, Type.Body, Type.Quote, Type.List
- Data.BigNum, Data.Progress, Data.Trend
- Media.Image (requires image_url)

Supported Preset Attributes:
- surface: Flat, Elevated, Sunken, Glass, Outline, NeoBrutal, Subtle
- shape: Sharp, Rounded, Pill, Curve, Squircle, Organic
- fill: Solid_Surface, Solid_Brand, Gradient_Linear, Gradient_Mesh, Pattern_Dot, Noise, Subtle
- effect: Glow, Shadow, Tape, Duotone

User: Populate content for these draft slides using atoms:

Current Slides: {draft_slides_json}
Atoms: {full_atoms_json}
Instructions: {user_instruction}

Output JSON Patch operations to:
1. Populate all widget content
2. Set state to "active"
```

**Expected Output**:
```json
[
  {
    "op": "replace",
    "path": "/slides/0/widgets",
    "value": {
      "cell_1": {
        "type": "Type.Display",
        "parameters": {"text": "NEURAL NETWORK ALPHA"},
        "preset": {"surface": "Elevated", "shape": "Rounded"}
      },
      "cell_2": {
        "type": "Type.Heading",
        "parameters": {"text": "System Overview", "level": 2}
      }
    }
  },
  {
    "op": "replace",
    "path": "/slides/0/state",
    "value": "active"
  },
  {
    "op": "replace",
    "path": "/slides/0/updated_at",
    "value": "2025-12-15T10:05:15Z"
  }
]
```

**Application**:
```python
slide_collection.apply_patch(content_generation_patch)
# Result: slides with full content, state = active
```

---

## LLM Prompt Templates

### System Prompt (Step 1 - State Transition)
```
You are a presentation structure designer specializing in layout strategy selection.

Your task: Analyze atoms and user instructions to determine:
1. Number of slides needed
2. Layout strategy for each slide (Bento.Standard, Swiss.Asymmetry, etc.)
3. Logical slide ordering

Output JSON Patch operations to initialize slides in "draft" state.

Available Layout Strategies:
- Bento.Standard: 6-cell grid, balanced content
- Bento.HeroTop: Hero at top, 3 footer cells
- Bento.HeroLeft: Hero left, 3 right cells
- Bento.Quarter: 4 equal cells
- Swiss.Poster: Single large headline
- Swiss.Asymmetry: Asymmetric content placement
- Swiss.SplitTypo: Split typography layout
- Cinematic.Split_50_50: Two equal halves
- Cinematic.Split_30_70: 30% sidebar, 70% stage
- Cinematic.Fullbleed: Full-screen content
- Focus.Solar_System: Central node + orbiting satellites
- Data.KPI_Row: Horizontal metrics row
- Edit.Magazine_Collage: Overlapping stickers
- Edit.Overlap_Left: Background + overlapping card

**Output Format**: JSON Patch array with "add" operations for slides.
```

### System Prompt (Step 2 - Content Generation)
```
You are a presentation content generator specializing in layout-driven design.

Your task: Populate slide content using atoms while strictly adhering to layout schema.

**CRITICAL CONSTRAINTS**:
1. Use ONLY widget types listed in schema (Type.*, Data.*, Media.*)
2. Match required slots for assigned strategy (e.g., Bento.Standard needs cell_1 through cell_6)
3. Derive text content from provided atoms (don't invent facts)
4. Use valid preset combinations (surface, shape, fill, effect)
5. Set state to "active" after populating content

**Widget Type Schemas**:

Type.Display: {"type": "Type.Display", "parameters": {"text": str}}
Type.Heading: {"type": "Type.Heading", "parameters": {"text": str, "level": 1-6}}
Type.Body: {"type": "Type.Body", "parameters": {"text": str}}
Type.Quote: {"type": "Type.Quote", "parameters": {"text": str, "citation": str}}
Type.List: {"type": "Type.List", "parameters": {"items": [str], "list_type": "ordered"|"unordered"}}

Data.BigNum: {"type": "Data.BigNum", "parameters": {"number": float, "label": str, "format": "integer"|"decimal"|"percentage"}}
Data.Progress: {"type": "Data.Progress", "parameters": {"percentage": 0-100, "label": str}}
Data.Trend: {"type": "Data.Trend", "parameters": {"value": float, "change": float, "direction": "up"|"down"|"flat", "label": str}}

**Preset Schema**: {"surface": str, "shape": str, "fill": str, "effect": str} (all optional)

**Output Format**: JSON Patch array with "replace" operations for widgets and state.
```

### User Prompt Template (Combined)
```
Step {step_number} of 2: {step_name}

Atoms Available:
{atoms_json}

User Instructions:
{user_instruction}

{step_specific_instructions}

Output JSON Patch operations only. No explanations.
```

## Error Responses

### State Transition Error
```json
{
  "error": "StateTransitionError",
  "message": "Invalid state transition: active → draft",
  "details": {
    "slide_id": "slide_001",
    "current_state": "active",
    "attempted_state": "draft",
    "valid_transitions": ["initial → draft", "draft → active"]
  }
}
```

### Schema Validation Error
```json
{
  "error": "ValidationError",
  "message": "Unsupported widget attribute: background_color",
  "details": {
    "slide_id": "slide_001",
    "widget_id": "cell_1",
    "invalid_attribute": "background_color",
    "supported_attributes": ["type", "parameters", "preset"]
  }
}
```

## Caching Contract

### Cache Key Computation
```python
cache_key = SHA256(
    atoms.to_dict().__str__() +
    user_instruction +
    config.system_prompt +
    config.model +
    str(config.temperature)
).hexdigest()
```

### Cache Storage
```python
cache.set(
    cache_key=cache_key,
    data=slide_collection.to_dict(),
    metadata=CacheMetadata(
        model=config.model,
        temperature=config.temperature,
        created_at=datetime.now(),
        source_files=atoms.source_ids,
        prompt_template_hash=SHA256(config.system_prompt).hexdigest()
    )
)
```

## Example Usage

```python
from src.generation.content import generate_layout
from src.generation.atom import extract_atoms

# Extract atoms first
atoms = extract_atoms(source, atom_config)

# Generate layout
instruction = "Create 5 slides: overview, features, comparison, process, conclusion"
layout_config = GenerationConfig(
    model="gpt-4-turbo",
    temperature=0.7,
    max_tokens=8000,
    system_prompt=LAYOUT_SYSTEM_PROMPT,
    user_prompt_template=LAYOUT_USER_TEMPLATE
)

slides = generate_layout(atoms, instruction, layout_config, use_cache=True)

# Access results
for slide in slides.slides:
    print(f"Slide {slide.slide_id}: {slide.strategy} - {slide.state}")
    for widget_id, widget in slide.widgets.items():
        print(f"  {widget_id}: {widget['type']}")
```

## Performance Expectations

- **Cache hit**: <100ms
- **Cache miss (full generation)**: <30s for 10-slide presentation
- **Step 1 (state transition)**: <5s
- **Step 2 (content generation)**: <25s
- **Token usage**: ~3x atom tokens (context + output)
- **Retry logic**: 3 attempts with exponential backoff

## Validation Rules

1. All slides MUST progress through state transitions: initial → draft → active
2. All widget types MUST be from supported schema
3. All preset attributes MUST be valid values
4. Strategy-required slots MUST be populated (e.g., Bento.Standard needs cell_1-6)
5. Content MUST derive from atoms (no hallucinated facts)
6. Patches MUST be valid JSON Patch (RFC 6902) format
7. Active slides MUST have non-empty widget content
