"""Cinematic layout strategies with auto-layout algorithms."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class CinematicSplit5050Strategy:
    """Cinematic.Split_50_50: Equal 50/50 left-right split.
    
    Two L slots dividing the screen equally.
    Ideal for comparisons, before/after, or dual content display.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Cinematic.Split_50_50"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 2 L slots for equal left/right division."""
        return [
            Slot(role="left", size=SizeClass.L),
            Slot(role="right", size=SizeClass.L),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate 50/50 split layout.
        
        Two equal panels side by side.
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Split width equally with gutter
        panel_width = (context.content_width - context.gutter) / 2
        
        for widget in widgets:
            if widget.role == "left":
                bounds_map["left"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=panel_width,
                    height=context.content_height
                )
            elif widget.role == "right":
                bounds_map["right"] = Bounds(
                    x=context.content_x + panel_width + context.gutter,
                    y=context.content_y,
                    width=panel_width,
                    height=context.content_height
                )
        
        return bounds_map


class CinematicFullBleedStrategy:
    """Cinematic.FullBleed: Edge-to-edge immersive content.
    
    Layout: 1 Size XL slot covering viewport edge-to-edge.
    Maximum visual impact with no margins or padding.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Cinematic.FullBleed"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return single XL slot for full-bleed content."""
        return [
            Slot(role="stage", size=SizeClass.XL),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate full-bleed layout.
        
        Single widget fills entire content area.
        """
        bounds_map: Dict[str, Bounds] = {}
        
        for widget in widgets:
            if widget.role == "stage":
                # Full content area
                bounds_map["stage"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=context.content_width,
                    height=context.content_height
                )
        
        return bounds_map


class CinematicSplit3070Strategy:
    """Cinematic.Split_30_70: Asymmetric 30/70 sidebar-stage split.
    
    Layout: Size M sidebar (30%) + Size XL stage (70%).
    Perfect for navigation + content or filtering + results.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Cinematic.Split_30_70"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return sidebar (M) + stage (XL) slots."""
        return [
            Slot(role="sidebar", size=SizeClass.M),
            Slot(role="stage", size=SizeClass.XL),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate 30/70 split layout.
        
        Sidebar (30%) on left, stage (70%) on right.
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Split width 30/70 with gutter
        sidebar_width = (context.content_width * 0.3) - (context.gutter / 2)
        stage_width = (context.content_width * 0.7) - (context.gutter / 2)
        
        for widget in widgets:
            if widget.role == "sidebar":
                bounds_map["sidebar"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=sidebar_width,
                    height=context.content_height
                )
            elif widget.role == "stage":
                bounds_map["stage"] = Bounds(
                    x=context.content_x + sidebar_width + context.gutter,
                    y=context.content_y,
                    width=stage_width,
                    height=context.content_height
                )
        
        return bounds_map
