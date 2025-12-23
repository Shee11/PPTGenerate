"""Todo package for task queue based pipeline execution.

Architecture:
    todos = planner.plan(state, user_instruction)
    for todo in todos:
        executor.execute_todo(todo, state, user_instruction)

All tools follow unified protocol and are SELF-DESCRIBING:
    context = tool.slice(state)
    patch = tool.generate(constitution, context, user_instruction)
    tool.apply(state, patch)

Planner uses get_all_descriptions() to understand all tools.

NOTE: Tools have been moved to src/tools/ (each tool in its own file).
      Tool protocol has been moved to src/common/tool_protocol.py.
"""
from src.generation.todo.models import (
    TodoType,
    TodoStatus,
    TodoItem,
    TodoQueue,
    ConstitutionPatch,
    AtomsParams,
    ThemeParams,
    AtomFilter,
    StoryParams,
    ContentParams,
    ExportParams,
)
from src.generation.todo.planner import plan
from src.generation.todo.executor import TodoExecutor
from src.generation.todo.runner import PipelineRunner, generate_slides

# Re-export tool protocol from new location (src/common/tool_protocol.py)
from src.common.tool_protocol import (
    Tool, DirectTool, LLMTool,
    ToolContext, ToolPatch,
    ToolDescription,
    get_tool, get_all_tools, get_all_descriptions, get_all_descriptions_structured,
    register_tool,
)

# Import tools to register them (all tools now in src/tools/)
from src.tools import constitution as _constitution  # noqa: F401
from src.tools import atoms as _atoms  # noqa: F401
from src.tools import theme as _theme  # noqa: F401
from src.tools import story as _story  # noqa: F401
from src.tools import content as _content  # noqa: F401
from src.tools import export as _export  # noqa: F401

__all__ = [
    # Models
    "TodoType",
    "TodoStatus", 
    "TodoItem",
    "TodoQueue",
    "ConstitutionPatch",
    "AtomsParams",
    "ThemeParams",
    "AtomFilter",
    "ContentParams",
    "ExportParams",
    # Planner
    "plan",
    # Executor
    "TodoExecutor",
    # Runner
    "PipelineRunner",
    "generate_slides",
    # Tool Protocol
    "Tool",
    "DirectTool",
    "LLMTool",
    "ToolDescription",
    "get_tool",
    "get_all_tools",
    "get_all_descriptions",
    "get_all_descriptions_structured",
    "register_tool",
]
