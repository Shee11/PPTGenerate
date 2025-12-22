"""Atom extractor for extracting structured atoms from source content."""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from src.common.source import Source, SourceReference
from src.common.patchable_context_pydantic import AddOperation, Patch
from src.generation.atom.models import (
    BioAtom,
    FactAtom,
    StatAtom,
    QuoteAtom,
    TensionAtom,
    ConceptAtom,
    VisualAtom,
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
        json_schema=config.json_schema,
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
    
    # Map LLM type tags to parser functions
    type_mapping = {
        # Full class names
        "BioAtom": _parse_bio_atom,
        "FactAtom": _parse_fact_atom,
        "StatAtom": _parse_stat_atom,
        "QuoteAtom": _parse_quote_atom,
        "TensionAtom": _parse_tension_atom,
        "ConceptAtom": _parse_concept_atom,
        "VisualAtom": _parse_visual_atom,
        # Short tags from prompt (case-insensitive)
        "BIO": _parse_bio_atom,
        "bio": _parse_bio_atom,
        "Bio": _parse_bio_atom,
        "FACT": _parse_fact_atom,
        "fact": _parse_fact_atom,
        "Fact": _parse_fact_atom,
        "STAT": _parse_stat_atom,
        "stat": _parse_stat_atom,
        "Stat": _parse_stat_atom,
        "QUOTE": _parse_quote_atom,
        "quote": _parse_quote_atom,
        "Quote": _parse_quote_atom,
        "TENSION": _parse_tension_atom,
        "tension": _parse_tension_atom,
        "Tension": _parse_tension_atom,
        "CONCEPT": _parse_concept_atom,
        "concept": _parse_concept_atom,
        "Concept": _parse_concept_atom,
        "VISUAL": _parse_visual_atom,
        "visual": _parse_visual_atom,
        "Visual": _parse_visual_atom,
        # Bracket-wrapped versions
        "[BIO]": _parse_bio_atom,
        "[FACT]": _parse_fact_atom,
        "[STAT]": _parse_stat_atom,
        "[QUOTE]": _parse_quote_atom,
        "[TENSION]": _parse_tension_atom,
        "[CONCEPT]": _parse_concept_atom,
        "[VISUAL]": _parse_visual_atom,
    }
    
    for atom_data in data["atoms"]:
        atom_type = atom_data.get("type", "")
        
        # Try to find the parser for this type
        parser = type_mapping.get(atom_type)
        
        if parser is None:
            raise ValueError(f"Unknown atom type: {atom_type}")
        
        atom = parser(atom_data)
        operations.append(AddOperation(add=atom))
    
    # Apply all operations in one patch
    if operations:
        collection.patch(Patch(operations=operations))
    
    return collection


def _parse_bio_atom(data: Dict[str, Any]) -> BioAtom:
    """Parse BioAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        BioAtom instance
    """
    return BioAtom(
        id=data["id"],
        rank=data["rank"],
        abstract=data.get("abstract", ""),
        name=data["name"],
        role=data.get("role", ""),
        credentials=data.get("credentials", ""),
        affiliation=data.get("affiliation", ""),
        visual=data.get("visual", "none"),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_fact_atom(data: Dict[str, Any]) -> FactAtom:
    """Parse FactAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        FactAtom instance
    """
    return FactAtom(
        id=data["id"],
        rank=data["rank"],
        abstract=data.get("abstract", ""),
        text=data["text"],
        category=data.get("category", "other"),
        visual=data.get("visual", "none"),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_stat_atom(data: Dict[str, Any]) -> StatAtom:
    """Parse StatAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        StatAtom instance
    """
    return StatAtom(
        id=data["id"],
        rank=data["rank"],
        abstract=data.get("abstract", ""),
        value=data["value"],
        label=data["label"],
        context=data.get("context", ""),
        visual=data.get("visual", "chart"),
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
        abstract=data.get("abstract", ""),
        quote=data["quote"],
        attribution=data.get("attribution", ""),
        context=data.get("context", ""),
        visual=data.get("visual", "quote-card"),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_tension_atom(data: Dict[str, Any]) -> TensionAtom:
    """Parse TensionAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        TensionAtom instance
    """
    return TensionAtom(
        id=data["id"],
        rank=data["rank"],
        abstract=data.get("abstract", ""),
        text=data["text"],
        tension_type=data.get("tension_type", "problem"),
        resolution_hint=data.get("resolution_hint", ""),
        visual=data.get("visual", "none"),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_concept_atom(data: Dict[str, Any]) -> ConceptAtom:
    """Parse ConceptAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        ConceptAtom instance
    """
    return ConceptAtom(
        id=data["id"],
        rank=data["rank"],
        abstract=data.get("abstract", ""),
        text=data["text"],
        concept_type=data.get("concept_type", "insight"),
        supporting_facts=data.get("supporting_facts", []),
        visual=data.get("visual", "none"),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )


def _parse_visual_atom(data: Dict[str, Any]) -> VisualAtom:
    """Parse VisualAtom from JSON data.
    
    Args:
        data: Atom data dict
        
    Returns:
        VisualAtom instance
    """
    return VisualAtom(
        id=data["id"],
        rank=data["rank"],
        abstract=data.get("abstract", ""),
        description=data["description"],
        visual_category=data.get("visual_category", "other"),
        related_atom=data.get("related_atom", ""),
        visual=data.get("visual", "none"),
        source_ref=SourceReference(**data["source_ref"]),
        metadata=data.get("metadata", {})
    )
