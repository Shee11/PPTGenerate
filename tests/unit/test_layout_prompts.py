"""Unit tests for layout generation prompt templates."""
import json
import pytest

from src.generation.atom.collection import AtomCollection
from src.generation.atom.models import StatementAtom, ProcessAtom, ComparisonAtom, ProcessStep
from src.generation.content.prompts import (
    STATE_TRANSITION_SYSTEM_PROMPT,
    CONTENT_GENERATION_SYSTEM_PROMPT,
    render_state_transition_prompt,
    render_content_generation_prompt,
    get_state_transition_config,
    get_content_generation_config,
)
from src.common.source import SourceReference
from src.utils.generation_config import GenerationConfig
from src.common.patchable_context_pydantic import Patch, AddOperation


class TestStateTransitionPrompt:
    """Test state transition prompt template."""

    def test_system_prompt_exists(self):
        """State transition system prompt is defined."""
        assert STATE_TRANSITION_SYSTEM_PROMPT
        assert isinstance(STATE_TRANSITION_SYSTEM_PROMPT, str)
        assert len(STATE_TRANSITION_SYSTEM_PROMPT) > 100
    
    def test_system_prompt_mentions_json_patch(self):
        """System prompt references JSON Patch format."""
        assert "JSON Patch" in STATE_TRANSITION_SYSTEM_PROMPT or "json patch" in STATE_TRANSITION_SYSTEM_PROMPT.lower()
    
    def test_system_prompt_mentions_draft_state(self):
        """System prompt mentions draft state."""
        assert "draft" in STATE_TRANSITION_SYSTEM_PROMPT.lower()
    
    def test_system_prompt_forbids_content_population(self):
        """System prompt explicitly forbids populating widget content in step 1."""
        assert "do not" in STATE_TRANSITION_SYSTEM_PROMPT.lower() or "must not" in STATE_TRANSITION_SYSTEM_PROMPT.lower()
        assert "widget" in STATE_TRANSITION_SYSTEM_PROMPT.lower() or "content" in STATE_TRANSITION_SYSTEM_PROMPT.lower()
    
    def test_render_state_transition_prompt_basic(self):
        """Render state transition user prompt with atoms and instruction."""
        atom_collection = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test statement",
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=0,
                length=10
            )
        )
        atom_collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        instruction = "Create 3 slides about testing"
        
        prompt = render_state_transition_prompt(atom_collection, instruction)
        
        assert isinstance(prompt, str)
        assert "Create 3 slides about testing" in prompt
        assert "stmt_001" in prompt  # atom IDs should appear
        assert "Test statement" in prompt  # atom content should appear
    
    def test_render_state_transition_prompt_with_multiple_atom_types(self):
        """User prompt includes all atom types (statement, process, comparison)."""
        atom_collection = AtomCollection(id="atoms_001")
        
        atom1 = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Statement text",
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=0,
                length=10
            )
        )
        
        atom2 = ProcessAtom(
            id="proc_001",
            rank=2,
            title="Process title",
            steps=[ProcessStep(order=1, text="Step 1", dependencies=[])],
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=20,
                length=10
            )
        )
        
        atom3 = ComparisonAtom(
            id="comp_001",
            rank=3,
            dimensions=["speed", "accuracy"],
            entities={"A": {"speed": "fast", "accuracy": "high"}, "B": {"speed": "slow", "accuracy": "low"}},
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=40,
                length=10
            )
        )
        
        atom_collection.patch(Patch(operations=[
            AddOperation(add=atom1),
            AddOperation(add=atom2),
            AddOperation(add=atom3)
        ]))
        
        instruction = "Create presentation"
        prompt = render_state_transition_prompt(atom_collection, instruction)
        
        # All atom types should be represented
        assert "stmt_001" in prompt
        assert "proc_001" in prompt
        assert "comp_001" in prompt
        assert "Statement text" in prompt
        assert "Process title" in prompt
    
    def test_render_state_transition_prompt_empty_collection_raises_error(self):
        """Rendering prompt with empty atom collection raises ValueError."""
        atom_collection = AtomCollection(id="atoms_001")
        instruction = "Create slides"
        
        with pytest.raises(ValueError, match="empty|no atoms"):
            render_state_transition_prompt(atom_collection, instruction)
    
    def test_render_state_transition_prompt_empty_instruction_raises_error(self):
        """Rendering prompt with empty instruction raises ValueError."""
        atom_collection = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=0,
                length=4
            )
        )
        atom_collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        with pytest.raises(ValueError, match="empty|instruction"):
            render_state_transition_prompt(atom_collection, "")
    
    def test_get_state_transition_config(self):
        """State transition generation config has appropriate parameters."""
        config = get_state_transition_config()
        
        assert isinstance(config, GenerationConfig)
        assert config.temperature <= 0.3  # Should be deterministic
        assert config.max_tokens >= 1000  # Need space for JSON patches
        assert config.model  # Model specified


class TestContentGenerationPrompt:
    """Test content generation prompt template."""

    def test_system_prompt_exists(self):
        """Content generation system prompt is defined."""
        assert CONTENT_GENERATION_SYSTEM_PROMPT
        assert isinstance(CONTENT_GENERATION_SYSTEM_PROMPT, str)
        assert len(CONTENT_GENERATION_SYSTEM_PROMPT) > 100
    
    def test_system_prompt_lists_supported_widgets(self):
        """System prompt lists supported widget types."""
        prompt_lower = CONTENT_GENERATION_SYSTEM_PROMPT.lower()
        assert "type.display" in prompt_lower or "display" in prompt_lower
        assert "type.heading" in prompt_lower or "heading" in prompt_lower
        assert "data.bignum" in prompt_lower or "bignum" in prompt_lower
    
    def test_system_prompt_lists_supported_presets(self):
        """System prompt lists supported preset attributes."""
        prompt_lower = CONTENT_GENERATION_SYSTEM_PROMPT.lower()
        assert "surface" in prompt_lower
        assert "shape" in prompt_lower
        assert "fill" in prompt_lower
    
    def test_system_prompt_mentions_active_state(self):
        """System prompt mentions setting slides to active state."""
        assert "active" in CONTENT_GENERATION_SYSTEM_PROMPT.lower()
    
    def test_system_prompt_warns_against_hallucination(self):
        """System prompt warns against hallucinating facts not in atoms."""
        prompt_lower = CONTENT_GENERATION_SYSTEM_PROMPT.lower()
        assert ("derive" in prompt_lower or "based on" in prompt_lower or "from atom" in prompt_lower)
    
    def test_render_content_generation_prompt_basic(self):
        """Render content generation user prompt with draft slides and atoms."""
        from src.common.slides import Slides
        from src.common.slide import Slide
        
        # Create draft slide collection
        slides = Slides(id="slides_001")
        draft_slide = Slide(
            id="slide_001",
            rank=1,
            state="draft",
            strategy="Bento.Standard",
            widgets={}
        )
        slides.patch(Patch(operations=[
            AddOperation(add=draft_slide)
        ]))
        
        # Create atom collection
        atom_collection = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test content",
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=0,
                length=12
            )
        )
        atom_collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        instruction = "Populate slides with atom content"
        
        prompt = render_content_generation_prompt(slides, atom_collection, instruction)
        
        assert isinstance(prompt, str)
        assert "Populate slides with atom content" in prompt
        assert "slide_001" in prompt  # Draft slide IDs should appear
        assert "Bento.Standard" in prompt  # Strategy should appear
        assert "stmt_001" in prompt  # Atom IDs should appear
        assert "Test content" in prompt  # Atom content should appear
    
    def test_render_content_generation_prompt_empty_slides_raises_error(self):
        """Rendering prompt with empty slide collection raises ValueError."""
        from src.common.slides import Slides
        
        slides = Slides(id="slides_001")
        atom_collection = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=0,
                length=4
            )
        )
        atom_collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        instruction = "Populate slides"
        
        with pytest.raises(ValueError, match="empty|no slides"):
            render_content_generation_prompt(slides, atom_collection, instruction)
    
    def test_render_content_generation_prompt_slides_not_in_draft_state_raises_error(self):
        """Rendering prompt with non-draft slides raises ValueError."""
        from src.common.slides import Slides
        from src.common.slide import Slide
        
        slides = Slides(id="slides_001")
        active_slide = Slide(
            id="slide_001",
            rank=1,
            state="active",  # Wrong state!
            strategy="Bento.Standard",
            widgets={}
        )
        slides.patch(Patch(operations=[
            AddOperation(add=active_slide)
        ]))
        
        atom_collection = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="Test",
            source_ref=SourceReference(
                source_id="source_001",
                file_path="/test.txt",
                offset=0,
                length=4
            )
        )
        atom_collection.patch(Patch(operations=[AddOperation(add=atom)]))
        
        instruction = "Populate slides"
        
        with pytest.raises(ValueError, match="draft|state"):
            render_content_generation_prompt(slides, atom_collection, instruction)
    
    def test_get_content_generation_config(self):
        """Content generation config has appropriate parameters."""
        config = get_content_generation_config()
        
        assert isinstance(config, GenerationConfig)
        assert config.temperature >= 0.5  # More creative than state transition
        assert config.max_tokens >= 4000  # Need space for widget content
        assert config.model  # Model specified


class TestPromptIntegration:
    """Test integration between prompt templates and configs."""

    def test_state_transition_config_matches_prompt_requirements(self):
        """State transition config model matches system prompt expectations."""
        config = get_state_transition_config()
        
        # Prompt expects JSON Patch output - config should support JSON mode or structured output
        assert config.model  # Should specify model capable of JSON output
    
    def test_content_generation_config_matches_prompt_requirements(self):
        """Content generation config model matches system prompt expectations."""
        config = get_content_generation_config()
        
        # Prompt expects widget population - config should support detailed output
        assert config.model
        assert config.max_tokens >= 4000  # Widget content can be verbose
