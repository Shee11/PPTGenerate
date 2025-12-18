"""Bento layout strategies with auto-layout algorithms."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class BentoStandardStrategy:
    """Bento.Standard: 3x2 grid of equal-sized cells.
    
    All 6 cells are Size S, arranged in a balanced grid.
    Ideal for dashboards, galleries, or feature grids.
    
    Layout Algorithm:
    - Fixed 3-column x 2-row grid
    - Each cell gets equal space: (content_width / 3) x (content_height / 2)
    - Gutter spacing applied between cells
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.Standard"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 6 slots arranged in 3x2 grid, all Size S."""
        return [
            Slot(role="cell_1", size=SizeClass.S),
            Slot(role="cell_2", size=SizeClass.S),
            Slot(role="cell_3", size=SizeClass.S),
            Slot(role="cell_4", size=SizeClass.S),
            Slot(role="cell_5", size=SizeClass.S),
            Slot(role="cell_6", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate 3x2 grid layout with equal cell sizes.
        
        Grid structure:
        [cell_1] [cell_2] [cell_3]
        [cell_4] [cell_5] [cell_6]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context with canvas and spacing info
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Calculate cell dimensions
        # 3 columns with 2 gutters between them
        cell_width = (context.content_width - (context.gutter * 2)) / 3
        # 2 rows with 1 gutter between them
        cell_height = (context.content_height - context.gutter) / 2
        
        # Grid positions (row, col) for each cell
        grid_positions = {
            "cell_1": (0, 0),
            "cell_2": (0, 1),
            "cell_3": (0, 2),
            "cell_4": (1, 0),
            "cell_5": (1, 1),
            "cell_6": (1, 2),
        }
        
        for widget in widgets:
            if widget.role not in grid_positions:
                continue
            
            row, col = grid_positions[widget.role]
            
            # Calculate absolute position
            x = context.content_x + (col * (cell_width + context.gutter))
            y = context.content_y + (row * (cell_height + context.gutter))
            
            bounds_map[widget.role] = Bounds(
                x=x,
                y=y,
                width=cell_width,
                height=cell_height
            )
        
        return bounds_map


class BentoHeroLeftStrategy:
    """Bento.HeroLeft: Hero on left (2x2) with 4 small side cells.
    
    Layout: 1 Size L hero slot on left, 4 Size S slots on right side.
    Emphasizes primary content while showing supporting metrics.
    
    Layout Algorithm:
    - Hero takes 2/3 of width, full height
    - 4 side cells split remaining 1/3 width in 2x2 grid
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.HeroLeft"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return hero slot (L) + 4 side slots (S)."""
        return [
            Slot(role="hero", size=SizeClass.L),
            Slot(role="side_1", size=SizeClass.S),
            Slot(role="side_2", size=SizeClass.S),
            Slot(role="side_3", size=SizeClass.S),
            Slot(role="side_4", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate hero-left layout with 2/3 - 1/3 split.
        
        Layout structure:
        [       hero        ] [side_1] [side_2]
        [       (2/3)       ] [side_3] [side_4]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Hero takes 2/3 width
        hero_width = (context.content_width * 2 / 3) - (context.gutter / 2)
        hero_height = context.content_height
        
        # Side cells share remaining 1/3 width in 2x2 grid
        side_width = (context.content_width / 3) - (context.gutter / 2)
        side_cell_width = (side_width - context.gutter) / 2
        side_cell_height = (context.content_height - context.gutter) / 2
        
        # Position mapping
        positions = {
            "hero": (0, 0, hero_width, hero_height),
            "side_1": (hero_width + context.gutter, 0, side_cell_width, side_cell_height),
            "side_2": (hero_width + context.gutter + side_cell_width + context.gutter, 0, side_cell_width, side_cell_height),
            "side_3": (hero_width + context.gutter, side_cell_height + context.gutter, side_cell_width, side_cell_height),
            "side_4": (hero_width + context.gutter + side_cell_width + context.gutter, side_cell_height + context.gutter, side_cell_width, side_cell_height),
        }
        
        for widget in widgets:
            if widget.role not in positions:
                continue
            
            x_offset, y_offset, width, height = positions[widget.role]
            
            bounds_map[widget.role] = Bounds(
                x=context.content_x + x_offset,
                y=context.content_y + y_offset,
                width=width,
                height=height
            )
        
        return bounds_map


class BentoHeroTopStrategy:
    """Bento.HeroTop: Hero on top (2x2) with 3 footer cells.
    
    Layout: 1 Size L hero slot on top, 3 Size S footer slots on bottom.
    Perfect for featured content with action buttons or stats below.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.HeroTop"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return hero slot (L) + 3 footer slots (S)."""
        return [
            Slot(role="hero", size=SizeClass.L),
            Slot(role="footer_1", size=SizeClass.S),
            Slot(role="footer_2", size=SizeClass.S),
            Slot(role="footer_3", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate hero-top layout.
        
        Hero on top (2/3 height), 3 footer cells below (1/3 height).
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Hero takes 2/3 height
        hero_height = (context.content_height * 2 / 3) - (context.gutter / 2)
        
        # Footer cells share remaining 1/3 height
        footer_height = (context.content_height / 3) - (context.gutter / 2)
        footer_cell_width = (context.content_width - (context.gutter * 2)) / 3
        
        positions = {
            "hero": (0, 0, context.content_width, hero_height),
            "footer_1": (0, hero_height + context.gutter, footer_cell_width, footer_height),
            "footer_2": (footer_cell_width + context.gutter, hero_height + context.gutter, footer_cell_width, footer_height),
            "footer_3": ((footer_cell_width + context.gutter) * 2, hero_height + context.gutter, footer_cell_width, footer_height),
        }
        
        for widget in widgets:
            if widget.role in positions:
                x_offset, y_offset, width, height = positions[widget.role]
                bounds_map[widget.role] = Bounds(
                    x=context.content_x + x_offset,
                    y=context.content_y + y_offset,
                    width=width,
                    height=height
                )
        
        return bounds_map


class BentoQuarterStrategy:
    """Bento.Quarter: 2x2 grid of medium-sized quadrants.
    
    Layout: 4 Size M slots arranged in balanced 2x2 grid.
    Each quadrant gets equal emphasis for comparison layouts.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.Quarter"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 4 slots arranged in 2x2 grid, all Size M."""
        return [
            Slot(role="quadrant_1", size=SizeClass.M),
            Slot(role="quadrant_2", size=SizeClass.M),
            Slot(role="quadrant_3", size=SizeClass.M),
            Slot(role="quadrant_4", size=SizeClass.M),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate 2x2 quadrant layout.
        
        Four equal quadrants in 2x2 grid.
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Calculate quadrant dimensions
        quad_width = (context.content_width - context.gutter) / 2
        quad_height = (context.content_height - context.gutter) / 2
        
        # Grid positions (row, col) for each quadrant
        grid_positions = {
            "quadrant_1": (0, 0),
            "quadrant_2": (0, 1),
            "quadrant_3": (1, 0),
            "quadrant_4": (1, 1),
        }
        
        for widget in widgets:
            if widget.role in grid_positions:
                row, col = grid_positions[widget.role]
                
                x = context.content_x + (col * (quad_width + context.gutter))
                y = context.content_y + (row * (quad_height + context.gutter))
                
                bounds_map[widget.role] = Bounds(
                    x=x,
                    y=y,
                    width=quad_width,
                    height=quad_height
                )
        
        return bounds_map


class BentoVerticalStackStrategy:
    """Bento.VerticalStack: Vertical stack flow with arrow separators.
    
    Layout: Max 3 S slots or 1 M + 1 S slot arranged vertically.
    Each stage displays content stacked top-to-bottom. Arrows between stages.
    Perfect for sequential processes, step-by-step flows, simple vertical progressions.
    
    Layout Algorithm:
    - All stages get equal height: content_height / num_stages
    - Full content width for each stage
    - Arrows rendered between stages (pointing downward)
    
    Slot Constraints:
    - Max 3 S (small) widgets for simple sequences
    - OR 1 M (medium) + 1 S (small) for mixed content
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.VerticalStack"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return vertical stack slots.
        
        Supports either:
        - Max 3 S (small) slots for simple sequential steps
        - 1 M (medium) + 1 S (small) for mixed content
        """
        return [
            Slot(role="stage_1", size=SizeClass.S),
            Slot(role="stage_2", size=SizeClass.S),
            Slot(role="stage_3", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate vertical stack layout with equal-height stages.
        
        Layout structure (max 3 stages):
        [stage_1]
            ↓
        [stage_2]
            ↓
        [stage_3]
        
        Args:
            widgets: List of widgets (max 3 S or 1 M + 1 S)
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        num_stages = len(widgets)
        if num_stages < 1 or num_stages > 3:
            # Fallback to 3 stages if invalid count
            num_stages = 3
        
        # Each stage gets equal height
        stage_width = context.content_width
        stage_height = context.content_height / num_stages
        
        for i, widget in enumerate(widgets):
            y = context.content_y + (i * stage_height)
            
            bounds_map[widget.role] = Bounds(
                x=context.content_x,
                y=y,
                width=stage_width,
                height=stage_height
            )
        
        return bounds_map
