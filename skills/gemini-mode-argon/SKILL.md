---
name: gemini-mode-argon
description: Universal frontier reasoning engine (v2.7) with Auto-Role (13 disciplines), Auto-Level, native subagents, and state-aware hooks. Trigger via /gemini-mode-argon [on|off].
---

# Gemini Mode Argon: Master Router (/gemini-mode-argon)

Controls the **Universal Frontier Reasoning Engine** featuring **Autonomous Role Dispatching (Auto-Role)**, **Gemini-Aligned Reasoning Effort Calibration (Auto-Level)**, **Native Argon Subagents**, and the **v2.7 Argon-Parity Specification** engineered to elevate Gemini 3.8 Flash to Gemini 4 Argon cognitive depth, diagnostic accuracy, and execution fluidity via state-aware physical gates (`hooks.json`). Master protocols live in `rules/AGENTS.md`.

## Usage
- `/gemini-mode-argon on` (or `/gemini-mode-argon`): Activates **Full Auto Mode** (Auto-Role across 13 disciplines + Auto-Level `low`/`medium`/`high` + active lifecycle hooks).
- `/gemini-mode-argon off`: Deactivates Argon mode (`< 3ms` zero-interference hook no-op) and restores standard assistant behavior.

## Overrides & Sub-Commands
- `/gemini-mode-argon level [auto | low | medium | high]`: Lock reasoning intensity (`low` <1s zero Pre-Flight; `medium` 4-Beat CoT; `high` Reflexion + Exit-Code-0 terminal auto-healing).
- `/gemini-mode-argon role [auto | engineer | reviewer | architect | tester | dba | devops | researcher | general | ui-designer | vector-designer | 3d-designer | motion-designer | trader]`: Lock specialist role.
- `/gemini-mode-argon token-saver [on | off]`: Toggle zero-prose mode (`| ⚡ **token-saver: ON**`).

## Mandatory Active Status Badge & Stateful Telemetry
`> 🟢 **gemini-mode-argon [<role-indicator>] [<level-indicator>] | Strike: <0-2>/2**`

*Examples:*
- Coding: `> 🟢 **gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2**`
- Hybrid: `> 🟢 **gemini-mode-argon [AUTO: trader + dba] [high] | Strike: 0/2**`
- Composed: `> 🟢 **gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2** | 📋 **gemini-spec: [AUTO: plan]** | ⚡ **gemini-exec: [AUTO: direct]** | ⚡ **token-saver: ON**`

## v2.7 Argon-Parity Core Architecture
1. **State-Aware Deterministic Scaffolding (`hooks.json`):** Zero interference when `OFF`; enforces 4 lifecycle hooks when `ON`:
   - `PreInvocation`: Turn-deduplicated 4-Beat CoT, dynamic skill root path, Active State Ledger, and CHECKPOINT-aware `/compact` monitor.
   - `PreToolUse`: Parallel-batch-safe `read-before-write` gate, `reviewer` read-only workspace gate, exit-code-preserving `( export PYTHONUNBUFFERED=1; set -o pipefail; cmd 2>&1 | tail -n 80 )` test cap, and destructive/publish confirmation.
   - `PostToolUse`: Automatic extraction of modified files and qualified symbols (`file:Symbol`) into `scratch/argon_state.json`.
   - `Stop`: Prevents premature exit on unverified edits OR failing verification runs (`Command exited with code != 0`).
2. **Native Standalone Subagents (`agents/`):**
   - `argon-investigator`: Read-only parallel codebase recon & counterfactual root-cause hunter.
   - `argon-coder`: Surgical 4-Beat implementation & Exit-Code-0 verification worker.
3. **Adaptive Multi-Turn Pre-Flight Delta:** Full 3–5 bullet Pre-Flight on Turn 1; 1-line `> 🎯 **Pre-Flight Delta [<role>]:**` on consecutive same-scope follow-ups.
