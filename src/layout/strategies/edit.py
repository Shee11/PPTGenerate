"""Edit layout strategies with overlap and collage effects."""
import math
import random
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
        
        Hero and stickers are sized based on their measured content size,
        creating a tight composition with minimal wasted space.
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Find hero widget to get its measured size
        hero_widget = next((w for w in widgets if w.role == "hero"), None)
        
        # Calculate hero size based on measured content
        if hero_widget and hero_widget.measured_size:
            # Use measured size with padding (15% for hero - tighter spacing)
            hero_width = hero_widget.measured_size.width * 1.15
            hero_height = hero_widget.measured_size.height * 1.15
            
            # Constrain only to maximum bounds (don't enforce minimum)
            max_hero_width = context.content_width * 0.8
            max_hero_height = context.content_height * 0.8
            
            hero_width = min(hero_width, max_hero_width)
            hero_height = min(hero_height, max_hero_height)
        else:
            # Fallback to 60% if no measured size
            hero_width = context.content_width * 0.6
            hero_height = context.content_height * 0.6
        
        # Center the hero
        hero_x = context.content_x + (context.content_width - hero_width) / 2
        hero_y = context.content_y + (context.content_height - hero_height) / 2
        
        # Hero bounds for collision detection
        hero_bounds = Bounds(x=hero_x, y=hero_y, width=hero_width, height=hero_height)
        
        # Minimum size fallback (12% of content area)
        min_sticker_size = min(context.content_width, context.content_height) * 0.12
        
        # Maximum size limit (20% of content area to avoid too large stickers)
        max_sticker_size = min(context.content_width, context.content_height) * 0.20
        
        # Helper function to check bounds collision
        def bounds_collide(b1: Bounds, b2: Bounds, margin: float = 10) -> bool:
            """Check if two bounds overlap with optional margin."""
            return not (b1.x + b1.width + margin < b2.x or
                       b2.x + b2.width + margin < b1.x or
                       b1.y + b1.height + margin < b2.y or
                       b2.y + b2.height + margin < b1.y)
        
        # Collect all sticker widgets with their sizes
        stickers = []
        for widget in widgets:
            if widget.role.startswith("sticker_"):
                # Calculate sticker size
                if widget.measured_size:
                    sticker_width = widget.measured_size.width * 1.1
                    sticker_height = widget.measured_size.height * 1.1
                    sticker_width = max(min_sticker_size, min(sticker_width, max_sticker_size))
                    sticker_height = max(min_sticker_size, min(sticker_height, max_sticker_size))
                    sticker_size = max(sticker_width, sticker_height)
                else:
                    sticker_size = min_sticker_size
                
                stickers.append({
                    'role': widget.role,
                    'size': sticker_size
                })
        
        # Generate random initial positions around hero and push away until no collision
        hero_center_x = hero_x + hero_width / 2
        hero_center_y = hero_y + hero_height / 2
        
        for sticker in stickers:
            # Random angle and initial distance from hero center
            angle = random.uniform(0, 2 * math.pi)
            initial_distance = min(hero_width, hero_height) * 0.3
            
            # Start position near hero
            pos_x = hero_center_x + math.cos(angle) * initial_distance - sticker['size'] / 2
            pos_y = hero_center_y + math.sin(angle) * initial_distance - sticker['size'] / 2
            
            # Push away from hero and other stickers until no collision
            max_iterations = 50
            push_step = 15  # pixels to push per iteration
            
            for _ in range(max_iterations):
                current_bounds = Bounds(x=pos_x, y=pos_y, width=sticker['size'], height=sticker['size'])
                
                # Check collision with hero
                collision = bounds_collide(current_bounds, hero_bounds, margin=15)
                
                # Check collision with already placed stickers
                if not collision:
                    for placed_role, placed_bounds in bounds_map.items():
                        if placed_role != 'hero':
                            if bounds_collide(current_bounds, placed_bounds, margin=10):
                                collision = True
                                break
                
                # No collision - we're done
                if not collision:
                    # Make sure within canvas bounds
                    pos_x = max(context.content_x, min(pos_x, context.content_x + context.content_width - sticker['size']))
                    pos_y = max(context.content_y, min(pos_y, context.content_y + context.content_height - sticker['size']))
                    break
                
                # Push away from hero along the angle
                pos_x += math.cos(angle) * push_step
                pos_y += math.sin(angle) * push_step
            
            bounds_map[sticker['role']] = Bounds(
                x=pos_x,
                y=pos_y,
                width=sticker['size'],
                height=sticker['size']
            )
        
        # Add hero to bounds_map
        bounds_map["hero"] = hero_bounds
        
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
