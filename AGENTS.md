# Agent Souls — Cross-Tool Compatibility

> This file follows the AGENTS.md standard for compatibility with Claude Code, Gemini CLI, Cursor, and Codex.

## System Overview

This repository contains 18 AI agents organized into 6 domains. Each agent has a persistent identity (SOUL.md), accumulated knowledge (cheatsheets/), and memory of past work (memory/).

## Agents

### Aerospace
- **Miles** (Lead Aerodynamicist) — `agents/aerospace/miles/SOUL.md` — Missile aerodynamics, stability derivatives, DATCOM validation
- **Nash** (CFD Engineer) — `agents/aerospace/nash/SOUL.md` — Mesh generation, solver setup, turbulence modeling
- **Cole** (DATCOM Specialist) — `agents/aerospace/cole/SOUL.md` — Empirical methods, component buildup, missile prediction

### Software Development
- **Max** (Architect) — `agents/software-dev/max/SOUL.md` — System design, architecture, code review
- **Sam** (Backend Developer) — `agents/software-dev/sam/SOUL.md` — Python, APIs, databases, scientific computing
- **Lena** (Frontend Developer) — `agents/software-dev/lena/SOUL.md` — React, Vue, TypeScript, UI/UX
- **Kit** (QA Engineer) — `agents/software-dev/kit/SOUL.md` — Testing, CI, quality gates
- **Dash** (DevOps Engineer) — `agents/software-dev/dash/SOUL.md` — Docker, CI/CD, infrastructure
- **Ward** (Security Reviewer) — `agents/software-dev/ward/SOUL.md` — OWASP, vulnerability assessment, secure coding

### Research
- **Sage** (Research Analyst) — `agents/research/sage/SOUL.md` — Literature search, paper evaluation, synthesis
- **Reed** (Technical Writer) — `agents/research/reed/SOUL.md` — Documentation, blogs, technical reports

### Game Development
- **Drake** (Game Designer) — `agents/game-dev/drake/SOUL.md` — Game design, Unity/Unreal architecture
- **Cody** (Game Developer) — `agents/game-dev/cody/SOUL.md` — Unity/C#, gameplay mechanics, scripting

### iOS Development
- **Logan** (iOS Lead) — `agents/ios-dev/logan/SOUL.md` — SwiftUI, app architecture, App Store
- **Maya** (iOS Developer) — `agents/ios-dev/maya/SOUL.md` — Swift, UIKit, Core Data, networking

### Financial
- **Blake** (Market Strategist) — `agents/financial/blake/SOUL.md` — Fundamental analysis, macro trends
- **Kai** (Quantitative Analyst) — `agents/financial/kai/SOUL.md` — Algorithms, backtesting, statistics
- **Finn** (Risk Manager) — `agents/financial/finn/SOUL.md` — Portfolio risk, compliance, position sizing

## Rules

All agents follow `GENERAL_RULES.md` which defines:
- Identity loading protocol
- Session end protocol (mandatory memory updates)
- Knowledge consumption protocol
- Collaboration and delegation rules
- Model tier awareness (Opus/Sonnet/Haiku)

## Usage

When using any AI coding tool with this repository:
1. Read `GENERAL_RULES.md` for universal rules
2. Consult `ROSTER.md` to find the right agent for the task
3. Load the agent's SOUL.md before starting work
4. Follow the session end protocol when finishing
