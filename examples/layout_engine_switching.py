"""Example demonstrating runtime layout engine switching.

This script shows three ways to switch layout engines at runtime:
1. Environment variable (LAYOUT_ENGINE)
2. Programmatic selection
3. Registering custom engines

Run this file to see all three methods in action.
"""
import os
from src.layout.engine_registry import LayoutEngineRegistry
from src.layout.layout_engine_protocol import LayoutEngine


# ========== Method 1: Environment Variable ==========

def demo_env_variable_switching():
    """Demonstrate switching via LAYOUT_ENGINE environment variable."""
    print("=" * 60)
    print("Method 1: Environment Variable Switching")
    print("=" * 60)
    
    # Show current active engine
    print(f"Current active engine: {LayoutEngineRegistry.get_active_engine_name()}")
    print(f"Available engines: {list(LayoutEngineRegistry.list_engines().keys())}")
    
    # Set environment variable
    os.environ["LAYOUT_ENGINE"] = "dummy"
    print(f"\nSet LAYOUT_ENGINE=dummy")
    print(f"Active engine: {LayoutEngineRegistry.get_active_engine_name()}")
    
    # Get documentation from active engine
    active = LayoutEngineRegistry.get_active_engine()
    docs = active.get_layout_documentation()
    print(f"Documentation preview: {docs[:100]}...")
    
    # Clean up
    del os.environ["LAYOUT_ENGINE"]
    print()


# ========== Method 2: Programmatic Selection ==========

def demo_programmatic_switching():
    """Demonstrate programmatic engine selection."""
    print("=" * 60)
    print("Method 2: Programmatic Switching")
    print("=" * 60)
    
    # List available engines
    engines = LayoutEngineRegistry.list_engines()
    print(f"Available engines: {list(engines.keys())}")
    
    # Switch to specific engine
    LayoutEngineRegistry.set_active_engine("dummy")
    print(f"\nCalled: LayoutEngineRegistry.set_active_engine('dummy')")
    print(f"Active engine: {LayoutEngineRegistry.get_active_engine_name()}")
    
    # Get active engine and use it
    engine = LayoutEngineRegistry.get_active_engine()
    print(f"Engine class: {engine.__name__}")
    print()


# ========== Method 3: Registering Custom Engines ==========

class CustomLayoutEngine:
    """Example custom layout engine implementation."""
    
    @classmethod
    def get_layout_documentation(cls) -> str:
        """Provide custom layout documentation."""
        return """Available Layout Strategies:

Custom Family: Experimental layouts for advanced use cases.
  - Custom.Holographic: Slots: [projection (size: XL)]
  - Custom.Parallax: Slots: [foreground (size: L), background (size: L)]
  
Advanced Family: AI-generated adaptive layouts.
  - Advanced.Adaptive: Slots: [dynamic (size: varies)]
"""
    
    @classmethod
    def calculate(cls, strategy_name, widget_assignments, theme, style, width=1920, height=1080):
        """Calculate layout (simplified for demo)."""
        raise NotImplementedError("Demo engine - calculation not implemented")
    
    @classmethod
    def calculate_slides(cls, slides, theme, style, width=1920, height=1080):
        """Calculate slides (simplified for demo)."""
        raise NotImplementedError("Demo engine - calculation not implemented")


def demo_custom_engine_registration():
    """Demonstrate registering and using custom engines."""
    print("=" * 60)
    print("Method 3: Custom Engine Registration")
    print("=" * 60)
    
    # Register custom engine
    LayoutEngineRegistry.register("custom", CustomLayoutEngine)
    print("Registered custom engine: 'custom'")
    
    # List engines
    engines = LayoutEngineRegistry.list_engines()
    print(f"Available engines: {list(engines.keys())}")
    
    # Switch to custom engine
    LayoutEngineRegistry.set_active_engine("custom")
    print(f"\nActive engine: {LayoutEngineRegistry.get_active_engine_name()}")
    
    # Get documentation from custom engine
    engine = LayoutEngineRegistry.get_active_engine()
    docs = engine.get_layout_documentation()
    print(f"\nCustom engine documentation:\n{docs}")
    
    # Switch back to dummy
    LayoutEngineRegistry.set_active_engine("dummy")
    print(f"Switched back to: {LayoutEngineRegistry.get_active_engine_name()}")
    print()


# ========== Practical Usage Scenario ==========

def demo_practical_usage():
    """Demonstrate practical usage in content generation."""
    print("=" * 60)
    print("Practical Usage: Content Generation Integration")
    print("=" * 60)
    
    # This is what happens inside prompts.py
    print("Inside content generation prompts:")
    print("```python")
    print("# Get active engine (respects env var and programmatic selection)")
    print("active_engine = LayoutEngineRegistry.get_active_engine()")
    print("layout_docs = active_engine.get_layout_documentation()")
    print("# ... use layout_docs in LLM prompt")
    print("```")
    print()
    
    # Show it in action
    from src.generation.content.prompts import _build_state_transition_system_prompt
    
    print("Current configuration:")
    print(f"  Active engine: {LayoutEngineRegistry.get_active_engine_name()}")
    
    # Generate prompt (uses active engine)
    prompt = _build_state_transition_system_prompt()
    
    # Check what's in the prompt
    if "Bento Family:" in prompt:
        print("  ✓ Prompt contains Bento layouts (from dummy engine)")
    
    print(f"  Prompt length: {len(prompt)} characters")
    print()


# ========== CLI Usage Examples ==========

def show_cli_examples():
    """Show how to use engine switching in CLI."""
    print("=" * 60)
    print("CLI Usage Examples")
    print("=" * 60)
    print()
    
    print("1. Use default engine (dummy):")
    print("   $ python -m cli.uce_render data/test_01.json")
    print()
    
    print("2. Switch engine via environment variable:")
    print("   $ set LAYOUT_ENGINE=custom")
    print("   $ python -m cli.uce_render data/test_01.json")
    print()
    
    print("3. In Python code before running CLI:")
    print("   from src.layout.engine_registry import LayoutEngineRegistry")
    print("   LayoutEngineRegistry.set_active_engine('custom')")
    print("   # Now run your generation...")
    print()


if __name__ == "__main__":
    print("\n🎨 Layout Engine Runtime Switching Demo\n")
    
    # Run all demonstrations
    demo_env_variable_switching()
    demo_programmatic_switching()
    demo_custom_engine_registration()
    demo_practical_usage()
    show_cli_examples()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
The registry pattern allows you to:
✓ Register multiple layout engines
✓ Switch between them at runtime
✓ Use environment variables for configuration
✓ Integrate seamlessly with content generation

When you create a new layout engine:
1. Implement the LayoutEngine protocol
2. Register it: LayoutEngineRegistry.register("myengine", MyEngine)
3. Switch to it: LayoutEngineRegistry.set_active_engine("myengine")
   OR: export LAYOUT_ENGINE=myengine
4. Content generation automatically uses your engine!
""")
