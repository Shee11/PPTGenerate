"""Tests for Edit family layout algorithm implementations."""
import pytest

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.common.measurement import MeasuredSize
from src.layout.layout_protocol import LayoutContext, WidgetLayoutInput
from src.layout.strategies.edit import (
    EditOverlapLeftStrategy,
    EditMagazineCollageStrategy,
    EditStaggeredStrategy,
)


class TestEditOverlapLeftLayout:
    """Test EditOverlapLeftStrategy.calculate_layout()."""
    
    def test_background_fills_content_area(self) -> None:
        """Test that background fills entire content area."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="back",
                measured_size=MeasuredSize(width=1500, height=800),
                slot=Slot(role="back", size=SizeClass.XL),
                style={}
            ),
            WidgetLayoutInput(
                role="card",
                measured_size=MeasuredSize(width=900, height=800),
                slot=Slot(role="card", size=SizeClass.L),
                style={}
            )
        ]
        
        layout = EditOverlapLeftStrategy.calculate_layout(widgets, context)
        back = layout["back"]
        
        # background should fill content area: 50px from all edges
        assert back.x == 50
        assert back.y == 50
        assert back.width == 1500  # 1600 - 100
        assert back.height == 800  # 900 - 100
    
    def test_card_is_60_percent_width(self) -> None:
        """Test that card is 60% of content width."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="back",
                measured_size=MeasuredSize(width=1500, height=800),
                slot=Slot(role="back", size=SizeClass.XL),
                style={}
            ),
            WidgetLayoutInput(
                role="card",
                measured_size=MeasuredSize(width=900, height=800),
                slot=Slot(role="card", size=SizeClass.L),
                style={}
            )
        ]
        
        layout = EditOverlapLeftStrategy.calculate_layout(widgets, context)
        card = layout["card"]
        
        # card width = content_width * 0.6 = 1500 * 0.6 = 900
        assert card.width == 900
    
    def test_card_offset_20_percent_from_left(self) -> None:
        """Test that card is positioned 20% from left edge."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="back",
                measured_size=MeasuredSize(width=1500, height=800),
                slot=Slot(role="back", size=SizeClass.XL),
                style={}
            ),
            WidgetLayoutInput(
                role="card",
                measured_size=MeasuredSize(width=900, height=800),
                slot=Slot(role="card", size=SizeClass.L),
                style={}
            )
        ]
        
        layout = EditOverlapLeftStrategy.calculate_layout(widgets, context)
        card = layout["card"]
        
        # card_x = content_x + (content_width * 0.2) = 50 + (1500 * 0.2) = 350
        assert card.x == 350
    
    def test_card_vertically_centered(self) -> None:
        """Test that card is vertically centered."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="back",
                measured_size=MeasuredSize(width=1500, height=800),
                slot=Slot(role="back", size=SizeClass.XL),
                style={}
            ),
            WidgetLayoutInput(
                role="card",
                measured_size=MeasuredSize(width=900, height=800),
                slot=Slot(role="card", size=SizeClass.L),
                style={}
            )
        ]
        
        layout = EditOverlapLeftStrategy.calculate_layout(widgets, context)
        card = layout["card"]
        
        # card_y = content_y + (content_height - card_height) / 2
        # card_height should match content_height for full vertical coverage
        assert card.y == 50
        assert card.height == 800


class TestEditMagazineCollageLayout:
    """Test EditMagazineCollageStrategy.calculate_layout()."""
    
    def test_hero_is_60_percent_width(self) -> None:
        """Test that hero is 60% of content width."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="hero", measured_size=MeasuredSize(width=900, height=450), slot=Slot(role="hero", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="sticker_1", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_2", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_3", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_4", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_5", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_6", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_6", size=SizeClass.S), style={})
        ]
        
        layout = EditMagazineCollageStrategy.calculate_layout(widgets, context)
        hero = layout["hero"]
        
        # hero_width = content_width * 0.6 = 1500 * 0.6 = 900
        assert hero.width == 900
    
    def test_hero_is_centered(self) -> None:
        """Test that hero is horizontally and vertically centered."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="hero", measured_size=MeasuredSize(width=900, height=450), slot=Slot(role="hero", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="sticker_1", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_2", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_3", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_4", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_5", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_6", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_6", size=SizeClass.S), style={})
        ]
        
        layout = EditMagazineCollageStrategy.calculate_layout(widgets, context)
        hero = layout["hero"]
        
        # hero_x = content_x + (content_width * 0.2) = 50 + (1500 * 0.2) = 350
        # hero_y = content_y + (content_height * 0.2) = 50 + (800 * 0.2) = 210
        # hero_width = content_width * 0.6 = 900
        # hero_height = content_height * 0.6 = 480
        assert hero.x == 350
        assert hero.y == 210
        assert hero.width == 900
        assert hero.height == 480
    
    def test_all_stickers_have_15_percent_size(self) -> None:
        """Test that all stickers are 15% of content dimensions."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="hero", measured_size=MeasuredSize(width=900, height=450), slot=Slot(role="hero", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="sticker_1", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_2", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_3", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_4", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_5", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_6", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_6", size=SizeClass.S), style={})
        ]
        
        layout = EditMagazineCollageStrategy.calculate_layout(widgets, context)
        
        # sticker_size = min(content_width, content_height) * 0.1 = 800 * 0.1 = 80
        expected_size = 80
        
        for i in range(1, 7):
            sticker = layout[f"sticker_{i}"]
            assert sticker.width == expected_size
            assert sticker.height == expected_size
    
    def test_sticker_positions_are_scattered(self) -> None:
        """Test that stickers are positioned at predefined scattered locations."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="hero", measured_size=MeasuredSize(width=900, height=450), slot=Slot(role="hero", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="sticker_1", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_2", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_3", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_4", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_5", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="sticker_6", measured_size=MeasuredSize(width=225, height=120), slot=Slot(role="sticker_6", size=SizeClass.S), style={})
        ]
        
        layout = EditMagazineCollageStrategy.calculate_layout(widgets, context)
        
        # Verify stickers are not all in same position
        positions = [(layout[f"sticker_{i}"].x, layout[f"sticker_{i}"].y) for i in range(1, 7)]
        unique_positions = set(positions)
        assert len(unique_positions) == 6, "All stickers should have unique positions"


class TestEditStaggeredLayout:
    """Test EditStaggeredStrategy.calculate_layout()."""
    
    def test_all_items_are_45_percent_width(self) -> None:
        """Test that all items are 45% of content width."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="item_1", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_1", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_2", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_2", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_3", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_3", size=SizeClass.M), style={})
        ]
        
        layout = EditStaggeredStrategy.calculate_layout(widgets, context)
        
        expected_width = 1500 * 0.45  # 675
        
        for i in range(1, 4):
            item = layout[f"item_{i}"]
            assert item.width == expected_width
    
    def test_items_have_staggered_vertical_positions(self) -> None:
        """Test that items are staggered vertically in Z-pattern."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="item_1", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_1", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_2", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_2", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_3", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_3", size=SizeClass.M), style={})
        ]
        
        layout = EditStaggeredStrategy.calculate_layout(widgets, context)
        
        item1 = layout["item_1"]
        item2 = layout["item_2"]
        item3 = layout["item_3"]
        
        # Verify items are at different vertical positions
        assert item1.y < item2.y < item3.y, "Items should be staggered vertically"
    
    def test_items_alternate_horizontally(self) -> None:
        """Test that items alternate between left and right sides."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="item_1", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_1", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_2", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_2", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_3", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_3", size=SizeClass.M), style={})
        ]
        
        layout = EditStaggeredStrategy.calculate_layout(widgets, context)
        
        item1 = layout["item_1"]
        item2 = layout["item_2"]
        item3 = layout["item_3"]
        
        # Item 1 and 3 should be on left (x = content_x)
        assert item1.x == 50
        assert item3.x == 50
        
        # Item 2 should be on right
        assert item2.x > item1.x, "Middle item should be offset to the right"
    
    def test_item_heights_are_equal(self) -> None:
        """Test that all items have equal height (~28% of content)."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="item_1", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_1", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_2", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_2", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="item_3", measured_size=MeasuredSize(width=675, height=224), slot=Slot(role="item_3", size=SizeClass.M), style={})
        ]
        
        layout = EditStaggeredStrategy.calculate_layout(widgets, context)
        
        expected_height = 800 * 0.28  # 224
        
        for i in range(1, 4):
            item = layout[f"item_{i}"]
            assert item.height == expected_height

