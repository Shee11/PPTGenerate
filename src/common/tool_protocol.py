"""Unified Tool Protocol.

All tools follow the same interface:
1. slice(state) -> context    # Extract relevant state for LLM
2. generate(constitution, context, user_instruction) -> patch  # LLM creates patch
3. apply(state, patch)        # Apply patch to state

Tools are SELF-DESCRIBING:
- description: What the tool does
- query_description: What user instruction triggers this tool
- args_description: What parameters the tool needs

Planner just concats all tool descriptions to understand capabilities.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Generic, TypeVar, Optional, List, ClassVar
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.generation.state import PipelineState
    from src.generation.todo.models import ConstitutionPatch


# Generic type variables for context and patch
TContext = TypeVar('TContext', bound=BaseModel)
TPatch = TypeVar('TPatch', bound=BaseModel)


class ToolContext(BaseModel):
    """Base class for tool-specific context extracted from state."""
    pass


class ToolPatch(BaseModel):
    """Base class for tool-specific patches to apply to state."""
    pass


class ToolDescription(BaseModel):
    """Self-description of a tool for planner."""
    name: str = Field(..., description="Tool identifier")
    description: str = Field(..., description="What this tool does")
    query_description: str = Field(..., description="What user instructions trigger this tool")
    args_description: List[str] = Field(default_factory=list, description="Parameters that affect this tool")
    requires: List[str] = Field(default_factory=list, description="Tools that must run before this")
    produces: List[str] = Field(default_factory=list, description="What this tool adds to state")
    examples: List[str] = Field(default_factory=list, description="Example todo JSON for this tool")


class Tool(ABC, Generic[TContext, TPatch]):
    """Base class for all pipeline tools.
    
    Each tool is SELF-DESCRIBING:
    - name: Tool identifier
    - description: What it does
    - query_description: What triggers it
    - args_description: What parameters it uses
    
    Planner calls get_all_descriptions() to understand all tools.
    
    Protocol:
    - slice: state -> context (what LLM sees)
    - generate: (constitution, context, instruction) -> patch
    - apply: (state, patch) -> None (mutates state)
    """
    
    # === TOOL DESCRIPTION (override in subclasses) ===
    name: ClassVar[str] = "base_tool"
    description: ClassVar[str] = "Base tool - override this"
    query_description: ClassVar[str] = "N/A - override this"
    args_description: ClassVar[List[str]] = []
    requires: ClassVar[List[str]] = []
    produces: ClassVar[List[str]] = []
    examples: ClassVar[List[str]] = []  # Example todo JSONs for planner
    
    # System prompt for LLM tools
    system_prompt: ClassVar[str] = ""
    
    def __init__(self, use_cache: bool = True, verbose: bool = False):
        self.use_cache = use_cache
        self.verbose = verbose
    
    @classmethod
    def get_description(cls) -> ToolDescription:
        """Get structured self-description for planner."""
        return ToolDescription(
            name=cls.name,
            description=cls.description,
            query_description=cls.query_description,
            args_description=list(cls.args_description),
            requires=list(cls.requires),
            produces=list(cls.produces),
            examples=list(cls.examples),
        )
    
    @classmethod
    def get_description_text(cls) -> str:
        """Get description as formatted text for planner prompt."""
        lines = [
            f"## {cls.name}",
            f"Description: {cls.description}",
            f"Triggers: {cls.query_description}",
        ]
        if cls.args_description:
            lines.append(f"Args: {', '.join(cls.args_description)}")
        if cls.requires:
            lines.append(f"Requires: {', '.join(cls.requires)}")
        if cls.produces:
            lines.append(f"Produces: {', '.join(cls.produces)}")
        if cls.examples:
            lines.append("Examples:")
            for example in cls.examples:
                lines.append(f"  {example}")
        return '\n'.join(lines)
    
    @abstractmethod
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> TContext:
        """Extract relevant context from state for LLM.
        
        Args:
            state: Pipeline state
            params: Optional tool-specific parameters from todo
        
        This controls what the LLM sees. Keep it minimal.
        Do NOT pass full state to LLM.
        """
        pass
    
    @abstractmethod
    def generate(
        self,
        constitution: "ConstitutionPatch",
        context: TContext,
        user_instruction: str,
    ) -> TPatch:
        """Generate a patch.
        
        Args:
            constitution: Global rules and constraints
            context: Tool-specific context (from slice)
            user_instruction: What the user wants
        
        Returns:
            Patch to apply to state
        """
        pass
    
    @abstractmethod
    def apply(self, state: "PipelineState", patch: TPatch) -> None:
        """Apply patch to state. This is the only place state is mutated."""
        pass
    
    def execute(
        self,
        state: "PipelineState",
        constitution: "ConstitutionPatch",
        user_instruction: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> TPatch:
        """Full execution: slice -> generate -> apply."""
        context = self.slice(state, params)
        patch = self.generate(constitution, context, user_instruction)
        self.apply(state, patch)
        return patch
    
    def _log(self, msg: str):
        if self.verbose:
            print(f"[{self.name}] {msg}")


class DirectTool(Tool[TContext, TPatch]):
    """Tool that doesn't use LLM (direct transformation)."""
    
    def generate(
        self,
        constitution: "ConstitutionPatch",
        context: TContext,
        user_instruction: str,
    ) -> TPatch:
        """Direct tools use transform() instead of LLM."""
        return self.transform(context, user_instruction)
    
    @abstractmethod
    def transform(self, context: TContext, user_instruction: str) -> TPatch:
        """Transform context directly without LLM."""
        pass


class LLMTool(Tool[TContext, TPatch]):
    """Tool that uses LLM for generation."""
    
    def generate(
        self,
        constitution: "ConstitutionPatch",
        context: TContext,
        user_instruction: str,
    ) -> TPatch:
        """Generate patch using LLM."""
        prompt = self.build_prompt(constitution, context, user_instruction)
        response = self.call_llm(prompt)
        return self.parse_response(response)
    
    def build_prompt(
        self,
        constitution: "ConstitutionPatch",
        context: TContext,
        user_instruction: str,
    ) -> str:
        """Build prompt for LLM."""
        parts = []
        
        if self.system_prompt:
            parts.append(f"# System\n{self.system_prompt}")
        
        if constitution:
            rules = "\n".join(f"- {r}" for r in constitution.style_rules)
            parts.append(f"# Rules\n{rules}")
            if constitution.tone:
                parts.append(f"Tone: {constitution.tone}")
        
        context_str = self.format_context(context)
        if context_str:
            parts.append(f"# Context\n{context_str}")
        
        parts.append(f"# Instruction\n{user_instruction}")
        
        return "\n\n".join(parts)
    
    @abstractmethod
    def format_context(self, context: TContext) -> str:
        """Format context for prompt."""
        pass
    
    @abstractmethod
    def call_llm(self, prompt: str) -> str:
        """Call LLM with prompt."""
        pass
    
    @abstractmethod
    def parse_response(self, response: str) -> TPatch:
        """Parse LLM response into patch."""
        pass


# =============================================================================
# TOOL REGISTRY
# =============================================================================

_TOOL_REGISTRY: Dict[str, type] = {}


def register_tool(tool_class: type) -> type:
    """Decorator to register a tool class."""
    _TOOL_REGISTRY[tool_class.name] = tool_class
    return tool_class


def get_tool(name: str, **kwargs) -> Tool:
    """Get tool instance by name."""
    if name not in _TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {name}. Available: {list(_TOOL_REGISTRY.keys())}")
    return _TOOL_REGISTRY[name](**kwargs)


def get_all_tools() -> Dict[str, type]:
    """Get all registered tool classes."""
    return dict(_TOOL_REGISTRY)


def get_all_descriptions() -> str:
    """Get all tool descriptions as text for planner.
    
    Planner can just call this to understand all available tools.
    """
    descriptions = []
    for tool_class in _TOOL_REGISTRY.values():
        descriptions.append(tool_class.get_description_text())
    return "\n\n".join(descriptions)


def get_all_descriptions_structured() -> List[ToolDescription]:
    """Get all tool descriptions as structured objects."""
    return [tool_class.get_description() for tool_class in _TOOL_REGISTRY.values()]
