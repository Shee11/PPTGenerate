"""React MDX layout engine - prompt components for LLM content generation."""


class ReactLayoutEngine:
    """Layout engine for React MDX presentations with semantic components."""
    
    @classmethod
    def get_layout_prompt(cls) -> str:
        """Provide React MDX layout reference for LLM prompts."""
        return """# VISUAL DESIGN INSTRUCTIONS

You are designing slides as MDX markup. Match layout to the visual_design intent.

## LAYOUT DECISIONS

**LayoutCover** — Use for opening, closing, or section breaks. Center a bold statement.
- Best: hero number, dramatic quote, single takeaway
- Components: Heading, BigNum, QuoteBlock

**LayoutSplit** — Use when pairing text with visual, or showing two related concepts.
- Best: metric + context, image + explanation, before/after
- Slots: Left, Right | ratio: 1:1, 2:1, 1:2, 3:1, 1:3
- Components: Any combination of Heading, Text, BigNum, SmartList, Charts, ImageBlock

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
- Components: MetricGroup, MetricStrip, Charts, BigNum

**LayoutTimeline** — Use for chronological or sequential flow.
- Best: history, roadmap, process, milestones
- Slots: Item ×n
- Components: Heading, Text, SmartList

## COMPONENT REFERENCE

**Metrics**: BigNum (hero stat with trend), MetricGroup (3-4 KPIs), MetricStrip (inline row)
**Content**: SmartList (bullets), CardGroup (feature cards), QuoteBlock, TableData, ImageBlock
**Charts**: ChartBar (comparison), ChartLine (trends), ChartPie (proportions)
**Diagrams**: Diagram (Mermaid code), ProcessDiagram (input→steps→output), Flowchart (step sequence)
**Text**: Heading (level 1-3), Text (lead/body/caption), Callout (alerts)

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
// Text
<Heading level={1}>Display Title</Heading>
<Text variant="lead">Lead paragraph</Text>
<Callout intent="info" title="Note">Content</Callout>

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

// Charts (must have id)
<ChartBar id="chart_001" title="Revenue" data={[{name: "Q1", value: 100}]}/>
<ChartLine id="chart_002" title="Growth" data={[{name: "Jan", value: 50}]}/>
<ChartPie id="chart_003" title="Share" data={[{name: "A", value: 60}]}/>

// Media
<ImageBlock id="img_001" src="/image.png" alt="Description"/>
<TableData id="table_001" headers={["Name", "Value"]} rows={[["A", "1"]]}/>

// Diagrams (use for processes, architectures, flows)
<Diagram id="diagram_001" title="Architecture" code={`graph LR
  A[Input] --> B[Process]
  B --> C[Output]
`}/>
<ProcessDiagram id="process_001" title="Pipeline" input="Raw Data" output="Clean Data" steps={["Validate", "Transform", "Load"]}/>
<Flowchart id="flow_001" title="Workflow" steps={[{id: "A", label: "Start"}, {id: "B", label: "End"}]}/>
```

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
| SmartList | ❌ | ✅ | ✅ | ⚠️ | ❌ | ❌ | ✅ |
| BigNum | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| MetricGroup | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Charts | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Diagram | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| QuoteBlock | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| CardGroup | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| TableData | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| ImageBlock | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |

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
| Slide 1-2 | SPARSE | cover, fullbleed |
| Slide 3-4 | MODERATE | split, stacked |
| Slide 5-8 | DENSE | dashboard, grid, timeline |
| Slide 9-10 | MODERATE | split, stacked |
| Final | SPARSE | cover, fullbleed |

## PAGE COVERAGE REQUIREMENTS (CRITICAL)
**Every page must have ≥70% content coverage - no sparse/empty-looking pages**

| Layout | Min Elements | Min Coverage | Must Include |
|--------|--------------|--------------|--------------|
| LayoutStacked | 4 | 70% | Heading + 2 content blocks + support |
| LayoutDashboard | 5 | 70% | Header content + Main visual + Sidebar list |
| LayoutTimeline | 4 | 70% | Heading + 3+ timeline items |
| LayoutSplit | 8 (4/side) | 70% | Each side: Heading + visual + text + support |

**ERROR patterns to avoid:**
- Page with only Heading + SmartList (looks incomplete)
- Dashboard with empty Main or Sidebar slots
- Stacked with only 2-3 small elements (gaps visible)

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
