"""Integration tests for atom extractor with mocked LLM.

Tests the new narrative atom types:
- FactAtom → Objective facts
- TensionAtom → Problems/conflicts
- ConceptAtom → Solutions/insights
- VisualAtom → Visual descriptions
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from src.common.source import Source
from src.generation.atom.extractor import extract_atoms
from src.generation.atom.collection import AtomCollection


@pytest.fixture
def sample_source():
    """Create a sample source for testing."""
    return Source(
        source_id="test_001",
        name="Test Document",
        file_path="/path/to/test.txt",
        content_type="text/plain",
        content="""Our system grew from 10K to 1M users in six months.

The legacy database couldn't handle the increased load.
Response times degraded from 50ms to 3 seconds.

We adopted microservices to solve the scaling problem.
Each service could now scale independently.

The dashboard looked like a Christmas tree of red alerts."""
    )


@pytest.fixture
def mock_llm_response():
    """Create a mock LLM response with valid atom JSON."""
    return json.dumps({
        "atoms": [
            {
                "id": "fact_001",
                "type": "FactAtom",
                "rank": 1,
                "text": "System grew from 10K to 1M users in six months",
                "category": "data",
                "visual": "chart",
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 0,
                    "length": 50
                }
            },
            {
                "id": "tension_001",
                "type": "TensionAtom",
                "rank": 2,
                "text": "Legacy database couldn't handle increased load, response times degraded from 50ms to 3 seconds",
                "tension_type": "problem",
                "visual": "before-after",
                "resolution_hint": "Microservices solved the scaling issue",
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 52,
                    "length": 100
                }
            },
            {
                "id": "concept_001",
                "type": "ConceptAtom",
                "rank": 3,
                "text": "Adopted microservices for independent scaling of services",
                "concept_type": "solution",
                "visual": "architecture",
                "supporting_facts": ["fact_001"],
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 154,
                    "length": 80
                }
            },
            {
                "id": "visual_001",
                "type": "VisualAtom",
                "rank": 4,
                "description": "Dashboard like a Christmas tree of red alerts",
                "visual_category": "metaphor",
                "visual": "screenshot",
                "related_atom": "tension_001",
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 236,
                    "length": 55
                }
            }
        ]
    })


class TestAtomExtractorBasics:
    """Test basic atom extraction functionality."""
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_returns_atom_collection(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify extract_atoms returns an AtomCollection."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        
        assert isinstance(result, AtomCollection)
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_parses_fact_atoms(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify FactAtom is correctly parsed."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        facts = result.get_by_type("FactAtom")
        
        assert len(facts) == 1
        assert facts[0].id == "fact_001"
        assert "10K to 1M users" in facts[0].text
        assert facts[0].category == "data"
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_parses_tension_atoms(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify TensionAtom is correctly parsed."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        tensions = result.get_by_type("TensionAtom")
        
        assert len(tensions) == 1
        assert tensions[0].id == "tension_001"
        assert "couldn't handle" in tensions[0].text
        assert tensions[0].tension_type == "problem"
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_parses_concept_atoms(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify ConceptAtom is correctly parsed."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        concepts = result.get_by_type("ConceptAtom")
        
        assert len(concepts) == 1
        assert concepts[0].id == "concept_001"
        assert "microservices" in concepts[0].text
        assert concepts[0].concept_type == "solution"
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_parses_visual_atoms(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify VisualAtom is correctly parsed."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        visuals = result.get_by_type("VisualAtom")
        
        assert len(visuals) == 1
        assert visuals[0].id == "visual_001"
        assert "Christmas tree" in visuals[0].description
        assert visuals[0].visual_category == "metaphor"
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_all_atom_types(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify all four atom types are extracted."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        
        assert len(result) == 4
        assert len(result.get_by_type("FactAtom")) == 1
        assert len(result.get_by_type("TensionAtom")) == 1
        assert len(result.get_by_type("ConceptAtom")) == 1
        assert len(result.get_by_type("VisualAtom")) == 1


class TestAtomExtractorNarrativeStructure:
    """Test that atoms maintain narrative relationships."""
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_concept_references_facts(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify ConceptAtom can reference supporting FactAtoms."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        concepts = result.get_by_type("ConceptAtom")
        
        assert concepts[0].supporting_facts == ["fact_001"]
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_visual_references_related_atom(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify VisualAtom can reference related atoms."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        visuals = result.get_by_type("VisualAtom")
        
        assert visuals[0].related_atom == "tension_001"
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_atoms_sorted_by_rank(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify atoms are sorted by rank for narrative order."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        atoms = result.list_contexts()
        
        ranks = [atom.rank for atom in atoms]
        assert ranks == sorted(ranks)


class TestAtomExtractorEdgeCases:
    """Test edge cases and error handling."""
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_empty_response_returns_empty_collection(self, mock_call_llm):
        """Verify empty LLM response returns empty collection."""
        # Use unique source to avoid cache
        unique_source = Source(
            source_id="empty_test_001",
            name="Empty Test Document",
            file_path="/path/to/empty_test.txt",
            content_type="text/plain",
            content="This is unique content for empty response test."
        )
        mock_call_llm.return_value = json.dumps({"atoms": []})
        
        result = extract_atoms(unique_source)
        
        assert isinstance(result, AtomCollection)
        assert len(result) == 0
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_single_atom_type_response(self, mock_call_llm):
        """Verify response with only one atom type works."""
        # Use unique source to avoid cache
        unique_source = Source(
            source_id="single_test_001",
            name="Single Test Document",
            file_path="/path/to/single_test.txt",
            content_type="text/plain",
            content="This is unique content for single atom type test."
        )
        single_fact_response = json.dumps({
            "atoms": [
                {
                    "id": "fact_001",
                    "type": "FactAtom",
                    "rank": 1,
                    "text": "Single fact",
                    "category": "data",
                    "source_ref": {
                        "source_id": "single_test_001",
                        "file_path": "/path/to/single_test.txt",
                        "offset": 0,
                        "length": 11
                    }
                }
            ]
        })
        mock_call_llm.return_value = single_fact_response
        
        result = extract_atoms(unique_source)
        
        assert len(result) == 1
        assert len(result.get_by_type("FactAtom")) == 1
        assert len(result.get_by_type("TensionAtom")) == 0
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_atoms_with_visual_hints(self, mock_call_llm, sample_source, mock_llm_response):
        """Verify visual hints are preserved on atoms."""
        mock_call_llm.return_value = mock_llm_response
        
        result = extract_atoms(sample_source)
        
        facts = result.get_by_type("FactAtom")
        assert facts[0].visual == "chart"
        
        tensions = result.get_by_type("TensionAtom")
        assert tensions[0].visual == "before-after"
        
        concepts = result.get_by_type("ConceptAtom")
        assert concepts[0].visual == "architecture"
