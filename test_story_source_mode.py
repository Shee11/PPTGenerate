"""Test story generation from source content (SCQA mode)."""
from pathlib import Path
from src.generation.state import PipelineState
from src.tools.story import StoryTool

def test_story_from_source():
    """Test generating story directly from source without atoms."""
    
    # Create a test source file
    test_content = """
    AI Meeting Assistant Product Vision
    
    Current Situation:
    - Teams spend 3 hours per week in meetings
    - 70% of meetings lack proper documentation
    - Action items are frequently lost or forgotten
    - Meeting ROI is declining year over year
    
    The Problem:
    - Manual note-taking reduces engagement
    - Post-meeting write-ups delay by 2-3 days
    - Critical decisions buried in transcripts
    - No actionable artifacts from discussions
    
    Our Solution:
    - Real-time AI transcription and summarization
    - Automatic action item extraction
    - Instant meeting briefs and reports
    - Integration with task management tools
    
    Market Opportunity:
    - $50B enterprise collaboration market
    - 80% CAGR in AI productivity tools
    - 15M potential enterprise users
    
    Our Advantage:
    - Proprietary meeting intelligence engine
    - 95% accuracy on technical jargon
    - Multi-language support (12 languages)
    - Enterprise-grade security and compliance
    """
    
    test_file = Path("test_source.txt")
    test_file.write_text(test_content)
    
    try:
        # Create state with source
        state = PipelineState()
        state.set_source(test_file)
        
        # Create story tool
        tool = StoryTool(verbose=True)
        
        # Test generate mode (should use source)
        print("\n=== Testing GENERATE mode (source-based) ===")
        context = tool.slice(state, params={"mode": "generate", "slide_count": 10})
        
        # Verify context
        assert context.source_content is not None, "Should have source content"
        assert context.atoms_collection is None, "Should not have atoms in generate mode"
        print(f"✓ Source content: {len(context.source_content)} chars")
        
        # Generate story
        patch = tool.transform(context, "Create an executive pitch deck using SCQA framework")
        
        print(f"✓ Generated {len(patch.slides)} slides")
        
        # Verify slide structure
        for i, slide in enumerate(patch.slides[:3], 1):
            print(f"\nSlide {i}:")
            print(f"  ID: {slide.get('id')}")
            print(f"  Story: {slide.get('story', '')[:100]}...")
            print(f"  Density: {slide.get('density')}")
            print(f"  Has content: {bool(slide.get('content'))}")
            print(f"  Content category: {slide.get('content', {}).get('category', 'N/A')}")
        
        # Apply patch to state
        tool.apply(state, patch)
        assert len(state.slides) == len(patch.slides), "Slides should be applied to state"
        print(f"\n✓ Applied {len(state.slides)} slides to state")
        
        # Test refine mode (should use atoms if available)
        print("\n=== Testing REFINE mode (would use atoms) ===")
        # Note: This will fail without atoms, which is expected
        try:
            refine_context = tool.slice(state, params={"mode": "refine"})
            print("  Refine mode requires atoms (not testing full flow)")
        except Exception as e:
            print(f"  Expected: Refine mode needs atoms - {type(e).__name__}")
        
        print("\n✅ All tests passed!")
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


if __name__ == "__main__":
    test_story_from_source()
