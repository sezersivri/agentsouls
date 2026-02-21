# Agent Souls -- Gemini CLI Integration

This repository provides a persistent identity, knowledge, and memory system for AI agent teams. It ships with 2 example agents — see [ROSTER.md](ROSTER.md) for details and [docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md) to create your own.

## Quick Start with Gemini CLI

1. Set your context file: add `"contextFileName": "AGENTS.md"` to your Gemini settings
2. Or use the skills directory: agents are available at `.agents/skills/{agent-name}/SKILL.md`

## Using Agent Skills

Each agent is packaged as a skill in `.agents/skills/`. To load an agent:

1. Read the agent's SKILL.md for their role, capabilities, and loading sequence
2. Follow the loading sequence to activate the agent's full context
3. When finishing, follow the session-end protocol in GENERAL_RULES.md

**Note:** The `.claude/skills/` directory contains Claude Code-specific framework skills (`/summon`, `/session-end`, `/learn`). These use Claude Code's native skill format and are not directly compatible with Gemini CLI. Use the loading sequence above instead.

## Available Agents

See [ROSTER.md](ROSTER.md) for the available example agents.

## Bootstrap Script

For maximum context loading, use the bootstrap script:

```bash
./scripts/load-agent.sh miles --format text
```

This assembles the agent's full context (rules + core + mistakes + knowledge index) to stdout.
