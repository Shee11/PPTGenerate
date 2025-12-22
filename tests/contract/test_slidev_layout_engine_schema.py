"""Contract tests for SlidevLayoutEngine protocol compliance."""
import pytest
from src.paged.layout.slidev.layout_engine import SlidevLayoutEngine


class TestSlidevLayoutEngineProtocol:
    """Test that SlidevLayoutEngine implements LayoutEngine protocol correctly."""
    
    def test_has_get_layout_documentation_classmethod(self):
        """Verify SlidevLayoutEngine has get_layout_documentation classmethod."""
        assert hasattr(SlidevLayoutEngine, 'get_layout_documentation')
        assert callable(getattr(SlidevLayoutEngine, 'get_layout_documentation'))
    
    def test_has_calculate_classmethod(self):
        """Verify SlidevLayoutEngine has calculate classmethod."""
        assert hasattr(SlidevLayoutEngine, 'calculate')
        assert callable(getattr(SlidevLayoutEngine, 'calculate'))
    
    def test_calculate_raises_not_implemented_error(self):
        """Verify calculate() raises NotImplementedError with guidance message."""
        with pytest.raises(NotImplementedError) as exc_info:
            SlidevLayoutEngine.calculate(None, None, None)
        
        error_message = str(exc_info.value)
        assert "Slidev engine does not use calculate()" in error_message
        assert "use SlidevRenderer directly" in error_message


class TestSlidevLayoutDocumentationSchema:
    """Test that layout documentation contains required keywords and structure."""
    
    def test_documentation_contains_layout_names(self):
        """Verify output contains all required layout names."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        assert "smart-grid" in docs.lower()
        assert "hero-split" in docs.lower()
        assert "full-bleed" in docs.lower()
    
    def test_documentation_contains_widget_types(self):
        """Verify output contains widget type prefixes."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        assert "Type.Display" in docs or "type.display" in docs.lower()
        assert "Type.Heading" in docs or "type.heading" in docs.lower()
        assert "Data.BigNum" in docs or "data.bignum" in docs.lower()
    
    def test_documentation_contains_theme_names(self):
        """Verify output contains both theme names."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        assert "business" in docs.lower()
        assert "cyber" in docs.lower()
    
    def test_documentation_minimum_length(self):
        """Verify documentation is comprehensive (>500 chars)."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        assert len(docs) > 500, f"Documentation too short: {len(docs)} chars"
    
    def test_documentation_contains_slot_names(self):
        """Verify documentation describes slot names for layouts."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        # Smart Grid slots
        assert "header" in docs.lower()
        assert "col1" in docs.lower() or "col2" in docs.lower()
        
        # Hero Split slots
        assert "left" in docs.lower() or "right" in docs.lower()
    
    def test_documentation_contains_component_mappings(self):
        """Verify documentation includes widget-to-component mappings."""
        docs = SlidevLayoutEngine.get_layout_documentation()
        
        assert "MetricCard" in docs or "metriccard" in docs.lower()
        assert "ProgressBar" in docs or "progressbar" in docs.lower()
        assert "StatusBadge" in docs or "statusbadge" in docs.lower()
