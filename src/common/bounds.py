"""Bounds model for widget positioning."""
from pydantic import BaseModel, Field


class Bounds(BaseModel):
    """Absolute position and size of a widget on the canvas.
    
    All values are in pixels relative to the canvas top-left corner (0, 0).
    """

    x: float = Field(..., description="X coordinate (left edge) in pixels", ge=0)
    y: float = Field(..., description="Y coordinate (top edge) in pixels", ge=0)
    width: float = Field(..., description="Width in pixels", gt=0)
    height: float = Field(..., description="Height in pixels", gt=0)

    @property
    def right(self) -> float:
        """Right edge x coordinate."""
        return self.x + self.width

    @property
    def bottom(self) -> float:
        """Bottom edge y coordinate."""
        return self.y + self.height

    @property
    def center_x(self) -> float:
        """Center x coordinate."""
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        """Center y coordinate."""
        return self.y + self.height / 2

    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is inside bounds."""
        return self.x <= x <= self.right and self.y <= y <= self.bottom

    def intersects(self, other: "Bounds") -> bool:
        """Check if this bounds intersects with another."""
        return not (
            self.right < other.x
            or self.x > other.right
            or self.bottom < other.y
            or self.y > other.bottom
        )

    def __str__(self) -> str:
        """String representation."""
        return f"Bounds(x={self.x}, y={self.y}, w={self.width}, h={self.height})"
