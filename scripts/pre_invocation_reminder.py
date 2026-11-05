#!/usr/bin/env python3
"""PreInvocation hook: state-aware, CHECKPOINT-aware 4-Beat CoT & State Ledger injector."""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from argon_core import (  # noqa: E402
    PLUGIN_ROOT,
    load_json_file,
    read_stdin_json,
    resolve_session_state,
    resolve_state_ledger_path,
    save_json_file,
)


def main():
    data = read_stdin_json()
    if not data:
        print(json.dumps({"injectSteps": []}))
        return

    state = resolve_session_state(data)
    if not state["active"]:
        print(json.dumps({"injectSteps": []}))
        return

    conv_id = data.get("conversationId", "")
    artifact_dir = data.get("artifactDirectoryPath", "")
    ledger_path = resolve_state_ledger_path(artifact_dir, conv_id)
    ledger = load_json_file(ledger_path)

    # Deduplicate per monotonic user turn so multi-step tool loops do not spam repeated injections
    current_turn = max(1, state["user_turn_count"])
    if ledger.get("lastInjectedUserTurn") == current_turn:
        print(json.dumps({"injectSteps": []}))
        return

    ledger["lastInjectedUserTurn"] = current_turn
    ledger["activeRole"] = state["role"]
    ledger["activeLevel"] = state["level"]
    save_json_file(ledger_path, ledger)

    role_label = state["role"].upper() if state["role"] != "auto" else "AUTO"
    level_label = state["level"]
    ts_label = " | token-saver: ON" if state["token_saver"] else ""

    if state["role"] != "auto":
        skill_path = os.path.join(
            PLUGIN_ROOT, "skills", f"gemini-mode-argon-{state['role']}", "SKILL.md"
        )
    else:
        skill_path = os.path.join(PLUGIN_ROOT, "skills", "gemini-mode-argon-<role>", "SKILL.md")

    messages = [
        f"⚡ [Argon v2.7 Scaffolding | role={role_label} | level={level_label}{ts_label}]: "
        "Prefix Line 1 with Mandatory Status Badge. Execute 4 Beats on medium/high: "
        "(1) Parallel Recon Batch (no 1-by-1 reads; bind role skill at "
        f"'{skill_path}'), "
        "(2) Latent Deliberation ([FALSIFICATION] -> [INVARIANT AUDIT] -> [PARALLEL TOOL BATCH]), "
        "(3) Complete Affirmative Artifact (zero placeholders; 1-line Pre-Flight Delta on Turn 2+ same scope), "
        "(4) Deterministic non-interactive verification (Exit Code 0)."
    ]

    # Photographic State Ledger across turns
    files = ledger.get("modifiedFiles", [])
    symbols = ledger.get("exportedSymbols", [])
    invariants = ledger.get("pinnedInvariants", [])

    ledger_parts = []
    if files:
        ledger_parts.append(f"Files: [{', '.join(files[:5])}]")
    if symbols:
        ledger_parts.append(f"Symbols: [{', '.join(symbols[:6])}]")
    if invariants:
        ledger_parts.append(f"Invariants: [{', '.join(invariants[:3])}]")

    if ledger_parts:
        messages.append(f"🧠 [Argon Active State Ledger]: {' | '.join(ledger_parts)}")

    # CHECKPOINT-aware Context Health Monitor (resets cleanly after /compact)
    turns_since_cp = state["turns_since_checkpoint"]
    if turns_since_cp >= 12 and (turns_since_cp - 12) % 5 == 0:
        messages.append(
            f"💡 [Argon Context Health]: Reached {turns_since_cp} user turns since last compaction. "
            "Once the current subtask is verified, suggest /compact to maintain peak attention sharpness."
        )

    out = {
        "injectSteps": [{"ephemeralMessage": "\n".join(messages)}],
        "terminationBehavior": "",
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
