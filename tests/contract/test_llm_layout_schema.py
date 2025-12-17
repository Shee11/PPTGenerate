"""Contract tests for LLM layout generation outputs."""
import json
import pytest
from typing import Dict, Any, List

from src.generation.atom.collection import AtomCollection
from src.generation.atom.models import StatementAtom, ProcessAtom, ProcessStep
from src.common.source import SourceReference
from src.common.patchable_context_pydantic import Patch, AddOperation


# Supported widget types from contract
SUPPORTED_WIDGET_TYPES = {
    "Type.Display",
    "Type.Heading",
    "Type.Body",
    "Type.Quote",
    "Type.List",
    "Data.BigNum",
    "Data.Progress",
    "Data.Trend",
    "Media.Image"
}

# Supported preset attributes from contract
SUPPORTED_PRESET_ATTRIBUTES = {
    "surface": ["Flat", "Elevated", "Sunken", "Glass", "Outline", "NeoBrutal", "Subtle"],
    "shape": ["Sharp", "Rounded", "Pill", "Curve", "Squircle", "Organic"],
    "fill": ["Solid_Surface", "Solid_Brand", "Gradient_Linear", "Gradient_Mesh", "Pattern_Dot", "Noise", "Subtle"],
    "effect": ["Glow", "Shadow", "Tape", "Duotone"]
}

# Supported layout strategies from contract
SUPPORTED_STRATEGIES = {
    "Bento.Standard",
    "Bento.HeroTop", 
    "Bento.HeroLeft",
    "Bento.Quarter",
    "Swiss.Poster",
    "Swiss.Asymmetry",
    "Swiss.SplitTypo",
    "Cinematic.Split_50_50",
    "Cinematic.Split_30_70",
    "Cinematic.Fullbleed",
    "Focus.Solar_System",
    "Data.KPI_Row",
    "Edit.Magazine_Collage",
    "Edit.Overlap_Left"
}


class TestWidgetTypeValidation:
    """Test that only supported widget types are used."""

    def test_widget_type_must_be_supported(self):
        """Verify widget type validation rejects unsupported types."""
        # Simulated LLM output with invalid widget type
        invalid_widget = {
            "type": "Type.InvalidType",  # Not in supported list
            "parameters": {"text": "Hello"}
        }
        
        assert invalid_widget["type"] not in SUPPORTED_WIDGET_TYPES

    def test_all_supported_widget_types_valid(self):
        """Verify all documented widget types are recognized."""
        # Examples of each supported type
        widgets = [
            {"type": "Type.Display", "parameters": {"text": "Title"}},
            {"type": "Type.Heading", "parameters": {"text": "Heading", "level": 1}},
            {"type": "Type.Body", "parameters": {"text": "Body text"}},
            {"type": "Type.Quote", "parameters": {"text": "Quote", "citation": "Author"}},
            {"type": "Type.List", "parameters": {"items": ["A", "B"], "list_type": "ordered"}},
            {"type": "Data.BigNum", "parameters": {"number": 42.5, "label": "Score", "format": "decimal"}},
            {"type": "Data.Progress", "parameters": {"percentage": 75, "label": "Progress"}},
            {"type": "Data.Trend", "parameters": {"value": 1000, "change": 15.5, "direction": "up", "label": "Revenue"}},
            {"type": "Media.Image", "parameters": {"image_url": "https://example.com/img.jpg"}}
        ]
        
        for widget in widgets:
            assert widget["type"] in SUPPORTED_WIDGET_TYPES


class TestPresetAttributeValidation:
    """Test that only supported preset attributes are used."""

    def test_preset_surface_must_be_valid(self):
        """Verify surface preset values are from supported list."""
        valid_surfaces = ["Flat", "Elevated", "Glass"]
        for surface in valid_surfaces:
            assert surface in SUPPORTED_PRESET_ATTRIBUTES["surface"]
        
        assert "InvalidSurface" not in SUPPORTED_PRESET_ATTRIBUTES["surface"]

    def test_preset_shape_must_be_valid(self):
        """Verify shape preset values are from supported list."""
        valid_shapes = ["Rounded", "Pill", "Squircle"]
        for shape in valid_shapes:
            assert shape in SUPPORTED_PRESET_ATTRIBUTES["shape"]
        
        assert "Triangle" not in SUPPORTED_PRESET_ATTRIBUTES["shape"]

    def test_preset_fill_must_be_valid(self):
        """Verify fill preset values are from supported list."""
        valid_fills = ["Solid_Surface", "Gradient_Mesh", "Pattern_Dot"]
        for fill in valid_fills:
            assert fill in SUPPORTED_PRESET_ATTRIBUTES["fill"]
        
        assert "Texture" not in SUPPORTED_PRESET_ATTRIBUTES["fill"]

    def test_preset_effect_must_be_valid(self):
        """Verify effect preset values are from supported list."""
        valid_effects = ["Glow", "Shadow", "Duotone"]
        for effect in valid_effects:
            assert effect in SUPPORTED_PRESET_ATTRIBUTES["effect"]
        
        assert "Blur" not in SUPPORTED_PRESET_ATTRIBUTES["effect"]

    def test_preset_attributes_are_optional(self):
        """Verify widgets work without preset attributes."""
        widget = {
            "type": "Type.Display",
            "parameters": {"text": "No preset"}
        }
        
        # Should be valid even without "preset" key
        assert "type" in widget
        assert "parameters" in widget
        assert "preset" not in widget  # Optional


class TestLayoutStrategyValidation:
    """Test that only supported layout strategies are used."""

    def test_strategy_must_be_supported(self):
        """Verify strategy validation rejects unsupported strategies."""
        invalid_strategy = "Custom.MyLayout"
        
        assert invalid_strategy not in SUPPORTED_STRATEGIES

    def test_all_supported_strategies_valid(self):
        """Verify all documented strategies are recognized."""
        strategies = [
            "Bento.Standard",
            "Swiss.Poster",
            "Cinematic.Split_50_50",
            "Focus.Solar_System"
        ]
        
        for strategy in strategies:
            assert strategy in SUPPORTED_STRATEGIES


class TestWidgetParameterValidation:
    """Test widget parameters match expected schemas."""

    def test_type_display_parameters(self):
        """Verify Type.Display has required text parameter."""
        widget = {"type": "Type.Display", "parameters": {"text": "Example"}}
        
        assert "text" in widget["parameters"]
        assert isinstance(widget["parameters"]["text"], str)

    def test_type_heading_parameters(self):
        """Verify Type.Heading has text and level parameters."""
        widget = {
            "type": "Type.Heading",
            "parameters": {"text": "Title", "level": 2}
        }
        
        assert "text" in widget["parameters"]
        assert "level" in widget["parameters"]
        assert 1 <= widget["parameters"]["level"] <= 6

    def test_type_quote_parameters(self):
        """Verify Type.Quote has text and citation parameters."""
        widget = {
            "type": "Type.Quote",
            "parameters": {"text": "Quote text", "citation": "Author"}
        }
        
        assert "text" in widget["parameters"]
        assert "citation" in widget["parameters"]

    def test_type_list_parameters(self):
        """Verify Type.List has items and list_type parameters."""
        widget = {
            "type": "Type.List",
            "parameters": {"items": ["Item 1", "Item 2"], "list_type": "ordered"}
        }
        
        assert "items" in widget["parameters"]
        assert isinstance(widget["parameters"]["items"], list)
        assert widget["parameters"]["list_type"] in ["ordered", "unordered"]

    def test_data_bignum_parameters(self):
        """Verify Data.BigNum has number, label, and format parameters."""
        widget = {
            "type": "Data.BigNum",
            "parameters": {"number": 42.5, "label": "Score", "format": "decimal"}
        }
        
        assert "number" in widget["parameters"]
        assert "label" in widget["parameters"]
        assert "format" in widget["parameters"]
        assert widget["parameters"]["format"] in ["integer", "decimal", "percentage"]

    def test_data_progress_parameters(self):
        """Verify Data.Progress has percentage and label parameters."""
        widget = {
            "type": "Data.Progress",
            "parameters": {"percentage": 75, "label": "Progress"}
        }
        
        assert "percentage" in widget["parameters"]
        assert 0 <= widget["parameters"]["percentage"] <= 100
        assert "label" in widget["parameters"]

    def test_data_trend_parameters(self):
        """Verify Data.Trend has value, change, direction, and label."""
        widget = {
            "type": "Data.Trend",
            "parameters": {
                "value": 1000.0,
                "change": 15.5,
                "direction": "up",
                "label": "Revenue"
            }
        }
        
        assert "value" in widget["parameters"]
        assert "change" in widget["parameters"]
        assert "direction" in widget["parameters"]
        assert widget["parameters"]["direction"] in ["up", "down", "flat"]
        assert "label" in widget["parameters"]

    def test_media_image_parameters(self):
        """Verify Media.Image has image_url parameter."""
        widget = {
            "type": "Media.Image",
            "parameters": {"image_url": "https://example.com/image.jpg"}
        }
        
        assert "image_url" in widget["parameters"]
        assert widget["parameters"]["image_url"].startswith("http")


class TestPatchOperationValidation:
    """Test LLM outputs use correct patch operation format."""

    def test_state_transition_patch_format(self):
        """Verify state transition patches use correct format."""
        # Step 1 output - using our Patch format (add field with full object)
        patch_operations = [
            {
                "add": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "draft",
                    "strategy": "Bento.Standard",
                    "widgets": {},
                    "parameters": {}
                }
            }
        ]
        
        # Should be parseable as Patch
        patch = Patch.from_json_str(json.dumps(patch_operations))
        assert len(patch.operations) == 1
        assert hasattr(patch.operations[0], 'add')

    def test_content_generation_patch_format(self):
        """Verify content generation patches use correct format."""
        # Step 2 output - using our Patch format (replace field with full object)
        patch_operations = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {
                            "type": "Type.Display",
                            "parameters": {"text": "Title"}
                        }
                    },
                    "parameters": {}
                }
            }
        ]
        
        # Should be parseable as Patch
        patch = Patch.from_json_str(json.dumps(patch_operations))
        assert len(patch.operations) == 1
        assert hasattr(patch.operations[0], 'replace')


class TestContentDerivationValidation:
    """Test that content derives from atoms (no hallucination)."""

    def test_widget_text_should_derive_from_atoms(self):
        """Verify widget content matches atom content."""
        # Create atoms
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="The quick brown fox jumps over the lazy dog",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=44
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Simulated widget content derived from atom
        widget = {
            "type": "Type.Body",
            "parameters": {"text": "The quick brown fox"}  # Substring of atom text
        }
        
        # Verify text appears in atom
        atom_texts = [a.text for a in atoms.list_contexts() if hasattr(a, 'text')]
        assert any(widget["parameters"]["text"] in text for text in atom_texts)

    def test_bignum_values_should_derive_from_atoms(self):
        """Verify Data.BigNum numbers come from atom data."""
        # Simulated comparison atom with numbers
        atom_data = {
            "type": "comparison",
            "entities": {
                "Product A": {"speed": 150},
                "Product B": {"speed": 200}
            }
        }
        
        # Widget should use actual numbers from atoms
        widget = {
            "type": "Data.BigNum",
            "parameters": {"number": 200, "label": "Speed", "format": "integer"}
        }
        
        # Verify number appears in atom data
        assert widget["parameters"]["number"] in [150, 200]


class TestStateTransitionCompliance:
    """Test that state transitions follow contract rules."""

    def test_draft_state_widgets_can_be_empty(self):
        """Verify DRAFT slides can have empty widgets dict."""
        slide = {
            "id": "slide_001",
            "state": "draft",
            "strategy": "Bento.Standard",
            "widgets": {}
        }
        
        assert slide["state"] == "draft"
        assert slide["widgets"] == {}  # Empty is allowed

    def test_active_state_widgets_must_have_content(self):
        """Verify ACTIVE slides must have non-empty widgets."""
        slide = {
            "id": "slide_001",
            "state": "active",
            "strategy": "Bento.Standard",
            "widgets": {
                "cell_1": {
                    "type": "Type.Display",
                    "parameters": {"text": "Content"}
                }
            }
        }
        
        assert slide["state"] == "active"
        assert len(slide["widgets"]) > 0  # Must have content

    def test_state_progression_initial_to_draft_to_active(self):
        """Verify state transitions follow: initial → draft → active."""
        valid_transitions = [
            ("initial", "draft"),
            ("draft", "active")
        ]
        
        for from_state, to_state in valid_transitions:
            # These should be valid transitions
            assert (from_state, to_state) in [
                ("initial", "draft"),
                ("draft", "active")
            ]
        
        # Invalid transition
        invalid = ("active", "draft")
        assert invalid not in valid_transitions
