"""React MDX layout engine - prompt components for LLM content generation."""


class ReactLayoutEngine:
    """Layout engine for React MDX presentations with semantic components."""

    @classmethod
    def get_chart_prompt(cls) -> str:
        """Provide chart component documentation for LLM prompts.

        This is the SINGLE SOURCE OF TRUTH for all chart-related documentation.
        Other modules should reference this instead of duplicating chart info.
        """
        return """# CHART DOCUMENTATION

## CHART TYPE SELECTION
**PRIORITY: If source content or user instruction explicitly specifies a chart type, USE THAT CHART TYPE.**

When NO chart type is specified, select based on data patterns:
| Data Pattern | Chart Type | Component |
|--------------|------------|-----------|
| Time-series/cumulative | area | `<ChartArea gradient={true}/>` |
| Categorical comparison | bar | `<ChartBar/>` |
| Before/after comparison | bar (clustered) | `<ChartBar data={[{label, before, after}]}/>` |
| Rankings/sorted values | barStats | `<BarStats sortDescending={true}/>` |
| Proportions (~100%) | pie/doughnut | `<ChartPie variant="donut"/>` |
| 3D relationships | bubble | `<ChartBubble data={[{label, x, y, size}]}/>` |
| Multivariate (4+ attrs) | radar | `<ChartRadar/>` (needs 3+ data points) |
| Cyclical/periodic | polarArea | `<ChartPolar/>` |
| Direction/wind distribution | rose | `<ChartCustom type="rose"/>` |

## STANDARD CHART COMPONENTS
| Component | Best For | Example |
|-----------|----------|---------|
| ChartBar | Categorical comparison | Sales by product |
| ChartLine | Trends over time | Monthly growth |
| ChartPie | Proportions (variant="donut" for doughnut) | Market share |
| ChartArea | Cumulative trends, time-series with volume | Revenue over months |
| ChartBubble | 3D data (x, y, size) | Price vs Sales vs Volume |
| ChartRadar | 4+ attributes per item | Product comparison matrix |
| ChartPolar | Cyclical patterns | Monthly distribution |
| BarStats | Rankings, sorted comparisons | Top 10 products |

## CUSTOM CHART (ChartCustom) - For Novel Visualizations
Use `<ChartCustom>` when standard charts don't fit or user requests custom visualization.

**Supported Types (type prop):**
| Type | Description | Best For |
|------|-------------|----------|
| `scatter` | Points with custom shapes | Comparing discrete items |
| `bar` | Vertical bars with custom styles | Category comparison |
| `horizontal-bar` | Horizontal bars | Rankings, long labels |
| `line` | Line with custom point shapes | Trends over time |
| `area` | Filled area with custom styling | Cumulative data |
| `pie` | Pie/donut chart | Proportions |
| `pictogram` | Repeating icons (isotype chart) | Making data tangible |
| `lollipop` | Line + shape markers | Clean comparison |
| `waffle` | 10x10 grid chart | Percentages out of 100 |
| `radial` | Circular progress bars | Progress/completion |
| `rose` | Nightingale/coxcomb chart | Direction distribution, cyclical data with magnitude |
| `funnel` | Funnel/conversion chart | Sales pipeline, conversion rates |
| `gauge` | Speedometer/dial | Single value progress |
| `treemap` | Nested rectangles | Hierarchical proportions |

**Custom Shapes (shape prop):**
`water droplet`, `star`, `heart`, `cloud`, `flame`, `leaf`, `diamond`, `hexagon`, `circle`

**Bar Styles (style prop):**
`default`, `rounded`, `pill`, `gradient`, `striped`, `3d`

**ChartCustom Syntax Examples:**
```jsx
// Pictogram with star icons
<ChartCustom type="pictogram" shape="star" data={[{label: "Team A", value: 5}]} colorScheme="purple"/>

// Waffle chart for percentages
<ChartCustom type="waffle" data={[{label: "Complete", value: 73}, {label: "Remaining", value: 27}]}/>

// Rose chart for direction distribution
<ChartCustom type="rose" data={[{label: "N", value: 145}, {label: "NE", value: 98}, {label: "E", value: 67}]} colorScheme="teal"/>

// Radial progress chart
<ChartCustom type="radial" data={[{label: "Sales", value: 75}, {label: "Growth", value: 60}]}/>

// Gauge for single value
<ChartCustom type="gauge" data={[{label: "Performance", value: 85}]} colorScheme="green"/>
```

**ChartCustom Props:**
- `type`: Chart paradigm (see table above)
- `shape`: Custom point/icon shape
- `style`: Bar style variant
- `data`: Array of `{label, value}`
- `colorScheme`: `blue|green|red|purple|orange|teal|pink|rainbow`
- `showGrid`, `showValues`, `donut`: boolean options

## CHART DATA FORMAT (CRITICAL)
Using wrong data properties causes EMPTY charts:

| Component | Required Format | Example |
|-----------|----------------|---------|
| ChartCustom | `{label, value}` | `{label: "Item", value: 50}` |
| ChartArea | `{label, value}` | `{label: "Jan", value: 100}` |
| ChartBar (simple) | `{label, value}` | `{label: "Q1", value: 50}` |
| ChartBar (clustered) | `{label, before, after}` | `{label: "Sales", before: 80, after: 120}` |
| BarStats | `{label, value}` | `{label: "Region A", value: 85}` |
| ChartPie/Doughnut | `{label, value}` | `{label: "Segment", value: 30}` |
| ChartPolar | `{label, value}` | `{label: "Mon", value: 250}` |
| ChartRadar | `{label, value}` | `{label: "Speed", value: 80}` |
| ChartBubble | `{label, x, y, size}` | `{label: "Item", x: 10, y: 20, size: 50}` |

**⚠️ NEVER use arbitrary keys** like `revenue`, `signups`, `sales` - components ignore unknown properties!
- BAD: `data={[{label: "Q1", revenue: 50}]}` ← renders EMPTY
- GOOD: `data={[{label: "Q1", value: 50}]}` ← renders correctly

## CHART LAYOUT RULES
- **ONE chart per slide** - never 2 charts or chart+image together
- Use LayoutSplit to pair chart with explanation text
- Charts work best in: split, dashboard, stacked layouts
- **3+ data points** → use Chart, not multiple BigNum/Metrics"""

    @classmethod
    def get_layout_prompt(cls) -> str:
        """Provide React MDX layout reference for LLM prompts."""
        return """# VISUAL DESIGN INSTRUCTIONS

You are designing slides as MDX markup. Match layout to the visual_design intent.

## LAYOUT DECISIONS

**LayoutCover** — TRADITIONAL cover page: title + subtitle only. Clean, minimal, impactful.
- Best: opening title slide, closing "Thank You" slide, section dividers
- Components: Heading (level 1), Text (subtitle), optionally ONE of: QuoteBlock OR simple Callout
- **🚫 FORBIDDEN on LayoutCover**: BigNum, MetricGroup, SmartList, Charts, Diagrams, CardGroup, ProcessStrip, StepList
- **MAX ELEMENTS**: 2-3 elements total (Heading + subtitle + optional quote/callout)
- Cover pages should feel SPACIOUS and IMPACTFUL, not cramped with data

**LayoutSplit** — Use when pairing text with visual, or showing two related concepts.
- Best: metric + context, chart + explanation, before/after
- Slots: Left, Right | ratio: 1:1, 2:1, 1:2, 3:1, 1:3
- Components: Any combination of Heading, Text, BigNum, SmartList, Charts
- **HEADING RULE**: Use the SAME heading level on both sides (both level={2} or both level={3}). Never mix heading levels in a split layout.
- **DIAGRAM RULE for Split Layouts**:
  - NetworkGraph in ANY split layout should use `direction="TB"` (vertical/top-to-bottom) to maximize height
  - Split columns are narrow → horizontal diagrams look cramped and short
  - Prefer vertical flow diagrams that fill the column height, not width
- **CONTENT PLANNING BY RATIO**:
  - **1:1**: Equal content on both sides (4-5 elements each)
  - **2:1**: Larger side (2) gets main content (5-6 elements); smaller side (1) gets 2-3 supporting elements
  - **1:2**: Smaller side (1) gets 2-3 elements; larger side (2) gets main content (5-6 elements)
  - **3:1 / 1:3**: Large side dominates (6+ elements); small side is accent only (1-2 elements: Heading + Callout or BigNum)
- **RULE**: Match content density to column width. Never cram the small column with as much as the large column.

**LayoutStacked** — Use for text-heavy narrative or sequential content.
- Best: storytelling, explanations, step-by-step instructions
- Components: Heading, Text, SmartList, TableData

**LayoutGrid** — Use for parallel items of equal importance.
- Best: features, team, products, categories
- Slots: Col ×2-4 | cols: 2, 3, 4
- Components: CardGroup, MetricGroup, Heading

**LayoutFullBleed** — Use for visual impact with background image.
- Best: hero moments, emotional beats, section transitions
- Components: Heading, QuoteBlock, BigNum (overlay on image)

**LayoutDashboard** — Use for data-dense KPI displays.
- Best: metrics overview, performance summary, status report
- Slots: Header, Main, Sidebar, Footer
- **Header slot**: Heading level={2} ONLY (no Text, no lead paragraph)
- **Main slot**: Text variant="lead" (first), MetricGroup, Charts, Tables, BigNum
- **Sidebar slot**: SmartList, Callout, compact text (supporting content)
- **AVOID**: Diagram alone in Main (leaves empty space), MetricGroup in Sidebar (too narrow)
- **NOTE**: Dashboard body (Main + Sidebar) is vertically centered; Header stays at top

**LayoutTimeline** — Use for chronological milestones with rich content per event.
- Best: company history, project milestones, annual roadmap with details
- Use when each milestone needs: title + description (rich content)
- Creates horizontal timeline with alternating nodes above/below center line
- **REQUIRED PROPS**: `headline` (string). `subtitle` is optional.
- Slots: LayoutTimeline.Item (with year prop) × 3-6 items
- Components inside Item: Heading level={3}, Text (keep brief)
- **HIGHLIGHT RULE**: You may mark the single MOST IMPORTANT milestone as `highlighted={true}` on that `LayoutTimeline.Item`.
  - Use at most ONE highlighted item per timeline. E.g., the north star, the biggest milestone, the most critical turning point, etc.
- **TEXT VARIANT RULE**: `Text`'s `variant` is optional.
  - Use plain `<Text>...</Text>` for the main body (concise, accurate).
  - Only use `<Text variant="caption">...</Text>` when you truly need a short caption/source note underneath the main text (e.g., emphasizing milestone).
- PREFER over ProcessStrip when milestones need detailed explanations

## CHART & IMAGE EXCLUSIVITY (CRITICAL)

**⚠️ ONE VISUAL ASSET PER SLIDE** — Never place 2 charts, 2 images, or 1 chart + 1 image on the same slide.
- Each slide gets exactly ONE of: Chart OR ImageBlock OR neither
- Pair the single visual with text elements (Heading, Text, SmartList, Callout)
- If you need multiple data views, split them across separate slides

**Why this matters:**
- Multiple visuals compete for attention and confuse the narrative
- Split layouts already have limited width per side
- One focused visual + supporting text = clear communication

## CHART & IMAGE PLACEMENT PATTERNS

**Use LayoutSplit to pair a single visual with explanatory content. Choose side based on content flow:**

| Pattern | When to Use | Layout |
|---------|-------------|--------|
| **Chart-Left** | Data DRIVES the narrative (evidence-first, then explain) | `<Left>Chart</Left><Right>SmartList+Text</Right>` |
| **Chart-Right** | Context FRAMES the data (explain setup, then show proof) | `<Left>Heading+SmartList</Left><Right>Chart</Right>` |
| **Image-Left** | Visual anchors the story (product, diagram, screenshot) | `<Left>ImageBlock</Left><Right>Text+SmartList</Right>` |
| **Image-Right** | Text leads, image supports (description, then show) | `<Left>Heading+Text</Left><Right>ImageBlock</Right>` |

**Detailed Placement Guidelines:**

### Chart-Left (Data-First Pattern)
Use when the data is the PRIMARY message:
- Performance metrics and KPIs being showcased
- Trend reveals ("Look at this growth!")
- Comparison results that speak for themselves
- Before/after demonstrations
```mdx
<LayoutSplit ratio="1:1">
  <Left>
    <ChartBar id="chart_001" data={[...]}/>
    <Text variant="caption">Source: Q4 Report</Text>
  </Left>
  <Right>
    <Heading level={2}>Key Takeaways</Heading>
    <SmartList id="list_001" items={["Insight 1", "Insight 2", "Insight 3"]}/>
    <Callout intent="success">Record-breaking quarter</Callout>
  </Right>
</LayoutSplit>
```

### Chart-Right (Context-First Pattern)
Use when context is needed to INTERPRET the data:
- Complex metrics requiring explanation
- New concepts or unfamiliar metrics
- Building toward a reveal/conclusion
- Stories where the "why" matters before the "what"
```mdx
<LayoutSplit ratio="1:1">
  <Left>
    <Heading level={2}>Understanding Churn Rate</Heading>
    <Text variant="lead">How we measure customer retention</Text>
    <SmartList id="list_001" items={["Monthly active users", "Engagement scoring", "Renewal tracking"]}/>
  </Left>
  <Right>
    <ChartLine id="chart_001" title="12-Month Trend" data={[...]}/>
    <Text variant="caption">Churn decreased 40% after Q2 initiatives</Text>
  </Right>
</LayoutSplit>
```

### Image-Left (Visual-Anchor Pattern)
Use when the image IS the subject:
- Product screenshots or demos
- Architecture diagrams
- Team photos or headshots
- Physical products or locations
```mdx
<LayoutSplit ratio="1:1">
  <Left>
    <ImageBlock src="/product-v2.png" alt="Product interface" size="lg"/>
    <Text variant="caption">New dashboard design</Text>
  </Left>
  <Right>
    <Heading level={2}>Redesigned Experience</Heading>
    <SmartList id="list_001" items={["50% faster navigation", "Unified search", "Dark mode support"]}/>
    <Callout intent="info">Launching Q1 2026</Callout>
  </Right>
</LayoutSplit>
```

### Image-Right (Description-First Pattern)
Use when narrative builds to visual reveal:
- Introducing a new feature or concept first
- Complex systems explained then illustrated
- Stories leading to a visual payoff
```mdx
<LayoutSplit ratio="2:1">
  <Left>
    <Heading level={2}>Next-Gen Architecture</Heading>
    <Text variant="lead">Built for scale from day one</Text>
    <SmartList id="list_001" items={["Microservices backbone", "Edge computing ready", "Auto-scaling clusters"]}/>
    <Text>Our new platform handles 10x the load with half the latency.</Text>
  </Left>
  <Right>
    <ImageBlock src="/architecture-diagram.png" alt="System architecture"/>
  </Right>
</LayoutSplit>
```

## COMPONENT REFERENCE

**⚠️ CONTENT MINIMUM PER SLIDE** (non-negotiable):
- Every slide must have **at least 1 visual block**: BigNum, MetricGroup, Chart, Diagram, CardGroup, TableData, QuoteBlock
- "Visual block" = anything that isn't just Heading/Text/SmartList
- Text-only slides with just Heading + SmartList look INCOMPLETE

**Metrics**: BigNum (hero stat with trend), MetricGroup (3-4 KPIs), MetricStrip (inline row)
**Content**: SmartList (bullet points), CardGroup (feature cards), QuoteBlock, TableData
**Text**: Heading (level 1-3), Text (lead/body/caption), Callout (alerts), Highlight (inline emphasis)

**⭐ PROCESSSTRIP - USE THIS FOR WORKFLOWS/FLOWS** (most common visual element!):
- **ProcessStrip**: Horizontal phases - USE FOR: any A→B→C→D flow, turn sequences, pipelines, stages
- **StepList**: Vertical numbered steps - USE FOR: setup guides, how-to, onboarding flows
- **LayoutTimeline**: Rich chronological milestones - USE FOR: company history with details

**🚫🚫🚫 PROCESSSTRIP WIDTH RULE (CRITICAL - WILL CAUSE OVERFLOW!):**
| Layout Context | Max ProcessStrip Items |
|----------------|------------------------|
| 1:1 split (Left or Right) | **3 items MAX** |
| 1:2 split small side | **2 items MAX** |
| 2:1 split large side | 4 items OK |
| LayoutStacked (full width) | 5+ items OK |
| LayoutDashboard Main | 4 items OK |

**IF YOU HAVE 4+ STEPS IN A 1:1 SPLIT → USE StepList INSTEAD (vertical, fits narrow columns)**

**⚠️⚠️⚠️ STOP! Before using NetworkGraph, ask: "Does ANY node branch to 2+ outputs?"**
- If NO → USE ProcessStrip (linear sequence) - this is 90% of cases!
- If YES → NetworkGraph is OK (true branching graph)
- "Speaker → Capture → Translate → Playback" = ProcessStrip (each step leads to ONE next)
- "Engine → [Interpreter, Captions, Transcription]" = NetworkGraph (Engine branches to 3)

**INLINE HIGHLIGHT**:
Use `<Highlight>` to emphasize key words within text:
```
<Text>We achieved <Highlight color="success">10x growth</Highlight> this quarter.</Text>
<Text>Key metric: <Highlight color="primary" bold>$1.2M revenue</Highlight></Text>
```
Colors: default, primary, success, warning, info, accent

**CHARTS (for numeric data)** - See Chart Documentation section for full details.
- ChartBar: comparison, before/after (use `before`/`after` keys for clustered bars)
- ChartLine: trends over time
- ChartPie: proportions/percentages (use variant="donut" for doughnut style)
- ChartArea: cumulative trends, time-series with volume
- ChartBubble: 3D relationships (x, y, size dimensions)
- ChartRadar: multivariate comparison (4+ attributes per item)
- ChartPolar: cyclical/periodic data
- BarStats: rankings, sorted comparisons
- ChartCustom: novel visualizations (rose, waffle, pictogram, gauge, funnel, treemap, radial)

- **RULE**: 3+ data points → use Chart, not multiple Metrics

## MDX OUTPUT FORMAT

Each slide wrapped in `<Slide>` with metadata:

```mdx
<Slide id="slide_01" rank={1} story="HOOK" atoms={["stat_001"]}>
<LayoutCover theme="dark">
  <Heading level={1}>The Future of AI</Heading>
  <BigNum id="stat_001" value="10B" label="Parameters"/>
</LayoutCover>
</Slide>

<Slide id="slide_02" rank={2} story="TENSION" atoms={["fact_001"]}>
<LayoutSplit ratio="2:1">
  <Left>
    <Heading level={2}>The Challenge</Heading>
    <SmartList id="list_001" items={["Scale", "Cost", "Complexity"]}/>
  </Left>
  <Right>
    <ChartBar id="chart_001" data={[{name: "2023", value: 100}, {name: "2024", value: 250}]}/>
  </Right>
</LayoutSplit>
</Slide>

<Slide id="slide_03" rank={3} story="JOURNEY" atoms={[]}>
<LayoutDashboard>
  <Header><Heading level={2}>Performance</Heading></Header>
  <Main>
    <Text variant="lead">Key metrics showing strong growth this quarter.</Text>
    <MetricGroup id="metrics_001" cols={3}>
      <Metric value="$1.2M" label="Revenue" change={12}/>
      <Metric value="89%" label="Margin"/>
      <Metric value="4.2" label="Rating"/>
    </MetricGroup>
  </Main>
</LayoutDashboard>
</Slide>
```

## COMPONENT SYNTAX

```mdx
// Text with inline highlights
<Heading level={1}>Display Title</Heading>
<Text variant="lead">We achieved <Highlight color="success">10x growth</Highlight> this quarter.</Text>
<Text>Key metric: <Highlight color="primary" bold>$1.2M</Highlight> in revenue.</Text>
<Callout intent="info" title="Note">Content with <Highlight>key terms</Highlight>.</Callout>

// Metrics (must have id for patching)
<BigNum id="stat_001" value="42%" label="Growth" trend="+5%"/>
<MetricGroup id="metrics_001" cols={3}>
  <Metric value="$1M" label="Revenue"/>
</MetricGroup>

// Content (must have id)
<SmartList id="list_001" items={["Item 1", "Item 2"]} ordered={false}/>
<CardGroup id="cards_001" columns={3}>
  <Card title="Speed" description="10x faster" icon="🚀"/>
</CardGroup>
<QuoteBlock id="quote_001" author="CEO">Stay focused.</QuoteBlock>

// ⭐⭐⭐ SEQUENCES - USE THESE OFTEN for any step-by-step content! ⭐⭐⭐
// These are VISUAL BLOCKS that make pages look professional and full!

// ProcessStrip: horizontal phases (PREFER THIS for workflows, pipelines, stages)
// ⚠️ WIDTH RULE: Max 3 items in 1:1 split or smaller. 4+ items need full width or 2:1 large side.
<ProcessStrip id="process_001" items={["Plan", "Build", "Test"]}/>  // 3 items OK in split
// ProcessStrip with status (use in full-width layouts for 4+ items):
<ProcessStrip id="process_002" items={[{label: "Collect", status: "done"}, {label: "Process", status: "active"}, {label: "Validate", status: "pending"}, {label: "Deploy", status: "pending"}]}/>
// USE ProcessStrip for: turn sequences, data pipelines, workflow stages, any A→B→C→D flow

// StepList: vertical numbered steps (BETTER for narrow columns - handles 4+ items well)
<StepList id="steps_001" items={["Collect data", "Process", "Validate", "Deploy"]}/>
// StepList with descriptions:
<StepList id="steps_002" items={[{label: "Plan", description: "Define scope"}, {label: "Build", description: "Implement"}]}/>

// LayoutTimeline: for chronological milestones with rich content (full page layout)
// Use when you need richer content per milestone (heading + text + callout per item)
// ALWAYS provide `headline`; `subtitle` is optional.
<LayoutTimeline headline="Roadmap" subtitle="Key milestones ahead (optional)">
  <LayoutTimeline.Item year="2020">
    <Heading level={3}>Product Launch</Heading>
    <Text>Released v1.0 to market</Text>
    <Text variant="caption">Reach 1M users</Text>  <!-- optional caption highlight the milestone -->
  </LayoutTimeline.Item>
  <LayoutTimeline.Item year="2022">
    <Heading level={3}>Series A</Heading>
    <Text variant="caption">Raised $10M funding</Text>  <!-- optional caption highlight the milestone -->
  </LayoutTimeline.Item>
  <LayoutTimeline.Item year="2024"  highlighted={true}>  <!-- highlighted the most important milestone -->
    <Heading level={3}>Global Expansion</Heading>
    <Text>Launched in 50 countries</Text>
    <Text variant="caption">Opened offices in 10 new cities</Text>  <!-- optional caption highlight the milestone -->
  </LayoutTimeline.Item>
</LayoutTimeline>
// NOTE: ProcessStrip is better for simple year labels; LayoutTimeline is better for detailed milestone stories

// Charts (must have id) - See Chart Documentation for full syntax
// Standard charts:
<ChartBar id="chart_001" title="Revenue" data={[{label: "Q1", value: 100}, {label: "Q2", value: 150}]}/>
<ChartBar id="chart_002" title="Improvements" data={[{label: "Accuracy", before: 65, after: 75}]}/>
<ChartLine id="chart_003" title="Growth" data={[{label: "Jan", value: 50}]}/>
<ChartPie id="chart_004" title="Share" data={[{label: "A", value: 60}]}/>
<ChartArea id="chart_005" title="Trend" data={[{label: "Jan", value: 100}]} gradient={true}/>
<BarStats id="chart_006" title="Rankings" data={[{label: "A", value: 95}]} sortDescending={true}/>
// For custom/novel visualizations: <ChartCustom type="rose|waffle|pictogram|gauge|funnel|treemap|radial" .../>

// Tables
<TableData id="table_001" headers={["Name", "Value"]} rows={[["A", "1"]]}/>

// ⚠️⚠️⚠️ CRITICAL: NetworkGraph vs ProcessStrip DECISION ⚠️⚠️⚠️
// STEP 1: Count how many edges come OUT of each node:
//   - If EVERY node has exactly 0 or 1 outgoing edge → USE ProcessStrip (it's linear!)
//   - If ANY node has 2+ outgoing edges → NetworkGraph is OK (it's branching)
//
// EXAMPLES OF LINEAR (USE ProcessStrip, NOT NetworkGraph):
//   "Speaker → Capture → Translate → Playback" ← each node has 1 output = ProcessStrip!
//   "Input → Process → Judge → Output" ← each node has 1 output = ProcessStrip!
//   "Today → Jan 2026 → Future" ← each node has 1 output = ProcessStrip!
//
// EXAMPLES OF BRANCHING (NetworkGraph OK):
//   "Engine → Interpreter, Captions, Transcription" ← Engine has 3 outputs = NetworkGraph OK
//   "API → Auth AND Cache; both → DB" ← API has 2 outputs = NetworkGraph OK
//
// ⚠️ In Split layouts: ALWAYS use direction="TB" (vertical) - horizontal diagrams look cramped
// ⚠️ SIZE PROP (REQUIRED - count your nodes!):
//   - size="compact": 2-3 nodes ONLY
//   - size="medium": 4-5 nodes ONLY
//   - size="tall": 6+ nodes (MUST use tall if ≥6 nodes!)
// RULE: Count <Node> elements, then pick size. 7 nodes = tall. 4 nodes = medium. 3 nodes = compact.
// Example valid use: API Gateway connects to BOTH Auth AND Cache (branching)
<NetworkGraph id="diagram_001" type="network" direction="TB" size="medium" title="System Architecture">
  <Node id="api" label="API Gateway" className="api" />
  <Node id="auth" label="Auth Service" className="process" />
  <Node id="db" label="Database" className="database" />
  <Node id="cache" label="Cache" className="process" />
  <Edge source="api" target="auth" />
  <Edge source="api" target="cache" />
  <Edge source="auth" target="db" />
  <Edge source="cache" target="db" />
</NetworkGraph>

// For hierarchy/org charts with 6+ nodes - MUST use size="tall":
<NetworkGraph id="diagram_002" type="network" direction="TB" size="tall" title="Org Structure">
  <Group id="frontend" label="Frontend">
    <Node id="web" label="Web App" className="api" />
    <Node id="mobile" label="Mobile App" className="api" />
  </Group>
  <Node id="gateway" label="API Gateway" className="process" />
  <Node id="db" label="Database" className="database" />
  <Edge source="web" target="gateway" />
  <Edge source="mobile" target="gateway" />
  <Edge source="gateway" target="db" />
</NetworkGraph>

## TEXT LIMITS
Display: 6 words | Heading: 8 | Body: 25 | List item: 10 words"""

    @classmethod
    def get_layout_constrain(cls) -> str:
        """Provide compact layout constraints."""
        return """# LAYOUT CONSTRAINTS

## LAYOUT-WIDGET COMPATIBILITY
| Widget | cover | split | stacked | grid | fullbleed | dashboard | timeline |
|--------|-------|-------|---------|------|-----------|-----------|----------|
| Heading | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Text | ✅ | ✅ | ✅ | ⚠️ | ✅ | ❌ | ✅ |
| SmartList | ❌ | ✅ | ✅ | ⚠️ | ❌ | ❌ | ❌ |
| BigNum | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| MetricGroup | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Charts | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| NetworkGraph | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| QuoteBlock | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| CardGroup | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| TableData | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Callout | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| StepList | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| ProcessStrip | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Highlight | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## SLIDE VARIETY (CRITICAL)
**Never use the same layout + component pattern on consecutive slides.**
- If slide N uses LayoutSplit with NetworkGraph+SmartList, slide N+1 MUST use a different layout OR different component types
- Repeating the same visual pattern makes the deck feel monotonous and template-like
- **Good**: Split→Dashboard→Split(different ratio)→Grid→Stacked
- **Bad**: Split(2:1)+Diagram→Split(2:1)+Diagram→Split(2:1)+Diagram
- Vary: layout type, split ratio, primary visual block (Chart vs Diagram vs MetricGroup vs CardGroup)

## SPLIT LAYOUT REQUIREMENTS (CRITICAL)
Split layouts (LayoutSplit) need SUBSTANTIAL content on BOTH sides:
- **Each side must have 4+ elements** (Heading + 2-3 content blocks + supporting text)
- **Both sides must have similar vertical height** so they visually overlap (not a sparse 2x3 grid)
- **Bad example**: Left has Heading+SmartList (2 items), Right has Heading+SmartList → looks like unfinished grid
- **Good example**: Left has Heading+Diagram+Text+Callout, Right has BigNum+MetricGroup+SmartList+Text

ERROR pattern to avoid: "2x3 grid with empty slots" - when split layout has only 2-3 small items per side,
the page looks like a 6-cell grid where half the cells are empty. This makes the slide look unfinished.

### SPLIT LAYOUT REQUIRED STRUCTURE (ALL ELEMENTS REQUIRED):
```
<LayoutSplit ratio="1:1">
  <Left>
    <Heading level={2}>Title Here</Heading>           <!-- Required -->
    <BigNum id="..." value="..." label="..."/>        <!-- Visual block required -->
    <SmartList id="..." items={[...3-4 items...]}/>  <!-- Text block required -->
    <Callout intent="info" title="...">...</Callout>  <!-- Supporting block required -->
  </Left>
  <Right>
    <Heading level={3}>Subtitle Here</Heading>        <!-- Required -->
    <MetricGroup id="..." cols={3}>...</MetricGroup>  <!-- Visual block required -->
    <Text variant="body">Explanation text...</Text>   <!-- Text block required -->
    <Text variant="caption">Source note...</Text>     <!-- Supporting block required -->
  </Right>
</LayoutSplit>
```

If you don't have enough content for 4+ elements per side, use LayoutStacked instead.

## DENSITY GUIDE
| Position | Density | Layout Choices |
|----------|---------|----------------|
| Slide 1 (Opening) | MINIMAL | cover (title + subtitle ONLY, no data) |
| Slide 2 | MODERATE | split, stacked (intro content) |
| Slide 3-8 | DENSE | dashboard, split, timeline, grid (main content) |
| Slide 9 | MODERATE | split, stacked (summary/next steps) |
| Final (Closing) | MINIMAL | cover ("Thank You" or CTA, no data) |

## PAGE COVERAGE REQUIREMENTS (CRITICAL)
**Every page must feel FULL - empty/sparse pages look unfinished and unprofessional**
**Target: Fill 70-85% of visible area with meaningful content**

| Layout | Min Elements | Typical Content Mix |
|--------|--------------|---------------------|
| LayoutCover | 2-3 | Heading + Text(subtitle) + optional QuoteBlock — KEEP IT MINIMAL! |
| LayoutStacked | 6-8 | Heading + Text + MetricGroup + SmartList + Callout + supporting text |
| LayoutDashboard | 8-10 | Header: Heading+Text. Main: MetricGroup + Chart + Text. Sidebar: SmartList + Callout |
| LayoutTimeline | 5-6 | 5-6 timeline items with Heading + Text each |
| LayoutSplit | 10-12 | Each side: Heading + 2 visuals(BigNum+Chart or Metric+List) + Text + Callout |
| LayoutGrid | 6-8 | Heading + Text + CardGroup(4 cards) + Callout or MetricGroup |

**CONTENT RICHNESS RULES** (follow strictly!):
- **Every slide needs at least TWO visual blocks**: BigNum + Chart, or MetricGroup + SmartList, etc.
- **Text-only slides look empty** - always pair text with visuals
- **EXCEPTION: Cover slides ARE "just title + subtitle"** - keep them clean and impactful, NO data
- **Dashboard sidebars can't be empty** - fill with SmartList + Callout + Text
- **Split layouts need BOTH sides full** - 5+ elements per side minimum
- **When in doubt, ADD more content** - sparse pages look unprofessional
- **Use ProcessStrip/StepList for workflows** - they add visual interest without complexity

**ERROR patterns to avoid:**
- Page with only Heading + SmartList (looks incomplete)
- Dashboard with empty Main or Sidebar slots
- Stacked with only 2-3 small elements (gaps visible)
- Cover with only title (add subtitle, quote, or metric)
- Split with one side nearly empty

## RULES
- ≥4 different layouts per deck
- Never same layout twice in a row
- Numbers → BigNum/MetricGroup (not in text)
- ≥3 slides with data components
- Lists max 4 items, body max 25 words
- Split layouts: BOTH sides need visual blocks, not just text
- **NO GAPS**: content should fill the page, not leave holes
- **NO REDUNDANCY**: Never show same data twice (e.g., MetricGroup + BigNum with same numbers)"""

    @classmethod
    def calculate(cls, slides, theme, style):
        """Not implemented - React engine is render-only."""
        raise NotImplementedError(
            "React engine does not use calculate() - use ReactMDXRenderer directly"
        )
