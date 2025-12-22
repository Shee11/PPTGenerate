"""Test script for layout validation functionality."""
from src.paged.layout.dummy.validation import LayoutValidator, format_issues_for_llm
from src.common.renderable_layout import RenderableLayout, WidgetAssignment
from src.common.slot import Slot
from src.common.bounds import Bounds
from src.paged.widgets.base import BaseWidget
from src.common.size_class import SizeClass

# Create a mock widget
class MockWidget(BaseWidget):
    def __init__(self):
        super().__init__(type="display", parameters={"text": "Test"})
    
    def get_widget_type(self):
        return "display"
    
    def measure(self, size_class, style):
        """Mock measure implementation."""
        return {"width": 100, "height": 50}
    
    def render_data(self, style):
        """Mock render_data implementation."""
        return {"text": "Test", "type": "display"}

# Test 1: Color contrast issue
def test_color_contrast():
    print("\n=== Test 1: Color Contrast ===")
    widget = MockWidget()
    slot = Slot(role="title", size=SizeClass.XL)
    bounds = Bounds(x=0, y=0, width=1920, height=200)
    
    # Create assignment with similar colors
    assignment = WidgetAssignment(
        role="title",
        widget=widget,
        slot=slot,
        applied_style={
            "color": "#333333",  # Dark gray text
            "background": "#444444"  # Slightly lighter gray background - low contrast!
        },
        bounds=bounds,
        preset=None
    )
    
    layout = RenderableLayout(
        strategy_name="Test.Strategy",
        widget_assignments=[assignment],
        theme_vars={},
        style_props={},
        width=1920,
        height=1080,
        slide_number=1,
        slide_id="test-1"
    )
    
    issues = LayoutValidator.validate(layout)
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  [{issue.severity}] {issue.category}: {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")

# Test 2: Content density issue
def test_content_density():
    print("\n=== Test 2: Content Density ===")
    widget = MockWidget()
    slot = Slot(role="subtitle", size=SizeClass.M)
    bounds = Bounds(x=100, y=100, width=200, height=50)  # Very small widget
    
    assignment = WidgetAssignment(
        role="subtitle",
        widget=widget,
        slot=slot,
        applied_style={"color": "#000000", "background": "#FFFFFF"},
        bounds=bounds,
        preset=None
    )
    
    # 1920x1080 = 2,073,600 total pixels
    # 200x50 = 10,000 pixels (0.48% density - very low!)
    layout = RenderableLayout(
        strategy_name="Test.Strategy",
        widget_assignments=[assignment],
        theme_vars={},
        style_props={},
        width=1920,
        height=1080,
        slide_number=1,
        slide_id="test-2"
    )
    
    issues = LayoutValidator.validate(layout)
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  [{issue.severity}] {issue.category}: {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")

# Test 3: Widget overlap
def test_widget_overlap():
    print("\n=== Test 3: Widget Overlap ===")
    widget1 = MockWidget()
    widget2 = MockWidget()
    slot1 = Slot(role="title", size=SizeClass.L)
    slot2 = Slot(role="subtitle", size=SizeClass.M)
    
    # Create overlapping bounds
    bounds1 = Bounds(x=100, y=100, width=800, height=200)
    bounds2 = Bounds(x=500, y=150, width=800, height=200)  # Overlaps with bounds1!
    
    assignment1 = WidgetAssignment(
        role="title",
        widget=widget1,
        slot=slot1,
        applied_style={"color": "#000000", "background": "#FFFFFF"},
        bounds=bounds1,
        preset=None
    )
    
    assignment2 = WidgetAssignment(
        role="subtitle",
        widget=widget2,
        slot=slot2,
        applied_style={"color": "#000000", "background": "#FFFFFF"},
        bounds=bounds2,
        preset=None
    )
    
    layout = RenderableLayout(
        strategy_name="Test.Strategy",
        widget_assignments=[assignment1, assignment2],
        theme_vars={},
        style_props={},
        width=1920,
        height=1080,
        slide_number=1,
        slide_id="test-3"
    )
    
    issues = LayoutValidator.validate(layout)
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  [{issue.severity}] {issue.category}: {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")

# Test 4: Style consistency
def test_style_consistency():
    print("\n=== Test 4: Style Consistency ===")
    widget1 = MockWidget()
    widget2 = MockWidget()
    slot1 = Slot(role="metric1", size=SizeClass.M)
    slot2 = Slot(role="metric2", size=SizeClass.M)
    
    bounds1 = Bounds(x=100, y=100, width=400, height=300)
    bounds2 = Bounds(x=600, y=100, width=400, height=300)
    
    # Same widget type but different presets - inconsistent!
    assignment1 = WidgetAssignment(
        role="metric1",
        widget=widget1,
        slot=slot1,
        applied_style={"color": "#000000", "background": "#FFFFFF"},
        bounds=bounds1,
        preset={"surface": "Elevated", "shape": "Rounded"}
    )
    
    assignment2 = WidgetAssignment(
        role="metric2",
        widget=widget2,
        slot=slot2,
        applied_style={"color": "#000000", "background": "#FFFFFF"},
        bounds=bounds2,
        preset={"surface": "Flat", "shape": "Sharp"}  # Different preset!
    )
    
    layout = RenderableLayout(
        strategy_name="Test.Strategy",
        widget_assignments=[assignment1, assignment2],
        theme_vars={},
        style_props={},
        width=1920,
        height=1080,
        slide_number=1,
        slide_id="test-4"
    )
    
    issues = LayoutValidator.validate(layout)
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  [{issue.severity}] {issue.category}: {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")

# Test 5: Format issues for LLM
def test_format_for_llm():
    print("\n=== Test 5: Format Issues for LLM ===")
    from src.paged.layout.dummy.validation import LayoutIssue
    
    issues = [
        LayoutIssue(
            severity="error",
            category="overlap",
            message="Widgets 'title' and 'subtitle' overlap by 150px",
            affected_widgets=["title", "subtitle"],
            suggestion="Reduce text length in widgets by 40-50%"
        ),
        LayoutIssue(
            severity="warning",
            category="color_contrast",
            message="Low contrast: foreground '#333' and background '#444'",
            affected_widgets=["title"],
            suggestion="Increase contrast using theme accent colors"
        )
    ]
    
    feedback = format_issues_for_llm(issues)
    print(feedback)

if __name__ == "__main__":
    print("Running Layout Validation Tests")
    print("=" * 80)
    
    test_color_contrast()
    test_content_density()
    test_widget_overlap()
    test_style_consistency()
    test_format_for_llm()
    
    print("\n" + "=" * 80)
    print("All tests completed!")
