"""Prompts for atom extraction from source content."""
import os
from src.common.source import Source
from src.utils.generation_config import GenerationConfig


ATOM_EXTRACTION_SYSTEM_PROMPT = """You are an expert content analyzer. Your task is to extract structured knowledge atoms from source content.

Extract six types of atoms:

1. **StatementAtom**: Individual claims, facts, or assertions
   - text: The statement text
   - related_to: IDs of atoms this supports or connects to (optional)
   - contradicts: IDs of atoms this contradicts (optional)

2. **ProcessAtom**: Step-by-step procedures or workflows
   - title: Name of the process
   - steps: Ordered list of steps
     - order: Step number (1-indexed)
     - text: Step description
     - dependencies: Step numbers that must complete first (optional)

3. **ComparisonAtom**: Comparisons across multiple dimensions
   - dimensions: List of comparison criteria
   - entities: Dict mapping entity names to dimension values

4. **QuoteAtom**: Quotes with attribution
   - quote_text: The exact quoted text
   - speaker: Name/title of person (e.g., "John Smith, CEO")
   - source: Document/context (e.g., "Q3 Review Meeting", "strategy.pdf")
   - context: Optional explanation of significance (default: "")
   
   **Use for**: Hard decisions, conclusions, meaningful comments, executive statements

5. **ActionItemAtom**: Action items with tracking
   - title: Action items category (e.g., "Q4 Launch Actions")
   - items: List of action items
     - description: What needs to be done
     - assignee: Person/team responsible (empty "" if unassigned)
     - state: "New" | "Update" | "Resolved" (default: "New")
     - due_date: Optional deadline in ISO format YYYY-MM-DD (default: "")
   
   **Use for**: Tasks, decisions needing follow-up, next steps from meetings

6. **TimelineAtom**: Chronological sequence of events (NEW - for journey/evolution narratives)
   - title: Timeline category (e.g., "Career Journey", "Product Evolution", "Company History")
   - events: Ordered list of timeline events (minimum 2)
     - time_marker: Year, date, or period (e.g., "2011", "Q4 2023", "Early 2020s", "2016-2018")
     - description: What happened at this point
     - details: Optional additional context (default: "")
   
   **Use for**: Career progressions, product roadmaps, historical narratives, speaker journeys
   **CRITICAL**: Look for chronological markers (years, dates, "from X to Y", "then", "later", "starting from")
   **Example**: "Starting from 2011... 2016... 2021..." → Extract as TimelineAtom, NOT multiple StatementAtoms

**Output Format**: Return a JSON object with an "atoms" array. Each atom must have:
- id: Unique identifier (e.g., "stmt_001", "proc_001", "comp_001", "quote_001", "action_001", "timeline_001")
- type: "StatementAtom" | "ProcessAtom" | "ComparisonAtom" | "QuoteAtom" | "ActionItemAtom" | "TimelineAtom"
- rank: Integer for ordering (start at 1)
- source_ref: Object with source_id, file_path, offset, length
- Additional fields per atom type

**Guidelines**:
- Extract HIGH-LEVEL atoms suitable for PRESENTATION slides (not documentation)
- Focus on MAIN TOPICS only - skip implementation details, background context, and minutiae
- Each atom should represent a KEY CONCEPT that deserves slide real estate
- Aim for 5-12 atoms total for typical talks (NOT 20-30+)
- **COMPRESS AGGRESSIVELY**: Merge related sub-points into single atoms (e.g., "3 benefits" → 1 StatementAtom with list)
- Synthesize multiple related ideas into rich, compound atoms rather than fragmenting
- **TIMELINE PRIORITY**: If you detect 3+ chronological references (years, dates), create ONE TimelineAtom instead of multiple StatementAtoms
- For quotes: Preserve exact wording and proper attribution
- For action items: Extract assignee if mentioned, infer state from context
- Preserve relationships between statements (related_to, contradicts)
- Identify process dependencies accurately
- Use consistent dimension names in comparisons
- Set source_ref offset/length to approximate character positions
- Assign sequential IDs within each type (stmt_001, quote_001, action_001, timeline_001, etc.)

Return ONLY valid JSON. No markdown code blocks or explanations."""


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
Return a JSON object with an "atoms" array containing the extracted atoms."""
    
    return prompt


def get_atom_extraction_config(
    temperature: float = 0.2,
    max_tokens: int = 64000  # Increased for models with reasoning tokens (e.g., gpt-5.1)
) -> GenerationConfig:
    """Get GenerationConfig for atom extraction.
    
    Args:
        temperature: Sampling temperature (default 0.2 for consistent extraction)
        max_tokens: Maximum tokens in response (default 16000 to account for reasoning tokens)
        
    Returns:
        GenerationConfig configured for atom extraction
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=ATOM_EXTRACTION_SYSTEM_PROMPT,
        user_prompt_template="{content}",  # Will be replaced with rendered prompt
        response_format="json"
    )
