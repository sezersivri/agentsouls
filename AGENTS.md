# Agent Souls -- Cross-Tool Compatibility

> This file follows the AGENTS.md standard for compatibility with Claude Code, Gemini CLI, Cursor, and Codex.

## System Overview

This repository provides a persistent identity, knowledge, and memory framework for AI agents. It ships with 2 example agents and templates for creating your own. Each agent has a persistent identity (CORE.md), accumulated knowledge (cheatsheets/), and memory of past work (memory/).

## Agent Loading Protocol

When activating any agent, follow this 5-step sequence:

1. **Read `GENERAL_RULES.md`** -- the universal constitution all agents follow
2. **Read the agent's `CORE.md`** -- identity, hard rules, personality, and expertise
3. **Check `memory/mistakes.md`** -- know what pitfalls to avoid from past sessions
4. **Scan `cheatsheets/_index.md`** -- discover what distilled knowledge is available
5. **Load relevant cheatsheets** -- only load what the current task requires (progressive disclosure)

Never skip steps 1-3. They exist to prevent repeated mistakes and ensure consistent identity.

## Session-End Protocol

Before ending ANY session, the active agent MUST follow the session-end protocol defined in `GENERAL_RULES.md`. In summary:

1. Update `memory/session-log.md` with what was done, learned, and any mistakes
2. Record mistakes in `memory/mistakes.md` with root cause and prevention
3. Record key decisions in `memory/decisions.md` with rationale
4. Update cheatsheets if new knowledge was learned
5. Update `shared-knowledge/` if learnings affect other agents

## Example Agents

- **Miles** (Aerodynamicist, Lead) -- `agents/aerospace/miles/CORE.md` -- Fully populated with cheatsheets and memory
- **Sam** (Backend Developer) -- `agents/software-dev/sam/CORE.md` -- Minimal shell showing the structure

## Rules

All agents follow `GENERAL_RULES.md` which defines:
- Identity loading protocol
- Session end protocol (mandatory memory updates)
- Knowledge consumption protocol
- Collaboration and delegation rules
- Model tier awareness (Opus/Sonnet/Haiku)

## Cross-Tool Usage

### Claude Code

Native integration. Agents are auto-discovered from `.claude/agents/`. Summon by name or use slash commands.

```
"Ask Miles to analyze the stability derivatives"
```

### Gemini CLI

Set `"contextFileName": "AGENTS.md"` in your Gemini settings, or use the skill files directly:

```
Read .agents/skills/miles/SKILL.md
```

See [GEMINI.md](GEMINI.md) for full Gemini CLI integration instructions.

### Codex CLI

Codex reads `AGENTS.md` automatically. For per-agent context, reference the skill files:

```
Read .agents/skills/sam/SKILL.md
```

### Cursor

Reference agent files in `.cursorrules`:

```
For backend tasks, load agents/software-dev/sam/CORE.md
```

## Usage

When using any AI coding tool with this repository:
1. Read `GENERAL_RULES.md` for universal rules
2. Consult `ROSTER.md` to find the right agent for the task
3. Load the agent's CORE.md before starting work
4. Follow the session end protocol when finishing
