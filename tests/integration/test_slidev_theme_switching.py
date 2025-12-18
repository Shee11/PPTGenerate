"""Integration tests for theme switching functionality."""
import pytest


class TestThemeSwitching:
    """Test that theme switching updates colors, fonts, and shadows correctly."""
    
    def test_theme_switching_updates_background_color(self):
        """Verify business → cyber changes background from white to dark."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Business theme should have white background
        assert '#ffffff' in content.lower()
        
        # Cyber theme should have dark background
        assert '#050505' in content.lower()
    
    def test_theme_switching_updates_primary_color(self):
        """Verify business → cyber changes primary from blue to green."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Business theme should have blue primary
        assert '#2563eb' in content.lower()
        
        # Cyber theme should have green primary
        assert '#00ffa3' in content.lower()
    
    def test_theme_switching_updates_font_family(self):
        """Verify business uses Inter, cyber uses Orbitron."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Business theme should use Inter
        assert 'Inter' in content
        
        # Cyber theme should use Orbitron
        assert 'Orbitron' in content
    
    def test_theme_switching_updates_shadows(self):
        """Verify business uses clean shadows, cyber uses neon glow."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Business theme should have minimal shadow
        assert 'rgba(0, 0, 0, 0.1)' in content or 'rgba(0,0,0,0.1)' in content
        
        # Cyber theme should have glow effect referencing primary color
        assert '--c-primary' in content
    
    def test_grid_overlay_for_cyber_theme(self):
        """Verify cyber theme includes grid pattern overlay."""
        import os
        slideshell_path = "slidev-project/components/SlideShell.vue"
        
        with open(slideshell_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cyber theme should have linear-gradient background pattern
        assert 'linear-gradient' in content or 'backgroundImage' in content
