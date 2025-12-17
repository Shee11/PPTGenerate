"""Integration tests for Slides state transitions (DRAFT → ACTIVE)."""
import pytest

from src.common.slides import Slides
from src.common.patchable_context_pydantic import (
    Patch,
    AddOperation,
    ReplaceOperation,
    PatchableContextState,
    PatchError
)


class TestSlideStateDraftTransition:
    """Test slides can be created in DRAFT state."""

    def test_add_slide_in_draft_state(self):
        """Verify slides can be added in DRAFT state."""
        slides = Slides()
        
        # Add slide in DRAFT state
        patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_001",
                "rank": 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Bento.Standard",
                "widgets": {},
                "parameters": {}
            })
        ])
        
        slides.patch(patch)
        
        # Verify slide exists in DRAFT state
        assert len(slides) == 1
        slide = slides.get("slide_001")
        assert slide is not None
        assert slide.state == PatchableContextState.DRAFT
        assert slide.strategy == "Bento.Standard"
        assert len(slide.widgets) == 0

    def test_add_multiple_slides_in_draft_state(self):
        """Verify multiple slides can be added in DRAFT state."""
        slides = Slides()
        
        patch = Patch(operations=[
            AddOperation(add={
                "id": f"slide_{i:03d}",
                "rank": i + 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Swiss.Poster",
                "widgets": {},
                "parameters": {}
            })
            for i in range(3)
        ])
        
        slides.patch(patch)
        
        assert len(slides) == 3
        for i in range(3):
            slide = slides.get(f"slide_{i:03d}")
            assert slide.state == PatchableContextState.DRAFT
            assert slide.rank == i + 1

    def test_draft_slides_not_included_in_active_slides(self):
        """Verify DRAFT slides are excluded from get_active_slides()."""
        slides = Slides()
        
        patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_001",
                "rank": 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Bento.Standard",
                "widgets": {},
                "parameters": {}
            }),
            AddOperation(add={
                "id": "slide_002",
                "rank": 2,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Swiss.Poster",
                "widgets": {"cell_1": {"type": "Type.Display", "parameters": {"text": "Active"}}},
                "parameters": {}
            })
        ])
        
        slides.patch(patch)
        
        # Only active slide should be returned
        active_slides = slides.get_active_slides()
        assert len(active_slides) == 1
        assert active_slides[0].id == "slide_002"
        assert active_slides[0].state == PatchableContextState.ACTIVE


class TestSlideStateActiveTransition:
    """Test slides can transition from DRAFT to ACTIVE."""

    def test_replace_draft_slide_to_active(self):
        """Verify slide can transition from DRAFT to ACTIVE via replace."""
        slides = Slides()
        
        # Create slide in DRAFT
        add_patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_001",
                "rank": 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Bento.Standard",
                "widgets": {},
                "parameters": {}
            })
        ])
        slides.patch(add_patch)
        
        # Transition to ACTIVE with populated widgets
        activate_patch = Patch(operations=[
            ReplaceOperation(replace={
                "id": "slide_001",
                "rank": 1,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Bento.Standard",
                "widgets": {
                    "cell_1": {
                        "type": "Type.Display",
                        "parameters": {"text": "Content", "size": 72}
                    }
                },
                "parameters": {}
            })
        ])
        slides.patch(activate_patch)
        
        # Verify state and content
        slide = slides.get("slide_001")
        assert slide.state == PatchableContextState.ACTIVE
        assert len(slide.widgets) == 1
        assert slide.widgets["cell_1"]["type"] == "Type.Display"

    def test_two_step_transition_multiple_slides(self):
        """Verify multiple slides can go DRAFT → ACTIVE in sequence."""
        slides = Slides()
        
        # Step 1: Create all slides in DRAFT
        draft_patch = Patch(operations=[
            AddOperation(add={
                "id": f"slide_{i:03d}",
                "rank": i + 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Focus.Solar_System",
                "widgets": {},
                "parameters": {}
            })
            for i in range(2)
        ])
        slides.patch(draft_patch)
        
        # Verify all in DRAFT
        assert len(slides.get_active_slides()) == 0
        
        # Step 2: Activate all with content
        activate_patch = Patch(operations=[
            ReplaceOperation(replace={
                "id": f"slide_{i:03d}",
                "rank": i + 1,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Focus.Solar_System",
                "widgets": {
                    "center": {
                        "type": "Type.Heading",
                        "parameters": {"text": f"Slide {i}", "level": 1}
                    }
                },
                "parameters": {}
            })
            for i in range(2)
        ])
        slides.patch(activate_patch)
        
        # Verify all now ACTIVE
        assert len(slides.get_active_slides()) == 2
        for i in range(2):
            slide = slides.get(f"slide_{i:03d}")
            assert slide.state == PatchableContextState.ACTIVE

    def test_partial_activation(self):
        """Verify only some slides can be activated while others stay DRAFT."""
        slides = Slides()
        
        # Create 3 slides in DRAFT
        patch = Patch(operations=[
            AddOperation(add={
                "id": f"slide_{i:03d}",
                "rank": i + 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Cinematic.Split_50_50",
                "widgets": {},
                "parameters": {}
            })
            for i in range(3)
        ])
        slides.patch(patch)
        
        # Activate only slide_001
        activate_patch = Patch(operations=[
            ReplaceOperation(replace={
                "id": "slide_001",
                "rank": 2,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Cinematic.Split_50_50",
                "widgets": {
                    "left": {"type": "Type.Body", "parameters": {"text": "Left content"}},
                    "right": {"type": "Type.Body", "parameters": {"text": "Right content"}}
                },
                "parameters": {}
            })
        ])
        slides.patch(activate_patch)
        
        # Verify mixed states
        active_slides = slides.get_active_slides()
        assert len(active_slides) == 1
        assert active_slides[0].id == "slide_001"
        
        assert slides.get("slide_000").state == PatchableContextState.DRAFT
        assert slides.get("slide_002").state == PatchableContextState.DRAFT


class TestSlideStateValidation:
    """Test state transition validation and constraints."""

    def test_add_slide_in_active_state_allowed(self):
        """Verify slides can be added directly in ACTIVE state (no DRAFT requirement)."""
        slides = Slides()
        
        # Add slide directly in ACTIVE state with content
        patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_001",
                "rank": 1,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Bento.Standard",
                "widgets": {
                    "cell_1": {"type": "Type.Display", "parameters": {"text": "Direct"}}
                },
                "parameters": {}
            })
        ])
        
        slides.patch(patch)
        
        # Should work - no enforcement of DRAFT-first workflow
        slide = slides.get("slide_001")
        assert slide.state == PatchableContextState.ACTIVE
        assert len(slide.widgets) == 1

    def test_replace_nonexistent_slide_raises_error(self):
        """Verify replacing non-existent slide raises PatchError."""
        slides = Slides()
        
        patch = Patch(operations=[
            ReplaceOperation(replace={
                "id": "nonexistent",
                "rank": 1,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Bento.Standard",
                "widgets": {},
                "parameters": {}
            })
        ])
        
        with pytest.raises(PatchError, match="not found"):
            slides.patch(patch)

    def test_state_change_preserves_other_fields(self):
        """Verify state change via replace preserves strategy and rank."""
        slides = Slides()
        
        # Add in DRAFT
        add_patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_001",
                "rank": 5,
                "state": PatchableContextState.DRAFT,
                "strategy": "Swiss.Asymmetry",
                "widgets": {},
                "parameters": {"special": "value"}
            })
        ])
        slides.patch(add_patch)
        
        # Replace to ACTIVE - must include all fields
        activate_patch = Patch(operations=[
            ReplaceOperation(replace={
                "id": "slide_001",
                "rank": 5,  # Same rank
                "state": PatchableContextState.ACTIVE,
                "strategy": "Swiss.Asymmetry",  # Same strategy
                "widgets": {"main": {"type": "Type.Heading", "parameters": {"text": "Title"}}},
                "parameters": {"special": "value"}  # Preserved
            })
        ])
        slides.patch(activate_patch)
        
        slide = slides.get("slide_001")
        assert slide.state == PatchableContextState.ACTIVE
        assert slide.rank == 5
        assert slide.strategy == "Swiss.Asymmetry"
        assert slide.parameters["special"] == "value"

    def test_empty_widgets_in_draft_allowed(self):
        """Verify DRAFT slides can have empty widgets dict."""
        slides = Slides()
        
        patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_001",
                "rank": 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Bento.Hero_Left",
                "widgets": {},  # Empty is fine for DRAFT
                "parameters": {}
            })
        ])
        
        slides.patch(patch)
        
        slide = slides.get("slide_001")
        assert slide.state == PatchableContextState.DRAFT
        assert slide.widgets == {}


class TestSlideStateQueryMethods:
    """Test Slides collection querying methods with different states."""

    def test_get_by_rank_includes_all_states(self):
        """Verify get_by_rank() returns slides in all states."""
        slides = Slides()
        
        patch = Patch(operations=[
            AddOperation(add={
                "id": "slide_draft",
                "rank": 1,
                "state": PatchableContextState.DRAFT,
                "strategy": "Bento.Standard",
                "widgets": {},
                "parameters": {}
            }),
            AddOperation(add={
                "id": "slide_active",
                "rank": 2,
                "state": PatchableContextState.ACTIVE,
                "strategy": "Swiss.Poster",
                "widgets": {"cell": {"type": "Type.Body", "parameters": {"text": "Hi"}}},
                "parameters": {}
            })
        ])
        slides.patch(patch)
        
        all_slides = slides.get_by_rank()
        assert len(all_slides) == 2
        assert all_slides[0].id == "slide_draft"
        assert all_slides[1].id == "slide_active"

    def test_count_includes_all_states(self):
        """Verify count() includes both DRAFT and ACTIVE slides."""
        slides = Slides()
        
        patch = Patch(operations=[
            AddOperation(add={
                "id": f"slide_{i:03d}",
                "rank": i + 1,
                "state": PatchableContextState.DRAFT if i % 2 == 0 else PatchableContextState.ACTIVE,
                "strategy": "Bento.Standard",
                "widgets": {} if i % 2 == 0 else {"cell": {"type": "Type.Body", "parameters": {"text": "X"}}},
                "parameters": {}
            })
            for i in range(4)
        ])
        slides.patch(patch)
        
        assert slides.count() == 4
        assert len(slides.get_active_slides()) == 2  # Only ACTIVE
