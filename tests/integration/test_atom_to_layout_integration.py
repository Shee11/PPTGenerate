"""Integration tests verifying atoms can feed into layout generation.

Tests the new narrative atom types integration with layout:
- FactAtom → Anchor slides
- TensionAtom → Friction slides
- ConceptAtom → Insight slides
- VisualAtom → Visual concepts for slide design
"""
import pytest
import json
from src.common.source import Source, SourceReference
from src.common.patchable_context_pydantic import AddOperation, Patch
from src.generation.atom.models import FactAtom, TensionAtom, ConceptAtom, VisualAtom
from src.generation.atom.collection import AtomCollection


@pytest.fixture
def sample_atom_collection():
    """Create a sample AtomCollection with all four atom types."""
    collection = AtomCollection(id="test_atoms")
    
    atoms = [
        FactAtom(
            id="fact_001",
            rank=1,
            text="System processes 1M requests per second",
            category="data",
            visual="chart",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=0,
                length=42
            )
        ),
        TensionAtom(
            id="tension_001",
            rank=2,
            text="Legacy systems couldn't scale to meet demand",
            tension_type="problem",
            visual="before-after",
            resolution_hint="Microservices solved the issue",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=50,
                length=50
            )
        ),
        ConceptAtom(
            id="concept_001",
            rank=3,
            text="Microservices enabled independent scaling",
            concept_type="solution",
            visual="architecture",
            supporting_facts=["fact_001"],
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=110,
                length=45
            )
        ),
        VisualAtom(
            id="visual_001",
            rank=4,
            description="Dashboard showing green health checks",
            visual_category="screenshot",
            visual="screenshot",
            related_atom="concept_001",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/path/to/source.txt",
                offset=160,
                length=40
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
        assert len(data["contexts"]) == 4
    
    def test_to_json_produces_valid_json(self, sample_atom_collection):
        """Verify to_json produces parseable JSON string."""
        json_str = sample_atom_collection.to_json()
        
        # Should be valid JSON
        parsed = json.loads(json_str)
        
        assert "id" in parsed
        assert "contexts" in parsed
        assert len(parsed["contexts"]) == 4
    
    def test_atom_types_preserved_in_serialization(self, sample_atom_collection):
        """Verify atom types are distinguishable in serialized output."""
        data = sample_atom_collection.to_dict()
        
        # Each atom should have identifying fields
        atom_ids = {ctx["id"] for ctx in data["contexts"]}
        assert "fact_001" in atom_ids
        assert "tension_001" in atom_ids
        assert "concept_001" in atom_ids
        assert "visual_001" in atom_ids


class TestAtomTypesForLayoutPrompt:
    """Test that atom types contain fields needed for layout generation."""
    
    def test_fact_atom_has_layout_fields(self, sample_atom_collection):
        """Verify FactAtom has fields needed for Anchor slides."""
        fact = sample_atom_collection.get("fact_001")
        
        assert hasattr(fact, "text")
        assert hasattr(fact, "category")
        assert hasattr(fact, "visual")
        assert fact.text is not None
        assert fact.category in ["data", "definition", "architecture", "status", "other"]
    
    def test_tension_atom_has_layout_fields(self, sample_atom_collection):
        """Verify TensionAtom has fields needed for Friction slides."""
        tension = sample_atom_collection.get("tension_001")
        
        assert hasattr(tension, "text")
        assert hasattr(tension, "tension_type")
        assert hasattr(tension, "visual")
        assert hasattr(tension, "resolution_hint")
        assert tension.tension_type in ["problem", "contradiction", "trade-off", "surprise", "mistake", "other"]
    
    def test_concept_atom_has_layout_fields(self, sample_atom_collection):
        """Verify ConceptAtom has fields needed for Insight slides."""
        concept = sample_atom_collection.get("concept_001")
        
        assert hasattr(concept, "text")
        assert hasattr(concept, "concept_type")
        assert hasattr(concept, "visual")
        assert hasattr(concept, "supporting_facts")
        assert concept.concept_type in ["solution", "insight", "method", "principle", "takeaway", "other"]
    
    def test_visual_atom_has_layout_fields(self, sample_atom_collection):
        """Verify VisualAtom has fields for slide visual concepts."""
        visual = sample_atom_collection.get("visual_001")
        
        assert hasattr(visual, "description")
        assert hasattr(visual, "visual_category")
        assert hasattr(visual, "visual")
        assert hasattr(visual, "related_atom")


class TestNarrativeArcConstruction:
    """Test that atoms can construct a narrative arc for presentation."""
    
    def test_atoms_ordered_by_rank(self, sample_atom_collection):
        """Verify atoms maintain narrative order via rank."""
        atoms = sample_atom_collection.list_contexts()
        
        ranks = [atom.rank for atom in atoms]
        assert ranks == [1, 2, 3, 4]  # Fact → Tension → Concept → Visual
    
    def test_narrative_progression(self, sample_atom_collection):
        """Verify atom types follow narrative progression."""
        atoms = sample_atom_collection.list_contexts()
        
        # First: establish facts (anchor)
        assert atoms[0].id.startswith("fact_")
        
        # Then: introduce tension (friction)
        assert atoms[1].id.startswith("tension_")
        
        # Then: present solution (insight)
        assert atoms[2].id.startswith("concept_")
        
        # Finally: visual reinforcement
        assert atoms[3].id.startswith("visual_")
    
    def test_tension_has_resolution_hint(self, sample_atom_collection):
        """Verify tension atoms can have resolution hints linking to concepts."""
        tension = sample_atom_collection.get("tension_001")
        
        assert tension.resolution_hint == "Microservices solved the issue"
    
    def test_concept_references_fact(self, sample_atom_collection):
        """Verify concept atoms can reference supporting facts."""
        concept = sample_atom_collection.get("concept_001")
        
        assert "fact_001" in concept.supporting_facts
    
    def test_visual_references_related_atom(self, sample_atom_collection):
        """Verify visual atoms can reference what they illustrate."""
        visual = sample_atom_collection.get("visual_001")
        
        assert visual.related_atom == "concept_001"


class TestAtomVisualHints:
    """Test that visual hints are available for layout decisions."""
    
    def test_all_atoms_have_visual_field(self, sample_atom_collection):
        """Verify all atoms have visual hint field."""
        atoms = sample_atom_collection.list_contexts()
        
        for atom in atoms:
            assert hasattr(atom, "visual")
            assert atom.visual is not None
    
    def test_visual_hints_for_slide_type_mapping(self, sample_atom_collection):
        """Verify visual hints can guide slide type selection."""
        fact = sample_atom_collection.get("fact_001")
        tension = sample_atom_collection.get("tension_001")
        concept = sample_atom_collection.get("concept_001")
        visual = sample_atom_collection.get("visual_001")
        
        # Data facts suggest charts
        assert fact.visual == "chart"
        
        # Problems suggest before-after comparisons
        assert tension.visual == "before-after"
        
        # Architecture solutions suggest diagrams
        assert concept.visual == "architecture"
        
        # Screenshots for visual demonstrations
        assert visual.visual == "screenshot"


class TestAtomCollectionFiltering:
    """Test filtering atoms for specific layout needs."""
    
    def test_get_by_type_for_facts(self, sample_atom_collection):
        """Verify filtering to get only FactAtoms."""
        facts = sample_atom_collection.get_by_type("FactAtom")
        
        assert len(facts) == 1
        assert all(atom.id.startswith("fact_") for atom in facts)
    
    def test_get_by_type_for_tensions(self, sample_atom_collection):
        """Verify filtering to get only TensionAtoms."""
        tensions = sample_atom_collection.get_by_type("TensionAtom")
        
        assert len(tensions) == 1
        assert all(atom.id.startswith("tension_") for atom in tensions)
    
    def test_get_by_type_for_concepts(self, sample_atom_collection):
        """Verify filtering to get only ConceptAtoms."""
        concepts = sample_atom_collection.get_by_type("ConceptAtom")
        
        assert len(concepts) == 1
        assert all(atom.id.startswith("concept_") for atom in concepts)
    
    def test_get_by_type_for_visuals(self, sample_atom_collection):
        """Verify filtering to get only VisualAtoms."""
        visuals = sample_atom_collection.get_by_type("VisualAtom")
        
        assert len(visuals) == 1
        assert all(atom.id.startswith("visual_") for atom in visuals)
    
    def test_get_by_source(self, sample_atom_collection):
        """Verify filtering atoms by source."""
        atoms = sample_atom_collection.get_by_source("src_001")
        
        assert len(atoms) == 4
