"""Contract tests for CLI interface."""
import pytest
import json
import tempfile
from pathlib import Path
from click.testing import CliRunner
from cli.uce_render import cli


class TestCLIContract:
    """Test CLI interface contracts (exit codes, error messages, output formats)."""
    
    def test_cli_help_message(self) -> None:
        """Test that CLI provides help message."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "uce-render" in result.output.lower() or "usage" in result.output.lower()
    
    def test_cli_missing_input_file_error(self) -> None:
        """Test that missing input file produces error exit code."""
        runner = CliRunner()
        result = runner.invoke(cli, ['nonexistent.json'])
        
        assert result.exit_code != 0
    
    def test_cli_valid_rendering_success_exit_code(self) -> None:
        """Test that valid rendering produces exit code 0."""
        runner = CliRunner()
        
        # Create valid configuration file with multi-slide format
        config = {
            "theme": {},
            "style": {"theme_name": "default"},
            "slides": [
                {
                    "id": "slide-1",
                    "rank": 0,
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {
                            "type": "Type.Display",
                            "parameters": {"text": "Test"}
                        }
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_file = f.name
        
        try:
            result = runner.invoke(cli, [config_file])
            assert result.exit_code == 0
        finally:
            Path(config_file).unlink()
    
    def test_cli_output_to_file(self) -> None:
        """Test that --output flag writes to specified file."""
        runner = CliRunner()
        
        config = {
            "theme": {},
            "style": {"theme_name": "default"},
            "slides": [
                {
                    "id": "slide-1",
                    "rank": 0,
                    "strategy": "Swiss.Poster",
                    "widgets": {
                        "headline": {
                            "type": "Type.Display",
                            "parameters": {"text": "Hello World"}
                        }
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as config_f:
            json.dump(config, config_f)
            config_file = config_f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as output_f:
            output_file = output_f.name
        
        try:
            result = runner.invoke(cli, [config_file, '--output', output_file])
            assert result.exit_code == 0
            
            # Verify output file was created
            assert Path(output_file).exists()
            
            # Verify it contains HTML
            content = Path(output_file).read_text(encoding='utf-8')
            assert "<!DOCTYPE html>" in content
            assert "Hello World" in content
        finally:
            Path(config_file).unlink()
            if Path(output_file).exists():
                Path(output_file).unlink()
    
    def test_cli_validation_mode(self) -> None:
        """Test that --validate-only flag validates without rendering."""
        runner = CliRunner()
        
        config = {
            "theme": {},
            "style": {"theme_name": "default"},
            "slides": [
                {
                    "id": "slide-1",
                    "rank": 0,
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "cell_1": {
                            "type": "Type.Body",
                            "parameters": {"text": "Test"}
                        }
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_file = f.name
        
        try:
            result = runner.invoke(cli, [config_file, '--validate-only'])
            assert result.exit_code == 0
            assert "valid" in result.output.lower() or "ok" in result.output.lower()
        finally:
            Path(config_file).unlink()
    
    def test_cli_invalid_json_error_message(self) -> None:
        """Test that invalid JSON produces clear error message."""
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json ")
            invalid_file = f.name
        
        try:
            result = runner.invoke(cli, [invalid_file])
            assert result.exit_code != 0
            assert "json" in result.output.lower() or "parse" in result.output.lower()
        finally:
            Path(invalid_file).unlink()
    
    def test_cli_size_constraint_error_message(self) -> None:
        """Test that size constraint violations produce helpful error messages."""
        runner = CliRunner()
        
        # Create configuration with hypothetical size violation
        # Since all current widgets require S, we can't create real violation
        # This tests the error handling path
        config = {
            "theme": {},
            "style": {"theme_name": "default"},
            "slides": [
                {
                    "id": "slide-1",
                    "rank": 0,
                    "strategy": "Bento.Standard",
                    "widgets": {
                        "invalid_role": {  # Invalid role should trigger error
                            "type": "Type.Display",
                            "parameters": {"text": "Test"}
                        }
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_file = f.name
        
        try:
            result = runner.invoke(cli, [config_file])
            assert result.exit_code != 0
        finally:
            Path(config_file).unlink()
