"""Comparison layout strategies for high information density."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class ComparisonTwoColumnStrategy:
    """Comparison.TwoColumn: Side-by-side comparison layout.
    
    Layout: Two equal-width columns for comparing concepts, approaches, or eras.
    Perfect for Before/After, Old vs New, Traditional vs Modern comparisons.
    
    Slots:
    - left_header: Title for left column (Size S)
    - left_body: Content for left column (Size M)
    - right_header: Title for right column (Size S)
    - right_body: Content for right column (Size M)
    
    Optional bottom slots for shared context:
    - bottom_left: Supporting detail (Size S)
    - bottom_right: Supporting detail (Size S)
    
    Layout Algorithm:
    - Split content area 50/50 vertically with gutter
    - Each column: header at top, body below
    - Optional bottom row for supplementary information
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Comparison.TwoColumn"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 6 slots: 2 headers, 2 bodies, 2 optional bottom cells."""
        return [
            Slot(role="left_header", size=SizeClass.S),
            Slot(role="left_body", size=SizeClass.M),
            Slot(role="right_header", size=SizeClass.S),
            Slot(role="right_body", size=SizeClass.M),
            Slot(role="bottom_left", size=SizeClass.S),
            Slot(role="bottom_right", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate two-column comparison layout.
        
        Layout structure:
        [left_header]  |  [right_header]
        [left_body]    |  [right_body]
        [bottom_left]  |  [bottom_right]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context with canvas and spacing info
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Calculate column width (50/50 split with gutter)
        column_width = (context.content_width - context.gutter) / 2
        
        # Check which widgets are present
        widget_roles = {w.role for w in widgets}
        has_bottom = "bottom_left" in widget_roles or "bottom_right" in widget_roles
        
        # Calculate header height (15% of content or minimum 80px)
        header_height = max(context.content_height * 0.15, 80)
        
        # Calculate body height
        if has_bottom:
            # Reserve space for bottom row (20% of content or minimum 100px)
            bottom_height = max(context.content_height * 0.2, 100)
            body_height = context.content_height - header_height - bottom_height - (context.gutter * 2)
            bottom_y = context.content_y + header_height + body_height + (context.gutter * 2)
        else:
            body_height = context.content_height - header_height - context.gutter
        
        # Left column
        for widget in widgets:
            if widget.role == "left_header":
                bounds_map[widget.role] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=column_width,
                    height=header_height
                )
            elif widget.role == "left_body":
                bounds_map[widget.role] = Bounds(
                    x=context.content_x,
                    y=context.content_y + header_height + context.gutter,
                    width=column_width,
                    height=body_height
                )
            elif widget.role == "bottom_left" and has_bottom:
                bounds_map[widget.role] = Bounds(
                    x=context.content_x,
                    y=bottom_y,
                    width=column_width,
                    height=bottom_height
                )
        
        # Right column (offset by column_width + gutter)
        right_x = context.content_x + column_width + context.gutter
        
        for widget in widgets:
            if widget.role == "right_header":
                bounds_map[widget.role] = Bounds(
                    x=right_x,
                    y=context.content_y,
                    width=column_width,
                    height=header_height
                )
            elif widget.role == "right_body":
                bounds_map[widget.role] = Bounds(
                    x=right_x,
                    y=context.content_y + header_height + context.gutter,
                    width=column_width,
                    height=body_height
                )
            elif widget.role == "bottom_right" and has_bottom:
                bounds_map[widget.role] = Bounds(
                    x=right_x,
                    y=bottom_y,
                    width=column_width,
                    height=bottom_height
                )
        
        return bounds_map


class ComparisonThreeColumnStrategy:
    """Comparison.ThreeColumn: Three-way comparison layout.
    
    Layout: Three equal-width columns for comparing multiple options or approaches.
    Perfect for Good/Better/Best, Phase 1/2/3, or multi-vendor comparisons.
    
    Slots:
    - col1_header: Title for column 1 (Size S)
    - col1_body: Content for column 1 (Size S)
    - col2_header: Title for column 2 (Size S)
    - col2_body: Content for column 2 (Size S)
    - col3_header: Title for column 3 (Size S)
    - col3_body: Content for column 3 (Size S)
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Comparison.ThreeColumn"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 6 slots: 3 headers, 3 bodies."""
        return [
            Slot(role="col1_header", size=SizeClass.S),
            Slot(role="col1_body", size=SizeClass.S),
            Slot(role="col2_header", size=SizeClass.S),
            Slot(role="col2_body", size=SizeClass.S),
            Slot(role="col3_header", size=SizeClass.S),
            Slot(role="col3_body", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate three-column comparison layout.
        
        Layout structure:
        [col1_header] | [col2_header] | [col3_header]
        [col1_body]   | [col2_body]   | [col3_body]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context with canvas and spacing info
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Calculate column width (33/33/33 split with 2 gutters)
        column_width = (context.content_width - (context.gutter * 2)) / 3
        
        # Calculate header height (20% of content or minimum 80px)
        header_height = max(context.content_height * 0.2, 80)
        body_height = context.content_height - header_height - context.gutter
        
        # Column positions
        columns = [
            ("col1", context.content_x),
            ("col2", context.content_x + column_width + context.gutter),
            ("col3", context.content_x + (column_width + context.gutter) * 2),
        ]
        
        for col_prefix, col_x in columns:
            for widget in widgets:
                if widget.role == f"{col_prefix}_header":
                    bounds_map[widget.role] = Bounds(
                        x=col_x,
                        y=context.content_y,
                        width=column_width,
                        height=header_height
                    )
                elif widget.role == f"{col_prefix}_body":
                    bounds_map[widget.role] = Bounds(
                        x=col_x,
                        y=context.content_y + header_height + context.gutter,
                        width=column_width,
                        height=body_height
                    )
        
        return bounds_map
