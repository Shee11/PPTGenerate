"""Unit tests for layout strategy slot definitions."""
import pytest
from src.layout.strategies.bento import (
    BentoStandardStrategy,
    BentoHeroLeftStrategy,
    BentoHeroTopStrategy,
    BentoQuarterStrategy
)
from src.layout.strategies.swiss import (
    SwissPosterStrategy,
    SwissAsymmetryStrategy,
    SwissSplitTypoStrategy
)
from src.layout.strategies.cinematic import (
    CinematicSplit5050Strategy,
    CinematicFullBleedStrategy,
    CinematicSplit3070Strategy
)
from src.common.size_class import SizeClass


class TestBentoStandardStrategy:
    """Test BentoStandardStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert BentoStandardStrategy.get_strategy_name() == "Bento.Standard"
    
    def test_has_six_slots(self) -> None:
        """Test that Bento.Standard has 6 slots (3x2 grid)."""
        slots = BentoStandardStrategy.get_slots()
        assert len(slots) == 6
    
    def test_all_slots_are_size_s(self) -> None:
        """Test that all slots in Bento.Standard are Size S."""
        slots = BentoStandardStrategy.get_slots()
        for slot in slots:
            assert slot.size == SizeClass.S
    
    def test_slot_roles(self) -> None:
        """Test that slot roles are correctly named."""
        slots = BentoStandardStrategy.get_slots()
        roles = [slot.role for slot in slots]
        
        # Should have 6 unique roles
        assert len(set(roles)) == 6
        
        # Roles should follow pattern: cell_1, cell_2, etc.
        for i in range(1, 7):
            assert f"cell_{i}" in roles


class TestSwissPosterStrategy:
    """Test SwissPosterStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert SwissPosterStrategy.get_strategy_name() == "Swiss.Poster"
    
    def test_has_one_slot(self) -> None:
        """Test that Swiss.Poster has 1 XL slot (full screen)."""
        slots = SwissPosterStrategy.get_slots()
        assert len(slots) == 1
    
    def test_slot_is_size_xl(self) -> None:
        """Test that the slot is Size XL."""
        slots = SwissPosterStrategy.get_slots()
        assert slots[0].size == SizeClass.XL
    
    def test_slot_role(self) -> None:
        """Test that slot role is 'headline'."""
        slots = SwissPosterStrategy.get_slots()
        assert slots[0].role == "headline"


class TestCinematicSplit5050Strategy:
    """Test CinematicSplit5050Strategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert CinematicSplit5050Strategy.get_strategy_name() == "Cinematic.Split_50_50"
    
    def test_has_two_slots(self) -> None:
        """Test that Cinematic.Split_50_50 has 2 slots (50/50 split)."""
        slots = CinematicSplit5050Strategy.get_slots()
        assert len(slots) == 2
    
    def test_both_slots_are_size_l(self) -> None:
        """Test that both slots are Size L (equal screen division)."""
        slots = CinematicSplit5050Strategy.get_slots()
        assert slots[0].size == SizeClass.L
        assert slots[1].size == SizeClass.L
    
    def test_slot_roles(self) -> None:
        """Test that slot roles are 'left' and 'right'."""
        slots = CinematicSplit5050Strategy.get_slots()
        roles = [slot.role for slot in slots]
        
        assert "left" in roles
        assert "right" in roles


class TestBentoHeroLeftStrategy:
    """Test BentoHeroLeftStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert BentoHeroLeftStrategy.get_strategy_name() == "Bento.HeroLeft"
    
    def test_has_correct_slot_count(self) -> None:
        """Test that BentoHeroLeft has hero (L) + 4 small slots."""
        slots = BentoHeroLeftStrategy.get_slots()
        assert len(slots) == 5
    
    def test_hero_slot_is_size_l(self) -> None:
        """Test that main hero slot is Size L (2x2 space)."""
        slots = BentoHeroLeftStrategy.get_slots()
        hero = [s for s in slots if s.role == "hero"][0]
        assert hero.size == SizeClass.L
    
    def test_side_slots_are_size_s(self) -> None:
        """Test that side slots are Size S."""
        slots = BentoHeroLeftStrategy.get_slots()
        sides = [s for s in slots if s.role.startswith("side_")]
        assert len(sides) == 4
        for side in sides:
            assert side.size == SizeClass.S


class TestBentoHeroTopStrategy:
    """Test BentoHeroTopStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert BentoHeroTopStrategy.get_strategy_name() == "Bento.HeroTop"
    
    def test_has_correct_slot_count(self) -> None:
        """Test that BentoHeroTop has hero (L) + 3 small slots."""
        slots = BentoHeroTopStrategy.get_slots()
        assert len(slots) == 4
    
    def test_hero_slot_is_size_l(self) -> None:
        """Test that main hero slot is Size L."""
        slots = BentoHeroTopStrategy.get_slots()
        hero = [s for s in slots if s.role == "hero"][0]
        assert hero.size == SizeClass.L
    
    def test_footer_slots_are_size_s(self) -> None:
        """Test that footer slots are Size S."""
        slots = BentoHeroTopStrategy.get_slots()
        footers = [s for s in slots if s.role.startswith("footer_")]
        assert len(footers) == 3
        for footer in footers:
            assert footer.size == SizeClass.S


class TestBentoQuarterStrategy:
    """Test BentoQuarterStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert BentoQuarterStrategy.get_strategy_name() == "Bento.Quarter"
    
    def test_has_four_slots(self) -> None:
        """Test that BentoQuarter has 4 slots (2x2 grid)."""
        slots = BentoQuarterStrategy.get_slots()
        assert len(slots) == 4
    
    def test_all_slots_are_size_m(self) -> None:
        """Test that all slots are Size M."""
        slots = BentoQuarterStrategy.get_slots()
        for slot in slots:
            assert slot.size == SizeClass.M


class TestSwissAsymmetryStrategy:
    """Test SwissAsymmetryStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert SwissAsymmetryStrategy.get_strategy_name() == "Swiss.Asymmetry"
    
    def test_has_one_content_slot(self) -> None:
        """Test that SwissAsymmetry has 1 content slot (void area implicit)."""
        slots = SwissAsymmetryStrategy.get_slots()
        assert len(slots) == 1
    
    def test_content_slot_is_size_l(self) -> None:
        """Test that content slot is Size L."""
        slots = SwissAsymmetryStrategy.get_slots()
        assert slots[0].size == SizeClass.L
        assert slots[0].role == "content"


class TestSwissSplitTypoStrategy:
    """Test SwissSplitTypoStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert SwissSplitTypoStrategy.get_strategy_name() == "Swiss.SplitTypo"
    
    def test_has_two_slots(self) -> None:
        """Test that SwissSplitTypo has 2 slots."""
        slots = SwissSplitTypoStrategy.get_slots()
        assert len(slots) == 2
    
    def test_headline_is_size_m(self) -> None:
        """Test that headline slot is Size M."""
        slots = SwissSplitTypoStrategy.get_slots()
        headline = [s for s in slots if s.role == "headline"][0]
        assert headline.size == SizeClass.M
    
    def test_body_is_size_l(self) -> None:
        """Test that body slot is Size L."""
        slots = SwissSplitTypoStrategy.get_slots()
        body = [s for s in slots if s.role == "body"][0]
        assert body.size == SizeClass.L


class TestCinematicFullBleedStrategy:
    """Test CinematicFullBleedStrategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert CinematicFullBleedStrategy.get_strategy_name() == "Cinematic.FullBleed"
    
    def test_has_one_slot(self) -> None:
        """Test that CinematicFullBleed has 1 XL slot (edge-to-edge)."""
        slots = CinematicFullBleedStrategy.get_slots()
        assert len(slots) == 1
    
    def test_stage_is_size_xl(self) -> None:
        """Test that stage slot is Size XL."""
        slots = CinematicFullBleedStrategy.get_slots()
        assert slots[0].size == SizeClass.XL
        assert slots[0].role == "stage"


class TestCinematicSplit3070Strategy:
    """Test CinematicSplit3070Strategy slot definitions."""
    
    def test_strategy_name(self) -> None:
        """Test that strategy has correct name."""
        assert CinematicSplit3070Strategy.get_strategy_name() == "Cinematic.Split_30_70"
    
    def test_has_two_slots(self) -> None:
        """Test that CinematicSplit3070 has 2 slots (30/70 split)."""
        slots = CinematicSplit3070Strategy.get_slots()
        assert len(slots) == 2
    
    def test_sidebar_is_size_m(self) -> None:
        """Test that sidebar (30%) is Size M."""
        slots = CinematicSplit3070Strategy.get_slots()
        sidebar = [s for s in slots if s.role == "sidebar"][0]
        assert sidebar.size == SizeClass.M
    
    def test_stage_is_size_xl(self) -> None:
        """Test that stage (70%) is Size XL."""
        slots = CinematicSplit3070Strategy.get_slots()
        stage = [s for s in slots if s.role == "stage"][0]
        assert stage.size == SizeClass.XL
