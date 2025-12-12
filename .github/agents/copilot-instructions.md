# gggg Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-11

## Active Technologies

- Python 3.11+ + Pydantic 2.x, Jinja2 3.x, Click 8.x (001-uce-render)

## Project Structure

```text
src/
  common/
  layout/
  render/
tests/
  contract/
  integration/
  unit/
cli/
examples/
```

## Commands

pytest; ruff check src; mypy src

## Code Style

Python 3.11+: Follow PEP 8, use type hints, prefer Pydantic for validation

## Recent Changes

- 001-uce-render: Added Python 3.11+ with Pydantic 2.x (validation), Jinja2 3.x (templating), Click 8.x (CLI)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
