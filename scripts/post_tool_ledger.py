#!/usr/bin/env python3
"""PostToolUse hook: automatically maintains scratch/argon_state.json photographic ledger."""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from argon_core import (  # noqa: E402
    MUTATION_TOOL_NAMES,
    canonical_path,
    extract_tool_target_path,
    is_artifact_or_scratch_path,
    load_json_file,
    read_stdin_json,
    resolve_session_state,
    resolve_state_ledger_path,
    save_json_file,
)

OOP_MODS = (
    r"(?:(?:export|default|public|private|protected|internal|final|abstract|sealed|"
    r"open|data|value|base|interface|mixin|readonly|partial|static)\s+)*"
)

# Tuple format: (kind_rank, compiled_regex)
# kind_rank=0 -> structural types (class/interface/struct/enum/trait/type/SQL table/view)
# kind_rank=1 -> functions/methods/constants/SQL procedures
SYMBOL_PATTERNS = [
    (
        0,
        re.compile(
            r"^([ \t]*)" + OOP_MODS + r"(?:class|interface|struct|enum|trait|record)\s+([A-Za-z_$][A-Za-z0-9_$]*)\b",
            re.MULTILINE,
        ),
    ),
    (
        0,
        re.compile(
            r"^([ \t]*)type\s+([A-Za-z_][A-Za-z0-9_]*)\s+(?:struct|interface)\b",
            re.MULTILINE,
        ),
    ),
    (
        0,
        re.compile(
            r"^([ \t]*)(?:export\s+)?type\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*(?:<[^=]+>)?\s*=",
            re.MULTILINE,
        ),
    ),
    (
        0,
        re.compile(
            r"^([ \t]*)CREATE\s+(?:OR\s+REPLACE\s+)?(?:TEMP\s+|TEMPORARY\s+)?(?:TABLE|VIEW|MATERIALIZED\s+VIEW)\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:[A-Za-z0-9_]+\.)?([A-Za-z_][A-Za-z0-9_]*)",
            re.MULTILINE | re.IGNORECASE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)def\s+(?:self\.)?([A-Za-z_][A-Za-z0-9_!?]*)\b",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\b",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)export\s+(?:const|let)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*(?::[^=\n]+)?=",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)const\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*(?:async\s*)?(?:\([^=\n]*\)|[A-Za-z_$][A-Za-z0-9_$]*)\s*=>",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)func\s+(?:\([^)]+\)\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)(?:pub(?:\([^)]+\))?\s+)?(?:async\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)\b",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)(?:(?:public|private|protected|internal|override|suspend|inline)\s+)*fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*[<(\[]",
            re.MULTILINE,
        ),
    ),
    (
        1,
        re.compile(
            r"^([ \t]*)CREATE\s+(?:OR\s+REPLACE\s+)?(?:FUNCTION|PROCEDURE)\s+(?:[A-Za-z0-9_]+\.)?([A-Za-z_][A-Za-z0-9_]*)",
            re.MULTILINE | re.IGNORECASE,
        ),
    ),
]

IGNORED_DUNDER = {"__init__", "__repr__", "__str__", "__eq__", "__hash__"}


def extract_file_symbols(file_path, max_symbols=6):
    """Extract top-level classes/types/functions first, falling back to indented methods if room remains."""
    if not os.path.isfile(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(65536)
    except Exception:
        return []

    base = os.path.basename(file_path)
    candidates = []
    for kind_rank, pattern in SYMBOL_PATTERNS:
        for match in pattern.finditer(content):
            indent = match.group(1) or ""
            sym = match.group(2)
            if sym in IGNORED_DUNDER:
                continue
            is_indented = 1 if len(indent) > 0 else 0
            candidates.append((is_indented, kind_rank, match.start(), f"{base}:{sym}"))

    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    seen = []
    for _ind, _rank, _pos, qualified in candidates:
        if qualified not in seen:
            seen.append(qualified)
            if len(seen) >= max_symbols:
                break
    return seen


def format_display_path(canon_file, workspace_paths):
    """Format file path relative to workspace root when possible for compact ledger display."""
    for wp in workspace_paths or []:
        canon_wp = canonical_path(wp)
        if canon_wp and canon_file.startswith(canon_wp + os.sep):
            return os.path.relpath(canon_file, canon_wp)
    home = os.path.realpath(os.path.expanduser("~"))
    if canon_file.startswith(home + os.sep):
        return "~/" + os.path.relpath(canon_file, home)
    return canon_file


def main():
    data = read_stdin_json()
    if not data:
        print("{}")
        return

    state = resolve_session_state(data)
    if not state["active"]:
        print("{}")
        return

    # Never record failed tool executions
    if data.get("error"):
        print("{}")
        return

    tool_call = data.get("toolCall", {})
    name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    if name not in MUTATION_TOOL_NAMES:
        print("{}")
        return

    artifact_dir = data.get("artifactDirectoryPath", "")
    conv_id = data.get("conversationId", "")
    workspace_paths = data.get("workspacePaths", [])
    raw_path = extract_tool_target_path(name, args)

    if not raw_path or is_artifact_or_scratch_path(raw_path, artifact_dir, conv_id):
        print("{}")
        return

    canon_file = canonical_path(raw_path)
    if not canon_file or not os.path.isfile(canon_file):
        print("{}")
        return

    ledger_path = resolve_state_ledger_path(artifact_dir, conv_id)
    ledger = load_json_file(ledger_path)

    # 1. Record verified touched canonical path (unlocks subsequent edits on newly created files)
    touched = list(ledger.get("verifiedTouchedPaths", []))
    if canon_file not in touched:
        touched.append(canon_file)
    ledger["verifiedTouchedPaths"] = touched[-50:]

    # 2. Record compact display path (most recent first, max 8)
    disp = format_display_path(canon_file, workspace_paths)
    mod_files = [p for p in ledger.get("modifiedFiles", []) if p != disp]
    mod_files.insert(0, disp)
    ledger["modifiedFiles"] = mod_files[:8]

    # 3. Extract and refresh top-level symbols for this file (max 12 across session)
    base_prefix = os.path.basename(canon_file) + ":"
    existing_symbols = [
        s for s in ledger.get("exportedSymbols", []) if not s.startswith(base_prefix)
    ]
    new_symbols = extract_file_symbols(canon_file, max_symbols=6)
    ledger["exportedSymbols"] = (new_symbols + existing_symbols)[:12]

    ledger["activeRole"] = state["role"]
    ledger["activeLevel"] = state["level"]

    save_json_file(ledger_path, ledger)
    print("{}")


if __name__ == "__main__":
    main()
