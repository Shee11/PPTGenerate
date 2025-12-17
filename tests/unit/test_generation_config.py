"""Tests for GenerationConfig Pydantic model."""
import pytest
from pydantic import ValidationError
from src.utils.generation_config import GenerationConfig


class TestGenerationConfig:
    """Test GenerationConfig validation and defaults."""
    
    def test_minimal_valid_config(self):
        """Verify minimal valid configuration with required fields only."""
        config = GenerationConfig(
            model="gpt-4-turbo",
            system_prompt="You are a helpful assistant",
            user_prompt_template="Process this: {content}"
        )
        
        assert config.model == "gpt-4-turbo"
        assert config.temperature == 0.7  # Default
        assert config.max_tokens == 4000  # Default
        assert config.response_format == "json"  # Default
    
    def test_full_config_with_all_fields(self):
        """Verify configuration with all fields specified."""
        config = GenerationConfig(
            model="gpt-4",
            temperature=0.2,
            max_tokens=2000,
            system_prompt="Custom system prompt",
            user_prompt_template="Template: {input}",
            response_format="text"
        )
        
        assert config.model == "gpt-4"
        assert config.temperature == 0.2
        assert config.max_tokens == 2000
        assert config.response_format == "text"
    
    def test_temperature_validation_bounds(self):
        """Verify temperature must be between 0 and 2."""
        # Valid temperatures
        GenerationConfig(
            model="gpt-4",
            system_prompt="Test",
            user_prompt_template="Test",
            temperature=0.0
        )
        GenerationConfig(
            model="gpt-4",
            system_prompt="Test",
            user_prompt_template="Test",
            temperature=2.0
        )
        
        # Invalid temperatures
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                system_prompt="Test",
                user_prompt_template="Test",
                temperature=-0.1
            )
        
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                system_prompt="Test",
                user_prompt_template="Test",
                temperature=2.1
            )
    
    def test_max_tokens_validation(self):
        """Verify max_tokens must be positive."""
        # Valid max_tokens
        GenerationConfig(
            model="gpt-4",
            system_prompt="Test",
            user_prompt_template="Test",
            max_tokens=1
        )
        
        # Invalid max_tokens
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                system_prompt="Test",
                user_prompt_template="Test",
                max_tokens=0
            )
        
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                system_prompt="Test",
                user_prompt_template="Test",
                max_tokens=-100
            )
    
    def test_response_format_validation(self):
        """Verify response_format accepts only 'json' or 'text'."""
        # Valid formats
        GenerationConfig(
            model="gpt-4",
            system_prompt="Test",
            user_prompt_template="Test",
            response_format="json"
        )
        GenerationConfig(
            model="gpt-4",
            system_prompt="Test",
            user_prompt_template="Test",
            response_format="text"
        )
        
        # Invalid format
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                system_prompt="Test",
                user_prompt_template="Test",
                response_format="xml"
            )
    
    def test_required_fields_validation(self):
        """Verify required fields raise ValidationError when missing."""
        # Missing model
        with pytest.raises(ValidationError):
            GenerationConfig(
                system_prompt="Test",
                user_prompt_template="Test"
            )
        
        # Missing system_prompt
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                user_prompt_template="Test"
            )
        
        # Missing user_prompt_template
        with pytest.raises(ValidationError):
            GenerationConfig(
                model="gpt-4",
                system_prompt="Test"
            )
    
    def test_prompt_template_placeholders(self):
        """Verify user_prompt_template can contain placeholders."""
        config = GenerationConfig(
            model="gpt-4",
            system_prompt="Test",
            user_prompt_template="Extract atoms from: {content}\n\nInstructions: {instructions}"
        )
        
        assert "{content}" in config.user_prompt_template
        assert "{instructions}" in config.user_prompt_template
