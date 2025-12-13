"""Focus layout strategies with radial and minimal designs."""
import math
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class FocusSolarSystemStrategy:
    """Focus.Solar_System: Central hub with orbital elements.
    
    Layout: XL center + 6 S planets in circular orbit.
    Creates ecosystem diagrams and mind maps.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Focus.Solar_System"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return sun (XL) + 6 planet (S) slots."""
        return [
            Slot(role="sun", size=SizeClass.XL),
            Slot(role="planet_1", size=SizeClass.S),
            Slot(role="planet_2", size=SizeClass.S),
            Slot(role="planet_3", size=SizeClass.S),
            Slot(role="planet_4", size=SizeClass.S),
            Slot(role="planet_5", size=SizeClass.S),
            Slot(role="planet_6", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate solar system layout with center + orbital positions.
        
        Layout structure:
                [planet_1]
        [planet_6]  [sun]  [planet_2]
        [planet_5]         [planet_3]
                [planet_4]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Sun centered, 40% of content area
        sun_size = min(context.content_width, context.content_height) * 0.4
        sun_x = context.content_x + (context.content_width - sun_size) / 2
        sun_y = context.content_y + (context.content_height - sun_size) / 2
        
        # Planet size (12% of content area)
        planet_size = min(context.content_width, context.content_height) * 0.12
        
        # Orbital radius (40% of content dimension)
        orbit_radius = min(context.content_width, context.content_height) * 0.4
        
        # Center point
        center_x = context.content_x + context.content_width / 2
        center_y = context.content_y + context.content_height / 2
        
        for widget in widgets:
            if widget.role == "sun":
                bounds_map["sun"] = Bounds(
                    x=sun_x,
                    y=sun_y,
                    width=sun_size,
                    height=sun_size
                )
            elif widget.role.startswith("planet_"):
                # Extract planet number (1-6)
                planet_num = int(widget.role.split("_")[1]) - 1
                
                # Calculate angle (evenly distributed around circle)
                angle = (planet_num * 2 * math.pi) / 6
                
                # Calculate position on orbit
                planet_x = center_x + (orbit_radius * math.cos(angle)) - (planet_size / 2)
                planet_y = center_y + (orbit_radius * math.sin(angle)) - (planet_size / 2)
                
                bounds_map[widget.role] = Bounds(
                    x=planet_x,
                    y=planet_y,
                    width=planet_size,
                    height=planet_size
                )
        
        return bounds_map


class FocusOffsetTitleStrategy:
    """Focus.Offset_Title: Minimalist bottom-left title.
    
    Layout: Single M element in bottom-left corner, 90% whitespace.
    Perfect for chapter dividers and section breaks.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Focus.Offset_Title"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return single M slot for offset title."""
        return [
            Slot(role="main", size=SizeClass.M),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate minimalist offset title layout.
        
        Layout structure:
        [                        ]
        [                        ]
        [main (10%)]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Title occupies bottom-left 10% area
        title_width = context.content_width * 0.3
        title_height = context.content_height * 0.15
        
        # Position in bottom-left corner with small margin
        title_x = context.content_x
        title_y = context.content_y + context.content_height - title_height
        
        for widget in widgets:
            if widget.role == "main":
                bounds_map["main"] = Bounds(
                    x=title_x,
                    y=title_y,
                    width=title_width,
                    height=title_height
                )
        
        return bounds_map
