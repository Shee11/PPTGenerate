"""Integration tests for PatchableCollection with atoms."""
import pytest
from src.common.patchable_context_pydantic import (
    PatchableContextState,
    AddOperation,
    RemoveOperation,
    ReplaceOperation,
    Patch,
    PatchError
)
from src.common.source import SourceReference
from src.generation.atom.models import StatementAtom, ProcessAtom, ProcessStep
from src.generation.atom.collection import AtomCollection


class TestAtomCollectionPatchOperations:
    """Test patch operations work correctly with AtomCollection."""
    
    def test_add_operation_adds_atom(self):
        """Verify AddOperation successfully adds atom to collection."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test statement",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=14
            )
        )
        
        patch = Patch(operations=[AddOperation(add=atom)])
        result = collection.patch(patch)
        
        # Patch should return self for chaining
        assert result is collection
        
        # Atom should be in collection
        assert len(collection) == 1
        retrieved = collection.get("stmt_001")
        assert retrieved is not None
        assert retrieved.text == "Test statement"
    
    def test_add_duplicate_id_raises_error(self):
        """Verify adding duplicate ID raises PatchError."""
        collection = AtomCollection(id="test")
        
        atom1 = StatementAtom(
            id="stmt_001", rank=1, text="First",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        atom2 = StatementAtom(
            id="stmt_001", rank=2, text="Duplicate",
            source_ref=SourceReference(source_id="s", file_path="p", offset=10, length=1)
        )
        
        collection.patch(Patch(operations=[AddOperation(add=atom1)]))
        
        with pytest.raises(PatchError, match="already exists"):
            collection.patch(Patch(operations=[AddOperation(add=atom2)]))
    
    def test_remove_operation_removes_atom(self):
        """Verify RemoveOperation successfully removes atom from collection."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="stmt_001", rank=1, text="To be removed",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        
        collection.patch(Patch(operations=[AddOperation(add=atom)]))
        assert len(collection) == 1
        
        collection.patch(Patch(operations=[RemoveOperation(remove={"id": "stmt_001"})]))
        
        assert len(collection) == 0
        assert collection.get("stmt_001") is None
    
    def test_remove_nonexistent_id_raises_error(self):
        """Verify removing nonexistent ID raises PatchError."""
        collection = AtomCollection(id="test")
        
        with pytest.raises(PatchError, match="not found"):
            collection.patch(Patch(operations=[RemoveOperation(remove={"id": "nonexistent"})]))
    
    def test_replace_operation_replaces_atom(self):
        """Verify ReplaceOperation successfully replaces atom in collection."""
        collection = AtomCollection(id="test")
        
        original = StatementAtom(
            id="stmt_001", rank=1, text="Original",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        
        updated = StatementAtom(
            id="stmt_001", rank=2, text="Updated", state=PatchableContextState.ACTIVE,
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        
        collection.patch(Patch(operations=[AddOperation(add=original)]))
        collection.patch(Patch(operations=[ReplaceOperation(replace=updated)]))
        
        retrieved = collection.get("stmt_001")
        assert retrieved.text == "Updated"
        assert retrieved.rank == 2
        assert retrieved.state == PatchableContextState.ACTIVE
    
    def test_replace_nonexistent_id_raises_error(self):
        """Verify replacing nonexistent ID raises PatchError."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="nonexistent", rank=1, text="Test",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        
        with pytest.raises(PatchError, match="not found"):
            collection.patch(Patch(operations=[ReplaceOperation(replace=atom)]))


class TestSequentialPatchApplication:
    """Test sequential patch application maintains collection state correctly."""
    
    def test_multiple_operations_in_single_patch(self):
        """Verify multiple operations in one patch execute in sequence."""
        collection = AtomCollection(id="test")
        
        atoms = [
            StatementAtom(
                id=f"stmt_{i:03d}", rank=i, text=f"Statement {i}",
                source_ref=SourceReference(source_id="s", file_path="p", offset=i*10, length=10)
            )
            for i in range(1, 6)
        ]
        
        operations = [AddOperation(add=atom) for atom in atoms]
        collection.patch(Patch(operations=operations))
        
        assert len(collection) == 5
        for i in range(1, 6):
            assert collection.get(f"stmt_{i:03d}") is not None
    
    def test_sequential_patches_maintain_state(self):
        """Verify applying patches sequentially maintains correct state."""
        collection = AtomCollection(id="test")
        
        # Patch 1: Add 3 atoms
        patch1 = Patch(operations=[
            AddOperation(add=StatementAtom(
                id=f"stmt_{i}", rank=i, text=f"Stmt {i}",
                source_ref=SourceReference(source_id="s", file_path="p", offset=i, length=1)
            ))
            for i in range(1, 4)
        ])
        collection.patch(patch1)
        assert len(collection) == 3
        
        # Patch 2: Remove one, add one
        patch2 = Patch(operations=[
            RemoveOperation(remove={"id": "stmt_2"}),
            AddOperation(add=StatementAtom(
                id="stmt_4", rank=4, text="Stmt 4",
                source_ref=SourceReference(source_id="s", file_path="p", offset=4, length=1)
            ))
        ])
        collection.patch(patch2)
        assert len(collection) == 3
        assert collection.get("stmt_2") is None
        assert collection.get("stmt_4") is not None
        
        # Patch 3: Replace one
        patch3 = Patch(operations=[
            ReplaceOperation(replace=StatementAtom(
                id="stmt_1", rank=10, text="Updated Stmt 1",
                source_ref=SourceReference(source_id="s", file_path="p", offset=1, length=1)
            ))
        ])
        collection.patch(patch3)
        updated = collection.get("stmt_1")
        assert updated.text == "Updated Stmt 1"
        assert updated.rank == 10
    
    def test_complex_workflow_scenario(self):
        """Verify complex workflow with mixed operations."""
        collection = AtomCollection(id="workflow")
        
        # Initial state: 5 atoms
        for i in range(1, 6):
            collection.patch(Patch(operations=[
                AddOperation(add=StatementAtom(
                    id=f"stmt_{i}", rank=i, text=f"Initial {i}",
                    source_ref=SourceReference(source_id="s", file_path="p", offset=i, length=1)
                ))
            ]))
        
        # Update workflow: remove 2, update 1, add 2
        workflow_patch = Patch(operations=[
            RemoveOperation(remove={"id": "stmt_2"}),
            RemoveOperation(remove={"id": "stmt_4"}),
            ReplaceOperation(replace=StatementAtom(
                id="stmt_3", rank=30, text="Updated 3",
                source_ref=SourceReference(source_id="s", file_path="p", offset=3, length=1)
            )),
            AddOperation(add=StatementAtom(
                id="stmt_6", rank=6, text="New 6",
                source_ref=SourceReference(source_id="s", file_path="p", offset=6, length=1)
            )),
            AddOperation(add=StatementAtom(
                id="stmt_7", rank=7, text="New 7",
                source_ref=SourceReference(source_id="s", file_path="p", offset=7, length=1)
            ))
        ])
        
        collection.patch(workflow_patch)
        
        # Verify final state
        assert len(collection) == 5  # 5 - 2 + 2 = 5
        assert collection.get("stmt_1") is not None
        assert collection.get("stmt_2") is None  # Removed
        assert collection.get("stmt_3").text == "Updated 3"
        assert collection.get("stmt_4") is None  # Removed
        assert collection.get("stmt_5") is not None
        assert collection.get("stmt_6") is not None
        assert collection.get("stmt_7") is not None


class TestPatchValidation:
    """Test patch validation catches invalid operations."""
    
    def test_add_with_invalid_source_ref_fails(self):
        """Verify adding atom with invalid source_ref fails validation."""
        collection = AtomCollection(id="test")
        
        # Source ref with negative offset should fail
        with pytest.raises(Exception):  # Pydantic validation error
            atom = StatementAtom(
                id="bad", rank=1, text="Bad",
                source_ref=SourceReference(
                    source_id="s", file_path="p", offset=-1, length=1
                )
            )
            collection.patch(Patch(operations=[AddOperation(add=atom)]))
    
    def test_remove_with_missing_id_field_fails(self):
        """Verify remove operation requires 'id' field."""
        collection = AtomCollection(id="test")
        
        # RemoveOperation expects {"id": "..."}
        with pytest.raises((KeyError, PatchError)):
            collection.patch(Patch(operations=[RemoveOperation(remove={})]))
    
    def test_patch_operations_preserve_referential_integrity(self):
        """Verify patch operations don't break atom relationships."""
        collection = AtomCollection(id="test")
        
        # Add atoms with relationships
        stmt1 = StatementAtom(
            id="stmt_1", rank=1, text="Base statement",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        stmt2 = StatementAtom(
            id="stmt_2", rank=2, text="Related statement",
            related_to=["stmt_1"],
            source_ref=SourceReference(source_id="s", file_path="p", offset=10, length=1)
        )
        
        collection.patch(Patch(operations=[
            AddOperation(add=stmt1),
            AddOperation(add=stmt2)
        ]))
        
        # Verify relationship preserved
        retrieved_stmt2 = collection.get("stmt_2")
        assert "stmt_1" in retrieved_stmt2.related_to
        
        # Remove stmt_1 - stmt_2's reference becomes orphaned
        # (Note: Collection doesn't enforce referential integrity,
        # that's a higher-level concern for layout generation)
        collection.patch(Patch(operations=[
            RemoveOperation(remove={"id": "stmt_1"})
        ]))
        
        # stmt_2 still exists with orphaned reference
        retrieved_stmt2 = collection.get("stmt_2")
        assert retrieved_stmt2 is not None
        assert "stmt_1" in retrieved_stmt2.related_to  # Orphaned reference


class TestPatchWithDifferentAtomTypes:
    """Test patches work correctly with mixed atom types."""
    
    def test_mixed_atom_types_in_single_patch(self):
        """Verify single patch can add different atom types."""
        collection = AtomCollection(id="mixed")
        
        stmt = StatementAtom(
            id="stmt", rank=1, text="Statement",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        proc = ProcessAtom(
            id="proc", rank=2, title="Process",
            steps=[ProcessStep(order=1, text="Step")],
            source_ref=SourceReference(source_id="s", file_path="p", offset=10, length=1)
        )
        
        patch = Patch(operations=[
            AddOperation(add=stmt),
            AddOperation(add=proc)
        ])
        collection.patch(patch)
        
        assert len(collection) == 2
        assert isinstance(collection.get("stmt"), StatementAtom)
        assert isinstance(collection.get("proc"), ProcessAtom)
    
    def test_replace_preserves_atom_type(self):
        """Verify replace works correctly when keeping same atom type."""
        collection = AtomCollection(id="test")
        
        # Add statement
        stmt = StatementAtom(
            id="atom_001", rank=1, text="Original statement",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        collection.patch(Patch(operations=[AddOperation(add=stmt)]))
        
        # Replace with updated statement (same ID, same type)
        updated_stmt = StatementAtom(
            id="atom_001", rank=2, text="Updated statement",
            related_to=["atom_002"],
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=17)
        )
        collection.patch(Patch(operations=[ReplaceOperation(replace=updated_stmt)]))
        
        # Should have updated fields
        retrieved = collection.get("atom_001")
        assert isinstance(retrieved, StatementAtom)
        assert retrieved.text == "Updated statement"
        assert retrieved.rank == 2
        assert retrieved.related_to == ["atom_002"]
