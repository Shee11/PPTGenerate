"""Unit tests for MDX parser module."""

import pytest
from src.paged.layout.react.mdx_parser import (
    parse_slides_from_mdx,
    parse_patches,
    apply_patches,
    ParsedSlide,
    PatchOperation,
)


class TestParseSlides:
    """Tests for parse_slides_from_mdx()."""
    
    def test_parse_single_slide(self):
        """Parse a single slide with all attributes."""
        mdx = '''
        <Slide id="slide_01" rank={1} story="HOOK" atoms={["stat_001", "stat_002"]}>
          <LayoutCover>
            <Heading level={1}>Welcome</Heading>
          </LayoutCover>
        </Slide>
        '''
        
        slides = parse_slides_from_mdx(mdx)
        
        assert len(slides) == 1
        assert slides[0].id == "slide_01"
        assert slides[0].rank == 1
        assert slides[0].story == "HOOK"
        assert slides[0].atoms == ["stat_001", "stat_002"]
        assert "<LayoutCover>" in slides[0].mdx
        assert "<Heading" in slides[0].mdx
    
    def test_parse_multiple_slides(self):
        """Parse multiple slides in sequence."""
        mdx = '''
        <Slide id="slide_01" rank={1} story="HOOK" atoms={[]}>
          <LayoutCover><Heading>Title</Heading></LayoutCover>
        </Slide>
        
        <Slide id="slide_02" rank={2} story="TENSION" atoms={["fact_001"]}>
          <LayoutSplit ratio="2:1">
            <Left><Text>Content</Text></Left>
            <Right><BigNum value="42%"/></Right>
          </LayoutSplit>
        </Slide>
        '''
        
        slides = parse_slides_from_mdx(mdx)
        
        assert len(slides) == 2
        assert slides[0].id == "slide_01"
        assert slides[1].id == "slide_02"
        assert slides[1].atoms == ["fact_001"]
    
    def test_parse_slide_with_empty_atoms(self):
        """Parse slide with empty atoms array."""
        mdx = '<Slide id="s1" rank={1} story="HOOK" atoms={[]}><Content/></Slide>'
        
        slides = parse_slides_from_mdx(mdx)
        
        assert slides[0].atoms == []
    
    def test_parse_slide_preserves_mdx_content(self):
        """Verify MDX content is preserved exactly (whitespace trimmed)."""
        content = '''<LayoutDashboard>
  <Header><Heading>Dashboard</Heading></Header>
  <Main><MetricGroup cols={3}>
    <Metric value="$1M"/>
  </MetricGroup></Main>
</LayoutDashboard>'''
        
        mdx = f'<Slide id="s1" rank={{1}} story="JOURNEY" atoms={{[]}}>{content}</Slide>'
        
        slides = parse_slides_from_mdx(mdx)
        
        assert slides[0].mdx == content.strip()
    
    def test_parse_slide_missing_optional_attrs(self):
        """Parse slide with minimal attributes, defaults applied."""
        mdx = '<Slide id="s1"><Content/></Slide>'
        
        slides = parse_slides_from_mdx(mdx)
        
        assert slides[0].id == "s1"
        assert slides[0].rank == 1  # Default
        assert slides[0].story == ""  # Default
        assert slides[0].atoms == []  # Default
    
    def test_parse_no_slides_returns_empty(self):
        """Return empty list when no slides found."""
        mdx = "Just some text without any Slide elements"
        
        slides = parse_slides_from_mdx(mdx)
        
        assert slides == []


class TestParsePatches:
    """Tests for parse_patches()."""
    
    def test_parse_single_patch(self):
        """Parse a single patch operation."""
        output = '''
        <Patch id="stat_001">
          <BigNum value="95%" label="Updated"/>
        </Patch>
        '''
        
        patches = parse_patches(output)
        
        assert len(patches) == 1
        assert patches[0].id == "stat_001"
        assert '<BigNum value="95%"' in patches[0].content
    
    def test_parse_multiple_patches(self):
        """Parse multiple patch operations."""
        output = '''
        <Patch id="stat_001">
          <BigNum value="50%"/>
        </Patch>
        
        <Patch id="list_001">
          <SmartList items={["A", "B", "C"]}/>
        </Patch>
        '''
        
        patches = parse_patches(output)
        
        assert len(patches) == 2
        assert patches[0].id == "stat_001"
        assert patches[1].id == "list_001"
    
    def test_parse_patch_with_complex_content(self):
        """Parse patch with nested elements."""
        output = '''
        <Patch id="metrics_001">
          <MetricGroup cols={2}>
            <Metric value="$1.2M" label="Revenue"/>
            <Metric value="89%" label="Margin"/>
          </MetricGroup>
        </Patch>
        '''
        
        patches = parse_patches(output)
        
        assert len(patches) == 1
        assert "MetricGroup" in patches[0].content
        assert "Metric value" in patches[0].content
    
    def test_parse_no_patches_returns_empty(self):
        """Return empty list when no patches found."""
        output = "Some text without any patches"
        
        patches = parse_patches(output)
        
        assert patches == []


class TestApplyPatches:
    """Tests for apply_patches()."""
    
    def test_apply_single_patch(self):
        """Apply one patch to matching element."""
        slides = [{
            'id': 'slide_01',
            'mdx': '''<LayoutSplit>
  <Left><BigNum id="stat_001" value="42%" label="Old"/></Left>
  <Right><Text>Context</Text></Right>
</LayoutSplit>'''
        }]
        
        patches = [PatchOperation(
            id="stat_001",
            content='<BigNum id="stat_001" value="95%" label="New"/>'
        )]
        
        result = apply_patches(slides, patches)
        
        assert 'value="95%"' in result[0]['mdx']
        assert 'label="New"' in result[0]['mdx']
        assert 'value="42%"' not in result[0]['mdx']
    
    def test_apply_multiple_patches(self):
        """Apply multiple patches to same slide."""
        slides = [{
            'id': 'slide_01',
            'mdx': '''<Layout>
  <BigNum id="stat_001" value="10"/>
  <BigNum id="stat_002" value="20"/>
</Layout>'''
        }]
        
        patches = [
            PatchOperation(id="stat_001", content='<BigNum id="stat_001" value="100"/>'),
            PatchOperation(id="stat_002", content='<BigNum id="stat_002" value="200"/>'),
        ]
        
        result = apply_patches(slides, patches)
        
        assert 'value="100"' in result[0]['mdx']
        assert 'value="200"' in result[0]['mdx']
    
    def test_apply_patch_to_self_closing_element(self):
        """Apply patch to self-closing element."""
        slides = [{
            'id': 'slide_01',
            'mdx': '<Layout><BigNum id="stat_001" value="old" /></Layout>'
        }]
        
        patches = [PatchOperation(
            id="stat_001",
            content='<BigNum id="stat_001" value="new" />'
        )]
        
        result = apply_patches(slides, patches)
        
        assert 'value="new"' in result[0]['mdx']
    
    def test_apply_patch_not_found_unchanged(self):
        """Leave slide unchanged if patch target not found."""
        original_mdx = '<Layout><BigNum id="other" value="keep"/></Layout>'
        slides = [{'id': 'slide_01', 'mdx': original_mdx}]
        
        patches = [PatchOperation(
            id="nonexistent",
            content='<BigNum value="ignored"/>'
        )]
        
        result = apply_patches(slides, patches)
        
        assert result[0]['mdx'] == original_mdx
    
    def test_apply_patches_across_multiple_slides(self):
        """Apply patches distributed across multiple slides."""
        slides = [
            {'id': 'slide_01', 'mdx': '<BigNum id="stat_001" value="A"/>'},
            {'id': 'slide_02', 'mdx': '<BigNum id="stat_002" value="B"/>'},
        ]
        
        patches = [
            PatchOperation(id="stat_001", content='<BigNum id="stat_001" value="A2"/>'),
            PatchOperation(id="stat_002", content='<BigNum id="stat_002" value="B2"/>'),
        ]
        
        result = apply_patches(slides, patches)
        
        assert 'value="A2"' in result[0]['mdx']
        assert 'value="B2"' in result[1]['mdx']
    
    def test_apply_patches_preserves_other_fields(self):
        """Verify non-mdx fields are preserved."""
        slides = [{
            'id': 'slide_01',
            'rank': 1,
            'story': 'HOOK',
            'atoms': ['a1'],
            'mdx': '<BigNum id="x" value="old"/>'
        }]
        
        patches = [PatchOperation(id="x", content='<BigNum id="x" value="new"/>')]
        
        result = apply_patches(slides, patches)
        
        assert result[0]['id'] == 'slide_01'
        assert result[0]['rank'] == 1
        assert result[0]['story'] == 'HOOK'
        assert result[0]['atoms'] == ['a1']
