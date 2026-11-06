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
    NO_RUN_FLAGS_RE,
    WATCH_FLAGS_RE,
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
    ".vue",
    ".svelte",
}

ENV_PREFIX_RE = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*=(?:\"[^\"]*\"|'[^']*'|[^\s]+)\s+)+")

VERIFICATION_RUNNER_PATTERN = (
    r"(?:"
    r"(?:pytest|vitest|jest|mocha|ruff|flake8|mypy|pyright|eslint|biome|tsc|phpunit|pest|rspec|ctest|playwright)\b"
    r"|(?:uv|poetry|pipenv)\s+run\s+(?:pytest|python3?(?:\.\d+)?\s+-m\s+(?:pytest|unittest)|\S*(?:test|audit|verify)\S*\.py)\b"
    r"|cargo\s+(?:test|check|build|clippy)\b"
    r"|go\s+(?:test|vet|build)\b"
    r"|(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?(?:test|check|lint|typecheck|build)\b"
    r"|(?:npx|bunx|pnpx)\s+(?:vitest|jest|mocha|playwright|tsc)\b"
    r"|(?:dart|flutter)\s+(?:test|analyze)\b"
    r"|(?:mvn|gradlew?)\s+(?:test|check|compile|verify)\b"
    r"|dotnet\s+(?:test|build)\b"
    r"|\bbundle\s+exec\s+(?:rspec|rake\s+test)\b"
    r"|\brake\s+test\b"
    r"|\bphp\s+artisan\s+test\b"
    r"|\bswift\s+(?:test|build)\b"
    r"|\bcmake\s+--build\b"
    r"|\bmake\s+(?:test|check|build)\b"
    r"|python3?(?:\.\d+)?\s+(?:-m\s+(?:pytest|unittest|py_compile|doctest)|\S*(?:test|audit|verify)\S*\.py)\b"
    r"|(?:bash|sh|zsh)\s+-n\b"
    r"|\bEXPLAIN\b"
    r")"
)

VERIFICATION_EXECUTABLE_RE = re.compile(
    r"^(?:[\w./~-]+/)?" + VERIFICATION_RUNNER_PATTERN,
    re.IGNORECASE,
)
VERIFICATION_RUNNER_UNANCHORED_RE = re.compile(
    r"\b" + VERIFICATION_RUNNER_PATTERN,
    re.IGNORECASE,
)

COMPOUND_MASKING_RE = re.compile(r"(?:\|\||;|(?:\|(?!\|)))")

SHELL_REDIRECTION_RE = re.compile(
    r"(?:[0-9]?>>?|&>>?)\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s;&|]+))"
)
SHELL_TEE_RE = re.compile(
    r"\btee\s+(?:-[a-zA-Z]+\s+)*(?:\"([^\"]+)\"|'([^']+)'|([^\s;&|]+))"
)
SHELL_SED_INPLACE_RE = re.compile(r"\b(?:sed|perl)\s+-[a-zA-Z]*i[^\s]*\b")


def extract_shell_source_edits(cmd_line, artifact_dir="", conv_id=""):
    """Extract source file targets created or modified via run_command."""
    if not isinstance(cmd_line, str) or not cmd_line.strip():
        return []

    targets = []

    # 1. Shell redirection: >, >>, 1>, 2>, &>, &>>
    for m in SHELL_REDIRECTION_RE.finditer(cmd_line):
        raw = m.group(1) or m.group(2) or m.group(3)
        if raw:
            p = raw.strip()
            if not p.startswith("&"):
                ext = os.path.splitext(p)[1].lower()
                if ext in CODE_EXTENSIONS:
                    canon = canonical_path(p)
                    if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                        targets.append(canon)

    # 2. tee [-a] file
    for m in SHELL_TEE_RE.finditer(cmd_line):
        raw = m.group(1) or m.group(2) or m.group(3)
        if raw:
            p = raw.strip()
            ext = os.path.splitext(p)[1].lower()
            if ext in CODE_EXTENSIONS:
                canon = canonical_path(p)
                if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                    targets.append(canon)

    # 3. sed -i / perl -i in-place modifications
    if SHELL_SED_INPLACE_RE.search(cmd_line):
        for token in re.findall(r"[\"']?([^\s\"'`;|&]+)[\"']?", cmd_line):
            ext = os.path.splitext(token)[1].lower()
            if ext in CODE_EXTENSIONS:
                canon = canonical_path(token)
                if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                    targets.append(canon)

    # 4. cp / mv / touch
    if re.search(r"\b(?:cp|mv|touch)\b", cmd_line):
        for token in re.findall(r"[\"']?([^\s\"'`;|&]+)[\"']?", cmd_line):
            ext = os.path.splitext(token)[1].lower()
            if ext in CODE_EXTENSIONS:
                canon = canonical_path(token)
                if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                    targets.append(canon)

    # 5. curl -o file / curl --output file
    for m in re.finditer(r"\bcurl\s+(?:.*?\s+)?(?:-[a-zA-Z]*o|--output)\s+([^\s;&|]+)", cmd_line, re.IGNORECASE):
        p = m.group(1).strip()
        ext = os.path.splitext(p)[1].lower()
        if ext in CODE_EXTENSIONS:
            canon = canonical_path(p)
            if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                targets.append(canon)

    # 6. wget -O file
    for m in re.finditer(r"\bwget\s+(?:.*?\s+)?-O\s*([^\s;&|]+)", cmd_line, re.IGNORECASE):
        p = m.group(1).strip()
        ext = os.path.splitext(p)[1].lower()
        if ext in CODE_EXTENSIONS:
            canon = canonical_path(p)
            if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                targets.append(canon)

    # 7. python3 -c / node -e file writes
    for m in re.finditer(r"""(?:open|writeFileSync|writeFile)\(\s*['"]([^'"]+)['"]\s*,\s*['"][wa+]""", cmd_line):
        p = m.group(1).strip()
        ext = os.path.splitext(p)[1].lower()
        if ext in CODE_EXTENSIONS:
            canon = canonical_path(p)
            if not is_artifact_or_scratch_path(canon, artifact_dir, conv_id):
                targets.append(canon)

    seen = set()
    deduped = []
    for t in targets:
        if t and t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


def is_verification_command(cmd_line):
    """Return True if cmd_line invokes a verification runner as executable, avoiding argument false positives and exit-code masking."""
    if not isinstance(cmd_line, str) or not cmd_line.strip():
        return False

    s = cmd_line.strip()

    # Reject no-run / help / version / dry-run options that do not execute test suites
    if NO_RUN_FLAGS_RE.search(s):
        return False

    # Reject watch mode runners which do not perform non-interactive deterministic verification
    if WATCH_FLAGS_RE.search(s):
        return False

    # Check if this is the argon pipefail/tempfile sanitized test wrapper
    if s.startswith("(") and s.endswith(")") and "export PYTHONUNBUFFERED=1" in s:
        # Extract inner command between 'then ' and ' 2>&1 | tail'
        m_inner = re.search(r"\bthen\s+(.*?)\s+2>&1\s*\|\s*tail", s)
        if m_inner:
            inner_cmd = m_inner.group(1).strip()
            return is_verification_command(inner_cmd)
        core = ENV_PREFIX_RE.sub("", s).strip()
        if NO_RUN_FLAGS_RE.search(core) or WATCH_FLAGS_RE.search(core):
            return False
        return bool(VERIFICATION_RUNNER_UNANCHORED_RE.search(core))

    # Reject compound commands containing chaining (||, ;) or un-sanitized pipelines (|)
    # which can swallow or mask non-zero test failure exit codes
    if COMPOUND_MASKING_RE.search(s):
        return False

    s = s.lstrip("(").rstrip(")").strip()
    core = ENV_PREFIX_RE.sub("", s).strip()
    return bool(VERIFICATION_EXECUTABLE_RE.match(core))


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
            if is_verification_command(cmd):
                if exit_code == "RUNNING":
                    continue
                passed = (not failed) and (exit_code is None or exit_code == 0)
                verifications.append(((step_idx, call_idx), passed, exit_code))
            elif not failed and (exit_code is None or exit_code == 0):
                targets = extract_shell_source_edits(cmd, artifact_dir, conv_id)
                for t in targets:
                    edits.append(((step_idx, call_idx), t))

    if not edits:
        if not verifications:
            return None, None, (-1, -1), None
        latest_v_step = verifications[-1][0][0]
        latest_runs = [v for v in verifications if v[0][0] == latest_v_step]
        failures = [v for v in latest_runs if not v[1]]
        if failures:
            _v_pos, _passed, latest_code = failures[-1]
            return "failed_test", None, _v_pos, latest_code
        return None, None, (-1, -1), None

    last_edit_pos, last_canon_file = edits[-1]
    last_edit_step = last_edit_pos[0]

    # Verification must run in a subsequent planner step (step_idx > last_edit_step)
    # because tools within the same batch can execute concurrently.
    post_runs = [v for v in verifications if v[0][0] > last_edit_step]

    if not post_runs:
        # Check if there was a failure in the same batch as the edit
        same_step_failures = [v for v in verifications if v[0][0] == last_edit_step and not v[1]]
        if same_step_failures:
            _v_pos, _passed, latest_code = same_step_failures[-1]
            return "failed_test", last_canon_file, _v_pos, latest_code
        return "unverified", last_canon_file, last_edit_pos, None

    latest_post_step = post_runs[-1][0][0]
    latest_post_runs = [v for v in post_runs if v[0][0] == latest_post_step]
    post_failures = [v for v in latest_post_runs if not v[1]]
    if post_failures:
        _v_pos, _passed, latest_code = post_failures[-1]
        return "failed_test", last_canon_file, _v_pos, latest_code

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
    if issue_kind:
        target_label = canon_file or "workspace"
        tracker = load_json_file(TRACKER_FILE)
        key = f"{conv_id}:{target_label}:{last_edit_pos[0]}_{last_edit_pos[1]}:{issue_kind}"
        if tracker.get(key, 0) < 1:
            tracker[key] = 1
            if len(tracker) > 500:
                oldest_keys = list(tracker.keys())[:-400]
                for k in oldest_keys:
                    tracker.pop(k, None)
            save_json_file(TRACKER_FILE, tracker)

            if issue_kind == "unverified":
                base = os.path.basename(canon_file) if canon_file else "code"
                msg = (
                    f"Argon Deterministic Verification Gate: Code changes in '{base}' have not "
                    "been verified via terminal test/build/lint. Execute a non-interactive check "
                    "(Exit Code 0) before concluding."
                )
            else:
                code_str = exit_code if exit_code is not None else "non-zero"
                if canon_file:
                    base = os.path.basename(canon_file)
                    msg = (
                        f"Argon Reflexion Auto-Healing Gate: Latest verification after editing '{base}' "
                        f"failed (Exit Code {code_str}). Diagnose and fix the root cause in production "
                        "code (never weaken test assertions) until Exit Code 0, or explicitly report "
                        "a 2-Strike blocker."
                    )
                else:
                    msg = (
                        f"Argon Reflexion Auto-Healing Gate: Recent verification test failed (Exit Code {code_str}). "
                        "Diagnose and fix the root cause in production code (never weaken test assertions) "
                        "until Exit Code 0, or explicitly report a 2-Strike blocker."
                    )

            print(json.dumps({"decision": "continue", "reason": msg}))
            return

    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
