"""Matrix layout strategies for structured high-density information."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class MatrixGridStrategy:
    """Matrix.Grid: High-density grid layout for structured information.
    
    Layout: 2x4 grid (2 columns x 4 rows) for detailed comparisons or feature matrices.
    Perfect for feature comparisons, role evolution tables, or process breakdowns.
    
    Slots:
    - header_left: Left column header (Size S)
    - header_right: Right column header (Size S)
    - row1_left, row1_right: First row cells (Size S each)
    - row2_left, row2_right: Second row cells (Size S each)
    - row3_left, row3_right: Third row cells (Size S each)
    - row4_left, row4_right: Fourth row cells (Size S each)
    
    Total: 10 slots (2 headers + 8 content cells)
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Matrix.Grid"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 10 slots: 2 headers + 8 content cells."""
        return [
            # Header row
            Slot(role="header_left", size=SizeClass.S),
            Slot(role="header_right", size=SizeClass.S),
            # Row 1
            Slot(role="row1_left", size=SizeClass.S),
            Slot(role="row1_right", size=SizeClass.S),
            # Row 2
            Slot(role="row2_left", size=SizeClass.S),
            Slot(role="row2_right", size=SizeClass.S),
            # Row 3
            Slot(role="row3_left", size=SizeClass.S),
            Slot(role="row3_right", size=SizeClass.S),
            # Row 4
            Slot(role="row4_left", size=SizeClass.S),
            Slot(role="row4_right", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate 2x4 grid layout.
        
        Layout structure:
        [header_left]  | [header_right]
        [row1_left]    | [row1_right]
        [row2_left]    | [row2_right]
        [row3_left]    | [row3_right]
        [row4_left]    | [row4_right]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context with canvas and spacing info
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Calculate column width (50/50 split)
        column_width = (context.content_width - context.gutter) / 2
        
        # Calculate row heights
        # Header: 15% of content height (emphasized)
        header_height = max(context.content_height * 0.15, 60)
        
        # Content rows: divide remaining space equally (4 gutters between 5 rows)
        remaining_height = context.content_height - header_height - (context.gutter * 4)
        row_height = remaining_height / 4
        
        # Row definitions (role_prefix, row_index)
        rows = [
            ("header", 0, header_height),
            ("row1", 1, row_height),
            ("row2", 2, row_height),
            ("row3", 3, row_height),
            ("row4", 4, row_height),
        ]
        
        for row_prefix, row_idx, height in rows:
            # Calculate Y position
            if row_idx == 0:
                y = context.content_y
            else:
                # Header + (row_idx - 1) content rows + row_idx gutters
                y = context.content_y + header_height + (row_idx - 1) * row_height + row_idx * context.gutter
            
            for widget in widgets:
                if widget.role == f"{row_prefix}_left":
                    bounds_map[widget.role] = Bounds(
                        x=context.content_x,
                        y=y,
                        width=column_width,
                        height=height
                    )
                elif widget.role == f"{row_prefix}_right":
                    bounds_map[widget.role] = Bounds(
                        x=context.content_x + column_width + context.gutter,
                        y=y,
                        width=column_width,
                        height=height
                    )
        
        return bounds_map


class MatrixTimelineStrategy:
    """Matrix.Timeline: Horizontal timeline with detailed stages.
    
    Layout: 4-stage horizontal timeline with descriptions.
    Perfect for process flows, roadmaps, or evolution narratives.
    
    Slots:
    - stage1_title: Stage 1 title (Size S)
    - stage1_detail: Stage 1 description (Size S)
    - stage2_title: Stage 2 title (Size S)
    - stage2_detail: Stage 2 description (Size S)
    - stage3_title: Stage 3 title (Size S)
    - stage3_detail: Stage 3 description (Size S)
    - stage4_title: Stage 4 title (Size S)
    - stage4_detail: Stage 4 description (Size S)
    
    Total: 8 slots (4 stages, each with title + detail)
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Matrix.Timeline"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 8 slots: 4 stages with title and detail each."""
        return [
            Slot(role="stage1_title", size=SizeClass.S),
            Slot(role="stage1_detail", size=SizeClass.S),
            Slot(role="stage2_title", size=SizeClass.S),
            Slot(role="stage2_detail", size=SizeClass.S),
            Slot(role="stage3_title", size=SizeClass.S),
            Slot(role="stage3_detail", size=SizeClass.S),
            Slot(role="stage4_title", size=SizeClass.S),
            Slot(role="stage4_detail", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate horizontal timeline layout.
        
        Layout structure (horizontal flow):
        [stage1_title] → [stage2_title] → [stage3_title] → [stage4_title]
        [stage1_detail]  [stage2_detail]  [stage3_detail]  [stage4_detail]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context with canvas and spacing info
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Calculate stage width (4 columns with 3 gutters)
        stage_width = (context.content_width - (context.gutter * 3)) / 4
        
        # Calculate heights
        # Title row: 25% of content (emphasized)
        title_height = max(context.content_height * 0.25, 80)
        # Detail row: remaining space
        detail_height = context.content_height - title_height - context.gutter
        
        # Stage positions
        stages = [
            ("stage1", 0),
            ("stage2", 1),
            ("stage3", 2),
            ("stage4", 3),
        ]
        
        for stage_prefix, stage_idx in stages:
            # Calculate X position
            x = context.content_x + stage_idx * (stage_width + context.gutter)
            
            for widget in widgets:
                if widget.role == f"{stage_prefix}_title":
                    bounds_map[widget.role] = Bounds(
                        x=x,
                        y=context.content_y,
                        width=stage_width,
                        height=title_height
                    )
                elif widget.role == f"{stage_prefix}_detail":
                    bounds_map[widget.role] = Bounds(
                        x=x,
                        y=context.content_y + title_height + context.gutter,
                        width=stage_width,
                        height=detail_height
                    )
        
        return bounds_map
