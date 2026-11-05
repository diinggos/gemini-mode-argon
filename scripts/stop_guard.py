#!/usr/bin/env python3
"""Stop hook: state-aware Exit-Code-0 verification gate preventing premature exit."""

import json
import os
import re
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from argon_core import (  # noqa: E402
    MUTATION_TOOL_NAMES,
    canonical_path,
    extract_tool_target_path,
    is_artifact_or_scratch_path,
    iter_transcript_tool_events,
    load_json_file,
    read_stdin_json,
    resolve_session_state,
    save_json_file,
    unwrap_arg,
)

TRACKER_FILE = os.path.join(tempfile.gettempdir(), "argon_stop_guard_tracker.json")

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".dart",
    ".rb",
    ".php",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".swift",
    ".sh",
    ".sql",
}

VERIFICATION_CMD_RE = re.compile(
    r"(?:"
    r"(?:^|\s|(?:[\w./~-]+/))(?:pytest|vitest|jest|mocha|ruff|flake8|mypy|pyright|eslint|biome|tsc|phpunit|pest|rspec|ctest|playwright)\b"
    r"|\b(?:uv|poetry|pipenv)\s+run\s+(?:pytest|python3?(?:\.\d+)?\s+-m\s+(?:pytest|unittest)|\S*(?:test|audit|verify)\S*\.py)\b"
    r"|\bcargo\s+(?:test|check|build|clippy)\b"
    r"|\bgo\s+(?:test|vet|build)\b"
    r"|\b(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?(?:test|check|lint|typecheck|build)\b"
    r"|\b(?:npx|bunx|pnpx)\s+(?:vitest|jest|mocha|playwright|tsc)\b"
    r"|\b(?:dart|flutter)\s+(?:test|analyze)\b"
    r"|(?:^|\s|(?:[\w./~-]+/))(?:mvn|gradlew?)\s+(?:test|check|compile|verify)\b"
    r"|\bdotnet\s+(?:test|build)\b"
    r"|\bbundle\s+exec\s+(?:rspec|rake\s+test)\b"
    r"|\brake\s+test\b"
    r"|\bphp\s+artisan\s+test\b"
    r"|\bswift\s+(?:test|build)\b"
    r"|\bcmake\s+--build\b"
    r"|\bmake\s+(?:test|check|build)\b"
    r"|(?:^|\s|(?:[\w./~-]+/))python3?(?:\.\d+)?\s+(?:-m\s+(?:pytest|unittest|py_compile|doctest)|\S*(?:test|audit|verify)\S*\.py)\b"
    r"|\b(?:bash|sh|zsh)\s+-n\b"
    r"|\bEXPLAIN\b"
    r")",
    re.IGNORECASE,
)


def inspect_code_verification(transcript_path, artifact_dir="", conv_id=""):
    """Check latest source edit against subsequent verification runs using (step_idx, call_idx) tuples."""
    edits = []
    verifications = []

    for step_idx, call_idx, name, args, failed, exit_code in iter_transcript_tool_events(
        transcript_path
    ):
        if name in MUTATION_TOOL_NAMES and not failed:
            raw_p = extract_tool_target_path(name, args)
            if not raw_p or is_artifact_or_scratch_path(raw_p, artifact_dir, conv_id):
                continue
            ext = os.path.splitext(str(raw_p))[1].lower()
            if ext in CODE_EXTENSIONS:
                edits.append(((step_idx, call_idx), canonical_path(raw_p)))
        elif name == "run_command":
            cmd = str(unwrap_arg(args.get("CommandLine", "")))
            if VERIFICATION_CMD_RE.search(cmd):
                if exit_code == "RUNNING":
                    continue
                passed = (not failed) and (exit_code is None or exit_code == 0)
                verifications.append(((step_idx, call_idx), passed, exit_code))

    if not edits:
        return None, None, (-1, -1), None

    last_edit_pos, last_canon_file = edits[-1]
    last_edit_step = last_edit_pos[0]

    # Verification must run in a subsequent planner step (step_idx > last_edit_step)
    # because tools within the same batch can execute concurrently.
    post_runs = [v for v in verifications if v[0][0] > last_edit_step]

    # Failures in the same batch or subsequent runs immediately block exit for Reflexion
    same_or_later_failures = [v for v in verifications if v[0] >= last_edit_pos and not v[1]]
    if same_or_later_failures:
        _v_pos, _passed, latest_code = same_or_later_failures[-1]
        return "failed_test", last_canon_file, last_edit_pos, latest_code

    if not post_runs:
        return "unverified", last_canon_file, last_edit_pos, None

    _v_pos, latest_passed, latest_code = post_runs[-1]
    if not latest_passed:
        return "failed_test", last_canon_file, last_edit_pos, latest_code

    return None, None, (-1, -1), None


def main():
    data = read_stdin_json()
    if not data:
        print(json.dumps({"decision": "allow"}))
        return

    reason = data.get("terminationReason", "")
    if reason != "NO_TOOL_CALL":
        print(json.dumps({"decision": "allow"}))
        return

    # Reactive Wakeup Gate: if background tasks or subagents are still working, allow pause without burning tracker
    if data.get("fullyIdle") is False:
        print(json.dumps({"decision": "allow"}))
        return

    state = resolve_session_state(data)
    if not state["active"] or state["role"] in ("reviewer", "researcher"):
        print(json.dumps({"decision": "allow"}))
        return

    transcript_path = data.get("transcriptPath", "")
    artifact_dir = data.get("artifactDirectoryPath", "")
    conv_id = data.get("conversationId", "default")

    issue_kind, canon_file, last_edit_pos, exit_code = inspect_code_verification(
        transcript_path, artifact_dir, conv_id
    )
    if issue_kind and canon_file:
        tracker = load_json_file(TRACKER_FILE)
        key = f"{conv_id}:{canon_file}:{last_edit_pos[0]}_{last_edit_pos[1]}:{issue_kind}"
        if tracker.get(key, 0) < 1:
            tracker[key] = 1
            if len(tracker) > 500:
                oldest_keys = list(tracker.keys())[:-400]
                for k in oldest_keys:
                    tracker.pop(k, None)
            save_json_file(TRACKER_FILE, tracker)

            base = os.path.basename(canon_file)
            if issue_kind == "unverified":
                msg = (
                    f"Argon Deterministic Verification Gate: Code changes in '{base}' have not "
                    "been verified via terminal test/build/lint. Execute a non-interactive check "
                    "(Exit Code 0) before concluding."
                )
            else:
                code_str = exit_code if exit_code is not None else "non-zero"
                msg = (
                    f"Argon Reflexion Auto-Healing Gate: Latest verification after editing '{base}' "
                    f"failed (Exit Code {code_str}). Diagnose and fix the root cause in production "
                    "code (never weaken test assertions) until Exit Code 0, or explicitly report "
                    "a 2-Strike blocker."
                )

            print(json.dumps({"decision": "continue", "reason": msg}))
            return

    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
