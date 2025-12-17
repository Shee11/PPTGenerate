"""Integration tests for CLI generation workflow with --source flag.

Tests verify that the CLI correctly:
1. Accepts --source, --user-instruction, --use-cache flags
2. Calls generation orchestrator when --source is provided
3. Integrates generated slides with LayoutEngine and HTMLRenderer
"""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from cli.uce_render import cli
from src.common.slides import Slides


@pytest.fixture
def runner():
    """Click test runner."""
    return CliRunner()


@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file for testing."""
    text_file = tmp_path / "test_source.txt"
    text_file.write_text(
        "Artificial Intelligence is transforming industries.\n"
        "Machine learning algorithms learn from data.\n"
        "Deep learning uses neural networks with multiple layers."
    )
    return text_file


@pytest.fixture
def sample_vtt_file(tmp_path):
    """Create a sample VTT subtitle file for testing."""
    vtt_file = tmp_path / "test_source.vtt"
    vtt_file.write_text(
        "WEBVTT\n\n"
        "00:00:00.000 --> 00:00:05.000\n"
        "Welcome to AI fundamentals\n\n"
        "00:00:05.000 --> 00:00:10.000\n"
        "Today we explore neural networks\n"
    )
    return vtt_file


@pytest.fixture
def mock_slides():
    """Create mock slides for testing."""
    slides = Slides(id="test_slides")
    # Use MagicMock for slide to avoid Pydantic validation
    # Add directly to _contexts to bypass validation
    mock_slide = MagicMock()
    mock_slide.id = "slide_1"
    mock_slide.rank = 0
    slides._contexts["slide_1"] = mock_slide
    return slides


class TestCLIFlags:
    """Test CLI flag parsing and validation."""
    
    def test_source_flag_accepts_txt_file(self, runner, sample_text_file, mock_slides):
        """Test that --source flag accepts .txt files."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    mock_generate.assert_called_once()
                    # Verify it was called with the source path
                    call_args = mock_generate.call_args
                    assert call_args.kwargs['source_path'] == sample_text_file
    
    def test_source_flag_accepts_vtt_file(self, runner, sample_vtt_file, mock_slides):
        """Test that --source flag accepts .vtt files."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_vtt_file),
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    mock_generate.assert_called_once()
    
    def test_user_instruction_flag(self, runner, sample_text_file, mock_slides):
        """Test that --user-instruction flag is accepted."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    instruction = 'Focus on technical concepts'
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--user-instruction', instruction,
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    # Verify user instruction was passed
                    call_args = mock_generate.call_args
                    assert call_args.kwargs.get('user_instruction') == instruction
    
    def test_use_cache_flag_default_true(self, runner, sample_text_file, mock_slides):
        """Test that --use-cache defaults to true."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    # Verify use_cache=True by default
                    call_args = mock_generate.call_args
                    assert call_args.kwargs.get('use_cache') is True
    
    def test_use_cache_flag_false(self, runner, sample_text_file, mock_slides):
        """Test that --use-cache=false works."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--use-cache', 'false',
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    # Verify use_cache=False
                    call_args = mock_generate.call_args
                    assert call_args.kwargs.get('use_cache') is False


class TestOrchestratorIntegration:
    """Test CLI integration with generation orchestrator."""
    
    def test_orchestrator_called_with_source(self, runner, sample_text_file, mock_slides):
        """Test that orchestrator is called when --source provided."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    mock_generate.assert_called_once()
                    
                    # Verify correct parameters
                    call_args = mock_generate.call_args
                    assert call_args.kwargs['source_path'] == sample_text_file
                    assert call_args.kwargs['use_cache'] is True
    
    def test_orchestrator_respects_cache_flag(self, runner, sample_text_file, mock_slides):
        """Test that orchestrator respects --use-cache flag."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--use-cache', 'false',
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    call_args = mock_generate.call_args
                    assert call_args.kwargs['use_cache'] is False


class TestRenderingIntegration:
    """Test CLI integration with LayoutEngine and HTMLRenderer."""
    
    def test_generated_slides_feed_to_layout_engine(self, runner, sample_text_file, mock_slides):
        """Test that generated Slides are passed to LayoutEngine."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    mock_engine.calculate_slides.assert_called_once()
    
    def test_html_output_written_to_file(self, runner, sample_text_file, mock_slides, tmp_path):
        """Test that HTML output is written to specified file."""
        output_file = tmp_path / "output.html"
        
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    html_content = "<html><body>Test Slides</body></html>"
                    mock_renderer.render.return_value = html_content
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--output', str(output_file)
                    ])
                    
                    assert result.exit_code == 0
                    assert output_file.exists()
                    assert output_file.read_text() == html_content


class TestErrorHandling:
    """Test CLI error handling for generation workflow."""
    
    def test_missing_source_file(self, runner):
        """Test error handling when source file doesn't exist."""
        result = runner.invoke(cli, [
            '--source', 'nonexistent.txt',
            '--output', 'test.html'
        ])
        
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower() or "not found" in result.output.lower()
    
    def test_unsupported_file_type(self, runner, tmp_path, mock_slides):
        """Test that unsupported file types are handled gracefully."""
        unsupported_file = tmp_path / "test.pdf"
        unsupported_file.write_text("dummy content")
        
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(unsupported_file),
                        '--output', 'test.html'
                    ])
                    
                    # Should succeed - orchestrator treats unknown as text/plain
                    assert result.exit_code == 0
    
    def test_empty_source_file(self, runner, tmp_path):
        """Test error handling for empty source files."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            mock_generate.side_effect = ValueError("Source file is empty")
            
            result = runner.invoke(cli, [
                '--source', str(empty_file),
                '--output', 'test.html'
            ])
            
            assert result.exit_code != 0
    
    def test_generation_failure_handling(self, runner, sample_text_file):
        """Test error handling when generation fails."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            mock_generate.side_effect = Exception("LLM API error")
            
            result = runner.invoke(cli, [
                '--source', str(sample_text_file),
                '--output', 'test.html'
            ])
            
            assert result.exit_code != 0
            assert "error" in result.output.lower()


class TestWidthHeightIntegration:
    """Test that --width and --height flags work with --source."""
    
    def test_width_height_passed_to_layout_engine(self, runner, sample_text_file, mock_slides):
        """Test that width/height are passed to LayoutEngine when using --source."""
        with patch('cli.uce_render.generate_from_file') as mock_generate:
            with patch('cli.uce_render.LayoutEngine') as mock_engine_class:
                with patch('cli.uce_render.HTMLRenderer') as mock_renderer_class:
                    mock_generate.return_value = mock_slides
                    
                    mock_engine = MagicMock()
                    mock_engine.calculate_slides.return_value = [MagicMock()]
                    mock_engine_class.calculate_slides = mock_engine.calculate_slides
                    
                    mock_renderer = MagicMock()
                    mock_renderer.render.return_value = "<html></html>"
                    mock_renderer_class.return_value = mock_renderer
                    
                    result = runner.invoke(cli, [
                        '--source', str(sample_text_file),
                        '--width', '3840',
                        '--height', '2160',
                        '--output', 'test.html'
                    ])
                    
                    assert result.exit_code == 0
                    # Verify LayoutEngine.calculate_slides called with correct dimensions
                    call_args = mock_engine.calculate_slides.call_args
                    assert call_args.kwargs.get('width') == 3840
                    assert call_args.kwargs.get('height') == 2160




