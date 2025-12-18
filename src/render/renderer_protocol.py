"""Renderer protocol for converting RenderableLayout to output format."""
from typing import Protocol, List, Union
from src.common.renderable_layout import RenderableLayout


class Renderer(Protocol):
    """Protocol for renderer implementations.
    
    Renderers convert RenderableLayout(s) into output format (HTML, PDF, etc.).
    They handle both single-slide and multi-slide presentations.
    """
    
    def render(self, renderable: Union[RenderableLayout, List[RenderableLayout]]) -> str:
        """Render layout(s) to output format.
        
        Args:
            renderable: Single RenderableLayout or list of RenderableLayouts for multi-slide
            
        Returns:
            Complete output string (e.g., HTML document)
        """
        ...
    
    def render_single_slide(self, renderable: RenderableLayout, slide_index: int = None) -> str:
        """Render a single RenderableLayout to output format.
        
        Args:
            renderable: Layout with all widget assignments and styling
            slide_index: Optional 1-based slide index for scoping in multi-slide presentations
            
        Returns:
            Output string for single slide
        """
        ...
    
    def render_multi_slide(self, renderables: List[RenderableLayout]) -> str:
        """Render multiple slides with navigation.
        
        Args:
            renderables: List of RenderableLayout instances
            
        Returns:
            Complete output with slide deck and navigation
        """
        ...
