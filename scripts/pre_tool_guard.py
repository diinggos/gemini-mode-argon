#!/usr/bin/env python3
"""PreToolUse hook: batch-aware read-before-write gate, destructive gate, and pipefail test cap."""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from argon_core import (  # noqa: E402
    EDIT_TOOL_NAMES,
    MUTATION_TOOL_NAMES,
    READ_TOOL_NAMES,
    WRITE_TOOL_NAMES,
    canonical_path,
    extract_tool_target_path,
    is_artifact_or_scratch_path,
    is_pure_new_file_creation,
    iter_transcript_tool_events,
    load_json_file,
    read_stdin_json,
    resolve_session_state,
    resolve_state_ledger_path,
    unwrap_arg,
)

DESTRUCTIVE_PATTERNS = [
    r"\bgit\b(?:\s+(?:-C\s+\S+|-c\s+\S+|--[a-z0-9-]+(?:=\S+)?))*\s+push\b",
    r"\bgit\b(?:\s+(?:-C\s+\S+|-c\s+\S+|--[a-z0-9-]+(?:=\S+)?))*\s+reset\s+--hard\b",
    r"\bgit\b(?:\s+(?:-C\s+\S+|-c\s+\S+|--[a-z0-9-]+(?:=\S+)?))*\s+clean\s+(?:-[a-zA-Z]*f|--force)",
    r"\brm\s+(?:-[a-zA-Z]*r[a-zA-Z]*|--recursive)(?:\s+-[a-zA-Z-]+)*\s+\S+",
    r"\bprisma\s+migrate\s+reset\b",
    r"\bsupabase\s+db\s+reset\b",
    r"\brails\s+db:(?:drop|reset)\b",
    r"\bphp\s+artisan\s+migrate:(?:fresh|reset)\b",
    r"\bdropdb\b",
    r"\bgh\s+repo\s+create\b",
    r"\bnpm\s+publish\b",
]

ENV_PREFIX_RE = re.compile(
    r"^(?:[A-Za-z_][A-Za-z0-9_]*=(?:\"[^\"]*\"|'[^']*'|[^\s]+)\s+)+"
)

TEST_RUNNER_RE = re.compile(
    r"^(?:[\w./~-]+/)?(?:"
    r"(?:(?:uv|poetry|pipenv)\s+run\s+)?pytest"
    r"|(?:(?:uv|poetry|pipenv)\s+run\s+)?python3?(?:\.\d+)?\s+-m\s+(?:pytest|unittest)"
    r"|(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?test"
    r"|cargo\s+test"
    r"|go\s+test"
    r"|(?:(?:npx|bunx|pnpx)\s+)?(?:vitest|jest|mocha|playwright)"
    r"|(?:mvn|gradlew?)\s+test"
    r"|(?:flutter|dart)\s+test"
    r"|dotnet\s+test"
    r"|(?:bundle\s+exec\s+)?(?:rspec|rake\s+test)"
    r"|phpunit|pest"
    r"|php\s+artisan\s+test"
    r"|swift\s+test"
    r"|ctest"
    r")\b"
)

COMPOUND_SHELL_TOKENS = ("|", ">", "<", "&&", "||", ";", "\n", "`", "$(")

REVIEWER_SHELL_MUTATION_RE = re.compile(
    r"(?:"
    r"(?:>|>>)\s*(?!(?:/dev/null|/tmp/|\$TMPDIR)\b)"
    r"|\b(?:sed|perl)\s+-[a-zA-Z]*i\b"
    r"|\b(?:touch|mkdir|rmdir|cp|mv|rm|tee|truncate|patch)\b"
    r"|\b(?:npm|pnpm|yarn|bun)\s+(?:install|add|remove|update)\b"
    r"|\b(?:pip|pip3)\s+install\b"
    r"|\b(?:poetry|uv|cargo)\s+add\b"
    r"|\bgit\s+(?:commit|checkout|restore|merge|rebase|cherry-pick|revert|apply)\b"
    r"|\b(?:python3?|node|ruby|perl|bash|sh|zsh)\s+-[ce]\b"
    r"|\bcurl\s+(?:.*?\s+)?(?:-[a-zA-Z]*[oO]|--output)\s+(?!(?:/dev/null|/tmp/|\$TMPDIR)\b)"
    r"|\bwget\s+(?!(?:-O\s*(?:/dev/null|/tmp/|\$TMPDIR))\b)"
    r")",
    re.IGNORECASE,
)


def is_pure_single_test_command(cmd):
    """Return True if cmd is a single-statement test runner invocation safe for pipefail wrapping."""
    if not cmd or cmd.startswith("(") or cmd.endswith("&"):
        return False
    if any(tok in cmd for tok in COMPOUND_SHELL_TOKENS):
        return False
    core_cmd = ENV_PREFIX_RE.sub("", cmd).strip()
    return bool(TEST_RUNNER_RE.match(core_cmd))


def has_prior_valid_touch(transcript_path, canon_target, ledger_path):
    """Check if canon_target was previously read in an earlier completed step or newly created."""
    if not canon_target:
        return False

    # 1. Check PostToolUse verifiedTouchedPaths ledger (populated only on non-error writes/edits)
    ledger = load_json_file(ledger_path)
    if canon_target in ledger.get("verifiedTouchedPaths", []):
        return True

    # 2. Inspect conversation transcript with exact 1-to-1 parallel tool batch mapping
    events = list(iter_transcript_tool_events(transcript_path))
    edit_step_indices = {
        step_idx
        for step_idx, _j, tc_name, tc_args, _failed, _code in events
        if tc_name in EDIT_TOOL_NAMES
        and canonical_path(extract_tool_target_path(tc_name, tc_args)) == canon_target
    }

    for step_idx, _j, tc_name, tc_args, failed, _code in events:
        if failed:
            continue
        target = canonical_path(extract_tool_target_path(tc_name, tc_args))
        if target != canon_target:
            continue
        if tc_name in READ_TOOL_NAMES:
            # Read must be completed in an earlier step, not batched with an edit for the same file
            if step_idx not in edit_step_indices:
                return True
        elif tc_name in WRITE_TOOL_NAMES and is_pure_new_file_creation(tc_name, tc_args):
            return True

    return False


def main():
    data = read_stdin_json()
    if not data:
        print(json.dumps({"decision": "allow"}))
        return

    state = resolve_session_state(data)
    if not state["active"]:
        print(json.dumps({"decision": "allow"}))
        return

    tool_call = data.get("toolCall", {})
    name = tool_call.get("name", "")
    args = tool_call.get("args", {}) or {}
    transcript_path = data.get("transcriptPath", "")
    artifact_dir = data.get("artifactDirectoryPath", "")
    conv_id = data.get("conversationId", "")
    ledger_path = resolve_state_ledger_path(artifact_dir, conv_id)

    # 1. Gate for run_command: destructive command safety & pipefail-safe test output limiter
    if name == "run_command":
        cmd = str(unwrap_arg(args.get("CommandLine", ""))).strip()
        for pattern in DESTRUCTIVE_PATTERNS:
            if re.search(pattern, cmd):
                out = {
                    "decision": "force_ask",
                    "reason": (
                        f"Argon Safety Gate: Command contains sensitive or destructive action "
                        f"('{cmd}'). Explicit user confirmation required."
                    ),
                }
                print(json.dumps(out))
                return

        if state["role"] == "reviewer" and REVIEWER_SHELL_MUTATION_RE.search(cmd):
            out = {
                "decision": "deny",
                "reason": (
                    "Argon Reviewer Gate: Role 'reviewer' is strictly read-only for workspace files. "
                    f"Shell file mutations and inline scripts ('{cmd}') are blocked. "
                    "Deliver patch diffs in your response/artifact or switch role to 'engineer'."
                ),
            }
            print(json.dumps(out))
            return

        if is_pure_single_test_command(cmd):
            sanitized_cmd = (
                f"( export PYTHONUNBUFFERED=1; "
                f"if (set -o pipefail 2>/dev/null) && set -o pipefail 2>/dev/null; then "
                f"{cmd} 2>&1 | tail -n 80; "
                f"else "
                f"_fifo=$(mktemp -u 2>/dev/null || echo /tmp/argon_fifo_$$.tmp); "
                f"mkfifo \"$_fifo\" 2>/dev/null || true; "
                f"if [ -p \"$_fifo\" ]; then "
                f"({cmd}) >\"$_fifo\" 2>&1 & _pid=$!; tail -n 80 <\"$_fifo\"; wait $_pid; _rc=$?; rm -f \"$_fifo\"; exit $_rc; "
                f"else "
                f"_tmp=$(mktemp 2>/dev/null || echo /tmp/argon_out_$$.tmp); "
                f"if touch \"$_tmp\" 2>/dev/null; then "
                f"({cmd}) >\"$_tmp\" 2>&1; _rc=$?; tail -n 80 \"$_tmp\"; rm -f \"$_tmp\"; exit $_rc; "
                f"else {cmd}; fi; "
                f"fi; "
                f"fi )"
            )
            out = {
                "decision": "allow",
                "overwrite": {"CommandLine": sanitized_cmd},
            }
            print(json.dumps(out))
            return

    # 2. Enforce strictly read-only invariant when locked in 'reviewer' role (outside artifacts)
    if name in MUTATION_TOOL_NAMES and state["role"] == "reviewer":
        raw_path = extract_tool_target_path(name, args)
        if raw_path and not is_artifact_or_scratch_path(raw_path, artifact_dir, conv_id):
            out = {
                "decision": "deny",
                "reason": (
                    "Argon Reviewer Gate: Role 'reviewer' is strictly read-only for workspace files. "
                    "Deliver patch diffs in your response/artifact or switch role to 'engineer'."
                ),
            }
            print(json.dumps(out))
            return

    # 3. Gate for edit tools: enforce read-before-write (skipping artifacts & newly created files)
    if name in EDIT_TOOL_NAMES:
        raw_path = extract_tool_target_path(name, args)
        if raw_path and not is_artifact_or_scratch_path(raw_path, artifact_dir, conv_id):
            canon = canonical_path(raw_path)
            if canon and os.path.exists(canon):
                if not has_prior_valid_touch(transcript_path, canon, ledger_path):
                    out = {
                        "decision": "deny",
                        "reason": (
                            f"Argon Physical Gate: File '{raw_path}' has not been inspected with "
                            "'read_file' / 'view_file' in this session. Inspect it first before editing!"
                        ),
                    }
                    print(json.dumps(out))
                    return

    # 4. Gate for write tools when overwriting/appending existing non-artifact file
    if name in WRITE_TOOL_NAMES:
        raw_path = extract_tool_target_path(name, args)
        if (
            raw_path
            and (not is_pure_new_file_creation(name, args))
            and not is_artifact_or_scratch_path(raw_path, artifact_dir, conv_id)
        ):
            canon = canonical_path(raw_path)
            if canon and os.path.exists(canon):
                if not has_prior_valid_touch(transcript_path, canon, ledger_path):
                    out = {
                        "decision": "deny",
                        "reason": (
                            f"Argon Physical Gate: Existing file '{raw_path}' is being "
                            "overwritten/appended without prior inspection. Call read_file/view_file first!"
                        ),
                    }
                    print(json.dumps(out))
                    return

    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
