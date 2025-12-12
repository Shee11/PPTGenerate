"""Base protocol for layout strategies."""
from typing import List, Protocol

from src.common.slot import Slot


class LayoutStrategy(Protocol):
    """Protocol defining the interface for layout strategies.
    
    All layout strategies must implement get_slots() to define
    the slots available in that layout variant.
    """

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return the list of slots for this layout strategy.
        
        Returns:
            List of Slot instances defining the layout structure
        """
        ...

    @staticmethod
    def get_strategy_name() -> str:
        """Return the name of this strategy (e.g., 'Bento.Standard').
        
        Returns:
            Strategy name as string
        """
        ...
