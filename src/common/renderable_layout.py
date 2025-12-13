"""RenderableLayout model - output of LayoutEngine."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.common.bounds import Bounds
from src.common.slot import Slot
from src.widgets.base import BaseWidget


class WidgetAssignment(BaseModel):
    """Assignment of a widget to a slot with applied styling and calculated bounds.
    
    This contains:
    - Widget instance (content)
    - Slot definition (size constraints)
    - Applied style (resolved CSS properties)
    - Bounds (absolute position and size on canvas)
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    role: str = Field(..., description="Slot role name")
    widget: BaseWidget = Field(..., description="Widget instance")
    slot: Slot = Field(..., description="Slot definition")
    applied_style: Dict[str, Any] = Field(
        default_factory=dict,
        description="Resolved CSS properties from Style config and Theme tokens"
    )
    bounds: Bounds = Field(..., description="Absolute position and size on canvas (pixels)")


class RenderableLayout(BaseModel):
    """Complete layout ready for rendering.

    This is the output of the LayoutEngine and input to the HTMLRenderer.
    Contains all information needed to generate HTML, including theme-derived
    layout properties like margins, gutter, and header/footer configurations.
    
    For multi-slide layouts, includes slide metadata (slide_number, total_slides, slide_id).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    strategy_name: str = Field(..., description="Layout strategy used (e.g., 'Bento.Standard')")
    widget_assignments: List[WidgetAssignment] = Field(..., description="Widgets assigned to slots")
    theme_vars: Dict[str, str] = Field(default_factory=dict, description="CSS theme variables")
    style_props: Dict[str, str] = Field(default_factory=dict, description="CSS style properties")
    width: int = Field(default=1920, description="Layout width in pixels")
    height: int = Field(default=1080, description="Layout height in pixels")
    
    # Theme-derived layout properties (consumed from theme)
    margin_x: str = Field(default="40px", description="Horizontal margin from theme")
    margin_y: str = Field(default="30px", description="Vertical margin from theme")
    gutter: str = Field(default="20px", description="Widget spacing from theme")
    
    # Header/footer configuration (consumed from theme)
    header_height: str = Field(default="15%", description="Header reserved area height")
    footer_height: str = Field(default="10%", description="Footer reserved area height")
    header_position: str = Field(default="fixed_top_left", description="Header positioning")
    footer_position: str = Field(default="fixed_bottom_left", description="Footer positioning")
    header_decoration: str = Field(default="underline_accent", description="Header decoration style")
    footer_decoration: str = Field(default="none", description="Footer decoration style")
    header_widget: Any | None = Field(default=None, description="Widget instance for header area")
    footer_widget: Any | None = Field(default=None, description="Widget instance for footer area")
    
    # Multi-slide metadata (optional, set by calculate_slides)
    slide_number: Optional[int] = Field(default=None, description="Current slide number (1-indexed)")
    total_slides: Optional[int] = Field(default=None, description="Total number of slides")
    slide_id: Optional[str] = Field(default=None, description="Slide identifier")
    background_override: Optional[str] = Field(default=None, description="Background color from sequence pattern")

    def get_assignment(self, role: str) -> WidgetAssignment | None:
        """Get widget assignment by slot role.
        
        Args:
            role: Slot role name
            
        Returns:
            WidgetAssignment if found, None otherwise
        """
        for assignment in self.widget_assignments:
            if assignment.role == role:
                return assignment
        return None
