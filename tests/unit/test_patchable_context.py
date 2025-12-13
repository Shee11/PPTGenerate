"""Unit tests for PatchableContextPydantic.patch() method."""
import pytest
from pydantic import BaseModel, Field
from src.common.patchable_context_pydantic import PatchableContextBase, PatchError


class TestPatchableContextPatching:
    """Test the patch() method on PatchableContext collections."""
    
    def test_patch_updates_existing_field(self):
        """Test patching an existing field."""
        # Create a context
        context = PatchableContextBase(id="test-1", rank=1)
        
        # Patch the rank field
        updated = context.model_copy(update={"rank": 2})
        
        assert updated.id == "test-1"
        assert updated.rank == 2
        assert context.rank == 1  # Original unchanged
    
    def test_patch_multiple_fields(self):
        """Test patching multiple fields at once."""
        context = PatchableContextBase(id="test-1", rank=1, state="draft")
        
        updated = context.model_copy(update={"rank": 5, "state": "active"})
        
        assert updated.rank == 5
        assert updated.state == "active"
    
    def test_patch_preserves_unmodified_fields(self):
        """Test that patching doesn't affect unmodified fields."""
        context = PatchableContextBase(id="original-id", rank=1, state="draft")
        
        updated = context.model_copy(update={"rank": 10})
        
        assert updated.id == "original-id"
        assert updated.state == "draft"
        assert updated.rank == 10
    
    def test_patch_validates_new_values(self):
        """Test that patching validates the new values."""
        from pydantic import ValidationError
        context = PatchableContextBase(id="test-1", rank=1)
        
        # rank must be >= 0
        with pytest.raises(ValidationError):  # Pydantic validation error
            PatchableContextBase(id="test-1", rank=-1)
    
    def test_patch_rejects_invalid_types(self):
        """Test that patching rejects invalid types."""
        from pydantic import ValidationError
        context = PatchableContextBase(id="test-1", rank=1)
        
        with pytest.raises(ValidationError):  # Pydantic validation error
            PatchableContextBase(id="test-1", rank="not-a-number")
    
    def test_patch_on_subclass_with_custom_fields(self):
        """Test patching works on subclasses with additional fields."""
        
        class CustomContext(PatchableContextBase):
            """Custom context with extra field."""
            title: str = Field(default="Untitled")
            description: str = Field(default="")
        
        context = CustomContext(
            id="custom-1",
            rank=1,
            title="Original Title",
            description="Original description"
        )
        
        updated = context.model_copy(update={
            "title": "Updated Title",
            "rank": 99
        })
        
        assert updated.title == "Updated Title"
        assert updated.rank == 99
        assert updated.description == "Original description"
        assert updated.id == "custom-1"
