"""Swiss layout strategies."""
from typing import List

from src.common.size_class import SizeClass
from src.common.slot import Slot


class SwissPosterStrategy:
    """Swiss.Poster: Single full-screen slot.
    
    One XL slot occupying the entire screen.
    Ideal for hero images, large typography, or full-bleed content.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Swiss.Poster"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 1 XL slot for full-screen headline."""
        return [
            Slot(role="headline", size=SizeClass.XL),
        ]


class SwissAsymmetryStrategy:
    """Swiss.Asymmetry: Content on right with intentional void space.
    
    Layout: 1 Size L content slot positioned right, void area on left.
    Creates visual tension with asymmetric balance.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Swiss.Asymmetry"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return single L slot for content (void area implicit)."""
        return [
            Slot(role="content", size=SizeClass.L),
        ]


class SwissSplitTypoStrategy:
    """Swiss.SplitTypo: Typography-focused vertical split.
    
    Layout: Size M headline slot on top, Size L body slot below.
    Emphasizes typographic hierarchy and readable content.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Swiss.SplitTypo"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return headline (M) + body (L) slots."""
        return [
            Slot(role="headline", size=SizeClass.M),
            Slot(role="body", size=SizeClass.L),
        ]
