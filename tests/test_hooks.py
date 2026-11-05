#!/usr/bin/env python3
"""Comprehensive 25-scenario end-to-end regression suite for Gemini Mode Argon v2.7."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PLUGIN_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import argon_core  # noqa: E402
import post_tool_ledger  # noqa: E402
import stop_guard  # noqa: E402


def run_hook(script_name, payload, env_extra=None):
    """Execute a hook script from PLUGIN_ROOT just like Antigravity hooks.json does."""
    env = os.environ.copy()
    env.pop("ARGON_FORCE_ACTIVE", None)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        [sys.executable, os.path.join("scripts", script_name)],
        cwd=PLUGIN_ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=env,
        timeout=10,
        check=True,
    )
    return json.loads(proc.stdout.strip())


def write_jsonl(path, steps):
    with open(path, "w", encoding="utf-8") as f:
        for step in steps:
            f.write(json.dumps(step) + "\n")


class ArgonV25HooksTestSuite(unittest.TestCase):
    def setUp(self):
        base_tmp = "/tmp" if os.path.isdir("/tmp") else tempfile.gettempdir()
        self.tmpdir = tempfile.mkdtemp(prefix="argon_v25_test_", dir=base_tmp)
        self.conv_id = f"test-{uuid.uuid4()}"
        self.workspace_dir = os.path.join(self.tmpdir, "workspace")
        self.artifact_dir = os.path.join(self.tmpdir, "brain", self.conv_id)
        os.makedirs(self.workspace_dir, exist_ok=True)
        os.makedirs(self.artifact_dir, exist_ok=True)
        self.transcript_path = os.path.join(self.tmpdir, "transcript.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def base_payload(self, last_user_input=""):
        return {
            "conversationId": self.conv_id,
            "workspacePaths": [self.workspace_dir],
            "transcriptPath": self.transcript_path,
            "artifactDirectoryPath": self.artifact_dir,
            "modelName": "gemini-3.8-flash",
            "lastUserInput": last_user_input,
        }

    def test_01_off_by_default_zero_interference(self):
        """Hooks must be 100% no-op when /gemini-mode-argon is OFF (even if mentioned in prose/code)."""
        target = os.path.join(self.workspace_dir, "app.py")
        with open(target, "w", encoding="utf-8") as f:
            f.write("x = 1\n")

        write_jsonl(
            self.transcript_path,
            [
                {
                    "type": "USER_INPUT",
                    "content": "Kenapa plugin /gemini-mode-argon bagus?\n```\n/gemini-mode-argon on\n```",
                },
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": target}}],
                },
            ],
        )

        self.assertEqual(run_hook("pre_invocation_reminder.py", self.base_payload())["injectSteps"], [])

        p_edit = self.base_payload()
        p_edit["toolCall"] = {"name": "edit_file", "args": {"Path": target}}
        self.assertEqual(run_hook("pre_tool_guard.py", p_edit)["decision"], "allow")

        p_cmd = self.base_payload()
        p_cmd["toolCall"] = {"name": "run_command", "args": {"CommandLine": "pytest"}}
        res_cmd = run_hook("pre_tool_guard.py", p_cmd)
        self.assertEqual(res_cmd["decision"], "allow")
        self.assertNotIn("overwrite", res_cmd)

        p_post = self.base_payload()
        p_post["toolCall"] = {"name": "write_file", "args": {"Path": target}}
        self.assertEqual(run_hook("post_tool_ledger.py", p_post), {})
        self.assertFalse(
            os.path.exists(os.path.join(self.artifact_dir, "scratch", "argon_state.json"))
        )

        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"
        self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "allow")

    def test_02_slash_command_activation_overrides_and_deactivation(self):
        """State resolver accurately tracks ON/OFF, role/level/token-saver overrides, and <USER_REQUEST> tags."""
        steps = [
            {"type": "USER_INPUT", "content": "<USER_REQUEST>\n/gemini-mode-argon on\n</USER_REQUEST>"},
            {"type": "USER_INPUT", "content": "/gemini-mode-argon role dba"},
            {"type": "USER_INPUT", "content": "/gemini-mode-argon level high"},
            {"type": "USER_INPUT", "content": "/gemini-mode-argon token-saver on"},
        ]
        write_jsonl(self.transcript_path, steps)

        state = argon_core.resolve_session_state(
            self.base_payload("<USER_REQUEST>\n/gemini-mode-argon token-saver on\n</USER_REQUEST>")
        )
        self.assertTrue(state["active"])
        self.assertEqual(state["role"], "dba")
        self.assertEqual(state["level"], "high")
        self.assertTrue(state["token_saver"])
        self.assertEqual(state["user_turn_count"], 4)

        state_off = argon_core.resolve_session_state(self.base_payload("/gemini-mode-argon off"))
        self.assertFalse(state_off["active"])
        self.assertEqual(state_off["user_turn_count"], 5)

        state_eng = argon_core.resolve_session_state(
            self.base_payload("/gemini-mode-argon-engineer on")
        )
        self.assertTrue(state_eng["active"])
        self.assertEqual(state_eng["role"], "engineer")

        # Test standalone /token-saver integration & punctuation stripping
        state_ts = argon_core.resolve_session_state(self.base_payload("/token-saver full"))
        self.assertTrue(state_ts["token_saver"])
        state_ts_off = argon_core.resolve_session_state(self.base_payload("/token-saver off, audit"))
        self.assertFalse(state_ts_off["token_saver"])
        state_ts_auto = argon_core.resolve_session_state(self.base_payload("/token-saver auto!"))
        self.assertTrue(state_ts_auto["token_saver"])

        # Test slash command punctuation safety
        state_punct = argon_core.resolve_session_state(self.base_payload("/gemini-mode-argon off, proceed"))
        self.assertFalse(state_punct["active"])

    def test_03_pre_invocation_turn_deduplication_and_compact_nudge(self):
        """PreInvocation injects once per user turn (no tool-loop spam) and triggers /compact at Turn 12."""
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )
        payload = self.base_payload("/gemini-mode-argon on")

        first = run_hook("pre_invocation_reminder.py", payload)
        self.assertEqual(len(first["injectSteps"]), 1)
        msg = first["injectSteps"][0]["ephemeralMessage"]
        self.assertIn("Argon v2.7 Scaffolding", msg)
        self.assertIn(os.path.join(PLUGIN_ROOT, "skills"), msg)

        second = run_hook("pre_invocation_reminder.py", payload)
        self.assertEqual(second["injectSteps"], [])

        steps_12 = [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}] + [
            {"type": "USER_INPUT", "content": f"Follow-up task {i}"} for i in range(2, 13)
        ]
        write_jsonl(self.transcript_path, steps_12)
        res_12 = run_hook("pre_invocation_reminder.py", self.base_payload("Follow-up task 12"))
        self.assertEqual(len(res_12["injectSteps"]), 1)
        self.assertIn("12 user turns since last compaction", res_12["injectSteps"][0]["ephemeralMessage"])

    def test_04_pre_tool_guard_quoted_compact_transcript_and_symlinks(self):
        """Read-before-write handles compact transcript.jsonl double quotes, symlinks, and blocks denied retries."""
        svc = os.path.join(self.workspace_dir, "service.py")
        with open(svc, "w", encoding="utf-8") as f:
            f.write("def run():\n    return 1\n")

        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )

        p_edit = self.base_payload()
        p_edit["toolCall"] = {"name": "edit_file", "args": {"Path": svc}}
        self.assertEqual(run_hook("pre_tool_guard.py", p_edit)["decision"], "deny")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": json.dumps(svc)}}],
                },
                {"type": "GENERIC", "status": "ERROR", "content": "tool call denied by pre-tool hook"},
            ],
        )
        self.assertEqual(run_hook("pre_tool_guard.py", p_edit)["decision"], "deny")

        real_svc = os.path.realpath(svc)
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "read_file", "args": {"Path": json.dumps(real_svc)}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "1: def run():"},
            ],
        )
        self.assertEqual(run_hook("pre_tool_guard.py", p_edit)["decision"], "allow")

    def test_05_self_created_file_and_post_tool_ledger_integration(self):
        """Creating a new file populates argon_state.json symbols and unlocks subsequent edit_file."""
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )
        new_mod = os.path.join(self.workspace_dir, "auth_helper.py")

        p_write = self.base_payload()
        p_write["toolCall"] = {
            "name": "write_file",
            "args": {"Path": new_mod, "Overwrite": False},
        }
        self.assertEqual(run_hook("pre_tool_guard.py", p_write)["decision"], "allow")

        with open(new_mod, "w", encoding="utf-8") as f:
            f.write(
                "class TokenValidator:\n    pass\n\n"
                "async def verify_jwt(token: str) -> bool:\n    return bool(token)\n"
            )

        self.assertEqual(run_hook("post_tool_ledger.py", p_write), {})
        ledger_file = os.path.join(self.artifact_dir, "scratch", "argon_state.json")
        self.assertTrue(os.path.isfile(ledger_file))
        with open(ledger_file, "r", encoding="utf-8") as lf:
            ledger = json.load(lf)
        self.assertIn("auth_helper.py", ledger["modifiedFiles"])
        self.assertIn("auth_helper.py:TokenValidator", ledger["exportedSymbols"])
        self.assertIn("auth_helper.py:verify_jwt", ledger["exportedSymbols"])

        p_edit = self.base_payload()
        p_edit["toolCall"] = {"name": "edit_file", "args": {"Path": new_mod}}
        self.assertEqual(run_hook("pre_tool_guard.py", p_edit)["decision"], "allow")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {"type": "USER_INPUT", "content": "Now add refresh token support"},
            ],
        )
        res_pre = run_hook("pre_invocation_reminder.py", self.base_payload("Now add refresh token support"))
        injected = res_pre["injectSteps"][0]["ephemeralMessage"]
        self.assertIn("Argon Active State Ledger", injected)
        self.assertIn("auth_helper.py:verify_jwt", injected)

    def test_06_artifact_exemption_and_reviewer_readonly_gate(self):
        """Artifacts in brain/<conv_id>/ bypass read-before-write; reviewer role blocks workspace writes."""
        plan_file = os.path.join(self.artifact_dir, "plan.md")
        with open(plan_file, "w", encoding="utf-8") as f:
            f.write("# Old Plan\n")

        ws_file = os.path.join(self.workspace_dir, "main.py")
        with open(ws_file, "w", encoding="utf-8") as f:
            f.write("print('hi')\n")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon-reviewer on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "read_file", "args": {"Path": ws_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "1: print('hi')"},
            ],
        )

        p_art = self.base_payload()
        p_art["toolCall"] = {
            "name": "write_file",
            "args": {"Path": plan_file, "Overwrite": True},
        }
        self.assertEqual(run_hook("pre_tool_guard.py", p_art)["decision"], "allow")

        p_ws = self.base_payload()
        p_ws["toolCall"] = {"name": "edit_file", "args": {"Path": ws_file}}
        res_ws = run_hook("pre_tool_guard.py", p_ws)
        self.assertEqual(res_ws["decision"], "deny")
        self.assertIn("Reviewer Gate", res_ws["reason"])

    def test_07_pipefail_test_sanitizer_preserves_exit_codes_and_env_prefix(self):
        """Rewritten test commands MUST return Exit Code != 0 on test failure and 0 on test pass."""
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )

        fail_test = os.path.join(self.workspace_dir, "test_fail.py")
        with open(fail_test, "w", encoding="utf-8") as f:
            f.write(
                "import unittest\n"
                "class T(unittest.TestCase):\n"
                "    def test_boom(self):\n"
                "        for i in range(120):\n"
                "            print(f'noise line {i}')\n"
                "        self.assertEqual(1, 2)\n"
            )

        orig_fail_cmd = (
            f"CI=true {sys.executable} -m unittest discover -s {self.workspace_dir} -p test_fail.py"
        )
        p_fail = self.base_payload()
        p_fail["toolCall"] = {"name": "run_command", "args": {"CommandLine": orig_fail_cmd}}
        res_fail = run_hook("pre_tool_guard.py", p_fail)
        self.assertEqual(res_fail["decision"], "allow")
        rewritten_fail = res_fail["overwrite"]["CommandLine"]
        self.assertIn("pipefail", rewritten_fail)
        self.assertIn("PYTHONUNBUFFERED=1", rewritten_fail)

        for shell_bin in ("/bin/zsh", "/bin/bash", "/bin/sh", "/bin/dash"):
            if os.path.exists(shell_bin):
                proc = subprocess.run(
                    [shell_bin, "-c", rewritten_fail],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertNotEqual(proc.returncode, 0)
                lines = proc.stdout.splitlines()
                self.assertEqual(len(lines), 80)
                self.assertTrue(any("AssertionError: 1 != 2" in ln for ln in lines))

        pass_test = os.path.join(self.workspace_dir, "test_pass.py")
        with open(pass_test, "w", encoding="utf-8") as f:
            f.write(
                "import unittest\n"
                "class T(unittest.TestCase):\n"
                "    def test_ok(self):\n"
                "        self.assertEqual(2 + 2, 4)\n"
            )
        orig_pass_cmd = (
            f"CI=true {sys.executable} -m unittest discover -s {self.workspace_dir} -p test_pass.py"
        )
        p_pass = self.base_payload()
        p_pass["toolCall"] = {"name": "run_command", "args": {"CommandLine": orig_pass_cmd}}
        rewritten_pass = run_hook("pre_tool_guard.py", p_pass)["overwrite"]["CommandLine"]
        tested_any_pass_shell = False
        for shell_bin in ("/bin/zsh", "/bin/bash", "/bin/sh", "/bin/dash"):
            if os.path.exists(shell_bin):
                proc_ok = subprocess.run(
                    [shell_bin, "-c", rewritten_pass],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(proc_ok.returncode, 0)
                tested_any_pass_shell = True
        self.assertTrue(tested_any_pass_shell, "At least one installed shell must be available for test_07")

    def test_08_compound_commands_and_destructive_gate(self):
        """Compound commands are untouched; destructive/publishing commands return force_ask."""
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )

        p_comp = self.base_payload()
        p_comp["toolCall"] = {
            "name": "run_command",
            "args": {"CommandLine": "pytest && rm -f tmp.db"},
        }
        res_comp = run_hook("pre_tool_guard.py", p_comp)
        self.assertEqual(res_comp["decision"], "allow")
        self.assertNotIn("overwrite", res_comp)

        for dangerous in ("git push origin main", "git reset --hard HEAD~1", "npm publish"):
            p_dang = self.base_payload()
            p_dang["toolCall"] = {"name": "run_command", "args": {"CommandLine": dangerous}}
            self.assertEqual(run_hook("pre_tool_guard.py", p_dang)["decision"], "force_ask")

    def test_09_stop_guard_precision_and_per_edit_index_rearming(self):
        """Stop guard ignores non-code/non-test noise, nudges once per edit index, and re-arms on new edits."""
        code_file = os.path.join(self.workspace_dir, "engine.py")
        svg_file = os.path.join(self.workspace_dir, "logo.svg")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "write_file", "args": {"Path": svg_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Created file."},
            ],
        )
        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"
        self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "allow")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": json.dumps(code_file)}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [
                        {"name": "run_command", "args": {"CommandLine": "git checkout -b fix/bug"}},
                        {"name": "run_command", "args": {"CommandLine": "python3 --version"}},
                    ],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
            ],
        )
        first_nudge = run_hook("stop_guard.py", p_stop)
        self.assertEqual(first_nudge["decision"], "continue")

        second_try = run_hook("stop_guard.py", p_stop)
        self.assertEqual(second_try["decision"], "allow")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": json.dumps(code_file)}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "CI=true pytest"}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
            ],
        )
        self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "allow")

        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": json.dumps(code_file)}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "CI=true pytest"}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": json.dumps(code_file)}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
            ],
        )
        self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "continue")

    def test_10_plugin_metadata_version_sync_and_rules_byte_budget(self):
        """Verify plugin.json (2.7.1), hooks.json, AGENTS.md (<16KB), and 100% v2.7 sync across all docs/skills."""
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), "r", encoding="utf-8") as f:
            plugin = json.load(f)
        self.assertEqual(plugin["version"], "2.7.1")
        self.assertEqual(plugin["logo"], "assets/logo.svg")
        self.assertEqual(len(plugin["suggestedPrompts"]), 3)
        self.assertNotIn("license", plugin)

        with open(os.path.join(PLUGIN_ROOT, "hooks.json"), "r", encoding="utf-8") as f:
            hooks = json.load(f)
        scaffolding = hooks["argon-scaffolding"]
        for event_key in ("PreInvocation", "PreToolUse", "PostToolUse", "Stop"):
            self.assertIn(event_key, scaffolding)

        agents_path = os.path.join(PLUGIN_ROOT, "rules", "AGENTS.md")
        agents_bytes = os.path.getsize(agents_path)
        self.assertLess(
            agents_bytes,
            16000,
            f"AGENTS.md should stay compact (<16KB) for defaultRulesBudget, got {agents_bytes} bytes",
        )

        checked_files = [
            os.path.join(PLUGIN_ROOT, "plugin.json"),
            agents_path,
            os.path.join(PLUGIN_ROOT, "README.md"),
            os.path.join(PLUGIN_ROOT, "README.id.md"),
        ]
        skills_root = os.path.join(PLUGIN_ROOT, "skills")
        for entry in sorted(os.listdir(skills_root)):
            skill_md = os.path.join(skills_root, entry, "SKILL.md")
            if os.path.isfile(skill_md):
                checked_files.append(skill_md)

        self.assertEqual(len(checked_files), 18)
        for fp in checked_files:
            with open(fp, "r", encoding="utf-8") as f:
                txt = f.read()
            for stale in ("v2.2", "v2.3", "v2.4", "v2.5", "v2.6", "2.3.0", "2.4.0", "2.5.0", "2.6.0", "2.7.0"):
                self.assertNotIn(stale, txt, f"Stale '{stale}' found in {fp}")

    def test_11_parallel_tool_batch_1_to_1_mapping(self):
        """In a parallel tool batch, tcs[0] failing must NOT invalidate tcs[1] read_file, nor vice-versa."""
        good_file = os.path.join(self.workspace_dir, "good.py")
        bad_new_file = os.path.join(self.workspace_dir, "bad_new.py")
        with open(good_file, "w", encoding="utf-8") as f:
            f.write("a = 1\n")
        with open(bad_new_file, "w", encoding="utf-8") as f:
            f.write("b = 2\n")

        # Batch: tcs[0] read_file("missing.py") -> ERROR; tcs[1] read_file(good_file) -> DONE;
        #        tcs[2] write_file(bad_new_file, Overwrite=False) -> ERROR (file already exists!)
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [
                        {"name": "read_file", "args": {"Path": "/nonexistent/missing.py"}},
                        {"name": "read_file", "args": {"Path": good_file}},
                        {"name": "write_file", "args": {"Path": bad_new_file, "Overwrite": False}},
                    ],
                },
                {"type": "GENERIC", "status": "ERROR", "content": "file does not exist"},
                {"type": "GENERIC", "status": "DONE", "content": "1: a = 1"},
                {"type": "GENERIC", "status": "ERROR", "content": "file already exists"},
            ],
        )

        # good_file succeeded at tcs[1] -> MUST be allowed!
        p_good = self.base_payload()
        p_good["toolCall"] = {"name": "edit_file", "args": {"Path": good_file}}
        self.assertEqual(run_hook("pre_tool_guard.py", p_good)["decision"], "allow")

        # bad_new_file failed at tcs[2] -> MUST still be denied!
        p_bad = self.base_payload()
        p_bad["toolCall"] = {"name": "edit_file", "args": {"Path": bad_new_file}}
        self.assertEqual(run_hook("pre_tool_guard.py", p_bad)["decision"], "deny")

    def test_12_stop_guard_blocks_premature_stop_on_failing_test_exit_code(self):
        """Stop guard MUST block stopping when pytest ran with status=DONE but 'Command exited with code 1.'."""
        code_file = os.path.join(self.workspace_dir, "calc.py")
        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"

        # 1. pytest ran after edit, step status="DONE", but content says "Command exited with code 1."
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "CI=true pytest"}}],
                },
                {
                    "type": "GENERIC",
                    "status": "DONE",
                    "content": "Created At: ...\nCommand exited with code 1.\n\nFAILED test_calc.py",
                },
            ],
        )
        res_fail = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_fail["decision"], "continue")
        self.assertIn("Exit Code 1", res_fail["reason"])

        # 2. Subsequent pytest passes ("Command exited with code 0.") -> stop allowed!
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "CI=true pytest"}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 1."},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "CI=true pytest"}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
            ],
        )
        self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "allow")

    def test_13_checkpoint_compaction_preserves_state_and_resets_compact_counter(self):
        """After a CHECKPOINT step, active/role persist while turns_since_checkpoint resets cleanly."""
        steps = [{"type": "USER_INPUT", "content": "/gemini-mode-argon-architect on"}]
        for i in range(2, 13):
            steps.append({"type": "USER_INPUT", "content": f"Design step {i}"})
        steps.append({"type": "CHECKPOINT", "content": "# Resuming from a compaction"})
        steps.append({"type": "USER_INPUT", "content": "Post-compact turn 1"})
        write_jsonl(self.transcript_path, steps)

        state = argon_core.resolve_session_state(self.base_payload("Post-compact turn 1"))
        self.assertTrue(state["active"])
        self.assertEqual(state["role"], "architect")
        self.assertEqual(state["user_turn_count"], 13)
        self.assertEqual(state["turns_since_checkpoint"], 1)

        # PreInvocation should NOT nag about /compact right after compaction!
        res_pre = run_hook("pre_invocation_reminder.py", self.base_payload("Post-compact turn 1"))
        msg = res_pre["injectSteps"][0]["ephemeralMessage"]
        self.assertNotIn("Context Health", msg)

    def test_14_zero_hardcoded_machine_paths_or_external_subagents(self):
        """Ensure zero '/Users/diinggo', 'poteto-agent', or hardcoded '/tmp/' in production plugin files."""
        prod_dirs = ["rules", "skills", "scripts", "agents"]
        prod_files = [
            os.path.join(PLUGIN_ROOT, "plugin.json"),
            os.path.join(PLUGIN_ROOT, "hooks.json"),
            os.path.join(PLUGIN_ROOT, "README.md"),
            os.path.join(PLUGIN_ROOT, "README.id.md"),
        ]
        for sub in prod_dirs:
            full_sub = os.path.join(PLUGIN_ROOT, sub)
            for root, dirs, files in os.walk(full_sub):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for fn in files:
                    if fn.endswith((".md", ".py", ".json")):
                        prod_files.append(os.path.join(root, fn))

        for fp in prod_files:
            with open(fp, "r", encoding="utf-8") as f:
                txt = f.read()
            self.assertNotIn("/Users/diinggo", txt, f"Hardcoded machine path found in {fp}")
            self.assertNotIn("poteto-agent", txt, f"External pstack dependency found in {fp}")
            if fp.endswith(".py"):
                # Allow comments explaining /tmp -> /private/tmp, forbid literal '"/tmp/' paths
                self.assertNotIn('"/tmp/', txt, f"Non-portable /tmp literal found in {fp}")

    def test_15_native_argon_subagents_valid_frontmatter(self):
        """Verify agents/argon-investigator.md (read-only) and agents/argon-coder.md exist and are valid."""
        inv_path = os.path.join(PLUGIN_ROOT, "agents", "argon-investigator.md")
        cod_path = os.path.join(PLUGIN_ROOT, "agents", "argon-coder.md")
        self.assertTrue(os.path.isfile(inv_path))
        self.assertTrue(os.path.isfile(cod_path))

        with open(inv_path, "r", encoding="utf-8") as f:
            inv_txt = f.read()
        self.assertTrue(inv_txt.startswith("---\nname: argon-investigator\n"))
        self.assertIn("subagent: true", inv_txt)
        self.assertNotIn("write_to_file", inv_txt)
        self.assertNotIn("replace_file_content", inv_txt)

        with open(cod_path, "r", encoding="utf-8") as f:
            cod_txt = f.read()
        self.assertTrue(cod_txt.startswith("---\nname: argon-coder\n"))
        self.assertIn("subagent: true", cod_txt)
        self.assertIn("commandExecutionPolicy: auto", cod_txt)
        self.assertIn("replace_file_content", cod_txt)
        self.assertIn("search_web", cod_txt)
        self.assertIn("read_url_content", cod_txt)

    def test_16_ide_cascade_tool_names_compatibility(self):
        """Hooks must seamlessly support Antigravity IDE / Cascade tool names (view_file, replace_file_content, write_to_file)."""
        ide_file = os.path.join(self.workspace_dir, "ide_module.ts")
        with open(ide_file, "w", encoding="utf-8") as f:
            f.write("export class IdeService {}\n")

        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )

        # 1. replace_file_content without prior view_file -> denied!
        p_rep = self.base_payload()
        p_rep["toolCall"] = {
            "name": "replace_file_content",
            "args": {"TargetFile": ide_file},
        }
        self.assertEqual(run_hook("pre_tool_guard.py", p_rep)["decision"], "deny")

        # 2. Record view_file(AbsolutePath=...) -> replace_file_content & multi_replace_file_content allowed!
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "view_file", "args": {"AbsolutePath": ide_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "1: export class IdeService {}"},
            ],
        )
        self.assertEqual(run_hook("pre_tool_guard.py", p_rep)["decision"], "allow")

        p_multi = self.base_payload()
        p_multi["toolCall"] = {
            "name": "multi_replace_file_content",
            "args": {"TargetFile": ide_file},
        }
        self.assertEqual(run_hook("pre_tool_guard.py", p_multi)["decision"], "allow")

        # 3. PostToolUse records symbols from write_to_file(TargetFile=...)
        new_ide_file = os.path.join(self.workspace_dir, "ide_created.ts")
        with open(new_ide_file, "w", encoding="utf-8") as f:
            f.write("export interface IdeContract {\n  id: string;\n}\n")
        p_w2f = self.base_payload()
        p_w2f["toolCall"] = {
            "name": "write_to_file",
            "args": {"TargetFile": new_ide_file, "Overwrite": False},
        }
        self.assertEqual(run_hook("post_tool_ledger.py", p_w2f), {})
        ledger_path = os.path.join(self.artifact_dir, "scratch", "argon_state.json")
        with open(ledger_path, "r", encoding="utf-8") as lf:
            ledger = json.load(lf)
        self.assertIn("ide_created.ts:IdeContract", ledger["exportedSymbols"])

    def test_17_same_step_parallel_edit_and_test_tuple_order(self):
        """Stop guard must use (step_idx, call_idx) so edit_file + run_command in the SAME step is recognized."""
        code_file = os.path.join(self.workspace_dir, "fast.py")
        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"

        # Single PLANNER_RESPONSE step with tcs[0]=edit_file and tcs[1]=run_command("CI=true pytest") exiting 0
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [
                        {"name": "edit_file", "args": {"Path": code_file}},
                        {"name": "run_command", "args": {"CommandLine": "CI=true pytest"}},
                    ],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
            ],
        )
        self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "allow")

        # Same single-step batch, but tcs[1] exits with code 1 -> must trigger Reflexion auto-healing!
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [
                        {"name": "edit_file", "args": {"Path": code_file}},
                        {"name": "run_command", "args": {"CommandLine": "CI=true pytest"}},
                    ],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
                {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 1."},
            ],
        )
        res_fail = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_fail["decision"], "continue")
        self.assertIn("Exit Code 1", res_fail["reason"])

    def test_18_polyglot_test_runners_and_git_global_flags(self):
        """Verify .NET/Ruby/PHP/Swift/C++ test runners and git -C / recursive rm destructive patterns."""
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )

        polyglot_cases = [
            ("App.cs", "dotnet test"),
            ("spec.rb", "bundle exec rspec"),
            ("UserTest.php", "php artisan test"),
            ("PkgTests.swift", "swift test"),
            ("main.cpp", "ctest --output-on-failure"),
        ]
        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"

        for filename, runner_cmd in polyglot_cases:
            p_cmd = self.base_payload()
            p_cmd["toolCall"] = {"name": "run_command", "args": {"CommandLine": runner_cmd}}
            res_pre = run_hook("pre_tool_guard.py", p_cmd)
            self.assertEqual(res_pre["decision"], "allow")
            self.assertIn("pipefail", res_pre.get("overwrite", {}).get("CommandLine", ""))

            fpath = os.path.join(self.workspace_dir, filename)
            write_jsonl(
                self.transcript_path,
                [
                    {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                    {
                        "type": "PLANNER_RESPONSE",
                        "status": "DONE",
                        "tool_calls": [
                            {"name": "edit_file", "args": {"Path": fpath}},
                            {"name": "run_command", "args": {"CommandLine": runner_cmd}},
                        ],
                    },
                    {"type": "GENERIC", "status": "DONE", "content": "Edited"},
                    {"type": "GENERIC", "status": "DONE", "content": "Command exited with code 0."},
                ],
            )
            self.assertEqual(run_hook("stop_guard.py", p_stop)["decision"], "allow")

        flagged_cmds = [
            "git -C /tmp/repo push origin main",
            "git --no-pager reset --hard HEAD",
            "git -c color.ui=false clean -fd",
            "rm -rf .",
            "rm -rf *",
            "rm --recursive --force /tmp/build",
            "rm -rf node_modules",
            "rm -r dist",
            "rm --recursive -f build",
        ]
        for d_cmd in flagged_cmds:
            p_d = self.base_payload()
            p_d["toolCall"] = {"name": "run_command", "args": {"CommandLine": d_cmd}}
            self.assertEqual(
                run_hook("pre_tool_guard.py", p_d)["decision"],
                "force_ask",
                f"Expected force_ask for: {d_cmd}",
            )

        p_safe = self.base_payload()
        p_safe["toolCall"] = {"name": "run_command", "args": {"CommandLine": "rm -f file.txt"}}
        self.assertEqual(run_hook("pre_tool_guard.py", p_safe)["decision"], "allow")

    def test_19_top_level_class_symbol_priority_and_line_wrap_guard(self):
        """Top-level classes/functions must take priority over indented helper methods; mid-text line wrap must not activate."""
        py_file = os.path.join(self.workspace_dir, "payment.py")
        methods = "\n".join([f"    def helper_{i}(self):\n        return {i}\n" for i in range(1, 9)])
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(
                f"class PaymentEngine:\n{methods}\n"
                "def settle_batch():\n    return True\n"
            )

        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )
        p_post = self.base_payload()
        p_post["toolCall"] = {"name": "edit_file", "args": {"Path": py_file}}
        run_hook("post_tool_ledger.py", p_post)

        ledger_path = os.path.join(self.artifact_dir, "scratch", "argon_state.json")
        with open(ledger_path, "r", encoding="utf-8") as lf:
            ledger = json.load(lf)
        syms = ledger["exportedSymbols"]
        self.assertEqual(syms[0], "payment.py:PaymentEngine")
        self.assertEqual(syms[1], "payment.py:settle_batch")

        # Line-wrap guard: mid-paragraph wrapped line starting with /gemini-mode-argon + prose must NOT turn ON
        wrapped_prose = (
            "Saya sedang menulis dokumentasi tentang plugin\n"
            "/gemini-mode-argon yang kemarin kita bahas."
        )
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": wrapped_prose}],
        )
        state_wrapped = argon_core.resolve_session_state(self.base_payload(wrapped_prose))
        self.assertFalse(state_wrapped["active"])

        # First-line prompt with task instruction DOES activate
        first_line_task = "/gemini-mode-argon Refactor modul payment.py"
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": first_line_task}],
        )
        state_first = argon_core.resolve_session_state(self.base_payload(first_line_task))
        self.assertTrue(state_first["active"])

    def test_20_logo_svg_hygiene_and_strict_plugin_json_schema(self):
        """Verify assets/logo.svg vector hygiene and strict official Antigravity plugin.json schema."""
        logo_path = os.path.join(PLUGIN_ROOT, "assets", "logo.svg")
        self.assertTrue(os.path.isfile(logo_path))
        with open(logo_path, "r", encoding="utf-8") as f:
            svg = f.read()
        self.assertIn('viewBox="0 0 512 512"', svg)
        self.assertIn("<title>", svg)
        self.assertIn('fill-rule="evenodd"', svg)
        for forbidden in ("<text", "<image", "<filter", "<style", "stroke="):
            self.assertNotIn(forbidden, svg)

        allowed_plugin_keys = {
            "name",
            "description",
            "logo",
            "suggestedPrompts",
            "displayName",
            "version",
            "author",
            "homepage",
            "repository",
            "disabled",
        }
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), "r", encoding="utf-8") as f:
            manifest = json.load(f)
        unknown_keys = set(manifest.keys()) - allowed_plugin_keys
        self.assertEqual(unknown_keys, set(), f"Unsupported plugin.json keys: {unknown_keys}")

    def test_21_coerce_bool_and_json_quoted_strings(self):
        """coerce_bool deterministically normalizes bools and json-quoted strings, unblocking new file creation."""
        for val, expected in [
            (True, True),
            (False, False),
            ("true", True),
            ("false", False),
            ('"false"', False),
            ('"true"', True),
            ("False", False),
            ("True", True),
            ("1", True),
            ("0", False),
            (1, True),
            (0, False),
        ]:
            self.assertEqual(argon_core.coerce_bool(val), expected, f"Failed for {val!r}")

        self.assertTrue(
            argon_core.is_pure_new_file_creation(
                "write_file", {"Path": "new.py", "Overwrite": '"false"', "Append": "False"}
            )
        )
        self.assertFalse(
            argon_core.is_pure_new_file_creation(
                "write_file", {"Path": "new.py", "Overwrite": '"true"'}
            )
        )

    def test_22_sequential_slash_command_token_scanner(self):
        """Sequential token scanner accurately parses multiple arguments in a single slash command line."""
        state1 = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon role dba level high token-saver on", state1)
        self.assertTrue(state1["active"])
        self.assertEqual(state1["role"], "dba")
        self.assertEqual(state1["level"], "high")
        self.assertTrue(state1["token_saver"])

        state2 = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon-engineer high token-saver on", state2)
        self.assertTrue(state2["active"])
        self.assertEqual(state2["role"], "engineer")
        self.assertEqual(state2["level"], "high")
        self.assertTrue(state2["token_saver"])

        state3 = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon on level medium", state3)
        self.assertTrue(state3["active"])
        self.assertEqual(state3["level"], "medium")

    def test_23_fully_idle_reactive_wakeup_gate(self):
        """Stop hook must allow exit when fullyIdle is False (waiting for subagent or background task), re-arming when True."""
        code_file = os.path.join(self.workspace_dir, "task.py")
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Made 1 replacement"},
            ],
        )
        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"
        p_stop["fullyIdle"] = False  # Task/subagent running in background!

        # Must allow pause without error and without burning the 1-shot tracker
        res_waiting = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_waiting["decision"], "allow")

        # Once background task finishes (fullyIdle=True) and still unverified -> must block and prompt for test
        p_stop["fullyIdle"] = True
        res_done = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_done["decision"], "continue")
        self.assertIn("Argon Deterministic Verification Gate", res_done["reason"])

    def test_24_polyglot_oop_and_sql_symbol_extraction(self):
        """Extract top-level symbols across Java, C#, Kotlin, Dart, SQL, and Ruby files."""
        polyglot_samples = {
            "OrderService.java": "public final class OrderService {\n    public void run() {}\n}\n",
            "Payment.cs": "public sealed class PaymentGateway {\n}\npublic interface IPayment {}\n",
            "State.kt": "data class UserState(val id: String)\nsealed interface UiEvent\nsuspend fun computeHash(): String = \"\"\n",
            "Widget.dart": "base class HomeController {}\nabstract interface class AuthRepo {}\n",
            "schema.sql": "CREATE TABLE IF NOT EXISTS ledger_entries (id INT);\nCREATE OR REPLACE VIEW active_ledgers AS SELECT 1;\n",
            "calc.rb": "class TaxCalculator\n  def calculate_rate\n    0.1\n  end\nend\n",
        }
        for fname, code in polyglot_samples.items():
            fpath = os.path.join(self.workspace_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(code)
            syms = [s.split(":", 1)[1] for s in post_tool_ledger.extract_file_symbols(fpath)]
            if fname == "OrderService.java":
                self.assertIn("OrderService", syms)
            elif fname == "Payment.cs":
                self.assertIn("PaymentGateway", syms)
                self.assertIn("IPayment", syms)
            elif fname == "State.kt":
                self.assertIn("UserState", syms)
                self.assertIn("UiEvent", syms)
                self.assertIn("computeHash", syms)
            elif fname == "Widget.dart":
                self.assertIn("HomeController", syms)
                self.assertIn("AuthRepo", syms)
            elif fname == "schema.sql":
                self.assertIn("ledger_entries", syms)
                self.assertIn("active_ledgers", syms)
            elif fname == "calc.rb":
                self.assertIn("TaxCalculator", syms)
                self.assertIn("calculate_rate", syms)

    def test_25_modern_wrapper_runners_database_reset_and_dual_theme_logo(self):
        """Verify modern wrapper runners (uv/poetry/bunx), database reset protection, and logo dual-theme contrast."""
        write_jsonl(
            self.transcript_path,
            [{"type": "USER_INPUT", "content": "/gemini-mode-argon on"}],
        )
        for runner in (
            "uv run pytest tests/test_core.py",
            "poetry run pytest",
            "bunx vitest run",
            "pnpx jest",
            "npx playwright test",
        ):
            p = self.base_payload()
            p["toolCall"] = {"name": "run_command", "args": {"CommandLine": runner}}
            res = run_hook("pre_tool_guard.py", p)
            self.assertEqual(res["decision"], "allow")
            self.assertIn("pipefail", res.get("overwrite", {}).get("CommandLine", ""))

        for dangerous_db in (
            "prisma migrate reset --force",
            "supabase db reset",
            "rails db:drop",
            "php artisan migrate:fresh",
            "dropdb prod_database",
        ):
            p_db = self.base_payload()
            p_db["toolCall"] = {"name": "run_command", "args": {"CommandLine": dangerous_db}}
            self.assertEqual(
                run_hook("pre_tool_guard.py", p_db)["decision"],
                "force_ask",
                f"Expected force_ask for DB command: {dangerous_db}",
            )

        # Audit logo.svg on both light (#FFFFFF) and dark (#1E1E1E) themes
        svg_audit_script = os.path.expanduser(
            "~/.gemini/config/plugins/logo-design/skills/logo-design/scripts/svg_audit.py"
        )
        if os.path.isfile(svg_audit_script):
            logo_path = os.path.join(PLUGIN_ROOT, "assets", "logo.svg")
            for bg_color in ("#FFFFFF", "#1E1E1E"):
                proc = subprocess.run(
                    [sys.executable, svg_audit_script, logo_path, "--bg", bg_color, "--json"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(proc.returncode, 0)
                audit_res = json.loads(proc.stdout.strip())
                self.assertEqual(audit_res[0]["score"], 100)
                self.assertEqual(audit_res[0]["findings"], [])

    def test_26_js_commonjs_noise_exclusion_and_ruby_self_methods(self):
        """CommonJS require() and local lets must not crowd exports; Ruby def self.method must extract method name."""
        js_file = os.path.join(self.workspace_dir, "webhook.ts")
        with open(js_file, "w", encoding="utf-8") as f:
            f.write(
                "const fs = require('fs');\n"
                "const path = require('path');\n"
                "const crypto = require('crypto');\n"
                "const http = require('http');\n"
                "let cache = null;\n"
                "let retries = 0;\n\n"
                "export async function verifyWebhookSignature(payload: string, sig: string): Promise<boolean> {\n"
                "  return true;\n"
                "}\n"
                "export const ApiEndpoint: FC<Props> = (props) => null;\n"
                "const internalHandler = async (req, res) => {\n"
                "  return true;\n"
                "};\n"
            )
        syms_js = [s.split(":", 1)[1] for s in post_tool_ledger.extract_file_symbols(js_file)]
        self.assertIn("verifyWebhookSignature", syms_js)
        self.assertIn("ApiEndpoint", syms_js)
        self.assertIn("internalHandler", syms_js)
        for noise in ("fs", "path", "crypto", "http", "cache", "retries"):
            self.assertNotIn(noise, syms_js)

        rb_file = os.path.join(self.workspace_dir, "tax.rb")
        with open(rb_file, "w", encoding="utf-8") as f:
            f.write(
                "class TaxCalculator\n"
                "  def self.calculate_rate(country)\n"
                "    0.15\n"
                "  end\n"
                "  def format_currency(amount)\n"
                "    \"$#{amount}\"\n"
                "  end\n"
                "end\n"
            )
        syms_rb = [s.split(":", 1)[1] for s in post_tool_ledger.extract_file_symbols(rb_file)]
        self.assertIn("TaxCalculator", syms_rb)
        self.assertIn("calculate_rate", syms_rb)
        self.assertNotIn("self", syms_rb)
        self.assertIn("format_currency", syms_rb)

    def test_27_async_background_test_launch_and_system_message_completion(self):
        """stop_guard skips RUNNING background launch, auto-heals on failure SYSTEM_MESSAGE, and allows on pass."""
        code_file = os.path.join(self.workspace_dir, "app_bg.py")
        task_id = "test-conv/task-42"
        p_stop = self.base_payload()
        p_stop["terminationReason"] = "NO_TOOL_CALL"
        p_stop["fullyIdle"] = True

        # 1. Background task launched, still running -> MUST not be treated as passed
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Edited file."},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "pytest"}}],
                },
                {
                    "type": "GENERIC",
                    "status": "RUNNING",
                    "content": f"Created At: ...\nTool is running as a background task with task id: {task_id}\nTask Description: pytest",
                },
            ],
        )
        res_running = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_running["decision"], "continue")
        self.assertIn("Argon Deterministic Verification Gate", res_running["reason"])

        # 1b. Unrelated background task (e.g. task-999) finishes -> task-42 is STILL running, must NOT be passed!
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Edited file."},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "pytest"}}],
                },
                {
                    "type": "GENERIC",
                    "status": "RUNNING",
                    "content": f"Tool is running as a background task with task id: {task_id}",
                },
                {
                    "type": "SYSTEM_MESSAGE",
                    "status": "DONE",
                    "content": (
                        '<SYSTEM_MESSAGE>\nTask id "test-conv/task-999" finished with result:\n\n'
                        "The command exited with code 0.\nOutput:\nDONE\n"
                    ),
                },
            ],
        )
        issue_unrelated, _canon, _pos, _code = stop_guard.inspect_code_verification(self.transcript_path)
        self.assertEqual(issue_unrelated, "unverified")

        # 2. Background task completes with error (Exit Code 1) -> MUST trigger Reflexion Auto-Healing
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Edited file."},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "pytest"}}],
                },
                {
                    "type": "GENERIC",
                    "status": "RUNNING",
                    "content": f"Tool is running as a background task with task id: {task_id}",
                },
                {
                    "type": "SYSTEM_MESSAGE",
                    "status": "DONE",
                    "content": (
                        f'<SYSTEM_MESSAGE>\nTask id "{task_id}" finished with result:\n\n'
                        "The command exited with code 1.\nOutput:\nFAILED test_app.py\n"
                    ),
                },
            ],
        )
        res_failed = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_failed["decision"], "continue")
        self.assertIn("Exit Code 1", res_failed["reason"])

        # 3. Background task completes with success (Exit Code 0) -> ALLOW stop!
        write_jsonl(
            self.transcript_path,
            [
                {"type": "USER_INPUT", "content": "/gemini-mode-argon on"},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "edit_file", "args": {"Path": code_file}}],
                },
                {"type": "GENERIC", "status": "DONE", "content": "Edited file."},
                {
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "pytest"}}],
                },
                {
                    "type": "GENERIC",
                    "status": "RUNNING",
                    "content": f"Tool is running as a background task with task id: {task_id}",
                },
                {
                    "type": "SYSTEM_MESSAGE",
                    "status": "DONE",
                    "content": (
                        f'<SYSTEM_MESSAGE>\nTask id "{task_id}" finished with result:\n\n'
                        "The command exited with code 0.\nOutput:\nPASSED\n"
                    ),
                },
            ],
        )
        res_ok = run_hook("stop_guard.py", p_stop)
        self.assertEqual(res_ok["decision"], "allow")

    def test_28_slash_parser_edge_cases_zombie_reviewer_reset_and_ast_hygiene(self):
        """Verify invalid role-suffix safety, token-saver chaining, zombie reviewer reset, and 0 unused imports."""
        # 1. Invalid role suffix must NOT activate Argon
        st_typo = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon-typo on", st_typo)
        self.assertFalse(st_typo["active"])

        # 2. token-saver without explicit on/off before role dba
        st_chain = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon token-saver role dba", st_chain)
        self.assertTrue(st_chain["active"])
        self.assertTrue(st_chain["token_saver"])
        self.assertEqual(st_chain["role"], "dba")

        # 3. Zombie reviewer reset
        st_rev = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon role reviewer", st_rev)
        self.assertTrue(st_rev["active"])
        self.assertEqual(st_rev["role"], "reviewer")
        argon_core.apply_slash_commands("/gemini-mode-argon off", st_rev)
        self.assertFalse(st_rev["active"])
        self.assertEqual(st_rev["role"], "auto")
        argon_core.apply_slash_commands("/gemini-mode-argon on", st_rev)
        self.assertTrue(st_rev["active"])
        self.assertEqual(st_rev["role"], "auto")

        # 3b. /gemini-mode-argon <task> on first-line preserves previously locked role
        st_task = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon role dba", st_task)
        self.assertEqual(st_task["role"], "dba")
        argon_core.apply_slash_commands("/gemini-mode-argon Optimize query users", st_task)
        self.assertTrue(st_task["active"])
        self.assertEqual(st_task["role"], "dba")

        # 3c. Leading slash normalization for chained /token-saver and /role
        st_slash = {"active": False, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/gemini-mode-argon /token-saver /role /dba", st_slash)
        self.assertTrue(st_slash["active"])
        self.assertTrue(st_slash["token_saver"])
        self.assertEqual(st_slash["role"], "dba")

        st_standalone = {"active": True, "role": "auto", "level": "auto", "token_saver": False}
        argon_core.apply_slash_commands("/token-saver-full\nPrompt", st_standalone)
        self.assertTrue(st_standalone["token_saver"])

        # 4. AST Static Analysis: 0 unused imports across scripts/ and tests/
        import ast
        for sub in ("scripts", "tests"):
            dirpath = os.path.join(PLUGIN_ROOT, sub)
            for fname in os.listdir(dirpath):
                if fname.endswith(".py"):
                    full_p = os.path.join(dirpath, fname)
                    with open(full_p, "r", encoding="utf-8") as pf:
                        tree = ast.parse(pf.read(), filename=fname)
                    imported = {}
                    used = set()
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                name = alias.asname or alias.name.split(".")[0]
                                imported[name] = node.lineno
                        elif isinstance(node, ast.ImportFrom):
                            for alias in node.names:
                                name = alias.asname or alias.name
                                imported[name] = node.lineno
                        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                            used.add(node.id)
                    unused = {k: v for k, v in imported.items() if k not in used}
                    self.assertEqual(
                        unused,
                        {},
                        f"Unused imports found in {fname}: {unused}",
                    )


if __name__ == "__main__":
    unittest.main()
