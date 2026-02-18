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
agents/software-dev/sam/
├── CORE.md              ← "I am Sam. I write Python APIs. I never use print() for logging."
├── cheatsheets/         ← Distilled knowledge I've learned across sessions
├── memory/
│   ├── mistakes.md      ← "Session 3: Used raw SQL instead of ORM. Root cause: skipped CORE.md rules."
│   ├── decisions.md     ← "Chose FastAPI over Flask — rationale: async + type hints"
│   └── session-log.md   ← What happened in every past session
```

When Sam starts a session, he loads his identity, checks his past mistakes, and picks up where he left off. When the session ends, he writes back what he learned. **No databases. No runtimes. Just files you can read, version, and control.**

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
│   ├── manifest.json            # Source of truth — all agents defined here
│   └── {domain}/{agent}/
│       ├── CORE.md              # Identity, rules, personality
│       ├── cheatsheets/         # Distilled domain knowledge
│       └── memory/              # Session logs, mistakes, decisions
├── templates/                   # Templates for new agents/cheatsheets
├── scripts/                     # generate, validate, index
├── .claude/agents/              # Auto-generated Claude Code wrappers
├── .agents/skills/              # Auto-generated cross-tool skill files
└── GENERAL_RULES.md             # The Constitution
```

## Cross-Tool Support

| Tool | How It Works |
|------|-------------|
| **Claude Code** | Native — agents auto-discovered from `.claude/agents/` |
| **Gemini CLI** | Set `contextFileName: "AGENTS.md"` or load skills directly |
| **Codex CLI** | Reads `AGENTS.md` automatically |
| **Cursor** | Reference `CORE.md` paths in `.cursorrules` |

## Commands

| Command | What It Does |
|---------|-------------|
| `/summon <name>` | Load an agent's full context and identity |
| `/session-end` | Execute the Session End Protocol (log, record, commit) |
| `/learn <source>` | Study source material and distill into cheatsheets |

## Contributing

Contributions to the **framework** are welcome — bug fixes, new tool integrations, template improvements, docs. See [CONTRIBUTING.md](CONTRIBUTING.md).

**Not accepted:** New agents. Agents are personal — create them in your [private fork](docs/PRIVATE-SETUP.md).

## Roadmap

1. **Knowledge Seeding** — Populate example cheatsheets through real usage
2. **Multi-repo Support** — Submodule overlay for agents across projects
3. **v1.0 Stable** — Stabilize manifest schema and cross-tool packaging

## Requirements

Python >= 3.10 (for scripts; no external dependencies).

## License

[MIT](LICENSE)
