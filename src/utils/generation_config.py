"""Generation configuration model."""
from typing import Literal, Any
from pydantic import BaseModel, Field


class GenerationConfig(BaseModel):
    """
    Configuration for LLM generation requests.
    
    Attributes:
        model: Azure OpenAI deployment name (e.g., "gpt-4-turbo")
        temperature: Sampling temperature between 0 and 2
        max_tokens: Maximum tokens in response
        system_prompt: System message defining LLM behavior
        user_prompt_template: Template for user messages (may contain placeholders)
        response_format: Expected response format ("json", "json_schema", or "text")
        json_schema: JSON schema definition for structured output (used when response_format="json_schema")
        max_reasoning_tokens: Maximum reasoning tokens for reasoning models (None to disable)
    """
    
    model: str = Field(..., description="Azure OpenAI deployment name")
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0=deterministic, 2=very random)"
    )
    max_tokens: int = Field(
        default=4000,
        gt=0,
        description="Maximum tokens in response"
    )
    max_reasoning_tokens: int | None = Field(
        default=None,
        description="Maximum reasoning tokens for reasoning models (default: None/disabled, set to 2000 if model supports it)"
    )
    system_prompt: str = Field(..., description="System message for LLM")
    user_prompt_template: str = Field(
        ...,
        description="User prompt template (may contain {placeholders})"
    )
    response_format: Literal["json", "json_schema", "text"] = Field(
        default="json",
        description="Expected response format"
    )
    json_schema: dict[str, Any] | None = Field(
        default=None,
        description="JSON schema for structured output (required when response_format='json_schema')"
    )
    
    class Config:
        """Pydantic configuration."""
        frozen = False  # Allow modification after creation
        validate_assignment = True  # Validate on attribute assignment
