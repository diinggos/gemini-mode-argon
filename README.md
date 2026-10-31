# 🚀 Gemini Mode Argon Suite (`gemini-mode-argon`)

**English** | [Bahasa Indonesia](README.id.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/google)
[![Reasoning](https://img.shields.io/badge/Reasoning-Frontier--Grade-orange.svg)](#)

A high-performance reasoning and operational engine for **Google Antigravity**, designed to bring frontier-grade reasoning discipline, autonomous role specialization, and self-healing terminal execution to Gemini-powered agent workflows.

---

## 🌟 Highlights

* **Two-Track Architecture:** Decouples **Reasoning Effort Calibration** (`low`, `medium`, `high`, `auto`) from **Specialized Role Dispatching** (8 technical domains).
* **Autonomous Auto-Role:** Automatically classifies user prompts to invoke the best engineering archetype on the fly.
* **Pre-Flight Protocols:** Enforces a mandatory 4-point verification checklist before synthesizing solutions or mutating files.
* **Terminal Auto-Healing (Level High):** Autonomously executes tests, captures runtime failures, and self-corrects until exit code 0.
* **Universal Triad Pattern & 5-Block Architecture:** Instinctively maps the "Jalan Tengah" (Missing Middle) across all roles and delivers responses with native Argon's decisive 5-block structure.
* **Frontier Fluid Rigor & Anti-Anchoring:** Selectively challenges false dichotomies gracefully with real-world DX empathy (database relations vs webhook sync, pricing cliffs).
* **Zero Overhead on Trivial Tasks:** System 1 instant latency for casual questions, escalating to deep System 2 Chain-of-Thought for complex engineering.

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
   │ • auto   : Dynamic Escalation    │        │ • tester     : QA & hermetic mock│
   └──────────────────────────────────┘        │ • dba        : SQL & EXPLAIN     │
                                               │ • devops     : SRE & CI/CD       │
                                               │ • researcher : Grounded facts    │
                                               │ • general    : 1st-principles    │
                                               ├──────────────────────────────────┤
                                               │ • ui-designer: Figma & Tokens    │
                                               │ • vector-des.: Affinity & SVG    │
                                               │ • 3d-designer: Blender & glTF    │
                                               │ • motion-des.: Video & Easing    │
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
* `/gemini-mode-argon level auto`: Dynamic escalation based on task complexity *(default)*.
* `/gemini-mode-argon level low`: Fast System 1 mode; zero Pre-Flight overhead (< 1s).
* `/gemini-mode-argon level medium`: Balanced System 2 CoT with compact 4-point Pre-Flight (1–3s).
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

---

## 📋 The Role-Native Adaptive Pre-Flight Protocol

Instead of enforcing a rigid, generic 4-point template across all domains, **`gemini-mode-argon`** implements a **Role-Native Adaptive Pre-Flight Protocol (3–5 points)** that dynamically tailors its verification checklist to the exact domain and risk profile of the active role.

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

> 💡 **Casual / Trivial Queries (`low`):** **Zero Pre-Flight** — instant, conversational responses with zero checklist overhead (< 1 sec).

---

## 💡 Real-World Examples in Action

Here is how `gemini-mode-argon` behaves across real engineering and architectural tasks:

### 1. Systems Architecture: The Universal Triad Pattern (`architect` | `high`)
When presented with a binary dilemma, the engine avoids simplistic trade-offs and surfaces the *Missing Middle*:

> **User Prompt:** *"Our app is getting slow due to background tasks (emails, image processing, webhook sync). Should we build our own queue using a Cron Job polling the database, or deploy Apache Kafka / RabbitMQ?"*

```text
> 🟢 gemini-mode-argon [AUTO: architect] [high]

### Argon [architect] Pre-Flight
- Selective De-anchoring & Spectrum Check: Rejects false dichotomy; evaluates OSS/Headless alternatives.
- Domain Boundaries & System Topology: Asynchronous Task Processing vs Event Streaming; idempotency & DLQ.
- Multi-Dimensional Trade-off Matrix: Latency, DB connection exhaustion, cluster maintenance overhead.
- Opinionated ADR Recommendation: Decisive roadmap recommendation tailored to current team scale.

[Executive Verdict]
For 95% of modern web applications, do not use Cron Job database polling, and do not jump prematurely to Apache Kafka. The battle-tested "Missing Middle" is a Redis-backed queue (BullMQ/Sidekiq/Celery) or PostgreSQL FOR UPDATE SKIP LOCKED.

[The Hidden Iceberg]
- Cron DB Polling: Causes race conditions, duplicate processing, and I/O thrashing on your primary OLTP database.
- Apache Kafka: An event streaming commit log, not a background task queue (lacks native per-task retry/delay).

[The Triad Comparison Matrix]
| Evaluation Dimension | 1. Custom Cron + DB Polling | 2. The Missing Middle (Redis / SKIP LOCKED) | 3. Enterprise Broker (Kafka) |
| Setup & Latency | Fragile, 1m+ delay | Near-instant (<10ms), hours to setup | Weeks of cluster configuration |
| Production DB Load | High (lock contention & polling) | Zero (Redis) / Minimal (SKIP LOCKED) | Zero (isolated broker cluster) |
| Built-in Queue Features | Manual retry/DLQ engineering | Native retry, exponential backoff, DLQ | Requires complex custom architecture |

[Grounded DX Guidance]
- Queue Isolation: Isolate CPU-bound image compression workers from latency-critical email queues.
```

---

### 2. Surgical Engineering: Autonomous Terminal Auto-Healing (`engineer` | `high`)
When fixing code or implementing features, the engine enforces strict read-before-write and autonomously iterates in the terminal until tests pass:

> **User Prompt:** *"Fix the TypeError in auth refresh token middleware and make sure all tests pass."*

```text
> 🟢 gemini-mode-argon [AUTO: engineer] [high]

### Argon [engineer] Pre-Flight
- Target Scope & Blast Radius: auth/middleware.ts & token verification logic.
- Invariants & System Contracts: Preserve JWT claims structure; handle null/expired refresh tokens gracefully.
- Edge-Cases & Null Safety: Undefined authorization header, malformed token payload, token reuse detection.
- Concrete Verification Test: CI=true npm test auth.test.ts.

[Execution Flow]
1. Reads auth/middleware.ts with read_file (preserves unrelated comments/docstrings).
2. Applies surgical chunk edits using edit_file (zero placeholders).
3. Executes terminal command: CI=true npm test auth.test.ts.
4. Captures exit code and stderr: if assertions fail, autonomously refines code and re-runs.
5. Reports complete solution only after achieving Exit Code 0.
```

---

### 3. Fast Trivial Query: Zero Overhead (< 1s) (`general` | `low`)
Casual or straightforward questions receive instant, natural responses without procedural bureaucracy:

> **User Prompt:** *"How do I convert a string to an integer in Go?"*

```text
> 🟢 gemini-mode-argon [AUTO: general] [low]

Use `strconv.Atoi` from the Go standard library:

package main

import (
    "fmt"
    "strconv"
)

func main() {
    i, err := strconv.Atoi("42")
    if err != nil {
        panic(err)
    }
    fmt.Println(i) // 42
}

*(Zero Pre-Flight checklist overhead, immediate System 1 response).*
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

Activates the **Application Security & Hardening Engine**.

## Usage
- `/gemini-mode-argon-secops on` (or `/gemini-mode-argon-secops`): Enables threat modeling, CVE audits, secret safety, and IAM least-privilege policies.
- `/gemini-mode-argon-secops off`: Returns to standard assistant behavior.

## Mandatory Active Status Badge
When active, every response begins with:
`> 🟢 **gemini-mode-argon-secops: ON**`
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
  - **`secops` (3–4 pts):** Threat Surface & Asset Scope → Attack Vectors & CVE Severity → Blast Radius Assessment → Non-Destructive Remediation Verification.
```

---

### Step 3: Use and Verify Your Role

Once registered, Antigravity automatically loads the new role upon next prompt:

1. **Automatic Detection (Full Auto):**
   * Ask any question matching the role's domain keywords:
     > *"Audit our Dockerfile and IAM policy for secret leaks and root privileges."*
   * The engine automatically activates:
     `> 🟢 **gemini-mode-argon [AUTO: secops] [high]**`
2. **Manual Command Override:**
   * Lock via master role override: `/gemini-mode-argon role secops`
   * Lock via dedicated slash command: `/gemini-mode-argon-secops on`
   * Deactivate: `/gemini-mode-argon-secops off`

---

## 🛡 Circuit Breakers & Safety Guards

* **2-Strike Circuit Breaker:** Stops execution if any command or tool fails twice with the identical error, preventing infinite loops and prompting immediate strategy pivot.
* **Non-Interactive Execution:** Enforces flags like `CI=true`, `--yes`, and `--watch=false` to prevent terminal hangs.
* **Safety Gate:** Always requests explicit user confirmation prior to destructive file operations, database drops, git history rewrites, or billing-impacting actions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
