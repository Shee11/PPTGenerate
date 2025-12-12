"""Size class enumeration for T-Shirt sizing."""
from enum import IntEnum


class SizeClass(IntEnum):
    """T-Shirt size enumeration with ordering support.
    
    Values are ordered to allow comparison: S < M < L < XL
    This enables validation that a widget's minimum size fits in a slot.
    """
    S = 1   # Small
    M = 2   # Medium
    L = 3   # Large
    XL = 4  # Extra Large

    def __str__(self) -> str:
        """Return the name of the size class."""
        return self.name

    @classmethod
    def from_string(cls, value: str) -> "SizeClass":
        """Create a SizeClass from a string name.
        
        Args:
            value: Size name as string (e.g., "S", "M", "L", "XL")
            
        Returns:
            SizeClass instance
            
        Raises:
            ValueError: If the value is not a valid size class name
        """
        try:
            return cls[value.upper()]
        except KeyError:
            valid_sizes = ", ".join([s.name for s in cls])
            raise ValueError(f"Invalid size '{value}'. Valid sizes: {valid_sizes}")
