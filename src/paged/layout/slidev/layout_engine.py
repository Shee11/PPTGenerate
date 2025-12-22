"""Slidev layout engine - provides documentation for LLM content generation.

ARCHITECTURE OVERVIEW:

Directory Structure:
- slidev-project/: SOURCE directory (version controlled)
  - layouts/: Custom Vue layout components (.vue files)
  - components/: Custom Vue widget components (.vue files)
  - package.json: Slidev dependencies and scripts
  
- slidev_build/: BUILD directory (temporary, auto-generated, gitignored)
  - Created fresh on each render by copying from slidev-project/
  - Receives generated slides.md from renderer
  - Executes `npm run build` to generate static HTML
  - Gets cleaned up after successful build

Development Workflow:
1. Add/edit layouts in slidev-project/layouts/*.vue
2. Add/edit components in slidev-project/components/*.vue
3. Update layout documentation in this file (get_layout_documentation method)
4. Run UCE render - it will:
   - Copy slidev-project/ → slidev_build/
   - Generate slides.md with your layouts
   - Build static HTML via Slidev/Vite
   
Key Design Decisions:
- slidev-project/ is the single source of truth
- slidev_build/ is disposable (never edit files here)
- Layout/component documentation drives LLM content generation
- LLM matches abstract visual_design to concrete layouts via documentation
- No hardcoded layout mappings - all via documentation matching
"""


class SlidevLayoutEngine:
    """Layout engine for Slidev presentations with Vue components.
    
    This engine does not calculate layouts (Vue handles rendering).
    It provides documentation for LLM content generation.
    """
    
    @classmethod
    def get_layout_documentation(cls) -> str:
        """Provide Slidev layout documentation for content generation LLMs.
        
        Returns:
            Formatted string describing Slidev layouts, slots, widgets, and themes.
        """
        return """# SLIDEV LAYOUT PROTOCOL

⚠️ **CRITICAL**: Use ONLY the exact layout and slot names listed below. Do NOT invent names.

## AVAILABLE LAYOUTS WITH EXACT SLOT NAMES

### hero-split
Two-panel split layout.
- **Slots**: `left`, `right` (EXACTLY these names)
- **Parameters**: `ratio: "50-50"` or `"60-40"` or `"70-30"`
- **Example widgets**:
```json
{
  "layout": "hero-split",
  "parameters": { "ratio": "60-40" },
  "widgets": {
    "left": { "type": "Type.Display", "parameters": { "text": "Title Here" } },
    "right": { "type": "Type.Body", "parameters": { "text": "Description" } }
  }
}
```

### smart-grid
Multi-column grid layout (2-4 columns) for **EQUAL** parallel content.
- **Slots**: `header`, `col1`, `col2`, `col3`, `col4` (EXACTLY these names)
- **Parameters**: `cols: 2` or `3` or `4`
- **Best for**: parallel items of same importance (3 pillars, 4 values, equal options)
- **NOT for**: labeled content pairs (use info-boxes instead)
- **Example** (3 equal pillars):
```json
{
  "layout": "smart-grid",
  "parameters": { "cols": 3 },
  "widgets": {
    "header": { "type": "Type.Heading", "parameters": { "text": "Three Pillars" } },
    "col1": { "type": "Type.Body", "parameters": { "text": "Speed" } },
    "col2": { "type": "Type.Body", "parameters": { "text": "Quality" } },
    "col3": { "type": "Type.Body", "parameters": { "text": "Scale" } }
  }
}
```

### info-boxes
Labeled content boxes (2-4 boxes, each with title + content).
- **Slots**: `title`, `box1_title`, `box1_content`, `box2_title`, `box2_content`, `box3_title`, `box3_content`, `box4_title`, `box4_content`
- **Parameters**: `boxes: 2` or `3` or `4`
- **Best for**: labeled sections, principles with explanations, features with descriptions
- **Example** (2 labeled boxes):
```json
{
  "layout": "info-boxes",
  "parameters": { "boxes": 2 },
  "widgets": {
    "title": { "type": "Type.Heading", "parameters": { "text": "Two Key Principles" } },
    "box1_title": { "type": "Type.Heading", "parameters": { "text": "1. Precise Problem Definition", "level": 4 } },
    "box1_content": { "type": "Type.Body", "parameters": { "text": "Define problems broadly to maximize solution space..." } },
    "box2_title": { "type": "Type.Heading", "parameters": { "text": "2. Evaluation Systems", "level": 4 } },
    "box2_content": { "type": "Type.Body", "parameters": { "text": "Build evaluation systems that measure real outcomes..." } }
  }
}
```

### timeline
Step-by-step process layout.
- **Slots**: `title`, `step1`, `step2`, `step3`, `step4`, `step5` (EXACTLY these names)
- **Example**:
```json
{
  "layout": "timeline",
  "widgets": {
    "title": { "type": "Type.Heading", "parameters": { "text": "Process" } },
    "step1": { "type": "Type.Body", "parameters": { "text": "First step" } },
    "step2": { "type": "Type.Body", "parameters": { "text": "Second step" } },
    "step3": { "type": "Type.Body", "parameters": { "text": "Third step" } }
  }
}
```

### comparison
Before/After comparison with VS divider.
- **Slots**: `title`, `beforeLabel`, `before`, `afterLabel`, `after` (EXACTLY these names)
- **Example**:
```json
{
  "layout": "comparison",
  "widgets": {
    "title": { "type": "Type.Heading", "parameters": { "text": "Old vs New" } },
    "beforeLabel": { "type": "Type.Heading", "parameters": { "text": "Before", "level": 3 } },
    "before": { "type": "Type.List", "parameters": { "items": ["Old way 1", "Old way 2"] } },
    "afterLabel": { "type": "Type.Heading", "parameters": { "text": "After", "level": 3 } },
    "after": { "type": "Type.List", "parameters": { "items": ["New way 1", "New way 2"] } }
  }
}
```

### dashboard
KPI dashboard with metrics and chart.
- **Slots**: `title`, `metric1`, `metric2`, `metric3`, `metric4`, `chart` (EXACTLY these names)
- **Example**:
```json
{
  "layout": "dashboard",
  "widgets": {
    "title": { "type": "Type.Heading", "parameters": { "text": "Key Metrics" } },
    "metric1": { "type": "Data.BigNum", "parameters": { "value": "99%", "label": "Uptime" } },
    "metric2": { "type": "Data.BigNum", "parameters": { "value": "2.5M", "label": "Users" } }
  }
}
```

### spotlight
Hero slide with large centered content and spotlight effect.
- **Slots**: `default` (main content), `subtitle` (EXACTLY these names)
- **Parameters**: `align: "left"` or `"center"` or `"right"`, `intensity: "soft"` or `"medium"` or `"strong"`
- **Example**:
```json
{
  "layout": "spotlight",
  "widgets": {
    "default": { "type": "Type.Display", "parameters": { "text": "Big Announcement" } },
    "subtitle": { "type": "Type.Body", "parameters": { "text": "Supporting details" } }
  }
}
```

### full-bleed
Full-screen content.
- **Slots**: `default` (single slot)
- **Parameters**: `align: "center"` or `"top"` or `"bottom"`

### feature-grid
Product features in 3x2 grid.
- **Slots**: `title`, `feature1`, `feature2`, `feature3`, `feature4`, `feature5`, `feature6`
- **Best for**: 6 features or benefits

### cards-grid
Flexible card grid (2-4 columns, up to 8 cards).
- **Slots**: `title`, `card-1`, `card-2`, `card-3`, `card-4`, `card-5`, `card-6`, `card-7`, `card-8`
- **Parameters**: `columns: 2` or `3` or `4`, `cardStyle: "elevated"` or `"flat"` or `"outlined"` or `"glass"`
- **Best for**: flexible number of cards (2-8 items)

### two-cols-header
Two columns with header.
- **Slots**: `header`, `left`, `right`

### quote-hero
Large quote display.
- **Slots**: `default` (the quote text), `author`, `context`
- **Example**:
```json
{
  "layout": "quote-hero",
  "widgets": {
    "default": { "type": "Type.Quote", "parameters": { "text": "The quote goes here..." } },
    "author": { "type": "Type.Body", "parameters": { "text": "Author Name" } },
    "context": { "type": "Type.Body", "parameters": { "text": "Context or title" } }
  }
}
```

### stats-showcase
Statistics display with dynamic slots.
- **Slots**: `title`, `stat-1`, `stat-2`, `stat-3`, `stat-4` (note the hyphen!)
- **Example**:
```json
{
  "layout": "stats-showcase",
  "widgets": {
    "title": { "type": "Type.Heading", "parameters": { "text": "Key Stats" } },
    "stat-1": { "type": "Data.BigNum", "parameters": { "value": "99%", "label": "Accuracy" } },
    "stat-2": { "type": "Data.BigNum", "parameters": { "value": "10x", "label": "Faster" } }
  }
}
```

### center (built-in)
Centered content.
- **Slots**: `default` (or no slots, content goes directly)

### default (built-in)
Basic content layout.
- **Slots**: `default` (or no slots, content goes directly)

## WIDGET TYPES
| Type | Parameters |
|------|------------|
| Type.Display | text, align |
| Type.Heading | text, level (1-6) |
| Type.Body | text |
| Type.List | items[], list_type ("ordered"/"unordered") |
| Type.Quote | text, author, attribution |
| Data.BigNum | value, label, unit |
| Data.Metric | label, value, change |

## ❌ COMMON MISTAKES TO AVOID
- ❌ `cell_1`, `cell_2` → Use `col1`, `col2` for smart-grid
- ❌ `stage1_title`, `stage1_detail` → Use `step1`, `step2` for timeline
- ❌ `left_header`, `right_body` → Use `beforeLabel`, `before`, `afterLabel`, `after` for comparison
- ❌ `stat1`, `stat2` → Use `stat-1`, `stat-2` for stats-showcase (note the hyphen!)
- ❌ `card1`, `card2` → Use `card-1`, `card-2` for cards-grid (note the hyphen!)
- ❌ Inventing slot names not listed above
- ❌ Using smart-grid for labeled pairs (header + content) → Use info-boxes instead
- ❌ Example bad pattern: col1="1. Title", col2="description", col3="2. Title", col4="description"
  → This is labeled pairs! Use info-boxes with box1_title, box1_content, box2_title, box2_content

## VIBE EFFECTS (optional slide parameter)
Options: none, particles, waves, noise, bokeh, mesh, aurora

## 🎯 LAYOUT PLANNING STRATEGY

### DIVERSITY RULE: Vary layouts for visual interest!
A good 10-14 slide presentation should use **at least 5-6 different layouts**.
Don't repeat the same layout more than 2-3 times.

### LAYOUT CATEGORIES & BEST USE CASES

#### 🎬 OPENING/CLOSING (dramatic impact)
| Layout | Best For | Emotional Effect |
|--------|----------|------------------|
| **spotlight** | Title slides, big reveals, key takeaways | Dramatic, focused |
| **full-bleed** | Opening hook, closing call-to-action | Bold, immersive |
| **quote-hero** | Memorable quotes, testimonials | Personal, inspiring |

#### 📊 DATA & METRICS (numbers and facts)
| Layout | Best For | Slots |
|--------|----------|-------|
| **dashboard** | KPIs with optional chart | metric1-4, chart |
| **stats-showcase** | Pure statistics display | stat-1 to stat-4 |

#### 📝 CONTENT & EXPLANATION (ideas and details)
| Layout | Best For | When to Use |
|--------|----------|-------------|
| **hero-split** | Two related concepts, image+text | Title+body, concept+details |
| **two-cols-header** | Two columns under one header | Comparing two aspects |
| **info-boxes** | Labeled principles/features | "1. Title" + explanation pairs |
| **smart-grid** | 3-4 EQUAL parallel items | Pillars, values, options |

#### 🔢 LISTS & FEATURES (multiple items)
| Layout | Best For | Item Count |
|--------|----------|------------|
| **timeline** | Sequential steps, process | 3-5 steps |
| **comparison** | Before/After, Old/New | 2 sides |
| **cards-grid** | Flexible card display | 2-8 cards |
| **feature-grid** | Fixed 6 features | Exactly 6 |

### RECOMMENDED FLOW FOR A 12-SLIDE PRESENTATION
| Slide | Purpose | Suggested Layouts |
|-------|---------|-------------------|
| 1 | Opening hook | spotlight, full-bleed |
| 2-3 | Context/Problem | hero-split, two-cols-header |
| 4-5 | Key points | info-boxes, smart-grid |
| 6-7 | Process/How | timeline, comparison |
| 8-9 | Evidence/Data | dashboard, stats-showcase |
| 10-11 | Details/Features | cards-grid, feature-grid |
| 12 | Call to action | spotlight, quote-hero |

### ❌ ANTI-PATTERNS
- Using hero-split for EVERY slide (monotonous)
- Using smart-grid for labeled pairs (use info-boxes)
- Using spotlight for data-heavy content (use dashboard)
- Never using data layouts in a business presentation
"""
    
    @classmethod
    def get_layout_constrain(cls) -> str:
        """Provide Slidev-specific layout-widget compatibility constraints.
        
        Returns:
            Formatted string describing widget-layout compatibility rules.
        """
        return """# LAYOUT-WIDGET CONSTRAINTS

## WIDGET SIZE REQUIREMENTS
| Widget Type | Space Needed | Best Layouts |
|-------------|--------------|--------------|
| Type.Quote, Data.Table | WIDE | full-bleed, hero-split (large side) |
| Type.Display | WIDE | spotlight, hero-split, full-bleed |
| Data.BigNum, Data.Metric | NARROW | smart-grid cols, dashboard, stats-showcase |
| Type.Heading, Type.Body | FLEXIBLE | Any layout |
| Type.List | MEDIUM | hero-split, two-cols-header, magazine |

## LAYOUT-WIDGET COMPATIBILITY
| Layout | ✅ Good Widgets | ❌ Avoid |
|--------|----------------|----------|
| spotlight | Type.Display, Type.Heading, Type.Body | Data.Table |
| hero-split | Any (put wide content in larger ratio side) | - |
| smart-grid | Data.Metric, Data.BigNum, Type.Heading | Type.Quote, Data.Table, labeled pairs |
| info-boxes | Type.Heading (in titles), Type.Body, Type.List (in content) | Data.Table |
| cards-grid | Type.Body, Type.Heading, Type.List | Data.Table, long text |
| full-bleed | Any (full width available) | - |
| timeline | Type.Body (brief), Type.Heading | Type.Quote, Data.Table |
| dashboard | Data.Metric, Data.BigNum, Data.Chart | Type.Quote, long text |
| quote-hero | Type.Quote | Data.Table, Type.List |
| stats-showcase | Data.BigNum, Data.Metric | Type.Quote, long text |

## LAYOUT SELECTION GUIDE
| Content Pattern | Use Layout |
|-----------------|------------|
| 3-4 equal parallel items (pillars, values) | smart-grid |
| Labeled pairs (numbered points with explanations) | info-boxes |
| Variable number of cards (2-8 items) | cards-grid |
| Exactly 6 features/benefits | feature-grid |
| Before/After or comparison | comparison |
| Step-by-step process | timeline |
| Single big statement | spotlight or full-bleed |
| Multiple KPIs/metrics | dashboard or stats-showcase |
| Two major sections | hero-split |
| Quote with attribution | quote-hero |
| Two columns under shared heading | two-cols-header |

## DIVERSITY CHECKLIST
Before finalizing, verify your presentation has:
✅ At least 1 dramatic layout (spotlight, full-bleed, quote-hero)
✅ At least 1 data layout if presenting metrics (dashboard, stats-showcase)
✅ At least 1 structured layout (timeline, comparison, info-boxes)
✅ No layout used more than 3 times
✅ Layout variety across consecutive slides (don't repeat same layout back-to-back)

## RULES
1. Match widget to layout slot size
2. Put wide content in hero-split large side (60% or 70%)
3. Use spotlight or full-bleed for big impactful text
4. Use dashboard or stats-showcase for metrics
5. Use timeline for step-by-step content
"""
    
    @classmethod
    def calculate(cls, slides, theme, style):
        """Not implemented - Slidev engine is render-only.
        
        Raises:
            NotImplementedError: Always raised with guidance message.
        """
        raise NotImplementedError(
            "Slidev engine does not use calculate() - use SlidevRenderer directly"
        )
