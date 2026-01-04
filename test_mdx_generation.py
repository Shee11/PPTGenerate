"""Quick test of MDX generation pipeline."""

from src.paged.layout.react.mdx_parser import parse_slides_from_mdx, parse_patches, apply_patches

# Test MDX generation parsing
mdx_output = '''
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
'''

print("=" * 60)
print("TEST 1: Parse MDX Slides")
print("=" * 60)

slides = parse_slides_from_mdx(mdx_output)
print(f"✓ Parsed {len(slides)} slides\n")

for s in slides:
    print(f"Slide: {s.id}")
    print(f"  rank: {s.rank}")
    print(f"  story: {s.story}")
    print(f"  atoms: {s.atoms}")
    print(f"  mdx preview: {s.mdx[:80]}...")
    print()

print("=" * 60)
print("TEST 2: Parse Patches")
print("=" * 60)

patch_output = '''
<Patch id="stat_001">
  <BigNum id="stat_001" value="50B" label="Updated Parameters" trend="+400%"/>
</Patch>

<Patch id="list_001">
  <SmartList id="list_001" items={["New Scale", "Lower Cost", "Simpler"]}/>
</Patch>
'''

patches = parse_patches(patch_output)
print(f"✓ Parsed {len(patches)} patches\n")

for p in patches:
    print(f"Patch target: {p.id}")
    print(f"  content: {p.content[:60]}...")
    print()

print("=" * 60)
print("TEST 3: Apply Patches")
print("=" * 60)

slide_dicts = [{"id": s.id, "mdx": s.mdx} for s in slides]
updated = apply_patches(slide_dicts, patches, verbose=True)

print(f"\n✓ Applied patches to {len(updated)} slides")

# Verify patches were applied
slide1_mdx = updated[0]["mdx"]
slide2_mdx = updated[1]["mdx"]

print("\nVerification:")
if 'value="50B"' in slide1_mdx:
    print("  ✓ stat_001 updated to 50B")
else:
    print("  ✗ stat_001 NOT updated")

if "New Scale" in slide2_mdx:
    print("  ✓ list_001 updated with new items")
else:
    print("  ✗ list_001 NOT updated")

print("\n" + "=" * 60)
print("TEST 4: Renderer MDX Passthrough")
print("=" * 60)

from src.paged.render.react.mdx_renderer import ReactMDXRenderer

renderer = ReactMDXRenderer(theme="business")

# Test with mdx field directly
slide_with_mdx = {
    "id": "slide_01",
    "mdx": '<LayoutCover><Heading level={1}>Direct MDX</Heading></LayoutCover>'
}

result = renderer.render_slide(slide_with_mdx)
print(f"Input mdx field: {slide_with_mdx['mdx'][:50]}...")
print(f"Output (should match): {result[:50]}...")

if result == slide_with_mdx["mdx"]:
    print("✓ MDX passthrough working - no conversion needed!")
else:
    print("✗ MDX was modified (unexpected)")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
