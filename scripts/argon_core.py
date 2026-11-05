#!/usr/bin/env python3
"""Shared state-aware utilities for Gemini Mode Argon v2.7 lifecycle hooks."""

import json
import os
import re
import sys
import tempfile

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

READ_TOOL_NAMES = {"read_file", "view_file"}
EDIT_TOOL_NAMES = {"edit_file", "replace_file_content", "multi_replace_file_content"}
WRITE_TOOL_NAMES = {"write_file", "write_to_file"}
MUTATION_TOOL_NAMES = EDIT_TOOL_NAMES | WRITE_TOOL_NAMES

VALID_ROLES = {
    "auto",
    "engineer",
    "reviewer",
    "architect",
    "tester",
    "dba",
    "devops",
    "researcher",
    "general",
    "ui-designer",
    "vector-designer",
    "3d-designer",
    "motion-designer",
    "trader",
}

VALID_LEVELS = {"auto", "low", "medium", "high"}

SLASH_CMD_RE = re.compile(
    r"^\s*/gemini-mode-argon(?:-([a-z0-9-]+))?(?:\s+(.*))?$",
    re.IGNORECASE,
)

STANDALONE_TOKEN_SAVER_RE = re.compile(
    r"^\s*/token-saver(?:-(full|lite|ultra))?(?:\s+(.*))?$",
    re.IGNORECASE,
)

USER_REQUEST_RE = re.compile(
    r"<USER_REQUEST>(.*?)</USER_REQUEST>",
    re.DOTALL | re.IGNORECASE,
)

METADATA_BLOCK_RE = re.compile(
    r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>",
    re.DOTALL | re.IGNORECASE,
)

EXIT_CODE_RE = re.compile(
    r"Command exited with code\s+(-?\d+)",
    re.IGNORECASE,
)

BG_TASK_LAUNCH_RE = re.compile(
    r"running (?:as a |in )background(?: task)?(?: with task id:\s*(\S+))?",
    re.IGNORECASE,
)

BG_TASK_FINISH_RE = re.compile(
    r'Task id\s+"?([^"\s]+)"?\s+finished with result:',
    re.IGNORECASE,
)

TOKEN_SAVER_ARGS = {"on", "off", "true", "false", "1", "0", "full", "lite", "ultra", "auto"}


def read_stdin_json():
    """Read and parse JSON payload from stdin, returning None on empty/invalid input."""
    try:
        raw = sys.stdin.read()
        if not raw or not raw.strip():
            return None
        return json.loads(raw)
    except Exception:
        return None


def unwrap_arg(val):
    """Unwrap JSON-encoded string values found in compact transcript.jsonl args."""
    if isinstance(val, str):
        stripped = val.strip()
        if len(stripped) >= 2 and stripped[0] == '"' and stripped[-1] == '"':
            try:
                return json.loads(stripped)
            except Exception:
                return stripped[1:-1]
        if stripped in ("true", "false", "null"):
            try:
                return json.loads(stripped)
            except Exception:
                pass
    return val


def coerce_bool(val, default=False):
    """Deterministically convert bools, numbers, and quoted/unquoted strings to bool."""
    unwrapped = unwrap_arg(val)
    while isinstance(unwrapped, str) and len(unwrapped) >= 2 and unwrapped[0] == '"' and unwrapped[-1] == '"':
        unwrapped = unwrap_arg(unwrapped)
    if isinstance(unwrapped, bool):
        return unwrapped
    if isinstance(unwrapped, (int, float)):
        return unwrapped != 0
    if isinstance(unwrapped, str):
        normalized = unwrapped.strip().lower()
        if normalized in ("true", "1", "yes", "on"):
            return True
        if normalized in ("false", "0", "no", "off", "null", ""):
            return False
    return bool(default)


def canonical_path(path):
    """Resolve symlinks (~, /tmp -> /private/tmp) and return canonical absolute path."""
    unwrapped = unwrap_arg(path)
    if not isinstance(unwrapped, str) or not unwrapped.strip():
        return ""
    expanded = os.path.expanduser(unwrapped.strip())
    return os.path.realpath(os.path.abspath(expanded))


def extract_tool_target_path(tc_name, tc_args):
    """Extract target file path across Antigravity 2.0 App and Antigravity IDE / Cascade tools."""
    _ = tc_name
    if not isinstance(tc_args, dict):
        return ""
    for key in ("Path", "TargetFile", "AbsolutePath"):
        raw = unwrap_arg(tc_args.get(key, ""))
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return ""


def is_pure_new_file_creation(tc_name, tc_args):
    """Return True when a write tool creates a brand-new file without overwriting or appending."""
    if not isinstance(tc_args, dict):
        return False
    if tc_name == "write_file":
        is_ow = coerce_bool(tc_args.get("Overwrite", False), default=False)
        is_ap = coerce_bool(tc_args.get("Append", False), default=False)
        return (not is_ow) and (not is_ap)
    if tc_name == "write_to_file":
        is_ow = coerce_bool(tc_args.get("Overwrite", False), default=False)
        return not is_ow
    return False


def is_artifact_or_scratch_path(path, artifact_dir="", conv_id=""):
    """Return True if path resides inside the conversation's brain/artifact/scratch directory."""
    canon = canonical_path(path)
    if not canon:
        return False

    if artifact_dir:
        canon_art = canonical_path(artifact_dir)
        if canon_art and (canon == canon_art or canon.startswith(canon_art + os.sep)):
            return True

    if conv_id:
        needle = f"{os.sep}brain{os.sep}{conv_id}{os.sep}"
        if needle in (canon + os.sep):
            return True

    return False


def strip_user_request_wrappers(text):
    """Extract raw user text from Antigravity <USER_REQUEST> tags if present."""
    if not isinstance(text, str) or not text:
        return ""
    match = USER_REQUEST_RE.search(text)
    if match:
        return match.group(1).strip()
    cleaned = METADATA_BLOCK_RE.sub("", text)
    return cleaned.strip()


def apply_slash_commands(clean_text, state):
    """Update Argon state dict from slash commands in clean user text (sequential token scanner)."""
    if not clean_text:
        return

    in_fence = False
    seen_nonempty_line = False
    for raw_line in clean_text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            seen_nonempty_line = True
            continue
        if in_fence or stripped.startswith(">"):
            seen_nonempty_line = True
            continue

        is_first_line = not seen_nonempty_line
        seen_nonempty_line = True

        ts_match = STANDALONE_TOKEN_SAVER_RE.match(raw_line)
        if ts_match:
            sub_mode = (ts_match.group(1) or "").lower()
            rest_ts = (ts_match.group(2) or "").strip()
            ts_tokens = [t.rstrip(",.;:!?").lstrip("/") for t in rest_ts.split() if t.rstrip(",.;:!?")]
            if sub_mode in ("full", "lite", "ultra"):
                state["token_saver"] = True
            elif not ts_tokens or ts_tokens[0].lower() in ("on", "auto", "true", "1", "full", "lite", "ultra"):
                state["token_saver"] = True
            elif ts_tokens[0].lower() in ("off", "false", "0"):
                state["token_saver"] = False
            continue

        match = SLASH_CMD_RE.match(raw_line)
        if not match:
            continue

        role_suffix = (match.group(1) or "").lower()
        rest = (match.group(2) or "").strip()
        tokens = [t.rstrip(",.;:!?") for t in rest.split() if t.rstrip(",.;:!?")]

        # Handle role-specific shorthand like /gemini-mode-argon-engineer [on|off|level]
        if role_suffix:
            if role_suffix in (VALID_ROLES - {"auto"}):
                if tokens and tokens[0].lower().lstrip("/") == "off":
                    state["active"] = False
                    state["role"] = "auto"
                    state["level"] = "auto"
                    state["token_saver"] = False
                    continue
                state["active"] = True
                state["role"] = role_suffix
                # Continue scanning any trailing parameters like level or token-saver
                tokens = tokens[1:] if (tokens and tokens[0].lower().lstrip("/") == "on") else tokens
            else:
                continue

        # Sequential token scanner across tokens
        i = 0
        consumed_any = False
        while i < len(tokens):
            tok = tokens[i].lower().lstrip("/")
            if tok == "off":
                state["active"] = False
                state["role"] = "auto"
                state["level"] = "auto"
                state["token_saver"] = False
                consumed_any = True
                i += 1
            elif tok in ("on",):
                state["active"] = True
                state["role"] = "auto"
                state["level"] = "auto"
                consumed_any = True
                i += 1
            elif tok == "role":
                state["active"] = True
                consumed_any = True
                if i + 1 < len(tokens) and tokens[i + 1].lower().lstrip("/") in VALID_ROLES:
                    state["role"] = tokens[i + 1].lower().lstrip("/")
                    i += 2
                else:
                    i += 1
            elif tok == "level":
                state["active"] = True
                consumed_any = True
                if i + 1 < len(tokens) and tokens[i + 1].lower().lstrip("/") in VALID_LEVELS:
                    state["level"] = tokens[i + 1].lower().lstrip("/")
                    i += 2
                else:
                    i += 1
            elif tok in VALID_LEVELS and tok != "auto":
                # Shorthand level without 'level' keyword, e.g. /gemini-mode-argon-dba high
                state["active"] = True
                state["level"] = tok
                consumed_any = True
                i += 1
            elif tok in ("token-saver", "tokensaver"):
                state["active"] = True
                consumed_any = True
                if i + 1 < len(tokens) and tokens[i + 1].lower().lstrip("/") in TOKEN_SAVER_ARGS:
                    mode_arg = tokens[i + 1].lower().lstrip("/")
                    state["token_saver"] = mode_arg in ("on", "true", "1", "full", "lite", "ultra", "auto")
                    i += 2
                else:
                    state["token_saver"] = True
                    i += 1
            else:
                break

        if not consumed_any and not role_suffix:
            if not tokens:
                state["active"] = True
                state["role"] = "auto"
                state["level"] = "auto"
            elif is_first_line:
                state["active"] = True


def resolve_session_state(data):
    """Inspect transcript.jsonl & lastUserInput for ON/OFF state, role, level, and CHECKPOINT turns."""
    force_env = os.environ.get("ARGON_FORCE_ACTIVE", "").strip().lower()
    initial_active = force_env in ("1", "true", "on")

    state = {
        "active": initial_active,
        "role": "auto",
        "level": "auto",
        "token_saver": False,
        "user_turn_count": 0,
        "turns_since_checkpoint": 0,
    }

    if not isinstance(data, dict):
        return state

    transcript_path = data.get("transcriptPath", "")
    last_transcript_clean = None

    if transcript_path and os.path.exists(transcript_path):
        try:
            with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        step = json.loads(line)
                    except Exception:
                        continue
                    step_type = str(step.get("type", "")).upper()
                    if step_type == "CHECKPOINT":
                        # Context compaction occurred: keep active/role/level, reset post-compact turn counter
                        state["turns_since_checkpoint"] = 0
                    elif step_type == "USER_INPUT":
                        raw_content = unwrap_arg(step.get("content", ""))
                        clean = strip_user_request_wrappers(str(raw_content))
                        state["user_turn_count"] += 1
                        state["turns_since_checkpoint"] += 1
                        last_transcript_clean = clean
                        apply_slash_commands(clean, state)
        except Exception:
            pass

    last_user_input = data.get("lastUserInput", "")
    if isinstance(last_user_input, str) and last_user_input.strip():
        clean_last = strip_user_request_wrappers(last_user_input)
        if clean_last and clean_last != last_transcript_clean:
            state["user_turn_count"] += 1
            state["turns_since_checkpoint"] += 1
            apply_slash_commands(clean_last, state)

    return state


def iter_transcript_tool_events(transcript_path):
    """Yield (step_idx, call_idx, tc_name, tc_args, failed, exit_code) with 1-to-1 batch mapping."""
    if not transcript_path or not os.path.exists(transcript_path):
        return

    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            steps = []
            for line in f:
                if not line.strip():
                    continue
                try:
                    steps.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return

    total = len(steps)
    bg_tasks = {}
    for idx, step in enumerate(steps):
        st_type = str(step.get("type", "")).upper()
        if st_type in ("SYSTEM_MESSAGE", "GENERIC"):
            content = str(unwrap_arg(step.get("content", "")))
            m_fin = BG_TASK_FINISH_RE.search(content)
            if m_fin:
                raw_tid = m_fin.group(1).strip() if m_fin.group(1) else ""
                tc_args = bg_tasks.get(raw_tid) if raw_tid else bg_tasks.get("__unkeyed__")
                if tc_args:
                    m_exit = EXIT_CODE_RE.search(content)
                    fin_code = None
                    if m_exit:
                        try:
                            fin_code = int(m_exit.group(1))
                        except ValueError:
                            fin_code = None
                    fin_failed = (fin_code is not None and fin_code != 0) or str(step.get("status", "")).upper() == "ERROR"
                    yield (idx, 0, "run_command", tc_args, fin_failed, fin_code)
                    continue

        tcs = step.get("tool_calls") or []
        if not tcs:
            continue
        if str(step.get("status", "")).upper() == "ERROR":
            continue

        # Collect consecutive GENERIC / TOOL_RESPONSE steps immediately following this planner step
        result_steps = []
        look = idx + 1
        while look < total:
            st_type = str(steps[look].get("type", "")).upper()
            if st_type in ("GENERIC", "TOOL_RESPONSE"):
                result_steps.append(steps[look])
                look += 1
            else:
                break

        for j, tc in enumerate(tcs):
            tc_name = tc.get("name", "")
            tc_args = tc.get("args", {}) or {}
            failed = False
            exit_code = None

            if j < len(result_steps):
                res = result_steps[j]
                res_status = str(res.get("status", "")).upper()
                res_content = str(unwrap_arg(res.get("content", "")))
                res_err = str(unwrap_arg(res.get("error", "")))
                if (
                    res_status == "ERROR"
                    or "denied by pre-tool hook" in res_content.lower()
                    or bool(res_err)
                ):
                    failed = True
                m_exit = EXIT_CODE_RE.search(res_content)
                if m_exit:
                    try:
                        exit_code = int(m_exit.group(1))
                    except ValueError:
                        exit_code = None
                elif res_status == "RUNNING" or BG_TASK_LAUNCH_RE.search(res_content):
                    exit_code = "RUNNING"
                    m_tid = BG_TASK_LAUNCH_RE.search(res_content)
                    if m_tid and m_tid.group(1):
                        bg_tasks[m_tid.group(1).strip()] = tc_args
                    else:
                        bg_tasks["__unkeyed__"] = tc_args

            yield (idx, j, tc_name, tc_args, failed, exit_code)


def resolve_state_ledger_path(artifact_dir="", conv_id=""):
    """Return canonical path to scratch/argon_state.json for the active conversation."""
    if artifact_dir:
        return os.path.join(canonical_path(artifact_dir), "scratch", "argon_state.json")
    tmp_root = tempfile.gettempdir()
    if conv_id:
        brain_candidate = os.path.expanduser(f"~/.gemini/antigravity/brain/{conv_id}")
        if os.path.isdir(brain_candidate):
            return os.path.join(os.path.realpath(brain_candidate), "scratch", "argon_state.json")
        safe_id = re.sub(r"[^A-Za-z0-9_.-]", "_", conv_id)
        return os.path.join(tmp_root, f"argon_state_{safe_id}.json")
    return os.path.join(tmp_root, "argon_state_default.json")


def load_json_file(path, default=None):
    """Safely load a JSON file or return a copy of default."""
    if default is None:
        default = {}
    if not path or not os.path.exists(path):
        return dict(default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        return loaded if isinstance(loaded, dict) else dict(default)
    except Exception:
        return dict(default)


def save_json_file(path, payload):
    """Atomically persist a JSON dictionary, creating parent directories if needed."""
    if not path:
        return
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        tmp_path = f"{path}.tmp.{os.getpid()}"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        pass
