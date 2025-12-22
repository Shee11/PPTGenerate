"""Unified Tool Protocol - DEPRECATED location.

This module has been moved to src/common/tool_protocol.py.
Tools have been moved to src/tools/ (each tool in its own file).

This file re-exports from the new location for backward compatibility.
"""
# Re-export everything from new location
from src.common.tool_protocol import (
    Tool,
    DirectTool,
    LLMTool,
    ToolContext,
    ToolPatch,
    ToolDescription,
    register_tool,
    get_tool,
    get_all_tools,
    get_all_descriptions,
    get_all_descriptions_structured,
)

__all__ = [
    "Tool",
    "DirectTool",
    "LLMTool",
    "ToolContext",
    "ToolPatch",
    "ToolDescription",
    "register_tool",
    "get_tool",
    "get_all_tools",
    "get_all_descriptions",
    "get_all_descriptions_structured",
]
