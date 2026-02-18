# Agent Souls

**Status: Public Alpha**

A persistent identity, knowledge, and memory system for AI agent teams — built on Markdown and Git.

## Purpose

Most coding agents forget everything between sessions. Your agent doesn't know your conventions, repeats yesterday's mistakes, and loses hard-won domain knowledge every time you close the terminal.

**Agent Souls fixes this.** Each agent gets a persistent identity (`CORE.md`), accumulated expertise (cheatsheets), and memory of past sessions — all stored as version-controlled files. When an agent is summoned, it loads who it is, what it knows, and what it's learned from past mistakes. When the session ends, it writes back what it learned.

No databases. No runtimes. Just files you can read, version, and control.

## Who This Is For

**Yes, if you:**
- Use AI CLI tools (Claude Code, Gemini CLI, Codex CLI) for real work
- Want agents that remember your project conventions and past mistakes
- Prefer inspectable, version-controlled configuration over opaque platforms
- Build across multiple projects and want shared agent knowledge

**Not yet, if you:**
- Want a turnkey platform with a GUI — this is a file-based system for CLI power users
- Need real-time multi-agent communication — agents share knowledge through files, not live messaging
- Expect a polished consumer product — this is an early-stage framework

## Quickstart

### Try the Examples

Clone the repo and try the included example agents (Miles and Sam) to see how the system works.

**Claude Code:**
```bash
git clone https://github.com/sezersivri/agentsouls.git
cd agentsouls
claude  # Agents auto-discovered from .claude/agents/
# Say: "Ask Miles to analyze the stability derivatives"
```

**Gemini CLI:**
```bash
git clone https://github.com/sezersivri/agentsouls.git
cd agentsouls
# Add to your Gemini settings: "contextFileName": "AGENTS.md"
gemini
# Say: "Load Miles from .agents/skills/miles/SKILL.md and analyze stability"
```

**Codex CLI:**
```bash
git clone https://github.com/sezersivri/agentsouls.git
cd agentsouls
codex  # Reads AGENTS.md automatically
# Say: "Use the Sam agent skill at .agents/skills/sam/SKILL.md for backend work"
```

### Create Your Own Agents

Once you've seen how the examples work, create agents tailored to your workflow:

1. Fork this repo and make it private (see [Private Setup Guide](docs/PRIVATE-SETUP.md))
2. Delete the example agents (Miles, Sam)
3. Copy `templates/CORE-TEMPLATE.md` to `agents/{domain}/{name}/CORE.md`
4. Fill in your agent's identity, expertise, and rules
5. Add the agent to `agents/manifest.json`
6. Run `python scripts/generate-tool-configs.py` and `python scripts/validate.py`

See [docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md) for the full step-by-step guide.

### Add to Your Project

```bash
# Add as a git submodule
git submodule add https://github.com/sezersivri/agentsouls.git .agents

# In your project's CLAUDE.md, add:
# See .agents/CLAUDE.md for agent team instructions

# Update to latest
git submodule update --remote .agents
```

## Use It Privately

**Agents are personal.** The value of Agent Souls comes from agents that know *your* conventions, *your* project, and *your* past mistakes. This repo provides the framework and examples — the agents you create should live in your own private repository.

Two setup paths:

| Path | Best for | Upstream updates? |
|------|----------|-------------------|
| **Private Fork** | Most users | Yes — pull from upstream |
| **Template Clone** | Full independence | No — you own everything |

See [docs/PRIVATE-SETUP.md](docs/PRIVATE-SETUP.md) for detailed instructions on both paths.

## Example Agents

The repo ships with 2 example agents to demonstrate the system. Use them as references when creating your own.

| Agent | Domain | Role | Model | Content |
|-------|--------|------|-------|---------|
| **Miles** | Aerospace | Aerodynamicist (Lead) | Opus | 3 cheatsheets, memory entries — fully populated example |
| **Sam** | Software Dev | Backend Developer | Sonnet | Empty shell — shows the minimal structure |

See [ROSTER.md](ROSTER.md) for details.

## How It Works

### The Core System

Each agent has a `CORE.md` that defines identity, personality, hard rules, expertise, and collaboration preferences. This file is read at every session start — the agent knows who it is before doing any work.

### The Knowledge System

Agents build **cheatsheets** — compressed, actionable reference files created from studying source materials. Each cheatsheet covers one topic, includes confidence levels (`[VERIFIED]`, `[TEXTBOOK]`, `[DERIVED]`), and is indexed for on-demand loading. Agents don't dump full textbooks into context — they load only what's relevant.

### The Memory System

Three memory files per agent:
- `session-log.md` — what happened in each session
- `mistakes.md` — errors made, root causes, prevention rules (read at every startup)
- `decisions.md` — key technical decisions and their rationale

### Progressive Disclosure

Agents always load: `CORE.md`, `mistakes.md`, `cheatsheets/_index.md`. Individual cheatsheets load on-demand based on the current task. Raw references never load — they get distilled into cheatsheets first.

## Architecture

```
agentsouls/
├── CLAUDE.md                    # Claude Code integration
├── AGENTS.md                    # Cross-tool compatibility (Gemini, Codex)
├── GENERAL_RULES.md             # The Constitution — rules all agents follow
├── ROSTER.md                    # Agent directory and summoning protocol
├── agents/
│   ├── manifest.json            # Single source of truth for all agents
│   └── {domain}/{agent}/
│       ├── CORE.md              # Identity, rules, personality
│       ├── cheatsheets/         # Distilled domain knowledge
│       ├── references/          # Source materials
│       └── memory/              # Session logs, mistakes, decisions
├── shared-knowledge/            # Cross-agent shared context
├── templates/                   # Templates for new agents/cheatsheets
├── scripts/                     # Automation (generate, validate, index)
├── .agents/skills/              # Cross-tool skill files (Gemini, Codex)
├── .claude/agents/              # Native Claude Code agent wrappers
└── .github/workflows/           # CI validation
```

## Cross-Tool Compatibility

| Tool | Integration | Agent Files |
|------|-------------|-------------|
| **Claude Code** | Native via `.claude/agents/` | Auto-discovered, use `/summon` |
| **Gemini CLI** | `AGENTS.md` or `contextFileName` setting | `.agents/skills/{agent}/SKILL.md` |
| **Codex CLI** | `AGENTS.md` auto-read | `.agents/skills/{agent}/SKILL.md` |
| **Cursor** | `.cursorrules` references | Direct `CORE.md` paths |

See [AGENTS.md](AGENTS.md) for cross-tool setup details. See [GEMINI.md](GEMINI.md) for Gemini CLI-specific instructions.

## Custom Commands

- `/summon <agent-name>` — Load an agent's full context and identity
- `/session-end` — Execute the mandatory Session End Protocol
- `/learn <source>` — Study source material and distill into cheatsheets

## Contributing

Agent Souls is an open-source framework. Contributions that improve the framework are welcome:

- Bug fixes in scripts (`validate.py`, `generate-tool-configs.py`)
- New tool integrations (Cursor, Windsurf, etc.)
- Template improvements
- Documentation improvements
- Suggestions and feature requests via [GitHub Issues](https://github.com/sezersivri/agentsouls/issues)

**Not accepted:** New agents. Agents are personal — create them in your [private fork](docs/PRIVATE-SETUP.md).

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Roadmap

**Next milestones:**

1. **Knowledge Seeding** — Populate cheatsheets for example agents through real usage sessions
2. **Multi-repo Support** — Submodule overlay system for using agents across multiple projects
3. **v1.0 Stable** — Stabilize the manifest schema, session-end protocol, and cross-tool packaging based on feedback

## Requirements

Python >= 3.10 (for validation and code generation scripts; no external dependencies).

## License

[MIT](LICENSE)
