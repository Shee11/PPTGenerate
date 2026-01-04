# Research: MDX Direct Output

## Current Architecture

### State Management (state.json)
**Location**: `src/common/slides.py`

Current slide schema:
```python
{
  "id": str,           # e.g., "slide_01"
  "rank": int,         # Ordering
  "state": "draft"|"active",
  "story": str,        # Narrative arc position
  "atoms": List[str],  # Referenced atom IDs
  "density": "minimal"|"moderate"|"dense",
  "layout": str,       # e.g., "split", "cover", "grid"
  "widgets": Dict[str, Dict],  # Slot → widget JSON mapping
  "parameters": Dict   # Layout parameters
}
```

### JSON Widget Format
```json
{
  "type": "Type.Display|Data.BigNum|Type.List|...",
  "parameters": {
    "text": "...",
    "items": ["..."],
    "value": "42%"
  }
}
```

### Two-Step Conversion Pipeline
1. **LLM** → JSON widgets
2. **ReactMDXRenderer** → MDX string

**Location**: `src/paged/render/react/mdx_renderer.py` (2844 lines)

Key mappings:
- `WIDGET_TYPE_MAP`: JSON type → React component
- `LAYOUT_TYPE_MAP`: layout string → Layout component

## Decision: MDX-in-JSON Approach

**Chosen**: Store raw MDX string in `mdx` field, replacing `widgets` for react-mdx projects.

**Rationale**:
- JSON patch still works for metadata (rank, story, atoms)
- LLM generates native MDX (leverages JSX training data)
- Renderer receives MDX directly, no conversion needed
- Human-editable content

**Rejected Alternatives**:
- Full MDX files with frontmatter: Too much architectural change
- Keep JSON + prompt MDX examples: Doesn't eliminate conversion

## New Slide Schema (for react-mdx)

```python
{
  "id": str,
  "rank": int,
  "story": str,
  "atoms": List[str],
  "mdx": str,  # NEW: Raw MDX markup
  # widgets field removed for react-mdx
}
```

## Patch Format for Refinement

**New format**: XML-style patch blocks in LLM output
```xml
<Patch id="stat_001">
  <BigNum value="95%" label="Uptime" trend="+5%"/>
</Patch>
```

**Why not JSON patch?**:
- MDX content is already markup
- Patches should match output format
- Easier for LLM to generate consistent format

**Patch Application**:
1. Parse `<Patch id="...">` blocks from LLM response
2. Find element with matching `id` attribute in slide MDX
3. Replace element content with patch content
4. Preserve surrounding MDX structure

## Component Inventory

| Layer | Components |
|-------|------------|
| L1 Layouts | LayoutCover, LayoutSplit, LayoutGrid, LayoutStacked, LayoutFullBleed, LayoutTimeline, LayoutDashboard |
| L2 Blocks | SmartList, BigNum, MetricGroup, MetricStrip, MetricCard, MetricBadges, ChartBar, ChartLine, ChartPie, QuoteBlock, ImageBlock, TableData, CardGroup |
| L3 Atoms | Heading, Text, Callout |

## Impact Analysis

### Files to Modify

1. **`src/generation/content/prompts.py`**
   - Update system prompt for MDX output format
   - Remove JSON schema, add MDX component reference
   - Add Patch format instructions for refinement

2. **`src/paged/layout/react/layout_engine.py`**
   - Update `get_layout_prompt()` to show MDX syntax
   - Remove TypeScript interface definitions

3. **`src/generation/content/generator.py`**
   - Add MDX parsing logic (extract slides from MDX blocks)
   - Add Patch parser for refinement responses
   - Route to MDX or JSON based on project type

4. **`src/common/slides.py`**
   - Add `mdx` field to Slide schema
   - Add MDX patch application logic

5. **`src/paged/render/react/mdx_renderer.py`**
   - Simplify to read `mdx` field directly
   - Skip JSON-to-MDX conversion when `mdx` present

### Backward Compatibility

- `project=slidev`: Unchanged (JSON output)
- `project=react-mdx`: New MDX output
- Existing tests continue to work
