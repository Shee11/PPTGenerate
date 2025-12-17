"""Slides collection for managing multiple slide configurations."""
from typing import List, Optional, Dict, Any

from src.common.patchable_context_pydantic import PatchableCollection, Patch, SetThemeOperation, SetPresetOperation
from src.common.slide import Slide


class Slides(PatchableCollection):
    """Collection of Slide instances with patchable context support.
    
    Manages slides in rank order and provides methods for accessing
    slides by index or id. Also stores theme and preset configurations.
    """
    
    def __init__(self, id: str = "slides"):
        """Initialize slides collection.
        
        Args:
            id: Collection identifier (default: "slides")
        """
        super().__init__(id=id, model_class=Slide)
        self.theme: Optional[Dict[str, Any]] = None
        self.preset: Optional[Dict[str, Any]] = None
    
    def patch(self, patch: Patch) -> 'Slides':
        """
        Apply a Patch to this collection, including theme and preset operations.
        
        Args:
            patch: Patch instance with operations
            
        Returns:
            Self for chaining
        """
        for op in patch.operations:
            if isinstance(op, SetThemeOperation):
                self.theme = op.set_theme
            elif isinstance(op, SetPresetOperation):
                self.preset = op.set_preset
            # else: delegate to parent class for add/remove/replace operations
        
        # Call parent patch for standard operations
        super().patch(patch)
        return self
    
    def get_by_rank(self) -> List[Slide]:
        """Get all slides sorted by rank.
        
        Returns:
            List of slides ordered by rank
        """
        return sorted(self._contexts.values(), key=lambda s: s.rank)
    
    def get_by_id(self, slide_id: str) -> Optional[Slide]:
        """Get slide by ID.
        
        Args:
            slide_id: Slide identifier
            
        Returns:
            Slide instance or None if not found
        """
        return self._contexts.get(slide_id)
    
    def get_active_slides(self) -> List[Slide]:
        """Get all active slides sorted by rank.
        
        Returns:
            List of active slides ordered by rank
        """
        return sorted(
            [s for s in self._contexts.values() if s.state == "active"],
            key=lambda s: s.rank
        )
    
    def count(self) -> int:
        """Get total number of slides.
        
        Returns:
            Number of slides in collection
        """
        return len(self._contexts)
    
    def __len__(self) -> int:
        """Support len() function."""
        return self.count()
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Slides(id='{self.id}', count={self.count()})"
