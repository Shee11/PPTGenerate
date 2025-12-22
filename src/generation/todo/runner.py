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
        
        self.executor = TodoExecutor(
            verbose=verbose,
            use_cache=use_cache,
            output_dir=self.output_dir,
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
        
        # Plan todos from instruction
        if self.verbose:
            print(f"📋 Planning todos from instruction...")
        
        todos = plan(state, user_instruction)
        state.todos = todos
        
        if self.verbose:
            print(f"📋 Planned {len(todos.todos)} todos:")
            for todo in todos.todos:
                deps = f" (depends: {todo.depends_on})" if todo.depends_on else ""
                print(f"   • {todo.type.value}: {todo.id}{deps}")
        
        # Execute all todos - pass user_instruction to executor
        if self.verbose:
            print(f"\n🔄 Executing todos...")
        
        count = self.executor.execute_all(state, user_instruction)
        
        # Save state to output folder
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state.save(state_path)
        if self.verbose:
            print(f"💾 State saved to {state_path}")
        
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
        
        # Execute - pass user_instruction
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
