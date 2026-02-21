"""Shared templates, constants, and helpers for agent file generation.

Used by both generate-tool-configs.py and validate.py to avoid duplication.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOMAIN_SORT_ORDER = [
    "aerospace",
    "financial",
    "game-dev",
    "ios-dev",
    "research",
    "software-dev",
]

# v2.0 field defaults — used to suppress default values in frontmatter
V2_FIELD_DEFAULTS = {
    "tools": None,
    "permissionMode": "default",
    "skills": [],
    "memory": None,
    "isolation": None,
}

VALID_PERMISSION_MODES = {"default", "plan", "bypassPermissions", "acceptEdits"}
VALID_MEMORY_SCOPES = {None, "user", "project", "local"}
VALID_ISOLATION_MODES = {None, "worktree"}

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

CLAUDE_AGENT_TEMPLATE = """\
<!-- AUTO-GENERATED from agents/manifest.json — DO NOT EDIT MANUALLY -->
<!-- generated_by: generate-tool-configs.py | schema: {schema_version} -->
---
{frontmatter}---

# {name} — {role}

{description}

## Activation

You are {name}. Follow this loading sequence:

1. Read `GENERAL_RULES.md`
2. Read `{core_path}`
3. Check `{mistakes_path}`
4. Scan `{cheatsheet_index_path}`
5. Load relevant cheatsheets as needed

When finishing work, follow the Session End Protocol in GENERAL_RULES.md.
"""

SKILL_TEMPLATE = """\
<!-- AUTO-GENERATED from agents/manifest.json — DO NOT EDIT MANUALLY -->
<!-- generated_by: generate-tool-configs.py | schema: {schema_version} -->

---
name: "{name}"
description: "{description}"
---

# {name} — {role}

**Domain:** {domain}
**Model tier:** {model}
**Capabilities:** {capabilities}

## When to Use

Summon {name} when you need help with {description_lower}.{delegates_sentence}

## Loading Sequence

1. Read `GENERAL_RULES.md` — universal rules for all agents
2. Read `{core_path}` — {name}'s identity and hard rules
3. Check `{mistakes_path}` — pitfalls to avoid
4. Scan `{cheatsheet_index_path}` — available knowledge
5. Load relevant cheatsheets for the current task (progressive disclosure)

## Session End

Before ending any session, {name} must follow the session-end protocol defined in `GENERAL_RULES.md`.
"""

# .cursorrules and .windsurfrules are repo-level files (not per-agent), so they
# take the full sorted agent list rather than a single agent dict.


def render_cursorrules(agents: list[dict], schema_version: str) -> str:
    """Render the .cursorrules file."""
    agent_lines: list[str] = []
    for a in agents:
        agent_lines.append(
            f"- **{a['name']}** ({a['role']}, {a['model']}): "
            f"@{a['paths']['core']}"
        )
    agent_block = "\n".join(agent_lines)

    return f"""\
# Agent Souls — Cursor Integration
# AUTO-GENERATED from agents/manifest.json — DO NOT EDIT MANUALLY
# generated_by: generate-tool-configs.py | schema: {schema_version}

This project uses the Agent Souls framework for persistent AI agent identities.
Read @GENERAL_RULES.md for the universal rules all agents follow.

## Available Agents

{agent_block}

## Loading an Agent

1. Read @GENERAL_RULES.md
2. Read the agent's CORE.md (paths listed above)
3. Check their memory/mistakes.md
4. Scan their cheatsheets/_index.md
5. Load relevant cheatsheets for the current task

## Session End

Before ending any session, follow the session-end protocol in @GENERAL_RULES.md:
update session-log.md, mistakes.md, decisions.md, and cheatsheets.
"""


def render_windsurfrules(agents: list[dict], schema_version: str) -> str:
    """Render the .windsurfrules file (kept concise due to 6K char limit)."""
    agent_lines: list[str] = []
    for a in agents:
        agent_lines.append(
            f"- {a['name']} ({a['role']}, {a['model']}): {a['paths']['core']}"
        )
    agent_block = "\n".join(agent_lines)

    return f"""\
# Agent Souls Framework
# AUTO-GENERATED from agents/manifest.json — DO NOT EDIT MANUALLY
# generated_by: generate-tool-configs.py | schema: {schema_version}

Persistent AI agent identities with knowledge and memory.
Rules: GENERAL_RULES.md

## Agents

{agent_block}

## Loading Sequence

1. Read GENERAL_RULES.md
2. Read the agent's CORE.md
3. Check memory/mistakes.md
4. Scan cheatsheets/_index.md
5. Load relevant cheatsheets

## Session End

Update session-log.md, mistakes.md, decisions.md, and cheatsheets before ending.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def lower_no_trailing_period(text: str) -> str:
    """Lowercase the first character and strip trailing period."""
    if not text:
        return text
    result = text[0].lower() + text[1:]
    return result.rstrip(".")


def build_delegates_sentence(agent: dict) -> str:
    """Build the delegates_to sentence fragment (with leading space) or empty string."""
    delegates = agent.get("delegates_to", [])
    if not delegates:
        return ""
    names = [d.capitalize() for d in delegates]
    return f" {agent['name']} delegates to {', '.join(names)}."


def sort_agents(agents: list[dict]) -> list[dict]:
    """Sort agents by domain (fixed order) then by name within domain."""
    domain_rank = {d: i for i, d in enumerate(DOMAIN_SORT_ORDER)}
    return sorted(
        agents,
        key=lambda a: (domain_rank.get(a["domain"], 999), a["name"].lower()),
    )


def build_frontmatter(agent: dict) -> str:
    """Build YAML frontmatter lines, only emitting non-null/non-default fields.

    Always emits: name, model, description.
    Conditionally emits: tools, permissionMode, skills, memory, isolation.
    """
    lines: list[str] = []

    # Always-present fields (unquoted for name/model, quoted for description)
    lines.append(f"name: {agent['slug']}")
    lines.append(f"model: {agent['model']}")
    lines.append(f'description: "{agent["description"]}"')

    # skills — emit as comma-separated if non-empty
    skills = agent.get("skills", V2_FIELD_DEFAULTS["skills"])
    if skills:
        lines.append(f"skills: {', '.join(skills)}")

    # tools — emit as comma-separated if not None
    tools = agent.get("tools", V2_FIELD_DEFAULTS["tools"])
    if tools is not None:
        lines.append(f"tools: {', '.join(tools)}")

    # permissionMode — emit only if not default
    perm = agent.get("permissionMode", V2_FIELD_DEFAULTS["permissionMode"])
    if perm != "default":
        lines.append(f"permissionMode: {perm}")

    # memory — emit only if not None
    mem = agent.get("memory", V2_FIELD_DEFAULTS["memory"])
    if mem is not None:
        lines.append(f"memory: {mem}")

    # isolation — emit only if not None
    iso = agent.get("isolation", V2_FIELD_DEFAULTS["isolation"])
    if iso is not None:
        lines.append(f"isolation: {iso}")

    return "\n".join(lines) + "\n"


def render_claude_agent(agent: dict, schema_version: str) -> str:
    """Render a .claude/agents/{slug}.md file."""
    return CLAUDE_AGENT_TEMPLATE.format(
        schema_version=schema_version,
        frontmatter=build_frontmatter(agent),
        name=agent["name"],
        role=agent["role"],
        description=agent["description"],
        core_path=agent["paths"]["core"],
        mistakes_path=agent["paths"]["mistakes"],
        cheatsheet_index_path=agent["paths"]["cheatsheet_index"],
    )


def render_skill(agent: dict, schema_version: str) -> str:
    """Render a .agents/skills/{slug}/SKILL.md file."""
    return SKILL_TEMPLATE.format(
        schema_version=schema_version,
        name=agent["name"],
        role=agent["role"],
        description=agent["description"],
        domain=agent["domain"],
        model=agent["model"],
        capabilities=", ".join(agent.get("capabilities", [])),
        description_lower=lower_no_trailing_period(agent["description"]),
        delegates_sentence=build_delegates_sentence(agent),
        core_path=agent["paths"]["core"],
        mistakes_path=agent["paths"]["mistakes"],
        cheatsheet_index_path=agent["paths"]["cheatsheet_index"],
    )
