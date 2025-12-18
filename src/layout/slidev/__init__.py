"""Slidev layout engine implementation."""
from src.layout.engine_registry import LayoutEngineRegistry
from src.layout.slidev.layout_engine import SlidevLayoutEngine

# Register Slidev engine with the registry
LayoutEngineRegistry.register("slidev", SlidevLayoutEngine)

__all__ = ["SlidevLayoutEngine"]
