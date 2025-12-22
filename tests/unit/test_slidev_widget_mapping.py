"""Unit tests for widget-to-markdown and widget-to-component mapping."""
import pytest


class TestWidgetToMarkdownMapping:
    """Test typography widget rendering to markdown."""
    
    def test_type_display_renders_as_plain_text(self):
        """Verify Type.Display renders as plain text."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Type.Display", "text": "Welcome to Slidev"}
        
        result = renderer._render_widget(widget)
        assert result == "Welcome to Slidev"
        assert "#" not in result  # No markdown heading
    
    def test_type_heading_renders_as_markdown_heading(self):
        """Verify Type.Heading renders as # Heading."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Type.Heading", "text": "Section Title", "level": 1}
        
        result = renderer._render_widget(widget)
        assert result.startswith("# ")
        assert "Section Title" in result
    
    def test_type_body_renders_as_paragraph(self):
        """Verify Type.Body renders as plain paragraph."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Type.Body", "text": "This is body text with **bold** formatting."}
        
        result = renderer._render_widget(widget)
        assert "This is body text" in result
        assert "**bold**" in result  # Markdown preserved
    
    def test_type_list_renders_as_markdown_bullets(self):
        """Verify Type.List renders as bullet list."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Type.List", "items": ["Item 1", "Item 2", "Item 3"]}
        
        result = renderer._render_widget(widget)
        assert "- Item 1" in result
        assert "- Item 2" in result
        assert "- Item 3" in result
    
    def test_type_code_renders_as_code_block(self):
        """Verify Type.Code renders as code block."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Type.Code", "code": "print('hello')", "language": "python"}
        
        result = renderer._render_widget(widget)
        assert "```python" in result
        assert "print('hello')" in result
        assert "```" in result


class TestWidgetToComponentMapping:
    """Test data widget rendering to Vue components."""
    
    def test_data_bignum_renders_as_metric_card(self):
        """Verify Data.BigNum renders as <MetricCard />."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Data.BigNum", "label": "Revenue", "value": "$1.2M", "variant": "primary"}
        
        result = renderer._render_widget(widget)
        assert "<MetricCard" in result
        assert 'label="Revenue"' in result
        assert 'value="$1.2M"' in result
        assert 'variant="primary"' in result
        assert "/>" in result
    
    def test_data_progress_renders_as_progress_bar(self):
        """Verify Data.Progress renders as <ProgressBar />."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        widget = {"type": "Data.Progress", "label": "Completion", "value": 75, "status": "success"}
        
        result = renderer._render_widget(widget)
        assert "<ProgressBar" in result
        assert 'label="Completion"' in result
        assert 'value="75"' in result or ':value="75"' in result
        assert 'status="success"' in result
        assert "/>" in result
