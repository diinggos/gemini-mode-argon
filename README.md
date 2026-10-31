# 🚀 Gemini Mode Argon Suite (`gemini-mode-argon`)

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

## 📋 The Argon Pre-Flight Protocol

Whenever running in **medium**, **high**, or complex **auto** modes, the agent executes a structured 4-point Pre-Flight checklist prior to modifying state:

1. **Goal & Scope:** Technical objective and exact blast radius.
2. **Key Variables & Invariants:** Core contracts, dependencies, and system constraints.
3. **Risks & Edge Cases:** Failure modes, null safety, race conditions, or counter-arguments.
4. **Validation Framework:** Concrete verification command, test metric, or proof check.

---

## 🛡 Circuit Breakers & Safety Guards

* **2-Strike Circuit Breaker:** Stops execution if any command or tool fails twice with the identical error, preventing infinite loops and prompting immediate strategy pivot.
* **Non-Interactive Execution:** Enforces flags like `CI=true`, `--yes`, and `--watch=false` to prevent terminal hangs.
* **Safety Gate:** Always requests explicit user confirmation prior to destructive file operations, database drops, git history rewrites, or billing-impacting actions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
