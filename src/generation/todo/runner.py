"""Pipeline Runner v2 - Todo-based architecture.

Clean architecture:
    todos = planner(state, user_instruction)
    for todo in todos:
        executor.execute_todo(todo, state, user_instruction)

All tools follow unified protocol:
    context = tool.slice(state)
    patch = tool.generate(constitution, context, user_instruction)
    tool.apply(state, patch)
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.generation.state import PipelineState
from src.generation.todo.planner import plan
from src.generation.todo.executor import TodoExecutor


class PipelineRunner:
    """Runs the todo-based generation pipeline.
    
    Usage:
        runner = PipelineRunner(verbose=True)
        
        # From scratch
        result = runner.run(
            source_path=Path("input.vtt"),
            user_instruction="create slides, 10 pages, professional"
        )
        
        # Incremental update
        result = runner.run_incremental(
            state_path=Path(".state.json"),
            user_instruction="add more visuals"
        )
    """
    
    def __init__(
        self,
        verbose: bool = False,
        use_cache: bool = True,
        output_dir: Optional[Path] = None,
    ):
        self.verbose = verbose
        self.use_cache = use_cache
        self.output_dir = output_dir or Path("output")
        self.state_path = self.output_dir / "state.json"
        
        self.executor = TodoExecutor(
            verbose=verbose,
            use_cache=use_cache,
            output_dir=self.output_dir,
            state_path=self.state_path,  # Pass state_path for persistence
        )
    
    def run(
        self,
        source_path: Path,
        user_instruction: str,
        state: Optional["PipelineState"] = None,
    ) -> "PipelineState":
        """Run full pipeline from source.
        
        Args:
            source_path: Path to source file (VTT, TXT, MD, etc.)
            user_instruction: User's natural language instruction
            state: Optional existing state (for incremental updates)
        
        Returns:
            Final pipeline state
        """
        # Late import to avoid circular dependency
        from src.generation.state import PipelineState
        
        # Try to load existing state from output folder
        state_path = self.output_dir / "state.json"
        if state is None and state_path.exists():
            if self.verbose:
                print(f"📂 Loading existing state from {state_path}")
            state = PipelineState.load(state_path)
        elif state is None:
            state = PipelineState()
            state.load_default_themes()
        
        # Set source
        state.set_source(source_path)
        
        # Check if state already has pending todos - if so, skip planning
        # This makes state.json the source of truth
        has_pending_todos = (
            state.todos is not None 
            and hasattr(state.todos, 'todos') 
            and len(state.todos.todos) > 0
            and any(t.status in ('pending', 'in_progress') for t in state.todos.todos)
        )
        
        if has_pending_todos:
            if self.verbose:
                print(f"📋 Using existing todos from state.json (skipping planning)")
                pending_count = sum(1 for t in state.todos.todos if t.status in ('pending', 'in_progress'))
                completed_count = sum(1 for t in state.todos.todos if t.status == 'completed')
                print(f"   • {completed_count} completed, {pending_count} pending")
            todos = state.todos
        else:
            # Plan todos from instruction
            if self.verbose:
                print(f"📋 Planning todos from instruction...")
            
            todos = plan(state, user_instruction)
            state.todos = todos
            
            # Persist state immediately after planning
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            state.save(self.state_path)
            if self.verbose:
                print(f"💾 Todos planned, state persisted")
        
        if self.verbose:
            print(f"📋 {len(todos.todos)} todos:")
            for todo in todos.todos:
                deps = f" (depends: {todo.depends_on})" if todo.depends_on else ""
                status = f"[{todo.status}]" if todo.status != 'pending' else ""
                print(f"   • {todo.type.value}: {todo.id}{deps} {status}")
        
        # Execute all todos - pass user_instruction to executor
        # (executor persists state on each todo status change)
        if self.verbose:
            print(f"\n🔄 Executing todos...")
        
        count = self.executor.execute_all(state, user_instruction)
        
        if self.verbose:
            print(f"\n✅ Completed {count} todos")
            print(state.summary())
        
        if self.verbose:
            print(f"\n✅ Completed {count} todos")
            print(state.summary())
        
        return state
    
    def run_incremental(
        self,
        state_path: Path,
        user_instruction: str,
    ) -> "PipelineState":
        """Run incremental update on existing state.
        
        Args:
            state_path: Path to saved state JSON
            user_instruction: User's refinement instruction
        
        Returns:
            Updated pipeline state
        """
        # Late import to avoid circular dependency
        from src.generation.state import PipelineState
        
        # Load existing state
        state = PipelineState.load(state_path)
        
        # Clear previous todos
        state.clear_todos()
        
        # Plan new todos based on current state + instruction
        todos = plan(state, user_instruction)
        state.todos = todos
        
        # Persist state immediately after planning
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state.save(state_path)
        
        # Execute - pass user_instruction
        # (executor persists state on each todo status change)
        count = self.executor.execute_all(state, user_instruction)
        
        if self.verbose:
            print(f"✅ Incremental: {count} todos executed")
        
        return state
    
    def save_state(self, state: "PipelineState", path: Path):
        """Save state to file."""
        state.save(path)
        if self.verbose:
            print(f"💾 State saved to {path}")
    
    def load_state(self, path: Path) -> "PipelineState":
        """Load state from file."""
        # Late import to avoid circular dependency
        from src.generation.state import PipelineState
        
        state = PipelineState.load(path)
        if self.verbose:
            print(f"📂 State loaded from {path}")
        return state


# Convenience function
def generate_slides(
    source_path: Path,
    user_instruction: str,
    output_dir: Optional[Path] = None,
    verbose: bool = False,
) -> Path:
    """Generate slides from source file.
    
    Args:
        source_path: Input file (VTT, TXT, MD)
        user_instruction: e.g. "create slides, 10 pages, professional, corp_modern_v1"
        output_dir: Where to write slides
        verbose: Print progress
    
    Returns:
        Path to generated slides
    """
    runner = PipelineRunner(
        verbose=verbose,
        output_dir=output_dir or Path("output"),
    )
    
    state = runner.run(source_path, user_instruction)
    
    # Return path to output
    return runner.output_dir / "slides.md"
