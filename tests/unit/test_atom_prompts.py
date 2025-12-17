"""Tests for atom extraction prompts."""
import pytest
from src.common.source import Source
from src.generation.atom.prompts import (
    ATOM_EXTRACTION_SYSTEM_PROMPT,
    render_atom_extraction_prompt,
    get_atom_extraction_config
)


class TestAtomExtractionSystemPrompt:
    """Test system prompt for atom extraction."""
    
    def test_system_prompt_exists(self):
        """Verify system prompt is defined."""
        assert ATOM_EXTRACTION_SYSTEM_PROMPT is not None
        assert len(ATOM_EXTRACTION_SYSTEM_PROMPT) > 0
    
    def test_system_prompt_mentions_atom_types(self):
        """Verify system prompt describes all atom types."""
        prompt = ATOM_EXTRACTION_SYSTEM_PROMPT
        assert "StatementAtom" in prompt or "statement" in prompt.lower()
        assert "ProcessAtom" in prompt or "process" in prompt.lower()
        assert "ComparisonAtom" in prompt or "comparison" in prompt.lower()
    
    def test_system_prompt_mentions_json_output(self):
        """Verify system prompt requests JSON format."""
        prompt = ATOM_EXTRACTION_SYSTEM_PROMPT
        assert "JSON" in prompt or "json" in prompt


class TestAtomExtractionUserPrompt:
    """Test user prompt rendering for atom extraction."""
    
    def test_render_prompt_with_text_source(self):
        """Verify prompt rendering with plain text source."""
        source = Source(
            source_id="test_001",
            name="Test Document",
            file_path="/path/to/test.txt",
            content_type="text/plain",
            content="This is a test document with some content."
        )
        
        prompt = render_atom_extraction_prompt(source)
        
        assert prompt is not None
        assert len(prompt) > 0
        assert source.content in prompt
    
    def test_render_prompt_with_vtt_source(self):
        """Verify prompt rendering with VTT source."""
        vtt_content = """WEBVTT

00:00:00.000 --> 00:00:05.000
First caption line

00:00:05.000 --> 00:00:10.000
Second caption line"""
        
        source = Source(
            source_id="vtt_001",
            name="Video Transcript",
            file_path="/path/to/video.vtt",
            content_type="text/vtt",
            content=vtt_content
        )
        
        prompt = render_atom_extraction_prompt(source)
        
        assert prompt is not None
        assert vtt_content in prompt or "First caption" in prompt
    
    def test_prompt_includes_source_context(self):
        """Verify prompt includes source identification."""
        source = Source(
            source_id="ctx_001",
            name="Context Test",
            file_path="/test/path.txt",
            content_type="text/plain",
            content="Content for context test"
        )
        
        prompt = render_atom_extraction_prompt(source)
        
        # Prompt should reference source name or file for context
        assert source.name in prompt or source.file_path in prompt or source.source_id in prompt
    
    def test_prompt_with_empty_content_raises_error(self):
        """Verify empty content is caught during source creation."""
        with pytest.raises(Exception):  # Pydantic validation error
            Source(
                source_id="empty",
                name="Empty",
                file_path="/empty.txt",
                content_type="text/plain",
                content=""  # Should fail min_length validation
            )
    
    def test_prompt_requests_specific_structure(self):
        """Verify prompt asks for structured JSON output."""
        source = Source(
            source_id="struct_001",
            name="Structure Test",
            file_path="/test.txt",
            content_type="text/plain",
            content="Test content"
        )
        
        prompt = render_atom_extraction_prompt(source)
        
        # Should mention expected structure
        assert "atoms" in prompt.lower() or "list" in prompt.lower()


class TestAtomExtractionConfig:
    """Test GenerationConfig creation for atom extraction."""
    
    def test_get_default_config(self):
        """Verify default config for atom extraction."""
        config = get_atom_extraction_config()
        
        assert config is not None
        assert config.response_format == "json"
        assert config.temperature >= 0.0
        assert config.temperature <= 2.0
        assert config.max_tokens > 0
    
    def test_config_has_atom_system_prompt(self):
        """Verify config uses atom extraction system prompt."""
        config = get_atom_extraction_config()
        
        assert config.system_prompt == ATOM_EXTRACTION_SYSTEM_PROMPT
    
    def test_config_has_user_prompt_template(self):
        """Verify config includes user prompt template."""
        config = get_atom_extraction_config()
        
        assert config.user_prompt_template is not None
        assert "{content}" in config.user_prompt_template or "{source" in config.user_prompt_template
    
    def test_config_temperature_for_extraction(self):
        """Verify temperature is appropriate for structured extraction."""
        config = get_atom_extraction_config()
        
        # Extraction should use low temperature for consistency
        assert config.temperature <= 0.5
    
    def test_custom_temperature(self):
        """Verify custom temperature can be set."""
        config = get_atom_extraction_config(temperature=0.8)
        
        assert config.temperature == 0.8
    
    def test_custom_max_tokens(self):
        """Verify custom max_tokens can be set."""
        config = get_atom_extraction_config(max_tokens=2000)
        
        assert config.max_tokens == 2000


class TestPromptIntegration:
    """Test prompt rendering with actual config."""
    
    def test_full_prompt_generation_flow(self):
        """Verify complete prompt generation from source to config."""
        source = Source(
            source_id="flow_001",
            name="Flow Test",
            file_path="/flow.txt",
            content_type="text/plain",
            content="Step 1: Initialize. Step 2: Process. Step 3: Finalize."
        )
        
        config = get_atom_extraction_config()
        user_prompt = render_atom_extraction_prompt(source)
        
        # Config should have both prompts ready
        assert config.system_prompt is not None
        assert user_prompt is not None
        
        # User prompt should contain content
        assert "Initialize" in user_prompt
        assert "Process" in user_prompt
        assert "Finalize" in user_prompt
