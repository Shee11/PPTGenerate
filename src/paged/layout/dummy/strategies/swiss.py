"""Swiss layout strategies with auto-layout algorithms."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class SwissPosterStrategy:
    """Swiss.Poster: Single full-screen slot.
    
    One XL slot occupying the entire screen.
    Ideal for hero images, large typography, or full-bleed content.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Swiss.Poster"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 1 XL slot for full-screen headline."""
        return [
            Slot(role="headline", size=SizeClass.XL),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate full-screen layout.
        
        Single widget fills entire content area.
        """
        bounds_map: Dict[str, Bounds] = {}
        
        for widget in widgets:
            if widget.role == "headline":
                # Full content area
                bounds_map["headline"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=context.content_width,
                    height=context.content_height
                )
        
        return bounds_map


class SwissAsymmetryStrategy:
    """Swiss.Asymmetry: Content on right with intentional void space.
    
    Layout: 1 Size L content slot positioned right, void area on left.
    Creates visual tension with asymmetric balance.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Swiss.Asymmetry"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return single L slot for content (void area implicit)."""
        return [
            Slot(role="content", size=SizeClass.L),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate asymmetric layout with content on right.
        
        Content takes right 60%, left 40% is void.
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Content on right side (60% width)
        content_width = context.content_width * 0.6
        
        for widget in widgets:
            if widget.role == "content":
                bounds_map["content"] = Bounds(
                    x=context.content_x + (context.content_width * 0.4),  # Start at 40%
                    y=context.content_y,
                    width=content_width,
                    height=context.content_height
                )
        
        return bounds_map


class SwissSplitTypoStrategy:
    """Swiss.SplitTypo: Typography-focused vertical split.
    
    Layout: Size M headline slot on top, Size L body slot below.
    Emphasizes typographic hierarchy and readable content.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Swiss.SplitTypo"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return headline (M) + body (L) slots."""
        return [
            Slot(role="headline", size=SizeClass.M),
            Slot(role="body", size=SizeClass.L),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate vertical split layout.
        
        Headline on top (35%), body below (65%).
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Split vertically with gutter
        headline_height = (context.content_height * 0.35) - (context.gutter / 2)
        body_height = (context.content_height * 0.65) - (context.gutter / 2)
        
        for widget in widgets:
            if widget.role == "headline":
                bounds_map["headline"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=context.content_width,
                    height=headline_height
                )
            elif widget.role == "body":
                bounds_map["body"] = Bounds(
                    x=context.content_x,
                    y=context.content_y + headline_height + context.gutter,
                    width=context.content_width,
                    height=body_height
                )
        
        return bounds_map
