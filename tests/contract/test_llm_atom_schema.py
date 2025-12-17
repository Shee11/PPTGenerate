"""Contract tests verifying LLM atom extraction outputs match Pydantic schemas.

These tests validate that the JSON structures returned by the LLM
can be successfully parsed into our Pydantic atom models without errors.
"""
import pytest
import json
from pydantic import ValidationError
from src.common.source import SourceReference
from src.generation.atom.models import StatementAtom, ProcessAtom, ComparisonAtom, ProcessStep


class TestStatementAtomSchema:
    """Test StatementAtom schema validation against LLM outputs."""
    
    def test_minimal_statement_atom(self):
        """Verify minimal valid StatementAtom structure."""
        data = {
            "id": "stmt_001",
            "rank": 1,
            "text": "This is a statement.",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 21
            }
        }
        
        atom = StatementAtom(**data)
        assert atom.id == "stmt_001"
        assert atom.text == "This is a statement."
        assert atom.related_to == []
        assert atom.contradicts == []
    
    def test_statement_with_relationships(self):
        """Verify StatementAtom with relationship fields."""
        data = {
            "id": "stmt_002",
            "rank": 2,
            "text": "This supports the previous statement.",
            "related_to": ["stmt_001"],
            "contradicts": [],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 22,
                "length": 38
            }
        }
        
        atom = StatementAtom(**data)
        assert atom.related_to == ["stmt_001"]
        assert len(atom.contradicts) == 0
    
    def test_statement_with_contradictions(self):
        """Verify StatementAtom with contradicts field."""
        data = {
            "id": "stmt_003",
            "rank": 3,
            "text": "This contradicts the first statement.",
            "related_to": [],
            "contradicts": ["stmt_001"],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 60,
                "length": 38
            }
        }
        
        atom = StatementAtom(**data)
        assert atom.contradicts == ["stmt_001"]
    
    def test_statement_missing_text_fails(self):
        """Verify missing text field fails validation."""
        data = {
            "id": "stmt_bad",
            "rank": 1,
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="text"):
            StatementAtom(**data)
    
    def test_statement_with_metadata(self):
        """Verify StatementAtom accepts optional metadata."""
        data = {
            "id": "stmt_004",
            "rank": 4,
            "text": "Statement with metadata.",
            "metadata": {"confidence": 0.95, "category": "fact"},
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 100,
                "length": 24
            }
        }
        
        atom = StatementAtom(**data)
        assert atom.metadata["confidence"] == 0.95


class TestProcessAtomSchema:
    """Test ProcessAtom schema validation against LLM outputs."""
    
    def test_minimal_process_atom(self):
        """Verify minimal valid ProcessAtom structure."""
        data = {
            "id": "proc_001",
            "rank": 1,
            "title": "Simple Process",
            "steps": [
                {"order": 1, "text": "First step"}
            ],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 50
            }
        }
        
        atom = ProcessAtom(**data)
        assert atom.title == "Simple Process"
        assert len(atom.steps) == 1
        assert atom.steps[0].order == 1
    
    def test_process_with_multiple_steps(self):
        """Verify ProcessAtom with sequential steps."""
        data = {
            "id": "proc_002",
            "rank": 2,
            "title": "Multi-Step Process",
            "steps": [
                {"order": 1, "text": "Initialize system", "dependencies": []},
                {"order": 2, "text": "Load configuration", "dependencies": [1]},
                {"order": 3, "text": "Start services", "dependencies": [2]},
                {"order": 4, "text": "Verify health", "dependencies": [3]}
            ],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 100,
                "length": 200
            }
        }
        
        atom = ProcessAtom(**data)
        assert len(atom.steps) == 4
        assert atom.steps[1].dependencies == [1]
        assert atom.steps[3].dependencies == [3]
    
    def test_process_with_parallel_steps(self):
        """Verify ProcessAtom with parallel execution dependencies."""
        data = {
            "id": "proc_003",
            "rank": 3,
            "title": "Parallel Process",
            "steps": [
                {"order": 1, "text": "Start", "dependencies": []},
                {"order": 2, "text": "Task A", "dependencies": [1]},
                {"order": 3, "text": "Task B", "dependencies": [1]},
                {"order": 4, "text": "Merge results", "dependencies": [2, 3]}
            ],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 300,
                "length": 150
            }
        }
        
        atom = ProcessAtom(**data)
        # Steps 2 and 3 depend on step 1 (parallel)
        assert atom.steps[1].dependencies == [1]
        assert atom.steps[2].dependencies == [1]
        # Step 4 depends on both steps 2 and 3
        assert atom.steps[3].dependencies == [2, 3]
    
    def test_process_missing_title_fails(self):
        """Verify missing title field fails validation."""
        data = {
            "id": "proc_bad",
            "rank": 1,
            "steps": [{"order": 1, "text": "Step"}],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="title"):
            ProcessAtom(**data)
    
    def test_process_empty_steps_fails(self):
        """Verify empty steps list fails validation."""
        data = {
            "id": "proc_bad2",
            "rank": 1,
            "title": "Empty Process",
            "steps": [],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError):
            ProcessAtom(**data)
    
    def test_process_step_zero_order_fails(self):
        """Verify step order must be >= 1."""
        data = {
            "id": "proc_bad3",
            "rank": 1,
            "title": "Bad Order",
            "steps": [{"order": 0, "text": "Invalid"}],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError):
            ProcessAtom(**data)


class TestComparisonAtomSchema:
    """Test ComparisonAtom schema validation against LLM outputs."""
    
    def test_minimal_comparison_atom(self):
        """Verify minimal valid ComparisonAtom structure."""
        data = {
            "id": "comp_001",
            "rank": 1,
            "dimensions": ["price"],
            "entities": {
                "Product A": {"price": "$100"}
            },
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 50
            }
        }
        
        atom = ComparisonAtom(**data)
        assert atom.dimensions == ["price"]
        assert "Product A" in atom.entities
    
    def test_comparison_multiple_dimensions(self):
        """Verify ComparisonAtom with multiple comparison dimensions."""
        data = {
            "id": "comp_002",
            "rank": 2,
            "dimensions": ["speed", "cost", "reliability"],
            "entities": {
                "Option A": {
                    "speed": "fast",
                    "cost": "high",
                    "reliability": "excellent"
                },
                "Option B": {
                    "speed": "medium",
                    "cost": "low",
                    "reliability": "good"
                },
                "Option C": {
                    "speed": "slow",
                    "cost": "very low",
                    "reliability": "fair"
                }
            },
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 100,
                "length": 200
            }
        }
        
        atom = ComparisonAtom(**data)
        assert len(atom.dimensions) == 3
        assert len(atom.entities) == 3
        assert atom.entities["Option A"]["speed"] == "fast"
        assert atom.entities["Option C"]["cost"] == "very low"
    
    def test_comparison_missing_dimensions_fails(self):
        """Verify missing dimensions field fails validation."""
        data = {
            "id": "comp_bad",
            "rank": 1,
            "entities": {"A": {"x": "y"}},
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="dimensions"):
            ComparisonAtom(**data)
    
    def test_comparison_empty_dimensions_fails(self):
        """Verify empty dimensions list fails validation."""
        data = {
            "id": "comp_bad2",
            "rank": 1,
            "dimensions": [],
            "entities": {"A": {"x": "y"}},
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError):
            ComparisonAtom(**data)
    
    def test_comparison_missing_entities_fails(self):
        """Verify missing entities field fails validation."""
        data = {
            "id": "comp_bad3",
            "rank": 1,
            "dimensions": ["x"],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="entities"):
            ComparisonAtom(**data)


class TestSourceReferenceSchema:
    """Test SourceReference schema validation."""
    
    def test_valid_source_reference(self):
        """Verify valid SourceReference structure."""
        data = {
            "source_id": "src_001",
            "file_path": "/path/to/file.txt",
            "offset": 0,
            "length": 100
        }
        
        ref = SourceReference(**data)
        assert ref.source_id == "src_001"
        assert ref.offset == 0
        assert ref.length == 100
    
    def test_source_reference_with_line_number(self):
        """Verify SourceReference with optional line_number."""
        data = {
            "source_id": "src_002",
            "file_path": "/path/to/file.txt",
            "offset": 500,
            "length": 50,
            "line_number": 25
        }
        
        ref = SourceReference(**data)
        assert ref.line_number == 25
    
    def test_negative_offset_fails(self):
        """Verify negative offset fails validation."""
        data = {
            "source_id": "src_bad",
            "file_path": "/path",
            "offset": -1,
            "length": 10
        }
        
        with pytest.raises(ValidationError):
            SourceReference(**data)
    
    def test_zero_length_fails(self):
        """Verify zero or negative length fails validation."""
        data = {
            "source_id": "src_bad2",
            "file_path": "/path",
            "offset": 0,
            "length": 0
        }
        
        with pytest.raises(ValidationError):
            SourceReference(**data)
    
    def test_zero_line_number_fails(self):
        """Verify line_number must be >= 1."""
        data = {
            "source_id": "src_bad3",
            "file_path": "/path",
            "offset": 0,
            "length": 10,
            "line_number": 0
        }
        
        with pytest.raises(ValidationError):
            SourceReference(**data)


class TestAtomCollectionSchema:
    """Test that LLM response structure matches collection expectations."""
    
    def test_valid_atoms_array_structure(self):
        """Verify expected 'atoms' array structure in LLM response."""
        llm_response = {
            "atoms": [
                {
                    "id": "stmt_001",
                    "type": "StatementAtom",
                    "rank": 1,
                    "text": "Test statement",
                    "source_ref": {
                        "source_id": "src_001",
                        "file_path": "/path",
                        "offset": 0,
                        "length": 14
                    }
                },
                {
                    "id": "proc_001",
                    "type": "ProcessAtom",
                    "rank": 2,
                    "title": "Test process",
                    "steps": [{"order": 1, "text": "Step 1"}],
                    "source_ref": {
                        "source_id": "src_001",
                        "file_path": "/path",
                        "offset": 15,
                        "length": 20
                    }
                }
            ]
        }
        
        # Verify structure
        assert "atoms" in llm_response
        assert isinstance(llm_response["atoms"], list)
        assert len(llm_response["atoms"]) == 2
        
        # Verify each atom has required fields
        for atom_data in llm_response["atoms"]:
            assert "id" in atom_data
            assert "type" in atom_data
            assert "rank" in atom_data
            assert "source_ref" in atom_data
    
    def test_mixed_atom_types_in_response(self):
        """Verify LLM can return multiple atom types in one response."""
        llm_response = {
            "atoms": [
                {
                    "id": "stmt_001",
                    "type": "StatementAtom",
                    "rank": 1,
                    "text": "Statement",
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 0, "length": 9}
                },
                {
                    "id": "proc_001",
                    "type": "ProcessAtom",
                    "rank": 2,
                    "title": "Process",
                    "steps": [{"order": 1, "text": "Step"}],
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 10, "length": 10}
                },
                {
                    "id": "comp_001",
                    "type": "ComparisonAtom",
                    "rank": 3,
                    "dimensions": ["d"],
                    "entities": {"E": {"d": "v"}},
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 20, "length": 10}
                }
            ]
        }
        
        # Verify we can parse all types
        types_found = set()
        for atom_data in llm_response["atoms"]:
            atom_type = atom_data["type"]
            types_found.add(atom_type)
            
            if atom_type == "StatementAtom":
                StatementAtom(**atom_data)
            elif atom_type == "ProcessAtom":
                ProcessAtom(**atom_data)
            elif atom_type == "ComparisonAtom":
                ComparisonAtom(**atom_data)
        
        assert types_found == {"StatementAtom", "ProcessAtom", "ComparisonAtom"}
