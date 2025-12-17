"""Integration tests for layout generation with two-step process."""
import json
import pytest
from unittest.mock import patch, MagicMock

from src.generation.atom.collection import AtomCollection
from src.generation.atom.models import StatementAtom, ProcessAtom, ProcessStep
from src.generation.content.generator import generate_layout
from src.common.source import SourceReference
from src.common.slides import Slides
from src.utils.generation_config import GenerationConfig
from src.common.patchable_context_pydantic import Patch, AddOperation


class TestLayoutGeneratorTwoStepProcess:
    """Test two-step layout generation with mocked LLM."""

    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_creates_slides_in_two_steps(self, mock_llm):
        """Verify generate_layout calls LLM twice (state transition + content)."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test content",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=12
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Mock LLM responses
        # Step 1: State transition patch (creates draft slide)
        state_transition_patch = [
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
        
        # Step 2: Content generation patch (populates widgets + activates)
        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {
                            "type": "Type.Display",
                            "parameters": {"text": "Test content"}
                        }
                    },
                    "parameters": {}
                }
            }
        ]
        
        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]
        
        # Execute
        instruction = "Create 1 slide"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        slides = generate_layout(atoms, instruction, config, use_cache=False)
        
        # Verify
        assert mock_llm.call_count == 2  # Two LLM calls
        assert isinstance(slides, Slides)
        assert len(slides) == 1
        
        slide = slides.get("slide_001")
        assert slide is not None
        assert slide.state == "active"
        assert slide.strategy == "Bento.Standard"
        assert "cell_1" in slide.widgets

    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_first_step_creates_draft_slides(self, mock_llm):
        """Verify step 1 creates slides in draft state."""
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Content",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=7
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Mock step 1 and 2 responses
        state_transition_patch = [
            {
                "add": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "draft",
                    "strategy": "Swiss.Poster",
                    "widgets": {},
                    "parameters": {}
                }
            }
        ]
        
        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Swiss.Poster",
                    "widgets": {},
                    "parameters": {}
                }
            }
        ]
        
        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]
        
        instruction = "Create presentation"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.2,
            max_tokens=2000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        slides = generate_layout(atoms, instruction, config, use_cache=False)
        
        # Verify first call created draft slides
        assert slides.get("slide_001").strategy == "Swiss.Poster"

    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_second_step_populates_content(self, mock_llm):
        """Verify step 2 populates widgets and activates slides."""
        atoms = AtomCollection(id="atoms_001")
        atom = ProcessAtom(
            id="proc_001",
            rank=1,
            title="Process",
            steps=[ProcessStep(order=1, text="Step 1", dependencies=[])],
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=7
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        state_transition_patch = [
            {
                "add": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "draft",
                    "strategy": "Focus.Solar_System",
                    "widgets": {},
                    "parameters": {}
                }
            }
        ]
        
        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Focus.Solar_System",
                    "widgets": {
                        "center": {
                            "type": "Type.Heading",
                            "parameters": {"text": "Process", "level": 1}
                        },
                        "satellite_1": {
                            "type": "Type.Body",
                            "parameters": {"text": "Step 1"}
                        }
                    },
                    "parameters": {}
                }
            }
        ]
        
        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]
        
        instruction = "Show process"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=6000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        slides = generate_layout(atoms, instruction, config, use_cache=False)
        
        # Verify content was populated
        slide = slides.get("slide_001")
        assert slide.state == "active"
        assert len(slide.widgets) == 2
        assert slide.widgets["center"]["parameters"]["text"] == "Process"

    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_with_multiple_slides(self, mock_llm):
        """Verify generation handles multiple slides correctly."""
        atoms = AtomCollection(id="atoms_001")
        for i in range(3):
            atom = StatementAtom(
                id=f"stmt_{i:03d}",
                rank=i+1,
                text=f"Content {i}",
                source_ref=SourceReference(
                    source_id="src_001",
                    file_path="/test.txt",
                    offset=i*10,
                    length=9
                )
            )
            atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Create 3 draft slides
        state_transition_patch = [
            {
                "add": {
                    "id": f"slide_{i:03d}",
                    "rank": i+1,
                    "state": "draft",
                    "strategy": "Bento.Standard",
                    "widgets": {},
                    "parameters": {}
                }
            }
            for i in range(3)
        ]
        
        # Populate all 3 slides
        content_patch = [
            {
                "replace": {
                    "id": f"slide_{i:03d}",
                    "rank": i+1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {
                            "type": "Type.Body",
                            "parameters": {"text": f"Content {i}"}
                        }
                    },
                    "parameters": {}
                }
            }
            for i in range(3)
        ]
        
        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]
        
        instruction = "Create 3 slides"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=6000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        slides = generate_layout(atoms, instruction, config, use_cache=False)
        
        # Verify all slides created and activated
        assert len(slides) == 3
        for i in range(3):
            slide = slides.get(f"slide_{i:03d}")
            assert slide.state == "active"
            assert slide.widgets["cell_1"]["parameters"]["text"] == f"Content {i}"


class TestLayoutGeneratorValidation:
    """Test validation and error handling."""

    def test_generate_layout_empty_atoms_raises_error(self):
        """Verify empty atom collection raises ValueError."""
        atoms = AtomCollection(id="atoms_001")
        instruction = "Create slides"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        with pytest.raises(ValueError, match="empty|no atoms"):
            generate_layout(atoms, instruction, config, use_cache=False)

    def test_generate_layout_empty_instruction_raises_error(self):
        """Verify empty instruction raises ValueError."""
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Content",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=7
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        with pytest.raises(ValueError, match="empty|instruction"):
            generate_layout(atoms, "", config, use_cache=False)

    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_invalid_json_response_raises_error(self, mock_llm):
        """Verify invalid JSON response raises appropriate error."""
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Content",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=7
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Mock invalid JSON response
        mock_llm.return_value = "Not valid JSON"
        
        instruction = "Create slides"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        with pytest.raises(json.JSONDecodeError):
            generate_layout(atoms, instruction, config, use_cache=False)


class TestLayoutGeneratorCaching:
    """Test caching behavior."""

    @patch('src.generation.content.generator._cache.load')
    @patch('src.generation.content.generator._cache.save')
    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_checks_cache_when_enabled(self, mock_llm, mock_cache_save, mock_cache_load):
        """Verify cache is checked when use_cache=True."""
        # Setup mock cache to return None (cache miss)
        mock_cache_load.return_value = None
        
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Content",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=7
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Mock LLM responses
        state_patch = [{"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}]
        content_patch = [{"replace": {"id": "slide_001", "rank": 1, "state": "active", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}]
        
        mock_llm.side_effect = [json.dumps(state_patch), json.dumps(content_patch)]
        
        instruction = "Create slides"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        slides = generate_layout(atoms, instruction, config, use_cache=True)
        
        # Verify cache was checked
        assert mock_cache_load.called
        assert mock_cache_save.called  # Should also save to cache

    @patch('src.generation.content.generator.call_llm')
    def test_generate_layout_skips_cache_when_disabled(self, mock_llm):
        """Verify cache is skipped when use_cache=False."""
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Content",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=7
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))
        
        # Mock LLM responses
        state_patch = [{"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}]
        content_patch = [{"replace": {"id": "slide_001", "rank": 1, "state": "active", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}]
        
        mock_llm.side_effect = [json.dumps(state_patch), json.dumps(content_patch)]
        
        instruction = "Create slides"
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        
        # Should not raise cache-related errors
        slides = generate_layout(atoms, instruction, config, use_cache=False)
        assert len(slides) == 1
