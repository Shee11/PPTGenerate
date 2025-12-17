"""Tests for Atom models - base class and subclasses."""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.common.patchable_context_pydantic import PatchableContextState
from src.common.source import SourceReference
from src.generation.atom.models import Atom, StatementAtom, ProcessAtom, ComparisonAtom, ProcessStep


class TestAtomBase:
    """Test Atom base class inheriting from PatchableContextBase."""
    
    def test_atom_has_required_patchable_fields(self):
        """Verify Atom includes id, rank, state from PatchableContextBase."""
        atom = StatementAtom(
            id="atom_001",
            rank=1,
            state=PatchableContextState.DRAFT,
            text="Test statement",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/file.txt",
                offset=0,
                length=10
            )
        )
        
        assert atom.id == "atom_001"
        assert atom.rank == 1
        assert atom.state == PatchableContextState.DRAFT
    
    def test_atom_requires_source_reference(self):
        """Verify all atoms must have source_ref."""
        # Valid with source_ref
        StatementAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        # Invalid without source_ref
        with pytest.raises(ValidationError):
            StatementAtom(
                id="atom_001",
                rank=1,
                text="Test"
            )
    
    def test_atom_created_at_auto_generated(self):
        """Verify created_at is automatically set."""
        before = datetime.utcnow()
        
        atom = StatementAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        after = datetime.utcnow()
        assert before <= atom.created_at <= after
    
    def test_atom_metadata_optional(self):
        """Verify metadata is optional with default empty dict."""
        atom = StatementAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.metadata == {}
    
    def test_atom_metadata_stores_llm_info(self):
        """Verify metadata can store LLM generation details."""
        metadata = {
            "model": "gpt-4-turbo",
            "temperature": 0.2,
            "prompt_version": "v1.0"
        }
        
        atom = StatementAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            ),
            metadata=metadata
        )
        
        assert atom.metadata == metadata


class TestStatementAtom:
    """Test StatementAtom for pure text statements."""
    
    def test_valid_statement_atom(self):
        """Verify valid StatementAtom with all fields."""
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            state=PatchableContextState.ACTIVE,
            text="Machine learning improves with more data.",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/ml.txt",
                offset=150,
                length=45,
                line_number=10
            ),
            related_to=["stmt_002", "stmt_003"],
            contradicts=["stmt_004"]
        )
        
        assert atom.text == "Machine learning improves with more data."
        assert atom.related_to == ["stmt_002", "stmt_003"]
        assert atom.contradicts == ["stmt_004"]
    
    def test_statement_requires_text(self):
        """Verify text field is required and non-empty."""
        # Valid with text
        StatementAtom(
            id="atom_001",
            rank=1,
            text="Valid text",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        # Invalid without text
        with pytest.raises(ValidationError):
            StatementAtom(
                id="atom_001",
                rank=1,
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
        
        # Invalid with empty text
        with pytest.raises(ValidationError):
            StatementAtom(
                id="atom_001",
                rank=1,
                text="",
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
    
    def test_statement_relationships_default_empty(self):
        """Verify related_to and contradicts default to empty lists."""
        atom = StatementAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.related_to == []
        assert atom.contradicts == []


class TestProcessStep:
    """Test ProcessStep nested model."""
    
    def test_valid_process_step(self):
        """Verify valid ProcessStep with all fields."""
        step = ProcessStep(
            order=1,
            text="Initialize the system",
            dependencies=[]
        )
        
        assert step.order == 1
        assert step.text == "Initialize the system"
        assert step.dependencies == []
    
    def test_process_step_with_dependencies(self):
        """Verify ProcessStep can reference dependent steps."""
        step = ProcessStep(
            order=3,
            text="Execute main process",
            dependencies=[1, 2]
        )
        
        assert step.dependencies == [1, 2]
    
    def test_process_step_order_positive(self):
        """Verify order must be positive (1-indexed)."""
        # Valid order
        ProcessStep(order=1, text="Step 1")
        
        # Invalid order (zero)
        with pytest.raises(ValidationError):
            ProcessStep(order=0, text="Step 0")
        
        # Invalid order (negative)
        with pytest.raises(ValidationError):
            ProcessStep(order=-1, text="Step -1")
    
    def test_process_step_dependencies_default_empty(self):
        """Verify dependencies defaults to empty list."""
        step = ProcessStep(order=1, text="Step 1")
        assert step.dependencies == []


class TestProcessAtom:
    """Test ProcessAtom for process descriptions."""
    
    def test_valid_process_atom(self):
        """Verify valid ProcessAtom with steps and dependencies."""
        atom = ProcessAtom(
            id="proc_001",
            rank=1,
            title="Software Installation Process",
            steps=[
                ProcessStep(order=1, text="Download installer", dependencies=[]),
                ProcessStep(order=2, text="Run installer", dependencies=[1]),
                ProcessStep(order=3, text="Configure settings", dependencies=[2]),
                ProcessStep(order=4, text="Verify installation", dependencies=[3])
            ],
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/install.txt",
                offset=200,
                length=150
            )
        )
        
        assert atom.title == "Software Installation Process"
        assert len(atom.steps) == 4
        assert atom.steps[1].dependencies == [1]
        assert atom.steps[3].dependencies == [3]
    
    def test_process_requires_title_and_steps(self):
        """Verify title and steps are required."""
        source_ref = SourceReference(
            source_id="src", file_path="path", offset=0, length=1
        )
        
        # Invalid without title
        with pytest.raises(ValidationError):
            ProcessAtom(
                id="proc_001",
                rank=1,
                steps=[ProcessStep(order=1, text="Step 1")],
                source_ref=source_ref
            )
        
        # Invalid without steps
        with pytest.raises(ValidationError):
            ProcessAtom(
                id="proc_001",
                rank=1,
                title="Process",
                source_ref=source_ref
            )
        
        # Invalid with empty steps
        with pytest.raises(ValidationError):
            ProcessAtom(
                id="proc_001",
                rank=1,
                title="Process",
                steps=[],
                source_ref=source_ref
            )
    
    def test_process_steps_ordered_sequence(self):
        """Verify steps maintain their order."""
        atom = ProcessAtom(
            id="proc_001",
            rank=1,
            title="Test Process",
            steps=[
                ProcessStep(order=1, text="First"),
                ProcessStep(order=2, text="Second"),
                ProcessStep(order=3, text="Third")
            ],
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.steps[0].order == 1
        assert atom.steps[1].order == 2
        assert atom.steps[2].order == 3


class TestComparisonAtom:
    """Test ComparisonAtom for comparison tables."""
    
    def test_valid_comparison_atom(self):
        """Verify valid ComparisonAtom with dimensions and entities."""
        atom = ComparisonAtom(
            id="comp_001",
            rank=1,
            dimensions=["speed", "accuracy", "cost"],
            entities={
                "Method A": {
                    "speed": "fast",
                    "accuracy": "high",
                    "cost": "expensive"
                },
                "Method B": {
                    "speed": "slow",
                    "accuracy": "very high",
                    "cost": "cheap"
                }
            },
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/comparison.txt",
                offset=300,
                length=200
            )
        )
        
        assert atom.dimensions == ["speed", "accuracy", "cost"]
        assert "Method A" in atom.entities
        assert atom.entities["Method A"]["speed"] == "fast"
    
    def test_comparison_requires_dimensions_and_entities(self):
        """Verify dimensions and entities are required."""
        source_ref = SourceReference(
            source_id="src", file_path="path", offset=0, length=1
        )
        
        # Invalid without dimensions
        with pytest.raises(ValidationError):
            ComparisonAtom(
                id="comp_001",
                rank=1,
                entities={"A": {"dim": "val"}},
                source_ref=source_ref
            )
        
        # Invalid without entities
        with pytest.raises(ValidationError):
            ComparisonAtom(
                id="comp_001",
                rank=1,
                dimensions=["dim"],
                source_ref=source_ref
            )
        
        # Invalid with empty dimensions
        with pytest.raises(ValidationError):
            ComparisonAtom(
                id="comp_001",
                rank=1,
                dimensions=[],
                entities={"A": {"dim": "val"}},
                source_ref=source_ref
            )
    
    def test_comparison_entities_structure(self):
        """Verify entities use dict[str, dict[str, str]] structure."""
        atom = ComparisonAtom(
            id="comp_001",
            rank=1,
            dimensions=["feature1", "feature2"],
            entities={
                "Product X": {"feature1": "excellent", "feature2": "good"},
                "Product Y": {"feature1": "good", "feature2": "excellent"}
            },
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert isinstance(atom.entities, dict)
        assert isinstance(atom.entities["Product X"], dict)
        assert isinstance(atom.entities["Product X"]["feature1"], str)
