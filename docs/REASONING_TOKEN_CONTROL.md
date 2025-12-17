# Reasoning Token Control

## Overview

The system supports limiting reasoning tokens for reasoning-capable models (like o1-preview, o1-mini, o3, or future reasoning models). By default, this is **disabled** to ensure compatibility with all models.

## What are Reasoning Tokens?

Reasoning models (like OpenAI's o1 series) use internal "reasoning tokens" to think through problems before generating the final output. These tokens:
- Don't appear in the response
- Count toward the total token budget
- Can be substantial (e.g., 2000+ tokens)
- Improve answer quality but increase cost and latency

## Configuration

### Default Behavior (Disabled)

By default, `max_reasoning_tokens` is `None`, meaning:
- No limit on reasoning tokens
- Works with all models (reasoning and non-reasoning)
- Model uses as many reasoning tokens as it needs

### Enabling Reasoning Token Limits

To limit reasoning tokens to 2000 (or any value):

**Option 1: Per-Config (Recommended)**

```python
from src.utils.generation_config import GenerationConfig

config = GenerationConfig(
    model="o1-preview",
    temperature=0.7,
    max_tokens=32000,
    max_reasoning_tokens=2000,  # Limit reasoning to 2000 tokens
    system_prompt="...",
    user_prompt_template="...",
    response_format="json"
)
```

**Option 2: Update Default Configs**

Edit the config creation functions in:
- `src/generation/atom/prompts.py::get_atom_extraction_config()`
- `src/generation/content/prompts.py::get_state_transition_config()`
- `src/generation/content/prompts.py::get_content_generation_config()`
- `src/generation/intent/detector.py::_get_intent_detection_config()`

Example:
```python
def get_content_generation_config() -> GenerationConfig:
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.7,
        max_tokens=32000,
        max_reasoning_tokens=2000,  # Add this line
        system_prompt=CONTENT_GENERATION_SYSTEM_PROMPT,
        user_prompt_template=""
    )
```

## Supported Models

The `max_reasoning_tokens` parameter is supported by:
- ✅ `o1-preview`
- ✅ `o1-mini`
- ✅ `o3-mini` (when available)
- ❌ `gpt-4-turbo` (not a reasoning model)
- ❌ `gpt-4o` (not a reasoning model)
- ❌ `gpt-3.5-turbo` (not a reasoning model)

For non-reasoning models, the parameter is ignored gracefully.

## Error Handling

The system automatically handles unsupported models:

1. If a model doesn't support `max_reasoning_tokens`, it logs a warning:
   ```
   Model gpt-5.1 does not support max_reasoning_tokens parameter, retrying without it
   ```

2. The request is retried without the parameter
3. Generation continues normally

## Why Control Reasoning Tokens?

### Benefits of Limiting:
- **Cost Control**: Reasoning tokens cost the same as output tokens
- **Latency**: Fewer reasoning tokens = faster responses
- **Predictability**: Known token budget for cost estimation

### When to Limit:
- Simple tasks that don't need deep reasoning
- Cost-sensitive applications
- Real-time/low-latency requirements

### When NOT to Limit:
- Complex problems requiring deep analysis
- Quality is more important than speed/cost
- Using non-reasoning models (limit has no effect)

## Example: Testing with Reasoning Limit

```bash
# 1. Set environment variable to use reasoning model
export AZURE_OPENAI_DEPLOYMENT="o1-preview"

# 2. Update config in code to enable reasoning limit
# Edit src/generation/content/prompts.py:
#   max_reasoning_tokens=2000

# 3. Generate slides
python -m cli --source data/context/career_talk.txt \
  --user-instruction "Create slides" \
  --output output/test.html --verbose

# 4. Check token usage in logs
# You'll see reasoning token count in the output
```

## Token Budget Planning

For reasoning models with `max_tokens=32000` and `max_reasoning_tokens=2000`:
- **Reasoning**: Up to 2000 tokens (internal thinking)
- **Output**: Up to 30000 tokens (actual response)
- **Total**: Max 32000 tokens

Without reasoning limit:
- **Reasoning**: Variable (could be 10K+)
- **Output**: Remaining budget
- **Total**: Max 32000 tokens

## Current Configuration

All generation configs currently have:
```python
max_reasoning_tokens=None  # Disabled by default
```

To enable globally, update the default in `src/utils/generation_config.py`:
```python
max_reasoning_tokens: int | None = Field(
    default=2000,  # Change from None to 2000
    description="..."
)
```
