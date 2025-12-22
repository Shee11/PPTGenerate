"""Integration tests for Slidev layout documentation with LLM prompts."""
import pytest
from src.paged.layout.slidev.layout_engine import SlidevLayoutEngine


class TestLayoutDocumentationIntegration:
    """Test that layout documentation works for LLM prompt integration."""
    
    def test_documentation_sufficient_length(self):
        """Verify documentation is comprehensive enough for LLM context."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        assert len(docs) > 500, "Documentation should be >500 chars for LLM context"
    
    def test_documentation_contains_all_layout_slot_names(self):
        """Verify each layout has slot names documented."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        # Smart Grid
        assert "smart-grid" in docs.lower()
        assert "header" in docs.lower()
        assert ("col1" in docs.lower() or "col2" in docs.lower() or 
                "col3" in docs.lower() or "col4" in docs.lower())
        
        # Hero Split
        assert "hero-split" in docs.lower()
        assert "left" in docs.lower()
        assert "right" in docs.lower()
        
        # Full Bleed
        assert "full-bleed" in docs.lower()
    
    def test_documentation_has_widget_to_component_mappings(self):
        """Verify widget type to component mappings are present."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        # Typography widgets → markdown
        assert "Type.Display" in docs or "type.display" in docs.lower()
        assert "Type.Heading" in docs or "type.heading" in docs.lower()
        assert "Type.Body" in docs or "type.body" in docs.lower()
        
        # Data widgets → components
        assert "Data.BigNum" in docs or "data.bignum" in docs.lower()
        assert ("MetricCard" in docs or "metriccard" in docs.lower())
    
    def test_documentation_describes_theme_characteristics(self):
        """Verify themes are described with visual characteristics."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        # Business theme
        assert "business" in docs.lower()
        assert ("#2563eb" in docs or "blue" in docs.lower())
        
        # Cyber theme
        assert "cyber" in docs.lower()
        assert ("#00ffa3" in docs or "green" in docs.lower() or "neon" in docs.lower())
    
    def test_documentation_has_example_json_structure(self):
        """Verify documentation includes example JSON showing slot names as keys."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        # Should show that widgets use slot names as keys
        assert "widgets" in docs.lower()
        # Look for JSON-like structure or guidance
        assert ("{" in docs or "dictionary" in docs.lower() or "mapping" in docs.lower())
