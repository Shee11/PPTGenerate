# LLM Pipeline Architecture

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INPUT                                        │
│  - Source file (career_talk.txt)                                           │
│  - User instruction ("Create an inspiring tech career presentation")       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LLM CALL 1: INTENT DETECTION                            │
│                                                                             │
│ Role: "Presentation design consultant specializing in audience analysis"   │
│                                                                             │
│ Input to LLM:                                                               │
│   - User instruction: "Create an inspiring tech career presentation"       │
│   - Source preview: First 1000 characters of career_talk.txt               │
│                                                                             │
│ Task Description:                                                           │
│   "Analyze this presentation request and detect:                           │
│    1. Target audience (technical engineers, executives, etc.)              │
│    2. Presentation purpose (educate, persuade, inform, entertain)          │
│    3. Slide pattern (story, tutorial, showcase, pitch, report, techtuber)  │
│    4. Tone (professional, casual, energetic, authoritative)                │
│    5. Visual density (minimal, balanced, rich)                             │
│    6. Theme colors and branding style                                      │
│    7. Preset visual style (TechTuber, Professional, Creative)"             │
│                                                                             │
│ Output from LLM (JSON):                                                     │
│   {                                                                         │
│     "audience": "Early-career to mid-level tech professionals",            │
│     "purpose": "educate",                                                   │
│     "pattern": "story",                                                     │
│     "tone": "energetic",                                                    │
│     "visual_density": "balanced",                                           │
│     "atom_extraction_guidance": "Focus on actionable career lessons,       │
│         key insights, and skills to develop. Extract principles and        │
│         takeaways, not biographical timeline.",                             │
│     "content_generation_guidance": "Create narrative arc with Hook →       │
│         Lessons → Climax. Emphasize what audience can LEARN, not           │
│         speaker's story. Use action-oriented titles.",                      │
│     "theme_guidance": "Dark tech theme with blue (#0047AB) primary,        │
│         orange (#FF6B35) accent, dark background (#0a0a0a)",                │
│     "preset_guidance": "TechTuber: Elevated+Rounded+Gradient_Linear+Glow", │
│     "reasoning": "Tech career content for early/mid-level professionals    │
│         needs energetic, modern style with clear actionable insights"      │
│   }                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
      ┌─────────────────────────┐   ┌─────────────────────────────────┐
      │ atom_extraction_guidance│   │ content_generation_guidance     │
      │ theme_guidance          │   │ + theme_guidance                │
      │ preset_guidance         │   │ + preset_guidance               │
      └─────────────────────────┘   └─────────────────────────────────┘
                    │                               │
                    ▼                               │
┌─────────────────────────────────────────────────┐│
│         LLM CALL 2: ATOM EXTRACTION             ││
│                                                  ││
│ Role: "Content analyzer extracting structured   ││
│        information atoms from source material"  ││
│                                                  ││
│ Input to LLM:                                    ││
│   - Full source content (career_talk.txt)       ││
│   - Intent guidance:                             ││
│     "Focus on actionable career lessons, key    ││
│      insights, and skills to develop. Extract   ││
│      principles and takeaways, not biographical ││
│      timeline."                                  ││
│                                                  ││
│ Task Description:                                ││
│   "Extract structured information atoms:        ││
│    - Facts: Objective statements, data points   ││
│    - Quotes: Direct quotations                  ││
│    - Insights: Key takeaways, lessons learned   ││
│    - Concepts: Abstract ideas, principles       ││
│    - Metrics: Quantifiable measurements         ││
│    Prioritize information that supports the     ││
│    intended purpose and audience."               ││
│                                                  ││
│ Output from LLM (JSON):                          ││
│   {                                              ││
│     "atoms": [                                   ││
│       {                                          ││
│         "id": "atom_001",                        ││
│         "type": "insight",                       ││
│         "content": "Continuous learning is      ││
│                    essential for tech careers", ││
│         "importance": 0.95,                      ││
│         "category": "career_principle"           ││
│       },                                         ││
│       {                                          ││
│         "id": "atom_002",                        ││
│         "type": "fact",                          ││
│         "content": "Tech skills have 2-year     ││
│                    half-life",                   ││
│         "importance": 0.85,                      ││
│         "category": "industry_insight"           ││
│       },                                         ││
│       ... (15-30 atoms total)                    ││
│     ]                                            ││
│   }                                              ││
└─────────────────────────────────────────────────┘│
                    │                               │
                    ▼                               │
              [AtomCollection]                      │
              (15-30 atoms)                         │
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              LLM CALL 3: STATE TRANSITION (Structure Planning)              │
│                                                                             │
│ Role: "Presentation structure designer specializing in layout strategy"    │
│                                                                             │
│ Input to LLM:                                                               │
│   - AtomCollection (all extracted atoms)                                    │
│   - User instruction: "Create an inspiring tech career presentation"       │
│                                                                             │
│ Task Description:                                                           │
│   "Analyze atoms and determine:                                            │
│    1. Number of slides needed (based on content volume)                    │
│    2. Layout strategy for each slide:                                      │
│       - Swiss.Poster (hero statement)                                      │
│       - Bento.HeroLeft (1 main + 2-3 supporting)                           │
│       - Bento.Standard (4 equal items)                                     │
│       - Cinematic.FullBleed (immersive visual)                             │
│       - Data.KPI_Row (metrics dashboard)                                   │
│       - etc. (50+ strategies available)                                    │
│    3. Logical slide ordering                                               │
│    Create draft slides (state='draft') with strategy only.                │
│    Do NOT populate content yet."                                           │
│                                                                             │
│ Output from LLM (JSON Patch):                                               │
│   [                                                                         │
│     {                                                                       │
│       "add": {                                                              │
│         "id": "slide_001",                                                  │
│         "rank": 1,                                                          │
│         "state": "draft",                                                   │
│         "strategy": "Swiss.Poster",                                         │
│         "widgets": {},                                                      │
│         "parameters": {}                                                    │
│       }                                                                     │
│     },                                                                      │
│     {                                                                       │
│       "add": {                                                              │
│         "id": "slide_002",                                                  │
│         "rank": 2,                                                          │
│         "state": "draft",                                                   │
│         "strategy": "Bento.HeroLeft",                                       │
│         "widgets": {},                                                      │
│         "parameters": {}                                                    │
│       }                                                                     │
│     },                                                                      │
│     ... (5-24 slides)                                                       │
│   ]                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                            [Draft Slides Created]
                            (5-24 slides with strategies)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│           LLM CALL 4: CONTENT GENERATION (Populate Slides)                  │
│                                                                             │
│ Role: "Presentation Architect and Narrative Designer"                      │
│                                                                             │
│ Input to LLM:                                                               │
│   - Draft slides (with strategies assigned)                                │
│   - AtomCollection (all extracted atoms)                                    │
│   - User instruction: "Create an inspiring tech career presentation"       │
│   - Intent guidance (CRITICAL):                                            │
│     "Content Strategy: Create narrative arc with Hook → Lessons →          │
│      Climax. Emphasize what audience can LEARN, not speaker's story.       │
│      Use action-oriented titles.                                           │
│                                                                             │
│      Theme Recommendation: Dark tech theme with blue (#0047AB) primary,    │
│      orange (#FF6B35) accent, dark background (#0a0a0a)                    │
│                                                                             │
│      Preset Recommendation: TechTuber: Elevated+Rounded+                   │
│      Gradient_Linear+Glow                                                  │
│                                                                             │
│      Additional Context:                                                   │
│      - Audience: Early-career to mid-level tech professionals              │
│      - Purpose: educate                                                    │
│      - Pattern: story                                                      │
│      - Tone: energetic                                                     │
│      - Visual Density: balanced"                                           │
│                                                                             │
│ Task Description (Core Directives):                                         │
│   "🎯 CORE DIRECTIVE 1: THE REDUNDANCY CUTTER                              │
│    - Rule A: Contextual Subtraction (remove implied context)               │
│    - Rule B: Action-Oriented Titles (verbs, not labels)                    │
│    - Rule C: 3-Second Rule (grasp in 3 seconds)                            │
│                                                                             │
│    🎬 CORE DIRECTIVE 2: NARRATIVE ARC                                      │
│    - Act 1 (Hook): Swiss.Poster, Cinematic.FullBleed                       │
│    - Act 2 (Meat): Bento.HeroLeft, Data.KPI_Row                            │
│    - Act 3 (Climax): Cinematic.Split_30_70, Focus.Solar_System             │
│                                                                             │
│    ⚡ CORE DIRECTIVE 3: PACING & VISUAL DYNAMICS                           │
│    - Alternate high/low intensity                                          │
│    - Max 2 dense slides in sequence                                        │
│    - Pattern: Poster→HeroLeft→Standard→FullBleed                           │
│                                                                             │
│    🎨 CORE DIRECTIVE 4: LAYOUT SELECTION MATRIX                            │
│    1. ONE Hero Point → Swiss.Poster, Cinematic.FullBleed                   │
│    2. Hero + Supporting → Bento.HeroLeft, Cinematic.Split_30_70            │
│    3. 4 Equal Points → Bento.Quarter, Bento.Standard                       │
│    4. Progressive Journey → Swiss.Asymmetry, Focus.Solar_System            │
│    5. Data-Heavy → Data.KPI_Row, Data.Comparison_2Col                      │
│    6. Code/Technical → Code.Snippet_Hero, Swiss.SplitTypo                  │
│    7. Visual Storytelling → Cinematic.Split_50_50, Media.Gallery_2x2       │
│                                                                             │
│    🎨 THEME & PRESET STYLING (REQUIRED)                                    │
│    MANDATORY: Your patch MUST start with 'set_theme' and 'set_preset'.    │
│    Generate custom colors based on user intent.                            │
│                                                                             │
│    📋 HEADER & FOOTER (REQUIRED on every slide)                            │
│    - Header: Type.Heading (M) or Type.Caption (S)                          │
│    - Footer: Type.Caption (S) - page numbers, copyright                    │
│                                                                             │
│    Text Length Rules:                                                      │
│    - S (Short): 1 word/number                                              │
│    - M (Medium): 2-4 words                                                 │
│    - L (Long): 6-10 words                                                  │
│    - XL (Extra Long): 12-20 words (max)"                                   │
│                                                                             │
│ Output from LLM (JSON Patch):                                               │
│   [                                                                         │
│     {                                                                       │
│       "set_theme": {                                                        │
│         "id": "tech_career_energetic",                                     │
│         "primary_color": "#0047AB",                                        │
│         "secondary_color": "#003366",                                      │
│         "accent_color": "#FF6B35",                                         │
│         "background_color": "#0a0a0a",                                     │
│         "text_color": "#ffffff",                                           │
│         "font_family": "Inter, sans-serif",                                │
│         "margin_x": "60px",                                                │
│         "margin_y": "40px",                                                │
│         "gutter": "24px"                                                   │
│       }                                                                     │
│     },                                                                      │
│     {                                                                       │
│       "set_preset": {                                                       │
│         "surface": "Elevated",                                             │
│         "shape": "Rounded",                                                │
│         "fill": "Gradient_Linear",                                         │
│         "effect": "Glow"                                                   │
│       }                                                                     │
│     },                                                                      │
│     {                                                                       │
│       "replace": {                                                          │
│         "id": "slide_001",                                                  │
│         "rank": 1,                                                          │
│         "state": "active",                                                  │
│         "strategy": "Swiss.Poster",                                         │
│         "widgets": {                                                        │
│           "stage": {                                                        │
│             "type": "Type.Display",                                         │
│             "parameters": {                                                 │
│               "text": "Why Continuous Learning"                            │
│             }                                                               │
│           }                                                                 │
│         },                                                                  │
│         "header": {                                                         │
│           "type": "Type.Caption",                                           │
│           "parameters": {                                                   │
│             "text": "Tech Career Insights"                                 │
│           }                                                                 │
│         },                                                                  │
│         "footer": {                                                         │
│           "type": "Type.Caption",                                           │
│           "parameters": {                                                   │
│             "text": "© 2025 | Slide 1"                                     │
│           }                                                                 │
│         },                                                                  │
│         "parameters": {}                                                    │
│       }                                                                     │
│     },                                                                      │
│     {                                                                       │
│       "replace": {                                                          │
│         "id": "slide_002",                                                  │
│         "rank": 2,                                                          │
│         "state": "active",                                                  │
│         "strategy": "Bento.HeroLeft",                                       │
│         "widgets": {                                                        │
│           "hero": {                                                         │
│             "type": "Type.Heading",                                         │
│             "parameters": {                                                 │
│               "text": "Skills Decay Fast"                                  │
│             }                                                               │
│           },                                                                │
│           "support_1": {                                                    │
│             "type": "Type.Body",                                            │
│             "parameters": {                                                 │
│               "text": "Tech skills: 2-year half-life"                      │
│             }                                                               │
│           },                                                                │
│           "support_2": {                                                    │
│             "type": "Data.Metric",                                          │
│             "parameters": {                                                 │
│               "value": "50%",                                               │
│               "label": "Obsolete in 2 years"                               │
│             }                                                               │
│           }                                                                 │
│         },                                                                  │
│         "header": {...},                                                    │
│         "footer": {...},                                                    │
│         "parameters": {}                                                    │
│       }                                                                     │
│     },                                                                      │
│     ... (remaining slides)                                                  │
│   ]                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        [Active Slides with Content]
                        (theme, preset, all widgets populated)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      VALIDATION & REFINEMENT LOOP                           │
│                                                                             │
│ LayoutValidator checks for 4 issue types:                                  │
│   1. Color Contrast (15% threshold)                                        │
│   2. Content Density (30% minimum)                                         │
│   3. Widget Overlap (2px tolerance)                                        │
│   4. Style Consistency (same type = same preset)                           │
│                                                                             │
│ If issues found → LLM CALL 5: REFINEMENT                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (if issues found)
┌─────────────────────────────────────────────────────────────────────────────┐
│                  LLM CALL 5: REFINEMENT (Optional, 0-3 times)               │
│                                                                             │
│ Role: "Layout refinement specialist fixing quality issues"                 │
│                                                                             │
│ Input to LLM:                                                               │
│   - Current active slides (with issues)                                    │
│   - AtomCollection (for reference)                                         │
│   - User instruction                                                       │
│   - Validation feedback:                                                   │
│     "[warning] content_density: Low content density (6.3%): slide          │
│      appears empty with only 7 widgets covering 6.3% of space              │
│      Suggestion: Add more content widgets, use larger text sizes, or       │
│      switch to a layout with fewer slots"                                  │
│                                                                             │
│ Task Description:                                                           │
│   "Fix the validation issues while maintaining narrative flow.             │
│    You can:                                                                │
│    - Change layout strategy (e.g., Bento.Standard → Swiss.Poster)          │
│    - Adjust widget sizes (S → M → L → XL)                                  │
│    - Add/remove widgets                                                    │
│    - Modify text content (maintain brevity)                                │
│    Do NOT change theme or global preset during refinement."                │
│                                                                             │
│ Output from LLM (JSON Patch):                                               │
│   [                                                                         │
│     {                                                                       │
│       "replace": {                                                          │
│         "id": "slide_003",                                                  │
│         "rank": 3,                                                          │
│         "state": "active",                                                  │
│         "strategy": "Swiss.Poster",  // Changed from Bento.Standard        │
│         "widgets": {                                                        │
│           "stage": {                                                        │
│             "type": "Type.Display",  // Larger widget for better density   │
│             "parameters": {                                                 │
│               "text": "Adapt or Become Obsolete"                           │
│             }                                                               │
│           }                                                                 │
│         },                                                                  │
│         "header": {...},                                                    │
│         "footer": {...},                                                    │
│         "parameters": {}                                                    │
│       }                                                                     │
│     }                                                                       │
│   ]                                                                         │
│                                                                             │
│ → Re-validate → Repeat up to 3 times or until validation passes            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                         [Validated Slides]
                         (All quality checks passed)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LAYOUT ENGINE                                       │
│                                                                             │
│ Calculates precise layouts:                                                │
│   - Apply theme (colors, fonts, spacing)                                   │
│   - Apply style (widget presets)                                           │
│   - Execute layout strategy (position widgets in grid)                     │
│   - Calculate widget dimensions (x, y, width, height)                      │
│   - Resolve widget parameters                                              │
│                                                                             │
│ Output: RenderableLayout[] (positioned widgets with computed styles)       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HTML RENDERER                                       │
│                                                                             │
│ Generates HTML with:                                                        │
│   - CSS variables from theme (--color-primary: #0047AB)                    │
│   - Widget HTML elements with computed positions                           │
│   - Preset styles (box-shadow, border-radius, gradients, effects)          │
│   - Headers and footers                                                    │
│   - Multi-slide navigation                                                 │
│                                                                             │
│ Output: presentation.html (138 KB, ready to open in browser)               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## LLM Call Summary

| Call # | Purpose | Role | Input Size | Output Size | Temperature | Max Tokens |
|--------|---------|------|------------|-------------|-------------|------------|
| 1 | Intent Detection | Design Consultant | ~1.5K tokens | ~500 tokens (JSON) | 0.3 | 1,000 |
| 2 | Atom Extraction | Content Analyzer | ~5-10K tokens | ~2-4K tokens (15-30 atoms) | 0.5 | 6,000 |
| 3 | State Transition | Structure Designer | ~3-5K tokens | ~1-2K tokens (5-24 slides) | 0.2 | 2,000 |
| 4 | Content Generation | Presentation Architect | ~14K tokens | ~6-12K tokens (full slides) | 0.7 | 32,000 |
| 5 | Refinement (optional) | Layout Specialist | ~8-12K tokens | ~1-3K tokens (fixes) | 0.5 | 8,000 |

**Total LLM Calls**: 4-7 (1 intent + 1 atom + 1 structure + 1 content + 0-3 refinement)

**Total Cost (estimated)**: 
- GPT-4 Turbo: ~$0.15-0.30 per generation
- GPT-5 (reasoning): ~$0.50-1.00 per generation (higher due to reasoning tokens)

## Key Design Principles

1. **Intent-Driven**: User intent detected first, guides all downstream LLM calls
2. **Theme Generation**: LLM generates custom colors/presets based on audience/tone (not hardcoded)
3. **Separation of Concerns**: Structure planning (strategies) separate from content (widgets)
4. **Narrative Architecture**: 4 core directives (Redundancy Cutter, Narrative Arc, Pacing, Layout Matrix)
5. **Quality Loop**: Automatic validation and refinement until quality standards met
6. **Extreme Brevity**: Text length enforcement (S/M/L/XL) prevents overcrowded slides
