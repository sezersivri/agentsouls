# Agent Souls — Claude Code Integration

## What This Is

This repository (or submodule) contains persistent AI agent identities with knowledge and memory. Each agent in `.claude/agents/` is a specialized team member with domain expertise, accumulated cheatsheets, and memory of past sessions.

## How to Use

### Automatic Agent Discovery

Claude Code automatically discovers agents from `.claude/agents/`. Each agent wrapper includes enriched frontmatter:

```yaml
---
name: miles
model: opus
description: "Lead aerodynamicist responsible for..."
skills: session-end, learn
---
```

Frontmatter fields: `name`, `model`, `description`, `skills`. Additional fields (`tools`, `permissionMode`) are supported when needed — see [CONTRIBUTING.md](CONTRIBUTING.md).

### Summoning Agents

Agents are summoned by name or by task context:
- **By name:** "Ask Miles to analyze the stability derivatives"
- **By skill:** `/summon miles`
- **By task:** Claude Code routes to the appropriate agent based on `.claude/agents/` definitions

### Skills

Framework skills live in `.claude/skills/` and provide standardized agent operations:

| Skill | Command | Purpose |
|-------|---------|---------|
| **summon** | `/summon <name>` | Load an agent's full context and identity |
| **session-end** | `/session-end` | Execute the Session End Protocol |
| **learn** | `/learn <source>` | Study source material and distill into cheatsheets |

Skills are distinct from per-agent skill files in `.agents/skills/` (which are auto-generated for cross-tool compatibility).

### Agent Loading Sequence

When an agent is activated, it MUST follow this sequence (defined in GENERAL_RULES.md):

1. Read `GENERAL_RULES.md` — the universal rules
2. Read their `CORE.md` — their identity and hard rules
3. Check `memory/mistakes.md` — pitfalls to avoid
4. Scan `cheatsheets/_index.md` — available knowledge index
5. Load relevant cheatsheets for the current task (progressive disclosure)

### Session End Protocol

Before ending ANY session, the active agent MUST:

1. Update `memory/session-log.md`
2. Record mistakes in `memory/mistakes.md`
3. Record decisions in `memory/decisions.md`
4. Update cheatsheets if new knowledge was learned
5. Update `shared-knowledge/` if learnings affect other agents
6. Commit: `git add . && git commit -m "[agent-name] session YYYY-MM-DD: description"`

## Submodule Usage

When this repo is included as a submodule (`.agents/`), the parent project's CLAUDE.md should reference it:

```markdown
## Agent Team
This project uses the agentsouls system at `.agents/`.
For specialized tasks, summon agents from `.agents/ROSTER.md`.
Agent definitions are in `.agents/.claude/agents/`.
```

## Example Agents

| Agent | Domain | Role | Model | Skills |
|-------|--------|------|-------|--------|
| Miles | Aerospace | Aerodynamicist (Lead) | Opus | session-end, learn |
| Sam | Software Dev | Backend Developer | Sonnet | session-end, learn |

## Model Configuration

Model assignments come from `agents/manifest.json`. To update models, edit the `model` field for the agent in the manifest, then run `python scripts/generate-tool-configs.py` to regenerate the wrapper files.

Current tier mapping:
- `opus` → Complex analysis, architecture, lead decisions
- `sonnet` → Implementation, domain work, specialist tasks
- `haiku` → Testing, documentation, routine tasks
