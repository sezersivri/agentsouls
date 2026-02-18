# Agent Souls -- Gemini CLI Integration

This repository contains 18 AI agents with persistent identities, knowledge, and memory. For the full agent roster and architecture, see [README.md](README.md).

## Quick Start with Gemini CLI

1. Set your context file: add `"contextFileName": "AGENTS.md"` to your Gemini settings
2. Or use the skills directory: agents are available at `.agents/skills/{agent-name}/SKILL.md`

## Using Agent Skills

Each agent is packaged as a skill in `.agents/skills/`. To load an agent:

1. Read the agent's SKILL.md for their role, capabilities, and loading sequence
2. Follow the loading sequence to activate the agent's full context
3. When finishing, follow the session-end protocol in GENERAL_RULES.md

## Available Agents

See [ROSTER.md](ROSTER.md) for the complete directory of 18 agents across 6 domains.

## Bootstrap Script

For maximum context loading, use the bootstrap script:

```bash
./scripts/load-agent.sh miles --format text
```

This assembles the agent's full context (rules + core + mistakes + knowledge index) to stdout.
