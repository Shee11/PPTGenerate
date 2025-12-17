"""Orchestrator for LLM-based content generation workflow.

This module coordinates the complete generation pipeline:
1. Detect presentation intent from user instruction
2. Generate visual styling (theme, style, preset) from intent
3. Extract atoms from source content (guided by intent)
4. Generate slide layouts from atoms (guided by intent)
5. Return Slides collection ready for rendering
"""
from pathlib import Path
from typing import Optional
import logging

from src.common.source import Source
from src.common.slides import Slides
from src.generation.atom.collection import AtomCollection
from src.generation.atom.extractor import extract_atoms
from src.generation.content.generator import generate_layout, refine_layout
from src.generation.intent.detector import detect_intent, PresentationIntent
from src.generation.visual.generator import generate_visual, Visual
from src.utils.generation_config import GenerationConfig
from src.common.patchable_context_pydantic import AddOperation, Patch

logger = logging.getLogger(__name__)


class GenerationOrchestrator:
    """Orchestrates the LLM-based content generation workflow.
    
    Coordinates visual generation, atom extraction, and layout generation with caching support.
    Supports continuous refinement with new user instructions while maintaining state.
    """
    
    def __init__(self, use_cache: bool = True):
        """Initialize orchestrator.
        
        Args:
            use_cache: Enable caching for LLM calls (default: True)
        """
        self.use_cache = use_cache
        
        # State for continuous refinement
        self._source: Optional[Source] = None
        self._created_sources: dict = {}  # Map source_ref -> Source
        self._intent: Optional[PresentationIntent] = None
        self._visual: Optional[Visual] = None  # Store visual styling
        self._atoms: Optional[AtomCollection] = None
        self._slides: Optional[Slides] = None  # Store previous slides for refinement
        self._last_instruction: Optional[str] = None
        self._config: Optional[GenerationConfig] = None
    
    def generate_from_source(
        self,
        source_path: Path,
        user_instruction: Optional[str] = None
    ) -> Slides:
        """Generate slides from source content file.
        
        Args:
            source_path: Path to source file (.txt or .vtt)
            user_instruction: Optional user guidance for generation
            
        Returns:
            Slides collection ready for rendering
            
        Raises:
            FileNotFoundError: If source file doesn't exist
            ValueError: If source file is empty or invalid format
            Exception: If LLM generation fails
        """
        # Validate source file
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Read source content
        source_content = source_path.read_text(encoding='utf-8')
        if not source_content.strip():
            raise ValueError("Source file is empty")
        
        # Determine content type
        content_type = self._get_content_type(source_path)
        
        # Create Source object
        source = Source(
            source_id=f"source_{source_path.stem}",
            name=source_path.name,
            file_path=str(source_path.absolute()),
            content=source_content,
            content_type=content_type,
            metadata={'filename': source_path.name}
        )
        
        # Store source for continuous refinement
        self._source = source
        self._last_instruction = user_instruction if user_instruction else "Create slides from the content"
        
        # Create generation config  
        # Use default configs from prompt modules since GenerationConfig
        # requires model, system_prompt, and user_prompt_template
        # These are defined in the extractor and generator modules
        from src.generation.atom.prompts import get_atom_extraction_config
        from src.generation.content.prompts import get_state_transition_config
        
        # For now, use extraction config as base (both functions create defaults)
        config = get_atom_extraction_config()
        self._config = config
        
        # Use user_instruction if provided, otherwise use default
        instruction = self._last_instruction
        
        # Step 0: Detect presentation intent (new step!)
        intent: Optional[PresentationIntent] = None
        try:
            # Get preview of source content for intent detection
            # Use abstract from source metadata (set by atom extraction)
            # If not available yet (before atom extraction), create basic preview
            source_preview = self._source.metadata.get(
                "abstract",
                f"{source.name}\n\nContent preview: {source_content[:200]}..."
            )
            
            # Build source_refs for multi-source atom extraction tasks
            # For now, single source - future: support multiple sources
            source_refs = [
                {
                    'ref': source.source_id,
                    'summary': source.metadata.get("abstract", f"{source.name}: {source_content[:100]}...")
                }
            ]
            
            intent = detect_intent(
                user_instruction=instruction,
                source_preview=source_preview,
                source_refs=source_refs,
                existing_slides_summary=None,  # No existing slides on first generation
                config=None,  # Use default config
                use_cache=self.use_cache
            )
            print(f"✓ Intent Detected - Audience: {intent.audience[:50]}..., Pattern: {intent.pattern}, Tone: {intent.tone}")
            
            # Log stage changes
            if intent.stage_changes:
                print(f"  Stage changes detected:")
                for stage in intent.stage_changes:
                    status = "✓" if stage.should_execute else "⊘"
                    print(f"    {status} {stage.stage_name}: {stage.guidance[:60]}...")
            
            # Log and process source changes (user-provided embedded content)
            created_sources = {}  # Map source_ref -> Source object
            if intent.source_changes:
                print(f"  Source changes detected: {len(intent.source_changes)} user-provided source(s)")
                for src_change in intent.source_changes:
                    if src_change.should_create:
                        print(f"    + Creating source: {src_change.source_ref} ({src_change.source_type})")
                        print(f"      Content preview: {src_change.content[:80]}...")
                        
                        # Create Source object from user-provided content
                        new_source = Source(
                            source_id=src_change.source_ref,
                            name=f"{src_change.source_ref}.txt",
                            file_path=f"virtual://{src_change.source_ref}",
                            content=src_change.content,
                            content_type=src_change.content_format,
                            metadata={
                                **src_change.metadata,
                                'created_from': 'user_instruction',
                                'source_type': src_change.source_type
                            }
                        )
                        created_sources[src_change.source_ref] = new_source
            
            # Log atom extraction tasks
            if intent.atom_extraction_tasks:
                print(f"  Atom extraction tasks: {len(intent.atom_extraction_tasks)} source(s)")
                for task in intent.atom_extraction_tasks:
                    creation_marker = " [requires source creation]" if task.requires_source_creation else ""
                    print(f"    - {task.source_ref} (priority {task.priority}){creation_marker}: {task.extraction_prompt[:60]}...")
            
            logger.info(f"Detected intent - Audience: {intent.audience}, Pattern: {intent.pattern}, Tone: {intent.tone}")
        except Exception as e:
            print(f"⚠ Intent detection failed: {e}. Proceeding without intent guidance.")
            logger.warning(f"Intent detection failed: {e}. Proceeding without intent guidance.")
            intent = None
        
        # Store intent and created sources for continuous refinement
        self._intent = intent
        self._created_sources = created_sources if intent else {}
        
        # Step 1: Extract atoms (with intent guidance if available)
        # Check if atom extraction should be executed
        should_extract_atoms = True
        atom_guidance = ""
        
        # Skip atom extraction if source already has abstract (atoms already extracted)
        if 'abstract' in source.metadata and self._atoms is not None:
            should_extract_atoms = False
            print(f"✓ Source already has atoms extracted, reusing existing atoms")
        elif intent and intent.stage_changes:
            atom_stage = next((s for s in intent.stage_changes if s.stage_name == "atom_extraction"), None)
            if atom_stage:
                should_extract_atoms = atom_stage.should_execute
                atom_guidance = atom_stage.guidance
                print(f"  Atom extraction stage: {'enabled' if should_extract_atoms else 'skipped (per intent)'}")
        
        # Use atom_extraction_guidance fallback if no stage-specific guidance
        if not atom_guidance and intent:
            atom_guidance = intent.atom_extraction_guidance
        
        if should_extract_atoms:
            from src.generation.atom.collection import AtomCollection
            combined_atoms = AtomCollection(id="combined_atoms")
            
            # Create tasks: use intent tasks if provided, otherwise create default task
            if intent and intent.atom_extraction_tasks:
                tasks = intent.atom_extraction_tasks
                print(f"⚙ Extracting atoms using {len(tasks)} task-specific prompt(s)...")
            else:
                # Single-source case: create default task for main source
                from src.generation.intent.detector import AtomExtractionTask
                tasks = [AtomExtractionTask(
                    source_ref=source.source_id,
                    source_summary=f"Main source: {source.source_id}",
                    extraction_prompt=atom_guidance or "",
                    priority=1,
                    requires_source_creation=False
                )]
                print(f"⚙ Extracting atoms from main source...")
            
            # Sort tasks by priority (1=highest)
            sorted_tasks = sorted(tasks, key=lambda t: t.priority)
            
            for task_idx, task in enumerate(sorted_tasks):
                # Determine which source to use
                if task.requires_source_creation:
                    # Use source from source_changes
                    if task.source_ref in created_sources:
                        task_source = created_sources[task.source_ref]
                        print(f"  Extracting from user-provided source: {task.source_ref}")
                    else:
                        print(f"  ⚠ Warning: Task requires source '{task.source_ref}' but it wasn't created. Skipping.")
                        continue
                else:
                    # Use original source
                    task_source = source
                    print(f"  Extracting from original source: {task.source_ref}")
                
                # Extract atoms with task-specific prompt
                task_atoms = extract_atoms(
                    source=task_source,
                    config=config,
                    use_cache=self.use_cache,
                    intent_guidance=task.extraction_prompt
                )
                
                # Combine atoms with unique IDs (prefix with task index to avoid collisions)
                for atom in task_atoms.list_contexts():
                    # Clone atom with prefixed ID if this is not the first task
                    if task_idx > 0:
                        atom_dict = atom.model_dump()
                        original_id = atom_dict['id']
                        atom_dict['id'] = f"t{task_idx}_{original_id}"
                        # Recreate atom with new ID
                        atom_class = type(atom)
                        atom = atom_class(**atom_dict)
                    
                    combined_atoms.patch(Patch(operations=[AddOperation(add=atom)]))
                
                print(f"    ✓ Extracted {len(task_atoms.list_contexts())} atoms from {task.source_ref}")
            
            atoms = combined_atoms
            print(f"  Total atoms collected: {len(atoms.list_contexts())}")
        else:
            # Skip atom extraction - use empty collection
            print(f"⊘ Skipping atom extraction per intent")
            from src.generation.atom.collection import AtomCollection
            atoms = AtomCollection(id="empty_atoms")
        
        # Store atoms for continuous refinement
        self._atoms = atoms
        
        # Step 2: Generate visual styling if needed
        if intent and intent.visual_change and intent.visual_change.should_generate:
            # User explicitly requested visual changes
            print(f"🎨 Generating visual styling (theme, style, preset)...")
            self._visual = generate_visual(
                intent_guidance=intent.visual_change.visual_guidance,
                audience=intent.audience,
                tone=intent.visual_change.tone,
                purpose=intent.purpose,
                use_cache=self.use_cache
            )
            print(f"✓ Visual styling generated")
        elif self._visual is not None:
            # Reuse cached visual from previous generation
            print(f"♻ Reusing cached visual styling")
        else:
            # No visual change requested and no cached visual - generate default
            print(f"🎨 Generating default visual styling...")
            self._visual = generate_visual(
                intent_guidance="Professional presentation styling",
                audience=intent.audience if intent else "general",
                tone=intent.tone if intent else "professional",
                purpose=intent.purpose if intent else "inform",
                use_cache=self.use_cache
            )
            print(f"✓ Default visual styling generated")
        
        # Step 3: Generate layout (with intent guidance if available)
        if intent:
            # Format content guidance (visual styling handled separately in Visual object)
            content_guidance = f"""**Content Strategy**: {intent.content_generation_guidance}

**Additional Context**:
- Audience: {intent.audience}
- Purpose: {intent.purpose}
- Pattern: {intent.pattern}
- Tone: {intent.tone}
- Visual Density: {intent.visual_density}"""
        else:
            content_guidance = ""
            
        slides = generate_layout(
            atoms=atoms,
            user_instruction=instruction,
            config=config,
            use_cache=self.use_cache,
            intent_guidance=content_guidance
        )
        
        # Store slides for future refinement
        # Note: Visual styling is stored separately in self._visual
        # and accessed via get_visual() method
        self._slides = slides
        
        return slides
    
    def regenerate_with_instruction(
        self,
        new_instruction: str,
        reuse_atoms: bool = True,
        redetect_intent: bool = True
    ) -> Slides:
        """Regenerate slides with a new user instruction.
        
        Maintains state from previous generation (source, atoms) and applies
        new instruction. Useful for iterative refinement in interactive mode.
        
        Args:
            new_instruction: New user instruction for generation
            reuse_atoms: Reuse extracted atoms from previous run (default: True)
            redetect_intent: Re-run intent detection with new instruction (default: True)
            
        Returns:
            Slides collection ready for rendering
            
        Raises:
            RuntimeError: If no previous generation exists (must call generate_from_source first)
        """
        if self._source is None:
            raise RuntimeError("No previous generation found. Call generate_from_source first.")
        
        if not new_instruction or not new_instruction.strip():
            raise ValueError("New instruction cannot be empty")
        
        print(f"\n🔄 Regenerating with new instruction: {new_instruction}")
        self._last_instruction = new_instruction
        
        # Re-detect intent with new instruction if requested
        if redetect_intent:
            try:
                # Use abstract from source metadata (set by atom extraction)
                source_preview = self._source.metadata.get(
                    "abstract",
                    f"{self._source.name}\n\nContent preview: {self._source.content[:200]}..."
                )
                
                source_refs = [
                    {
                        'ref': self._source.source_id,
                        'summary': self._source.metadata.get("abstract", f"{self._source.name}: {self._source.content[:100]}...")
                    }
                ]
                
                # Build existing slides summary for context
                existing_slides_summary = None
                if self._slides and len(self._slides.list_contexts()) > 0:
                    slides_list = []
                    for slide in self._slides.get_active_slides():
                        story_preview = slide.story[:80] + "..." if len(slide.story) > 80 else slide.story
                        slides_list.append(f"  - Slide {slide.rank}: {slide.id} | {story_preview}")
                    existing_slides_summary = f"{len(slides_list)} existing slides:\n" + "\n".join(slides_list)
                
                self._intent = detect_intent(
                    user_instruction=new_instruction,
                    source_preview=source_preview,
                    source_refs=source_refs,
                    existing_slides_summary=existing_slides_summary,
                    config=None,
                    use_cache=self.use_cache
                )
                print(f"✓ Intent Re-detected - Pattern: {self._intent.pattern}, Tone: {self._intent.tone}")
                
                # Process new source_changes if any
                if self._intent.source_changes:
                    print(f"  New source changes: {len(self._intent.source_changes)}")
                    for src_change in self._intent.source_changes:
                        if src_change.should_create and src_change.source_ref not in self._created_sources:
                            new_source = Source(
                                source_id=src_change.source_ref,
                                name=f"{src_change.source_ref}.txt",
                                file_path=f"virtual://{src_change.source_ref}",
                                content=src_change.content,
                                content_type=src_change.content_format,
                                metadata={**src_change.metadata, 'created_from': 'user_instruction'}
                            )
                            self._created_sources[src_change.source_ref] = new_source
                            print(f"    + Created: {src_change.source_ref}")
                
            except Exception as e:
                print(f"⚠ Intent re-detection failed: {e}. Using previous intent.")
                logger.warning(f"Intent re-detection failed: {e}")
        
        # Regenerate visual if explicitly requested
        if self._intent and self._intent.visual_change and self._intent.visual_change.should_generate:
            print(f"🎨 Regenerating visual styling (theme, style, preset)...")
            self._visual = generate_visual(
                intent_guidance=self._intent.visual_change.visual_guidance,
                audience=self._intent.audience,
                tone=self._intent.visual_change.tone,
                purpose=self._intent.purpose,
                use_cache=self.use_cache
            )
            print(f"✓ Visual styling regenerated")
        elif self._visual is not None:
            # Reuse cached visual
            print(f"♻ Reusing cached visual styling")
        else:
            # No cached visual - generate default
            print(f"🎨 Generating default visual styling...")
            self._visual = generate_visual(
                intent_guidance="Professional presentation styling",
                audience=self._intent.audience if self._intent else "general",
                tone=self._intent.tone if self._intent else "professional",
                purpose=self._intent.purpose if self._intent else "inform",
                use_cache=self.use_cache
            )
            print(f"✓ Default visual styling generated")
        
        # Re-extract atoms only if explicitly needed (not for visual-only changes)
        # Check if this is a visual-only refinement
        is_visual_only = (
            self._intent 
            and self._intent.visual_change 
            and self._intent.visual_change.should_generate
            and not any(s.should_execute for s in self._intent.stage_changes if s.stage_name in ["atom_extraction", "storyline", "slide_generation"])
        )
        
        if is_visual_only:
            print(f"✓ Visual-only refinement detected - skipping atom extraction and content regeneration")
            # Return existing slides with updated visual
            return self._slides
        
        # Re-extract atoms if not reusing or if intent requires it
        should_reextract = False
        if not reuse_atoms:
            should_reextract = True
        elif self._intent and self._intent.stage_changes:
            atom_stage = next((s for s in self._intent.stage_changes if s.stage_name == "atom_extraction"), None)
            if atom_stage and atom_stage.should_execute:
                should_reextract = True
        
        if should_reextract:
            print(f"⚙ Re-extracting atoms with new guidance...")
            self._atoms = self._extract_atoms_from_intent()
        else:
            print(f"♻ Reusing {len(self._atoms.list_contexts())} atoms from previous extraction")
        
        # Refine existing slides incrementally with new instruction
        content_guidance = self._build_content_guidance()
        
        if self._slides is not None:
            # Incremental refinement: patch existing slides
            print(f"🔧 Applying incremental refinement to {len(self._slides.list_contexts())} existing slides...")
            slides = refine_layout(
                existing_slides=self._slides,
                atoms=self._atoms,
                refinement_instruction=new_instruction,
                config=self._config,
                use_cache=self.use_cache,
                intent_guidance=content_guidance
            )
        else:
            # Fallback to full generation if no previous slides
            print(f"⚙ No previous slides found, generating from scratch...")
            slides = generate_layout(
                atoms=self._atoms,
                user_instruction=new_instruction,
                config=self._config,
                use_cache=self.use_cache,
                intent_guidance=content_guidance
            )
        
        # Store refined slides for next iteration
        self._slides = slides
        
        return slides
    
    def _extract_atoms_from_intent(self) -> AtomCollection:
        """Extract atoms based on current intent and sources.
        
        Returns:
            AtomCollection with atoms from all sources
        """
        from src.generation.atom.collection import AtomCollection
        from src.generation.intent.detector import AtomExtractionTask
        
        # Check if atom extraction should be executed
        should_extract = True
        atom_guidance = ""
        
        if self._intent and self._intent.stage_changes:
            atom_stage = next((s for s in self._intent.stage_changes if s.stage_name == "atom_extraction"), None)
            if atom_stage:
                should_extract = atom_stage.should_execute
                atom_guidance = atom_stage.guidance
        
        if not atom_guidance and self._intent:
            atom_guidance = self._intent.atom_extraction_guidance
        
        if not should_extract:
            print(f"⊘ Skipping atom extraction per intent")
            return AtomCollection(id="skipped_atoms")
        
        # Create tasks: use intent tasks if provided, otherwise create default task
        combined_atoms = AtomCollection(id="multi_source_atoms")
        
        if self._intent and self._intent.atom_extraction_tasks:
            tasks = self._intent.atom_extraction_tasks
        else:
            # Single-source case: create default task
            tasks = [AtomExtractionTask(
                source_ref=self._source.source_id,
                source_summary=f"Main source: {self._source.source_id}",
                extraction_prompt=atom_guidance or "",
                priority=1,
                requires_source_creation=False
            )]
        
        sorted_tasks = sorted(tasks, key=lambda t: t.priority)
        
        for task_idx, task in enumerate(sorted_tasks):
            if task.requires_source_creation:
                if task.source_ref in self._created_sources:
                    task_source = self._created_sources[task.source_ref]
                else:
                    print(f"  ⚠ Source '{task.source_ref}' not found, skipping")
                    continue
            else:
                task_source = self._source
            
            task_atoms = extract_atoms(
                source=task_source,
                config=self._config,
                use_cache=self.use_cache,
                intent_guidance=task.extraction_prompt
            )
            
            # Combine atoms with unique IDs (prefix with task index to avoid collisions)
            for atom in task_atoms.list_contexts():
                # Clone atom with prefixed ID if this is not the first task
                if task_idx > 0:
                    atom_dict = atom.model_dump()
                    original_id = atom_dict['id']
                    atom_dict['id'] = f"t{task_idx}_{original_id}"
                    # Recreate atom with new ID
                    atom_class = type(atom)
                    atom = atom_class(**atom_dict)
                
                combined_atoms.patch(Patch(operations=[AddOperation(add=atom)]))
            
            print(f"  ✓ Extracted {len(task_atoms.list_contexts())} atoms from {task.source_ref}")
        
        return combined_atoms
    
    def _build_content_guidance(self) -> str:
        """Build content guidance string from current intent.
        
        Returns:
            Formatted guidance string for content generation
        """
        if not self._intent:
            return ""
        
        return f"""**Content Strategy**: {self._intent.content_generation_guidance}

**Theme Recommendation**: {self._intent.theme_guidance}
**Preset Recommendation**: {self._intent.preset_guidance}

**Additional Context**:
- Audience: {self._intent.audience}
- Purpose: {self._intent.purpose}
- Pattern: {self._intent.pattern}
- Tone: {self._intent.tone}
- Visual Density: {self._intent.visual_density}"""
    
    def get_visual(self) -> Optional[Visual]:
        """Get the current visual styling.
        
        Returns:
            Visual object if generated, None otherwise
        """
        return self._visual
    
    def get_current_state(self) -> dict:
        """Get current orchestrator state for inspection.
        
        Returns:
            Dictionary with current state information
        """
        return {
            'has_source': self._source is not None,
            'source_id': self._source.source_id if self._source else None,
            'created_sources': list(self._created_sources.keys()),
            'has_intent': self._intent is not None,
            'intent_pattern': self._intent.pattern if self._intent else None,
            'has_visual': self._visual is not None,
            'atoms_count': len(self._atoms.list_contexts()) if self._atoms else 0,
            'slides_count': len(self._slides.list_contexts()) if self._slides else 0,
            'last_instruction': self._last_instruction
        }
    
    def reset_state(self):
        """Reset orchestrator state for new generation."""
        self._source = None
        self._created_sources = {}
        self._intent = None
        self._visual = None
        self._atoms = None
        self._slides = None
        self._last_instruction = None
        self._config = None
    
    def _get_content_type(self, source_path: Path) -> str:
        """Determine content type from file extension.
        
        Args:
            source_path: Path to source file
            
        Returns:
            Content type string
        """
        suffix = source_path.suffix.lower()
        
        if suffix == '.txt':
            return 'text/plain'
        elif suffix == '.vtt':
            return 'text/vtt'
        else:
            # Default to text/plain for unknown types
            return 'text/plain'


def generate_from_file(
    source_path: Path,
    user_instruction: Optional[str] = None,
    use_cache: bool = True
) -> tuple[Slides, Optional[Visual]]:
    """Convenience function to generate slides from source file.
    
    Args:
        source_path: Path to source file (.txt or .vtt)
        user_instruction: Optional user guidance for generation
        use_cache: Enable caching for LLM calls (default: True)
        
    Returns:
        Tuple of (Slides collection ready for rendering, Visual styling if generated)
        
    Raises:
        FileNotFoundError: If source file doesn't exist
        ValueError: If source file is empty or invalid format
        Exception: If LLM generation fails
    """
    orchestrator = GenerationOrchestrator(use_cache=use_cache)
    slides = orchestrator.generate_from_source(source_path, user_instruction)
    visual = orchestrator.get_visual()
    return slides, visual
