"""Paged presentation engine.

This package combines layout, render, widgets, and tool protocols for paged presentations.
"Paged" distinguishes from other formats like:
- sectioned (documents)
- noded (flashcards)

Structure:
- layout/: Layout strategies and engine registry
- render/: Renderers (Slidev, HTML)
- widgets/: Widget definitions
- content.py: ContentTool - connects atoms to layout engine (LLM)
- export.py: ExportTool - connects slides to renderer (Direct)

Usage:
    from src.paged.layout import LayoutEngineRegistry
    from src.paged.render import SlidevRenderer
    from src.paged.content import ContentTool
    from src.paged.export import ExportTool
"""
# Lazy imports to avoid loading heavy modules eagerly
# Users should import from submodules directly

__all__ = [
    "layout",
    "render", 
    "widgets",
    "content",
    "export",
]
