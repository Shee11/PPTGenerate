"""Unit tests for Slidev theme resolution and CSS variable injection."""
import pytest


class TestThemeResolution:
    """Test theme resolution from hex colors to semantic names."""
    
    def test_business_theme_from_blue_primary(self):
        """Verify #2563eb maps to business theme."""
        from src.render.slidev.markdown_renderer import resolve_theme
        
        theme = resolve_theme("#2563eb")
        assert theme == "business"
    
    def test_cyber_theme_from_green_primary(self):
        """Verify #00ffa3 maps to cyber theme."""
        from src.render.slidev.markdown_renderer import resolve_theme
        
        theme = resolve_theme("#00ffa3")
        assert theme == "cyber"
    
    def test_default_theme_for_unknown_color(self):
        """Verify unknown colors default to business theme."""
        from src.render.slidev.markdown_renderer import resolve_theme
        
        theme = resolve_theme("#ff0000")
        assert theme == "business"
    
    def test_default_theme_for_none(self):
        """Verify None color defaults to business theme."""
        from src.render.slidev.markdown_renderer import resolve_theme
        
        theme = resolve_theme(None)
        assert theme == "business"
    
    def test_case_insensitive_color_matching(self):
        """Verify color matching is case-insensitive."""
        from src.render.slidev.markdown_renderer import resolve_theme
        
        assert resolve_theme("#2563EB") == "business"
        assert resolve_theme("#00FFA3") == "cyber"


class TestThemeCSSVariableInjection:
    """Test that SlideShell.vue correctly injects CSS variables based on theme."""
    
    def test_business_theme_css_variables(self):
        """Verify business theme sets correct CSS variables."""
        # This test would require Vue component testing setup
        # For now, we verify the SlideShell.vue file contains the correct mappings
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        assert os.path.exists(slideshell_path), "SlideShell.vue should exist"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verify business theme variables are defined
        assert '--c-bg-base' in content
        assert '#ffffff' in content  # Business bg
        assert '#2563eb' in content  # Business primary
        assert '--c-primary' in content
        assert '--font-family' in content
        assert 'Inter' in content
    
    def test_cyber_theme_css_variables(self):
        """Verify cyber theme sets correct CSS variables."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verify cyber theme variables are defined
        assert '#050505' in content  # Cyber bg
        assert '#00ffa3' in content  # Cyber primary
        assert 'Orbitron' in content
    
    def test_theme_prop_accepted(self):
        """Verify SlideShell.vue accepts theme prop."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verify theme prop is defined
        assert 'theme?' in content or 'theme:' in content
        assert "'business'" in content or '"business"' in content
        assert "'cyber'" in content or '"cyber"' in content
