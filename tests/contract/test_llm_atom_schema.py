"""Contract tests verifying LLM atom extraction outputs match Pydantic schemas.

These tests validate that the JSON structures returned by the LLM
can be successfully parsed into our new narrative atom models.

Atom Types (Narrative-focused):
- FactAtom → Objective context, definitions (Anchor slides)
- StatAtom → Quantitative data, metrics (Data visualization slides)
- QuoteAtom → Verbatim memorable phrases (Impact slides)
- TensionAtom → Problems, conflicts, contradictions (Friction slides)
- ConceptAtom → Solutions, insights, takeaways (Insight slides)
- VisualAtom → Visual descriptions, metaphors, demos
"""
import pytest
from pydantic import ValidationError
from src.common.source import SourceReference
from src.generation.atom.models import FactAtom, StatAtom, QuoteAtom, TensionAtom, ConceptAtom, VisualAtom


class TestFactAtomSchema:
    """Test FactAtom schema validation against LLM outputs."""
    
    def test_minimal_fact_atom(self):
        """Verify minimal valid FactAtom structure."""
        data = {
            "id": "fact_001",
            "rank": 1,
            "text": "System handles 1M requests per second.",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 40
            }
        }
        
        atom = FactAtom(**data)
        assert atom.id == "fact_001"
        assert atom.text == "System handles 1M requests per second."
        assert atom.category == "other"  # default
        assert atom.visual == "none"  # default
    
    def test_fact_with_category(self):
        """Verify FactAtom with category field."""
        data = {
            "id": "fact_002",
            "rank": 2,
            "text": "The microservices architecture enables independent deployment.",
            "category": "architecture",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 50,
                "length": 60
            }
        }
        
        atom = FactAtom(**data)
        assert atom.category == "architecture"
    
    def test_fact_with_visual_hint(self):
        """Verify FactAtom with visual field."""
        data = {
            "id": "fact_003",
            "rank": 3,
            "text": "Revenue grew 300% year over year.",
            "category": "data",
            "visual": "chart",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 120,
                "length": 35
            }
        }
        
        atom = FactAtom(**data)
        assert atom.visual == "chart"
    
    def test_fact_all_categories(self):
        """Verify all valid category values."""
        valid_categories = ["data", "definition", "architecture", "status", "other"]
        
        for i, category in enumerate(valid_categories):
            data = {
                "id": f"fact_{i:03d}",
                "rank": i + 1,
                "text": f"Fact with {category} category",
                "category": category,
                "source_ref": {
                    "source_id": "src",
                    "file_path": "/path",
                    "offset": i * 10,
                    "length": 10
                }
            }
            atom = FactAtom(**data)
            assert atom.category == category
    
    def test_fact_missing_text_fails(self):
        """Verify missing text field fails validation."""
        data = {
            "id": "fact_bad",
            "rank": 1,
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="text"):
            FactAtom(**data)
    
    def test_fact_accepts_any_category(self):
        """Verify category field accepts any string value (LLM flexibility)."""
        data = {
            "id": "fact_flex",
            "rank": 1,
            "text": "Some fact",
            "category": "custom_category",
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 10
            }
        }
        
        # Should not raise - category is now a flexible string field
        atom = FactAtom(**data)
        assert atom.category == "custom_category"


class TestStatAtomSchema:
    """Test StatAtom schema validation against LLM outputs."""
    
    def test_minimal_stat_atom(self):
        """Verify minimal valid StatAtom structure."""
        data = {
            "id": "stat_001",
            "rank": 1,
            "value": "50%",
            "label": "Latency Reduction",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 30
            }
        }
        
        atom = StatAtom(**data)
        assert atom.id == "stat_001"
        assert atom.value == "50%"
        assert atom.label == "Latency Reduction"
        assert atom.context == ""  # default
        assert atom.visual == "none"  # default
    
    def test_stat_with_context(self):
        """Verify StatAtom with context field."""
        data = {
            "id": "stat_002",
            "rank": 2,
            "value": "200ms",
            "label": "Response Time",
            "context": "measured under peak load",
            "visual": "big-number",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 50,
                "length": 40
            }
        }
        
        atom = StatAtom(**data)
        assert atom.context == "measured under peak load"
        assert atom.visual == "big-number"
    
    def test_stat_various_value_formats(self):
        """Verify StatAtom accepts various numeric formats."""
        test_cases = [
            ("50%", "Improvement"),
            ("3x", "Battery Drain Reduction"),
            ("1M", "Requests Per Second"),
            ("95.5%", "Accuracy Rate"),
            ("$1.2B", "Revenue"),
        ]
        
        for i, (value, label) in enumerate(test_cases):
            data = {
                "id": f"stat_{i:03d}",
                "rank": i + 1,
                "value": value,
                "label": label,
                "source_ref": {
                    "source_id": "src",
                    "file_path": "/path",
                    "offset": i * 10,
                    "length": 10
                }
            }
            atom = StatAtom(**data)
            assert atom.value == value
            assert atom.label == label
    
    def test_stat_missing_value_fails(self):
        """Verify missing value field fails validation."""
        data = {
            "id": "stat_bad",
            "rank": 1,
            "label": "Some Metric",
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 10
            }
        }
        
        with pytest.raises(ValidationError, match="value"):
            StatAtom(**data)
    
    def test_stat_missing_label_fails(self):
        """Verify missing label field fails validation."""
        data = {
            "id": "stat_bad2",
            "rank": 1,
            "value": "50%",
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 10
            }
        }
        
        with pytest.raises(ValidationError, match="label"):
            StatAtom(**data)


class TestQuoteAtomSchema:
    """Test QuoteAtom schema validation against LLM outputs."""
    
    def test_minimal_quote_atom(self):
        """Verify minimal valid QuoteAtom structure."""
        data = {
            "id": "quote_001",
            "rank": 1,
            "quote": "Speed is not a feature. It is a requirement.",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 50
            }
        }
        
        atom = QuoteAtom(**data)
        assert atom.id == "quote_001"
        assert atom.quote == "Speed is not a feature. It is a requirement."
        assert atom.attribution == ""  # default
        assert atom.context == ""  # default
        assert atom.visual == "none"  # default
    
    def test_quote_with_attribution(self):
        """Verify QuoteAtom with attribution field."""
        data = {
            "id": "quote_002",
            "rank": 2,
            "quote": "We don't ship features. We ship outcomes.",
            "attribution": "CTO",
            "visual": "quote-card",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 60,
                "length": 45
            }
        }
        
        atom = QuoteAtom(**data)
        assert atom.attribution == "CTO"
        assert atom.visual == "quote-card"
    
    def test_quote_with_context(self):
        """Verify QuoteAtom with context field."""
        data = {
            "id": "quote_003",
            "rank": 3,
            "quote": "The best code is no code at all.",
            "attribution": "Senior Engineer",
            "context": "during code review discussion",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 120,
                "length": 35
            }
        }
        
        atom = QuoteAtom(**data)
        assert atom.context == "during code review discussion"
    
    def test_quote_missing_quote_fails(self):
        """Verify missing quote field fails validation."""
        data = {
            "id": "quote_bad",
            "rank": 1,
            "attribution": "Someone",
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 10
            }
        }
        
        with pytest.raises(ValidationError, match="quote"):
            QuoteAtom(**data)


class TestTensionAtomSchema:
    """Test TensionAtom schema validation against LLM outputs."""
    
    def test_minimal_tension_atom(self):
        """Verify minimal valid TensionAtom structure."""
        data = {
            "id": "tension_001",
            "rank": 1,
            "text": "Legacy systems couldn't handle the new load requirements.",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 60
            }
        }
        
        atom = TensionAtom(**data)
        assert atom.id == "tension_001"
        assert atom.text == "Legacy systems couldn't handle the new load requirements."
        assert atom.tension_type == "problem"  # default
    
    def test_tension_with_type(self):
        """Verify TensionAtom with tension_type field."""
        data = {
            "id": "tension_002",
            "rank": 2,
            "text": "Teams wanted autonomy but needed consistency.",
            "tension_type": "trade-off",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 70,
                "length": 45
            }
        }
        
        atom = TensionAtom(**data)
        assert atom.tension_type == "trade-off"
    
    def test_tension_all_types(self):
        """Verify all valid tension_type values."""
        valid_types = ["problem", "contradiction", "trade-off", "surprise", "mistake", "other"]
        
        for i, tension_type in enumerate(valid_types):
            data = {
                "id": f"tension_{i:03d}",
                "rank": i + 1,
                "text": f"Tension with {tension_type} type",
                "tension_type": tension_type,
                "source_ref": {
                    "source_id": "src",
                    "file_path": "/path",
                    "offset": i * 10,
                    "length": 10
                }
            }
            atom = TensionAtom(**data)
            assert atom.tension_type == tension_type
    
    def test_tension_with_resolution_hint(self):
        """Verify TensionAtom with resolution_hint field."""
        data = {
            "id": "tension_003",
            "rank": 3,
            "text": "Performance degraded as user base grew.",
            "tension_type": "problem",
            "resolution_hint": "Solved by adopting microservices",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 120,
                "length": 40
            }
        }
        
        atom = TensionAtom(**data)
        assert atom.resolution_hint == "Solved by adopting microservices"
    
    def test_tension_missing_text_fails(self):
        """Verify missing text field fails validation."""
        data = {
            "id": "tension_bad",
            "rank": 1,
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="text"):
            TensionAtom(**data)


class TestConceptAtomSchema:
    """Test ConceptAtom schema validation against LLM outputs."""
    
    def test_minimal_concept_atom(self):
        """Verify minimal valid ConceptAtom structure."""
        data = {
            "id": "concept_001",
            "rank": 1,
            "text": "Microservices enabled independent scaling of components.",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 55
            }
        }
        
        atom = ConceptAtom(**data)
        assert atom.id == "concept_001"
        assert atom.text == "Microservices enabled independent scaling of components."
        assert atom.concept_type == "insight"  # default
    
    def test_concept_with_type(self):
        """Verify ConceptAtom with concept_type field."""
        data = {
            "id": "concept_002",
            "rank": 2,
            "text": "We adopted event-driven architecture to solve the coupling problem.",
            "concept_type": "solution",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 60,
                "length": 70
            }
        }
        
        atom = ConceptAtom(**data)
        assert atom.concept_type == "solution"
    
    def test_concept_all_types(self):
        """Verify all valid concept_type values."""
        valid_types = ["solution", "insight", "method", "principle", "takeaway", "other"]
        
        for i, concept_type in enumerate(valid_types):
            data = {
                "id": f"concept_{i:03d}",
                "rank": i + 1,
                "text": f"Concept with {concept_type} type",
                "concept_type": concept_type,
                "source_ref": {
                    "source_id": "src",
                    "file_path": "/path",
                    "offset": i * 10,
                    "length": 10
                }
            }
            atom = ConceptAtom(**data)
            assert atom.concept_type == concept_type
    
    def test_concept_with_supporting_facts(self):
        """Verify ConceptAtom with supporting_facts field."""
        data = {
            "id": "concept_003",
            "rank": 3,
            "text": "Start with a monolith, then extract services.",
            "concept_type": "method",
            "supporting_facts": ["fact_001", "fact_003"],
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 140,
                "length": 45
            }
        }
        
        atom = ConceptAtom(**data)
        assert atom.supporting_facts == ["fact_001", "fact_003"]
    
    def test_concept_missing_text_fails(self):
        """Verify missing text field fails validation."""
        data = {
            "id": "concept_bad",
            "rank": 1,
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="text"):
            ConceptAtom(**data)


class TestVisualAtomSchema:
    """Test VisualAtom schema validation against LLM outputs."""
    
    def test_minimal_visual_atom(self):
        """Verify minimal valid VisualAtom structure."""
        data = {
            "id": "visual_001",
            "rank": 1,
            "description": "Screen filled with red error messages.",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 0,
                "length": 40
            }
        }
        
        atom = VisualAtom(**data)
        assert atom.id == "visual_001"
        assert atom.description == "Screen filled with red error messages."
        assert atom.visual_category == "other"  # default
    
    def test_visual_with_category(self):
        """Verify VisualAtom with visual_category field."""
        data = {
            "id": "visual_002",
            "rank": 2,
            "description": "Architecture like a thousand-layer cake.",
            "visual_category": "metaphor",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 50,
                "length": 45
            }
        }
        
        atom = VisualAtom(**data)
        assert atom.visual_category == "metaphor"
    
    def test_visual_all_categories(self):
        """Verify all valid visual_category values."""
        valid_categories = ["metaphor", "demo", "screenshot", "diagram", "comparison", "other"]
        
        for i, category in enumerate(valid_categories):
            data = {
                "id": f"visual_{i:03d}",
                "rank": i + 1,
                "description": f"Visual with {category} category",
                "visual_category": category,
                "source_ref": {
                    "source_id": "src",
                    "file_path": "/path",
                    "offset": i * 10,
                    "length": 10
                }
            }
            atom = VisualAtom(**data)
            assert atom.visual_category == category
    
    def test_visual_with_related_atom(self):
        """Verify VisualAtom with related_atom field."""
        data = {
            "id": "visual_003",
            "rank": 3,
            "description": "Before/after comparison of response times.",
            "visual_category": "comparison",
            "related_atom": "fact_001",
            "source_ref": {
                "source_id": "src_001",
                "file_path": "/path/to/file.txt",
                "offset": 100,
                "length": 45
            }
        }
        
        atom = VisualAtom(**data)
        assert atom.related_atom == "fact_001"
    
    def test_visual_missing_description_fails(self):
        """Verify missing description field fails validation."""
        data = {
            "id": "visual_bad",
            "rank": 1,
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 1
            }
        }
        
        with pytest.raises(ValidationError, match="description"):
            VisualAtom(**data)


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


class TestAtomCollectionSchema:
    """Test that LLM response structure matches collection expectations."""
    
    def test_valid_atoms_array_structure(self):
        """Verify expected 'atoms' array structure in LLM response."""
        llm_response = {
            "atoms": [
                {
                    "id": "fact_001",
                    "type": "FactAtom",
                    "rank": 1,
                    "text": "Test fact",
                    "category": "data",
                    "source_ref": {
                        "source_id": "src_001",
                        "file_path": "/path",
                        "offset": 0,
                        "length": 10
                    }
                },
                {
                    "id": "tension_001",
                    "type": "TensionAtom",
                    "rank": 2,
                    "text": "Test tension",
                    "category": "problem",
                    "source_ref": {
                        "source_id": "src_001",
                        "file_path": "/path",
                        "offset": 15,
                        "length": 15
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
        """Verify LLM can return all four atom types in one response."""
        llm_response = {
            "atoms": [
                {
                    "id": "fact_001",
                    "type": "FactAtom",
                    "rank": 1,
                    "text": "A factual statement",
                    "category": "data",
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 0, "length": 20}
                },
                {
                    "id": "tension_001",
                    "type": "TensionAtom",
                    "rank": 2,
                    "text": "A problem emerged",
                    "category": "problem",
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 25, "length": 20}
                },
                {
                    "id": "concept_001",
                    "type": "ConceptAtom",
                    "rank": 3,
                    "text": "The solution was clear",
                    "concept_type": "solution",
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 50, "length": 25}
                },
                {
                    "id": "visual_001",
                    "type": "VisualAtom",
                    "rank": 4,
                    "description": "A striking visual metaphor",
                    "visual_category": "metaphor",
                    "source_ref": {"source_id": "s", "file_path": "p", "offset": 80, "length": 30}
                }
            ]
        }
        
        # Verify we can parse all types
        types_found = set()
        for atom_data in llm_response["atoms"]:
            atom_type = atom_data["type"]
            types_found.add(atom_type)
            
            if atom_type == "FactAtom":
                FactAtom(**atom_data)
            elif atom_type == "TensionAtom":
                TensionAtom(**atom_data)
            elif atom_type == "ConceptAtom":
                ConceptAtom(**atom_data)
            elif atom_type == "VisualAtom":
                VisualAtom(**atom_data)
        
        assert types_found == {"FactAtom", "TensionAtom", "ConceptAtom", "VisualAtom"}


class TestVisualFieldValues:
    """Test valid visual field values across all atoms."""
    
    def test_all_visual_types(self):
        """Verify all valid visual type values work."""
        valid_visuals = [
            "chart", "diagram", "code", "screenshot", "photo",
            "icon", "quote-card", "timeline", "comparison-table",
            "flow", "architecture", "before-after", "none"
        ]
        
        for i, visual in enumerate(valid_visuals):
            data = {
                "id": f"fact_{i:03d}",
                "rank": i + 1,
                "text": f"Fact with {visual} visual",
                "visual": visual,
                "source_ref": {
                    "source_id": "src",
                    "file_path": "/path",
                    "offset": i * 10,
                    "length": 10
                }
            }
            atom = FactAtom(**data)
            assert atom.visual == visual
    
    def test_invalid_visual_fails(self):
        """Verify invalid visual value fails validation."""
        data = {
            "id": "fact_bad",
            "rank": 1,
            "text": "Some fact",
            "visual": "invalid_visual_type",
            "source_ref": {
                "source_id": "src",
                "file_path": "/path",
                "offset": 0,
                "length": 10
            }
        }
        
        with pytest.raises(ValidationError):
            FactAtom(**data)
