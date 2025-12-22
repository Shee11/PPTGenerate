"""Atom extraction from source content.

Narrative Atoms: A story-driven atom system for presentations.
- BioAtom → Title/Intro slides (identity, history, credentials)
- FactAtom → Anchor slides (objective foundation, context)
- StatAtom → Data visualization slides (metrics, KPIs, numbers)
- QuoteAtom → Impact slides (verbatim memorable phrases)
- TensionAtom → Friction slides (conflict/problem)
- ConceptAtom → Insight slides (solution/takeaway)
- VisualAtom → Visual instruction for slide design
"""

from src.generation.atom.models import (
    Atom,
    BioAtom,
    FactAtom,
    StatAtom,
    QuoteAtom,
    TensionAtom,
    ConceptAtom,
    VisualAtom,
)
from src.generation.atom.collection import AtomCollection
from src.generation.atom.extractor import extract_atoms

__all__ = [
    'Atom',
    'BioAtom',
    'FactAtom',
    'StatAtom',
    'QuoteAtom',
    'TensionAtom',
    'ConceptAtom',
    'VisualAtom',
    'AtomCollection',
    'extract_atoms'
]
