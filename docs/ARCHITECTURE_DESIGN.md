# UCE Render - Architecture Design Document

> **Universal Content Engine**: AI-powered presentation generation from source content

## Table of Contents

1. [State Tree](#1-state-tree)
2. [Planner, Executor & Tools](#2-planner-executor--tools)
3. [Tool Operations: Slice, Transform, Patch](#3-tool-operations-slice-transform-patch)
4. [Tool Expansion Roadmap](#4-tool-expansion-roadmap)
5. [Test & Evaluation Framework](#5-test--evaluation-framework)

---

## 1. State Tree

The state tree is the single source of truth for the entire pipeline. It represents the complete snapshot of the system at any point in time.

### 1.1 State Schema

```
State
├── meta
│   ├── id: string                    # Unique state identifier
│   ├── created_at: datetime          # Creation timestamp
│   ├── updated_at: datetime          # Last modification timestamp
│   └── version: string               # Schema version for migrations
│
├── source
│   ├── path: string                  # Source file path (VTT, TXT, MD, etc.)
│   ├── content_hash: string          # SHA256 hash for change detection
│   ├── content_type: string          # MIME type or content classifier
│   └── content: string | null        # Cached content (optional)
│
├── constitution
│   ├── tone: string                  # "professional", "casual", "academic"
│   ├── target_slides: int | null     # Target slide count
│   ├── style_rules: List[string]     # User-defined constraints
│   ├── content_exclusions: List[str] # Topics to exclude
│   ├── selected_theme: string | null # User-selected theme ID
│   └── selected_vibe: string | null  # User-selected vibe
│
├── themes
│   └── {theme_id}: Theme             # Theme registry (dict of theme objects)
│       ├── id: string
│       ├── name: string
│       ├── typography: TypographyConfig
│       ├── colors: ColorPalette
│       ├── font_family: string
│       ├── heading_font: string
│       └── decorations: Dict
│
├── active_theme_id: string           # Currently active theme
├── project: string                   # Slidev project: "slidev", "duolingo", "cyberpunk", etc.
│
├── atoms
│   ├── id: string                    # Collection identifier
│   ├── model: string                 # "FactAtom" - atom model version
│   └── contexts: List[Atom]          # Extracted atoms
│       └── Atom
│           ├── id: string            # "bio_001", "stat_002"
│           ├── type: AtomType        # BIO, FACT, STAT, QUOTE, TENSION, CONCEPT, VISUAL
│           ├── rank: int             # Importance score (1-10)
│           ├── state: string         # "draft", "active", "excluded"
│           ├── abstract: string      # One-line summary
│           ├── content: Dict         # Type-specific payload
│           └── metadata: Dict        # Source reference, timestamps
│
├── slides
│   └── List[Slide]                   # Generated slides
│       └── Slide
│           ├── slide_number: int
│           ├── title: string
│           ├── story: string         # Narrative purpose
│           ├── visual_design: string # Design intent
│           ├── layout: string        # Layout template name
│           ├── atoms: List[string]   # Referenced atom IDs
│           ├── widgets: List[Widget] # UI components
│           ├── theme: string         # Theme ID for this slide
│           └── vibe: string          # Visual vibe
│
├── todos
│   └── TodoQueue                     # Task queue
│       ├── items: List[TodoItem]
│       └── TodoItem
│           ├── id: string
│           ├── type: TodoType        # CONSTITUTION, ATOMS, THEME, STORY, CONTENT, EXPORT
│           ├── status: TodoStatus    # PENDING, IN_PROGRESS, COMPLETED, FAILED
│           ├── params: Dict          # Tool-specific parameters
│           ├── dependencies: List[str]
│           ├── created_at: datetime
│           └── completed_at: datetime | null
│
└── status: string                    # Pipeline status: "pending", "complete", "error"
```

### 1.2 State Transitions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STATE LIFECYCLE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   INIT ──────► SOURCE ──────► ATOMS ──────► STORY ──────► CONTENT ──────► EXPORT
│    │            │               │             │              │               │
│    │            │               │             │              │               │
│    ▼            ▼               ▼             ▼              ▼               ▼
│  state.json  source.*       atoms.json    slides[]       slides[]      dist/
│  created     loaded         extracted     (draft)        (active)      index.html
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 State Invariants

| Invariant | Description |
|-----------|-------------|
| **Source Immutability** | Once set, source.content_hash never changes in a session |
| **Atom Referential Integrity** | slides[].atoms[] must reference valid atoms.contexts[].id |
| **Theme Availability** | active_theme_id must exist in themes registry |
| **Todo Ordering** | Todos execute only when all dependencies are COMPLETED |
| **Idempotent Apply** | Running apply(state, patch) twice produces same result |

---

## 2. Planner, Executor & Tools

### 2.1 Three-Layer Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              USER LAYER                                      │
│    User Instruction: "Create 10 slides from this transcript with duolingo   │
│                       style, exclude Q&A section"                           │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            PLANNER LAYER                                     │
│                                                                              │
│   ┌─────────────┐    ┌──────────────────┐    ┌─────────────────────┐        │
│   │   STATE     │───►│   LLM PLANNER    │───►│   TODO QUEUE        │        │
│   │   SLICER    │    │                  │    │                     │        │
│   └─────────────┘    │  • Tool catalog  │    │  1. constitution    │        │
│                      │  • State context │    │  2. atoms           │        │
│                      │  • User intent   │    │  3. theme           │        │
│                      └──────────────────┘    │  4. story           │        │
│                                              │  5. content         │        │
│                                              │  6. export          │        │
│                                              └─────────────────────┘        │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           EXECUTOR LAYER                                     │
│                                                                              │
│   while has_pending_todos():                                                 │
│       todo = get_next_ready_todo()  # Respects dependencies                 │
│       tool = get_tool(todo.type)                                            │
│       execute(tool, state, todo.params, instruction)                        │
│                                                                              │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                             TOOL LAYER                                       │
│                                                                              │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│   │CONSTITUTION│  │   ATOMS    │  │   THEME    │  │   STORY    │            │
│   │   TOOL     │  │   TOOL     │  │   TOOL     │  │   TOOL     │            │
│   └────────────┘  └────────────┘  └────────────┘  └────────────┘            │
│                                                                              │
│   ┌────────────┐  ┌────────────┐                                            │
│   │  CONTENT   │  │   EXPORT   │                                            │
│   │   TOOL     │  │   TOOL     │                                            │
│   └────────────┘  └────────────┘                                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Planner Details

The planner is an LLM-based system that converts user instructions into a structured todo queue.

```python
class Planner:
    """
    Converts user instruction + current state into TodoQueue
    """
    
    def plan(self, state: State, instruction: str) -> TodoQueue:
        # 1. Build context
        state_slice = self.slice_state_for_planning(state)
        tool_catalog = get_all_tool_descriptions()
        
        # 2. Construct prompt
        system_prompt = f"""
        You are a presentation pipeline planner.
        
        Available Tools:
        {tool_catalog}
        
        Current State:
        {state_slice}
        """
        
        user_prompt = f"Plan todos for: {instruction}"
        
        # 3. LLM generates JSON todo list
        response = llm.generate(system_prompt, user_prompt)
        
        # 4. Parse and validate
        return self.parse_todo_queue(response)
```

**Planning Strategies:**

| Strategy | Trigger | Todo Sequence |
|----------|---------|---------------|
| Full Pipeline | New source, no atoms | constitution → atoms → theme → story → content → export |
| Regenerate | "regenerate slides" | story → content → export |
| Theme Change | "change to cyberpunk" | theme → export |
| Content Update | "add more stats" | content (selective) → export |
| Export Only | "export to PDF" | export |

### 2.3 Executor Details

The executor runs the todo queue sequentially, respecting dependencies.

```python
class TodoExecutor:
    """
    Executes todos from queue, managing state persistence
    """
    
    def execute_all(self, state: State, instruction: str):
        while state.has_pending_todos():
            todo = state.get_next_ready_todo()  # None if blocked by deps
            if todo is None:
                raise CyclicDependencyError()
            
            self.execute_one(todo, state, instruction)
            state.persist()  # Checkpoint after each todo
    
    def execute_one(self, todo: TodoItem, state: State, instruction: str):
        tool = self.get_tool(todo.type)
        
        try:
            state.mark_todo_started(todo.id)
            
            # TOOL PROTOCOL
            context = tool.slice(state, todo.params)
            patch = tool.generate(state.constitution, context, instruction)
            tool.apply(state, patch)
            
            state.mark_todo_completed(todo.id)
        except Exception as e:
            state.mark_todo_failed(todo.id, str(e))
            raise
```

### 2.4 Tool Registration & Discovery

Tools self-register with metadata for planner discovery:

```python
@register_tool
class AtomsTool(BaseTool):
    name = "atoms"
    description = "Extract structured facts from source content"
    triggers = ["extract facts", "analyze content", "find key points"]
    parameters = {
        "source_type": "Type of source: transcript, article, notes",
        "focus_areas": "Areas to prioritize in extraction"
    }
    requires = ["constitution"]
    produces = ["atoms"]
    examples = [
        {"type": "atoms", "params": {"source_type": "transcript"}}
    ]
```

---

## 3. Tool Operations: Slice, Transform, Patch

### 3.1 The Tool Protocol

Every tool follows the **Slice → Transform → Patch** pattern:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TOOL PROTOCOL                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    STATE                    TOOL                         STATE'         │
│   ┌──────┐               ┌────────┐                    ┌──────┐        │
│   │      │   SLICE       │        │                    │      │        │
│   │  S   │──────────────►│Context │                    │  S'  │        │
│   │      │               │        │                    │      │        │
│   │      │               │        │   TRANSFORM        │      │        │
│   │      │               │        │──────────────┐     │      │        │
│   │      │               │        │              │     │      │        │
│   │      │               └────────┘              │     │      │        │
│   │      │                                       ▼     │      │        │
│   │      │               ┌────────┐         ┌────────┐│      │        │
│   │      │               │        │         │        ││      │        │
│   │      │◄──────────────│ Patch  │◄────────│  LLM   ││      │        │
│   │      │    APPLY      │        │         │        ││      │        │
│   │      │               └────────┘         └────────┘│      │        │
│   └──────┘                                            └──────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Slice Operation

**Purpose:** Extract minimal relevant context from state for tool execution.

**Benefits:**
- Reduces LLM token usage
- Focuses tool on relevant data
- Enables parallel execution (non-overlapping slices)

```python
class SliceOperation:
    """
    Extracts tool-specific context from state
    """
    
    # ATOMS TOOL SLICE
    def slice_for_atoms(self, state: State, params: AtomsParams) -> AtomsContext:
        return AtomsContext(
            source=state.source,
            intent_guidance=params.focus_areas,
            existing_atoms=None  # Fresh extraction
        )
    
    # CONTENT TOOL SLICE
    def slice_for_content(self, state: State, params: ContentParams) -> ContentContext:
        slide_idx = params.slide_indices
        return ContentContext(
            draft_slides=state.slides[slide_idx],
            context_before=state.slides[max(0, slide_idx-2):slide_idx],
            context_after=state.slides[slide_idx+1:slide_idx+3],
            atoms_collection=self._filter_atoms(state.atoms, params.atom_filter),
            theme=state.get_theme(state.active_theme_id),
            available_layouts=self._get_layouts_for_project(state.project)
        )
```

**Slice Patterns by Tool:**

| Tool | Slice Contents | Size Reduction |
|------|---------------|----------------|
| constitution | instruction only | 100% reduction |
| atoms | source.content | ~0% (needs full source) |
| theme | available_themes, user preferences | ~95% reduction |
| story | atoms (abstract only), slide_count | ~80% reduction |
| content | 1 slide + 2 neighbors + filtered atoms | ~90% reduction |
| export | slides + active_theme | ~70% reduction |

### 3.3 Transform Operation

**Purpose:** Generate new data using LLM or deterministic logic.

**Two Types:**

```python
# TYPE 1: LLM Transform (GenerativeTool)
class GenerativeTool(BaseTool):
    def transform(self, constitution: Constitution, 
                  context: Context, instruction: str) -> Patch:
        prompt = self.build_prompt(constitution, context, instruction)
        response = self.llm.generate(prompt, schema=self.patch_schema)
        return self.parse_patch(response)

# TYPE 2: Direct Transform (DirectTool)  
class DirectTool(BaseTool):
    def transform(self, constitution: Constitution,
                  context: Context, instruction: str) -> Patch:
        # Deterministic logic, no LLM
        return self.compute_patch(context)
```

**Transform Examples:**

```python
# ATOMS TRANSFORM: Extract structured atoms from text
def transform_atoms(context: AtomsContext) -> AtomsPatch:
    """
    Input:  "Chao Wang joined Microsoft in 2011..."
    Output: Atom(id="bio_001", type="BIO", 
                 content={"name": "Chao Wang", "event": "joined Microsoft", "year": "2011"})
    """

# STORY TRANSFORM: Create narrative arc
def transform_story(context: StoryContext) -> StoryPatch:
    """
    Input:  atoms=[bio_001, stat_002, tension_003, ...]
    Output: slides=[
        {story: "Hook - introduce speaker", atoms: ["bio_001"]},
        {story: "Rising action - show problem", atoms: ["tension_003"]},
        ...
    ]
    """

# CONTENT TRANSFORM: Generate visual layout
def transform_content(context: ContentContext) -> ContentPatch:
    """
    Input:  draft_slide={story: "Show key metrics", atoms: ["stat_001", "stat_002"]}
    Output: active_slide={
        layout: "dashboard",
        widgets: [
            {type: "metric-card", atom: "stat_001", position: "top-left"},
            {type: "metric-card", atom: "stat_002", position: "top-right"}
        ]
    }
    """
```

### 3.4 Patch Operation

**Purpose:** Apply generated changes to state immutably.

**Patch Types:**

```python
# MERGE PATCH - Add/update fields
class MergePatch:
    """Merges new data into existing state"""
    def apply(self, state: State, patch: Dict):
        state.constitution.merge(patch.constitution)
        # Does not delete existing fields

# REPLACE PATCH - Full replacement
class ReplacePatch:
    """Replaces entire section"""
    def apply(self, state: State, patch: AtomsPatch):
        state.atoms = patch.collection
        # Replaces all atoms

# SELECTIVE PATCH - Update specific items
class SelectivePatch:
    """Updates specific items by ID"""
    def apply(self, state: State, patch: ContentPatch):
        for slide_patch in patch.slides:
            idx = slide_patch.slide_number - 1
            state.slides[idx] = slide_patch
```

**Patch Application Rules:**

| Patch Type | Behavior | Idempotent? |
|------------|----------|-------------|
| Constitution | Merge with existing | Yes |
| Atoms | Replace collection | Yes |
| Theme | Add/update in registry | Yes |
| Story | Replace slides array | Yes |
| Content | Update specific slides | Yes |
| Export | Write to filesystem | Yes (overwrite) |

### 3.5 Tool Summary Table

| Tool | Slice | Transform | Patch |
|------|-------|-----------|-------|
| **constitution** | instruction | Pattern matching | Merge rules |
| **atoms** | source.content | LLM extraction | Replace atoms |
| **theme** | theme registry | Load or LLM generate | Add to registry |
| **story** | atoms (abstract) | LLM narrative planning | Replace slides |
| **content** | slide + neighbors | LLM layout generation | Update slides |
| **export** | slides + theme | Template rendering | Write files |

---

## 4. Tool Expansion Roadmap

### 4.1 Current vs. Future Tool Scope

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TOOL EXPANSION ROADMAP                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CURRENT                           FUTURE                                   │
│  ───────                           ──────                                   │
│                                                                             │
│  ┌─────────┐                      ┌─────────────────────────────────────┐  │
│  │  ATOMS  │ ─────────────────►   │            ATOMS                    │  │
│  │(source) │                      │  ├── Source Parser                  │  │
│  └─────────┘                      │  ├── Web Search                     │  │
│                                   │  ├── Enterprise Search (RAG)        │  │
│                                   │  └── Real-time Data Fetch           │  │
│                                   └─────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────┐                      ┌─────────────────────────────────────┐  │
│  │  THEME  │ ─────────────────►   │            THEME                    │  │
│  │ (load)  │                      │  ├── Theme Loader                   │  │
│  └─────────┘                      │  ├── Theme Creator (LLM)            │  │
│                                   │  ├── Vibe Generator                 │  │
│                                   │  └── Template Synthesizer           │  │
│                                   └─────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────┐                      ┌─────────────────────────────────────┐  │
│  │  STORY  │ ─────────────────►   │            STORY                    │  │
│  │  (arc)  │                      │  ├── Narrative Planner              │  │
│  └─────────┘                      │  ├── Content Writer                 │  │
│                                   │  └── Visual Designer                │  │
│                                   └─────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────┐                      ┌─────────────────────────────────────┐  │
│  │ CONTENT │ ─────────────────►   │           CONTENT                   │  │
│  │(layout) │                      │  ├── Text Generator                 │  │
│  └─────────┘                      │  ├── Image Prompt Generator         │  │
│                                   │  ├── Chart/Diagram Generator        │  │
│                                   │  └── Animation Sequencer            │  │
│                                   └─────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────┐                      ┌─────────────────────────────────────┐  │
│  │ EXPORT  │ ─────────────────►   │            EXPORT                   │  │
│  │ (html)  │                      │  ├── HTML (Slidev)                  │  │
│  └─────────┘                      │  ├── PPTX (python-pptx)             │  │
│                                   │  ├── PDF (puppeteer)                │  │
│                                   │  ├── Video (ffmpeg)                 │  │
│                                   │  └── Figma (API)                    │  │
│                                   └─────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Atoms Expansion

#### 4.2.1 Web Search Integration

```python
@register_tool
class WebSearchTool(BaseTool):
    """
    Enrich atoms with web-sourced information
    """
    name = "websearch"
    requires = ["atoms"]
    produces = ["atoms.enriched"]
    
    def slice(self, state: State, params: WebSearchParams) -> WebSearchContext:
        return WebSearchContext(
            atoms_to_enrich=[a for a in state.atoms if a.needs_enrichment],
            search_queries=params.queries,
            max_results_per_query=params.max_results
        )
    
    def transform(self, context: WebSearchContext) -> WebSearchPatch:
        enriched = []
        for atom in context.atoms_to_enrich:
            # Generate search query from atom
            query = self.atom_to_query(atom)
            
            # Search web
            results = self.search_engine.search(query)
            
            # Enrich atom with findings
            atom.metadata["web_sources"] = results
            atom.content["enriched_data"] = self.extract_relevant(results, atom)
            enriched.append(atom)
        
        return WebSearchPatch(enriched_atoms=enriched)
```

#### 4.2.2 Enterprise Search (RAG)

```python
@register_tool
class EnterpriseSearchTool(BaseTool):
    """
    Search internal knowledge bases for supporting content
    """
    name = "enterprise_search"
    requires = ["atoms"]
    produces = ["atoms.enterprise_context"]
    
    def transform(self, context: EnterpriseContext) -> EnterprisePatch:
        # Connect to vector store
        vectordb = self.get_enterprise_vectordb()
        
        for atom in context.atoms:
            # Semantic search in enterprise docs
            similar_docs = vectordb.similarity_search(
                atom.abstract,
                filter={"department": context.department}
            )
            
            # Add enterprise context
            atom.metadata["enterprise_refs"] = similar_docs
        
        return EnterprisePatch(atoms=context.atoms)
```

### 4.3 Theme Expansion

#### 4.3.1 Theme Creator (LLM-based)

```python
@register_tool
class ThemeCreatorTool(GenerativeTool):
    """
    Generate new themes from description or reference images
    """
    name = "theme_creator"
    produces = ["themes"]
    
    def transform(self, context: ThemeCreatorContext) -> ThemePatch:
        if context.reference_image:
            # Extract colors and style from image
            style_analysis = self.vision_model.analyze(context.reference_image)
            prompt = f"Create theme based on: {style_analysis}"
        else:
            prompt = f"Create theme for: {context.description}"
        
        theme_json = self.llm.generate(prompt, schema=ThemeSchema)
        return ThemePatch(theme=Theme.from_json(theme_json))
```

#### 4.3.2 Vibe Generator

```python
@register_tool  
class VibeGeneratorTool(GenerativeTool):
    """
    Generate visual vibe variations on a base theme
    """
    name = "vibe_generator"
    requires = ["theme"]
    produces = ["vibes"]
    
    VIBE_DIMENSIONS = [
        "energy",      # calm ↔ energetic
        "formality",   # casual ↔ formal
        "density",     # minimal ↔ dense
        "mood",        # serious ↔ playful
    ]
    
    def transform(self, context: VibeContext) -> VibePatch:
        base_theme = context.theme
        vibes = []
        
        for dimension in self.VIBE_DIMENSIONS:
            for level in ["low", "medium", "high"]:
                vibe = self.generate_vibe(base_theme, dimension, level)
                vibes.append(vibe)
        
        return VibePatch(vibes=vibes)
```

### 4.4 Story Expansion (Content + Visual Design)

#### 4.4.1 Content Writer

```python
@register_tool
class ContentWriterTool(GenerativeTool):
    """
    Generate rich text content for slides
    """
    name = "content_writer"
    requires = ["story"]
    produces = ["slides.content"]
    
    def transform(self, context: ContentWriterContext) -> ContentWriterPatch:
        for slide in context.draft_slides:
            # Generate headline
            slide.headline = self.generate_headline(
                slide.story, 
                context.constitution.tone
            )
            
            # Generate body text
            slide.body = self.generate_body(
                slide.atoms,
                slide.story,
                max_words=context.constitution.density
            )
            
            # Generate speaker notes
            slide.notes = self.generate_notes(slide)
        
        return ContentWriterPatch(slides=context.draft_slides)
```

#### 4.4.2 Visual Designer

```python
@register_tool
class VisualDesignerTool(GenerativeTool):
    """
    Plan visual hierarchy and composition
    """
    name = "visual_designer"
    requires = ["story"]
    produces = ["slides.visual_design"]
    
    def transform(self, context: VisualDesignContext) -> VisualDesignPatch:
        for slide in context.draft_slides:
            # Analyze content complexity
            complexity = self.analyze_complexity(slide)
            
            # Choose layout strategy
            slide.visual_design = {
                "layout_type": self.recommend_layout(complexity),
                "focal_point": self.determine_focal_point(slide),
                "visual_hierarchy": self.plan_hierarchy(slide),
                "whitespace_strategy": self.plan_whitespace(complexity),
                "color_emphasis": self.plan_color_use(slide, context.theme)
            }
        
        return VisualDesignPatch(slides=context.draft_slides)
```

### 4.5 Content Expansion (Text + Image Prompts)

#### 4.5.1 Text Generator

```python
@register_tool
class TextGeneratorTool(GenerativeTool):
    """
    Generate and refine text content for widgets
    """
    name = "text_generator"
    requires = ["content"]
    produces = ["slides.widgets.text"]
    
    TEXT_TYPES = {
        "headline": {"max_words": 8, "style": "impactful"},
        "subhead": {"max_words": 15, "style": "clarifying"},
        "bullet": {"max_words": 12, "style": "scannable"},
        "stat_label": {"max_words": 4, "style": "descriptive"},
        "quote": {"max_words": 30, "style": "conversational"},
        "caption": {"max_words": 20, "style": "informative"},
    }
    
    def transform(self, context: TextGenContext) -> TextGenPatch:
        for widget in context.widgets:
            text_type = self.classify_text_need(widget)
            config = self.TEXT_TYPES[text_type]
            
            widget.text = self.generate_text(
                atom=context.get_atom(widget.atom_id),
                style=config["style"],
                max_words=config["max_words"],
                tone=context.constitution.tone
            )
        
        return TextGenPatch(widgets=context.widgets)
```

#### 4.5.2 Image Prompt Generator

```python
@register_tool
class ImagePromptTool(GenerativeTool):
    """
    Generate DALL-E/Midjourney prompts for slide imagery
    """
    name = "image_prompt"
    requires = ["content"]
    produces = ["slides.widgets.image_prompts"]
    
    def transform(self, context: ImagePromptContext) -> ImagePromptPatch:
        prompts = []
        
        for slide in context.slides:
            if slide.needs_image:
                prompt = self.generate_prompt(
                    slide_story=slide.story,
                    visual_design=slide.visual_design,
                    theme=context.theme,
                    aspect_ratio=self.get_aspect_ratio(slide.layout)
                )
                
                prompts.append(ImagePrompt(
                    slide_id=slide.slide_number,
                    widget_id=slide.image_widget_id,
                    prompt=prompt,
                    negative_prompt=self.generate_negative_prompt(context.theme),
                    style_reference=context.theme.image_style
                ))
        
        return ImagePromptPatch(prompts=prompts)
```

### 4.6 Export Expansion

#### 4.6.1 Multi-Format Export Architecture

```python
class ExportManager:
    """
    Unified export interface for multiple formats
    """
    
    EXPORTERS = {
        "html": SlidevExporter,      # Current - Slidev + Vue
        "pptx": PowerPointExporter,  # python-pptx
        "pdf": PDFExporter,          # Puppeteer/Playwright
        "video": VideoExporter,      # FFmpeg + TTS
        "figma": FigmaExporter,      # Figma API
    }
    
    def export(self, state: State, format: str, options: ExportOptions):
        exporter = self.EXPORTERS[format](options)
        return exporter.export(state)
```

#### 4.6.2 PowerPoint Exporter

```python
@register_tool
class PowerPointExportTool(DirectTool):
    """
    Export to native PowerPoint format
    """
    name = "export_pptx"
    requires = ["slides"]
    produces = ["output_pptx"]
    
    def transform(self, context: ExportContext) -> ExportPatch:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        
        for slide_data in context.slides:
            layout = self.get_pptx_layout(slide_data.layout)
            slide = prs.slides.add_slide(layout)
            
            # Map widgets to PowerPoint shapes
            for widget in slide_data.widgets:
                self.add_widget_to_slide(slide, widget, context.theme)
        
        output_path = context.output_dir / "presentation.pptx"
        prs.save(output_path)
        
        return ExportPatch(output_path=output_path, format="pptx")
```

#### 4.6.3 Video Exporter

```python
@register_tool
class VideoExportTool(DirectTool):
    """
    Export to video with narration
    """
    name = "export_video"
    requires = ["slides", "export_html"]
    produces = ["output_video"]
    
    def transform(self, context: VideoExportContext) -> VideoExportPatch:
        frames = []
        audio_segments = []
        
        for slide in context.slides:
            # Capture slide as frame
            frame = self.capture_slide_frame(
                html_path=context.html_path,
                slide_number=slide.slide_number
            )
            frames.append(frame)
            
            # Generate TTS for speaker notes
            if slide.speaker_notes:
                audio = self.text_to_speech(
                    text=slide.speaker_notes,
                    voice=context.voice_config
                )
                audio_segments.append(audio)
        
        # Combine with FFmpeg
        video_path = self.render_video(
            frames=frames,
            audio=audio_segments,
            transitions=context.transitions,
            output_path=context.output_dir / "presentation.mp4"
        )
        
        return VideoExportPatch(output_path=video_path, format="mp4")
```

### 4.7 Expansion Summary

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      TOOL EXPANSION MATRIX                                   │
├──────────┬───────────────────────────────────────────────────────────────────┤
│ DOMAIN   │ CURRENT          │ PLANNED                                       │
├──────────┼──────────────────┼───────────────────────────────────────────────┤
│ ATOMS    │ Source Parser    │ + Web Search, Enterprise RAG, Real-time API   │
├──────────┼──────────────────┼───────────────────────────────────────────────┤
│ THEME    │ Theme Loader     │ + Theme Creator, Vibe Generator, Template Syn │
├──────────┼──────────────────┼───────────────────────────────────────────────┤
│ STORY    │ Narrative Arc    │ + Content Writer, Visual Designer             │
├──────────┼──────────────────┼───────────────────────────────────────────────┤
│ CONTENT  │ Layout Generator │ + Text Gen, Image Prompts, Charts, Animation  │
├──────────┼──────────────────┼───────────────────────────────────────────────┤
│ EXPORT   │ HTML (Slidev)    │ + PPTX, PDF, Video, Figma                     │
└──────────┴──────────────────┴───────────────────────────────────────────────┘
```

---

## 5. Test & Evaluation Framework

### 5.1 State-Based Testing Philosophy

Testing in a state-machine architecture focuses on state transitions:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        STATE-BASED TESTING MODEL                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    Test Input              System Under Test           Expected Output      │
│   ┌──────────┐            ┌──────────────┐           ┌──────────────┐      │
│   │Instruction│            │              │           │              │      │
│   │    +     │───────────►│   PLANNER    │──────────►│ state.todos  │      │
│   │  State   │            │              │           │              │      │
│   └──────────┘            └──────────────┘           └──────────────┘      │
│                                                                             │
│   ┌──────────┐            ┌──────────────┐           ┌──────────────┐      │
│   │  State   │            │              │           │              │      │
│   │    +     │───────────►│   EXECUTOR   │──────────►│    State'    │      │
│   │  Todos   │            │              │           │              │      │
│   └──────────┘            └──────────────┘           └──────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Test Categories

#### 5.2.1 Unit Tests (Tool Level)

```python
class TestAtomsTool:
    """Test atoms tool in isolation"""
    
    def test_slice_extracts_source(self):
        """Slice should extract source content"""
        state = create_test_state(source={"content": "Test content"})
        tool = AtomsTool()
        
        context = tool.slice(state, AtomsParams())
        
        assert context.source.content == "Test content"
    
    def test_transform_extracts_atoms(self):
        """Transform should produce valid atoms"""
        context = AtomsContext(source=Source(content="John joined in 2020"))
        tool = AtomsTool()
        
        patch = tool.transform(Constitution(), context, "extract facts")
        
        assert len(patch.collection.contexts) > 0
        assert patch.collection.contexts[0].type == AtomType.BIO
    
    def test_apply_updates_state(self):
        """Apply should update state atoms"""
        state = create_test_state()
        patch = AtomsPatch(collection=AtomCollection(contexts=[
            Atom(id="test_001", type=AtomType.FACT, abstract="Test")
        ]))
        tool = AtomsTool()
        
        tool.apply(state, patch)
        
        assert len(state.atoms.contexts) == 1
        assert state.atoms.contexts[0].id == "test_001"
```

#### 5.2.2 Integration Tests (Pipeline Level)

```python
class TestPipeline:
    """Test complete pipeline execution"""
    
    def test_full_pipeline_from_transcript(self):
        """Complete pipeline should produce slides"""
        state = State.create_new()
        state.set_source("test_transcript.vtt")
        
        queue = plan(state, "Create 5 slides from this transcript")
        executor = TodoExecutor()
        executor.execute_all(state)
        
        assert state.status == "complete"
        assert len(state.slides) == 5
        assert all(s.layout for s in state.slides)
    
    def test_theme_change_preserves_content(self):
        """Theme change should not alter slide content"""
        state = create_state_with_slides(5)
        original_content = [s.story for s in state.slides]
        
        queue = plan(state, "Change to cyberpunk theme")
        executor = TodoExecutor()
        executor.execute_all(state)
        
        assert state.active_theme_id == "cyber_neon"
        assert [s.story for s in state.slides] == original_content
```

#### 5.2.3 State Transition Tests

```python
class TestStateTransitions:
    """Test state invariants across transitions"""
    
    @pytest.mark.parametrize("instruction,expected_todos", [
        ("Create slides", ["constitution", "atoms", "story", "content", "export"]),
        ("Change to duolingo", ["theme", "export"]),
        ("Regenerate slides", ["story", "content", "export"]),
        ("Export to PDF", ["export"]),
    ])
    def test_planner_produces_correct_todos(self, instruction, expected_todos):
        """Planner should produce expected todo sequence"""
        state = create_test_state()
        
        queue = plan(state, instruction)
        
        todo_types = [t.type.value for t in queue.items]
        assert todo_types == expected_todos
    
    def test_atom_referential_integrity(self):
        """Slides should only reference existing atoms"""
        state = create_state_with_atoms(["atom_1", "atom_2", "atom_3"])
        
        queue = plan(state, "Create slides")
        executor = TodoExecutor()
        executor.execute_all(state)
        
        atom_ids = {a.id for a in state.atoms.contexts}
        for slide in state.slides:
            for atom_ref in slide.atoms:
                assert atom_ref in atom_ids, f"Slide references non-existent atom: {atom_ref}"
```

### 5.3 Evaluation Framework

#### 5.3.1 Evaluation Dimensions

```python
class SlideEvaluator:
    """
    Multi-dimensional evaluation of generated slides
    """
    
    DIMENSIONS = {
        "content_coverage": ContentCoverageMetric,    # Are all atoms used?
        "narrative_flow": NarrativeFlowMetric,        # Does story progress logically?
        "visual_variety": VisualVarietyMetric,        # Are layouts diverse?
        "information_density": DensityMetric,         # Is density appropriate?
        "theme_consistency": ThemeConsistencyMetric,  # Are colors/fonts consistent?
        "accessibility": AccessibilityMetric,         # Contrast, font sizes
    }
    
    def evaluate(self, state: State) -> EvaluationReport:
        scores = {}
        for name, metric_class in self.DIMENSIONS.items():
            metric = metric_class()
            scores[name] = metric.evaluate(state)
        
        return EvaluationReport(
            overall_score=self.weighted_average(scores),
            dimension_scores=scores,
            recommendations=self.generate_recommendations(scores)
        )
```

#### 5.3.2 Metric Implementations

```python
class ContentCoverageMetric:
    """Measures how well slides cover source atoms"""
    
    def evaluate(self, state: State) -> MetricResult:
        total_atoms = len(state.atoms.contexts)
        used_atoms = set()
        
        for slide in state.slides:
            used_atoms.update(slide.atoms)
        
        coverage = len(used_atoms) / total_atoms if total_atoms > 0 else 0
        
        # Penalize if high-rank atoms are unused
        unused_high_rank = [
            a for a in state.atoms.contexts 
            if a.id not in used_atoms and a.rank >= 7
        ]
        
        return MetricResult(
            score=coverage,
            penalty=len(unused_high_rank) * 0.1,
            details={
                "total_atoms": total_atoms,
                "used_atoms": len(used_atoms),
                "unused_high_rank": [a.id for a in unused_high_rank]
            }
        )


class NarrativeFlowMetric:
    """Measures logical progression of slide narrative"""
    
    NARRATIVE_PATTERNS = {
        "hook_body_conclusion": [
            r"introduc|hook|open",
            r".*",  # body
            r"conclus|summar|takeaway"
        ],
        "problem_solution": [
            r"problem|challenge|issue",
            r"solution|approach|method",
            r"result|outcome|impact"
        ]
    }
    
    def evaluate(self, state: State) -> MetricResult:
        stories = [s.story.lower() for s in state.slides]
        
        best_match = 0
        for pattern_name, patterns in self.NARRATIVE_PATTERNS.items():
            match_score = self.match_pattern(stories, patterns)
            best_match = max(best_match, match_score)
        
        # Check for abrupt transitions
        transition_scores = []
        for i in range(len(stories) - 1):
            score = self.semantic_similarity(stories[i], stories[i+1])
            transition_scores.append(score)
        
        avg_transition = sum(transition_scores) / len(transition_scores) if transition_scores else 0
        
        return MetricResult(
            score=(best_match + avg_transition) / 2,
            details={
                "pattern_match": best_match,
                "avg_transition_smoothness": avg_transition
            }
        )


class VisualVarietyMetric:
    """Measures diversity of visual layouts"""
    
    def evaluate(self, state: State) -> MetricResult:
        layouts = [s.layout for s in state.slides]
        unique_layouts = set(layouts)
        
        # Calculate variety score
        variety = len(unique_layouts) / len(layouts) if layouts else 0
        
        # Penalize too much variety (inconsistent) or too little (boring)
        ideal_variety = 0.4  # 40% unique layouts is ideal
        variety_score = 1 - abs(variety - ideal_variety)
        
        # Check for consecutive same layouts
        consecutive_same = sum(
            1 for i in range(len(layouts) - 1) 
            if layouts[i] == layouts[i + 1]
        )
        
        return MetricResult(
            score=variety_score,
            penalty=consecutive_same * 0.05,
            details={
                "unique_layouts": list(unique_layouts),
                "layout_distribution": {l: layouts.count(l) for l in unique_layouts},
                "consecutive_same": consecutive_same
            }
        )
```

### 5.4 Test Data Generation

#### 5.4.1 State Fixtures

```python
@pytest.fixture
def minimal_state():
    """State with only required fields"""
    return State(
        meta=Meta(id="test_001"),
        source=Source(path="test.txt", content_hash="abc123"),
        todos=TodoQueue()
    )

@pytest.fixture
def state_with_atoms():
    """State with pre-extracted atoms"""
    state = minimal_state()
    state.atoms = AtomCollection(contexts=[
        Atom(id="bio_001", type=AtomType.BIO, rank=8,
             abstract="Speaker background", content={"name": "Test User"}),
        Atom(id="stat_001", type=AtomType.STAT, rank=9,
             abstract="Key metric", content={"value": "50%", "label": "Growth"}),
        Atom(id="tension_001", type=AtomType.TENSION, rank=7,
             abstract="Main challenge", content={"problem": "Scaling issues"}),
    ])
    return state

@pytest.fixture
def state_with_slides():
    """State with generated slides"""
    state = state_with_atoms()
    state.slides = [
        Slide(slide_number=1, title="Introduction", layout="spotlight",
              story="Hook the audience", atoms=["bio_001"]),
        Slide(slide_number=2, title="The Challenge", layout="comparison",
              story="Present the problem", atoms=["tension_001"]),
        Slide(slide_number=3, title="Results", layout="dashboard",
              story="Show impact", atoms=["stat_001"]),
    ]
    return state
```

#### 5.4.2 Instruction Corpus

```python
INSTRUCTION_CORPUS = {
    "creation": [
        "Create a 10-slide presentation from this transcript",
        "Generate slides about AI in healthcare",
        "Make a pitch deck for our startup",
    ],
    "modification": [
        "Add more statistics",
        "Make it more casual",
        "Focus on the technical aspects",
    ],
    "theme": [
        "Use a dark theme",
        "Make it look like Duolingo",
        "Apply a professional corporate style",
    ],
    "export": [
        "Export to PowerPoint",
        "Generate a PDF",
        "Create a video with narration",
    ],
}

def generate_test_instructions(category: str, count: int) -> List[str]:
    """Generate varied test instructions"""
    base_instructions = INSTRUCTION_CORPUS[category]
    return [
        augment_instruction(random.choice(base_instructions))
        for _ in range(count)
    ]
```

### 5.5 Continuous Evaluation Pipeline

```yaml
# .github/workflows/evaluation.yml
name: Slide Generation Evaluation

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Evaluation Suite
        run: |
          python -m pytest tests/evaluation/ \
            --eval-report=reports/evaluation.json \
            --benchmark-compare
      
      - name: Generate Evaluation Report
        run: |
          python scripts/generate_eval_report.py \
            --input reports/evaluation.json \
            --output reports/evaluation.html
      
      - name: Check Quality Gates
        run: |
          python scripts/check_quality_gates.py \
            --min-content-coverage 0.8 \
            --min-narrative-flow 0.7 \
            --max-regression 0.05
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: evaluation-report
          path: reports/
```

### 5.6 Evaluation Dashboard Schema

```python
@dataclass
class EvaluationDashboard:
    """Dashboard data for evaluation tracking"""
    
    # Time series metrics
    content_coverage_history: List[TimeSeriesPoint]
    narrative_flow_history: List[TimeSeriesPoint]
    visual_variety_history: List[TimeSeriesPoint]
    
    # Current scores
    current_scores: Dict[str, float]
    
    # Regression detection
    regressions: List[RegressionAlert]
    
    # Test case breakdown
    test_results: List[TestResult]
    
    # Recommendations
    improvement_suggestions: List[str]
    
    def to_html(self) -> str:
        """Generate HTML dashboard"""
        ...
    
    def to_json(self) -> Dict:
        """Export as JSON for API"""
        ...
```

---

## Appendix

### A. State JSON Example

```json
{
  "meta": {
    "id": "slide_20251224_001",
    "created_at": "2025-12-24T10:00:00Z",
    "updated_at": "2025-12-24T10:30:00Z",
    "version": "2.0"
  },
  "source": {
    "path": "transcript.vtt",
    "content_hash": "sha256:abc123...",
    "content_type": "vtt"
  },
  "constitution": {
    "tone": "professional",
    "target_slides": 10,
    "style_rules": ["Use active voice", "Include metrics"],
    "selected_theme": "duolingo_v1",
    "selected_vibe": "energetic"
  },
  "themes": {
    "duolingo_v1": {
      "id": "duolingo_v1",
      "primary_color": "#58CC02",
      "font_family": "Nunito"
    }
  },
  "active_theme_id": "duolingo_v1",
  "project": "duolingo",
  "atoms": {
    "id": "atoms_001",
    "model": "FactAtom",
    "contexts": [
      {
        "id": "bio_001",
        "type": "BIO",
        "rank": 8,
        "state": "active",
        "abstract": "Speaker joined Microsoft in 2011"
      }
    ]
  },
  "slides": [
    {
      "slide_number": 1,
      "title": "Introduction",
      "story": "Hook with speaker background",
      "layout": "spotlight",
      "atoms": ["bio_001"],
      "widgets": [
        {"type": "heading", "content": "From Models to Workflows"}
      ]
    }
  ],
  "todos": {
    "items": [
      {
        "id": "todo_001",
        "type": "export",
        "status": "completed",
        "params": {"format": "html"}
      }
    ]
  },
  "status": "complete"
}
```

### B. Tool Registry

| Tool | Type | Requires | Produces |
|------|------|----------|----------|
| constitution | Direct | - | constitution |
| atoms | Generative | source | atoms |
| theme | Direct/Generative | - | themes, active_theme_id |
| story | Generative | atoms | slides (draft) |
| content | Generative | slides, atoms | slides (active) |
| export | Direct | slides, theme | output files |

### C. Glossary

| Term | Definition |
|------|------------|
| **Atom** | Smallest unit of content (fact, stat, quote, etc.) |
| **Vibe** | Visual mood variation on a theme |
| **Slice** | Extract minimal context from state |
| **Patch** | Immutable update to apply to state |
| **Todo** | Scheduled task in execution queue |
| **Constitution** | Global rules and constraints |
| **Widget** | Visual component in a slide |

---

*Document Version: 1.0*
*Last Updated: December 24, 2025*
