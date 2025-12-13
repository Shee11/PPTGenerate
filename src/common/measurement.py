"""Widget size measurement for layout calculation."""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MeasuredSize:
    """Result of widget size measurement.
    
    Contains the calculated dimensions based on content and styling.
    """
    
    width: float  # Calculated width in pixels
    height: float  # Calculated height in pixels
    min_width: float = 0  # Minimum width constraint
    min_height: float = 0  # Minimum height constraint
    max_width: float = float('inf')  # Maximum width constraint
    max_height: float = float('inf')  # Maximum height constraint
    
    def constrain(self, available_width: float, available_height: float) -> "MeasuredSize":
        """Constrain size to available space while respecting min/max.
        
        Args:
            available_width: Maximum available width
            available_height: Maximum available height
            
        Returns:
            New MeasuredSize with constrained dimensions
        """
        constrained_width = max(self.min_width, min(self.width, available_width, self.max_width))
        constrained_height = max(self.min_height, min(self.height, available_height, self.max_height))
        
        return MeasuredSize(
            width=constrained_width,
            height=constrained_height,
            min_width=self.min_width,
            min_height=self.min_height,
            max_width=self.max_width,
            max_height=self.max_height
        )


class WidgetMeasurement:
    """Utility for measuring widget content size.
    
    This is a simplified measurement that estimates size based on:
    - Text content length
    - Font size from styling
    - Padding/margins
    - Widget-specific constraints
    
    For production, this should integrate with actual text rendering libraries
    for accurate font metrics (e.g., fontTools, Pillow).
    """
    
    # Approximate character width multipliers by font size
    # These are rough estimates - real implementation needs font metrics
    CHAR_WIDTH_RATIO = 0.6  # avg char width is ~60% of font size
    
    @classmethod
    def measure_text_widget(
        cls,
        text: str,
        font_size: float,
        max_width: float = float('inf'),
        line_height: float = 1.2,
        padding: float = 20,
    ) -> MeasuredSize:
        """Measure text content size.
        
        Args:
            text: Text content to measure
            font_size: Font size in pixels
            max_width: Maximum width before wrapping
            line_height: Line height multiplier
            padding: Total padding (horizontal + vertical)
            
        Returns:
            MeasuredSize with calculated dimensions
        """
        if not text:
            return MeasuredSize(
                width=padding * 2,
                height=font_size * line_height + padding * 2,
                min_width=100,
                min_height=50
            )
        
        # Estimate character width
        char_width = font_size * cls.CHAR_WIDTH_RATIO
        
        # Calculate text width (single line)
        text_width = len(text) * char_width
        
        # If text exceeds max_width, calculate wrapped lines
        if text_width > max_width - padding * 2:
            # Rough word wrapping estimation
            chars_per_line = int((max_width - padding * 2) / char_width)
            num_lines = max(1, len(text) // chars_per_line + 1)
            width = max_width
            height = (font_size * line_height * num_lines) + padding * 2
        else:
            width = text_width + padding * 2
            height = font_size * line_height + padding * 2
        
        return MeasuredSize(
            width=width,
            height=height,
            min_width=max(100, font_size * 5),  # At least 5 chars wide
            min_height=font_size * line_height + padding * 2
        )
    
    @classmethod
    def measure_number_widget(
        cls,
        number: float,
        font_size: float,
        label: str = "",
        padding: float = 20,
    ) -> MeasuredSize:
        """Measure numeric display widget.
        
        Args:
            number: Number to display
            font_size: Font size in pixels for number
            label: Optional label text
            padding: Total padding
            
        Returns:
            MeasuredSize with calculated dimensions
        """
        # Number string representation
        number_str = f"{number:,.2f}" if isinstance(number, float) else str(number)
        number_width = len(number_str) * font_size * cls.CHAR_WIDTH_RATIO
        
        # Label dimensions (smaller font)
        label_font_size = font_size * 0.4
        label_width = len(label) * label_font_size * cls.CHAR_WIDTH_RATIO if label else 0
        
        # Total dimensions
        width = max(number_width, label_width) + padding * 2
        height = font_size * 1.2  # Number height
        if label:
            height += label_font_size * 1.2 + 10  # Label height + spacing
        height += padding * 2
        
        return MeasuredSize(
            width=width,
            height=height,
            min_width=max(150, font_size * 3),
            min_height=max(100, height)
        )
    
    @classmethod
    def measure_fixed_size(cls, width: float, height: float) -> MeasuredSize:
        """Create fixed size measurement (for images, charts, etc.).
        
        Args:
            width: Fixed width
            height: Fixed height
            
        Returns:
            MeasuredSize with fixed dimensions
        """
        return MeasuredSize(
            width=width,
            height=height,
            min_width=width,
            min_height=height,
            max_width=width,
            max_height=height
        )
