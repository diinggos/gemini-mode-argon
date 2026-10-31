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
* `/gemini-mode-argon level high`: Maximum rigor (~92% Argon equivalence) with mandatory terminal execution and autonomous auto-healing (5–10s).

### 3. Dedicated Role Overrides
* `/gemini-mode-argon role auto`: Dynamic role detection *(default)*.
* `/gemini-mode-argon-engineer on`: Lock into Principal Software Engineer mode.
* `/gemini-mode-argon-architect on`: Lock into Principal Systems Architect mode.
* `/gemini-mode-argon-reviewer on`: Lock into Read-Only Security Auditor & PR Reviewer mode.
* `/gemini-mode-argon-tester on`: Lock into QA & Test Automation Specialist mode.
* `/gemini-mode-argon-dba on`: Lock into Database Administrator & SQL Performance mode.
* `/gemini-mode-argon-devops on`: Lock into SRE & Infrastructure Automation mode.
* `/gemini-mode-argon-researcher on`: Lock into Primary-Source Technical Researcher mode.
* `/gemini-mode-argon-general on`: Lock into First-Principles Cross-Domain Strategist mode.

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

> 💡 **Casual / Trivial Queries (`low`):** **Zero Pre-Flight** — instant, conversational responses with zero checklist overhead (< 1 sec).

---

## 🛡 Circuit Breakers & Safety Guards

* **2-Strike Circuit Breaker:** Stops execution if any command or tool fails twice with the identical error, preventing infinite loops and prompting immediate strategy pivot.
* **Non-Interactive Execution:** Enforces flags like `CI=true`, `--yes`, and `--watch=false` to prevent terminal hangs.
* **Safety Gate:** Always requests explicit user confirmation prior to destructive file operations, database drops, git history rewrites, or billing-impacting actions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
