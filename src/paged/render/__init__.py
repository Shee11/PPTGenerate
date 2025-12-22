"""Rendering components and widgets."""
from src.paged.render.renderer_protocol import Renderer
from src.paged.render.slidev.markdown_renderer import SlidevRenderer
from src.paged.render.dummy.html_renderer import HTMLRenderer

__all__ = [
    "Renderer",
    "SlidevRenderer",
    "HTMLRenderer",
]
