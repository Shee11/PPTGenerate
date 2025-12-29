# MDX Output Contract

## LLM Output Format (New Slide Generation)

When `project=react-mdx`, LLM outputs slides as MDX blocks:

```
<Slide id="slide_01" rank={1} story="HOOK" atoms={["stat_001", "stat_002"]}>
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
```

## Slide Wrapper Element

Each slide is wrapped in a `<Slide>` element with metadata attributes:

```typescript
interface SlideElement {
  id: string;           // Unique identifier
  rank: number;         // Display order
  story: string;        // Story arc position
  atoms: string[];      // Referenced atom IDs
  children: JSX;        // Layout component with content
}
```

## Layout Components

Root element inside `<Slide>` must be a Layout component:

| Layout | Required Props | Optional Props | Slots |
|--------|----------------|----------------|-------|
| LayoutCover | - | theme, vibe | children |
| LayoutSplit | ratio | - | Left, Right |
| LayoutStacked | - | align | children |
| LayoutGrid | cols | - | Col (children) |
| LayoutFullBleed | image | overlay, align, valign | children |
| LayoutDashboard | - | variant | Header, Main, Sidebar, Footer |
| LayoutTimeline | - | - | Item (children) |

## Content Components

### L2 Blocks (must have `id` for patching)

```mdx
<BigNum id="stat_001" value="42%" label="Growth" trend="+5%"/>

<MetricGroup id="metrics_001" cols={3}>
  <Metric value="$1.2M" label="Revenue" change={12}/>
  <Metric value="89%" label="Margin"/>
</MetricGroup>

<SmartList id="list_001" items={["Item 1", "Item 2"]} ordered={false}/>

<CardGroup id="cards_001" columns={3}>
  <Card title="Speed" description="10x faster" icon="🚀"/>
</CardGroup>

<ChartBar id="chart_001" title="Revenue" data={[{name: "Q1", value: 100}]}/>

<QuoteBlock id="quote_001" author="Steve Jobs">
  Stay hungry, stay foolish.
</QuoteBlock>

<TableData id="table_001" headers={["Name", "Value"]} rows={[["A", "1"]]}/>

<ImageBlock id="img_001" src="/path/to/image.png" alt="Description"/>
```

### L3 Atoms (inline, no ID needed)

```mdx
<Heading level={1}>Display Title</Heading>
<Heading level={2}>Section Title</Heading>
<Text variant="lead">Lead paragraph</Text>
<Text>Body text</Text>
<Callout intent="info" title="Note">Important information</Callout>
```

## Parsing Contract

Parser extracts:
1. `<Slide ...>` elements → slide metadata + mdx content
2. Content between `<Slide>` tags → stored in `mdx` field
3. Attributes from `<Slide>` → stored as slide properties

## Validation

- [ ] Each `<Slide>` has required attributes: id, rank, story
- [ ] Each slide has exactly one Layout component as root
- [ ] All L2 blocks have `id` attribute
- [ ] Component names match available React components
- [ ] JSX syntax is valid (parseable)
