"""Integration tests verifying atoms can feed into layout generation."""
import pytest
import json
from src.common.source import Source, SourceReference
from src.common.patchable_context_pydantic import AddOperation, Patch
from src.generation.atom.models import StatementAtom, ProcessAtom, ComparisonAtom, ProcessStep
from src.generation.atom.collection import AtomCollection


@pytest.fixture
def sample_atom_collection():
    """Create a sample AtomCollection with mixed atom types."""
    collection = AtomCollection(id="test_atoms")
    
    atoms = [
        StatementAtom(
            id="stmt_001",
            rank=1,
            text="Machine learning requires large datasets.",
            related_to=[],
            contradicts=[],
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=0,
                length=42
            )
        ),
        ProcessAtom(
            id="proc_001",
            rank=2,
            title="ML Training Pipeline",
            steps=[
                ProcessStep(order=1, text="Collect data", dependencies=[]),
                ProcessStep(order=2, text="Clean data", dependencies=[1]),
                ProcessStep(order=3, text="Train model", dependencies=[2]),
                ProcessStep(order=4, text="Evaluate", dependencies=[3])
            ],
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=50,
                length=100
            )
        ),
        ComparisonAtom(
            id="comp_001",
            rank=3,
            dimensions=["accuracy", "speed", "complexity"],
            entities={
                "Linear Regression": {
                    "accuracy": "moderate",
                    "speed": "fast",
                    "complexity": "low"
                },
                "Neural Network": {
                    "accuracy": "high",
                    "speed": "slow",
                    "complexity": "high"
                }
            },
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=160,
                length=150
            )
        )
    ]
    
    operations = [AddOperation(add=atom) for atom in atoms]
    collection.patch(Patch(operations=operations))
    
    return collection


class TestAtomCollectionSerialization:
    """Test AtomCollection serialization for layout generation input."""
    
    def test_to_dict_produces_valid_structure(self, sample_atom_collection):
        """Verify to_dict produces expected structure for layout prompts."""
        data = sample_atom_collection.to_dict()
        
        # Verify top-level structure
        assert "id" in data
        assert "contexts" in data
        assert data["id"] == "test_atoms"
        assert isinstance(data["contexts"], list)
        assert len(data["contexts"]) == 3
    
    def test_to_json_produces_valid_json(self, sample_atom_collection):
        """Verify to_json produces parseable JSON string."""
        json_str = sample_atom_collection.to_json()
        
        # Should be valid JSON
        parsed = json.loads(json_str)
        
        assert "id" in parsed
        assert "contexts" in parsed
        assert len(parsed["contexts"]) == 3
    
    def test_serialized_atoms_preserve_type_info(self, sample_atom_collection):
        """Verify serialized atoms include type information."""
        data = sample_atom_collection.to_dict()
        
        types_found = set()
        for context in data["contexts"]:
            # Type info should be preserved via class name or discriminator
            if "text" in context and "related_to" in context:
                types_found.add("StatementAtom")
            elif "title" in context and "steps" in context:
                types_found.add("ProcessAtom")
            elif "dimensions" in context and "entities" in context:
                types_found.add("ComparisonAtom")
        
        assert len(types_found) == 3
    
    def test_serialized_format_matches_layout_input_expectations(self, sample_atom_collection):
        """Verify serialized format has all fields layout generation needs."""
        data = sample_atom_collection.to_dict()
        
        for context in data["contexts"]:
            # All atoms should have these base fields
            assert "id" in context
            assert "rank" in context
            assert "source_ref" in context
            
            # Source ref should have location info
            source_ref = context["source_ref"]
            assert "source_id" in source_ref
            assert "file_path" in source_ref
            assert "offset" in source_ref
            assert "length" in source_ref


class TestAtomRelationshipPreservation:
    """Test that atom relationships are preserved in serialization."""
    
    def test_statement_relationships_preserved(self):
        """Verify statement relationships survive serialization."""
        collection = AtomCollection(id="related_atoms")
        
        stmt1 = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Statement 1",
            source_ref=SourceReference(
                source_id="s", file_path="p", offset=0, length=1
            )
        )
        
        stmt2 = StatementAtom(
            id="stmt_002",
            rank=2,
            text="Statement 2 supports stmt_001",
            related_to=["stmt_001"],
            contradicts=[],
            source_ref=SourceReference(
                source_id="s", file_path="p", offset=10, length=1
            )
        )
        
        stmt3 = StatementAtom(
            id="stmt_003",
            rank=3,
            text="Statement 3 contradicts stmt_001",
            related_to=[],
            contradicts=["stmt_001"],
            source_ref=SourceReference(
                source_id="s", file_path="p", offset=20, length=1
            )
        )
        
        collection.patch(Patch(operations=[
            AddOperation(add=stmt1),
            AddOperation(add=stmt2),
            AddOperation(add=stmt3)
        ]))
        
        data = collection.to_dict()
        
        # Find stmt_002 and verify related_to
        stmt2_data = next(c for c in data["contexts"] if c["id"] == "stmt_002")
        assert "related_to" in stmt2_data
        assert "stmt_001" in stmt2_data["related_to"]
        
        # Find stmt_003 and verify contradicts
        stmt3_data = next(c for c in data["contexts"] if c["id"] == "stmt_003")
        assert "contradicts" in stmt3_data
        assert "stmt_001" in stmt3_data["contradicts"]
    
    def test_process_dependencies_preserved(self):
        """Verify process step dependencies survive serialization."""
        collection = AtomCollection(id="process_atoms")
        
        process = ProcessAtom(
            id="proc_001",
            rank=1,
            title="Complex Process",
            steps=[
                ProcessStep(order=1, text="Init", dependencies=[]),
                ProcessStep(order=2, text="Task A", dependencies=[1]),
                ProcessStep(order=3, text="Task B", dependencies=[1]),
                ProcessStep(order=4, text="Merge", dependencies=[2, 3])
            ],
            source_ref=SourceReference(
                source_id="s", file_path="p", offset=0, length=100
            )
        )
        
        collection.patch(Patch(operations=[AddOperation(add=process)]))
        
        data = collection.to_dict()
        proc_data = data["contexts"][0]
        
        # Verify all step dependencies preserved
        assert len(proc_data["steps"]) == 4
        assert proc_data["steps"][0]["dependencies"] == []
        assert proc_data["steps"][1]["dependencies"] == [1]
        assert proc_data["steps"][2]["dependencies"] == [1]
        assert proc_data["steps"][3]["dependencies"] == [2, 3]
    
    def test_comparison_structure_preserved(self):
        """Verify comparison entity-dimension mapping survives serialization."""
        collection = AtomCollection(id="comparison_atoms")
        
        comparison = ComparisonAtom(
            id="comp_001",
            rank=1,
            dimensions=["cost", "quality", "speed"],
            entities={
                "Option A": {"cost": "low", "quality": "high", "speed": "fast"},
                "Option B": {"cost": "high", "quality": "high", "speed": "slow"},
                "Option C": {"cost": "medium", "quality": "medium", "speed": "medium"}
            },
            source_ref=SourceReference(
                source_id="s", file_path="p", offset=0, length=100
            )
        )
        
        collection.patch(Patch(operations=[AddOperation(add=comparison)]))
        
        data = collection.to_dict()
        comp_data = data["contexts"][0]
        
        # Verify dimensions preserved
        assert set(comp_data["dimensions"]) == {"cost", "quality", "speed"}
        
        # Verify entity mappings preserved
        assert "Option A" in comp_data["entities"]
        assert comp_data["entities"]["Option A"]["cost"] == "low"
        assert comp_data["entities"]["Option B"]["quality"] == "high"
        assert comp_data["entities"]["Option C"]["speed"] == "medium"


class TestLayoutGenerationCompatibility:
    """Test that atom data format is compatible with layout generation."""
    
    def test_atoms_can_be_converted_to_layout_prompt_context(self, sample_atom_collection):
        """Verify atoms can be formatted as context for layout prompts."""
        json_str = sample_atom_collection.to_json()
        data = json.loads(json_str)
        
        # Simulate what layout generation would do: extract content for prompt
        content_summary = []
        for atom in data["contexts"]:
            if "text" in atom:
                content_summary.append(f"Statement: {atom['text']}")
            elif "title" in atom:
                content_summary.append(f"Process: {atom['title']} ({len(atom['steps'])} steps)")
            elif "dimensions" in atom:
                content_summary.append(f"Comparison: {len(atom['entities'])} entities across {len(atom['dimensions'])} dimensions")
        
        # Should have extracted meaningful content from all atoms
        assert len(content_summary) == 3
        assert any("Statement" in s for s in content_summary)
        assert any("Process" in s for s in content_summary)
        assert any("Comparison" in s for s in content_summary)
    
    def test_atom_metadata_available_for_layout_decisions(self, sample_atom_collection):
        """Verify atom metadata can inform layout generation decisions."""
        data = sample_atom_collection.to_dict()
        
        # Layout generation might use metadata for decisions
        for atom in data["contexts"]:
            # All atoms have rank for ordering
            assert "rank" in atom
            assert isinstance(atom["rank"], int)
            
            # All atoms have source_ref for traceability
            assert "source_ref" in atom
            
            # Metadata field available for LLM confidence, categories, etc.
            # (may be empty but should be accessible)
            if "metadata" in atom:
                assert isinstance(atom["metadata"], dict)
    
    def test_empty_collection_serializes_safely(self):
        """Verify empty collections don't break layout generation."""
        collection = AtomCollection(id="empty")
        
        data = collection.to_dict()
        json_str = collection.to_json()
        
        assert data["contexts"] == []
        parsed = json.loads(json_str)
        assert parsed["contexts"] == []
    
    def test_large_collection_serialization_performance(self):
        """Verify serialization works efficiently with many atoms."""
        collection = AtomCollection(id="large")
        
        # Create 100 atoms
        operations = []
        for i in range(100):
            atom = StatementAtom(
                id=f"stmt_{i:03d}",
                rank=i + 1,
                text=f"Statement number {i}",
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=i * 100, length=20
                )
            )
            operations.append(AddOperation(add=atom))
        
        collection.patch(Patch(operations=operations))
        
        # Should serialize without errors
        import time
        start = time.time()
        json_str = collection.to_json()
        elapsed = time.time() - start
        
        # Should be fast (< 1 second for 100 atoms)
        assert elapsed < 1.0
        
        # Should produce valid JSON
        data = json.loads(json_str)
        assert len(data["contexts"]) == 100
