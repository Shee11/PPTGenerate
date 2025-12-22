"""Tests for Atom models - base class and subclasses."""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.common.patchable_context_pydantic import PatchableContextState
from src.common.source import SourceReference
from src.generation.atom.models import Atom, FactAtom, TensionAtom, ConceptAtom, VisualAtom


class TestAtomBase:
    """Test Atom base class inheriting from PatchableContextBase."""
    
    def test_atom_has_required_patchable_fields(self):
        """Verify Atom includes id, rank, state from PatchableContextBase."""
        atom = FactAtom(
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
        FactAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        # Invalid without source_ref
        with pytest.raises(ValidationError):
            FactAtom(
                id="atom_001",
                rank=1,
                text="Test"
            )
    
    def test_atom_created_at_auto_generated(self):
        """Verify created_at is automatically set."""
        before = datetime.utcnow()
        
        atom = FactAtom(
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
        atom = FactAtom(
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
        
        atom = FactAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            ),
            metadata=metadata
        )
        
        assert atom.metadata == metadata
    
    def test_atom_visual_field(self):
        """Verify visual field exists with default 'none'."""
        atom = FactAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.visual == "none"
    
    def test_atom_visual_field_with_value(self):
        """Verify visual field can be set."""
        atom = FactAtom(
            id="atom_001",
            rank=1,
            text="Test",
            visual="chart",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.visual == "chart"


class TestFactAtom:
    """Test FactAtom for objective information."""
    
    def test_valid_fact_atom(self):
        """Verify valid FactAtom with all fields."""
        atom = FactAtom(
            id="fact_001",
            rank=1,
            state=PatchableContextState.ACTIVE,
            text="System handles 1M requests per second.",
            category="data",
            visual="chart",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/metrics.txt",
                offset=150,
                length=45,
                line_number=10
            )
        )
        
        assert atom.text == "System handles 1M requests per second."
        assert atom.category == "data"
        assert atom.visual == "chart"
    
    def test_fact_requires_text(self):
        """Verify text field is required and non-empty."""
        # Valid with text
        FactAtom(
            id="atom_001",
            rank=1,
            text="Valid text",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        # Invalid without text
        with pytest.raises(ValidationError):
            FactAtom(
                id="atom_001",
                rank=1,
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
        
        # Invalid with empty text
        with pytest.raises(ValidationError):
            FactAtom(
                id="atom_001",
                rank=1,
                text="",
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
    
    def test_fact_category_default(self):
        """Verify category defaults to 'other'."""
        atom = FactAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.category == "other"
    
    def test_fact_category_values(self):
        """Verify category accepts valid values."""
        for category in ["data", "definition", "architecture", "status", "other"]:
            atom = FactAtom(
                id="atom_001",
                rank=1,
                text="Test",
                category=category,
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
            assert atom.category == category


class TestTensionAtom:
    """Test TensionAtom for conflicts and problems."""
    
    def test_valid_tension_atom(self):
        """Verify valid TensionAtom with all fields."""
        atom = TensionAtom(
            id="tension_001",
            rank=1,
            text="But latency spiked to 2 seconds under load.",
            tension_type="problem",
            resolution_hint="Solved by caching",
            visual="before-after",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/issues.txt",
                offset=200,
                length=50
            )
        )
        
        assert atom.text == "But latency spiked to 2 seconds under load."
        assert atom.tension_type == "problem"
        assert atom.resolution_hint == "Solved by caching"
    
    def test_tension_type_default(self):
        """Verify tension_type defaults to 'problem'."""
        atom = TensionAtom(
            id="atom_001",
            rank=1,
            text="Test tension",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.tension_type == "problem"
    
    def test_tension_type_values(self):
        """Verify tension_type accepts valid values."""
        for tension_type in ["problem", "contradiction", "trade-off", "surprise", "mistake", "other"]:
            atom = TensionAtom(
                id="atom_001",
                rank=1,
                text="Test",
                tension_type=tension_type,
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
            assert atom.tension_type == tension_type
    
    def test_tension_resolution_hint_default(self):
        """Verify resolution_hint defaults to empty string."""
        atom = TensionAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.resolution_hint == ""


class TestConceptAtom:
    """Test ConceptAtom for solutions and insights."""
    
    def test_valid_concept_atom(self):
        """Verify valid ConceptAtom with all fields."""
        atom = ConceptAtom(
            id="concept_001",
            rank=1,
            text="Solution: Cache at the edge for sub-100ms latency.",
            concept_type="solution",
            supporting_facts=["fact_001", "fact_002"],
            visual="diagram",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/solution.txt",
                offset=300,
                length=60
            )
        )
        
        assert atom.text == "Solution: Cache at the edge for sub-100ms latency."
        assert atom.concept_type == "solution"
        assert atom.supporting_facts == ["fact_001", "fact_002"]
    
    def test_concept_type_default(self):
        """Verify concept_type defaults to 'insight'."""
        atom = ConceptAtom(
            id="atom_001",
            rank=1,
            text="Test concept",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.concept_type == "insight"
    
    def test_concept_type_values(self):
        """Verify concept_type accepts valid values."""
        for concept_type in ["solution", "insight", "method", "principle", "takeaway", "other"]:
            atom = ConceptAtom(
                id="atom_001",
                rank=1,
                text="Test",
                concept_type=concept_type,
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
            assert atom.concept_type == concept_type
    
    def test_concept_supporting_facts_default(self):
        """Verify supporting_facts defaults to empty list."""
        atom = ConceptAtom(
            id="atom_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.supporting_facts == []


class TestVisualAtom:
    """Test VisualAtom for concrete imagery."""
    
    def test_valid_visual_atom(self):
        """Verify valid VisualAtom with all fields."""
        atom = VisualAtom(
            id="visual_001",
            rank=1,
            description="Screen filled with red error messages",
            visual_category="screenshot",
            related_atom="tension_001",
            visual="screenshot",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/docs/story.txt",
                offset=400,
                length=40
            )
        )
        
        assert atom.description == "Screen filled with red error messages"
        assert atom.visual_category == "screenshot"
        assert atom.related_atom == "tension_001"
    
    def test_visual_category_default(self):
        """Verify visual_category defaults to 'other'."""
        atom = VisualAtom(
            id="atom_001",
            rank=1,
            description="Test visual",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.visual_category == "other"
    
    def test_visual_category_values(self):
        """Verify visual_category accepts valid values."""
        for category in ["metaphor", "demo", "screenshot", "diagram", "comparison", "other"]:
            atom = VisualAtom(
                id="atom_001",
                rank=1,
                description="Test",
                visual_category=category,
                source_ref=SourceReference(
                    source_id="src", file_path="path", offset=0, length=1
                )
            )
            assert atom.visual_category == category
    
    def test_visual_related_atom_default(self):
        """Verify related_atom defaults to empty string."""
        atom = VisualAtom(
            id="atom_001",
            rank=1,
            description="Test",
            source_ref=SourceReference(
                source_id="src", file_path="path", offset=0, length=1
            )
        )
        
        assert atom.related_atom == ""
