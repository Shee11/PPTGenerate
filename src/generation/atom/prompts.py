"""Prompts for atom extraction from source content."""
import os
from src.common.source import Source
from src.utils.generation_config import GenerationConfig


# JSON Schema for structured output - defines exact atom structure
ATOM_EXTRACTION_SCHEMA = {
    "name": "atom_extraction_response",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "abstract": {
                "type": "string",
                "description": "2-3 sentence summary of the source content"
            },
            "atoms": {
                "type": "array",
                "description": "Array of extracted atoms",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Unique identifier (e.g., 'fact_001', 'stat_001', 'quote_001')"
                        },
                        "abstract": {
                            "type": "string",
                            "description": "One-line summary of this atom (max 100 chars, e.g., 'John Smith is a Google engineer' or 'Latency improved by 50%')"
                        },
                        "type": {
                            "type": "string",
                            "enum": ["BIO", "FACT", "STAT", "QUOTE", "TENSION", "CONCEPT", "VISUAL"],
                            "description": "Atom type tag"
                        },
                        "rank": {
                            "type": "integer",
                            "description": "Importance rank (1=most important)"
                        },
                        "text": {
                            "type": "string",
                            "description": "Main text content (for FACT, TENSION, CONCEPT). Use empty string for others."
                        },
                        "name": {
                            "type": "string",
                            "description": "Person/entity name for BIO atoms. Use empty string for non-BIO."
                        },
                        "role": {
                            "type": "string",
                            "description": "Role/title for BIO atoms. Use empty string for non-BIO."
                        },
                        "credentials": {
                            "type": "string",
                            "description": "Background/achievements for BIO atoms. Use empty string for non-BIO."
                        },
                        "affiliation": {
                            "type": "string",
                            "description": "Company/organization for BIO atoms. Use empty string for non-BIO."
                        },
                        "description": {
                            "type": "string",
                            "description": "Visual description (for VISUAL type). Use empty string for non-VISUAL."
                        },
                        "category": {
                            "type": "string",
                            "description": "Category for FACT atoms (e.g., definition, architecture, status, context). Use empty string for non-FACT."
                        },
                        "value": {
                            "type": "string",
                            "description": "Numeric value for STAT atoms (e.g., '50%', '200ms', '3x'). Use empty string for non-STAT."
                        },
                        "label": {
                            "type": "string",
                            "description": "Label for STAT atoms (e.g., 'Latency Reduction'). Use empty string for non-STAT."
                        },
                        "quote": {
                            "type": "string",
                            "description": "Verbatim quote for QUOTE atoms. Use empty string for non-QUOTE."
                        },
                        "attribution": {
                            "type": "string",
                            "description": "Attribution for QUOTE atoms (who said it). Use empty string if not applicable."
                        },
                        "context": {
                            "type": "string",
                            "description": "Context for STAT or QUOTE atoms. Use empty string if not applicable."
                        },
                        "tension_type": {
                            "type": "string",
                            "description": "Type for TENSION atoms (e.g., problem, contradiction, trade-off). Use empty string for non-TENSION."
                        },
                        "resolution_hint": {
                            "type": "string",
                            "description": "Optional resolution hint for TENSION atoms. Use empty string if not applicable."
                        },
                        "concept_type": {
                            "type": "string",
                            "description": "Type for CONCEPT atoms (e.g., solution, insight, method). Use empty string for non-CONCEPT."
                        },
                        "supporting_facts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "IDs of supporting FACT atoms for CONCEPT atoms. Use empty array for non-CONCEPT."
                        },
                        "visual_category": {
                            "type": "string",
                            "description": "Category for VISUAL atoms (e.g., metaphor, demo, screenshot). Use empty string for non-VISUAL."
                        },
                        "related_atom": {
                            "type": "string",
                            "description": "ID of related atom for VISUAL atoms. Use empty string if not applicable."
                        },
                        "visual": {
                            "type": "string",
                            "description": "Suggested visual representation (e.g., chart, diagram, big-number, quote-card, code, screenshot, photo, icon, timeline, comparison-table, flow, architecture, before-after, list, table, graph, none)"
                        },
                        "source_ref": {
                            "type": "object",
                            "description": "Reference to source location",
                            "properties": {
                                "source_id": {"type": "string"},
                                "file_path": {"type": "string"},
                                "offset": {"type": "integer"},
                                "length": {"type": "integer"}
                            },
                            "required": ["source_id", "file_path", "offset", "length"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["id", "abstract", "type", "rank", "text", "name", "role", "credentials", "affiliation", "description", "category", "value", "label", "quote", "attribution", "context", "tension_type", "resolution_hint", "concept_type", "supporting_facts", "visual_category", "related_atom", "visual", "source_ref"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["abstract", "atoms"],
        "additionalProperties": False
    }
}


ATOM_EXTRACTION_SYSTEM_PROMPT = """Extract "Narrative Atoms" from content for slide decks.

**Atom Types** (use exact: BIO, FACT, STAT, QUOTE, TENSION, CONCEPT, VISUAL):

| Type | Purpose | Key Fields |
|------|---------|------------|
| BIO | Identity/credentials | name, role, credentials, affiliation |
| FACT | Context/definitions | text, category (definition/architecture/status) |
| STAT | Numbers/metrics | value ("50%"), label ("Latency"), context |
| QUOTE | Verbatim phrases | quote, attribution, context |
| TENSION | Problems/conflicts | text, tension_type (problem/trade-off) |
| CONCEPT | Solutions/insights | text, concept_type (solution/insight) |
| VISUAL | Concrete imagery | description, visual_category |

**All atoms require**: id, abstract (1-line summary), type, rank (1=most important), visual (chart/big-number/quote-card/diagram/none), source_ref

**Rules**:
- Extract 5-20 atoms, ignore fluff
- STAT for numbers, QUOTE for memorable phrases, FACT for context
- Fill type-specific fields, use empty "" for others
- QUOTE: Use for impact phrases relevant to the audience/scenario
"""


def render_atom_extraction_prompt(source: Source, intent_guidance: str = "") -> str:
    """Render user prompt for atom extraction from a source.
    
    Args:
        source: Source content to extract atoms from
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted user prompt string with source content
        
    Raises:
        ValueError: If source content is empty
    """
    if not source.content or len(source.content.strip()) == 0:
        raise ValueError("Source content cannot be empty")
    
    prompt = f"""Extract knowledge atoms from the following source:

**Source ID**: {source.source_id}
**Source Name**: {source.name}
**File Path**: {source.file_path}
**Content Type**: {source.content_type}

**Content**:
{source.content}

---
"""
    
    # Add intent guidance if provided
    if intent_guidance:
        prompt += f"""
**Extraction Guidance**:
{intent_guidance}

Focus on atoms that align with the above guidance while extracting from the content.

---
"""
    
    prompt += """
Extract all relevant atoms (statements, processes, comparisons) from the content above.
Return a JSON object with:
1. "abstract": 2-3 sentence summary of the source content
2. "atoms": Array containing the extracted atoms"""
    
    return prompt


def get_atom_extraction_config(
    temperature: float = 0.2,
    max_tokens: int = 64000  # Increased for models with reasoning tokens (e.g., gpt-5.1)
) -> GenerationConfig:
    """Get GenerationConfig for atom extraction with structured output.
    
    Args:
        temperature: Sampling temperature (default 0.2 for consistent extraction)
        max_tokens: Maximum tokens in response (default 64000 to account for reasoning tokens)
        
    Returns:
        GenerationConfig configured for atom extraction with JSON schema
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=ATOM_EXTRACTION_SYSTEM_PROMPT,
        user_prompt_template="{content}",  # Will be replaced with rendered prompt
        response_format="json_schema",
        json_schema=ATOM_EXTRACTION_SCHEMA
    )
