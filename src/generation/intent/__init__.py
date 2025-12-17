"""Intent detection module for presentation generation."""

from src.generation.intent.detector import (
    PresentationIntent,
    SourceChange,
    AtomExtractionTask,
    StageChange,
    detect_intent
)

__all__ = [
    'PresentationIntent',
    'SourceChange',
    'AtomExtractionTask',
    'StageChange',
    'detect_intent'
]
