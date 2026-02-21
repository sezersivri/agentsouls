# Agent Souls -- Windsurf Integration

This repository provides a persistent identity, knowledge, and memory system for AI agent teams. It ships with 2 example agents -- see [ROSTER.md](ROSTER.md) for details and [docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md) to create your own.

## Quick Start with Windsurf

Windsurf (Codeium) reads `.windsurfrules` from the repo root. This file is auto-generated from `agents/manifest.json` and kept concise (under 6K characters) to fit Windsurf's rules limit.

No manual setup needed -- just open the project in Windsurf.

## Using Agents

The `.windsurfrules` file lists available agents with paths to their CORE.md files. To load an agent:

1. Read GENERAL_RULES.md for the universal rules
2. Read the agent's CORE.md (path listed in .windsurfrules)
3. Check their memory/mistakes.md
4. Scan their cheatsheets/_index.md
5. Load relevant cheatsheets for the current task

When finishing, follow the session-end protocol in GENERAL_RULES.md.

## Limitations

Windsurf rules have a 6K character limit per file and do not support file references. The generated `.windsurfrules` is intentionally condensed. For full agent context, read the CORE.md files directly.

## Available Agents

See [ROSTER.md](ROSTER.md) for the available example agents.

## Regenerating .windsurfrules

The `.windsurfrules` file is auto-generated. To update it after changing the manifest:

```bash
python scripts/generate-tool-configs.py
```
