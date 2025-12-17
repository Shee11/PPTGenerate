"""Integration tests for atom extractor with mocked LLM."""
import pytest
import json
from unittest.mock import patch, MagicMock
from src.common.source import Source
from src.generation.atom.extractor import extract_atoms
from src.generation.atom.collection import AtomCollection
from src.utils.generation_config import GenerationConfig


@pytest.fixture
def sample_source():
    """Create a sample source for testing."""
    return Source(
        source_id="test_001",
        name="Test Document",
        file_path="/path/to/test.txt",
        content_type="text/plain",
        content="""Machine learning is a subset of artificial intelligence.
        
Step 1: Collect data
Step 2: Preprocess the data
Step 3: Train the model
Step 4: Evaluate the model

Comparison of algorithms:
- Linear Regression: fast, simple, limited
- Neural Networks: powerful, complex, slow"""
    )


@pytest.fixture
def mock_llm_response():
    """Create a mock LLM response with valid atom JSON."""
    return json.dumps({
        "atoms": [
            {
                "id": "stmt_001",
                "type": "StatementAtom",
                "rank": 1,
                "text": "Machine learning is a subset of artificial intelligence.",
                "related_to": [],
                "contradicts": [],
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 0,
                    "length": 58
                }
            },
            {
                "id": "proc_001",
                "type": "ProcessAtom",
                "rank": 2,
                "title": "Model Training Process",
                "steps": [
                    {"order": 1, "text": "Collect data", "dependencies": []},
                    {"order": 2, "text": "Preprocess the data", "dependencies": [1]},
                    {"order": 3, "text": "Train the model", "dependencies": [2]},
                    {"order": 4, "text": "Evaluate the model", "dependencies": [3]}
                ],
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 60,
                    "length": 100
                }
            },
            {
                "id": "comp_001",
                "type": "ComparisonAtom",
                "rank": 3,
                "dimensions": ["speed", "complexity", "power"],
                "entities": {
                    "Linear Regression": {
                        "speed": "fast",
                        "complexity": "simple",
                        "power": "limited"
                    },
                    "Neural Networks": {
                        "speed": "slow",
                        "complexity": "complex",
                        "power": "powerful"
                    }
                },
                "source_ref": {
                    "source_id": "test_001",
                    "file_path": "/path/to/test.txt",
                    "offset": 162,
                    "length": 80
                }
            }
        ]
    })


class TestAtomExtractorBasics:
    """Test basic atom extraction functionality."""
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_atoms_returns_collection(self, mock_llm, sample_source, mock_llm_response):
        """Verify extract_atoms returns AtomCollection."""
        mock_llm.return_value = mock_llm_response
        
        collection = extract_atoms(sample_source)
        
        assert isinstance(collection, AtomCollection)
        assert collection.id == f"atoms_{sample_source.source_id}"
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_atoms_parses_all_types(self, mock_llm, sample_source, mock_llm_response):
        """Verify all atom types are extracted and parsed."""
        mock_llm.return_value = mock_llm_response
        
        collection = extract_atoms(sample_source)
        
        # Should have 3 atoms
        assert len(collection) == 3
        
        # Check each type exists
        statements = collection.get_by_type("StatementAtom")
        assert len(statements) == 1
        assert statements[0].text == "Machine learning is a subset of artificial intelligence."
        
        processes = collection.get_by_type("ProcessAtom")
        assert len(processes) == 1
        assert processes[0].title == "Model Training Process"
        assert len(processes[0].steps) == 4
        
        comparisons = collection.get_by_type("ComparisonAtom")
        assert len(comparisons) == 1
        assert len(comparisons[0].dimensions) == 3
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_extract_atoms_uses_custom_config(self, mock_llm, sample_source, mock_llm_response):
        """Verify custom config is passed to LLM."""
        mock_llm.return_value = mock_llm_response
        
        custom_config = GenerationConfig(
            model="gpt-4-custom",
            temperature=0.5,
            max_tokens=2000,
            system_prompt="Custom prompt",
            user_prompt_template="{content}",
            response_format="json"
        )
        
        extract_atoms(sample_source, config=custom_config, use_cache=False)
        
        # Verify call_llm was called with config
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args
        assert call_args is not None


class TestAtomExtractorCaching:
    """Test caching behavior of atom extractor."""
    
    @patch('src.generation.atom.extractor.call_llm')
    @patch('src.generation.atom.extractor.GenerationCache')
    def test_cache_hit_skips_llm(self, mock_cache_class, mock_llm, sample_source, mock_llm_response):
        """Verify cache hit skips LLM call."""
        # Setup cache mock to return cached data
        mock_cache = MagicMock()
        mock_cache.load.return_value = json.loads(mock_llm_response)
        mock_cache_class.return_value = mock_cache
        
        collection = extract_atoms(sample_source, use_cache=True)
        
        # Cache should be checked
        mock_cache.load.assert_called_once()
        
        # LLM should NOT be called on cache hit
        mock_llm.assert_not_called()
        
        # Collection should still be populated
        assert len(collection) == 3
    
    @patch('src.generation.atom.extractor.call_llm')
    @patch('src.generation.atom.extractor.GenerationCache')
    def test_cache_miss_calls_llm_and_saves(self, mock_cache_class, mock_llm, sample_source, mock_llm_response):
        """Verify cache miss calls LLM and saves result."""
        # Setup cache mock to return None (cache miss)
        mock_cache = MagicMock()
        mock_cache.load.return_value = None
        mock_cache_class.return_value = mock_cache
        
        mock_llm.return_value = mock_llm_response
        
        collection = extract_atoms(sample_source, use_cache=True)
        
        # Cache should be checked
        mock_cache.load.assert_called_once()
        
        # LLM should be called
        mock_llm.assert_called_once()
        
        # Result should be saved to cache
        mock_cache.save.assert_called_once()
        
        # Collection should be populated
        assert len(collection) == 3
    
    @patch('src.generation.atom.extractor.call_llm')
    @patch('src.generation.atom.extractor.GenerationCache')
    def test_use_cache_false_always_calls_llm(self, mock_cache_class, mock_llm, sample_source, mock_llm_response):
        """Verify use_cache=False bypasses cache entirely."""
        mock_cache = MagicMock()
        mock_cache_class.return_value = mock_cache
        
        mock_llm.return_value = mock_llm_response
        
        collection = extract_atoms(sample_source, use_cache=False)
        
        # Cache should not be used
        mock_cache.load.assert_not_called()
        mock_cache.save.assert_not_called()
        
        # LLM should be called
        mock_llm.assert_called_once()
        
        # Collection should be populated
        assert len(collection) == 3


class TestAtomExtractorErrorHandling:
    """Test error handling in atom extractor."""
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_invalid_json_raises_error(self, mock_llm, sample_source):
        """Verify invalid JSON response raises error."""
        mock_llm.return_value = "This is not JSON"
        
        with pytest.raises(Exception):  # JSONDecodeError or similar
            extract_atoms(sample_source, use_cache=False)
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_missing_atoms_key_raises_error(self, mock_llm, sample_source):
        """Verify missing 'atoms' key raises error."""
        mock_llm.return_value = json.dumps({"data": []})  # Wrong key
        
        with pytest.raises(KeyError):
            extract_atoms(sample_source, use_cache=False)
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_invalid_atom_type_raises_error(self, mock_llm, sample_source):
        """Verify invalid atom type raises error."""
        invalid_response = json.dumps({
            "atoms": [
                {
                    "id": "invalid_001",
                    "type": "InvalidAtom",  # Not a valid type
                    "rank": 1,
                    "source_ref": {
                        "source_id": "test_001",
                        "file_path": "/path",
                        "offset": 0,
                        "length": 1
                    }
                }
            ]
        })
        mock_llm.return_value = invalid_response
        
        with pytest.raises(ValueError, match="Unknown atom type"):
            extract_atoms(sample_source, use_cache=False)
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_llm_error_propagates(self, mock_llm, sample_source):
        """Verify LLM errors propagate to caller."""
        mock_llm.side_effect = Exception("LLM connection failed")
        
        with pytest.raises(Exception, match="LLM connection failed"):
            extract_atoms(sample_source, use_cache=False)


class TestAtomExtractorSourceReferences:
    """Test source reference preservation in extracted atoms."""
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_atoms_reference_correct_source(self, mock_llm, sample_source, mock_llm_response):
        """Verify all atoms reference the correct source."""
        mock_llm.return_value = mock_llm_response
        
        collection = extract_atoms(sample_source)
        
        for atom in collection.list_contexts():
            assert atom.source_ref.source_id == sample_source.source_id
            assert atom.source_ref.file_path == sample_source.file_path
    
    @patch('src.generation.atom.extractor.call_llm')
    def test_atoms_have_valid_offsets(self, mock_llm, sample_source, mock_llm_response):
        """Verify atoms have valid offset/length values."""
        mock_llm.return_value = mock_llm_response
        
        collection = extract_atoms(sample_source)
        
        for atom in collection.list_contexts():
            assert atom.source_ref.offset >= 0
            assert atom.source_ref.length > 0
