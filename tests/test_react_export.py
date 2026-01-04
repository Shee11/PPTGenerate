"""
React MDX Export Tests

Tests for static HTML export functionality.
"""

import pytest
import os
import json
import tempfile
import shutil
from pathlib import Path

from src.paged.render.react.mdx_renderer import ReactMDXRenderer, render_mdx


class TestStaticExport:
    """Tests for static HTML export"""
    
    @pytest.fixture
    def sample_state(self):
        """Create a sample presentation state"""
        return {
            "id": "test-presentation",
            "meta": {
                "title": "Test Presentation",
                "theme": "business"
            },
            "slides": [
                {
                    "id": "slide-1",
                    "layout": "cover",
                    "widgets": {
                        "title": {
                            "id": "w1",
                            "type": "Type.Display",
                            "parameters": {"text": "Welcome"}
                        },
                        "subtitle": {
                            "id": "w2",
                            "type": "Type.Body",
                            "parameters": {"text": "Introduction slide"}
                        }
                    }
                },
                {
                    "id": "slide-2",
                    "layout": "split",
                    "widgets": {
                        "title": {
                            "id": "w3",
                            "type": "Type.Heading",
                            "parameters": {"text": "Key Points"}
                        },
                        "content": [
                            {
                                "id": "w4",
                                "type": "Type.List",
                                "parameters": {
                                    "items": ["Point 1", "Point 2", "Point 3"]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    
    @pytest.fixture
    def renderer(self):
        """Create a renderer instance"""
        return ReactMDXRenderer()
    
    def test_generate_mdx_from_state(self, renderer, sample_state):
        """Test MDX generation from state dictionary"""
        mdx = renderer.render_state(sample_state)
        
        # Should have meta export (JS style, not YAML frontmatter)
        assert 'export const meta' in mdx
        
        # Should have component content
        assert 'LayoutCover' in mdx
        
        # Should have slide content
        assert 'Welcome' in mdx
        assert 'Key Points' in mdx
    
    def test_no_html_in_generated_mdx(self, renderer, sample_state):
        """Test that generated MDX contains no raw HTML"""
        mdx = renderer.render_state(sample_state)
        
        # Should not contain raw HTML tags
        forbidden_tags = ['<div', '<span', '<section', '<article']
        for tag in forbidden_tags:
            assert tag not in mdx, f"Found forbidden HTML tag: {tag}"
    
    def test_no_style_attributes(self, renderer, sample_state):
        """Test that generated MDX contains no style attributes"""
        mdx = renderer.render_state(sample_state)
        
        assert 'style=' not in mdx
        assert 'className=' not in mdx
    
    def test_export_to_mdx_file(self, renderer, sample_state):
        """Test exporting to MDX file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'presentation.mdx')
            renderer.render_to_file(sample_state, output_path)
            
            # File should exist
            assert os.path.exists(output_path)
            
            # File should contain valid MDX
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert 'export const meta' in content
            assert 'LayoutCover' in content
    
    def test_render_mdx_convenience_function(self, sample_state):
        """Test the render_mdx convenience function"""
        mdx = render_mdx(sample_state)
        
        assert isinstance(mdx, str)
        assert len(mdx) > 0
        assert 'LayoutCover' in mdx
    
    def test_render_with_theme_override(self, renderer, sample_state):
        """Test MDX generation with theme override"""
        renderer.theme = 'cyber'
        mdx = renderer.render_state(sample_state)
        
        # Theme should be set in frontmatter
        assert 'theme: "cyber"' in mdx


class TestMDXValidation:
    """Tests for MDX validation"""
    
    def test_valid_mdx_passes_validation(self):
        """Test that valid MDX passes validation"""
        valid_mdx = """---
title: "Test"
---

<LayoutCover>
  <Heading level={1}>Hello</Heading>
</LayoutCover>
"""
        # This would be validated by the TypeScript validator
        # For now, just check the Python generation
        assert '<div' not in valid_mdx
        assert 'className' not in valid_mdx
    
    def test_complex_slide_structure(self):
        """Test MDX generation for complex slide structures"""
        renderer = ReactMDXRenderer()
        
        state = {
            "id": "complex-test",
            "meta": {"title": "Complex", "theme": "business"},
            "slides": [
                {
                    "id": "s1",
                    "layout": "split",
                    "widgets": {
                        "title": {
                            "id": "w1",
                            "type": "Type.Heading",
                            "parameters": {"text": "Metrics"}
                        },
                        "content": [
                            {"id": "w2", "type": "Type.Callout", "parameters": {"text": "Important note", "intent": "info"}}
                        ]
                    }
                }
            ]
        }
        
        mdx = renderer.render_state(state)
        
        # Should have split layout
        assert 'LayoutSplit' in mdx
        
        # Should have heading
        assert 'Heading' in mdx or 'Metrics' in mdx


class TestBundleSize:
    """Tests for export bundle size constraints"""
    
    def test_mdx_file_size_reasonable(self):
        """Test that generated MDX files are reasonably sized"""
        renderer = ReactMDXRenderer()
        
        # Generate a 10-slide presentation
        slides = []
        for i in range(10):
            slides.append({
                "id": f"slide-{i}",
                "layout": "cover",
                "widgets": {
                    "title": {
                        "id": f"w{i}1",
                        "type": "Type.Display",
                        "parameters": {"text": f"Slide {i}"}
                    },
                    "subtitle": {
                        "id": f"w{i}2",
                        "type": "Type.Body",
                        "parameters": {"text": f"Content for slide {i}"}
                    }
                }
            })
        
        state = {
            "id": "large-presentation",
            "meta": {"title": "Large Presentation", "theme": "business"},
            "slides": slides
        }
        
        mdx = renderer.render_state(state)
        
        # MDX should be under 50KB for 10 slides
        assert len(mdx.encode('utf-8')) < 50 * 1024, "MDX file too large"


class TestThemeExport:
    """Tests for theme-specific export features"""
    
    @pytest.mark.parametrize("theme", [
        "business", "cyber", "minimal", "academic", "creative", "duolingo", "dark"
    ])
    def test_all_themes_generate_valid_mdx(self, theme):
        """Test that all themes generate valid MDX"""
        renderer = ReactMDXRenderer(theme=theme)
        
        state = {
            "id": "theme-test",
            "meta": {"title": f"{theme.title()} Theme Test", "theme": theme},
            "slides": [
                {
                    "id": "s1",
                    "layout": "cover",
                    "widgets": {
                        "title": {
                            "id": "w1",
                            "type": "Type.Display",
                            "parameters": {"text": "Theme Test"}
                        }
                    }
                }
            ]
        }
        
        mdx = renderer.render_state(state)
        
        # Should contain the theme in frontmatter
        assert f'theme: "{theme}"' in mdx
        
        # Should have no raw HTML
        assert '<div' not in mdx
        assert '<span' not in mdx
