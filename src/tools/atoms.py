"""Atoms Tool - Extract content atoms from source.

DirectTool: Delegates to src.generation.atom.extractor for sophisticated extraction.
Uses LLM internally via the extractor module with proper prompts and JSON schema.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, ClassVar, Optional, Any, Dict
from pydantic import Field

from src.common.tool_protocol import DirectTool, ToolContext, ToolPatch, register_tool

if TYPE_CHECKING:
    from src.generation.state import PipelineState


class AtomsContext(ToolContext):
    """Context for atom extraction - holds the Source object."""
    # Use Any to avoid Pydantic forward reference issues
    source: Optional[Any] = Field(default=None, description="Source object for extraction")
    intent_guidance: str = Field(default="", description="Extraction guidance from constitution")


class AtomsPatch(ToolPatch):
    """Patch containing the AtomCollection."""
    collection: Optional[Any] = Field(default=None, description="Extracted atom collection")
    
    class Config:
        arbitrary_types_allowed = True


@register_tool
class AtomsTool(DirectTool[AtomsContext, AtomsPatch]):
    """Extracts atoms from source content using the atom extractor.
    
    This is a DirectTool that delegates to src.generation.atom.extractor
    which has sophisticated extraction with:
    - 7 atom types: BIO, FACT, STAT, QUOTE, TENSION, CONCEPT, VISUAL
    - JSON schema for structured output
    - Caching support
    - Intent guidance support
    """
    
    # Self-description
    name: ClassVar[str] = "atoms"
    description: ClassVar[str] = "Extract structured atoms (BIO, FACT, STAT, QUOTE, TENSION, CONCEPT, VISUAL) from source content."
    query_description: ClassVar[str] = "Runs when source file is provided. Extracts structured atoms from VTT, TXT, MD files using sophisticated prompts."
    args_description: ClassVar[List[str]] = [
        "source_path (path to source file)",
        "content_type (text/vtt, text/plain, text/markdown)",
        "intent_guidance (optional extraction guidance from constitution)",
    ]
    requires: ClassVar[List[str]] = ["constitution"]
    produces: ClassVar[List[str]] = ["atoms"]
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> AtomsContext:
        """Extract source and guidance from state."""
        if not state.source:
            raise ValueError("No source in state")
        
        # Build intent guidance from constitution
        intent_guidance = ""
        constitution = state.get_constitution()
        if constitution:
            if hasattr(constitution, 'style_rules') and constitution.style_rules:
                intent_guidance = "\n".join(constitution.style_rules)
        
        return AtomsContext(
            source=state.source,
            intent_guidance=intent_guidance,
        )
    
    def transform(
        self,
        context: AtomsContext,
        user_instruction: str,
    ) -> AtomsPatch:
        """Execute extraction via the extractor module."""
        from pathlib import Path
        from src.generation.atom.extractor import extract_atoms
        from src.common.source import Source
        
        # Build full Source from SourceInfo (which doesn't have content)
        source_info = context.source
        source_path = Path(source_info.path)
        content = source_path.read_text(encoding='utf-8')
        
        source = Source(
            source_id=source_info.content_hash,
            name=source_path.name,
            file_path=str(source_path.absolute()),
            content_type=source_info.content_type if source_info.content_type in ["text/plain", "text/vtt"] else "text/plain",
            content=content,
        )
        
        # Add user instruction to guidance
        full_guidance = context.intent_guidance
        if user_instruction:
            if full_guidance:
                full_guidance += f"\n\nUser instruction: {user_instruction}"
            else:
                full_guidance = f"User instruction: {user_instruction}"
        
        self._log(f"Extracting atoms from {source.name}")
        if full_guidance:
            self._log(f"With guidance: {full_guidance[:100]}...")
        
        # Delegate to the sophisticated extractor
        collection = extract_atoms(
            source=source,
            use_cache=self.use_cache,
            intent_guidance=full_guidance
        )
        
        atom_count = len(collection.list_contexts())
        self._log(f"Extracted {atom_count} atoms")
        
        return AtomsPatch(collection=collection)
    
    def apply(self, state: "PipelineState", patch: AtomsPatch) -> None:
        """Apply the atom collection to state."""
        if patch.collection:
            state.set_atoms(patch.collection)
            self._log(f"Applied: {len(patch.collection.list_contexts())} atoms")
