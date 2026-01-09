from __future__ import annotations

import json
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.tools.codegen import (
    CodegenTool,
    _extract_invent_components_from_mdx,
    _validate_and_fix_component_code,
)


def main() -> None:
    mdx_path = Path(__file__).with_name("min_codegen_demo.mdx")
    mdx_text = mdx_path.read_text(encoding="utf-8")

    comps = _extract_invent_components_from_mdx(mdx_text)
    print(f"[demo] extracted InventComponent count: {len(comps)}")
    if not comps:
        raise SystemExit(1)

    tool = CodegenTool()
    comp = comps[0]

    user_prompt = tool._build_single_component_prompt(  # noqa: SLF001
        comp=comp,
        existing_components=[],
        user_instruction="",
    )

    print("\n===== CODEGEN SYSTEM PROMPT (first 40 lines) =====")
    sys_lines = tool.system_prompt.splitlines()
    print("\n".join(sys_lines[:40]))

    print("\n===== CODEGEN USER PROMPT =====")
    print(user_prompt)

    expected_json_path = Path(__file__).with_name("min_codegen_demo_expected_output.json")
    expected = json.loads(expected_json_path.read_text(encoding="utf-8"))
    comp0 = expected["components"][0]

    fixed_code, fixed_props, fixes = _validate_and_fix_component_code(
        code=comp0["code"],
        props_interface=comp0["props_interface"],
        component_name=comp0["name"],
    )

    print("\n===== VALIDATOR FIXES =====")
    print("- " + "\n- ".join(fixes) if fixes else "(none)")

    print("\n===== FIXED PROPS (first 15 lines) =====")
    print("\n".join(fixed_props.splitlines()[:15]))

    print("\n===== FIXED CODE (first 40 lines) =====")
    print("\n".join(fixed_code.splitlines()[:40]))


if __name__ == "__main__":
    main()
