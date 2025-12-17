"""Tests for AtomCollection class."""
import pytest
import json
from src.common.patchable_context_pydantic import (
    PatchableContextState,
    Patch,
    AddOperation,
    RemoveOperation,
    ReplaceOperation,
    PatchError
)
from src.common.source import SourceReference
from src.generation.atom.models import StatementAtom, ProcessAtom, ProcessStep, ComparisonAtom
from src.generation.atom.collection import AtomCollection


class TestAtomCollectionBasics:
    """Test basic AtomCollection operations."""
    
    def test_create_empty_collection(self):
        """Verify AtomCollection can be created empty."""
        collection = AtomCollection(id="test_collection")
        
        assert collection.id == "test_collection"
        assert len(collection) == 0
        assert collection.list_contexts() == []
    
    def test_collection_uses_atom_model_class(self):
        """Verify collection model_class is StatementAtom (base for all atoms)."""
        collection = AtomCollection(id="test")
        # Collection should accept any Atom subclass
        assert collection.model_class.__name__ in ["StatementAtom", "Atom"]


class TestAtomCollectionPatchOperations:
    """Test patch operations on AtomCollection."""
    
    def test_add_statement_atom(self):
        """Verify AddOperation adds StatementAtom to collection."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test statement",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/file.txt",
                offset=0,
                length=10
            )
        )
        
        patch = Patch(operations=[AddOperation(add=atom)])
        collection.patch(patch)
        
        assert len(collection) == 1
        retrieved = collection.get("stmt_001")
        assert retrieved is not None
        assert retrieved.text == "Test statement"
    
    def test_add_process_atom(self):
        """Verify AddOperation adds ProcessAtom to collection."""
        collection = AtomCollection(id="test")
        
        atom = ProcessAtom(
            id="proc_001",
            rank=1,
            title="Test Process",
            steps=[
                ProcessStep(order=1, text="Step 1"),
                ProcessStep(order=2, text="Step 2", dependencies=[1])
            ],
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/file.txt",
                offset=0,
                length=10
            )
        )
        
        patch = Patch(operations=[AddOperation(add=atom)])
        collection.patch(patch)
        
        assert len(collection) == 1
        retrieved = collection.get("proc_001")
        assert retrieved is not None
        assert retrieved.title == "Test Process"
    
    def test_add_comparison_atom(self):
        """Verify AddOperation adds ComparisonAtom to collection."""
        collection = AtomCollection(id="test")
        
        atom = ComparisonAtom(
            id="comp_001",
            rank=1,
            dimensions=["speed", "cost"],
            entities={
                "Option A": {"speed": "fast", "cost": "high"},
                "Option B": {"speed": "slow", "cost": "low"}
            },
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/file.txt",
                offset=0,
                length=10
            )
        )
        
        patch = Patch(operations=[AddOperation(add=atom)])
        collection.patch(patch)
        
        assert len(collection) == 1
        retrieved = collection.get("comp_001")
        assert retrieved is not None
        assert retrieved.dimensions == ["speed", "cost"]
    
    def test_add_duplicate_atom_raises_error(self):
        """Verify adding atom with existing ID raises PatchError."""
        collection = AtomCollection(id="test")
        
        atom1 = StatementAtom(
            id="stmt_001",
            rank=1,
            text="First",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        atom2 = StatementAtom(
            id="stmt_001",
            rank=2,
            text="Second",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=10, length=1
            )
        )
        
        collection.patch(Patch(operations=[AddOperation(add=atom1)]))
        
        with pytest.raises(PatchError, match="already exists"):
            collection.patch(Patch(operations=[AddOperation(add=atom2)]))
    
    def test_remove_atom(self):
        """Verify RemoveOperation removes atom from collection."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        collection.patch(Patch(operations=[AddOperation(add=atom)]))
        assert len(collection) == 1
        
        collection.patch(Patch(operations=[RemoveOperation(remove={"id": "stmt_001"})]))
        assert len(collection) == 0
        assert collection.get("stmt_001") is None
    
    def test_remove_nonexistent_atom_raises_error(self):
        """Verify removing non-existent atom raises PatchError."""
        collection = AtomCollection(id="test")
        
        with pytest.raises(PatchError, match="not found"):
            collection.patch(Patch(operations=[RemoveOperation(remove={"id": "nonexistent"})]))
    
    def test_replace_atom(self):
        """Verify ReplaceOperation replaces atom in collection."""
        collection = AtomCollection(id="test")
        
        original = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Original text",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        updated = StatementAtom(
            id="stmt_001",
            rank=2,
            text="Updated text",
            state=PatchableContextState.ACTIVE,
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        collection.patch(Patch(operations=[AddOperation(add=original)]))
        collection.patch(Patch(operations=[ReplaceOperation(replace=updated)]))
        
        retrieved = collection.get("stmt_001")
        assert retrieved.text == "Updated text"
        assert retrieved.rank == 2
        assert retrieved.state == PatchableContextState.ACTIVE
    
    def test_replace_nonexistent_atom_raises_error(self):
        """Verify replacing non-existent atom raises PatchError."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="nonexistent",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        with pytest.raises(PatchError, match="not found"):
            collection.patch(Patch(operations=[ReplaceOperation(replace=atom)]))
    
    def test_multiple_operations_in_patch(self):
        """Verify patch with multiple operations executes in sequence."""
        collection = AtomCollection(id="test")
        
        atom1 = StatementAtom(
            id="stmt_001", rank=1, text="First",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        atom2 = StatementAtom(
            id="stmt_002", rank=2, text="Second",
            source_ref=SourceReference(source_id="s", file_path="p", offset=10, length=1)
        )
        atom3 = StatementAtom(
            id="stmt_003", rank=3, text="Third",
            source_ref=SourceReference(source_id="s", file_path="p", offset=20, length=1)
        )
        
        # Add three atoms in one patch
        patch = Patch(operations=[
            AddOperation(add=atom1),
            AddOperation(add=atom2),
            AddOperation(add=atom3)
        ])
        collection.patch(patch)
        
        assert len(collection) == 3


class TestAtomCollectionFiltering:
    """Test filtering operations on AtomCollection."""
    
    def test_list_contexts_sorted_by_rank(self):
        """Verify list_contexts returns atoms sorted by rank."""
        collection = AtomCollection(id="test")
        
        # Add atoms in non-rank order
        atoms = [
            StatementAtom(
                id=f"stmt_{i}", rank=i, text=f"Text {i}",
                source_ref=SourceReference(source_id="s", file_path="p", offset=i*10, length=1)
            )
            for i in [3, 1, 4, 2, 5]
        ]
        
        for atom in atoms:
            collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        listed = collection.list_contexts()
        ranks = [atom.rank for atom in listed]
        assert ranks == [1, 2, 3, 4, 5]  # Sorted by rank
    
    def test_filter_by_state(self):
        """Verify list_contexts can filter by state."""
        collection = AtomCollection(id="test")
        
        draft_atom = StatementAtom(
            id="draft", rank=1, state=PatchableContextState.DRAFT, text="Draft",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        active_atom = StatementAtom(
            id="active", rank=2, state=PatchableContextState.ACTIVE, text="Active",
            source_ref=SourceReference(source_id="s", file_path="p", offset=10, length=1)
        )
        
        collection.patch(Patch(operations=[
            AddOperation(add=draft_atom),
            AddOperation(add=active_atom)
        ]))
        
        # Filter by ACTIVE state
        active_atoms = collection.list_contexts(state=PatchableContextState.ACTIVE)
        assert len(active_atoms) == 1
        assert active_atoms[0].id == "active"
        
        # Filter by DRAFT state
        draft_atoms = collection.list_contexts(state=PatchableContextState.DRAFT)
        assert len(draft_atoms) == 1
        assert draft_atoms[0].id == "draft"
    
    def test_get_by_source(self):
        """Verify get_by_source filters atoms by source_id."""
        collection = AtomCollection(id="test")
        
        atom1 = StatementAtom(
            id="atom1", rank=1, text="From source 1",
            source_ref=SourceReference(source_id="src_001", file_path="p", offset=0, length=1)
        )
        atom2 = StatementAtom(
            id="atom2", rank=2, text="From source 2",
            source_ref=SourceReference(source_id="src_002", file_path="p", offset=0, length=1)
        )
        atom3 = StatementAtom(
            id="atom3", rank=3, text="Also from source 1",
            source_ref=SourceReference(source_id="src_001", file_path="p", offset=10, length=1)
        )
        
        collection.patch(Patch(operations=[
            AddOperation(add=atom1),
            AddOperation(add=atom2),
            AddOperation(add=atom3)
        ]))
        
        src1_atoms = collection.get_by_source("src_001")
        assert len(src1_atoms) == 2
        assert {a.id for a in src1_atoms} == {"atom1", "atom3"}
        
        src2_atoms = collection.get_by_source("src_002")
        assert len(src2_atoms) == 1
        assert src2_atoms[0].id == "atom2"
    
    def test_get_by_type(self):
        """Verify get_by_type filters atoms by atom type."""
        collection = AtomCollection(id="test")
        
        stmt = StatementAtom(
            id="stmt", rank=1, text="Statement",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        proc = ProcessAtom(
            id="proc", rank=2, title="Process", steps=[ProcessStep(order=1, text="Step")],
            source_ref=SourceReference(source_id="s", file_path="p", offset=10, length=1)
        )
        comp = ComparisonAtom(
            id="comp", rank=3, dimensions=["d"], entities={"E": {"d": "v"}},
            source_ref=SourceReference(source_id="s", file_path="p", offset=20, length=1)
        )
        
        collection.patch(Patch(operations=[
            AddOperation(add=stmt),
            AddOperation(add=proc),
            AddOperation(add=comp)
        ]))
        
        statements = collection.get_by_type("StatementAtom")
        assert len(statements) == 1
        assert statements[0].id == "stmt"
        
        processes = collection.get_by_type("ProcessAtom")
        assert len(processes) == 1
        assert processes[0].id == "proc"
        
        comparisons = collection.get_by_type("ComparisonAtom")
        assert len(comparisons) == 1
        assert comparisons[0].id == "comp"


class TestAtomCollectionSerialization:
    """Test serialization methods."""
    
    def test_to_dict(self):
        """Verify to_dict serializes collection correctly."""
        collection = AtomCollection(id="test_collection")
        
        atom = StatementAtom(
            id="stmt_001", rank=1, text="Test",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        data = collection.to_dict()
        
        assert data["id"] == "test_collection"
        assert "contexts" in data
        assert len(data["contexts"]) == 1
        assert data["contexts"][0]["id"] == "stmt_001"
    
    def test_to_json(self):
        """Verify to_json produces valid JSON string."""
        collection = AtomCollection(id="test")
        
        atom = StatementAtom(
            id="stmt_001", rank=1, text="Test",
            source_ref=SourceReference(source_id="s", file_path="p", offset=0, length=1)
        )
        collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        json_str = collection.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["id"] == "test"
        assert len(parsed["contexts"]) == 1
