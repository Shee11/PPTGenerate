"""Bento layout strategies."""
from typing import List

from src.common.size_class import SizeClass
from src.common.slot import Slot


class BentoStandardStrategy:
    """Bento.Standard: 3x2 grid of equal-sized cells.
    
    All 6 cells are Size S, arranged in a balanced grid.
    Ideal for dashboards, galleries, or feature grids.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.Standard"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 6 slots arranged in 3x2 grid, all Size S."""
        return [
            Slot(role="cell_1", size=SizeClass.S),
            Slot(role="cell_2", size=SizeClass.S),
            Slot(role="cell_3", size=SizeClass.S),
            Slot(role="cell_4", size=SizeClass.S),
            Slot(role="cell_5", size=SizeClass.S),
            Slot(role="cell_6", size=SizeClass.S),
        ]


class BentoHeroLeftStrategy:
    """Bento.HeroLeft: Hero on left (2x2) with 4 small side cells.
    
    Layout: 1 Size L hero slot on left, 4 Size S slots on right side.
    Emphasizes primary content while showing supporting metrics.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.HeroLeft"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return hero slot (L) + 4 side slots (S)."""
        return [
            Slot(role="hero", size=SizeClass.L),
            Slot(role="side_1", size=SizeClass.S),
            Slot(role="side_2", size=SizeClass.S),
            Slot(role="side_3", size=SizeClass.S),
            Slot(role="side_4", size=SizeClass.S),
        ]


class BentoHeroTopStrategy:
    """Bento.HeroTop: Hero on top (2x2) with 3 footer cells.
    
    Layout: 1 Size L hero slot on top, 3 Size S footer slots on bottom.
    Perfect for featured content with action buttons or stats below.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.HeroTop"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return hero slot (L) + 3 footer slots (S)."""
        return [
            Slot(role="hero", size=SizeClass.L),
            Slot(role="footer_1", size=SizeClass.S),
            Slot(role="footer_2", size=SizeClass.S),
            Slot(role="footer_3", size=SizeClass.S),
        ]


class BentoQuarterStrategy:
    """Bento.Quarter: 2x2 grid of medium-sized quadrants.
    
    Layout: 4 Size M slots arranged in balanced 2x2 grid.
    Each quadrant gets equal emphasis for comparison layouts.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Bento.Quarter"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 4 slots arranged in 2x2 grid, all Size M."""
        return [
            Slot(role="quadrant_1", size=SizeClass.M),
            Slot(role="quadrant_2", size=SizeClass.M),
            Slot(role="quadrant_3", size=SizeClass.M),
            Slot(role="quadrant_4", size=SizeClass.M),
        ]
