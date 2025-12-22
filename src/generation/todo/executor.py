"""Todo Executor using unified Tool protocol.

All tools follow:
1. context = tool.slice(state)
2. patch = tool.generate(constitution, context, instruction)
3. tool.apply(state, patch)

Tools are self-describing - planner uses get_all_descriptions().
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Dict

if TYPE_CHECKING:
    from src.generation.state import PipelineState
from src.generation.todo.models import (
    TodoItem,
    TodoType,
    TodoStatus,
)
from src.generation.todo.tool_protocol import get_tool, Tool

logger = logging.getLogger(__name__)


class TodoExecutor:
    """Executes todos using the unified Tool protocol.
    
    Usage:
        executor = TodoExecutor(verbose=True)
        executor.execute_all(state, user_instruction)
    """
    
    def __init__(
        self,
        use_cache: bool = True,
        verbose: bool = False,
        output_dir: Optional[Path] = None,
    ):
        self.use_cache = use_cache
        self.verbose = verbose
        self.output_dir = output_dir or Path("output")
        
        # Tool name mapping
        self._tool_names: Dict[TodoType, str] = {
            TodoType.CONSTITUTION: "constitution",
            TodoType.ATOMS: "atoms",
            TodoType.THEME: "theme",
            TodoType.CONTENT: "content",
            TodoType.EXPORT: "export",
        }
    
    def execute_all(
        self,
        state: PipelineState,
        user_instruction: str,
        stop_on_error: bool = True,
    ) -> int:
        """Execute all pending todos.
        
        Args:
            state: Pipeline state
            user_instruction: User's instruction (passed to tools)
            stop_on_error: Stop on first error
        
        Returns:
            Number of todos executed
        """
        count = 0
        while state.has_pending_todos():
            todo = state.get_next_todo()
            if todo is None:
                pending = state.todos.get_pending()
                if pending:
                    logger.warning(f"Stuck: {len(pending)} pending, none ready")
                break
            
            try:
                self.execute_todo(todo, state, user_instruction)
                count += 1
            except Exception as e:
                if stop_on_error:
                    raise
                logger.error(f"Todo failed: {e}")
        
        return count
    
    def execute_todo(
        self,
        todo: TodoItem,
        state: PipelineState,
        user_instruction: str,
    ) -> TodoItem:
        """Execute a single todo using the Tool protocol.
        
        Steps:
        1. Get tool for todo type
        2. context = tool.slice(state, todo.params)
        3. patch = tool.generate(constitution, context, instruction)
        4. tool.apply(state, patch)
        """
        # Get tool name
        tool_name = self._tool_names.get(todo.type)
        if not tool_name:
            raise ValueError(f"No tool for todo type: {todo.type}")
        
        # Create tool instance
        tool_kwargs = {
            "use_cache": self.use_cache,
            "verbose": self.verbose,
        }
        if tool_name == "export":
            tool_kwargs["output_dir"] = self.output_dir
        
        tool = get_tool(tool_name, **tool_kwargs)
        
        # Mark started
        todo.mark_started()
        self._log(f"▶ {todo.type.value}: {todo.id}")
        
        try:
            # Get constitution from state
            constitution = state.get_constitution()
            
            # Extract params dict for slice
            params = {}
            if todo.params:
                if isinstance(todo.params, dict):
                    params = todo.params
                else:
                    params = todo.params.model_dump() if hasattr(todo.params, 'model_dump') else dict(todo.params)
            
            # Execute tool protocol: slice -> generate -> apply
            context = tool.slice(state, params)
            patch = tool.generate(constitution, context, user_instruction)
            tool.apply(state, patch)
            
            todo.mark_completed()
            self._log(f"✓ {todo.type.value}: {todo.id}")
            
        except Exception as e:
            todo.mark_failed(str(e))
            logger.error(f"✗ {todo.type.value}: {todo.id} - {e}")
            raise
        
        return todo
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
