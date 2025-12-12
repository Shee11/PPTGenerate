"""Cinematic layout strategies."""
from typing import List

from src.common.size_class import SizeClass
from src.common.slot import Slot


class CinematicSplit5050Strategy:
    """Cinematic.Split_50_50: Equal 50/50 left-right split.
    
    Two L slots dividing the screen equally.
    Ideal for comparisons, before/after, or dual content display.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Cinematic.Split_50_50"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return 2 L slots for equal left/right division."""
        return [
            Slot(role="left", size=SizeClass.L),
            Slot(role="right", size=SizeClass.L),
        ]


class CinematicFullBleedStrategy:
    """Cinematic.FullBleed: Edge-to-edge immersive content.
    
    Layout: 1 Size XL slot covering viewport edge-to-edge.
    Maximum visual impact with no margins or padding.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Cinematic.FullBleed"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return single XL slot for full-bleed content."""
        return [
            Slot(role="stage", size=SizeClass.XL),
        ]


class CinematicSplit3070Strategy:
    """Cinematic.Split_30_70: Asymmetric 30/70 sidebar-stage split.
    
    Layout: Size M sidebar (30%) + Size XL stage (70%).
    Perfect for navigation + content or filtering + results.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Cinematic.Split_30_70"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return sidebar (M) + stage (XL) slots."""
        return [
            Slot(role="sidebar", size=SizeClass.M),
            Slot(role="stage", size=SizeClass.XL),
        ]
