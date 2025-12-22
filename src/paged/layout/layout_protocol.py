"""Layout strategy protocol for auto-layout algorithms."""
from typing import Protocol, List, Dict, Any
from src.common.bounds import Bounds
from src.common.slot import Slot
from src.common.measurement import MeasuredSize


class LayoutContext:
    """Context information for layout calculation."""
    
    def __init__(
        self,
        canvas_width: float,
        canvas_height: float,
        margin_x: float,
        margin_y: float,
        gutter: float,
        header_height: float = 0,
        footer_height: float = 0,
    ):
        """Initialize layout context.
        
        Args:
            canvas_width: Total canvas width in pixels
            canvas_height: Total canvas height in pixels
            margin_x: Horizontal margin from edges
            margin_y: Vertical margin from top/bottom
            gutter: Spacing between widgets
            header_height: Reserved header space (pixels or percentage converted to pixels)
            footer_height: Reserved footer space (pixels or percentage converted to pixels)
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.gutter = gutter
        self.header_height = header_height
        self.footer_height = footer_height
        
        # Calculate content area (excluding margins and header/footer)
        self.content_x = margin_x
        self.content_y = margin_y + header_height
        self.content_width = canvas_width - (margin_x * 2)
        # Content height: from after header to before footer (margins already in content_y)
        # Don't subtract bottom margin since footer position already accounts for it
        self.content_height = canvas_height - margin_y - header_height - footer_height - margin_y


class WidgetLayoutInput:
    """Input for widget layout calculation."""
    
    def __init__(
        self,
        role: str,
        measured_size: MeasuredSize,
        slot: Slot,
        style: Dict[str, Any],
    ):
        """Initialize widget layout input.
        
        Args:
            role: Slot role identifier
            measured_size: Measured content size
            slot: Slot definition with size constraints
            style: Applied style dictionary
        """
        self.role = role
        self.measured_size = measured_size
        self.slot = slot
        self.style = style


class LayoutStrategy(Protocol):
    """Protocol for layout strategy implementations.
    
    Each layout strategy must implement:
    1. get_strategy_name() - return strategy identifier
    2. get_slots() - return slot definitions
    3. calculate_layout() - perform auto-layout calculation
    """
    
    @staticmethod
    def get_strategy_name() -> str:
        """Return unique strategy name (e.g., 'Bento.Standard')."""
        ...
    
    @staticmethod
    def get_slots() -> List[Slot]:
        """Return slot definitions for this strategy.
        
        Slots define the available positions and size constraints,
        but NOT the actual pixel positions (calculated in calculate_layout).
        """
        ...
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate absolute positions and sizes for all widgets.
        
        This is the core auto-layout algorithm that:
        1. Takes measured widget sizes
        2. Takes layout context (canvas, margins, spacing)
        3. Calculates final absolute bounds for each widget
        
        Args:
            widgets: List of widgets with measured sizes
            context: Layout context with canvas dimensions and spacing
            
        Returns:
            Dictionary mapping role -> Bounds with absolute positions
            
        Note:
            - Bounds must be absolute positions relative to canvas (0, 0)
            - Implementation must handle collision avoidance
            - Must respect content area (exclude margins/header/footer)
            - Must apply gutter spacing between widgets
        """
        ...
