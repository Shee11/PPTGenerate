"""Slot model for layout slot definitions."""
from pydantic import BaseModel, Field

from src.common.size_class import SizeClass


class Slot(BaseModel):
    """Represents a slot within a layout strategy.
    
    A slot is a named region that can contain a widget.
    Each slot has a role (semantic name) and a size class.
    """

    role: str = Field(..., description="Semantic name of the slot (e.g., 'hero', 'sidebar')")
    size: SizeClass = Field(..., description="T-Shirt size class for this slot")

    def __str__(self) -> str:
        """Return string representation."""
        return f"Slot(role='{self.role}', size={self.size})"
