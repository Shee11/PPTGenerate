"""Custom exception types for UCE rendering system."""


class UCERenderError(Exception):
    """Base exception for all UCE rendering errors."""
    pass


class SizeConstraintError(UCERenderError):
    """Raised when a widget's minimum size exceeds its assigned slot size.
    
    This error indicates that a widget requires a larger slot than
    the one it has been assigned to.
    """

    def __init__(
        self,
        widget_type: str,
        widget_min_size: str,
        slot_role: str,
        slot_size: str
    ):
        """Initialize size constraint error.
        
        Args:
            widget_type: Type of the widget (e.g., "Chart.Sankey")
            widget_min_size: Minimum size required by the widget
            slot_role: Role name of the slot
            slot_size: Actual size of the slot
        """
        self.widget_type = widget_type
        self.widget_min_size = widget_min_size
        self.slot_role = slot_role
        self.slot_size = slot_size

        message = (
            f"Size constraint violation: Widget '{widget_type}' requires "
            f"minimum size {widget_min_size}, but slot '{slot_role}' is only {slot_size}. "
            f"Suggestion: Assign this widget to a slot with size >= {widget_min_size}."
        )
        super().__init__(message)


class MissingReferenceError(UCERenderError):
    """Raised when a widget references a non-existent atom_id or theme.
    
    This error indicates that the configuration contains a reference
    to data or resources that don't exist.
    """

    def __init__(self, reference_type: str, reference_id: str, context: str = ""):
        """Initialize missing reference error.
        
        Args:
            reference_type: Type of reference (e.g., "atom_id", "theme")
            reference_id: The missing identifier
            context: Additional context about where the error occurred
        """
        self.reference_type = reference_type
        self.reference_id = reference_id
        self.context = context

        message = f"Missing {reference_type}: '{reference_id}'"
        if context:
            message += f" in {context}"
        message += f". Ensure the {reference_type} exists before referencing it."

        super().__init__(message)


class ValidationError(UCERenderError):
    """Raised when configuration validation fails.
    
    This is a general validation error for schema or constraint violations.
    """
    pass
