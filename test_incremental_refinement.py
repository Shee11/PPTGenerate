"""Test incremental refinement capability."""
import tempfile
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from src.generation.orchestrator import GenerationOrchestrator

# Create a test source file
test_content = """
Python Best Practices for Beginners

1. Use descriptive variable names
2. Write comments for complex logic
3. Follow PEP 8 style guide
4. Use version control (Git)
5. Write unit tests
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write(test_content)
    test_file = Path(f.name)

try:
    print("=" * 80)
    print("Testing Incremental Refinement")
    print("=" * 80)
    
    orchestrator = GenerationOrchestrator(use_cache=False)
    
    # Initial generation
    print("\n--- Initial Generation ---")
    slides_1 = orchestrator.generate_from_source(
        source_path=test_file,
        user_instruction="Create 5 tutorial slides"  # Simpler instruction to avoid embedded content detection
    )
    print(f"\n✓ Generated {len(slides_1.list_contexts())} slides initially")
    
    state_1 = orchestrator.get_current_state()
    print(f"State: {state_1['slides_count']} slides, {state_1['atoms_count']} atoms")
    
    # First refinement - should use incremental patching
    print("\n--- Refinement 1: Make it more technical ---")
    slides_2 = orchestrator.regenerate_with_instruction(
        new_instruction="Make it more technical with code examples"
    )
    print(f"\n✓ Refined to {len(slides_2.list_contexts())} slides")
    
    state_2 = orchestrator.get_current_state()
    print(f"State: {state_2['slides_count']} slides, {state_2['atoms_count']} atoms (reused)")
    
    # Second refinement - should continue incremental patching
    print("\n--- Refinement 2: Simplify ---")
    slides_3 = orchestrator.regenerate_with_instruction(
        new_instruction="Simplify for absolute beginners"
    )
    print(f"\n✓ Refined to {len(slides_3.list_contexts())} slides")
    
    print("\n" + "=" * 80)
    print("✓ Incremental Refinement Test Completed")
    print("=" * 80)
    print("\nKey observation:")
    print("- If you see '🔧 Applying incremental refinement' → SUCCESS")
    print("- If you see '⚙ Generating slide storyline' → Still full regeneration")
    
finally:
    # Cleanup
    test_file.unlink()
    print("\n✓ Cleaned up test file")
