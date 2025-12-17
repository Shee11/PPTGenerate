"""AtomCollection class for managing extracted atoms."""
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
from src.common.patchable_context_pydantic import PatchableCollection, PatchableContextBase, PatchError
from src.generation.atom.models import (
    Atom,
    StatementAtom,
    ProcessAtom,
    ComparisonAtom,
    QuoteAtom,
    ActionItemAtom,
    TimelineAtom
)


class AtomCollection(PatchableCollection):
    """Collection of extracted atoms from source content.
    
    Manages Atom instances (StatementAtom, ProcessAtom, ComparisonAtom)
    with support for filtering by source, type, and state.
    """
    
    def __init__(self, id: str):
        """Initialize AtomCollection.
        
        Args:
            id: Unique identifier for the collection
        """
        super().__init__(id=id, model_class=StatementAtom)
    
    def _patch_add(self, context: PatchableContextBase):
        """Override to handle multiple atom types without re-validation.
        
        Args:
            context: Atom instance to add
            
        Raises:
            PatchError: If atom with same ID already exists
        """
        if context.id in self._contexts:
            raise PatchError(f"Cannot add: context '{context.id}' already exists")
        
        # Don't re-validate - atoms already validated by their own constructors
        self._contexts[context.id] = context
    
    def _patch_replace(self, context: PatchableContextBase):
        """Override to handle multiple atom types without re-validation.
        
        Args:
            context: Atom instance to replace existing one
            
        Raises:
            PatchError: If atom with ID doesn't exist
        """
        if context.id not in self._contexts:
            raise PatchError(f"Cannot replace: context '{context.id}' not found")
        
        # Don't re-validate - atoms already validated by their own constructors
        self._contexts[context.id] = context
    
    def to_json(self, indent: int = 2) -> str:
        """Convert collection to JSON string with datetime support.
        
        Args:
            indent: Number of spaces for indentation
            
        Returns:
            JSON string representation
        """
        def datetime_encoder(obj):
            """Custom JSON encoder for datetime objects."""
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
        
        return json.dumps(self.to_dict(), indent=indent, default=datetime_encoder)
    
    def get_by_source(self, source_id: str) -> List[Atom]:
        """Get all atoms from a specific source.
        
        Args:
            source_id: Source identifier to filter by
            
        Returns:
            List of atoms from the specified source, sorted by rank
        """
        all_atoms = self.list_contexts()
        return [
            atom for atom in all_atoms
            if atom.source_ref.source_id == source_id
        ]
    
    def get_by_type(self, atom_type: str) -> List[Atom]:
        """Get all atoms of a specific type.
        
        Args:
            atom_type: Atom class name ("StatementAtom", "ProcessAtom", "ComparisonAtom")
            
        Returns:
            List of atoms matching the type, sorted by rank
        """
        all_atoms = self.list_contexts()
        return [
            atom for atom in all_atoms
            if type(atom).__name__ == atom_type
        ]
    
    def get_atom(self, atom_id: str) -> Optional[Atom]:
        """Get a single atom by ID.
        
        Args:
            atom_id: Atom identifier
            
        Returns:
            Atom instance if found, None otherwise
        """
        return self._contexts.get(atom_id)
