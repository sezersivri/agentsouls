---
name: summon
description: Summon an agent from the agentsouls roster
allowed-tools: Read, Grep, Glob
---

Summon an agent from the agentsouls roster.

Usage: /summon <agent-name>

The agent name should match a slug in `agents/manifest.json` or an entry in `.claude/agents/` (e.g., Miles, Sam). See ROSTER.md for a human-readable list.

When summoning, execute the agent's loading sequence:
1. Read GENERAL_RULES.md
2. Read the agent's CORE.md from their directory in agents/
3. Check their memory/mistakes.md
4. Read their memory/brief.md — token-capped state snapshot (do NOT read session-log.md on summon; brief.md is the bounded alternative)
5. Scan their cheatsheets/_index.md
6. Load relevant cheatsheets for the current task

Then announce: "I am [Agent Name], [role]. I've loaded my identity, reviewed my past mistakes, and scanned my available knowledge. Ready to work."

The argument provided is: $ARGUMENTS
