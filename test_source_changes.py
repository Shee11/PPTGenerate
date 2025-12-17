"""Test intent detection with embedded user content (source_changes)."""

import sys
import io

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.generation.intent.detector import detect_intent

print("=" * 80)
print("Testing Source Changes Detection (User-Provided Embedded Content)")
print("=" * 80)

# Test 1: User provides explicit list of topics in instruction
print("\n--- Test 1: Explicit Topic List ---")
user_instruction_1 = """
Create slides about AI for executives. Cover these key topics:
1. AI Safety - ensuring AI systems behave as intended and don't cause harm
2. Ethics - moral implications of AI decisions and bias
3. Regulation - need for government oversight and standards
4. Business Impact - ROI and competitive advantages

Use professional tone with data-driven approach.
"""

source_preview_1 = "General AI industry report with statistics and trends."

# Provide source_refs to simulate original source
source_refs_1 = [
    {
        'ref': 'ai_industry_report',
        'summary': 'General AI industry report with statistics and trends'
    }
]

try:
    intent_1 = detect_intent(
        user_instruction=user_instruction_1,
        source_preview=source_preview_1,
        source_refs=source_refs_1,  # Now providing source_refs
        use_cache=False
    )
    
    print(f"\n✓ Intent Detected:")
    print(f"  Audience: {intent_1.audience}")
    print(f"  Pattern: {intent_1.pattern}")
    
    print(f"\n  Source Changes: {len(intent_1.source_changes)}")
    for src_change in intent_1.source_changes:
        print(f"    + {src_change.source_ref} ({src_change.source_type})")
        print(f"      Should create: {src_change.should_create}")
        print(f"      Content preview: {src_change.content[:100]}...")
        print(f"      Metadata: {src_change.metadata}")
    
    print(f"\n  Atom Extraction Tasks: {len(intent_1.atom_extraction_tasks)}")
    for task in intent_1.atom_extraction_tasks:
        requires_marker = " [REQUIRES CREATION]" if task.requires_source_creation else ""
        print(f"    - {task.source_ref} (priority {task.priority}){requires_marker}")
        print(f"      Prompt: {task.extraction_prompt[:80]}...")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: User provides inline data
print("\n\n--- Test 2: Inline Data ---")
user_instruction_2 = """
Create quarterly results presentation. Show these metrics:
- Q1 Revenue: $2.5M
- Q2 Revenue: $3.8M  
- Q3 Revenue: $4.2M
- Q4 Revenue: $5.1M

Also include this quote from CEO: "Our growth trajectory exceeded all expectations, 
driven by strong customer retention and new market expansion."

Target audience: investors, use pitch pattern.
"""

source_preview_2 = "Annual report PDF with detailed financial information."

source_refs_2 = [
    {
        'ref': 'annual_report',
        'summary': 'Annual report PDF with detailed financial information'
    }
]

try:
    intent_2 = detect_intent(
        user_instruction=user_instruction_2,
        source_preview=source_preview_2,
        source_refs=source_refs_2,
        use_cache=False
    )
    
    print(f"\n✓ Intent Detected:")
    print(f"  Pattern: {intent_2.pattern}")
    
    print(f"\n  Source Changes: {len(intent_2.source_changes)}")
    for src_change in intent_2.source_changes:
        print(f"    + {src_change.source_ref}")
        print(f"      Content: {src_change.content[:150]}...")
    
    print(f"\n  Atom Extraction Tasks: {len(intent_2.atom_extraction_tasks)}")
    for task in intent_2.atom_extraction_tasks:
        requires_marker = " [REQUIRES CREATION]" if task.requires_source_creation else ""
        print(f"    - {task.source_ref}{requires_marker}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: User provides structured agenda
print("\n\n--- Test 3: Structured Agenda ---")
user_instruction_3 = """
Create product demo presentation following this structure:
- Introduction: Who we are and what we solve
- Problem: Current pain points in the market
- Solution: Our product features and benefits  
- Demo: Live walkthrough of key capabilities
- Pricing: Three tier pricing model
- Next Steps: Call to action

Keep it energetic and visual-heavy.
"""

source_preview_3 = "Product documentation and feature descriptions."

source_refs_3 = [
    {
        'ref': 'product_docs',
        'summary': 'Product documentation and feature descriptions'
    }
]

try:
    intent_3 = detect_intent(
        user_instruction=user_instruction_3,
        source_preview=source_preview_3,
        source_refs=source_refs_3,
        use_cache=False
    )
    
    print(f"\n✓ Intent Detected:")
    print(f"  Pattern: {intent_3.pattern}")
    print(f"  Tone: {intent_3.tone}")
    
    print(f"\n  Source Changes: {len(intent_3.source_changes)}")
    for src_change in intent_3.source_changes:
        print(f"    + {src_change.source_ref}")
        print(f"      Content format: {src_change.content_format}")
        print(f"      Content: {src_change.content[:120]}...")
    
    print(f"\n  Atom Extraction Tasks: {len(intent_3.atom_extraction_tasks)}")
    for task in intent_3.atom_extraction_tasks:
        requires_marker = " ✓ USER-PROVIDED" if task.requires_source_creation else " ○ ORIGINAL"
        print(f"    {requires_marker} | {task.source_ref} (priority {task.priority})")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: No embedded content (should have empty source_changes)
print("\n\n--- Test 4: No Embedded Content (Control) ---")
user_instruction_4 = "Create technical tutorial for developers, focus on best practices and code examples."

source_preview_4 = "Python programming guide with examples and explanations."

try:
    intent_4 = detect_intent(
        user_instruction=user_instruction_4,
        source_preview=source_preview_4,
        source_refs=None,
        use_cache=False
    )
    
    print(f"\n✓ Intent Detected:")
    print(f"  Pattern: {intent_4.pattern}")
    
    print(f"\n  Source Changes: {len(intent_4.source_changes)} (should be 0 - no embedded content)")
    print(f"  Atom Extraction Tasks: {len(intent_4.atom_extraction_tasks)}")
    
    if len(intent_4.source_changes) == 0:
        print("\n  ✓ Correctly detected no embedded content in instruction")
    else:
        print("\n  ⚠ Warning: False positive - detected source changes when there shouldn't be any")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✓ Source Changes Tests Completed")
print("=" * 80)
