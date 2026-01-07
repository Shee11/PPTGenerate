"""LLM client utilities for Azure OpenAI integration."""
import os
import time
import json
from datetime import datetime
from functools import lru_cache
from typing import Optional
from openai import AzureOpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@lru_cache(maxsize=1)
def get_llm_client() -> AzureOpenAI:
    """
    Get singleton Azure OpenAI client instance.

    Auth methods (in priority order):
    1) API key via `AZURE_OPENAI_API_KEY`
    2) Azure CLI credential via `az login`
    
    Returns:
        AzureOpenAI: Configured client instance
        
    Raises:
        ValueError: If required environment variables are missing
    """
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    if not endpoint:
        raise ValueError(
            "Missing required environment variable: "
            "AZURE_OPENAI_ENDPOINT must be set"
        )
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if api_key:
        return AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )

    credential = AzureCliCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default",
    )

    return AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version=api_version,
    )


def call_llm(
    system_prompt: str,
    user_prompt: str,
    deployment: str,
    temperature: float = 0.7,
    max_tokens: int = 4000,
    response_format: Optional[str] = None,
    json_schema: Optional[dict] = None,
    max_retries: int = 3,
    initial_retry_delay: float = 1.0,
    max_reasoning_tokens: Optional[int] = None
) -> str:
    """
    Call LLM with retry logic and exponential backoff.
    
    Args:
        system_prompt: System message defining LLM behavior
        user_prompt: User message with actual request
        deployment: Azure OpenAI deployment name
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens in response (total for reasoning + output)
        response_format: Optional response format ("json" for JSON mode, "json_schema" for structured output)
        json_schema: JSON schema dict for structured output (required when response_format="json_schema")
        max_retries: Maximum number of retry attempts
        initial_retry_delay: Initial delay in seconds before first retry
        max_reasoning_tokens: Maximum reasoning tokens for reasoning models (default: None/disabled)
                              Set to 2000 if your model supports it (o1-preview, o1-mini, o3, etc.)
        
    Returns:
        str: LLM response content
        
    Raises:
        Exception: If API call fails after all retries
    """
    client = get_llm_client()
    
    # Prepare API call parameters
    params = {
        "model": deployment,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        # Use max_completion_tokens for newer models (gpt-4o, gpt-5), max_tokens for older
        "max_completion_tokens": max_tokens
    }
    
    # Add reasoning token limit if specified (for reasoning models like gpt-5.x, o1, o3)
    # Only add if not None - some models/API versions don't support this parameter
    if max_reasoning_tokens is not None:
        params["max_reasoning_tokens"] = max_reasoning_tokens
    
    # Add JSON response format if requested
    if response_format == "json_schema" and json_schema is not None:
        params["response_format"] = {
            "type": "json_schema",
            "json_schema": json_schema
        }
    elif response_format == "json":
        params["response_format"] = {"type": "json_object"}
    
    # Retry loop with exponential backoff
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            trace_file = os.getenv("LLM_TRACE_FILE")
            trace_step = os.getenv("LLM_TRACE_STEP")
            if trace_file:
                try:
                    sent_record = {
                        "ts": datetime.utcnow().isoformat() + "Z",
                        "step": trace_step,
                        "event": "sent",
                        "deployment": deployment,
                        "attempt": attempt,
                        "system_prompt": system_prompt,
                        "user_prompt": user_prompt,
                        "response_format": response_format,
                    }
                    with open(trace_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(sent_record, ensure_ascii=False) + "\n")
                except Exception:
                    # Tracing must never break generation.
                    pass

            response = client.chat.completions.create(**params)
            content = response.choices[0].message.content
            
            if content is None or content.strip() == "":
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"LLM returned empty content. Finish reason: {response.choices[0].finish_reason}")
                logger.error(f"Full response: {response}")
                raise ValueError(f"LLM returned empty content. Finish reason: {response.choices[0].finish_reason}")
            
            if trace_file:
                try:
                    record = {
                        "ts": datetime.utcnow().isoformat() + "Z",
                        "step": trace_step,
                        "event": "response",
                        "deployment": deployment,
                        "attempt": attempt,
                        "response": content,
                        "response_format": response_format,
                    }
                    with open(trace_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")
                except Exception:
                    # Tracing must never break generation.
                    pass

            return content
        except TypeError as e:
            # If max_reasoning_tokens is not supported, retry without it
            if "max_reasoning_tokens" in str(e) and "max_reasoning_tokens" in params:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Model {deployment} does not support max_reasoning_tokens parameter, retrying without it")
                params.pop("max_reasoning_tokens")
                continue
            last_exception = e
            if attempt < max_retries:
                delay = initial_retry_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                raise last_exception
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                # Calculate exponential backoff delay
                delay = initial_retry_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                # Max retries exceeded, raise the last exception
                raise last_exception
