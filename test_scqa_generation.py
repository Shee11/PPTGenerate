"""Test SCQA story generation from source content."""
import json
from pathlib import Path
from src.generation.content.story_generator import generate_story_from_source


def main():
    # Read source content from file
    source_file = Path("data/context/output_driven_meeting.txt")
    print(f"Reading source content from: {source_file}")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()
    print("=" * 80)
    print("Testing SCQA Story Generation")
    print("=" * 80)
    
    # Call the function
    print("\nGenerating story from source content...")
    try:
        slides = generate_story_from_source(
            source_content=source_content,
            user_instruction="Create an executive pitch deck for leadership review",
            slide_count=12,
            intent_guidance="Focus on business value and competitive advantage"
        )
        
        print(f"\n✓ Generated {len(slides)} slides\n")
        
        # Display each slide
        for i, slide in enumerate(slides, 1):
            print(f"\n{'─' * 80}")
            print(f"SLIDE {i}: {slide.get('id', 'unknown')}")
            print(f"{'─' * 80}")
            print(f"Rank:          {slide.get('rank')}")
            print(f"Story:         {slide.get('story', 'N/A')}")
            print(f"Density:       {slide.get('density', 'N/A')}")
            print(f"Visual Design: {slide.get('visual_design', 'N/A')[:100]}...")
            
            content = slide.get('content', {})
            if content:
                print(f"\nCONTENT:")
                print(f"  Headline:  {content.get('headline', 'N/A')}")
                if content.get('subtitle'):
                    print(f"  Subtitle:  {content.get('subtitle')}")
                print(f"  Category:  {content.get('category', 'N/A')}")
                
                if content.get('sections'):
                    print(f"  Sections:  {len(content['sections'])} section(s)")
                    for section in content['sections']:
                        print(f"    - {section.get('title', 'Untitled')}: {len(section.get('bullets', []))} bullets")
        
        # Save full JSON output
        output_file = "test_scqa_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(slides, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'=' * 80}")
        print(f"✓ Full output saved to: {output_file}")
        print(f"{'=' * 80}\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
