"""Layout engine registry for runtime engine selection.

This module provides a central registry for layout engine implementations,
allowing runtime selection via configuration or environment variables.
"""
import os
from typing import Type, Dict, Optional
from src.paged.layout.layout_engine_protocol import LayoutEngine


class LayoutEngineRegistry:
    """Registry for layout engine implementations.
    
    Allows registration and runtime selection of layout engines.
    Supports environment variable configuration and programmatic selection.
    
    Example usage:
        # Register engines
        LayoutEngineRegistry.register("dummy", DummyLayoutEngine)
        LayoutEngineRegistry.register("advanced", AdvancedLayoutEngine)
        
        # Select at runtime
        engine = LayoutEngineRegistry.get_active_engine()
        docs = engine.get_layout_prompt()
    """
    
    _engines: Dict[str, Type[LayoutEngine]] = {}
    _active_engine_name: Optional[str] = None
    
    @classmethod
    def register(cls, name: str, engine_class: Type[LayoutEngine]) -> None:
        """Register a layout engine implementation.
        
        Args:
            name: Unique identifier for this engine (e.g., "dummy", "advanced")
            engine_class: Layout engine class implementing LayoutEngine protocol
            
        Raises:
            ValueError: If name is already registered
        """
        if name in cls._engines:
            raise ValueError(f"Layout engine '{name}' is already registered")
        
        cls._engines[name] = engine_class
        
        # Set as active if it's the first registered engine
        if cls._active_engine_name is None:
            cls._active_engine_name = name
    
    @classmethod
    def get_engine(cls, name: str) -> Type[LayoutEngine]:
        """Get a specific layout engine by name.
        
        Args:
            name: Engine identifier
            
        Returns:
            Layout engine class
            
        Raises:
            KeyError: If engine not found
        """
        if name not in cls._engines:
            available = ", ".join(cls._engines.keys())
            raise KeyError(
                f"Layout engine '{name}' not found. "
                f"Available engines: {available}"
            )
        
        return cls._engines[name]
    
    @classmethod
    def get_active_engine(cls) -> Type[LayoutEngine]:
        """Get the currently active layout engine.
        
        The active engine is determined by (in priority order):
        1. Programmatically set via set_active_engine()
        2. LAYOUT_ENGINE environment variable
        3. First registered engine (default)
        
        Returns:
            Currently active layout engine class
            
        Raises:
            RuntimeError: If no engines registered
        """
        if not cls._engines:
            raise RuntimeError(
                "No layout engines registered. "
                "Register at least one engine using LayoutEngineRegistry.register()"
            )
        
        # Check environment variable override
        env_engine = os.getenv("LAYOUT_ENGINE")
        if env_engine and env_engine in cls._engines:
            return cls._engines[env_engine]
        
        # Use programmatically set active engine
        if cls._active_engine_name:
            return cls._engines[cls._active_engine_name]
        
        # Fallback to first registered (shouldn't happen due to register() logic)
        return next(iter(cls._engines.values()))
    
    @classmethod
    def set_active_engine(cls, name: str) -> None:
        """Set the active layout engine programmatically.
        
        Args:
            name: Engine identifier
            
        Raises:
            KeyError: If engine not found
        """
        if name not in cls._engines:
            available = ", ".join(cls._engines.keys())
            raise KeyError(
                f"Cannot set active engine '{name}' - not registered. "
                f"Available engines: {available}"
            )
        
        cls._active_engine_name = name
    
    @classmethod
    def list_engines(cls) -> Dict[str, Type[LayoutEngine]]:
        """List all registered layout engines.
        
        Returns:
            Dictionary mapping engine names to engine classes
        """
        return cls._engines.copy()
    
    @classmethod
    def get_active_engine_name(cls) -> Optional[str]:
        """Get the name of the currently active engine.
        
        Returns:
            Active engine name or None if no engines registered
        """
        if not cls._engines:
            return None
        
        # Check environment variable
        env_engine = os.getenv("LAYOUT_ENGINE")
        if env_engine and env_engine in cls._engines:
            return env_engine
        
        return cls._active_engine_name
    
    @classmethod
    def reset(cls) -> None:
        """Reset registry (primarily for testing).
        
        Clears all registered engines and active engine selection.
        """
        cls._engines.clear()
        cls._active_engine_name = None


# Auto-register dummy engine on module import
def _auto_register_dummy_engine():
    """Automatically register the dummy layout engine."""
    try:
        from src.paged.layout.dummy.layout_engine import LayoutEngine as DummyLayoutEngine
        LayoutEngineRegistry.register("dummy", DummyLayoutEngine)
    except ImportError:
        # Dummy engine not available, continue without it
        pass


def _auto_register_react_engine():
    """Automatically register the React MDX layout engine."""
    try:
        from src.paged.layout.react.layout_engine import ReactLayoutEngine
        LayoutEngineRegistry.register("react", ReactLayoutEngine)
    except ImportError:
        # React engine not available, continue without it
        pass


_auto_register_dummy_engine()
_auto_register_react_engine()
