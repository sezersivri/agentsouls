# Contributing to Agent Souls

This guide covers how to improve the framework, write cheatsheets, extend cross-tool support, and maintain the repository.

## What We Accept

Agent Souls is an open-source **framework**. Contributions that improve the framework for everyone are welcome:

- Bug fixes in scripts (`validate.py`, `generate-tool-configs.py`, `update-indexes.sh`)
- New tool integrations (Cursor, Windsurf, etc.)
- Template improvements
- Documentation improvements
- Suggestions via GitHub Issues

## What We Don't Accept

**New agents.** Agents are personal — they should reflect your workflow, your conventions, and your domain expertise. Create them in your [private fork](docs/PRIVATE-SETUP.md), not as a PR to this repo.

## Requirements

- **Python >= 3.10** (no external dependencies needed)
- **Bash** (for update-indexes.sh)
- **Git** (for version control and submodule usage)

## Golden Rule: Generated Files Are Read-Only

The following files are auto-generated from `agents/manifest.json` and templates. Never edit them directly:

- `.claude/agents/*.md` -- Claude Code agent wrappers
- `.agents/skills/*/SKILL.md` -- Cross-tool skill files
- `.cursorrules` -- Cursor integration
- `.windsurfrules` -- Windsurf integration

To change these files, edit `agents/manifest.json` (or the templates in `scripts/templates.py`), then run the generator:

```bash
python scripts/generate-tool-configs.py
```

**Note:** Framework skills (`.claude/skills/`) are manually maintained, not generated. Per-agent skills (`.agents/skills/`) are auto-generated.

## Creating Agents (For Your Private Fork)

The steps below are for creating agents in **your own private repo**, not for PRs to this repository.

### Step 1: Create the CORE.md

Copy the template and fill in the agent's identity:

```bash
# Example: adding an agent named "Nova" in the "research" domain
mkdir -p agents/research/nova/{cheatsheets,memory}
cp templates/CORE-TEMPLATE.md agents/research/nova/CORE.md
```

Edit `agents/research/nova/CORE.md` and fill in all fields. The YAML frontmatter **must** include:

```yaml
---
agent_name: "Nova"
domain: "research"
role: "Data Scientist"
model: "sonnet"
version: "1.0"
last_updated: "YYYY-MM-DD"
created: "YYYY-MM-DD"
---
```

### Step 2: Create memory files

```bash
cp templates/session-log-template.md agents/research/nova/memory/session-log.md
cp templates/mistakes-template.md agents/research/nova/memory/mistakes.md
cp templates/decisions-template.md agents/research/nova/memory/decisions.md
```

After copying, open each file and replace `[Agent Name]` with your agent's actual name (e.g., "Nova").

### Step 3: Create the cheatsheet index

```bash
cp templates/cheatsheet-index-template.md agents/research/nova/cheatsheets/_index.md
```

Then replace `[Agent Name]` with your agent's name.

### Step 4: Add to manifest.json

Add a new entry to `agents/manifest.json` in the `agents` array:

```json
{
  "name": "Nova",
  "slug": "nova",
  "domain": "research",
  "role": "Data Scientist",
  "description": "Data scientist responsible for statistical analysis, ML pipelines, and data visualization.",
  "model": "sonnet",
  "capabilities": ["python", "pandas", "scikit-learn", "jupyter"],
  "tags": ["specialist", "research"],
  "skills": ["session-end", "learn"],
  "paths": {
    "core": "agents/research/nova/CORE.md",
    "cheatsheets": "agents/research/nova/cheatsheets/",
    "cheatsheet_index": "agents/research/nova/cheatsheets/_index.md",
    "memory": "agents/research/nova/memory/",
    "mistakes": "agents/research/nova/memory/mistakes.md",
    "session_log": "agents/research/nova/memory/session-log.md",
    "decisions": "agents/research/nova/memory/decisions.md"
  },
  "delegates_to": [],
  "defers_to": ["sage"],
  "escalates_to": ["sage"]
}
```

#### v2.0 Manifest Fields

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `skills` | `string[]` | `[]` | Pre-load framework skills (e.g. `["session-end", "learn"]`) |
| `tools` | `string[]` or `null` | `null` (all) | Restrict which tools the agent can use |
| `permissionMode` | `string` | `"default"` | Permission mode: `default`, `plan`, `acceptEdits`, `bypassPermissions` |

All v2.0 fields are optional and default to v1.0 behavior if omitted.

### Step 5: Run the generator

```bash
python scripts/generate-tool-configs.py
```

This creates:
- `.claude/agents/nova.md` -- Claude Code agent wrapper
- `.agents/skills/nova/SKILL.md` -- Cross-tool skill file

### Step 6: Update indexes

```bash
bash scripts/update-indexes.sh
```

### Step 7: Add to ROSTER.md

Manually add the agent to the appropriate domain section in `ROSTER.md`.

### Step 8: Validate

```bash
python scripts/validate.py
```

All checks should pass before committing.

### Step 9: Commit

```bash
git add .
git commit -m "[nova] init: add Data Scientist agent"
```

## Writing a Cheatsheet

### Use the template

```bash
cp templates/cheatsheet-template.md agents/research/nova/cheatsheets/pandas-patterns.md
```

### Frontmatter requirements

Every cheatsheet **must** have YAML frontmatter:

```yaml
---
topic: "Pandas Patterns"
agent: "nova"
confidence: "VERIFIED"
source: "pandas docs 2.x, personal experience"
last_updated: "2026-02-18"
version: "1.0"
---
```

### Confidence levels

| Level | Meaning |
|-------|---------|
| `VERIFIED` | Tested and confirmed in practice |
| `TEXTBOOK` | From authoritative reference, not yet personally verified |
| `DERIVED` | Inferred from first principles or multiple sources |
| `UNCERTAIN` | Reasonable but not yet validated |

### Size limits

- Maximum ~500 lines per cheatsheet
- If a cheatsheet grows beyond this, split it into focused sub-topics
- One topic per file, use kebab-case filenames (e.g., `pandas-patterns.md`)

### After creating/updating a cheatsheet

Always regenerate the index:

```bash
bash scripts/update-indexes.sh
```

## Creating Framework Skills

Framework skills live in `.claude/skills/{skill-name}/SKILL.md`. They are manually maintained (not auto-generated).

### Skill structure

```
.claude/skills/my-skill/
└── SKILL.md
```

### SKILL.md format

Every skill must have YAML frontmatter:

```yaml
---
name: my-skill
description: Short description of what this skill does
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---
```

- `name`: Matches the directory name
- `description`: Shown in the skill list
- `allowed-tools`: Restricts which tools the skill can use

Use `$ARGUMENTS` in the skill body to accept user input (e.g., `/learn <source>` passes `<source>` as `$ARGUMENTS`).

### After creating a skill

1. Add the skill name to relevant agents' `skills` array in `manifest.json`
2. Regenerate wrappers: `python scripts/generate-tool-configs.py`
3. Run validation: `python scripts/validate.py` (check `skills-validation` validates skill frontmatter, check `v2-fields` validates skill refs)

## Adding Cross-Tool Support for a New CLI Tool

The agentsouls system is designed for multi-tool compatibility. To add support for a new AI coding tool:

### Step 1: Identify the tool's context mechanism

Each tool has a different way of loading context:

| Tool | Context file | Agent integration |
|------|-------------|-------------------|
| Claude Code | `CLAUDE.md` | `.claude/agents/*.md` (native) |
| Gemini CLI | `AGENTS.md` or `contextFileName` setting | `.agents/skills/*/SKILL.md` |
| Codex | `AGENTS.md` | `.agents/skills/*/SKILL.md` |
| Cursor | `.cursorrules` | Reference agent files directly |

### Step 2: Add a template to generate-tool-configs.py

If the new tool needs generated wrapper files (like Claude Code's `.claude/agents/` or the `.agents/skills/` directory):

1. Add a new template constant or render function to `scripts/templates.py`
2. Add a new render function
3. Add the file generation to the `generate()` function
4. Update this document

### Step 3: Create a tool-specific integration guide

Create a `TOOLNAME.md` at the repo root (e.g., `GEMINI.md`, `CURSOR.md`) explaining how to use agentsouls with that tool.

### Step 4: Update README.md

Add the new tool to the Cross-Tool Compatibility section.

## Schema Version Rules

The `schema_version` field in `agents/manifest.json` tracks the structure of the manifest.

### When to bump the version

- **Minor bump** (e.g., 1.0 -> 1.1): Adding optional fields, backward-compatible changes
- **Major bump** (e.g., 1.0 -> 2.0): Removing fields, renaming fields, changing field semantics

### Migration requirement

Any PR that changes `schema_version` **must** include one of:

1. A migration script or migration instructions in the PR description
2. An explicit statement: "No migration needed -- this change is purely additive"

This ensures that forks and submodule users can upgrade smoothly.

## Rollback Instructions

If a commit group introduces a failure (CI fails, validation breaks):

1. **Revert only that commit group** -- do not manually patch generated files
2. Run `python scripts/validate.py` to confirm the revert fixed the issue
3. Fix the root cause in `agents/manifest.json` or templates
4. Re-run the generator and commit the fix

Never manually edit generated files to fix a broken state. Always fix the source (manifest + templates) and regenerate.

## PR Process

### Before opening a PR

1. Run all validation: `python scripts/validate.py`
2. Check generated file drift: `python scripts/generate-tool-configs.py --check`
3. Check index accuracy: `bash scripts/update-indexes.sh --check`

### PR checklist

- [ ] `python scripts/validate.py` passes with all checks green
- [ ] Generated files are in sync (`python scripts/generate-tool-configs.py --check` exits 0)
- [ ] Index files are accurate (`bash scripts/update-indexes.sh --check` exits 0)
- [ ] If changing schema_version: migration instructions provided
- [ ] Commit messages follow the format: `[agent-name] [action]: [description]`
- [ ] If adding a framework skill: SKILL.md has valid frontmatter
- [ ] If adding v2.0 fields: values are within the valid set (see CONTRIBUTING.md)
