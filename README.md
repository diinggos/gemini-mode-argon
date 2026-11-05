# 🚀 Gemini Mode Argon Suite v2.7 (`gemini-mode-argon`)

**English** | [Bahasa Indonesia](README.id.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/google)
[![Reasoning](https://img.shields.io/badge/Reasoning-Frontier--Grade-orange.svg)](#)
[![Version](https://img.shields.io/badge/Version-2.7.1-emerald.svg)](#)

A high-performance reasoning and operational engine for **Google Antigravity**, engineered to elevate **Gemini 3.8 Flash** to **Gemini 4 Argon** cognitive depth, diagnostic accuracy, autonomous role specialization, and self-healing terminal execution with the **v2.7 Argon-Parity Specification**, **Standalone Native Argon Subagents (`agents/`)**, and **Cross-Surface State-Aware Lifecycle Hooks (`hooks.json`)**.

---

## 🌟 Highlights & v2.7 Argon-Parity Architecture

* **State-Aware Deterministic Scaffolding (`hooks.json` — Antigravity 2.0 App & IDE/Cascade):** Physically enforces Argon cognitive contracts when `/gemini-mode-argon` is **`ON`**, while maintaining **100% Zero-Interference (`< 3ms` no-op)** when **`OFF`**:
  * **`PreInvocation` Hook:** Injects turn-deduplicated 4-Beat CoT prompts, dynamic skill root resolution, and the live State Ledger once per user turn, plus **CHECKPOINT-aware** `/compact` health checks (resets cleanly after compaction).
  * **`PreToolUse` Hook:** Enforces **1-to-1 parallel-batch-safe** `read-before-write` across both App (`read_file`/`edit_file`/`write_file`) and IDE (`view_file`/`replace_file_content`/`multi_replace_file_content`/`write_to_file`) tools (exempting newly created session files & `brain/` artifacts via strict `coerce_bool` parsing), enforces read-only workspace safety in `reviewer` mode, wraps single-statement polyglot test runners in exit-code-preserving & unbuffered `( export PYTHONUNBUFFERED=1; set -o pipefail; cmd 2>&1 | tail -n 80 )`, and prompts on destructive/publishing commands (including `git -C` global flags and database resets like `prisma migrate reset` or `dropdb`).
  * **`PostToolUse` Hook (Photographic State Ledger):** Automatically extracts modified file paths and prioritized top-level code symbols (`class`/`interface`/`struct`/`fn` in `file:Symbol` format across Java, C#, Kotlin, Dart, Python, TS/JS, Go, Rust, Ruby, and SQL) into `scratch/argon_state.json` with zero token effort from Flash.
  * **`Stop` Hook (Exit-Code-0 Auto-Healing Gate):** Tracks `(step_idx, call_idx)` tuple ordering across polyglot test suites (`pytest`, `vitest`, `cargo`, `go`, `dotnet`, `rspec`, `phpunit`, `swift`, `ctest`, etc.), honors `fullyIdle: false` Reactive Wakeup gates for subagents and background tasks, and blocks premature turn termination whenever source-code modifications are unverified **OR** when the latest verification run exited non-zero (`Command exited with code != 0`).
* **Standalone Native Argon Subagents (`agents/`):** Zero third-party plugin dependencies for Horizontal Compute Scale-Out on complex multi-file tasks (Blast Radius $> 3$ files):
  * **`argon-investigator`:** Read-only parallel codebase recon and counterfactual root-cause hunter.
  * **`argon-coder`:** Surgical 4-Beat implementation and Exit-Code-0 verification worker.
* **Context-Budget Engineered (`rules/AGENTS.md` ~13 KB):** Compact high-density master rule preserves >70% of Antigravity's global `defaultRulesBudget` (`20,000` tokens) for workspace rules and peer plugins.
* **4-Beat Argon Execution Cadence:** `1. Parallel Recon Batch` $\rightarrow$ `2. Latent Counterfactual Gate` $\rightarrow$ `3. Adaptive Pre-Flight & Affirmative Execution` $\rightarrow$ `4. Deterministic Exit-Code-0 Verification`.
* **Adaptive Multi-Turn Pre-Flight Delta & 15/85 Token Rule:** Full 3–5 bullet Pre-Flight on Turn 1; 1-line `> 🎯 **Pre-Flight Delta [<role>]:**` on consecutive same-scope follow-ups; $\le 15\%$ framing and $\ge 85\%$ complete implementation.

---

## 🏛 Architecture Overview

```
                                      [User Prompt]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
         [Track 1: Auto-Level]                         [Track 2: Auto-Role]
      (Reasoning Effort & Cadence)                  (Autonomous Specialization)
   ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
   │ • low    : Fast / System 1 (<1s) │        │ • engineer   : Surgical coding   │
   │ • medium : 4-Beat CoT (1-3s)     │        │ • architect  : Macro & ADRs      │
   │ • high   : Reflexion & Healing   │        │ • reviewer   : Zero-trust audit  │
   │ • auto   : Deterministic Trigger │        │ • tester     : QA & hermetic mock│
   └──────────────────────────────────┘        │ • dba        : SQL & EXPLAIN     │
                     │                         │ • devops     : SRE & CI/CD       │
                     ▼                         │ • researcher : Grounded facts    │
        [Native Argon Subagents]               │ • general    : 1st-principles    │
   ┌──────────────────────────────────┐        ├──────────────────────────────────┤
   │ • argon-investigator (Read-Only) │        │ • ui-designer: Figma & Tokens    │
   │ • argon-coder (Surgical Worker)  │        │ • vector-des.: Affinity & SVG    │
   └──────────────────────────────────┘        │ • 3d-designer: Blender & glTF    │
                                               │ • motion-des.: Video & Easing    │
                                               ├──────────────────────────────────┤
                                               │ • trader     : Sentinel & Quant  │
                                               ├──────────────────────────────────┤
                                               │ • Hybrid     : [role1 + role2]   │
                                               └──────────────────────────────────┘
```

---

## ⚙️ Recommended Configuration

1. **Engine (Antigravity UI):** Set Model to **`Gemini 3.8 Flash (High)`** (delivers maximum CoT budget at Flash speed; requires `python3` on PATH for lifecycle hooks).
2. **Discipline (Plugin):** Activate once per session with `/gemini-mode-argon on`.

---

## 📦 Installation & Verification

Install into your local Antigravity plugins directory:

```bash
git clone https://github.com/diinggos/gemini-mode-argon.git ~/.gemini/config/plugins/gemini-mode-argon
```

Restart Antigravity or open a new conversation. Run the 28-scenario end-to-end verification suite locally:

```bash
python3 -m unittest discover -s ~/.gemini/config/plugins/gemini-mode-argon/tests -v
```

---

## 🕹 Slash Commands & Usage

### 1. Master Control
* `/gemini-mode-argon on` (or `/gemini-mode-argon`): Activates Full-Auto Mode (Auto-Role + Auto-Level + Active Hooks).
* `/gemini-mode-argon off`: Deactivates the suite (Zero-Interference mode) and returns to default agent behavior.
* `/gemini-mode-argon token-saver [on|off]`: Toggles zero-prose output mode (`| ⚡ **token-saver: ON**`).

### 2. Reasoning Level Overrides
* `/gemini-mode-argon level [auto | low | medium | high]`

### 3. Dedicated Role Overrides
* `/gemini-mode-argon role auto` *(default)* or `/gemini-mode-argon-<role> [on|off]`:
  * **Technical Suite (8):** `engineer`, `architect`, `reviewer`, `tester`, `dba`, `devops`, `researcher`, `general`.
  * **Creative Suite (4):** `ui-designer`, `vector-designer`, `3d-designer`, `motion-designer`.
  * **Financial & Quantitative Suite (1):** `trader`.

---

## 📋 The Role-Native Adaptive Pre-Flight Protocol

| Role | Points | Tailored Pre-Flight Protocol Steps | Focus & Safety Objective |
| :--- | :---: | :--- | :--- |
| **`engineer`** | 3–4 | `1. Pinned Scope & Blast Radius` → `2. Invariants & Contracts` → `3. Edge-Cases & Null Safety` → `4. Verification Test` | Parallel batch read, zero regression, non-interactive terminal verification |
| **`dba`** | 4–5 | `1. Pinned DB & Query Objective` → `2. Lock & Blast Radius` → `3. Index Strategy` → `4. Rollback Plan` → `5. EXPLAIN Check` | Zero table lock, composite index order, zero-data-loss rollback |
| **`architect`** | 3–4 | `1. Pinned Baseline & De-Anchoring` → `2. Domain Boundaries` → `3. Triad Matrix & Capacity Math` → `4. Opinionated ADR` | Anti-false-dichotomy, "Missing Middle" (OSS/Headless), RPS/GB math |
| **`devops`** | 4–5 | `1. Pinned Env Scope` → `2. Secret Safety & Non-Root` → `3. Pipeline/Layer Health` → `4. Rollback Strategy` → `5. Smoke Check` | Multi-stage non-root containers, zero secret leaks, automated rollback |
| **`tester`** | 3–4 | `1. Pinned Function & Framework` → `2. Equivalence Partitions` → `3. Fault Injection` → `4. Hermetic Mock Isolation` | Zero happy-path bias, boundary negative testing, strict test isolation |
| **`reviewer`** | 3–4 | `1. Pinned Audit Scope` → `2. OWASP & Concurrency Risks` → `3. Blast Radius` → `4. Readiness Score Target` | Strictly read-only, caller-verified threat triage, readiness score (1–10) |
| **`researcher`** | 3–4 | `1. Pinned Scope & Version` → `2. Source Trust Hierarchy` → `3. Deprecation & Version Drift` → `4. Grounded Evidence` | Zero hallucination, Context7/primary sources, version-pinned verification |
| **`general`** | 3–4 | `1. Pinned Baseline & Frame Check` → `2. Orthogonal Space` → `3. Causal Mechanisms` → `4. Decisive Verdict` | First-principles decomposition, Pareto synthesis, anti-sycophancy |
| **`ui-designer`** | 3–4 | `1. Pinned Viewport & Density` → `2. Hierarchy & WCAG` → `3. Semantic Token Mapping` → `4. 5 Micro-States & Edge-Cases` | W3C Design Tokens, WCAG contrast (4.5:1), touch targets (44px), Figma Auto-Layout |
| **`vector-designer`** | 3–4 | `1. Pinned Canvas/ViewBox` → `2. Geometry & Booleans` → `3. Node Density & Precision` → `4. Export & Byte Budget` | Affinity Designer MCP (`localhost:6767/sse`), Bézier curve economics, surgical SVG |
| **`3d-designer`** | 3–4 | `1. Pinned Output Target` → `2. Topology & Poly Budget` → `3. PBR Shader Strategy` → `4. Lighting & Camera Staging` | Blender `bpy` headless scripting, clean quad topology, PBR realism, glTF/GLB Draco |
| **`motion-designer`** | 3–4 | `1. Pinned FPS & Frame Duration` → `2. Physics Easing Curves` → `3. Layers & Keyframes` → `4. Encoding & Budget` | Remotion programmatic video, FFmpeg filtering, physics cubic-bezier easing, Lottie |
| **`trader`** | 5 | `1. Pinned Account & Sentinel DEFCON` → `2. Asset & Macro Regime` → `3. Weather & Lot Math` → `4. Microstructure & SMC` → `5. Lifecycle Gate` | Layer 0 AI Sentinel (DEFCON 1/3/5), deterministic Python lot sizing, MT5/Binance MCP |

> 💡 **Casual / Trivial Queries (`low`):** **Zero Pre-Flight** — instant, conversational responses with zero checklist overhead (< 1 sec).

---

## 💡 Real-World Examples (Turn 1 Full Pre-Flight vs Turn 2 Delta)

### Turn 1 — Initial Bug Fix (`engineer` on `high`)
```markdown
> 🟢 **gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2**

### Argon [engineer] Pre-Flight
- Pinned Scope & Blast Radius: `src/auth/jwt.ts:L42-L68` (`verifyAccessToken`) -> called by `src/middleware/requireAuth.ts`.
- Invariants & Contracts: Preserve `AuthClaims` return interface and HTTP 401 `TOKEN_EXPIRED` error code.
- Edge-Cases & Null Safety: Guard missing `exp` claim, clock skew (`clockTolerance: 5`), and malformed Bearer prefixes.
- Concrete Verification Test: `CI=true npx vitest run src/auth/jwt.test.ts`

**Root-Cause Delta:** `verifyAccessToken` treated numeric `0` timestamps as falsy and skipped expiration checks when `clockTolerance` was omitted.

[... 100% complete surgical diff & passing Vitest output (Exit Code 0) ...]
```

### Turn 2 — Same-Scope Follow-Up (`Pre-Flight Delta`)
```markdown
> 🟢 **gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2**
> 🎯 **Pre-Flight Delta [engineer]:** `AuthClaims` contract (`src/auth/jwt.ts`) -> Add `aud` claim validation + negative unit test -> `CI=true npx vitest run src/auth/jwt.test.ts`

[... Direct surgical implementation & Exit Code 0 verification ...]
```

---

## 🧩 Adding Custom Roles (Extensibility Guide)

1. Create `skills/gemini-mode-argon-<custom-role>/SKILL.md` with YAML frontmatter (`name`, `description`), **Universal Triad**, **Response Blueprint (`A`, `B`, or `C`)**, and **3–5 Point Pre-Flight Checklist**.
2. Add `<custom-role>` to `VALID_ROLES` in `scripts/argon_core.py` and register a compact 1-row summary in `rules/AGENTS.md` (keeping `rules/AGENTS.md` `< 24,000 bytes`).
3. Run `python3 -m unittest discover -s tests -v` to verify hook recognition.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
