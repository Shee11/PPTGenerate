"""Test script to demonstrate intent detection."""
from src.generation.intent.detector import detect_intent

# Test different user instructions
test_cases = [
    {
        "instruction": "TechTuber style walkthrough - energetic and dev-focused",
        "preview": "A tech career journey with AI and LLMs"
    },
    {
        "instruction": "Create a professional pitch deck for investors",
        "preview": "Our startup has grown 300% year over year with $2M ARR"
    },
    {
        "instruction": "Step-by-step tutorial for beginners",
        "preview": "How to set up your first Python development environment"
    },
    {
        "instruction": "Quarterly business review for executives",
        "preview": "Q4 2024 results: Revenue up 15%, customer satisfaction at 92%"
    }
]

print("=" * 80)
print("INTENT DETECTION DEMO")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. User Instruction: \"{test['instruction']}\"")
    print(f"   Source Preview: \"{test['preview']}\"")
    print("-" * 80)
    
    try:
        intent = detect_intent(
            user_instruction=test["instruction"],
            source_preview=test["preview"],
            use_cache=False
        )
        
        print(f"   ✓ Detected:")
        print(f"     - Audience: {intent.audience}")
        print(f"     - Purpose: {intent.purpose}")
        print(f"     - Pattern: {intent.pattern}")
        print(f"     - Tone: {intent.tone}")
        print(f"     - Visual Density: {intent.visual_density}")
        print(f"     - Reasoning: {intent.reasoning}")
        print(f"   ✓ Atom Extraction Guidance:")
        print(f"     {intent.atom_extraction_guidance}")
        print(f"   ✓ Content Generation Guidance:")
        print(f"     {intent.content_generation_guidance}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n" + "=" * 80)
