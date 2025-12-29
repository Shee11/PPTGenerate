"""Tests for React MDX Renderer."""
import json
import pytest
from pathlib import Path
from src.paged.render.react.mdx_renderer import ReactMDXRenderer, render_mdx


class TestReactMDXRenderer:
    """Test cases for ReactMDXRenderer class."""
    
    def test_init_default(self):
        """Test default initialization."""
        renderer = ReactMDXRenderer()
        assert renderer.theme == "business"
        assert renderer.output_dir == Path("output")
    
    def test_init_custom(self, tmp_path):
        """Test custom initialization."""
        renderer = ReactMDXRenderer(output_dir=tmp_path, theme="cyber")
        assert renderer.theme == "cyber"
        assert renderer.output_dir == tmp_path
    
    def test_render_cover_slide(self):
        """Test rendering a cover slide."""
        renderer = ReactMDXRenderer()
        slide = {
            "layout": "cover",
            "widgets": {
                "title": {"type": "Type.Display", "parameters": {"text": "Hello World"}},
                "subtitle": {"type": "Type.Body", "parameters": {"text": "Welcome"}}
            }
        }
        
        mdx = renderer.render_slide(slide)
        
        assert "<LayoutCover" in mdx
        assert "<Heading level={1}>Hello World</Heading>" in mdx
        assert "<Text>Welcome</Text>" in mdx
        assert "</LayoutCover>" in mdx
    
    def test_render_split_slide(self):
        """Test rendering a split layout slide."""
        renderer = ReactMDXRenderer()
        slide = {
            "layout": "split",
            "ratio": "2:1",
            "widgets": {
                "left": [
                    {"type": "Type.Heading", "parameters": {"text": "Features"}},
                    {"type": "Type.List", "parameters": {"items": ["Item 1", "Item 2"]}}
                ],
                "right": [
                    {"type": "Type.Chart", "parameters": {"data": [{"label": "Q1", "value": 100}]}}
                ]
            }
        }
        
        mdx = renderer.render_slide(slide)
        
        assert '<LayoutSplit ratio="2:1"' in mdx
        assert "<LayoutSplit.Left>" in mdx
        assert "<LayoutSplit.Right>" in mdx
        assert "<Heading level={2}>Features</Heading>" in mdx
        assert "<SmartList" in mdx
        assert "<ChartBar" in mdx
    
    def test_render_grid_slide(self):
        """Test rendering a grid layout slide."""
        renderer = ReactMDXRenderer()
        slide = {
            "layout": "grid",
            "cols": 3,
            "widgets": {
                "columns": [
                    [{"type": "Type.Body", "parameters": {"text": "Col 1"}}],
                    [{"type": "Type.Body", "parameters": {"text": "Col 2"}}],
                    [{"type": "Type.Body", "parameters": {"text": "Col 3"}}]
                ]
            }
        }
        
        mdx = renderer.render_slide(slide)
        
        assert "<LayoutGrid cols={3}" in mdx
        assert "<LayoutGrid.Col>" in mdx
        assert mdx.count("<LayoutGrid.Col>") == 3
    
    def test_no_html_in_output(self):
        """Test that no raw HTML elements appear in output."""
        renderer = ReactMDXRenderer()
        slide = {
            "layout": "cover",
            "widgets": {
                "title": {"type": "Type.Display", "parameters": {"text": "Test"}},
                "content": {"type": "Type.List", "parameters": {"items": ["A", "B"]}}
            }
        }
        
        mdx = renderer.render_slide(slide)
        
        # No raw HTML elements
        assert "<div" not in mdx
        assert "<span" not in mdx
        assert "<ul" not in mdx
        assert "<li" not in mdx
        assert "<section" not in mdx
    
    def test_no_classname_in_output(self):
        """Test that className attribute never appears in output."""
        renderer = ReactMDXRenderer()
        state = {
            "presentation": {"title": "Test"},
            "slides": [
                {
                    "layout": "split",
                    "widgets": {
                        "left": [{"type": "Type.Heading", "parameters": {"text": "Title"}}],
                        "right": [{"type": "Type.Chart", "parameters": {"data": []}}]
                    }
                }
            ]
        }
        
        mdx = renderer.render_state(state)
        
        assert "className" not in mdx
        assert "class=" not in mdx
    
    def test_no_style_attribute_in_output(self):
        """Test that style attribute never appears in output."""
        renderer = ReactMDXRenderer()
        state = {
            "presentation": {"title": "Test"},
            "slides": [
                {"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "Hi"}}}}
            ]
        }
        
        mdx = renderer.render_state(state)
        
        assert "style=" not in mdx
        assert "style:{" not in mdx
    
    def test_render_state_with_multiple_slides(self):
        """Test rendering complete state with multiple slides."""
        renderer = ReactMDXRenderer()
        state = {
            "presentation": {
                "title": "My Presentation",
                "theme": "business"
            },
            "slides": [
                {"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "Slide 1"}}}},
                {"layout": "split", "widgets": {"left": [{"type": "Type.Body", "parameters": {"text": "Content"}}]}},
            ]
        }
        
        mdx = renderer.render_state(state)
        
        assert 'title: "My Presentation"' in mdx
        assert 'theme: "business"' in mdx
        assert "slideCount: 2" in mdx
        assert "Slide 1" in mdx
        assert "Slide 2" in mdx
    
    def test_render_to_file(self, tmp_path):
        """Test rendering to MDX file."""
        renderer = ReactMDXRenderer(output_dir=tmp_path)
        state = {
            "presentation": {"title": "Test"},
            "slides": [{"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "Hi"}}}}]
        }
        
        output_path = renderer.render_to_file(state, "test.mdx")
        
        assert output_path.exists()
        assert output_path.name == "test.mdx"
        
        content = output_path.read_text()
        assert "<LayoutCover" in content
    
    def test_render_from_file(self, tmp_path):
        """Test rendering from state.json file."""
        # Create state.json
        state_path = tmp_path / "state.json"
        state = {
            "presentation": {"title": "From File"},
            "slides": [{"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "Test"}}}}]
        }
        state_path.write_text(json.dumps(state))
        
        # Render
        renderer = ReactMDXRenderer(output_dir=tmp_path)
        output_path = renderer.render_from_file(state_path, "output.mdx")
        
        assert output_path.exists()
        content = output_path.read_text()
        assert "From File" in content
    
    def test_widget_type_mapping(self):
        """Test all widget type mappings."""
        renderer = ReactMDXRenderer()
        
        # Test heading types
        slide = {"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "H1"}}}}
        mdx = renderer.render_slide(slide)
        assert "<Heading level={1}" in mdx
        
        # Test body/text
        slide = {"layout": "cover", "widgets": {"title": {"type": "Type.Body", "parameters": {"text": "Body"}}}}
        mdx = renderer.render_slide(slide)
        assert "<Text>Body</Text>" in mdx
        
        # Test caption
        slide = {"layout": "cover", "widgets": {"title": {"type": "Type.Caption", "parameters": {"text": "Cap"}}}}
        mdx = renderer.render_slide(slide)
        assert '<Text variant="caption"' in mdx
    
    def test_callout_rendering(self):
        """Test Callout component rendering."""
        renderer = ReactMDXRenderer()
        slide = {
            "layout": "cover",
            "widgets": {
                "title": {
                    "type": "Type.Callout",
                    "parameters": {"intent": "warning", "title": "Alert", "text": "Message"}
                }
            }
        }
        
        mdx = renderer.render_slide(slide)
        
        assert '<Callout intent="warning" title="Alert">' in mdx
        assert "Message</Callout>" in mdx
    
    def test_metric_group_rendering(self):
        """Test MetricGroup component rendering."""
        renderer = ReactMDXRenderer()
        slide = {
            "layout": "cover",
            "widgets": {
                "title": {
                    "type": "Type.MetricGroup",
                    "parameters": {
                        "metrics": [{"value": "$1M", "label": "Revenue"}],
                        "cols": 3
                    }
                }
            }
        }
        
        mdx = renderer.render_slide(slide)
        
        assert "<MetricGroup" in mdx
        assert "cols={3}" in mdx
        assert '"value": "$1M"' in mdx


class TestRenderMDXConvenience:
    """Test cases for render_mdx convenience function."""
    
    def test_render_mdx_returns_string(self):
        """Test that render_mdx returns MDX string."""
        state = {
            "presentation": {"title": "Test"},
            "slides": [{"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "Hi"}}}}]
        }
        
        mdx = render_mdx(state)
        
        assert isinstance(mdx, str)
        assert "<LayoutCover" in mdx
    
    def test_render_mdx_with_theme(self):
        """Test render_mdx with custom theme."""
        state = {
            "presentation": {"title": "Test"},
            "slides": [{"layout": "cover", "widgets": {"title": {"type": "Type.Display", "parameters": {"text": "Hi"}}}}]
        }
        
        mdx = render_mdx(state, theme="cyber")
        
        assert 'theme="cyber"' in mdx


class TestL0Compliance:
    """Integration tests to verify L0 compliance (no forbidden elements/attributes)."""
    
    FORBIDDEN_ELEMENTS = ["div", "span", "section", "ul", "ol", "li", "table", "tr", "td", "th"]
    FORBIDDEN_ATTRIBUTES = ["className", "class", "style"]
    
    def test_comprehensive_slide_no_l0_elements(self):
        """Test complex slide has no L0 elements."""
        renderer = ReactMDXRenderer()
        state = {
            "presentation": {"title": "Complex"},
            "slides": [
                {
                    "layout": "cover",
                    "widgets": {
                        "title": {"type": "Type.Display", "parameters": {"text": "Welcome"}},
                        "subtitle": {"type": "Type.Body", "parameters": {"text": "To our presentation"}}
                    }
                },
                {
                    "layout": "split",
                    "ratio": "2:1",
                    "widgets": {
                        "left": [
                            {"type": "Type.Heading", "parameters": {"text": "Features"}},
                            {"type": "Type.List", "parameters": {"items": ["Fast", "Easy", "Powerful"]}}
                        ],
                        "right": [
                            {"type": "Type.Chart", "parameters": {"data": [{"label": "Q1", "value": 100}]}}
                        ]
                    }
                },
                {
                    "layout": "grid",
                    "cols": 3,
                    "widgets": {
                        "columns": [
                            [{"type": "Type.MetricGroup", "parameters": {"metrics": [{"value": "100%", "label": "Uptime"}], "cols": 1}}],
                            [{"type": "Type.Callout", "parameters": {"intent": "info", "text": "Note"}}],
                            [{"type": "Type.Body", "parameters": {"text": "Details"}}]
                        ]
                    }
                }
            ]
        }
        
        mdx = renderer.render_state(state)
        
        # Check no forbidden elements
        for element in self.FORBIDDEN_ELEMENTS:
            assert f"<{element}" not in mdx.lower(), f"Found forbidden element: {element}"
        
        # Check no forbidden attributes
        for attr in self.FORBIDDEN_ATTRIBUTES:
            assert attr not in mdx, f"Found forbidden attribute: {attr}"
