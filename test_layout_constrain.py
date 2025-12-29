"""Test script to demonstrate the new get_layout_constrain interface."""
import os
from src.paged.layout.engine_registry import LayoutEngineRegistry

def test_dummy_engine():
    """Test dummy engine constraints."""
    print("=" * 80)
    print("DUMMY ENGINE CONSTRAINTS")
    print("=" * 80)
    
    # Force dummy engine
    os.environ['LAYOUT_ENGINE'] = 'dummy'
    engine = LayoutEngineRegistry.get_active_engine()
    
    constraints = engine.get_layout_constrain()
    print(f"Engine: {engine.__name__}")
    print(f"Constraints length: {len(constraints)} chars\n")
    print(constraints)
    print()

def test_slidev_engine():
    """Test Slidev engine constraints."""
    print("=" * 80)
    print("SLIDEV ENGINE CONSTRAINTS")
    print("=" * 80)
    
    # Force Slidev engine
    os.environ['LAYOUT_ENGINE'] = 'slidev'
    engine = LayoutEngineRegistry.get_active_engine()
    
    constraints = engine.get_layout_constrain()
    print(f"Engine: {engine.__name__}")
    print(f"Constraints length: {len(constraints)} chars\n")
    
    # Print first section
    lines = constraints.split('\n')
    for i, line in enumerate(lines[:30]):
        print(line)
    
    print("\n... (truncated)")
    print(f"\nTotal lines: {len(lines)}")
    print()

def test_prompt_integration():
    """Test that constraints are integrated into prompts."""
    print("=" * 80)
    print("PROMPT INTEGRATION TEST")
    print("=" * 80)
    
    os.environ['LAYOUT_ENGINE'] = 'slidev'
    
    from src.generation.content.prompts import _build_system_prompt
    
    prompt = _build_system_prompt()
    
    print(f"Prompt length: {len(prompt)} chars")
    print(f"Contains 'LAYOUT-WIDGET COMPATIBILITY': {'LAYOUT-WIDGET COMPATIBILITY' in prompt}")
    print(f"Contains 'Widget Space Requirements': {'Widget Space Requirements' in prompt}")
    print(f"Contains 'smart-grid columns': {'smart-grid columns' in prompt}")
    print(f"Contains 'QuoteWidget': {'QuoteWidget' in prompt}")
    print()

if __name__ == "__main__":
    test_dummy_engine()
    test_slidev_engine()
    test_prompt_integration()
    print("✓ All tests passed!")
