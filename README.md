# Agent Souls

A persistent identity, knowledge, and memory system for AI agent teams. Each agent has a defined role, accumulated expertise, and memory of past sessions — all stored as version-controlled markdown files.

## What This Is

This repository stores the "souls" of AI agents — their personalities, hard rules, domain knowledge (as cheatsheets), and memories of past work. When connected to Claude Code (or other AI coding tools), agents are summoned with their full context, making them consistent, knowledgeable team members that learn over time.

**Key features:**
- **Persistent memory** — agents remember mistakes and don't repeat them
- **Distilled knowledge** — cheatsheets compress textbooks into actionable reference
- **Version-controlled growth** — every learning is a git commit
- **Multi-tool compatible** — works with Claude Code, Gemini CLI, Cursor, and others
- **Model-tier routing** — Opus for leads, Sonnet for specialists, Haiku for utilities

## Quick Start

### Using with Claude Code

This repo is designed to be added as a **git submodule** to any project:

```bash
# Add to your project
git submodule add https://github.com/sezersivri/agent-souls.git .agents

# In your project's CLAUDE.md, add:
# See .agents/CLAUDE.md for agent team instructions
```

Or use it standalone:

```bash
git clone https://github.com/sezersivri/agent-souls.git
cd agent-souls
claude  # Start Claude Code in this directory
```

### Summoning an Agent

Claude Code automatically discovers agents from `.claude/agents/`. You can:

1. **Direct mention:** "Ask Miles to analyze the stability derivatives"
2. **Slash command:** Use `/summon miles` to load an agent's full context
3. **Agent Teams:** Launch multiple agents working in parallel on complex tasks

### Agent Roster

See [ROSTER.md](ROSTER.md) for the full directory of 18 agents across 6 domains:

| Domain | Agents | Lead |
|--------|--------|------|
| Aerospace | Miles, Nash, Cole | Miles (Opus) |
| Software Dev | Max, Sam, Lena, Kit, Dash, Ward | Max (Opus) |
| Research | Sage, Reed | Sage (Sonnet) |
| Game Dev | Drake, Cody | Drake (Opus) |
| iOS Dev | Logan, Maya | Logan (Opus) |
| Financial | Blake, Kai, Finn | Blake (Opus) |

## Architecture

```
agent-souls/
├── CLAUDE.md                    # Claude Code integration instructions
├── AGENTS.md                    # Cross-tool compatibility (Gemini, Cursor)
├── GENERAL_RULES.md             # The Constitution — rules all agents follow
├── ROSTER.md                    # Agent directory and summoning protocol
├── agents/                      # Agent definitions (portable format)
│   ├── aerospace/
│   │   ├── miles/
│   │   │   ├── SOUL.md          # Identity, rules, personality
│   │   │   ├── cheatsheets/     # Distilled domain knowledge
│   │   │   ├── references/      # Source materials (PDFs, papers)
│   │   │   └── memory/          # Session logs, mistakes, decisions
│   │   ├── nash/
│   │   └── cole/
│   ├── software-dev/            # 6 agents: max, sam, lena, kit, dash, ward
│   ├── research/                # 2 agents: sage, reed
│   ├── game-dev/                # 2 agents: drake, cody
│   ├── ios-dev/                 # 2 agents: logan, maya
│   └── financial/               # 3 agents: blake, kai, finn
├── shared-knowledge/            # Cross-agent shared context
├── templates/                   # Templates for new agents/cheatsheets
└── .claude/
    ├── agents/                  # Native Claude Code agent wrappers
    ├── commands/                # Custom slash commands (/summon, /session-end, /learn)
    └── settings.json            # Hooks and configuration
```

## How It Works

### The Soul System

Each agent has a `SOUL.md` that defines:
- **Identity** — name, role, model tier, seniority
- **Personality** — specific working style and approach
- **Hard Rules** — inviolable constraints (e.g., "never assume symmetric flow")
- **Expertise** — what the agent knows deeply
- **Collaboration** — who to delegate to, who to defer to

### The Knowledge System

Agents build **cheatsheets** — compressed, actionable reference files created from studying source materials. Each cheatsheet:
- Covers one topic (max ~500 lines)
- Includes confidence levels: `[VERIFIED]` `[TEXTBOOK]` `[DERIVED]` `[UNCERTAIN]`
- Has quick-reference tables, WARNING blocks, and worked EXAMPLES
- Is indexed in `_index.md` for progressive disclosure

### The Memory System

Agents maintain three memory files:
- `session-log.md` — what happened in each session
- `mistakes.md` — errors made, root causes, and prevention rules
- `decisions.md` — key technical decisions and their rationale

### Progressive Disclosure

To save context window space, agents don't load everything at startup. They:
1. Always load: SOUL.md, mistakes.md, cheatsheets/_index.md
2. Load on demand: individual cheatsheets relevant to the current task
3. Never load: raw references (those get distilled into cheatsheets)

## Adding a New Agent

1. Copy `templates/SOUL-TEMPLATE.md` to `agents/[domain]/[agent-name]/SOUL.md`
2. Fill in identity, rules, expertise, and collaboration fields
3. Create `cheatsheets/_index.md` (empty index)
4. Create `memory/session-log.md`, `mistakes.md`, `decisions.md` (from templates)
5. Create `.claude/agents/[agent-name].md` wrapper (see existing examples)
6. Add the agent to `ROSTER.md`

## Using as Git Submodule

For any project that wants to use these agents:

```bash
# Add as submodule
git submodule add https://github.com/sezersivri/agent-souls.git .agents

# Update to latest
git submodule update --remote .agents
```

In your project's `CLAUDE.md`:
```markdown
## Agent Team
This project uses the agent-souls system. See `.agents/CLAUDE.md` for instructions.
When a task requires specialized knowledge, summon the appropriate agent from `.agents/ROSTER.md`.
```

## Custom Commands

- `/summon <agent-name>` — Load an agent's full context and identity
- `/session-end` — Execute the mandatory Session End Protocol
- `/learn <source>` — Study source material and distill into cheatsheets

## Cross-Tool Compatibility

This system works with:
- **Claude Code** — native integration via `.claude/agents/`
- **Gemini CLI** — via `AGENTS.md` standard
- **Cursor** — via `.cursorrules` referencing agent files
- **Codex** — via `AGENTS.md` standard

See [AGENTS.md](AGENTS.md) for cross-tool setup.
