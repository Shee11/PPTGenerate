"""Edit layout strategies with overlap and collage effects."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class EditOverlapLeftStrategy:
    """Edit.Overlap_Left: Layered card effect with 2.5D depth.
    
    Layout: XL background + L card overlapping left side.
    Creates visual depth with foreground element over background.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Edit.Overlap_Left"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return background (XL) + card (L) slots."""
        return [
            Slot(role="back", size=SizeClass.XL),
            Slot(role="card", size=SizeClass.L),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate overlap layout with background + foreground card.
        
        Layout structure:
        [  back (full)  ]
           [card 60%]  <- positioned at 20% from left
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Card dimensions and positioning
        card_width = context.content_width * 0.6
        card_height = context.content_height
        card_x = context.content_x + (context.content_width * 0.2)  # 20% from left
        
        for widget in widgets:
            if widget.role == "back":
                # Background fills entire content area
                bounds_map["back"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=context.content_width,
                    height=context.content_height
                )
            elif widget.role == "card":
                # Card overlaps on left side
                bounds_map["card"] = Bounds(
                    x=card_x,
                    y=context.content_y,
                    width=card_width,
                    height=card_height
                )
        
        return bounds_map


class EditMagazineCollageStrategy:
    """Edit.Magazine_Collage: Random scattered sticker layout.
    
    Layout: XL hero anchor + multiple S stickers scattered around.
    Creates playful, editorial-style compositions.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Edit.Magazine_Collage"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return hero (XL) + 6 sticker (S) slots."""
        return [
            Slot(role="hero", size=SizeClass.XL),
            Slot(role="sticker_1", size=SizeClass.S),
            Slot(role="sticker_2", size=SizeClass.S),
            Slot(role="sticker_3", size=SizeClass.S),
            Slot(role="sticker_4", size=SizeClass.S),
            Slot(role="sticker_5", size=SizeClass.S),
            Slot(role="sticker_6", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate collage layout with centered hero + scattered stickers.
        
        Layout structure:
        [sticker]    [sticker]
             [  hero (60%)  ]
        [sticker]    [sticker]
             [sticker] [sticker]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Hero centered, 60% of width and height
        hero_width = context.content_width * 0.6
        hero_height = context.content_height * 0.6
        hero_x = context.content_x + (context.content_width * 0.2)
        hero_y = context.content_y + (context.content_height * 0.2)
        
        # Sticker size (10% of content area)
        sticker_size = min(context.content_width, context.content_height) * 0.1
        
        # Predefined sticker positions (scattered around hero)
        sticker_positions = [
            (0.05, 0.1),   # top-left
            (0.75, 0.05),  # top-right
            (0.1, 0.55),   # middle-left
            (0.8, 0.5),    # middle-right
            (0.3, 0.85),   # bottom-left
            (0.7, 0.9),    # bottom-right
        ]
        
        for widget in widgets:
            if widget.role == "hero":
                bounds_map["hero"] = Bounds(
                    x=hero_x,
                    y=hero_y,
                    width=hero_width,
                    height=hero_height
                )
            elif widget.role.startswith("sticker_"):
                # Extract sticker number (1-6)
                sticker_num = int(widget.role.split("_")[1]) - 1
                if sticker_num < len(sticker_positions):
                    pos_x, pos_y = sticker_positions[sticker_num]
                    bounds_map[widget.role] = Bounds(
                        x=context.content_x + (context.content_width * pos_x),
                        y=context.content_y + (context.content_height * pos_y),
                        width=sticker_size,
                        height=sticker_size
                    )
        
        return bounds_map


class EditStaggeredStrategy:
    """Edit.Staggered: Z-pattern alternating layout.
    
    Layout: 3 M items in staggered vertical positions.
    Creates dynamic flow for multi-step processes.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Edit.Staggered"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 3 staggered M slots."""
        return [
            Slot(role="item_1", size=SizeClass.M),
            Slot(role="item_2", size=SizeClass.M),
            Slot(role="item_3", size=SizeClass.M),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate staggered Z-pattern layout.
        
        Layout structure:
        [item_1]
                [item_2]
        [item_3]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Each item takes 45% width, 28% height
        item_width = context.content_width * 0.45
        item_height = context.content_height * 0.28
        
        # Vertical spacing
        vertical_step = context.content_height / 3
        
        # Staggered positions
        positions = [
            (0.0, 0.0),           # Left, top
            (0.55, 0.36),         # Right, middle
            (0.0, 0.72),          # Left, bottom
        ]
        
        for widget in widgets:
            if widget.role in ["item_1", "item_2", "item_3"]:
                item_num = int(widget.role.split("_")[1]) - 1
                if item_num < len(positions):
                    pos_x, pos_y = positions[item_num]
                    bounds_map[widget.role] = Bounds(
                        x=context.content_x + (context.content_width * pos_x),
                        y=context.content_y + (context.content_height * pos_y),
                        width=item_width,
                        height=item_height
                    )
        
        return bounds_map
