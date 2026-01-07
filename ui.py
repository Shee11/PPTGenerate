"""Gradio UI to run the UCE pipeline in 7 explicit steps.

Steps:
  1) planner
  2) constitution
  3) atoms
  4) theme
  5) story
  6) content
  7) export

Requirements covered:
  1) Each step has a button to execute.
  2) If step involves LLM: show predefined prompts after Initialize and show LLM response after execution.
  3) If step does not involve LLM: show result only.
  4) Export: show produced files + a button to preview the MDX PPT (React renderer link).

Run:
  ./.venv/bin/python ui.py
"""

from __future__ import annotations

import io
import json
import os
import shutil
import html as _html
import socket
import subprocess
import threading
import time
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import gradio as gr

from src.generation.state import PipelineState
from src.generation.todo.executor import TodoExecutor
from src.generation.todo.models import TodoType
from src.generation.todo.planner import plan


UI_CSS = """
/* Force prompt/code panes to stay compact and scroll */
.code-fixed .ace_editor { height: 220px !important; }
.code-fixed { max-height: 240px; overflow: auto; }

/* Dark background for selected file path field */
.path-dark input,
.path-dark textarea {
    background: #111827 !important;
    color: #f9fafb !important;
}

/* (Source file section uses standard Gradio layout; only input is darkened) */

/* Tiny timer inline next to Run button */
#planner_timer,
#atoms_timer,
#theme_timer,
#story_timer,
#content_timer {
    font-size: 12px;
    opacity: 0.65;
    padding-top: 6px;
    white-space: nowrap;
}

#planner_timer > div,
#atoms_timer > div,
#theme_timer > div,
#story_timer > div,
#content_timer > div {
    margin: 0 !important;
    padding: 0 !important;
}
"""


Session = Dict[str, object]


@dataclass
class OutputFiles:
    state_json: Optional[Path]
    slides_mdx: Optional[Path]
    pptx_files: List[Path]
    html_files: List[Path]


def _status_one_liner(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    lines = t.splitlines()
    if len(lines) == 1:
        return lines[0]
    return f"{lines[0]} … (+{len(lines) - 1} lines)"


def _theme_change_summary(before: PipelineState, after: PipelineState) -> str:
    before_active = getattr(before, "active_theme_id", None)
    after_active = getattr(after, "active_theme_id", None)
    before_count = len(getattr(before, "themes", None) or {})
    after_count = len(getattr(after, "themes", None) or {})

    lines: List[str] = []
    if before_active != after_active:
        lines.append(f"active_theme_id: {before_active or '(none)'} → {after_active or '(none)'}")
    else:
        lines.append(f"active_theme_id: {after_active or '(none)'}")

    if before_count != after_count:
        lines.append(f"themes: {before_count} → {after_count}")

    if after_active and (getattr(after, "themes", None) or {}).get(after_active):
        t = after.themes.get(after_active) or {}
        name = (t.get("name") or "").strip()
        desc = (t.get("description") or "").strip()
        if name:
            lines.append(f"name: {name}")
        if desc:
            lines.append(f"description: {desc}")

    return "\n".join([l for l in lines if l.strip()]).strip() or "(no theme changes detected)"


def _theme_summary_from_state(state: PipelineState) -> str:
    active = getattr(state, "active_theme_id", None)
    themes = getattr(state, "themes", None) or {}
    lines: List[str] = [f"active_theme_id: {active or '(none)'}", f"themes: {len(themes)}"]
    if active and themes.get(active):
        t = themes.get(active) or {}
        name = (t.get("name") or "").strip()
        desc = (t.get("description") or "").strip()
        if name:
            lines.append(f"name: {name}")
        if desc:
            lines.append(f"description: {desc}")
    return "\n".join(lines).strip()


def _read_all_trace(trace_path: Path) -> List[dict]:
    if not trace_path.exists():
        return []
    records: List[dict] = []
    try:
        for line in trace_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    except Exception:
        return []
    return records


def export_progress(
    session: Session,
    planner_sys: str,
    planner_user: str,
    atoms_sys: str,
    atoms_user: str,
    theme_sys: str,
    theme_user: str,
    story_sys: str,
    story_user: str,
    content_sys: str,
    content_user: str,
) -> Tuple[Session, object, str]:
    """Export current progress to a JSON file and return it for download."""
    session = _ensure_session(session)
    if not session.get("output_dir"):
        return session, gr.update(value=None, visible=False), ""

    output_dir, state_path, trace_path = _session_paths(session)
    if not state_path.exists():
        return session, gr.update(value=None, visible=False), ""

    try:
        state_json = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return session, gr.update(value=None, visible=False), ""

    payload = {
        "version": 1,
        "exported_at": datetime.now().isoformat(),
        "session": {
            "output_dir": str(output_dir),
            "instruction": str(session.get("instruction", "")),
            "use_cache": bool(session.get("use_cache", True)),
            "project": str(state_json.get("project") or ""),
            "mdx_theme": str(state_json.get("mdx_theme") or ""),
        },
        "state": state_json,
        "prompts": {
            "planner": {"system": planner_sys or "", "user": planner_user or ""},
            "atoms": {"system": atoms_sys or "", "user": atoms_user or ""},
            "theme": {"system": theme_sys or "", "user": theme_user or ""},
            "story": {"system": story_sys or "", "user": story_user or ""},
            "content": {"system": content_sys or "", "user": content_user or ""},
        },
        "llm_trace": _read_all_trace(trace_path),
    }

    out_path = output_dir / f"UCE Pipeline_progress_{_now_id()}.json"
    try:
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return session, gr.update(value=None, visible=False), ""

    # Note: browsers generally require a user click to download.
    return session, gr.update(value=str(out_path), visible=True), _now_id()


def import_progress(progress_file):
    """Import a progress JSON file and restore session + UI fields."""
    def _empty(msg: str):
        empty_session: Session = {}
        return (
            empty_session,
            "",  # source_name
            "",  # instruction_text
            "",  # output_name
            "react-mdx",  # project
            "business",  # mdx_theme
            True,  # use_cache
            "",  # planner sys
            "",  # planner user
            "",  # atoms sys
            "",  # atoms user
            "",  # theme sys
            "",  # theme user
            "",  # story sys
            "",  # story user
            "",  # content sys
            "",  # content user
            "",  # constitution_result
            "",  # planner_sent
            "",  # planner_resp
            "",  # atoms_sent
            "",  # atoms_resp
            gr.update(value="", visible=False),  # theme_result
            gr.update(value="", visible=True),  # theme_sent
            gr.update(value="", visible=True),  # theme_resp
            "",  # story_sent
            "",  # story_resp
            "",  # content_sent
            "",  # content_resp
        )
    if progress_file is None:
        return _empty("")

    path = Path(getattr(progress_file, "name", "") or str(progress_file))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return _empty("")

    state_json = payload.get("state") or {}
    sess = payload.get("session") or {}
    out_dir = Path(str(sess.get("output_dir") or state_json.get("output_dir") or "output/imported"))
    out_dir.mkdir(parents=True, exist_ok=True)

    state_path = out_dir / "state.json"
    try:
        state_path.write_text(json.dumps(state_json, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return _empty("")

    trace_path = out_dir / "llm_trace.jsonl"
    llm_trace = payload.get("llm_trace") or []
    if isinstance(llm_trace, list) and llm_trace:
        try:
            trace_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in llm_trace) + "\n", encoding="utf-8")
        except Exception:
            pass

    instruction = str(sess.get("instruction") or "")
    use_cache = bool(sess.get("use_cache", True))
    project = str(sess.get("project") or state_json.get("project") or "react-mdx")
    mdx_theme = str(sess.get("mdx_theme") or state_json.get("mdx_theme") or "business")

    # Restore prompts
    prompts = payload.get("prompts") or {}
    def _p(step: str, k: str) -> str:
        v = (prompts.get(step) or {}).get(k)
        return str(v or "")

    planner_sys = _p("planner", "system")
    planner_user = _p("planner", "user")
    atoms_sys = _p("atoms", "system")
    atoms_user = _p("atoms", "user")
    theme_sys = _p("theme", "system")
    theme_user = _p("theme", "user")
    story_sys = _p("story", "system")
    story_user = _p("story", "user")
    content_sys = _p("content", "system")
    content_user = _p("content", "user")

    # Restore step outputs from state/trace
    state = PipelineState.load(state_path)
    source_path = ""
    try:
        if state.source and getattr(state.source, "path", None):
            source_path = str(state.source.path)
    except Exception:
        source_path = ""

    all_records = _read_all_trace(trace_path)
    def _sr(step: str) -> List[dict]:
        return _filter_records_for_step(all_records, step)

    planner_sent = _format_llm_sent(_sr("planner"))
    planner_resp = _format_llm_response(_sr("planner"))
    atoms_sent = _format_llm_sent(_sr("atoms"))
    atoms_resp = _format_llm_response(_sr("atoms"))
    theme_sent = _format_llm_sent(_sr("theme"))
    theme_resp = _format_llm_response(_sr("theme"))
    story_sent = _format_llm_sent(_sr("story"))
    story_resp = _format_llm_response(_sr("story"))
    content_sent = _format_llm_sent(_sr("content"))
    content_resp = _format_llm_response(_sr("content"))

    theme_used_llm = bool((theme_sent or "").strip() or (theme_resp or "").strip())
    theme_result_update = gr.update(value="", visible=False)
    theme_sent_update = gr.update(value=theme_sent, visible=True)
    theme_resp_update = gr.update(value=theme_resp, visible=True)
    if not theme_used_llm:
        theme_result_update = gr.update(value=_theme_summary_from_state(state), visible=True)
        theme_sent_update = gr.update(value="", visible=False)
        theme_resp_update = gr.update(value="", visible=False)

    session: Session = {
        "output_dir": str(out_dir),
        "instruction": instruction,
        "use_cache": bool(use_cache),
        "trace_pos": 0,
    }

    return (
        session,
        source_path,
        instruction,
        str(out_dir.name),
        project,
        mdx_theme,
        bool(use_cache),
        planner_sys,
        planner_user,
        atoms_sys,
        atoms_user,
        theme_sys,
        theme_user,
        story_sys,
        story_user,
        content_sys,
        content_user,
        _constitution_text(state),
        planner_sent,
        planner_resp,
        atoms_sent,
        atoms_resp,
        theme_result_update,
        theme_sent_update,
        theme_resp_update,
        story_sent,
        story_resp,
        content_sent,
        content_resp,
    )


def _now_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _ensure_session(session: Optional[Session]) -> Session:
    return session or {}


def _session_paths(session: Session) -> Tuple[Path, Path, Path]:
    output_dir = Path(str(session["output_dir"]))
    state_path = output_dir / "state.json"
    trace_path = output_dir / "llm_trace.jsonl"
    return output_dir, state_path, trace_path


def _read_instruction_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _collect_outputs(output_dir: Path) -> OutputFiles:
    state_json = output_dir / "state.json"
    slides_mdx = output_dir / "slides.mdx"
    pptx_files = sorted(output_dir.glob("**/*.pptx"))
    html_files = sorted(output_dir.glob("**/*.html"))
    return OutputFiles(
        state_json=state_json if state_json.exists() else None,
        slides_mdx=slides_mdx if slides_mdx.exists() else None,
        pptx_files=pptx_files,
        html_files=html_files,
    )


def _as_downloadable_files(files: OutputFiles) -> List[str]:
    out: List[str] = []
    if files.state_json:
        out.append(str(files.state_json))
    if files.slides_mdx:
        out.append(str(files.slides_mdx))
    for p in files.pptx_files:
        out.append(str(p))
    for p in files.html_files:
        out.append(str(p))
    return out


def _read_mdx_preview(output_dir: Path, max_chars: int = 12000) -> str:
    mdx = output_dir / "slides.mdx"
    if not mdx.exists():
        return "(no slides.mdx)"
    text = mdx.read_text(encoding="utf-8")
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n... (truncated)"
    return text


def _read_new_trace(trace_path: Path, from_pos: int) -> Tuple[int, List[dict]]:
    if not trace_path.exists():
        return from_pos, []
    try:
        with trace_path.open("r", encoding="utf-8") as f:
            f.seek(from_pos)
            chunk = f.read()
            new_pos = f.tell()
        records: List[dict] = []
        for line in chunk.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
        return new_pos, records
    except Exception:
        return from_pos, []


def _filter_records_for_step(records: List[dict], step: str) -> List[dict]:
    tagged = [r for r in records if r.get("step") == step]
    return tagged if tagged else records


def _format_llm_sent(records: List[dict]) -> str:
    if not records:
        return ""
    parts: List[str] = []
    for r in records:
        sys_p = r.get("system_prompt")
        user_p = r.get("user_prompt")
        if sys_p or user_p:
            parts.append(
                "\n".join(
                    [
                        "# System",
                        sys_p or "",
                        "\n# User",
                        user_p or "",
                    ]
                ).strip()
            )
    return "\n\n---\n\n".join([p for p in parts if p.strip()])


def _format_llm_response(records: List[dict]) -> str:
    if not records:
        return ""
    parts: List[str] = []
    for r in records:
        resp = r.get("response")
        if resp:
            parts.append(str(resp).strip())
    return "\n\n---\n\n".join([p for p in parts if p.strip()])


def _find_todo(state: PipelineState, todo_type: TodoType):
    if not state.todos:
        return None
    # TodoQueue stores todos in .todos
    todos = getattr(state.todos, "todos", None)
    if todos is None and isinstance(state.todos, list):
        todos = state.todos
    if not todos:
        return None

    for t in todos:
        if getattr(t, "type", None) == todo_type:
            return t
    return None


def _constitution_text(state: PipelineState) -> str:
    c = state.get_constitution()
    if not c:
        return "(no constitution)"
    lines: List[str] = []
    tone = getattr(c, "tone", None)
    if tone:
        lines.append(f"tone: {tone}")
    tgt = getattr(c, "slide_count_target", None)
    if tgt:
        lines.append(f"slide_count_target: {tgt}")
    rules = getattr(c, "style_rules", None) or []
    if rules:
        lines.append("style_rules:")
        lines.extend([f"- {r}" for r in rules])
    excl = getattr(c, "content_exclusions", None) or []
    if excl:
        lines.append("content_exclusions:")
        lines.extend([f"- {r}" for r in excl])
    req = getattr(c, "content_requirements", None) or []
    if req:
        lines.append("content_requirements:")
        lines.extend([f"- {r}" for r in req])
    return "\n".join(lines).strip() or "(empty constitution)"


def _with_llm_env(session: Session, step: str, override_system: Optional[str], override_user: Optional[str]):
    output_dir, _, trace_path = _session_paths(session)
    _ = output_dir

    old_trace = os.environ.get("LLM_TRACE_FILE")
    old_step = os.environ.get("LLM_TRACE_STEP")
    old_os = os.environ.get("LLM_OVERRIDE_SYSTEM_PROMPT")
    old_ou = os.environ.get("LLM_OVERRIDE_USER_PROMPT")

    os.environ["LLM_TRACE_FILE"] = str(trace_path)
    os.environ["LLM_TRACE_STEP"] = step

    override_system = (override_system or "").strip()
    override_user = (override_user or "").strip()

    if override_system:
        os.environ["LLM_OVERRIDE_SYSTEM_PROMPT"] = override_system
    else:
        os.environ.pop("LLM_OVERRIDE_SYSTEM_PROMPT", None)

    if override_user:
        os.environ["LLM_OVERRIDE_USER_PROMPT"] = override_user
    else:
        os.environ.pop("LLM_OVERRIDE_USER_PROMPT", None)

    return old_trace, old_step, old_os, old_ou


def _restore_llm_env(old_vals) -> None:
    old_trace, old_step, old_os, old_ou = old_vals

    if old_trace is None:
        os.environ.pop("LLM_TRACE_FILE", None)
    else:
        os.environ["LLM_TRACE_FILE"] = old_trace

    if old_step is None:
        os.environ.pop("LLM_TRACE_STEP", None)
    else:
        os.environ["LLM_TRACE_STEP"] = old_step

    if old_os is None:
        os.environ.pop("LLM_OVERRIDE_SYSTEM_PROMPT", None)
    else:
        os.environ["LLM_OVERRIDE_SYSTEM_PROMPT"] = old_os

    if old_ou is None:
        os.environ.pop("LLM_OVERRIDE_USER_PROMPT", None)
    else:
        os.environ["LLM_OVERRIDE_USER_PROMPT"] = old_ou


def build_default_prompts(session: Session, step: str) -> Tuple[str, str, str]:
    """Return (note, system_prompt, user_prompt) for a step."""
    output_dir, state_path, _ = _session_paths(session)
    _ = output_dir
    if not state_path.exists():
        return "[note] state.json missing (Initialize first)", "", ""

    state = PipelineState.load(state_path)
    instruction = str(session.get("instruction", ""))

    if step == "planner":
        from src.generation.todo.planner import build_planner_prompt

        sys_p, user_p = build_planner_prompt(state, instruction)
        return "", sys_p, user_p

    if step == "atoms":
        from src.generation.atom.prompts import get_atom_extraction_config, render_atom_extraction_prompt
        from src.common.source import Source

        if not state.source:
            return "[note] No source in state.", "", ""
        source_path = Path(state.source.path)
        content = source_path.read_text(encoding="utf-8")

        guidance = ""
        c = state.get_constitution()
        if c and getattr(c, "style_rules", None):
            guidance = "\n".join(c.style_rules)
        if instruction:
            guidance = (guidance + "\n\nUser instruction: " + instruction).strip()

        src = Source(
            source_id=state.source.content_hash,
            name=source_path.name,
            file_path=str(source_path.absolute()),
            content_type=state.source.content_type if state.source.content_type in ["text/plain", "text/vtt"] else "text/plain",
            content=content,
        )

        cfg = get_atom_extraction_config()
        user_prompt = render_atom_extraction_prompt(src, guidance)
        return "", cfg.system_prompt, user_prompt

    if step == "theme":
        lower = instruction.lower()
        create_keywords = ["create theme", "generate theme", "new theme", "custom theme", "make theme"]
        style_keywords = ["dark theme", "light theme", "neon", "pastel", "vibrant", "colorful", "minimal"]
        if not (any(k in lower for k in create_keywords) or any(k in lower for k in style_keywords)):
            return "[note] Theme likely loads existing/default theme (no LLM).", "", ""

        from src.generation.theme.prompts import get_theme_creation_config, render_theme_creation_prompt

        c = state.get_constitution()
        guidance = ""
        if c and getattr(c, "style_rules", None):
            guidance = "\n".join(c.style_rules)
        if c and getattr(c, "tone", None):
            guidance = (guidance + f"\nTone: {c.tone}").strip()

        cfg = get_theme_creation_config()
        user_prompt = render_theme_creation_prompt(
            user_instruction=instruction,
            base_theme=None,
            intent_guidance=guidance,
        )
        return "", cfg.system_prompt, user_prompt

    if step == "story":
        atoms = state.get_atoms()
        if not atoms:
            return "[note] Run atoms first.", "", ""

        from src.generation.content import story_generator

        slide_count = None
        c = state.get_constitution()
        if c:
            slide_count = getattr(c, "slide_count_target", None)
        prompt = story_generator._get_story_prompt(atoms, instruction, slide_count, "")  # noqa: SLF001
        return "", "You are a presentation storyteller. Output only valid JSON array.", prompt

    if step == "content":
        atoms = state.get_atoms()
        if not atoms:
            return "[note] Run atoms first.", "", ""
        if not state.slides:
            return "[note] Run story first.", "", ""
        from src.generation.content.prompts import get_slide_generation_config, render_slide_generation_prompt

        cfg = get_slide_generation_config(project=str(state.project or "slidev"))
        base = render_slide_generation_prompt(
            atoms=atoms,
            user_instruction="",
            intent_guidance="",
            themes=None,
        )
        return "[note] Content prompts vary per draft slide; actual prompt is shown after execution.", cfg.system_prompt, base

    return "", "", ""


def init_session(
    source_file,
    instruction_text: str,
    output_name: str,
    project: str,
    mdx_theme: str,
    use_cache: bool,
) -> Tuple[
    Session,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
]:
    """Create output folder, state.json, trace file, and compute default prompts."""
    if isinstance(source_file, list):
        source_file = source_file[0] if source_file else None

    if source_file is None:
        empty_session: Session = {}
        empty = ""
        return (
            empty_session,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
        )

    output_name = (output_name or "ui_run").strip() or "ui_run"
    output_dir = Path("output") / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    sources_dir = output_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    src_path = Path(source_file.name)
    copied_source = sources_dir / src_path.name
    shutil.copy(src_path, copied_source)

    instruction = (instruction_text or "").strip()
    instruction = instruction.strip() or "Generate slides."

    state = PipelineState()
    state.load_default_themes()
    state.set_source(copied_source)
    state.project = project
    state.mdx_theme = mdx_theme
    state.save(output_dir / "state.json")

    trace_path = output_dir / "llm_trace.jsonl"
    try:
        trace_path.write_text("", encoding="utf-8")
    except Exception:
        pass

    session: Session = {
        "output_dir": str(output_dir),
        "instruction": instruction,
        "use_cache": bool(use_cache),
        "trace_pos": 0,
    }

    defp = {}
    for step in ["planner", "atoms", "theme", "story", "content"]:
        note, sys_p, user_p = build_default_prompts(session, step)
        defp[step] = (note, sys_p, user_p)

    return (
        session,
        defp["planner"][1],
        defp["planner"][2],
        defp["atoms"][1],
        defp["atoms"][2],
        defp["theme"][1],
        defp["theme"][2],
        defp["story"][1],
        defp["story"][2],
        defp["content"][1],
        defp["content"][2],
    )


def _update_trace(session: Session) -> Tuple[Session, List[dict]]:
    output_dir, _, trace_path = _session_paths(session)
    _ = output_dir
    pos = int(session.get("trace_pos", 0) or 0)
    new_pos, records = _read_new_trace(trace_path, pos)
    session["trace_pos"] = new_pos
    return session, records


def run_step_planner(
    session: Session, override_system: Optional[str], override_user: Optional[str]
) -> Tuple[Session, str, str]:
    session = _ensure_session(session)
    if not session.get("output_dir"):
        return session, "", ""

    output_dir, state_path, _ = _session_paths(session)
    state = PipelineState.load(state_path)
    instruction = str(session.get("instruction", ""))

    old_env = _with_llm_env(session, "planner", override_system, override_user)
    try:
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            state.todos = plan(state, instruction)
            state.save(state_path)
        log = buf.getvalue().strip() or "[planner] ok"

        session, records = _update_trace(session)
        records = _filter_records_for_step(records, "planner")
        _ = log
        return session, _format_llm_sent(records), _format_llm_response(records)
    finally:
        _restore_llm_env(old_env)


def run_step_constitution(session: Session) -> Tuple[Session, str]:
    session = _ensure_session(session)
    if not session.get("output_dir"):
        return session, "[error] Initialize first."

    output_dir, state_path, _ = _session_paths(session)
    state = PipelineState.load(state_path)
    instruction = str(session.get("instruction", ""))

    todo = _find_todo(state, TodoType.CONSTITUTION)
    if todo is None:
        return session, "[constitution] todo missing (run planner first)\n\n" + _constitution_text(state)

    executor = TodoExecutor(
        verbose=True,
        use_cache=bool(session.get("use_cache", True)),
        output_dir=output_dir,
        state_path=state_path,
    )

    buf = io.StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        executor.execute_todo(todo, state, instruction)
        state.save(state_path)

    _ = buf.getvalue().strip() or "[constitution] ok"
    return session, _constitution_text(state)


def run_step_todo_llm(
    session: Session,
    step: str,
    todo_type: TodoType,
    override_system: Optional[str],
    override_user: Optional[str],
) -> Tuple[Session, str, str, str]:
    session = _ensure_session(session)
    if not session.get("output_dir"):
        return session, f"[{step}] Initialize first.", "", ""

    output_dir, state_path, _ = _session_paths(session)
    state = PipelineState.load(state_path)
    instruction = str(session.get("instruction", ""))

    todo = _find_todo(state, todo_type)
    if todo is None:
        return session, f"[{step}] todo missing (run planner first)", "", ""

    executor = TodoExecutor(
        verbose=True,
        use_cache=bool(session.get("use_cache", True)),
        output_dir=output_dir,
        state_path=state_path,
    )

    old_env = _with_llm_env(session, step, override_system, override_user)
    try:
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            executor.execute_todo(todo, state, instruction)
            state.save(state_path)
        log = buf.getvalue().strip() or f"[{step}] ok"

        session, records = _update_trace(session)
        records = _filter_records_for_step(records, step)
        return session, _status_one_liner(log), _format_llm_sent(records), _format_llm_response(records)
    finally:
        _restore_llm_env(old_env)


def _refresh_predefined_prompt(session: Session, step: str) -> Tuple[str, str]:
    """Return (system_prompt, user_prompt) for a step based on current state.json.

    Notes are intentionally dropped (we removed note UI boxes).
    """
    try:
        _, sys_p, user_p = build_default_prompts(session, step)
        return sys_p, user_p
    except Exception:
        return "", ""


def _stream_llm_trace_updates(
    session: Session,
    step: str,
    trace_path: Path,
    from_pos: int,
    records: List[dict],
    last_sent: str,
    last_resp: str,
) -> Tuple[int, str, str, bool]:
    """Read new trace records and return (new_pos, sent, resp, changed)."""
    new_pos, new_records = _read_new_trace(trace_path, from_pos)
    if new_records:
        records.extend(new_records)
    step_records = _filter_records_for_step(records, step)
    sent = _format_llm_sent(step_records)
    resp = _format_llm_response(step_records)
    changed = (sent != last_sent) or (resp != last_resp)
    return new_pos, sent, resp, changed


def run_step_planner_stream(session: Session):
    """Stream planner updates: show sent immediately, response ASAP."""
    # Backwards-compatible default (no overrides)
    return run_step_planner_stream_with_overrides(session, None, None)


def run_step_planner_stream_with_overrides(
    session: Session,
    override_system: Optional[str],
    override_user: Optional[str],
):
    """Stream planner updates; optionally override prompts from the UI."""
    session = _ensure_session(session)
    if not session.get("output_dir"):
        yield session, "", ""
        return

    output_dir, state_path, trace_path = _session_paths(session)
    _ = output_dir
    instruction = str(session.get("instruction", ""))

    # Keep env set for the duration of the worker.
    old_env = _with_llm_env(session, "planner", override_system, override_user)
    result: dict = {"done": False, "log": "", "exc": None}

    def _worker():
        try:
            state = PipelineState.load(state_path)
            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(buf):
                state.todos = plan(state, instruction)
                state.save(state_path)
            result["log"] = buf.getvalue().strip() or "[planner] ok"
        except Exception as e:  # noqa: BLE001
            result["exc"] = e
        finally:
            result["done"] = True

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

    pos = int(session.get("trace_pos", 0) or 0)
    records: List[dict] = []
    sent = ""
    resp = ""

    # Initial state
    yield session, sent, resp

    try:
        while not result["done"]:
            pos, sent2, resp2, changed = _stream_llm_trace_updates(session, "planner", trace_path, pos, records, sent, resp)
            if changed:
                sent, resp = sent2, resp2
            # Yield every tick so UI (and timer) keeps updating.
            yield session, sent, resp
            time.sleep(0.2)

        # Final read
        pos, sent2, resp2, changed = _stream_llm_trace_updates(session, "planner", trace_path, pos, records, sent, resp)
        if changed:
            sent, resp = sent2, resp2

        session["trace_pos"] = pos

        yield session, sent, resp
    finally:
        _restore_llm_env(old_env)


def run_step_todo_llm_stream(session: Session, step: str, todo_type: TodoType):
    """Stream todo LLM step updates: show sent immediately, response ASAP."""
    return run_step_todo_llm_stream_with_overrides(session, step, todo_type, None, None)


def run_step_todo_llm_stream_with_overrides(
    session: Session,
    step: str,
    todo_type: TodoType,
    override_system: Optional[str],
    override_user: Optional[str],
):
    """Stream todo LLM step updates; optionally override prompts from the UI."""
    session = _ensure_session(session)
    if not session.get("output_dir"):
        yield session, "", ""
        return

    output_dir, state_path, trace_path = _session_paths(session)
    state = PipelineState.load(state_path)
    instruction = str(session.get("instruction", ""))

    todo = _find_todo(state, todo_type)
    if todo is None:
        yield session, "", ""
        return

    executor = TodoExecutor(
        verbose=True,
        use_cache=bool(session.get("use_cache", True)),
        output_dir=output_dir,
        state_path=state_path,
    )

    old_env = _with_llm_env(session, step, override_system, override_user)
    result: dict = {"done": False, "log": "", "exc": None}

    def _worker():
        try:
            print(f"[UI] Starting execution for step: {step} (todo: {todo_type})")
            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(buf):
                executor.execute_todo(todo, state, instruction)
                state.save(state_path)
            result["log"] = buf.getvalue().strip() or f"[{step}] ok"
            print(f"[UI] Execution finished for step: {step}")
        except Exception as e:  # noqa: BLE001
            print(f"[UI] Execution failed for step: {step}: {e}")
            result["exc"] = e
        finally:
            result["done"] = True

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

    pos = int(session.get("trace_pos", 0) or 0)
    records: List[dict] = []
    sent = ""
    resp = ""
    yield session, sent, resp

    try:
        while not result["done"]:
            pos, sent2, resp2, changed = _stream_llm_trace_updates(session, step, trace_path, pos, records, sent, resp)
            if changed:
                sent, resp = sent2, resp2
            # Yield every tick so UI (and timer) keeps updating.
            yield session, sent, resp
            time.sleep(0.2)

        pos, sent2, resp2, changed = _stream_llm_trace_updates(session, step, trace_path, pos, records, sent, resp)
        if changed:
            sent, resp = sent2, resp2

        session["trace_pos"] = pos

        # If we have a tool log but no LLM response (or short one), show the log.
        # This is critical for tools that exit early or don't use LLM.
        tool_log = result.get("log", "").strip()
        if tool_log and (not resp or len(resp) < 50):
            if resp:
                resp = f"{resp}\n\n--- Tool Output ---\n{tool_log}"
            else:
                resp = tool_log

        yield session, sent, resp
    finally:
        _restore_llm_env(old_env)


def run_step_atoms_and_refresh_stream(session: Session, override_system: Optional[str], override_user: Optional[str]):
    for session, sent, resp in run_step_todo_llm_stream_with_overrides(
        session, "atoms", TodoType.ATOMS, override_system, override_user
    ):
        # While running, keep downstream prompts blank.
        yield session, sent, resp, "", "", "", ""

    story_sys, story_user = _refresh_predefined_prompt(session, "story")
    content_sys, content_user = _refresh_predefined_prompt(session, "content")
    yield session, sent, resp, story_sys, story_user, content_sys, content_user


def run_step_story_and_refresh_stream(session: Session, override_system: Optional[str], override_user: Optional[str]):
    for session, sent, resp in run_step_todo_llm_stream_with_overrides(
        session, "story", TodoType.STORY, override_system, override_user
    ):
        yield session, sent, resp, "", ""

    content_sys, content_user = _refresh_predefined_prompt(session, "content")
    yield session, sent, resp, content_sys, content_user


def run_step_theme_stream(session: Session, override_system: Optional[str], override_user: Optional[str]):
    """Theme can be LLM or non-LLM; if no LLM, show what changed instead."""
    session = _ensure_session(session)
    if not session.get("output_dir"):
        yield session, gr.update(value="[error] Initialize first.", visible=True), gr.update(value="", visible=False), gr.update(value="", visible=False)
        return

    _, state_path, _ = _session_paths(session)
    if not state_path.exists():
        yield session, gr.update(value="[error] state.json missing (Initialize first)", visible=True), gr.update(value="", visible=False), gr.update(value="", visible=False)
        return

    before = PipelineState.load(state_path)

    last_sent = ""
    last_resp = ""
    for session, sent, resp in run_step_todo_llm_stream_with_overrides(
        session, "theme", TodoType.THEME, override_system, override_user
    ):
        last_sent, last_resp = sent, resp
        # During execution, prefer showing LLM panes (they may remain empty).
        yield (
            session,
            gr.update(value="", visible=False),
            gr.update(value=sent, visible=True),
            gr.update(value=resp, visible=True),
        )

    after = PipelineState.load(state_path)
    summary = _theme_change_summary(before, after)
    used_llm = bool((last_sent or "").strip() or (last_resp or "").strip())
    if used_llm:
        yield (
            session,
            gr.update(value="", visible=False),
            gr.update(value=last_sent, visible=True),
            gr.update(value=last_resp, visible=True),
        )
    else:
        yield (
            session,
            gr.update(value=summary, visible=True),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
        )


def run_step_content_stream(session: Session, override_system: Optional[str], override_user: Optional[str]):
    """Streaming wrapper for content step (Gradio can't stream from a lambda)."""
    yield from run_step_todo_llm_stream_with_overrides(
        session,
        "content",
        TodoType.CONTENT,
        override_system,
        override_user,
    )


def run_step_planner_stream_with_overrides_timed(
    session: Session,
    override_system: Optional[str],
    override_user: Optional[str],
):
    t0 = time.perf_counter()
    for session, sent, resp in run_step_planner_stream_with_overrides(session, override_system, override_user):
        elapsed = f"{(time.perf_counter() - t0):.2f}s"
        yield session, sent, resp, elapsed


def run_step_atoms_and_refresh_stream_timed(session: Session, override_system: Optional[str], override_user: Optional[str]):
    t0 = time.perf_counter()
    for session, sent, resp, story_sys, story_user, content_sys, content_user in run_step_atoms_and_refresh_stream(
        session, override_system, override_user
    ):
        elapsed = f"{(time.perf_counter() - t0):.2f}s"
        yield session, sent, resp, story_sys, story_user, content_sys, content_user, elapsed


def run_step_story_and_refresh_stream_timed(session: Session, override_system: Optional[str], override_user: Optional[str]):
    t0 = time.perf_counter()
    for session, sent, resp, content_sys, content_user in run_step_story_and_refresh_stream(session, override_system, override_user):
        elapsed = f"{(time.perf_counter() - t0):.2f}s"
        yield session, sent, resp, content_sys, content_user, elapsed


def run_step_theme_stream_timed(session: Session, override_system: Optional[str], override_user: Optional[str]):
    t0 = time.perf_counter()
    for session, theme_result, sent, resp in run_step_theme_stream(session, override_system, override_user):
        elapsed = f"{(time.perf_counter() - t0):.2f}s"
        yield session, theme_result, sent, resp, elapsed


def run_step_content_stream_timed(session: Session, override_system: Optional[str], override_user: Optional[str]):
    t0 = time.perf_counter()
    for session, sent, resp in run_step_content_stream(session, override_system, override_user):
        elapsed = f"{(time.perf_counter() - t0):.2f}s"
        yield session, sent, resp, elapsed


def run_step_atoms_and_refresh(session: Session) -> Tuple[Session, str, str, str, str, str, str, str]:
    session, log, sent, resp = run_step_todo_llm(session, "atoms", TodoType.ATOMS, None, None)
    story_sys, story_user = _refresh_predefined_prompt(session, "story")
    content_sys, content_user = _refresh_predefined_prompt(session, "content")
    return session, log, sent, resp, story_sys, story_user, content_sys, content_user


def run_step_story_and_refresh(session: Session) -> Tuple[Session, str, str, str, str, str]:
    session, log, sent, resp = run_step_todo_llm(session, "story", TodoType.STORY, None, None)
    content_sys, content_user = _refresh_predefined_prompt(session, "content")
    return session, log, sent, resp, content_sys, content_user


def run_step_export(session: Session) -> Tuple[Session, List[str], str]:
    session = _ensure_session(session)
    if not session.get("output_dir"):
        return session, [], "[error] Initialize first."

    output_dir, state_path, _ = _session_paths(session)
    state = PipelineState.load(state_path)
    instruction = str(session.get("instruction", ""))

    todo = _find_todo(state, TodoType.EXPORT)
    if todo is None:
        return session, _as_downloadable_files(_collect_outputs(output_dir)), "[export] todo missing (run planner first)"

    executor = TodoExecutor(
        verbose=True,
        use_cache=bool(session.get("use_cache", True)),
        output_dir=output_dir,
        state_path=state_path,
    )

    buf = io.StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        executor.execute_todo(todo, state, instruction)
        state.save(state_path)

    log = buf.getvalue().strip() or "[export] ok"
    files = _collect_outputs(output_dir)
    downloads = _as_downloadable_files(files)
    preview = "\n\n".join([log, "\n--- slides.mdx preview ---\n", _read_mdx_preview(output_dir)]).strip()
    return session, downloads, preview


_REACT_PREVIEW_PROC: Optional[subprocess.Popen] = None
_REACT_PREVIEW_LOCK = threading.Lock()


def _is_port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.3):
            return True
    except Exception:
        return False


def _ensure_react_preview_server() -> Tuple[bool, str]:
    """Ensure Next dev server is running for the React MDX preview."""
    host = "127.0.0.1"
    port = 3000
    if _is_port_open(host, port):
        return True, ""

    react_dir = Path(__file__).parent / "src" / "paged" / "render" / "react"
    # ui.py lives at repo root, so build absolute path from cwd
    react_dir = Path.cwd() / "src" / "paged" / "render" / "react"
    if not react_dir.exists():
        return False, "React preview app not found at src/paged/render/react"

    with _REACT_PREVIEW_LOCK:
        global _REACT_PREVIEW_PROC
        if _is_port_open(host, port):
            return True, ""

        # If we already started a process and it died, clear it.
        if _REACT_PREVIEW_PROC is not None and _REACT_PREVIEW_PROC.poll() is not None:
            _REACT_PREVIEW_PROC = None

        if _REACT_PREVIEW_PROC is None:
            npm = "npm.cmd" if Path("C:/Windows").exists() else "npm"
            env = os.environ.copy()
            env["PORT"] = str(port)
            env["HOSTNAME"] = host
            try:
                _REACT_PREVIEW_PROC = subprocess.Popen(
                    [npm, "run", "dev", "--", "-p", str(port), "-H", host],
                    cwd=str(react_dir),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=env,
                )
            except Exception as e:  # noqa: BLE001
                _REACT_PREVIEW_PROC = None
                return False, f"Failed to start React preview server: {e}"

    # Wait briefly for server to come up
    t0 = time.time()
    while time.time() - t0 < 12:
        if _is_port_open(host, port):
            return True, ""
        time.sleep(0.25)

    return False, "React preview server did not start (check Node/npm deps)"


def get_export_preview(session: Session) -> Tuple[Session, str]:
    """Single Preview button: render slides in browser via React viewer."""
    session = _ensure_session(session)
    if not session.get("output_dir"):
        return session, "<div>Initialize first.</div>"

    output_dir, state_path, _ = _session_paths(session)
    if not state_path.exists():
        return session, "<div>state.json missing (run Initialize).</div>"

    state = PipelineState.load(state_path)
    if not (state.slides or []):
        return session, "<div>No slides in state (run story/content first).</div>"

    ok, err = _ensure_react_preview_server()
    if not ok:
        return session, f"<div>Preview failed: {_html.escape(err)}</div>"

    url = f"http://127.0.0.1:3000/{output_dir.name}"
    iframe = (
        "<div style='margin-bottom:8px'>Preview (React MDX renderer)</div>"
        "<iframe "
        "style='width:100%;height:85vh;min-height:900px;border:1px solid #ddd;overflow:hidden' "
        f"src=\"{_html.escape(url, quote=True)}\"></iframe>"
    )
    return session, iframe


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="UCE Pipeline UI") as demo:
        gr.Markdown("# UCE Pipeline UI\nInitialize a session, then run each step.")

        session_state = gr.State({})

        source_state = gr.State(None)

        with gr.Row():
            import_progress_upload = gr.UploadButton(
                "Import progress",
                file_count="single",
                variant="secondary",
                scale=1,
            )
            export_progress_btn = gr.Button("Export progress", scale=0, min_width=160)
            export_progress_download = gr.DownloadButton(
                "Download progress.json",
                value=None,
                visible=False,
                elem_id="export_progress_download",
                scale=0,
                min_width=220,
            )
            export_progress_done = gr.Textbox(
                label="",
                value="",
                visible=False,
                elem_id="export_progress_done",
            )

        with gr.Row():
            source_name = gr.Textbox(
                label="Source file",
                lines=1,
                max_lines=1,
                interactive=False,
                elem_classes=["path-dark"],
                scale=1,
            )
            source_upload = gr.UploadButton(
                "Upload",
                file_count="single",
                variant="secondary",
                size="lg",
                scale=0,
                min_width=120,
            )

        def _on_source_uploaded(f):
            if f is None:
                return None, ""
            name = getattr(f, "name", "")
            return f, name or ""

        source_upload.upload(
            fn=_on_source_uploaded,
            inputs=[source_upload],
            outputs=[source_state, source_name],
        )

        with gr.Row():
            instruction_text = gr.Textbox(
                label="User instruction (optional)",
                lines=1,
                max_lines=1,
                elem_classes=["path-dark"],
            )

        with gr.Row():
            output_name = gr.Textbox(label="Output name (under output/)", value=f"ui_run_{_now_id()}")
            project = gr.Dropdown(label="Project", choices=["react-mdx", "slidev"], value="react-mdx")
            mdx_theme = gr.Dropdown(
                label="MDX theme (react-mdx)",
                choices=["business", "cyber", "minimal", "academic", "creative", "duolingo", "dark", "purple"],
                value="business",
            )
            use_cache = gr.Checkbox(label="Use cache", value=True)

        init_btn = gr.Button("Initialize")

        gr.Markdown("## 0) planner")
        with gr.Accordion("Prompts", open=False):
            planner_default_sys = gr.Code(
                label="system prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
            planner_default_user = gr.Code(
                label="user prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
        with gr.Row():
            with gr.Column(scale=9, min_width=160):
                planner_run = gr.Button("0) Run planner")
            with gr.Column(scale=1, min_width=60):
                planner_timer = gr.HTML(value="", elem_id="planner_timer")
        with gr.Row():
            with gr.Column():
                planner_sent = gr.Textbox(label="call", lines=8, max_lines=8)
            with gr.Column():
                planner_resp = gr.Textbox(label="response", lines=8, max_lines=8)

        gr.Markdown("## 1) constitution")
        constitution_run = gr.Button("1) Run constitution")
        constitution_result = gr.Textbox(label="constitution result", lines=8, max_lines=8)

        gr.Markdown("## 2) atoms")
        with gr.Accordion("Prompts", open=False):
            atoms_default_sys = gr.Code(
                label="system prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
            atoms_default_user = gr.Code(
                label="user prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
        with gr.Row():
            with gr.Column(scale=9, min_width=160):
                atoms_run = gr.Button("2) Run atoms")
            with gr.Column(scale=1, min_width=60):
                atoms_timer = gr.HTML(value="", elem_id="atoms_timer")
        with gr.Row():
            with gr.Column():
                atoms_sent = gr.Textbox(label="call", lines=8, max_lines=8)
            with gr.Column():
                atoms_resp = gr.Textbox(label="response", lines=8, max_lines=8)

        gr.Markdown("## 3) theme")
        with gr.Accordion("Prompts", open=False):
            theme_default_sys = gr.Code(
                label="system prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
            theme_default_user = gr.Code(
                label="user prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
        with gr.Row():
            with gr.Column(scale=9, min_width=160):
                theme_run = gr.Button("3) Run theme")
            with gr.Column(scale=1, min_width=60):
                theme_timer = gr.HTML(value="", elem_id="theme_timer")
        theme_result = gr.Textbox(label="theme result (no LLM)", lines=6, max_lines=6, visible=False)
        with gr.Row():
            with gr.Column():
                theme_sent = gr.Textbox(label="call", lines=8, max_lines=8, visible=True)
            with gr.Column():
                theme_resp = gr.Textbox(label="response", lines=8, max_lines=8, visible=True)

        gr.Markdown("## 4) story")
        with gr.Accordion("Prompts", open=False):
            story_default_sys = gr.Code(
                label="system prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
            story_default_user = gr.Code(
                label="user prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
        with gr.Row():
            with gr.Column(scale=9, min_width=160):
                story_run = gr.Button("4) Run story")
            with gr.Column(scale=1, min_width=60):
                story_timer = gr.HTML(value="", elem_id="story_timer")
        with gr.Row():
            with gr.Column():
                story_sent = gr.Textbox(label="call", lines=8, max_lines=8)
            with gr.Column():
                story_resp = gr.Textbox(label="response", lines=8, max_lines=8)

        gr.Markdown("## 5) content")
        with gr.Accordion("Prompts", open=False):
            content_default_sys = gr.Code(
                label="system prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
            content_default_user = gr.Code(
                label="user prompt",
                language="markdown",
                lines=8,
                max_lines=8,
                elem_classes=["code-fixed"],
                interactive=True,
            )
        with gr.Row():
            with gr.Column(scale=9, min_width=160):
                content_run = gr.Button("5) Run content")
            with gr.Column(scale=1, min_width=60):
                content_timer = gr.HTML(value="", elem_id="content_timer")
        with gr.Row():
            with gr.Column():
                content_sent = gr.Textbox(label="call", lines=8, max_lines=8)
            with gr.Column():
                content_resp = gr.Textbox(label="response", lines=8, max_lines=8)

        gr.Markdown("## 6) export")
        export_run = gr.Button("6) Run export")
        export_preview_btn = gr.Button("Preview")
        export_preview_link = gr.HTML(label="preview")
        output_files = gr.Files(label="produced files")
        export_preview = gr.Code(
            label="export preview",
            language="markdown",
            lines=10,
            max_lines=10,
            elem_classes=["code-fixed"],
        )

        init_btn.click(
            fn=init_session,
            inputs=[source_state, instruction_text, output_name, project, mdx_theme, use_cache],
            outputs=[
                session_state,
                planner_default_sys,
                planner_default_user,
                atoms_default_sys,
                atoms_default_user,
                theme_default_sys,
                theme_default_user,
                story_default_sys,
                story_default_user,
                content_default_sys,
                content_default_user,
            ],
        )

        export_progress_btn.click(
            fn=export_progress,
            inputs=[
                session_state,
                planner_default_sys,
                planner_default_user,
                atoms_default_sys,
                atoms_default_user,
                theme_default_sys,
                theme_default_user,
                story_default_sys,
                story_default_user,
                content_default_sys,
                content_default_user,
            ],
            outputs=[session_state, export_progress_download, export_progress_done],
        )

        export_progress_done.change(
            fn=None,
            inputs=None,
            outputs=None,
            js="""
() => {
    const tryClick = () => {
        const root = document.getElementById('export_progress_download');
        if (!root) return false;
        const el = root.querySelector('a, button, input[type="button"], input[type="submit"]');
        if (el && typeof el.click === 'function') {
            el.click();
            return true;
        }
        return false;
    };

    // Wait a bit for Gradio to render the download target.
    let tries = 0;
    const timer = setInterval(() => {
        tries += 1;
        let ok = false;
        try { ok = tryClick(); } catch (e) { ok = false; }
        if (ok || tries >= 50) clearInterval(timer);
    }, 100);
}
""",
        )

        def _on_import_uploaded(f):
            return import_progress(f)

        import_progress_upload.upload(
            fn=_on_import_uploaded,
            inputs=[import_progress_upload],
            outputs=[
                session_state,
                source_name,
                instruction_text,
                output_name,
                project,
                mdx_theme,
                use_cache,
                planner_default_sys,
                planner_default_user,
                atoms_default_sys,
                atoms_default_user,
                theme_default_sys,
                theme_default_user,
                story_default_sys,
                story_default_user,
                content_default_sys,
                content_default_user,
                constitution_result,
                planner_sent,
                planner_resp,
                atoms_sent,
                atoms_resp,
                theme_result,
                theme_sent,
                theme_resp,
                story_sent,
                story_resp,
                content_sent,
                content_resp,
            ],
        )

        planner_run.click(
            fn=run_step_planner_stream_with_overrides_timed,
            inputs=[session_state, planner_default_sys, planner_default_user],
            outputs=[session_state, planner_sent, planner_resp, planner_timer],
        )

        constitution_run.click(
            fn=run_step_constitution,
            inputs=[session_state],
            outputs=[session_state, constitution_result],
        )

        atoms_run.click(
            fn=run_step_atoms_and_refresh_stream_timed,
            inputs=[session_state, atoms_default_sys, atoms_default_user],
            outputs=[
                session_state,
                atoms_sent,
                atoms_resp,
                story_default_sys,
                story_default_user,
                content_default_sys,
                content_default_user,
                atoms_timer,
            ],
        )

        theme_run.click(
            fn=run_step_theme_stream_timed,
            inputs=[session_state, theme_default_sys, theme_default_user],
            outputs=[session_state, theme_result, theme_sent, theme_resp, theme_timer],
        )

        story_run.click(
            fn=run_step_story_and_refresh_stream_timed,
            inputs=[session_state, story_default_sys, story_default_user],
            outputs=[
                session_state,
                story_sent,
                story_resp,
                content_default_sys,
                content_default_user,
                story_timer,
            ],
        )

        content_run.click(
            fn=run_step_content_stream_timed,
            inputs=[session_state, content_default_sys, content_default_user],
            outputs=[session_state, content_sent, content_resp, content_timer],
        )

        export_run.click(
            fn=run_step_export,
            inputs=[session_state],
            outputs=[session_state, output_files, export_preview],
        )

        export_preview_btn.click(
            fn=get_export_preview,
            inputs=[session_state],
            outputs=[session_state, export_preview_link],
        )

    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch(css=UI_CSS)
