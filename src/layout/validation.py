"""Layout validation to detect rendering issues and provide feedback for refinement."""
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import colorsys

from src.common.renderable_layout import RenderableLayout, WidgetAssignment


@dataclass
class LayoutIssue:
    """Represents a detected issue in the layout."""
    severity: str  # "error", "warning"
    category: str  # "color_contrast", "content_density", "overlap", "style_consistency"
    message: str  # Human-readable description
    affected_widgets: List[str]  # Widget roles affected
    suggestion: str  # Suggested fix


class LayoutValidator:
    """Validates RenderableLayout and detects common rendering issues."""
    
    # Thresholds for validation
    COLOR_SIMILARITY_THRESHOLD = 0.15  # Max color distance for "too similar" warning
    MIN_CONTENT_DENSITY = 0.3  # Min ratio of used space (widgets vs. total area)
    OVERLAP_TOLERANCE = 2  # Pixels of acceptable overlap
    
    # WCAG AA contrast ratios
    MIN_CONTRAST_NORMAL_TEXT = 4.5  # For text < 18pt or < 14pt bold
    MIN_CONTRAST_LARGE_TEXT = 3.0   # For text >= 18pt or >= 14pt bold
    
    @staticmethod
    def validate(layout: RenderableLayout) -> List[LayoutIssue]:
        """Validate a RenderableLayout and return detected issues.
        
        Args:
            layout: RenderableLayout to validate
            
        Returns:
            List of detected LayoutIssue objects
        """
        issues = []
        
        # Check color contrast issues
        issues.extend(LayoutValidator._check_color_contrast(layout))
        
        # Check content density
        issues.extend(LayoutValidator._check_content_density(layout))
        
        # Check for overlapping widgets
        issues.extend(LayoutValidator._check_overlaps(layout))
        
        # Check style consistency
        issues.extend(LayoutValidator._check_style_consistency(layout))
        
        return issues
    
    @staticmethod
    def _check_color_contrast(layout: RenderableLayout) -> List[LayoutIssue]:
        """Detect foreground/background color contrast issues using WCAG AA standards.
        
        Args:
            layout: RenderableLayout to check
            
        Returns:
            List of color contrast issues
        """
        issues = []
        
        # Check theme-level contrast (background vs text_color from theme_vars)
        theme_bg = layout.theme_vars.get('--color-background', None)
        theme_text = layout.theme_vars.get('--color-text', None)
        
        if theme_bg and theme_text:
            contrast_ratio = LayoutValidator._calculate_contrast_ratio(theme_text, theme_bg)
            
            if contrast_ratio < LayoutValidator.MIN_CONTRAST_NORMAL_TEXT:
                issues.append(LayoutIssue(
                    severity="error",
                    category="color_contrast",
                    message=f"CRITICAL: Theme text color '{theme_text}' has insufficient contrast ({contrast_ratio:.2f}:1) against background '{theme_bg}'. WCAG AA requires 4.5:1 for normal text.",
                    affected_widgets=["theme"],
                    suggestion=f"Change theme colors: use light text (#ffffff, #f5f5f5) on dark backgrounds (#0a0a0a, #1a1a1a), OR dark text (#000000, #1a1a1a) on light backgrounds (#ffffff, #fafafa). Current contrast {contrast_ratio:.2f}:1 is below minimum 4.5:1."
                ))
        
        for assignment in layout.widget_assignments:
            fg_color = assignment.applied_style.get('color', '')
            bg_color = assignment.applied_style.get('background', '') or \
                      assignment.applied_style.get('background-color', '')
            
            if fg_color and bg_color:
                # Check WCAG AA contrast ratio
                contrast_ratio = LayoutValidator._calculate_contrast_ratio(fg_color, bg_color)
                
                if contrast_ratio < LayoutValidator.MIN_CONTRAST_NORMAL_TEXT:
                    issues.append(LayoutIssue(
                        severity="error" if contrast_ratio < LayoutValidator.MIN_CONTRAST_LARGE_TEXT else "warning",
                        category="color_contrast",
                        message=f"Low contrast ({contrast_ratio:.2f}:1): widget '{assignment.role}' text '{fg_color}' on background '{bg_color}' fails WCAG AA (requires 4.5:1 for normal text)",
                        affected_widgets=[assignment.role],
                        suggestion=f"Increase contrast for widget '{assignment.role}': use light text (#ffffff) on dark backgrounds (#000000), or dark text (#000000) on light backgrounds (#ffffff). Current {contrast_ratio:.2f}:1 is below minimum 4.5:1."
                    ))
                
                # Also check similarity-based detection (legacy)
                similarity = LayoutValidator._color_similarity(fg_color, bg_color)
                
                if similarity > LayoutValidator.COLOR_SIMILARITY_THRESHOLD and contrast_ratio >= LayoutValidator.MIN_CONTRAST_NORMAL_TEXT:
                    # Colors are similar but pass WCAG - still warn
                    issues.append(LayoutIssue(
                        severity="warning",
                        category="color_contrast",
                        message=f"Colors very similar in widget '{assignment.role}': '{fg_color}' and '{bg_color}' (contrast {contrast_ratio:.2f}:1 passes WCAG but may be hard to read)",
                        affected_widgets=[assignment.role],
                        suggestion=f"Consider increasing color difference for better readability in widget '{assignment.role}'."
                    ))
        
        return issues
    
    @staticmethod
    def _calculate_contrast_ratio(color1: str, color2: str) -> float:
        """Calculate WCAG contrast ratio between two colors.
        
        Args:
            color1: CSS color string (text)
            color2: CSS color string (background)
            
        Returns:
            Contrast ratio (1-21, where 21 is black on white)
        """
        try:
            rgb1 = LayoutValidator._parse_color(color1)
            rgb2 = LayoutValidator._parse_color(color2)
            
            if not rgb1 or not rgb2:
                return 21.0  # Assume maximum contrast if parsing fails
            
            # Calculate relative luminance
            lum1 = LayoutValidator._relative_luminance(rgb1)
            lum2 = LayoutValidator._relative_luminance(rgb2)
            
            # Contrast ratio formula
            lighter = max(lum1, lum2)
            darker = min(lum1, lum2)
            
            return (lighter + 0.05) / (darker + 0.05)
        except:
            return 21.0  # Assume maximum contrast on error
    
    @staticmethod
    def _relative_luminance(rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance for WCAG contrast.
        
        Args:
            rgb: (r, g, b) tuple with values 0-255
            
        Returns:
            Relative luminance (0-1)
        """
        # Convert to 0-1 range
        r, g, b = [x / 255.0 for x in rgb]
        
        # Apply gamma correction
        def gamma_correct(c):
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4
        
        r = gamma_correct(r)
        g = gamma_correct(g)
        b = gamma_correct(b)
        
        # Calculate luminance using sRGB coefficients
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @staticmethod
    def _check_content_density(layout: RenderableLayout) -> List[LayoutIssue]:
        """Detect insufficient content to fill the slide.
        
        Args:
            layout: RenderableLayout to check
            
        Returns:
            List of content density issues
        """
        issues = []
        
        # Calculate total widget area vs. total slide area
        total_area = layout.width * layout.height
        widget_area = sum(
            assignment.bounds.width * assignment.bounds.height
            for assignment in layout.widget_assignments
        )
        
        density = widget_area / total_area if total_area > 0 else 0
        
        if density < LayoutValidator.MIN_CONTENT_DENSITY:
            widget_roles = [a.role for a in layout.widget_assignments]
            issues.append(LayoutIssue(
                severity="warning",
                category="content_density",
                message=f"Low content density ({density:.1%}): slide appears empty with only {len(layout.widget_assignments)} widgets covering {density:.1%} of space",
                affected_widgets=widget_roles,
                suggestion=f"Add more content widgets or use a layout with fewer, larger slots. Current layout '{layout.strategy_name}' may not be optimal for this amount of content. Consider using Cinematic.FullBleed or Swiss.Poster for minimal content."
            ))
        
        return issues
    
    @staticmethod
    def _check_overlaps(layout: RenderableLayout) -> List[LayoutIssue]:
        """Detect overlapping widgets (indicates content overflow).
        
        Args:
            layout: RenderableLayout to check
            
        Returns:
            List of overlap issues
        """
        issues = []
        assignments = layout.widget_assignments
        
        for i, a1 in enumerate(assignments):
            for a2 in assignments[i+1:]:
                overlap = LayoutValidator._calculate_overlap(a1, a2)
                
                if overlap > LayoutValidator.OVERLAP_TOLERANCE:
                    issues.append(LayoutIssue(
                        severity="error",
                        category="overlap",
                        message=f"Widgets '{a1.role}' and '{a2.role}' overlap by {overlap}px - likely due to content overflow",
                        affected_widgets=[a1.role, a2.role],
                        suggestion=f"Reduce text length in widgets '{a1.role}' and/or '{a2.role}'. Content is too long for assigned space. Cut text by 30-50% or use shorter words."
                    ))
        
        return issues
    
    @staticmethod
    def _check_style_consistency(layout: RenderableLayout) -> List[LayoutIssue]:
        """Detect inconsistent styling of same widget types.
        
        Args:
            layout: RenderableLayout to check
            
        Returns:
            List of style consistency issues
        """
        issues = []
        
        # Group widgets by type
        widgets_by_type: Dict[str, List[WidgetAssignment]] = {}
        for assignment in layout.widget_assignments:
            widget_type = assignment.widget.get_widget_type()
            if widget_type not in widgets_by_type:
                widgets_by_type[widget_type] = []
            widgets_by_type[widget_type].append(assignment)
        
        # Check for style variations within same type
        for widget_type, assignments in widgets_by_type.items():
            if len(assignments) < 2:
                continue  # Need at least 2 widgets of same type
            
            # Compare presets
            presets = [a.preset for a in assignments if a.preset]
            if len(set(str(p) for p in presets)) > 1:
                roles = [a.role for a in assignments]
                issues.append(LayoutIssue(
                    severity="warning",
                    category="style_consistency",
                    message=f"Inconsistent presets for {widget_type} widgets: {roles}",
                    affected_widgets=roles,
                    suggestion=f"Use consistent visual presets for all {widget_type} widgets on same slide. Either apply same preset to all, or use 'set_preset' for global consistency."
                ))
        
        return issues
    
    @staticmethod
    def _color_similarity(color1: str, color2: str) -> float:
        """Calculate color similarity (0 = different, 1 = identical).
        
        Args:
            color1: CSS color string (hex, rgb, or color name)
            color2: CSS color string
            
        Returns:
            Similarity score 0-1
        """
        try:
            # Simple approximation: compare hex values if available
            # For more accuracy, would convert to Lab color space
            c1 = LayoutValidator._parse_color(color1)
            c2 = LayoutValidator._parse_color(color2)
            
            if c1 and c2:
                # Calculate Euclidean distance in RGB space
                r_diff = (c1[0] - c2[0]) ** 2
                g_diff = (c1[1] - c2[1]) ** 2
                b_diff = (c1[2] - c2[2]) ** 2
                distance = (r_diff + g_diff + b_diff) ** 0.5
                max_distance = (255**2 + 255**2 + 255**2) ** 0.5
                
                # Convert to similarity (1 - normalized distance)
                return 1 - (distance / max_distance)
            
            return 0.0
        except:
            return 0.0
    
    @staticmethod
    def _parse_color(color: str) -> Tuple[int, int, int] | None:
        """Parse CSS color to RGB tuple.
        
        Args:
            color: CSS color string
            
        Returns:
            (r, g, b) tuple or None if parsing fails
        """
        color = color.strip().lower()
        
        # Handle hex colors
        if color.startswith('#'):
            hex_color = color[1:]
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return (r, g, b)
            elif len(hex_color) == 3:
                r = int(hex_color[0] * 2, 16)
                g = int(hex_color[1] * 2, 16)
                b = int(hex_color[2] * 2, 16)
                return (r, g, b)
        
        # Handle rgb/rgba
        if color.startswith('rgb'):
            import re
            match = re.search(r'rgb\w*\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color)
            if match:
                return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        
        return None
    
    @staticmethod
    def _calculate_overlap(a1: WidgetAssignment, a2: WidgetAssignment) -> int:
        """Calculate overlap area between two widget assignments.
        
        Args:
            a1: First widget assignment
            a2: Second widget assignment
            
        Returns:
            Overlap area in pixels
        """
        # Calculate intersection rectangle
        x_left = max(a1.bounds.x, a2.bounds.x)
        y_top = max(a1.bounds.y, a2.bounds.y)
        x_right = min(a1.bounds.x + a1.bounds.width, a2.bounds.x + a2.bounds.width)
        y_bottom = min(a1.bounds.y + a1.bounds.height, a2.bounds.y + a2.bounds.height)
        
        if x_right > x_left and y_bottom > y_top:
            return (x_right - x_left) * (y_bottom - y_top)
        
        return 0


def format_issues_for_llm(issues: List[LayoutIssue]) -> str:
    """Format validation issues as feedback for LLM refinement.
    
    Args:
        issues: List of detected issues
        
    Returns:
        Formatted feedback string
    """
    if not issues:
        return ""
    
    feedback = "**LAYOUT VALIDATION ISSUES DETECTED**\n\n"
    feedback += f"Found {len(issues)} issue(s) that need correction:\n\n"
    
    for i, issue in enumerate(issues, 1):
        feedback += f"{i}. [{issue.severity.upper()}] {issue.category}\n"
        feedback += f"   Problem: {issue.message}\n"
        feedback += f"   Affected: {', '.join(issue.affected_widgets)}\n"
        feedback += f"   Fix: {issue.suggestion}\n\n"
    
    feedback += "\n**REQUIRED ACTION**:\n"
    feedback += "Generate a new patch that addresses these issues. Focus on:\n"
    
    # Categorize issues
    has_overlap = any(i.category == "overlap" for i in issues)
    has_contrast = any(i.category == "color_contrast" for i in issues)
    has_density = any(i.category == "content_density" for i in issues)
    has_consistency = any(i.category == "style_consistency" for i in issues)
    
    if has_overlap:
        feedback += "- SHORTEN TEXT in overlapping widgets by 40-60%\n"
    if has_contrast:
        feedback += "- ADJUST COLORS to improve contrast (use theme variables)\n"
    if has_density:
        feedback += "- ADD MORE WIDGETS or SWITCH TO SIMPLER LAYOUT\n"
    if has_consistency:
        feedback += "- APPLY CONSISTENT PRESETS to widgets of same type\n"
    
    return feedback
