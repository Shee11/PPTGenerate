"""Integration tests for Slidev Vue layout components."""
import pytest
import os


class TestSmartGridLayout:
    """Test SmartGrid layout component with dynamic column configuration."""
    
    def test_smart_grid_layout_file_exists(self):
        """Verify SmartGrid.vue layout file exists."""
        layout_path = "slidev-project/layouts/smart-grid.vue"
        assert os.path.exists(layout_path), f"SmartGrid layout should exist at {layout_path}"
    
    def test_smart_grid_has_slot_definitions(self):
        """Verify SmartGrid layout defines header and column slots."""
        layout_path = "slidev-project/layouts/smart-grid.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should have slot definitions for header and columns
        assert 'slot' in content.lower()
        assert 'header' in content
        assert 'col1' in content
        assert 'col2' in content
        assert 'col3' in content
        assert 'col4' in content
    
    def test_smart_grid_uses_cols_parameter(self):
        """Verify SmartGrid reads cols parameter from frontmatter."""
        layout_path = "slidev-project/layouts/smart-grid.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should reference cols parameter
        assert 'cols' in content
    
    def test_smart_grid_uses_css_grid(self):
        """Verify SmartGrid uses CSS Grid for layout."""
        layout_path = "slidev-project/layouts/smart-grid.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should use CSS Grid
        assert 'grid' in content.lower()
    
    def test_smart_grid_uses_theme_variables(self):
        """Verify SmartGrid uses theme CSS variables."""
        layout_path = "slidev-project/layouts/smart-grid.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should reference theme variables
        assert '--c-' in content or 'var(--' in content or 'bg-theme' in content


class TestHeroSplitLayout:
    """Test HeroSplit layout component with ratio configuration."""
    
    def test_hero_split_layout_file_exists(self):
        """Verify HeroSplit.vue layout file exists."""
        layout_path = "slidev-project/layouts/hero-split.vue"
        assert os.path.exists(layout_path), f"HeroSplit layout should exist at {layout_path}"
    
    def test_hero_split_has_left_right_slots(self):
        """Verify HeroSplit layout defines left and right slots."""
        layout_path = "slidev-project/layouts/hero-split.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should have left and right slots
        assert 'left' in content
        assert 'right' in content
    
    def test_hero_split_uses_ratio_parameter(self):
        """Verify HeroSplit reads ratio parameter from frontmatter."""
        layout_path = "slidev-project/layouts/hero-split.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should reference ratio parameter
        assert 'ratio' in content
    
    def test_hero_split_uses_flexbox(self):
        """Verify HeroSplit uses flexbox for layout."""
        layout_path = "slidev-project/layouts/hero-split.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should use flex or width percentages
        assert 'flex' in content.lower() or 'width' in content.lower()
    
    def test_hero_split_uses_theme_variables(self):
        """Verify HeroSplit uses theme CSS variables."""
        layout_path = "slidev-project/layouts/hero-split.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should reference theme variables
        assert '--c-' in content or 'var(--' in content or 'bg-theme' in content


class TestFullBleedLayout:
    """Test FullBleed layout component with vertical alignment."""
    
    def test_full_bleed_layout_file_exists(self):
        """Verify FullBleed.vue layout file exists."""
        layout_path = "slidev-project/layouts/full-bleed.vue"
        assert os.path.exists(layout_path), f"FullBleed layout should exist at {layout_path}"
    
    def test_full_bleed_has_default_slot(self):
        """Verify FullBleed layout defines default slot."""
        layout_path = "slidev-project/layouts/full-bleed.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should have slot definition
        assert '<slot' in content.lower()
    
    def test_full_bleed_uses_align_parameter(self):
        """Verify FullBleed reads align parameter from frontmatter."""
        layout_path = "slidev-project/layouts/full-bleed.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should reference align parameter
        assert 'align' in content
    
    def test_full_bleed_supports_vertical_alignment(self):
        """Verify FullBleed supports top/center/bottom alignment."""
        layout_path = "slidev-project/layouts/full-bleed.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should have alignment logic (flex-start, center, flex-end or similar)
        has_alignment = (
            'flex-start' in content or 
            'flex-end' in content or 
            'justify' in content.lower() or
            'align' in content.lower()
        )
        assert has_alignment, "Should support vertical alignment"
    
    def test_full_bleed_uses_theme_variables(self):
        """Verify FullBleed uses theme CSS variables."""
        layout_path = "slidev-project/layouts/full-bleed.vue"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should reference theme variables
        assert '--c-' in content or 'var(--' in content or 'bg-theme' in content
