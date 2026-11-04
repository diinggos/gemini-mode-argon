# 🚀 Gemini Mode Argon Suite v2.0 (`gemini-mode-argon`)

**English** | [Bahasa Indonesia](README.id.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/google)
[![Reasoning](https://img.shields.io/badge/Reasoning-Frontier--Grade-orange.svg)](#)
[![Version](https://img.shields.io/badge/Version-2.0.0-emerald.svg)](#)

A high-performance reasoning and operational engine for **Google Antigravity**, designed to bring frontier-grade reasoning discipline, autonomous role specialization, and self-healing terminal execution to Gemini-powered agent workflows with **v2.0 Argon-Parity Specification**.

---

## 🌟 Highlights & v2.0 Argon-Parity Architecture

* **Two-Track Architecture:** Decouples **Reasoning Effort Calibration** (`low`, `medium`, `high`, `auto`) from **Specialized Role Dispatching** (13 domains across Technical, Creative, and Financial suites).
* **Stateful Cognitive Anchor & Telemetry:** Line 1 active status badge includes live strike telemetry (`| Strike: <0-2>/2`) to prevent context drift and strike amnesia across conversation turns.
* **Multi-Domain Hybrid Role Composition:** Blends dual specialties (e.g. `[AUTO: trader + dba]` or `[AUTO: devops + reviewer]`) when prompts span multiple domains instead of degrading to generic behavior.
* **Mid-Flight Dynamic Pivot:** Unanchors from initial assumptions when file inspection or terminal output uncovers deeper system complexity mid-turn.
* **Deterministic Auto-Level Escalation:** Rigorous deterministic boundaries guarantee appropriate level selection (`low` <15 lines with 0 mutations, `medium` audits/designs, `high` code/migrations/quant).
* **3 Domain-Matched Output Blueprints (15/85 Token Rule):** Strict token budget allocation allocating $\le 15\%$ to Pre-Flight framing and $\ge 85\%$ to complete, unabridged technical implementation across Blueprints A (Macro), B (Engineering), and C (Audit/Gate).
* **Anti-Reward-Hacking Gate:** Terminal auto-healing strictly prohibits weakening test assertions, deleting failing tests, or suppressing types to fake passing builds.
* **Zero-Strike MCP & CLI Graceful Fallback:** Automatically pivots to complete standalone code artifacts if external MCP servers (Figma, Affinity Designer, Blender bpy, MT5/Binance) are offline.
* **Context-Clean Terminal Execution:** Pipes and flags (`CI=true`, `--quiet`, `| tail -n 80`) protect context hygiene against massive log blowouts.

---

## 🏛 Architecture Overview

```
                                      [User Prompt]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
         [Track 1: Auto-Level]                         [Track 2: Auto-Role]
      (Reasoning Effort Calibration)                 (Autonomous Specialization)
   ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
   │ • low    : Fast / System 1 (<1s) │        │ • engineer   : Surgical coding   │
   │ • medium : Balanced CoT (1-3s)   │        │ • architect  : Macro & ADRs      │
   │ • high   : Reflexion & Healing   │        │ • reviewer   : Zero-trust audit  │
   │ • auto   : Deterministic Heuristic│       │ • tester     : QA & hermetic mock│
   └──────────────────────────────────┘        │ • dba        : SQL & EXPLAIN     │
                                               │ • devops     : SRE & CI/CD       │
                                               │ • researcher : Grounded facts    │
                                               │ • general    : 1st-principles    │
                                               ├──────────────────────────────────┤
                                               │ • ui-designer: Figma & Tokens    │
                                               │ • vector-des.: Affinity & SVG    │
                                               │ • 3d-designer: Blender & glTF    │
                                               │ • motion-des.: Video & Easing    │
                                               ├──────────────────────────────────┤
                                               │ • trader     : Sentinel & Quant  │
                                               ├──────────────────────────────────┤
                                               │ • Hybrid     : [role1 + role2]   │
                                               └──────────────────────────────────┘
```

---

## ⚙️ Recommended Configuration

For the optimal balance of throughput and deep reasoning:

1. **Engine (Antigravity UI):** Set Model to **`Gemini 3.8 Flash (High)`**
   * Delivers maximum Chain-of-Thought (CoT) token budget without latency penalties.
2. **Discipline (Plugin):** Keep in **`auto`** mode
   * Activate once with `/gemini-mode-argon on`.
   * Automatically executes fast System 1 responses for casual chat, and scales to rigorous System 2 Pre-Flight + Auto-Healing for complex tasks.

---

## 📦 Installation

To install into your local Antigravity environment:

```bash
git clone https://github.com/diinggos/gemini-mode-argon.git ~/.gemini/config/plugins/gemini-mode-argon
```

Restart Antigravity or open a new conversation. Antigravity will automatically detect and load the plugin.

---

## 🕹 Slash Commands & Usage

### 1. Master Control
* `/gemini-mode-argon on` (or `/gemini-mode-argon`): Activates Full-Auto Mode (Auto-Role + Auto-Level).
* `/gemini-mode-argon off`: Deactivates the suite and returns to default agent behavior.

### 2. Reasoning Level Overrides
* `/gemini-mode-argon level auto`: Dynamic escalation based on deterministic heuristics *(default)*.
* `/gemini-mode-argon level low`: Fast System 1 mode; zero Pre-Flight overhead (< 1s).
* `/gemini-mode-argon level medium`: Balanced System 2 CoT with compact 3–5 point Pre-Flight (1–3s).
* `/gemini-mode-argon level high`: Deep multi-pass reflexion with mandatory terminal auto-healing (5–10s).

### 3. Dedicated Role Overrides
* `/gemini-mode-argon role auto`: Dynamic role detection *(default)*.
* **Technical Suite:**
  * `/gemini-mode-argon-engineer on`: Lock into Principal Software Engineer mode.
  * `/gemini-mode-argon-architect on`: Lock into Principal Systems Architect mode.
  * `/gemini-mode-argon-reviewer on`: Lock into Read-Only Security Auditor & PR Reviewer mode.
  * `/gemini-mode-argon-tester on`: Lock into QA & Test Automation Specialist mode.
  * `/gemini-mode-argon-dba on`: Lock into Database Administrator & SQL Performance mode.
  * `/gemini-mode-argon-devops on`: Lock into SRE & Infrastructure Automation mode.
  * `/gemini-mode-argon-researcher on`: Lock into Primary-Source Technical Researcher mode.
  * `/gemini-mode-argon-general on`: Lock into First-Principles Cross-Domain Strategist mode.
* **Creative Suite:**
  * `/gemini-mode-argon-ui-designer on`: Lock into Principal UI/UX & Design Systems mode.
  * `/gemini-mode-argon-vector-designer on`: Lock into Precision Vector & Affinity Designer mode.
  * `/gemini-mode-argon-3d-designer on`: Lock into 3D Artist & Blender bpy mode.
  * `/gemini-mode-argon-motion-designer on`: Lock into Motion Designer & Remotion/FFmpeg mode.
* **Financial & Quantitative Suite:**
  * `/gemini-mode-argon-trader on`: Lock into Principal Quantitative Strategist, AI Sentinel & Algorithmic Trading mode.

---

## 📋 The Role-Native Adaptive Pre-Flight Protocol

Instead of enforcing a rigid, generic template across all domains, **`gemini-mode-argon`** implements a **Role-Native Adaptive Pre-Flight Protocol (3–5 points)** enforcing Pinned Assumptions (Bullet #1) and Concrete Workspace Anchoring.

| Role | Points | Tailored Pre-Flight Protocol Steps | Focus & Safety Objective |
| :--- | :---: | :--- | :--- |
| **`engineer`** | 3–4 | `1. Scope & Blast Radius` → `2. Invariants & Contracts` → `3. Edge-Cases & Null Safety` → `4. Verification Test` | Zero regression, non-interactive flags, verified terminal execution |
| **`dba`** | 4–5 | `1. Query Objective` → `2. Lock & Blast Radius` → `3. Index Strategy` → `4. Rollback & Data Safety` → `5. EXPLAIN Check` | Zero table lock, composite index order, zero-data-loss rollback |
| **`architect`** | 3–4 | `1. Selective De-Anchoring` → `2. Domain Boundaries` → `3. Triad Trade-off Matrix` → `4. Opinionated ADR` | Anti-false-dichotomy, "Missing Middle" (OSS/Headless), DX ergonomics |
| **`devops`** | 4–5 | `1. Target Environment` → `2. Secret Safety` → `3. Pipeline/Container Health` → `4. Rollback Strategy` → `5. Smoke Test` | Multi-stage non-root containers, zero secret leaks, automated rollback |
| **`tester`** | 3–4 | `1. Function Under Test` → `2. Equivalence Partitions` → `3. Fault Injection` → `4. Hermetic Mock Isolation` | Zero happy-path bias, boundary negative testing, strict test isolation |
| **`reviewer`** | 3–4 | `1. Audit Scope` → `2. OWASP & Concurrency Risks` → `3. Blast Radius` → `4. Production Readiness Score` | Strictly read-only, threat surface triage, production readiness (1–10) |
| **`researcher`** | 3–4 | `1. Research Scope` → `2. Source Trust Hierarchy` → `3. Deprecation & Version Drift` → `4. Grounded Evidence` | Zero hallucination, primary sources only, version-pinned verification |
| **`general`** | 3–4 | `1. Frame Invalidation` → `2. Orthogonal Space` → `3. Causal Mechanisms` → `4. Decisive Recommendation` | First-principles decomposition, Pareto synthesis, anti-sycophancy |
| **`ui-designer`** | 3–4 | `1. Viewport & Density` → `2. Information Hierarchy` → `3. Token Mapping (Color/Grid)` → `4. 5 Micro-States & Edge-Cases` | W3C Design Tokens, WCAG contrast (4.5:1), touch targets (44px), Figma Auto-Layout |
| **`vector-designer`** | 3–4 | `1. Canvas/ViewBox Target` → `2. Geometry & Booleans` → `3. Node Density & Precision` → `4. Export & Byte Budget` | Affinity Designer MCP (`localhost:6767/sse`), Bézier curve economics, surgical SVG |
| **`3d-designer`** | 3–4 | `1. Output Target (Web/Render)` → `2. Topology & Budget` → `3. PBR Shader Strategy` → `4. Lighting & Staging` | Blender `bpy` headless scripting, clean quad topology, PBR realism, glTF/GLB Draco |
| **`motion-designer`** | 3–4 | `1. FPS & Duration Target` → `2. Easing & Interpolation` → `3. Layers & Keyframes` → `4. Performance Budget` | Remotion programmatic video, FFmpeg filtering, physics cubic-bezier easing, Lottie |
| **`trader`** | 5 | `1. Sentinel DEFCON Status` → `2. Market Regime & Drivers` → `3. Weather & Lot Math` → `4. Microstructure & Confluence` → `5. Execution & Lifecycle` | Layer 0 AI Sentinel (DEFCON 1/3/5), deterministic lot sizing, MT5/Binance MCP, Auto-BE |

> 💡 **Casual / Trivial Queries (`low`):** **Zero Pre-Flight** — instant, conversational responses with zero checklist overhead (< 1 sec).

---

## 💡 Real-World Examples in Action (v2.0 Telemetry & Blueprints)

### 1. Hybrid Multi-Domain Execution (`trader + dba` | `high`)
When a task crosses two technical domains, the engine composes both roles without falling back to generic behavior:

> **User Prompt:** *"Design a PostgreSQL audit ledger schema for our crypto trading bot to record execution fills, fees, and funding rates with zero lock contention."*

```text
> 🟢 gemini-mode-argon [AUTO: trader + dba] [high] | Strike: 0/2

### Argon [trader + dba] Pre-Flight
- Pinned DB Baseline & Sentinel Status: PostgreSQL 16 + DEFCON 5 All-Clear -> [Ledger schema for trade fills].
- Table Lock & Concurrency Scope: High-frequency append-only ledger; avoid row locking on hot execution path.
- Index & Partition Strategy: Partition by range (timestamp month); composite index (symbol, fill_time DESC).
- Zero-Data-Loss Safety & Rollback: Transactional DDL migration with reversible rollback script.

[Blueprint B Execution: Outputting complete SQL migration script, composite indexing, and partition logic]
```

---

### 2. Systems Architecture: The Universal Triad Pattern (`architect` | `high`)
When presented with a binary dilemma, the engine avoids simplistic trade-offs and surfaces the *Missing Middle*:

```text
> 🟢 gemini-mode-argon [AUTO: architect] [high] | Strike: 0/2

### Argon [architect] Pre-Flight
- Pinned Baseline & Selective De-anchoring: Rejects false dichotomy; evaluates OSS/Headless alternatives.
- Domain Boundaries & System Topology: Asynchronous Task Processing vs Event Streaming; idempotency & DLQ.
- Multi-Dimensional Trade-off Matrix: Latency, DB connection exhaustion, cluster maintenance overhead.
- Opinionated ADR Recommendation: Decisive roadmap recommendation tailored to current team scale.

[Blueprint A Execution: Executive Verdict -> The Hidden Iceberg -> Triad Matrix -> Decision Guide -> Next Steps]
```

---

### 3. Surgical Engineering: Autonomous Terminal Auto-Healing (`engineer` | `high`)
When fixing code, the engine enforces strict read-before-write, anti-reward-hacking, and iterates until tests pass:

```text
> 🟢 gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2

### Argon [engineer] Pre-Flight
- Pinned Scope & Blast Radius: auth/middleware.ts:L42-L88 -> Token verification callers.
- Invariants & System Contracts: Preserve JWT claims structure; handle null/expired refresh tokens gracefully.
- Edge-Cases & Null Safety: Undefined authorization header, malformed token payload, token reuse detection.
- Concrete Verification Test: CI=true npm test auth.test.ts.

[Execution Flow]
1. Reads auth/middleware.ts with read_file.
2. Applies surgical chunk edits using edit_file (zero placeholders).
3. Executes terminal command: CI=true npm test auth.test.ts | tail -n 80.
4. Auto-healing strictly fixes root cause without weakening test assertions.
5. Reports complete solution only after achieving Exit Code 0.
```

---

## 🛠 Adding Custom Roles (Extensibility Guide)

`gemini-mode-argon` is designed to be fully extensible. You can define your own specialized domain roles (e.g., `secops`, `mlops`, `frontend`, `product`) in 3 simple steps:

### Step 1: Create the Skill Definition File
Create a new directory and `SKILL.md` file inside the `skills/` folder:
`skills/gemini-mode-argon-<role-name>/SKILL.md`

Example for a new **`secops`** role (`skills/gemini-mode-argon-secops/SKILL.md`):

```markdown
---
name: gemini-mode-argon-secops
description: Cloud security and application security hardening specialist. Triggered via /gemini-mode-argon-secops [on|off].
---

# Gemini Mode Argon: SecOps (/gemini-mode-argon-secops)

Activates the **Application Security & Hardening Engine**. Governed by `rules/AGENTS.md` v2.0.

## Usage
- `/gemini-mode-argon-secops on` (or `/gemini-mode-argon-secops`): Enables threat modeling, CVE audits, secret safety, and IAM least-privilege policies.
- `/gemini-mode-argon-secops off`: Returns to standard assistant behavior.

## Mandatory Active Status Badge & Telemetry
When active, every response begins with:
`> 🟢 **gemini-mode-argon [SECOPS] [<level>] | Strike: <0-2>/2**`
```

---

### Step 2: Register in `rules/AGENTS.md`
Open `rules/AGENTS.md` and add your role to three sections:

#### 1. Add to Track 2 (Autonomous Role Dispatcher Table):
```markdown
| **Security / IAM / CVE / Hardening / Pentest** | **`secops`** | Zero-trust least-privilege, threat surface modeling, secret zero-leakage, container hardening. |
```

#### 2. Define its "Missing Middle" in Track 3 (Universal Triad Pattern):
```markdown
- **`secops`:** Ignoring security entirely $\longleftrightarrow$ **Automated Static Scanning & Hardened Baseline Defaults (Jalan Tengah)** $\longleftrightarrow$ Rigid security bureaucracy that halts all shipping.
```

#### 3. Define its Tailored Adaptive Pre-Flight Checklist:
```markdown
  - **`secops` (3–4 pts):** Pinned Asset Scope & Threat Surface → Attack Vectors & CVE Severity → Blast Radius Assessment → Non-Destructive Remediation Verification.
```

---

### Step 3: Use and Verify Your Role

Once registered, Antigravity automatically loads the new role upon next prompt:

1. **Automatic Detection (Full Auto):**
   * Ask any question matching the role's domain keywords:
     > *"Audit our Dockerfile and IAM policy for secret leaks and root privileges."*
   * The engine automatically activates:
     `> 🟢 **gemini-mode-argon [AUTO: secops] [high] | Strike: 0/2**`
2. **Manual Command Override:**
   * Lock via master role override: `/gemini-mode-argon role secops`
   * Lock via dedicated slash command: `/gemini-mode-argon-secops on`
   * Deactivate: `/gemini-mode-argon-secops off`

---

## 🛡 Circuit Breakers & Safety Guards

* **Stateful 2-Strike Circuit Breaker:** Stops execution if any command or tool fails twice with the identical error, incrementing strike telemetry (`| Strike: 1/2` $\rightarrow$ `| Strike: 2/2`) and prompting immediate strategy pivot.
* **Anti-Reward-Hacking Gate:** Strictly prohibits modifying or weakening unit test assertions during auto-healing loops.
* **Zero-Strike MCP Fallback:** Gracefully outputs standalone code artifacts when external MCP servers are offline.
* **Context-Clean Terminal Execution:** Enforces non-interactive flags (`CI=true`, `--yes`, `--watch=false`) and concise log output (`| tail -n 80` or `head -n 20`) to prevent context pollution.
* **Strict Scope Confinement:** Confines execution strictly to the direct problem and local files requested by the user. Zero unilateral scope creep or unrequested actions.
* **Mandatory Remote & Publishing Confirmation:** Strictly prohibits executing external publishing, remote repository creation (`gh repo create`), remote push (`git push`), package publishing (`npm publish`), or cloud deployments without explicit, interactive confirmation in chat immediately prior to execution—even if outlined in an approved plan.
* **Destructive Operations Safety Gate:** Always requests explicit user confirmation prior to destructive file operations, database drops, git history rewrites (`git reset --hard`), or billing-impacting actions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
