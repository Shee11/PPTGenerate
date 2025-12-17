"""Atom extractor for extracting structured atoms from source content."""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from src.common.source import Source, SourceReference
from src.common.patchable_context_pydantic import AddOperation, Patch
from src.generation.atom.models import (
    StatementAtom,
    ProcessAtom,
    ComparisonAtom,
    QuoteAtom,
    ActionItemAtom,
    TimelineAtom,
    ProcessStep,
    ActionItem,
    TimelineEvent
)
from src.generation.atom.collection import AtomCollection
from src.generation.atom.prompts import render_atom_extraction_prompt, get_atom_extraction_config
from src.utils.llm_client import call_llm
from src.utils.generation_config import GenerationConfig
from src.utils.cache import GenerationCache

logger = logging.getLogger(__name__)


def extract_atoms(
    source: Source,
    config: Optional[GenerationConfig] = None,
    use_cache: bool = True,
    intent_guidance: str = ""
) -> AtomCollection:
    """Extract structured atoms from source content using LLM.
    
    Args:
        source: Source content to extract atoms from
        config: Optional custom GenerationConfig (uses default if None)
        use_cache: Whether to use cache for LLM responses (default True)
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        AtomCollection containing extracted atoms
        
    Raises:
        ValueError: If atom type is unknown or response is malformed
        JSONDecodeError: If LLM response is not valid JSON
        KeyError: If response missing required keys
        Exception: If LLM call fails
    """
    # Use default config if not provided
    if config is None:
        config = get_atom_extraction_config()
    
    # Render user prompt from source with intent guidance
    user_prompt = render_atom_extraction_prompt(source, intent_guidance)
    
    # Setup cache
    cache = GenerationCache(Path(".cache/atoms"))
    cache_key = None
    
    if use_cache:
        cache_key = cache.hash_key(config.system_prompt, user_prompt)
        cached_data = cache.load(cache_key)
        
        if cached_data is not None:
            logger.info(f"Cache hit for source {source.source_id}")
            print(f"✓ Using cached atom extraction")
            return _build_collection_from_data(source, cached_data)
    
    # Cache miss or cache disabled - call LLM
    logger.info(f"Extracting atoms from source {source.source_id}")
    print(f"⚙ Extracting atoms via LLM...")
    
    response = call_llm(
        system_prompt=config.system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        response_format=config.response_format,
        max_reasoning_tokens=config.max_reasoning_tokens
    )
    
    # Parse JSON response
    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        logger.error(f"Response content (first 500 chars): {response[:500]}")
        raise
    
    # Validate required keys
    if "atoms" not in data:
        raise KeyError("Response missing 'atoms' key")
    
    # Store abstract in source metadata if provided
    if "abstract" in data and data["abstract"]:
        source.metadata["abstract"] = data["abstract"]
        logger.info(f"Extracted abstract: {data['abstract'][:100]}...")
    
    # Save to cache if enabled
    if use_cache and cache_key is not None:
        cache.save(cache_key, data)
        logger.info(f"Saved extraction result to cache for source {source.source_id}")
    
    return _build_collection_from_data(source, data)


def _build_collection_from_data(source: Source, data: Dict[str, Any]) -> AtomCollection:
    """Build AtomCollection from parsed JSON data.
    
    Args:
        source: Original source (for validation)
        data: Parsed JSON data with 'atoms' key
        
    Returns:
        AtomCollection with all atoms added
        
    Raises:
        ValueError: If atom type is unknown
        KeyError: If required atom fields are missing
    """
    collection = AtomCollection(id=f"atoms_{source.source_id}")
    operations = []
    
    for atom_data in data["atoms"]:
        atom_type = atom_data.get("type")
        
        if atom_type == "StatementAtom":
            atom = _parse_statement_atom(atom_data)
        elif atom_type == "ProcessAtom":
            atom = _parse_process_atom(atom_data)
        elif atom_type == "ComparisonAtom":
            atom = _parse_comparison_atom(atom_data)
        elif atom_type == "QuoteAtom":
            atom = _parse_quote_atom(atom_data)
        elif atom_type == "ActionItemAtom":
            atom = _parse_action_item_atom(atom_data)
        elif atom_type == "TimelineAtom":
            atom = _parse_timeline_atom(atom_data)
        else:
            raise ValueError(f"Unknown atom type: {atom_type}")
        
        operations.append(AddOperation(add=atom))
    
    # Apply all operations in one patch
    if operations:
        collection.patch(Patch(operations=operations))
    
    return collection


def _parse_statement_atom(data: Dict[str, Any]) -> StatementAtom:
    """Parse StatementAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        StatementAtom instance
    """
    return StatementAtom(
        id=data["id"],
        rank=data["rank"],
        text=data["text"],
        related_to=data.get("related_to", []),
        contradicts=data.get("contradicts", []),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_process_atom(data: Dict[str, Any]) -> ProcessAtom:
    """Parse ProcessAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        ProcessAtom instance
    """
    steps = [
        ProcessStep(
            order=step["order"],
            text=step["text"],
            dependencies=step.get("dependencies", [])
        )
        for step in data["steps"]
    ]
    
    return ProcessAtom(
        id=data["id"],
        rank=data["rank"],
        title=data["title"],
        steps=steps,
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_comparison_atom(data: Dict[str, Any]) -> ComparisonAtom:
    """Parse ComparisonAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        ComparisonAtom instance
    """
    return ComparisonAtom(
        id=data["id"],
        rank=data["rank"],
        dimensions=data["dimensions"],
        entities=data["entities"],
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_quote_atom(data: Dict[str, Any]) -> QuoteAtom:
    """Parse QuoteAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        QuoteAtom instance
    """
    return QuoteAtom(
        id=data["id"],
        rank=data["rank"],
        quote_text=data["quote_text"],
        speaker=data["speaker"],
        source=data["source"],
        context=data.get("context", ""),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_action_item_atom(data: Dict[str, Any]) -> ActionItemAtom:
    """Parse ActionItemAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        ActionItemAtom instance
    """
    items = [
        ActionItem(
            description=item["description"],
            assignee=item.get("assignee", ""),
            state=item.get("state", "New"),
            due_date=item.get("due_date", "")
        )
        for item in data["items"]
    ]
    
    return ActionItemAtom(
        id=data["id"],
        rank=data["rank"],
        title=data["title"],
        items=items,
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_timeline_atom(data: Dict[str, Any]) -> TimelineAtom:
    """Parse TimelineAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        TimelineAtom instance
    """
    events = [
        TimelineEvent(
            time_marker=event["time_marker"],
            description=event["description"],
            details=event.get("details", "")
        )
        for event in data["events"]
    ]
    
    return TimelineAtom(
        id=data["id"],
        rank=data["rank"],
        title=data["title"],
        events=events,
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )
