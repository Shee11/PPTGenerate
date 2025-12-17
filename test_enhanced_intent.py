"""Test enhanced intent detection with stage changes and atom extraction tasks."""

from src.generation.intent.detector import detect_intent

# Test with career talk example
user_instruction = "Generate slides, target audience is entry, mid level devs, high contrast style"

source_preview = """
I started my journey in tech after graduating from a coding bootcamp in 2018. 
Coming from a non-technical background, I faced many challenges learning to code.

My first job was as a junior frontend developer at a small startup. I learned React, 
JavaScript, and how to work in a team. The biggest lesson I learned was the importance
of asking questions and not being afraid to say "I don't know."

After two years, I moved to a larger company as a mid-level engineer. This is where
I really grew. I learned system design, mentored junior developers, and started 
contributing to open source projects.

Key skills that helped me progress:
- Strong fundamentals in JavaScript and TypeScript
- Understanding of system design patterns
- Communication and collaboration skills
- Continuous learning mindset

Advice for aspiring developers:
1. Focus on fundamentals before frameworks
2. Build projects, not just tutorials
3. Contribute to open source
4. Network and find mentors
5. Never stop learning
"""

# Test with multiple sources
source_refs = [
    {
        'ref': 'career_transcript',
        'summary': 'Career journey from bootcamp to senior engineer, lessons learned, skills developed'
    },
    {
        'ref': 'tech_skills_doc',
        'summary': 'Detailed breakdown of technical skills: JavaScript, TypeScript, React, system design'
    }
]

print("=" * 80)
print("Testing Enhanced Intent Detection")
print("=" * 80)

try:
    # Test with source_refs
    print("\n--- Test 1: With source_refs (multi-source) ---")
    intent = detect_intent(
        user_instruction=user_instruction,
        source_preview=source_preview,
        source_refs=source_refs,
        use_cache=False
    )
    
    print(f"\n✓ Intent Detection Results:")
    print(f"  Audience: {intent.audience}")
    print(f"  Pattern: {intent.pattern}")
    print(f"  Tone: {intent.tone}")
    print(f"  Visual Density: {intent.visual_density}")
    
    print(f"\n  Atom Extraction Tasks: {len(intent.atom_extraction_tasks)}")
    for i, task in enumerate(intent.atom_extraction_tasks, 1):
        print(f"    {i}. {task.source_ref} (priority {task.priority})")
        print(f"       Summary: {task.source_summary[:80]}...")
        print(f"       Prompt: {task.extraction_prompt[:100]}...")
    
    print(f"\n  Stage Changes: {len(intent.stage_changes)}")
    for stage in intent.stage_changes:
        status = "✓ Execute" if stage.should_execute else "⊘ Skip"
        print(f"    {status} | {stage.stage_name}")
        print(f"       Guidance: {stage.guidance[:80]}...")
        if stage.parameters:
            print(f"       Parameters: {stage.parameters}")
    
    print(f"\n  Reasoning: {intent.reasoning}")
    
    # Test without source_refs
    print("\n\n--- Test 2: Without source_refs (single-source) ---")
    intent2 = detect_intent(
        user_instruction=user_instruction,
        source_preview=source_preview,
        source_refs=None,
        use_cache=False
    )
    
    print(f"\n✓ Intent Detection Results:")
    print(f"  Audience: {intent2.audience}")
    print(f"  Pattern: {intent2.pattern}")
    print(f"  Atom Extraction Tasks: {len(intent2.atom_extraction_tasks)} (should be 0 for single source)")
    print(f"  Stage Changes: {len(intent2.stage_changes)}")
    
    print("\n" + "=" * 80)
    print("✓ Tests completed successfully!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
