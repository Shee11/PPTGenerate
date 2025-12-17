"""Integration tests verifying LLM-generated layouts render correctly through existing pipeline."""
import json
import pytest
from unittest.mock import patch

from src.generation.atom.collection import AtomCollection
from src.generation.atom.models import StatementAtom, ProcessAtom, ProcessStep
from src.generation.content.generator import generate_layout
from src.common.source import SourceReference
from src.common.slides import Slides
from src.common.slide import Slide
from src.utils.generation_config import GenerationConfig
from src.common.patchable_context_pydantic import Patch, AddOperation
from src.layout.layout_engine import LayoutEngine
from src.layout.theme import Theme
from src.layout.style import Style
from src.render.html_renderer import HTMLRenderer


class TestLayoutEngineIntegration:
    """Test LayoutEngine accepts and processes generated Slides."""

    @patch('src.generation.content.generator.call_llm')
    def test_layout_engine_accepts_generated_slides(self, mock_llm):
        """Verify LayoutEngine.calculate_slides() accepts LLM-generated Slides."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_001")
        atom = StatementAtom(
            id="stmt_001",
            rank=1,
            text="AI is transforming industries",
            source_ref=SourceReference(
                source_id="src_001",
                file_path="/test.txt",
                offset=0,
                length=30
            )
        )
        atoms.patch(Patch(operations=[AddOperation(add=atom)]))

        # Mock LLM responses for two-step generation
        state_transition_patch = [
            {
                "add": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "draft",
                    "strategy": "Bento.Standard",
                    "widgets": {},
                    "parameters": {}
                }
            }
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {
                            "type": "Type.Display",
                            "parameters": {"text": "AI Revolution"}
                        },
                        "cell_2": {
                            "type": "Type.Body",
                            "parameters": {"text": "AI is transforming industries"}
                        }
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Generate layout
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 1 slide about AI", config, use_cache=False)

        # Verify slides were generated
        assert len(slides.get_active_slides()) == 1

        # Test LayoutEngine.calculate_slides() accepts generated Slides
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )

        renderable_layouts = LayoutEngine.calculate_slides(
            slides=slides,
            theme=theme,
            style=style,
            width=1920,
            height=1080
        )

        # Verify output
        assert len(renderable_layouts) == 1
        renderable = renderable_layouts[0]
        assert renderable.strategy_name == "Bento.Standard"
        assert len(renderable.widget_assignments) == 2  # cell_1 + cell_2

    @patch('src.generation.content.generator.call_llm')
    def test_layout_engine_handles_multiple_slides(self, mock_llm):
        """Verify LayoutEngine.calculate_slides() handles multiple generated slides."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_002")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="First point",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=11)
            )),
            AddOperation(add=StatementAtom(
                id="stmt_002",
                rank=2,
                text="Second point",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=12, length=12)
            ))
        ]))

        # Mock LLM responses for 2 slides
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}},
            {"add": {"id": "slide_002", "rank": 2, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "First"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "First point"}}
                    },
                    "parameters": {}
                }
            },
            {
                "replace": {
                    "id": "slide_002",
                    "rank": 2,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Second"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "Second point"}}
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Generate layouts
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 2 slides", config, use_cache=False)

        # Test LayoutEngine with multiple slides
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )

        renderable_layouts = LayoutEngine.calculate_slides(
            slides=slides,
            theme=theme,
            style=style
        )

        # Verify output
        assert len(renderable_layouts) == 2
        assert renderable_layouts[0].strategy_name == "Bento.Standard"
        assert renderable_layouts[1].strategy_name == "Bento.Standard"


class TestHTMLRendererIntegration:
    """Test HTMLRenderer accepts and renders LayoutEngine output."""

    @patch('src.generation.content.generator.call_llm')
    def test_html_renderer_renders_generated_layout(self, mock_llm):
        """Verify HTMLRenderer.render() accepts LayoutEngine output from generated slides."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_003")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="Quantum computing breakthrough",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=28)
            ))
        ]))

        # Mock LLM responses
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Quantum Leap"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "Quantum computing breakthrough"}}
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Generate layout
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 1 slide", config, use_cache=False)

        # Calculate layout
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)

        # Test HTMLRenderer.render()
        renderer = HTMLRenderer()
        html_output = renderer.render(renderable_layouts[0])

        # Verify HTML output is valid
        assert isinstance(html_output, str)
        assert len(html_output) > 0
        assert "<!DOCTYPE html>" in html_output or "<html" in html_output
        assert "Quantum Leap" in html_output
        assert "Quantum computing breakthrough" in html_output

    @patch('src.generation.content.generator.call_llm')
    def test_html_renderer_multi_slide_rendering(self, mock_llm):
        """Verify HTMLRenderer.render() handles multiple slides from generator."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_004")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="First concept",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=13)
            )),
            AddOperation(add=StatementAtom(
                id="stmt_002",
                rank=2,
                text="Second concept",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=14, length=14)
            ))
        ]))

        # Mock LLM responses for 2 slides
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}},
            {"add": {"id": "slide_002", "rank": 2, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Concept 1"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "First concept"}}
                    },
                    "parameters": {}
                }
            },
            {
                "replace": {
                    "id": "slide_002",
                    "rank": 2,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Concept 2"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "Second concept"}}
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Generate layouts
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 2 slides", config, use_cache=False)

        # Calculate layouts
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)

        # Test HTMLRenderer with list of renderables
        renderer = HTMLRenderer()
        html_output = renderer.render(renderable_layouts)

        # Verify multi-slide HTML output
        assert isinstance(html_output, str)
        assert len(html_output) > 0
        assert "Concept 1" in html_output
        assert "Concept 2" in html_output
        assert "First concept" in html_output
        assert "Second concept" in html_output


class TestHTMLOutputValidation:
    """Test generated HTML output structure and validity."""

    @patch('src.generation.content.generator.call_llm')
    def test_html_output_structure_valid(self, mock_llm):
        """Verify generated HTML has valid structure (DOCTYPE, html, head, body)."""
        # Setup minimal atoms
        atoms = AtomCollection(id="atoms_005")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="Test content",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=12)
            ))
        ]))

        # Mock LLM responses
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Title"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "Test content"}}
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Full pipeline
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 1 slide", config, use_cache=False)
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)
        renderer = HTMLRenderer()
        html_output = renderer.render(renderable_layouts[0])

        # Validate HTML structure
        assert "<!DOCTYPE html>" in html_output or "<html" in html_output
        assert "<head>" in html_output or "<head " in html_output
        assert "<body>" in html_output or "<body " in html_output
        assert "</html>" in html_output

    @patch('src.generation.content.generator.call_llm')
    def test_html_output_contains_widgets(self, mock_llm):
        """Verify generated HTML contains widget content."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_006")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="Widget test content",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=19)
            ))
        ]))

        # Mock LLM with multiple widget types
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Display Widget"}},
                        "cell_2": {"type": "Type.Heading", "parameters": {"text": "Heading Widget", "level": 2}},
                        "cell_3": {"type": "Type.Body", "parameters": {"text": "Widget test content"}}
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Full pipeline
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 1 slide", config, use_cache=False)
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)
        renderer = HTMLRenderer()
        html_output = renderer.render(renderable_layouts[0])

        # Verify widget content in HTML
        assert "Display Widget" in html_output
        assert "Heading Widget" in html_output
        assert "Widget test content" in html_output


class TestStateFilteringInRender:
    """Test that rendering pipeline correctly handles slide states."""

    @patch('src.generation.content.generator.call_llm')
    def test_active_slides_render_correctly(self, mock_llm):
        """Verify ACTIVE slides render through pipeline."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_007")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="Active slide content",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=20)
            ))
        ]))

        # Mock LLM responses (slide transitions to ACTIVE)
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",  # ACTIVE state
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Active"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "Active slide content"}}
                    },
                    "parameters": {}
                }
            }
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Generate and render
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 1 slide", config, use_cache=False)

        # Verify slide is ACTIVE
        active_slides = slides.get_active_slides()
        assert len(active_slides) == 1
        assert active_slides[0].state == "active"

        # Render through pipeline
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)
        assert len(renderable_layouts) == 1

        renderer = HTMLRenderer()
        html_output = renderer.render(renderable_layouts[0])
        assert "Active slide content" in html_output

    def test_draft_slides_filtered_by_layout_engine(self):
        """Verify LayoutEngine.calculate_slides() filters out DRAFT slides."""
        # Create slides manually with mixed states
        slides = Slides(id="slides_001")
        
        # Add DRAFT slide
        draft_slide = Slide(
            id="slide_draft",
            rank=1,
            strategy="Bento.Standard",
            widgets={}
        )
        draft_slide.state = "draft"
        slides.patch(Patch(operations=[AddOperation(add=draft_slide)]))

        # Add ACTIVE slide
        active_slide = Slide(
            id="slide_active",
            rank=2,
            strategy="Bento.Standard",
            widgets={
                "cell_1": {"type": "Type.Display", "parameters": {"text": "Active"}},
                "cell_2": {"type": "Type.Body", "parameters": {"text": "Active content"}}
            }
        )
        active_slide.state = "active"
        slides.patch(Patch(operations=[AddOperation(add=active_slide)]))

        # Verify both slides exist
        all_slides = slides.get_by_rank()
        assert len(all_slides) == 2

        # LayoutEngine should filter to only ACTIVE
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)

        # Only ACTIVE slide should be rendered
        assert len(renderable_layouts) == 1
        # Note: Cannot directly check slide ID, but verify only 1 renderable returned

    @patch('src.generation.content.generator.call_llm')
    def test_mixed_states_only_active_rendered(self, mock_llm):
        """Verify pipeline renders only ACTIVE slides when collection has mixed states."""
        # Setup atoms
        atoms = AtomCollection(id="atoms_008")
        atoms.patch(Patch(operations=[
            AddOperation(add=StatementAtom(
                id="stmt_001",
                rank=1,
                text="First",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=0, length=5)
            )),
            AddOperation(add=StatementAtom(
                id="stmt_002",
                rank=2,
                text="Second",
                source_ref=SourceReference(source_id="src_001", file_path="/test.txt", offset=6, length=6)
            ))
        ]))

        # Mock LLM responses (2 slides, but only 1 transitions to ACTIVE)
        state_transition_patch = [
            {"add": {"id": "slide_001", "rank": 1, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}},
            {"add": {"id": "slide_002", "rank": 2, "state": "draft", "strategy": "Bento.Standard", "widgets": {}, "parameters": {}}}
        ]

        # Only populate slide_001, leave slide_002 in DRAFT
        content_patch = [
            {
                "replace": {
                    "id": "slide_001",
                    "rank": 1,
                    "state": "active",
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {"type": "Type.Display", "parameters": {"text": "Active Only"}},
                        "cell_2": {"type": "Type.Body", "parameters": {"text": "First"}}
                    },
                    "parameters": {}
                }
            }
            # slide_002 stays DRAFT
        ]

        mock_llm.side_effect = [
            json.dumps(state_transition_patch),
            json.dumps(content_patch)
        ]

        # Generate slides
        config = GenerationConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            system_prompt="test",
            user_prompt_template="test"
        )
        slides = generate_layout(atoms, "Create 2 slides", config, use_cache=False)

        # Verify mixed states
        all_slides = slides.get_by_rank()
        assert len(all_slides) == 2
        active_slides = slides.get_active_slides()
        assert len(active_slides) == 1

        # Render - should only render ACTIVE slide
        theme = Theme()
        style = Style(
            theme_name="test",
            widgets={
                "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"},
                "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"},
                "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"},
                "Type.Quote": {"font": "h2", "align": "center", "foreground": "text_color"},
                "Type.List": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.BigNum": {"font": "h1", "align": "center", "foreground": "brand_color"},
                "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"},
                "Data.Trend": {"font": "body", "align": "left", "foreground": "brand_color"},
                "Media.Image": {"fit": "cover"}
            }
        )
        renderable_layouts = LayoutEngine.calculate_slides(slides, theme, style)
        assert len(renderable_layouts) == 1

        renderer = HTMLRenderer()
        html_output = renderer.render(renderable_layouts[0])
        assert "Active Only" in html_output
        assert "First" in html_output





