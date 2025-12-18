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
        return """SLIDEV CUSTOM LAYOUT SYSTEM

Source Directory: slidev-project/ (layouts and components are source-controlled here)
Build Directory: slidev_build/ (temporary, auto-generated during rendering)

Available Custom Layouts (slidev-project/layouts/):

1. smart-grid (Smart Grid Layout)
   - Dynamic column-based layout supporting 2-4 columns
   - Slot names: 'header' (full-width), 'col1', 'col2', 'col3', 'col4'
   - Parameters: cols (integer, 2-4)
   - Best for: Multi-column content, data dashboards, comparison views
   - Visual: Grid with equal-width columns, optional header
   - Design characteristics: grid, symmetrical, hierarchical (with header), organized
   
   Example JSON:
   {
     "layout": "smart-grid",
     "parameters": {"cols": 3},
     "widgets": {
       "header": {"type": "Type.Heading", "parameters": {"text": "Q4 Metrics"}},
       "col1": {"type": "Data.BigNum", "parameters": {"text": "Revenue\\n$5.2M"}},
       "col2": {"type": "Data.BigNum", "parameters": {"text": "Users\\n12.5K"}},
       "col3": {"type": "Data.BigNum", "parameters": {"text": "Growth\\n+23%"}}
     }
   }

2. hero-split (Hero Split Layout)
   - Two-panel layout with configurable width ratios
   - Slot names: 'left', 'right'
   - Parameters: ratio (string: "50-50", "60-40", "40-60", "70-30", "30-70")
   - Best for: Featured content, before/after, visual storytelling, image + text
   - Visual: Horizontal split with adjustable column widths
   - Design characteristics: split, asymmetrical (unless 50-50), comparison, dual-concept
   
   Example JSON:
   {
     "layout": "hero-split",
     "parameters": {"ratio": "60-40"},
     "widgets": {
       "left": {"type": "Type.Display", "parameters": {"text": "# Main Message\\n\\nKey content here"}},
       "right": {"type": "Data.BigNum", "parameters": {"text": "Success Rate\\n95%"}}
     }
   }

3. full-bleed (Full Bleed Layout)
   - Single full-screen content area with vertical alignment
   - Slot names: default (unnamed slot)
   - Parameters: align (string: "top", "center", "bottom")
   - Best for: Hero slides, large images, title slides, dramatic quotes
   - Visual: Full viewport, centered horizontally, vertical align configurable
   
   Example JSON:
   {
     "layout": "full-bleed",
     "parameters": {"align": "center"},
     "widgets": {
       "default": {"type": "Type.Display", "parameters": {"text": "# Innovation Starts Here"}}
     }
   }

4. feature-grid (Feature Grid Layout)
   - 3x2 grid for showcasing features/benefits
   - Slot names: 'title', 'feature1', 'feature2', 'feature3', 'feature4', 'feature5', 'feature6'
   - Parameters: None
   - Best for: Product features, benefit lists, service offerings
   - Visual: 3 columns, up to 6 feature boxes with gradient backgrounds
   
   Example JSON:
   {
     "layout": "feature-grid",
     "widgets": {
       "title": {"type": "Type.Heading", "parameters": {"text": "Key Features"}},
       "feature1": {"type": "Type.Body", "parameters": {"text": "**Fast**\\nOptimized performance"}},
       "feature2": {"type": "Type.Body", "parameters": {"text": "**Secure**\\nEnd-to-end encryption"}},
       "feature3": {"type": "Type.Body", "parameters": {"text": "**Scalable**\\nGrows with you"}}
     }
   }

5. comparison (Comparison Layout)
   - Before/after or vs comparison with visual divider
   - Slot names: 'title', 'beforeLabel', 'before', 'afterLabel', 'after'
   - Parameters: None
   - Best for: Before/after, old vs new, problem/solution
   - Visual: Two sides with color coding (red/green), VS divider
   
   Example JSON:
   {
     "layout": "comparison",
     "widgets": {
       "title": {"type": "Type.Heading", "parameters": {"text": "Transformation"}},
       "beforeLabel": {"type": "Type.Body", "parameters": {"text": "Before"}},
       "before": {"type": "Type.List", "parameters": {"items": ["Manual", "Slow", "Error-prone"]}},
       "afterLabel": {"type": "Type.Body", "parameters": {"text": "After"}},
       "after": {"type": "Type.List", "parameters": {"items": ["Automated", "Fast", "Reliable"]}}
     }
   }

6. timeline (Timeline Layout)
   - Step-by-step timeline with numbered markers
   - Slot names: 'title', 'step1', 'step2', 'step3', 'step4', 'step5'
   - Parameters: None
   - Best for: Processes, roadmaps, step-by-step guides, historical events
   - Visual: Vertical timeline with numbered circles and connecting lines
   
   Example JSON:
   {
     "layout": "timeline",
     "widgets": {
       "title": {"type": "Type.Heading", "parameters": {"text": "Development Roadmap"}},
       "step1": {"type": "Type.Body", "parameters": {"text": "**Q1**: Research & Planning"}},
       "step2": {"type": "Type.Body", "parameters": {"text": "**Q2**: Development Sprint"}},
       "step3": {"type": "Type.Body", "parameters": {"text": "**Q3**: Testing & QA"}},
       "step4": {"type": "Type.Body", "parameters": {"text": "**Q4**: Launch"}}
     }
   }

7. dashboard (Dashboard Layout)
   - Executive dashboard with metrics and chart area
   - Slot names: 'title', 'metric1', 'metric2', 'metric3', 'metric4', 'chart'
   - Parameters: None
   - Best for: KPI dashboards, data overview, executive summaries
   - Visual: 2 large metric cards on top, 2 small on right, large chart area below
   
   Example JSON:
   {
     "layout": "dashboard",
     "widgets": {
       "title": {"type": "Type.Heading", "parameters": {"text": "Performance Dashboard"}},
       "metric1": {"type": "Data.BigNum", "parameters": {"text": "Revenue\\n$2.3M"}},
       "metric2": {"type": "Data.BigNum", "parameters": {"text": "Customers\\n1,247"}},
       "metric3": {"type": "Data.BigNum", "parameters": {"text": "Growth\\n+18%"}},
       "metric4": {"type": "Data.BigNum", "parameters": {"text": "Churn\\n2.1%"}},
       "chart": {"type": "Type.Body", "parameters": {"text": "[Chart visualization area]"}}
     }
   }

Slidev Built-in Layouts (also available):

- cover: Title slide with centered content - Design: full-canvas, hierarchical, bold
- intro: Speaker introduction - Design: hierarchical, personal, focused
- default: Standard content slide - Design: hierarchical, simple
- center: Centered content - Design: symmetrical, balanced, minimal
- two-cols: Two columns (slots: ::left::, ::right::) - Design: split, symmetrical
- two-cols-header: Two columns with header (slots: ::header::, ::left::, ::right::) - Design: split, hierarchical
- quote: Large quotation display - Design: full-canvas, textual-emphasis, minimal
- section: Section divider - Design: hierarchical, transitional, minimal
- statement: Bold key message - Design: full-canvas, bold, singular-focus
- fact: Single fact highlight - Design: hierarchical, data-highlight
- image: Full-image slide - Design: full-canvas, immersive
- image-left: Image left, content right - Design: split, asymmetrical
- image-right: Image right, content left - Design: split, asymmetrical
- end: Closing slide - Design: full-canvas, minimal

Custom Vue Components (slidev-project/components/):

STANDARD COMPONENTS:

1. <ChartWidget> - Data visualization component
   Usage in markdown:
   ```vue
   <ChartWidget
     chartType="bar|line|pie|donut"
     title="Chart Title"
     :data="[{label: 'Q1', value: 75, color: '#3b82f6'}, ...]"
     unit="%"
   />
   ```
   Props:
   - chartType: bar, line, pie, donut
   - title: Optional chart title
   - data: Array of {label, value, color}
   - unit: Unit suffix (default: "%")
   - width/height: Dimensions for line charts
   
   Example:
   ```vue
   <ChartWidget
     chartType="bar"
     title="Quarterly Revenue"
     :data="[
       {label: 'Q1', value: 85, color: '#3b82f6'},
       {label: 'Q2', value: 92, color: '#10b981'},
       {label: 'Q3', value: 78, color: '#f59e0b'},
       {label: 'Q4', value: 95, color: '#8b5cf6'}
     ]"
   />
   ```

2. <TableWidget> - Data table component
   Usage in markdown:
   ```vue
   <TableWidget
     title="Performance Metrics"
     variant="default|striped|bordered|minimal"
     :columns="[{key: 'name', label: 'Name', align: 'left', format: 'text'}, ...]"
     :rows="[{name: 'Product A', value: 1234, change: 12.5}, ...]"
   />
   ```
   Props:
   - title: Optional table title
   - variant: default, striped, bordered, minimal
   - showHeader: Boolean (default: true)
   - columns: Array of {key, label, align, format}
     - Formats: text, badge, number, percent, change
   - rows: Array of data objects
   
   Example:
   ```vue
   <TableWidget
     title="Sales Performance"
     variant="striped"
     :columns="[
       {key: 'product', label: 'Product', align: 'left', format: 'text'},
       {key: 'sales', label: 'Sales', align: 'right', format: 'number'},
       {key: 'change', label: 'Change', align: 'right', format: 'change'}
     ]"
     :rows="[
       {product: 'Widget A', sales: 12500, change: 15.2},
       {product: 'Widget B', sales: 8300, change: -3.5}
     ]"
   />
   ```

3. <QuoteWidget> - Quote/testimonial component
   Usage in markdown:
   ```vue
   <QuoteWidget
     text="Quote text here"
     author="Author Name"
     attribution="Role, Company"
     variant="default|minimal|boxed|accent|large"
     :showIcon="true"
   />
   ```
   Props:
   - text: Quote text (required)
   - author: Author name
   - attribution: Role, company, context
   - variant: default, minimal, boxed, accent, large
   - showIcon: Show quotation mark icon
   
   Example:
   ```vue
   <QuoteWidget
     text="This solution transformed our workflow and saved us countless hours."
     author="Jane Smith"
     attribution="CTO, Tech Corp"
     variant="accent"
   />
   ```

4. <MetricWidget> - KPI/metric display component
   Usage in markdown:
   ```vue
   <MetricWidget
     label="Metric Label"
     value="1.2M"
     :change="15.3"
     changeLabel="vs last month"
     subtitle="Additional context"
     icon="trend-up|trend-down|users|dollar|chart"
     variant="default|compact|large|card"
   />
   ```
   Props:
   - label: Metric label (required)
   - value: Metric value (required)
   - change: Percentage change (optional)
   - changeLabel: Change context (e.g., "vs last month")
   - subtitle: Additional context
   - icon: trend-up, trend-down, users, dollar, chart
   - variant: default, compact, large, card
   
   Example:
   ```vue
   <MetricWidget
     label="Total Revenue"
     value="$2.3M"
     :change="18.5"
     changeLabel="vs last quarter"
     icon="dollar"
     variant="card"
   />
   ```

STYLE-RICH COMPONENTS (High Design Impact):

5. <PolaroidCard> - Instant photo frame with handwritten caption
   Usage in markdown:
   ```vue
   <PolaroidCard
     caption="Summer 2023"
     variant="classic|vintage|modern"
     :tilt="true"
   >
     Your content here (image, text, etc.)
   </PolaroidCard>
   ```
   Props:
   - caption: Handwritten-style caption text
   - variant: classic (white), vintage (sepia), modern (dark)
   - tilt: Enable random rotation (default: true)
   
   Best for: Photo galleries, testimonials, portfolio items, creative displays

6. <NeonFrame> - Cyberpunk neon border frame
   Usage in markdown:
   ```vue
   <NeonFrame
     color="cyan|magenta|lime|orange"
     :pulse="false"
   >
     Your content here
   </NeonFrame>
   ```
   Props:
   - color: Neon glow color (cyan, magenta, lime, orange)
   - pulse: Animated pulsing effect (default: false)
   
   Best for: Cyber/tech themes, highlighting key content, futuristic aesthetics

7. <GlassCard> - Glassmorphism card with blur and transparency
   Usage in markdown:
   ```vue
   <GlassCard
     variant="light|dark|tinted"
     blur="light|medium|heavy"
   >
     Your content here
   </GlassCard>
   ```
   Props:
   - variant: light (white), dark (black), tinted (blue/purple)
   - blur: Backdrop blur intensity
   
   Best for: Modern UI, overlay content, premium feel, iOS-style design

8. <RetroTerminal> - Vintage computer terminal with CRT effects
   Usage in markdown:
   ```vue
   <RetroTerminal
     title="SYSTEM.EXE"
     color="green|amber|cyan"
   >
     > Your terminal content
     > Commands and output
   </RetroTerminal>
   ```
   Props:
   - title: Terminal window title
   - color: Phosphor color (green, amber, cyan)
   
   Best for: Code presentations, retro themes, command-line demos, hacker aesthetic

9. <HolographicCard> - Iridescent holographic effect card
   Usage in markdown:
   ```vue
   <HolographicCard :shimmer="true">
     Your content here
   </HolographicCard>
   ```
   Props:
   - shimmer: Animated color-shifting effect (default: true)
   
   Best for: Futuristic themes, premium content, eye-catching highlights, sci-fi aesthetic

SHELL LAYER - VIBE EFFECTS:

All slides support a `vibe` parameter for ambient background effects:

Available vibes:
- none: No effects (default)
- particles: Floating particles animation
- waves: Subtle wave motion
- noise: Film grain texture overlay
- bokeh: Soft bokeh light orbs
- mesh: Animated gradient mesh

Usage in frontmatter:
```yaml
---
layout: smart-grid
vibe: particles
---
```

Example combinations:
- Business presentation: vibe="mesh" for subtle sophistication
- Tech/Cyber theme: vibe="particles" for dynamic energy
- Creative/Artistic: vibe="bokeh" for dreamy atmosphere
- Vintage/Film: vibe="noise" for texture and depth
- Calm/Serene: vibe="waves" for gentle motion

Widget-to-Markdown Mappings:

Typography Widgets (render as markdown text):
- Type.Display → # Large heading text
- Type.Heading → ## Heading text
- Type.Subhead → ### Subheading text
- Type.Body → Paragraph text
- Type.Caption → *Caption text*
- Type.List → - Bulleted list items
- Type.Quote → <QuoteWidget> component (use for rich quotes)
- Type.Code → ```language\\ncode\\n```

Data Widgets (render as Vue components or markdown):
- Data.BigNum → <MetricWidget> component (for KPIs with icons)
- Data.Metric → **Label**\\nValue (two lines, bold label)
- Data.Table → <TableWidget> component (for structured data)
- Data.Chart → <ChartWidget> component (for visualizations)
- Data.Progress → Simple text or markdown progress indicator

Supported Themes:

1. default (Slidev Default Theme)
   - Colors: Clean blue accents (#2563eb), white/dark backgrounds
   - Typography: System fonts (Avenir Next, Georgia, Fira Code)
   - Visual: Modern, minimal, professional
   - Use for: General presentations, business content

2. seriph (Seriph Theme)
   - Colors: Elegant serif styling, muted tones
   - Typography: Serif fonts for formal aesthetic
   - Visual: Classic, sophisticated, academic
   - Use for: Formal presentations, academic talks

3. apple-basic (Apple-style Theme)
   - Colors: Apple-inspired minimal palette
   - Typography: San Francisco-style fonts
   - Visual: Clean, spacious, premium
   - Use for: Product launches, design presentations

Theme Configuration (in global frontmatter):
```yaml
---
theme: default
background: https://source.unsplash.com/...
highlighter: shiki
lineNumbers: true
transition: slide-left  # fade-out, slide-up, etc.
fonts:
  sans: 'Avenir Next'
  serif: 'Georgia'
  mono: 'Fira Code'
colorSchema: auto  # auto, light, or dark
---
```

Layout Selection Best Practices:

1. **Opening slide**: full-bleed or cover
   - Use for dramatic title slides
   - Align: center for balance

2. **Content slides**: default, smart-grid, or hero-split
   - smart-grid for data-heavy content (2-4 columns)
   - hero-split for image + text (adjust ratio as needed)
   - default for text-heavy content

3. **Feature showcase**: feature-grid
   - Perfect for 3-6 features/benefits
   - Visual hierarchy with gradient boxes

4. **Comparisons**: comparison or two-cols
   - comparison for before/after with color coding
   - two-cols for neutral side-by-side

5. **Process/Timeline**: timeline
   - Step-by-step guides
   - Roadmaps and schedules

6. **Data overview**: dashboard
   - Executive summaries
   - KPI displays

7. **Section breaks**: section or full-bleed
   - Visual pause between topics
   - Clear chapter divisions

8. **Closing slide**: end or full-bleed
   - Thank you message
   - Contact information

Slot Usage Guidelines:
- Use slot names exactly as specified (case-sensitive)
- For unnamed default slots, use "default" as key
- Fill all visible slots to avoid empty areas
- Mix widget types within slots for visual variety
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
