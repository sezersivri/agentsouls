# Agent Roster

> Directory of all agents. Use this to find the right agent for the job.

## Summoning Protocol

Use `/summon <name>` to activate an agent. The loading sequence is automatic:

1. Agent reads `GENERAL_RULES.md`
2. Agent reads their `CORE.md`
3. Agent checks `memory/mistakes.md`
4. Agent scans `cheatsheets/_index.md`
5. Agent loads relevant cheatsheets for the current task
6. Agent begins work

For Claude Code: agents are auto-discovered from `.claude/agents/` with enriched frontmatter (name, model, description, skills).
For other tools: load agents via `.agents/skills/{slug}/SKILL.md`.

## Example Agents

| Agent | Domain | Role | Model | Location |
|-------|--------|------|-------|----------|
| **Miles** | Aerospace | Aerodynamicist (Lead) | Opus | `agents/aerospace/miles/` |
| **Sam** | Software Dev | Backend Developer | Sonnet | `agents/software-dev/sam/` |

Miles is a fully populated example with cheatsheets and memory entries. Sam is a minimal shell showing the basic structure.

## Creating Your Own Agents

To create agents for your workflow, set up a private fork and follow the step-by-step guide in [docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md). For the technical reference on agent creation (templates, manifest schema, validation), see [CONTRIBUTING.md](CONTRIBUTING.md).

## Stats

- **Example agents:** 2 — Miles (Opus), Sam (Sonnet)
- **Templates:** `templates/CORE-TEMPLATE.md`, `templates/cheatsheet-template.md`
