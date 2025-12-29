# Patch Format Contract

## Overview

For refinement operations, LLM outputs `<Patch>` elements that target specific widget IDs.

## Patch Element Structure

```xml
<Patch id="target_element_id">
  <!-- New MDX content for this element -->
</Patch>
```

## Example Patch Output

Given existing slide:
```mdx
<LayoutSplit ratio="2:1">
  <Left>
    <Heading level={2}>Performance</Heading>
  </Left>
  <Right>
    <BigNum id="stat_001" value="42%" label="Growth"/>
  </Right>
</LayoutSplit>
```

User instruction: "Update the growth stat to 95%"

LLM outputs:
```xml
<Patch id="stat_001">
  <BigNum value="95%" label="Growth" trend="+53%"/>
</Patch>
```

## Multiple Patches

LLM can output multiple patches in one response:

```xml
<Patch id="stat_001">
  <BigNum value="95%" label="Uptime"/>
</Patch>

<Patch id="list_001">
  <SmartList items={["New item 1", "New item 2", "New item 3"]}/>
</Patch>

<Patch id="chart_001">
  <ChartBar data={[{name: "2024", value: 300}]} title="Updated Chart"/>
</Patch>
```

## Patch Application Algorithm

```python
def apply_patches(slide_mdx: str, patches: List[Patch]) -> str:
    for patch in patches:
        # Find element with matching id
        pattern = rf'<(\w+)\s+[^>]*id="{patch.id}"[^>]*>.*?</\1>|<(\w+)\s+[^>]*id="{patch.id}"[^>]*/>'
        # Replace with patch content
        slide_mdx = re.sub(pattern, patch.content, slide_mdx, flags=re.DOTALL)
    return slide_mdx
```

## Patch Parsing

Extract patches from LLM response:

```python
def parse_patches(response: str) -> List[Patch]:
    pattern = r'<Patch\s+id="([^"]+)">(.*?)</Patch>'
    matches = re.findall(pattern, response, re.DOTALL)
    return [Patch(id=m[0], content=m[1].strip()) for m in matches]
```

## Edge Cases

### Element Not Found
If patch targets non-existent ID:
- Log warning
- Skip patch
- Continue with remaining patches

### Malformed Patch
If patch content is invalid MDX:
- Log error with context
- Skip patch
- Return original content

### Nested Elements
Patches replace the entire element including children:

```xml
<!-- Before -->
<MetricGroup id="metrics_001" cols={3}>
  <Metric value="$1M" label="Revenue"/>
  <Metric value="50%" label="Margin"/>
</MetricGroup>

<!-- Patch -->
<Patch id="metrics_001">
  <MetricGroup cols={2}>
    <Metric value="$2M" label="Revenue" change={100}/>
    <Metric value="75%" label="Margin" change={25}/>
  </MetricGroup>
</Patch>

<!-- After -->
<MetricGroup cols={2}>
  <Metric value="$2M" label="Revenue" change={100}/>
  <Metric value="75%" label="Margin" change={25}/>
</MetricGroup>
```

## Validation

- [ ] Patch `id` attribute is present
- [ ] Patch content is non-empty
- [ ] Patch content is valid JSX
- [ ] Target element exists in slide (warning if not)
