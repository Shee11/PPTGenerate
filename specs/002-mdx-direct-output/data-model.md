# Data Model: MDX Direct Output

## Slide State (react-mdx project)

```typescript
interface SlideState {
  // Metadata (patched via JSON)
  id: string;           // e.g., "slide_01"
  rank: number;         // Display order (1-based)
  story: "HOOK" | "TENSION" | "JOURNEY" | "REVELATION" | "CLOSE";
  atoms: string[];      // Referenced atom IDs from source material
  
  // Content (MDX string)
  mdx: string;          // Raw MDX markup
}
```

## MDX Content Structure

Each slide's `mdx` field contains a complete slide layout:

```mdx
<LayoutSplit ratio="2:1">
  <Left>
    <Heading level={1}>Revenue Growth</Heading>
    <Text>Our Q4 performance exceeded expectations</Text>
  </Left>
  <Right>
    <BigNum id="stat_revenue" value="$2.4M" label="Total Revenue" trend="+23%"/>
  </Right>
</LayoutSplit>
```

### Element IDs

Widget elements that may be patched MUST have `id` attributes:

```mdx
<BigNum id="stat_001" value="42%" label="Growth"/>
<MetricGroup id="metrics_001" cols={3}>
  ...
</MetricGroup>
```

## Patch Operation

```typescript
interface PatchOperation {
  id: string;           // Target element ID (matches id attribute in MDX)
  content: string;      // New MDX content for that element
}
```

### Patch Format in LLM Output

```xml
<Patch id="stat_001">
  <BigNum value="95%" label="Uptime" trend="+5%"/>
</Patch>

<Patch id="metrics_001">
  <MetricGroup cols={2}>
    <Metric value="$1.2M" label="Revenue"/>
    <Metric value="89%" label="Margin"/>
  </MetricGroup>
</Patch>
```

## State Transitions

### New Slide Generation

```
Input:  atoms + user_instruction
LLM:    Generates complete MDX per slide
Output: [{ id, rank, story, atoms, mdx }, ...]
```

### Refinement (Patch)

```
Input:  existing_slides + user_instruction
LLM:    Generates <Patch id="...">...</Patch> blocks
Output: Patches applied to matching elements in slide.mdx
```

## Migration Path

### JSON Mode (slidev)
```json
{
  "id": "slide_01",
  "layout": "split",
  "widgets": {
    "Left": {"type": "Type.Heading", "parameters": {"text": "Title"}},
    "Right": {"type": "Data.BigNum", "parameters": {"value": "42%"}}
  }
}
```

### MDX Mode (react-mdx)
```json
{
  "id": "slide_01",
  "mdx": "<LayoutSplit ratio=\"1:1\"><Left><Heading>Title</Heading></Left><Right><BigNum value=\"42%\"/></Right></LayoutSplit>"
}
```

## Validation Rules

1. **MDX Syntax**: Must be valid JSX (parseable)
2. **Required IDs**: All patchable elements must have `id` attribute
3. **Component Names**: Must match available React components
4. **Layout Structure**: Must use Layout components as root
