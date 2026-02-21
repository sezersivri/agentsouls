# Agent Souls -- Cursor Integration

This repository provides a persistent identity, knowledge, and memory system for AI agent teams. It ships with 2 example agents -- see [ROSTER.md](ROSTER.md) for details and [docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md) to create your own.

## Quick Start with Cursor

Cursor automatically reads `.cursorrules` from the repo root. This file is auto-generated from `agents/manifest.json` and includes:

- The list of available agents with `@` references to their CORE.md files
- The loading sequence for activating an agent
- The session-end protocol

No manual setup needed -- just open the project in Cursor.

## Using Agents

Each agent is listed in `.cursorrules` with an `@` reference to their CORE.md. To load an agent:

1. Read GENERAL_RULES.md for the universal rules
2. Read the agent's CORE.md (Cursor resolves the `@` reference)
3. Check their memory/mistakes.md
4. Scan their cheatsheets/_index.md
5. Load relevant cheatsheets for the current task

When finishing, follow the session-end protocol in GENERAL_RULES.md.

## Available Agents

See [ROSTER.md](ROSTER.md) for the available example agents.

## Regenerating .cursorrules

The `.cursorrules` file is auto-generated. To update it after changing the manifest:

```bash
python scripts/generate-tool-configs.py
```
