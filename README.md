# Agent Souls

[![Validate](https://github.com/sezersivri/agentsouls/actions/workflows/validate.yml/badge.svg)](https://github.com/sezersivri/agentsouls/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-blueviolet)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-compatible-blue)
![Codex CLI](https://img.shields.io/badge/Codex_CLI-compatible-green)

**Your AI coding agent forgets everything between sessions. Agent Souls gives it a persistent brain.**

> Identity. Knowledge. Memory. All in Markdown, all in Git.

---

### The Problem

You open a new session. Your agent doesn't know your naming conventions. It repeats yesterday's mistake. It suggests a pattern you've explicitly rejected three times. You explain everything again — and tomorrow, you'll do it all over.

### The Fix

```
agents/aerospace/miles/
├── CORE.md              ← Identity: "Lead aerodynamicist. Starts every analysis with a
│                           back-of-envelope sanity check. Distrusts any result that
│                           violates physical intuition without thorough investigation."
├── cheatsheets/         ← Accumulated expertise:
│   ├── stability-derivatives.md    [TEXTBOOK] — reference axis systems, sign conventions
│   ├── x-tail-configurations.md    [DERIVED]  — roll coupling effects he worked out
│   └── common-unit-pitfalls.md     [VERIFIED] — mistakes he's seen in real sessions
├── memory/
│   ├── mistakes.md      ← "Forgot to convert Cm_alpha from /rad to /deg. Sanity check
│   │                        caught it — 57× too large. RULE: always state units explicitly."
│   ├── decisions.md     ← "Used body-axis over stability-axis — rationale: decouples
│   │                        lateral modes at high alpha where stability-axis breaks down."
│   └── session-log.md   ← Full history of every past session
```

When Miles starts a session, he loads who he is, checks his past mistakes, and picks up where he left off. When the session ends, he writes back what he learned. **No databases. No runtimes. Just files you can read, version, and control.**

---

## Quickstart

### Try It (2 minutes)

**Claude Code:**
```bash
git clone https://github.com/sezersivri/agentsouls.git
cd agentsouls
claude  # Agents auto-discovered from .claude/agents/
# Say: "Ask Miles to analyze the stability derivatives"
```

**Gemini CLI:**
```bash
git clone https://github.com/sezersivri/agentsouls.git && cd agentsouls
# Add to your Gemini settings: "contextFileName": "AGENTS.md"
gemini
# Say: "Load Miles from .agents/skills/miles/SKILL.md and analyze stability"
```

**Codex CLI:**
```bash
git clone https://github.com/sezersivri/agentsouls.git && cd agentsouls
codex  # Reads AGENTS.md automatically
# Say: "Use the Sam agent skill at .agents/skills/sam/SKILL.md for backend work"
```

### Make It Yours (10 minutes)

Agents are personal — the real value comes from agents that know *your* conventions and *your* past mistakes.

1. **Fork** this repo and [make it private](docs/PRIVATE-SETUP.md)
2. **Delete** the example agents (Miles, Sam)
3. **Create** your own: copy `templates/CORE-TEMPLATE.md`, fill in identity and rules
4. **Generate**: `python scripts/generate-tool-configs.py && python scripts/validate.py`

Full guide: **[docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md)** (two setup paths: Private Fork or Template Clone)

### Add to Your Project

```bash
git submodule add https://github.com/sezersivri/agentsouls.git .agents
# Your agents travel with you across projects
```

## How It Works

| Layer | What It Does | Files |
|-------|-------------|-------|
| **Identity** | Who the agent is, hard rules, personality | `CORE.md` |
| **Knowledge** | Distilled domain expertise, loaded on-demand | `cheatsheets/*.md` |
| **Memory** | What happened, what went wrong, what was decided | `memory/mistakes.md`, `decisions.md`, `session-log.md` |

**Loading sequence** (automatic on summon):
1. Read `GENERAL_RULES.md` — universal rules all agents follow
2. Read `CORE.md` — identity and hard rules
3. Check `mistakes.md` — pitfalls to avoid
4. Scan `cheatsheets/_index.md` — available knowledge
5. Load relevant cheatsheets for the current task

**Session end** (automatic via `/session-end`):
- Log what happened, record mistakes, update cheatsheets, commit to Git

## Example Agents

| Agent | Domain | Role | Model | What It Demonstrates |
|-------|--------|------|-------|---------------------|
| **Miles** | Aerospace | Aerodynamicist | Opus | Fully populated: 3 cheatsheets, memory entries, past sessions |
| **Sam** | Software Dev | Backend Developer | Sonnet | Minimal shell: shows the bare structure |

## Architecture

```
agentsouls/
├── agents/
│   ├── manifest.json            # Source of truth (v2.0 schema)
│   └── {domain}/{agent}/
│       ├── CORE.md              # Identity, rules, personality
│       ├── cheatsheets/         # Distilled domain knowledge
│       └── memory/              # Session logs, mistakes, decisions
├── .claude/
│   ├── agents/                  # Auto-generated Claude Code wrappers
│   ├── skills/                  # Framework skills (summon, session-end, learn)
│   └── settings.json            # Lifecycle hooks
├── .agents/skills/              # Auto-generated cross-tool skill files
├── scripts/                     # generate, validate, index
├── templates/                   # Templates for new agents/cheatsheets
└── GENERAL_RULES.md             # The Constitution
```

### Manifest v2.0

Agents are defined in `agents/manifest.json`. The v2.0 schema adds optional fields beyond the original identity fields:

```json
{
  "name": "Miles",
  "slug": "miles",
  "model": "opus",
  "skills": ["session-end", "learn"],
  ...
}
```

| Field | Purpose | Default |
|-------|---------|---------|
| `skills` | Framework skills to pre-load | `[]` |
| `tools` | Restrict available tools | `null` (all) |
| `permissionMode` | Permission mode for agent sessions | `"default"` |

All v2.0 fields are optional — omit them for v1.0 behavior. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full reference.

### Generated Wrappers

Running `python scripts/generate-tool-configs.py` produces wrappers from the manifest. Claude Code wrappers get enriched frontmatter:

```yaml
---
name: miles
model: opus
description: "Lead aerodynamicist responsible for..."
skills: session-end, learn
---
```

Claude Code reads these fields natively — `name`, `model`, `description` for agent discovery, `skills` for pre-loading framework skills.

## Cross-Tool Support

| Tool | How It Works |
|------|-------------|
| **Claude Code** | Native — agents auto-discovered from `.claude/agents/` with enriched frontmatter |
| **Gemini CLI** | Set `contextFileName: "AGENTS.md"` or load skills directly |
| **Codex CLI** | Reads `AGENTS.md` automatically |
| **Cursor** | Reference `CORE.md` paths in `.cursorrules` |

## Skills

Framework skills live in `.claude/skills/` and are invoked via slash commands:

| Skill | Command | What It Does |
|-------|---------|-------------|
| **summon** | `/summon <name>` | Load an agent's full context and identity |
| **session-end** | `/session-end` | Execute the Session End Protocol (log, record, commit) |
| **learn** | `/learn <source>` | Study source material and distill into cheatsheets |

Each skill has `allowed-tools` in its frontmatter — for example, `/summon` is read-only (`Read, Grep, Glob`), while `/session-end` can write (`Read, Grep, Glob, Edit, Write, Bash`).

**Two types of skill files:**
- `.claude/skills/` — framework skills, manually maintained, shared across all agents
- `.agents/skills/` — per-agent skill files, auto-generated from manifest for cross-tool compatibility

## Lifecycle Hooks

The framework configures Claude Code hooks in `.claude/settings.json`:

| Hook | What It Does |
|------|-------------|
| **Stop** | Reminds you to run `/session-end` if an agent was active |
| **PreCompact** | Warns if there are uncommitted memory updates before context compaction |
| **SubagentStop** | Same reminder when a subagent finishes |

These prevent the most common mistake: forgetting to persist what the agent learned.

## Contributing

Contributions to the **framework** are welcome — bug fixes, new tool integrations, template improvements, docs. See [CONTRIBUTING.md](CONTRIBUTING.md).

**Not accepted:** New agents. Agents are personal — create them in your [private fork](docs/PRIVATE-SETUP.md).

## Validation

The framework includes a 10-check validation suite:

```bash
python scripts/validate.py          # Run all checks
python scripts/generate-tool-configs.py --check  # Verify no drift in generated files
bash scripts/update-indexes.sh --check           # Verify cheatsheet indexes
```

Checks cover manifest schema, path resolution, frontmatter, UTF-8, generated file drift, memory structure, skills, and v2.0 field validity.

## Roadmap

1. **Knowledge Seeding** — Populate example cheatsheets through real usage
2. **Multi-repo Support** — Submodule overlay for agents across projects
3. **Agent Teams** — Multi-agent coordination for complex cross-domain tasks

## Requirements

Python >= 3.10 (for scripts; no external dependencies).

## License

[MIT](LICENSE)
