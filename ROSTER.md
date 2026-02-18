# Agent Roster

> Directory of all agents. Use this to find the right agent for the job.

## Summoning Protocol

When summoning an agent, the following sequence is automatic:

1. Agent reads `GENERAL_RULES.md`
2. Agent reads their `CORE.md`
3. Agent checks `memory/mistakes.md`
4. Agent scans `cheatsheets/_index.md`
5. Agent loads relevant cheatsheets for the current task
6. Agent begins work

## Example Agents

| Agent | Domain | Role | Model | Location |
|-------|--------|------|-------|----------|
| **Miles** | Aerospace | Aerodynamicist (Lead) | Opus | `agents/aerospace/miles/` |
| **Sam** | Software Dev | Backend Developer | Sonnet | `agents/software-dev/sam/` |

Miles is a fully populated example with cheatsheets and memory entries. Sam is a minimal shell showing the basic structure.

## Adding Your Own Agents

See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions on creating a new agent.

## Stats

- **Example agents:** 2 — Miles (Opus), Sam (Sonnet)
- **Templates:** `templates/CORE-TEMPLATE.md`, `templates/cheatsheet-template.md`
