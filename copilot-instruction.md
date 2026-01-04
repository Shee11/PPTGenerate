# Copilot Instructions

## Multi-Phase Generation Architecture (FUNDAMENTAL DESIGN PATTERN)

The slide generation pipeline has **three distinct phases**. Each phase has its own responsibility and prompts must be placed in the correct phase.

### Phase 1: Atom Extraction
**Tool**: `AtomTool` in `src/tools/atoms.py`
**Input**: Source document (markdown, text)
**Output**: `AtomCollection` with extracted content units (stats, quotes, facts, lists, etc.)

**Responsibility**: Parse source content into atomic, reusable content units.

### Phase 2: Story Planning  
**Tool**: `StoryTool` in `src/tools/story.py`
**Generator**: `src/generation/content/story_generator.py`
**Input**: AtomCollection + user instruction
**Output**: Draft slides with `story` and `visual_design` fields populated

**Responsibility**: 
- Plan narrative arc across slides (Hook → Context → Journey → Insight → Close)
- Decide WHAT story each slide tells (HEADLINE, NARRATIVE, EVIDENCE, TAKEAWAY)
- Define HOW to visualize each slide (layout hints, visual emphasis, diagram needs)

**The `story` field must contain**:
```
HEADLINE: Conclusion-first title stating the insight
NARRATIVE: Why this matters, the speaker's voice
EVIDENCE: What atoms prove this, with context
TAKEAWAY: What audience should remember
```

**The `visual_design` field must contain**:
- Layout concept (split, dashboard, timeline, etc.)
- Element placement (where narrative text goes, where metrics go)
- Diagram needs (flowchart, architecture, etc.)

### Phase 3: Content & Layout Execution
**Tool**: `ContentTool` in `src/tools/content.py`  
**Prompts**: `src/generation/content/prompts.py`
**Input**: Draft slides with `story` + `visual_design` + AtomCollection
**Output**: Active slides with `layout` + `widgets` + `mdx` populated

**Responsibility**:
- Select concrete layout based on `visual_design`
- Populate widgets with atoms to render the `story`
- Render NARRATIVE from story as `<Text variant="lead">` 
- Render TAKEAWAY from story as `<Text variant="caption">` or `<Callout>`
- Fill visual space effectively (no empty areas)

### Critical Rule: Prompts in Correct Phase

| Concern | Correct Phase | Wrong Phase |
|---------|---------------|-------------|
| "Each slide must tell a story" | Story | ❌ Content |
| "Use conclusion-first titles" | Story | ❌ Content |
| "Include narrative before metrics" | Story (in visual_design) | ❌ Content |
| "Fill 75% of visual space" | Content | ❌ Story |
| "Use LayoutDashboard for metrics" | Content | ❌ Story |
| "Diagram nodes should be short" | Content | ❌ Story |

**Anti-pattern**: Adding storytelling requirements to `prompts.py` (content phase).
**Correct pattern**: Storytelling requirements go in `story_generator.py`, content phase just executes the blueprint.

---

## Prompt Update Guidelines

### Rule 1: Update/Merge, Never Append

When modifying prompts in any generation stage:
- **UPDATE** existing sections with new content
- **MERGE** new rules into existing rule lists
- **NEVER append** new sections at the end creating duplicate concepts
- **REMOVE** conflicting or outdated instructions when adding new ones

**Anti-pattern**:
```python
# BAD: Appending creates bloated, contradictory prompts
prompt = existing_prompt + """
## NEW SECTION
New rules that may conflict with existing rules above...
"""
```

**Correct pattern**:
```python
# GOOD: Find and replace the relevant section
# If adding VISUAL SELECTION rules, find existing visual guidance and update it
```

### Rule 2: Length Restriction

| Stage | Max Prompt Lines | Prompt File | Formatter File |
|-------|------------------|-------------|----------------|
| Atom Extraction | ≤50 lines | `src/generation/atom/prompts.py` | - |
| Story Planning | ≤200 lines | `src/generation/content/story_generator.py` | - |
| Content (what) | ≤100 lines | `src/generation/content/prompts.py` | `layout_generator.py` |
| Layout (how) | ≤100 lines | `src/paged/layout/react/layout_engine.py` | `layout_generator.py` |

**Architecture**:
- `prompts.py` → Content prompts (WHAT to say: storytelling, narrative, evidence)
- `layout_engine.py` → Layout prompts (HOW to render: layouts, widgets, MDX syntax)
- `layout_generator.py` → Orchestrator only (composes prompts, NO actual prompt text)

**Why**: Longer prompts dilute key instructions. LLMs follow the most recent/prominent rules, causing earlier rules to be ignored.

### Rule 3: Single Source of Truth

Each concept should appear in ONE place:
- **Density interpretation** → Story stage only
- **Visual selection (diagram vs list)** → Story stage's `visual_design`
- **Layout selection** → Content stage only
- **Widget population** → Content stage only

If you find the same concept in multiple files, consolidate it.

### Rule 4: Module Boundaries

`src/generation/content/` must be **layout-engine agnostic**:
- Should NOT know about MDX, React, Slidev, or any specific rendering format
- Should only deal with abstract concepts: story, atoms, density, visual_design

`src/paged/layout/<engine>/` contains **engine-specific code**:
- `react/` → MDX parsing, React component syntax, layout_engine.py
- Parser files (e.g., `mdx_parser.py`) belong in the engine folder, NOT in `generation/content/`

**TODO**: Move `src/generation/content/mdx_parser.py` → `src/paged/layout/react/mdx_parser.py`

---

## Python Environment

Always use `.venv\Scripts\python.exe` instead of `python` when running Python commands:

```powershell
.venv\Scripts\python.exe -m cli.uce_render ...
```

## HTTP Server for Slidev Viewing

When testing Slidev output:
1. **Do NOT start a new HTTP server** - assume one is already running on port 8080
2. Server typically serves from `output/<project>/dist`
3. If no server is running, user will start it manually

## Chrome MCP for Web Testing

When verifying rendered slides or web pages:
1. **Always open the page first** using `mcp_io_github_chr_new_page` before taking snapshots
2. Use `mcp_io_github_chr_take_snapshot` to capture the page state
3. Use `mcp_io_github_chr_list_pages` to see open pages
4. Do NOT use `open_simple_browser` - use Chrome MCP tools instead

Example flow:
```
1. mcp_io_github_chr_new_page with url http://localhost:8080/
2. mcp_io_github_chr_take_snapshot to verify content
```

## CLI E2E Test Command

When asked to "run e2e cli" or "test e2e" or "regenerate" or "full generation", execute this command:
To regenerate slides from scratch (creates new state.json with fresh content):

```powershell
.venv\Scripts\python.exe -m cli --source "data/context/golden_set.md" --user-instruction-file "data/context/golden_set_instruction_singlestep.md" --project react-mdx --mdx-theme purple --export-html --output "output/golden_set_mdx/"
```

This will:
- Parse the source markdown file
- Use the instruction file to guide LLM content generation
- Create a new state.json with slide content
- Export to HTML

## Re-export with Different Project Theme

To re-export an existing slide with a different project theme (e.g., cyberpunk, duolingo):

1. **Add/update `project` field** at the top of `state.json`:
   ```json
   {
     "project": "cyberpunk",
     "todos": { ... }
   }
   ```

2. **Override todos to keep only export** - remove all other todos and keep only export with no dependencies:
   ```json
   {
     "project": "cyberpunk",
     "todos": {
       "todos": [
         {
           "id": "export",
           "type": "export",
           "status": "pending",
           "params": {
             "layout_engine": "slidev",
             "output_format": "html",
             "output_path": null
           },
           "created_at": "2025-12-24T08:20:15.103666",
           "started_at": null,
           "completed_at": null,
           "error": null,
           "depends_on": []
         }
       ]
     },
     "source": { ... }
   }
   ```

3. **Run the CLI**:
   ```powershell
   .venv\Scripts\python.exe -m cli.uce_render --state output/<slide_folder>/state.json --output output/<slide_folder>
   ```

Available project themes:
- `react-mdx` (default) - React MDX components with modern styling
- `duolingo` - Playful Duolingo-style with bright colors
- `cyberpunk` - Futuristic neon aesthetic with glows and HUD frames

**DEPRECATED**: `slidev` - Do not use. Always use `react-mdx` instead.


### Continue from existing state.json (render only)

To re-render an existing state.json without regenerating content:

```powershell
.venv\Scripts\python.exe -m cli --render "output/golden_set_mdx/state.json" --project react-mdx --mdx-theme purple --export-html --output "output/golden_set_mdx/slides_v2.html"
```

This will:
- Load existing state.json (slide content unchanged)
- Re-render using React MDX components
- Export to HTML with current CSS/layout fixes

### Key Files

| File | Purpose |
|------|---------|
| `data/context/golden_set.md` | Source content for slides |
| `data/context/golden_set_instruction_singlestep.md` | User instructions for LLM |
| `output/golden_set_mdx/state.json` | Generated slide state (content) |
| `output/golden_set_mdx/slides.html` | Exported HTML presentation |

### Available MDX Themes
- `purple` - Purple accent color (#7c3aed)
- `blue` - Blue accent
- `green` - Green accent
- `red` - Red accent
- `business` - Professional gray/blue
