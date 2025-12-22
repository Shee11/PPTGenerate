"""Slidev layout engine implementation."""
from src.paged.layout.engine_registry import LayoutEngineRegistry
from src.paged.layout.slidev.layout_engine import SlidevLayoutEngine

# Register Slidev engine with the registry
LayoutEngineRegistry.register("slidev", SlidevLayoutEngine)

__all__ = ["SlidevLayoutEngine"]
