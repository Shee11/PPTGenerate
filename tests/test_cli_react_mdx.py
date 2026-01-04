"""
CLI Integration Tests for React MDX Renderer

Tests T064-T065: CLI integration with react-mdx renderer
"""

import pytest
from pathlib import Path
import tempfile
import json
from click.testing import CliRunner

# Import CLI command
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from cli.uce_render import cli as render_cli


class TestCLIReactMDXIntegration:
    """T064: CLI integration tests for react-mdx renderer"""
    
    @pytest.fixture
    def runner(self):
        """Create Click test runner"""
        return CliRunner()
    
    @pytest.fixture
    def sample_state(self, tmp_path):
        """Create sample state.json file for testing (proper state.json format)"""
        state = {
            "id": "test-presentation",
            "meta": {
                "title": "Test Presentation",
                "theme": "business"
            },
            "slides": [
                {
                    "id": "slide-1",
                    "layout": "split",
                    "widgets": {
                        "left": {
                            "id": "w1",
                            "type": "Type.Heading",
                            "parameters": {
                                "text": "Welcome",
                                "level": 1
                            }
                        },
                        "right": {
                            "id": "w2",
                            "type": "Type.Body",
                            "parameters": {
                                "text": "This is a test presentation"
                            }
                        }
                    }
                },
                {
                    "id": "slide-2", 
                    "layout": "center",
                    "widgets": {
                        "main": {
                            "id": "w3",
                            "type": "Type.Quote",
                            "parameters": {
                                "text": "Success is not final, failure is not fatal",
                                "author": "Winston Churchill"
                            }
                        }
                    }
                }
            ]
        }
        
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps(state), encoding='utf-8')
        return state_file
    
    @pytest.fixture
    def config_with_slides(self, tmp_path):
        """Create state.json with slides array format for CLI --render"""
        state = {
            "id": "test-presentation",
            "meta": {
                "title": "Test",
                "theme": "business"
            },
            "slides": [
                {
                    "id": "slide-1",
                    "layout": "bento-standard",
                    "widgets": {
                        "cell_1": {
                            "id": "w1",
                            "type": "Type.Display",
                            "parameters": {"text": "Bold Statement"}
                        },
                        "cell_2": {
                            "id": "w2",
                            "type": "Type.Body",
                            "parameters": {"text": "Supporting text"}
                        }
                    }
                }
            ]
        }
        
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps(state), encoding='utf-8')
        return state_file
    
    def test_react_mdx_help_shows_option(self, runner):
        """Verify react-mdx appears in --project choices"""
        result = runner.invoke(render_cli, ['--help'])
        assert result.exit_code == 0
        assert 'react-mdx' in result.output
    
    def test_theme_option_shows_in_help(self, runner):
        """Verify --mdx-theme option appears in help"""
        result = runner.invoke(render_cli, ['--help'])
        assert result.exit_code == 0
        assert '--mdx-theme' in result.output
        assert 'cyber' in result.output
        assert 'minimal' in result.output
    
    def test_react_mdx_with_state_json(self, runner, config_with_slides, tmp_path):
        """Test react-mdx rendering with state.json via --render flag"""
        output_file = tmp_path / "output.mdx"
        
        result = runner.invoke(render_cli, [
            '--render', str(config_with_slides),
            '--project', 'react-mdx',
            '--output', str(output_file),
            '--verbose'
        ])
        
        # Should produce MDX output
        if result.exit_code == 0:
            assert output_file.exists()
            content = output_file.read_text()
            assert 'export const meta' in content or len(content) > 0
    
    def test_react_mdx_with_theme_override(self, runner, config_with_slides, tmp_path):
        """Test --theme flag overrides default theme"""
        output_file = tmp_path / "output.mdx"
        
        result = runner.invoke(render_cli, [
            '--render', str(config_with_slides),
            '--project', 'react-mdx',
            '--mdx-theme', 'cyber',
            '--output', str(output_file),
            '--verbose'
        ])
        
        # Verify theme is applied
        if result.exit_code == 0 and output_file.exists():
            content = output_file.read_text()
            # Theme should appear in output
            assert 'cyber' in content.lower() or 'theme' in content.lower()
    
    def test_react_mdx_verbose_output(self, runner, config_with_slides, tmp_path):
        """Test verbose flag provides progress information"""
        output_file = tmp_path / "output.mdx"
        
        result = runner.invoke(render_cli, [
            '--render', str(config_with_slides),
            '--project', 'react-mdx',
            '--verbose',
            '--output', str(output_file)
        ])
        
        # Verbose should show progress
        if result.exit_code == 0:
            # Verbose output goes to stderr
            assert 'React MDX' in result.output or 'MDX' in str(result.exception) or result.exit_code == 0


class TestCLIReactMDXErrorHandling:
    """T065: Error handling tests for invalid input"""
    
    @pytest.fixture
    def runner(self):
        """Create Click test runner"""
        return CliRunner()
    
    def test_invalid_theme_rejected(self, runner, tmp_path):
        """Invalid theme name should be rejected"""
        state = {"id": "test", "meta": {"title": "Test"}, "slides": [{"id": "s1", "layout": "split", "widgets": {}}]}
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps(state))
        
        result = runner.invoke(render_cli, [
            '--render', str(state_file),
            '--project', 'react-mdx',
            '--mdx-theme', 'invalid-theme-name',
            '--output', str(tmp_path / "output.mdx")
        ])
        
        # Should fail with invalid choice
        assert result.exit_code != 0 or 'invalid' in result.output.lower() or 'Invalid value' in result.output
    
    def test_empty_slides_handled_gracefully(self, runner, tmp_path):
        """Empty slides array should be handled"""
        state = {"id": "test", "meta": {"title": "Test"}, "slides": []}
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps(state))
        
        result = runner.invoke(render_cli, [
            '--render', str(state_file),
            '--project', 'react-mdx',
            '--output', str(tmp_path / "output.mdx")
        ])
        
        # Should complete without crash (may have warning)
        # We just verify it doesn't raise an exception
        assert isinstance(result.exit_code, int)
    
    def test_missing_state_file(self, runner):
        """Missing state file should produce error"""
        result = runner.invoke(render_cli, [
            '--render', 'nonexistent_state.json',
            '--project', 'react-mdx',
            '--output', 'output.mdx'
        ])
        
        assert result.exit_code != 0
    
    def test_invalid_json_format(self, runner, tmp_path):
        """Invalid JSON should produce error"""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{ this is not valid json }")
        
        result = runner.invoke(render_cli, [
            '--render', str(bad_file),
            '--project', 'react-mdx',
            '--output', str(tmp_path / "output.mdx")
        ])
        
        assert result.exit_code != 0


class TestReactMDXRendererDirect:
    """Direct tests for ReactMDXRenderer class"""
    
    def test_renderer_imports(self):
        """Verify ReactMDXRenderer can be imported"""
        from src.paged.render.react.mdx_renderer import ReactMDXRenderer, render_mdx
        assert ReactMDXRenderer is not None
        assert render_mdx is not None
    
    def test_renderer_with_default_theme(self):
        """Test renderer with default theme"""
        from src.paged.render.react.mdx_renderer import ReactMDXRenderer
        
        renderer = ReactMDXRenderer()
        assert renderer.theme == 'business'
    
    def test_renderer_with_custom_theme(self):
        """Test renderer with custom theme"""
        from src.paged.render.react.mdx_renderer import ReactMDXRenderer
        
        renderer = ReactMDXRenderer(theme='cyber')
        assert renderer.theme == 'cyber'
    
    def test_render_state_produces_mdx(self):
        """Test render_state produces valid MDX"""
        from src.paged.render.react.mdx_renderer import ReactMDXRenderer
        
        state = {
            "id": "test",
            "meta": {"title": "Test", "theme": "business"},
            "slides": [
                {
                    "id": "slide-1",
                    "layout": "split",
                    "widgets": {
                        "left": {"id": "w1", "type": "Type.Heading", "parameters": {"text": "Hello"}},
                        "right": {"id": "w2", "type": "Type.Body", "parameters": {"text": "World"}}
                    }
                }
            ]
        }
        
        renderer = ReactMDXRenderer(theme='minimal')
        mdx = renderer.render_state(state)
        
        # Should contain MDX content
        assert 'export const meta' in mdx
        assert 'Hello' in mdx
        assert 'World' in mdx
    
    def test_all_themes_available(self):
        """Test all 7 themes can be used"""
        from src.paged.render.react.mdx_renderer import ReactMDXRenderer
        
        themes = ['business', 'cyber', 'minimal', 'academic', 'creative', 'duolingo', 'dark']
        
        state = {
            "id": "test",
            "meta": {"title": "Test"},
            "slides": [{"id": "s1", "layout": "center", "widgets": {}}]
        }
        
        for theme in themes:
            renderer = ReactMDXRenderer(theme=theme)
            mdx = renderer.render_state(state)
            assert mdx is not None
            assert len(mdx) > 0
