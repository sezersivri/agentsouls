#!/usr/bin/env python3
"""Generate Claude Code agent wrappers and cross-tool skill files from manifest.json.

Usage:
    python generate-tool-configs.py          # Generate all files
    python generate-tool-configs.py --check  # Verify committed files match (exits non-zero on drift)

AUTO-GENERATED files produced:
    .claude/agents/{slug}.md   — Claude Code agent wrappers (18 files)
    .agents/skills/{slug}/SKILL.md — Cross-tool skill files (18 files)

Requirements: Python 3.10+, no external dependencies.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

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

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

CLAUDE_AGENT_TEMPLATE = """\
<!-- AUTO-GENERATED from agents/manifest.json — DO NOT EDIT MANUALLY -->
<!-- generated_by: generate-tool-configs.py | schema: {schema_version} -->
---
model: "{model}"
---

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

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_manifest(repo_root: Path) -> dict:
    """Load and return the parsed manifest.json."""
    manifest_path = repo_root / "agents" / "manifest.json"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def sort_agents(agents: list[dict]) -> list[dict]:
    """Sort agents by domain (fixed order) then by name within domain."""
    domain_rank = {d: i for i, d in enumerate(DOMAIN_SORT_ORDER)}
    return sorted(
        agents,
        key=lambda a: (domain_rank.get(a["domain"], 999), a["name"].lower()),
    )


def lower_no_trailing_period(text: str) -> str:
    """Lowercase the first character and strip trailing period."""
    if not text:
        return text
    result = text[0].lower() + text[1:]
    if result.endswith("."):
        result = result[:-1]
    return result


def build_delegates_sentence(agent: dict) -> str:
    """Build the delegates_to sentence fragment (with leading space) or empty string."""
    delegates = agent.get("delegates_to", [])
    if not delegates:
        return ""
    # Capitalise delegate slugs for display
    names = [d.capitalize() for d in delegates]
    return f" {agent['name']} delegates to {', '.join(names)}."


def render_claude_agent(agent: dict, schema_version: str) -> str:
    """Render a .claude/agents/{slug}.md file."""
    return CLAUDE_AGENT_TEMPLATE.format(
        schema_version=schema_version,
        model=agent["model"],
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
        capabilities=", ".join(agent["capabilities"]),
        description_lower=lower_no_trailing_period(agent["description"]),
        delegates_sentence=build_delegates_sentence(agent),
        core_path=agent["paths"]["core"],
        mistakes_path=agent["paths"]["mistakes"],
        cheatsheet_index_path=agent["paths"]["cheatsheet_index"],
    )


def write_file(path: Path, content: str) -> bool:
    """Write content to path, creating parent dirs. Returns True if file changed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Check if content is already identical (for idempotency reporting)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def generate(repo_root: Path, output_root: Path) -> list[tuple[str, str]]:
    """Generate all files under output_root. Returns list of (relative_path, content)."""
    manifest = load_manifest(repo_root)
    schema_version = manifest["schema_version"]
    agents = sort_agents(manifest["agents"])

    generated: list[tuple[str, str]] = []

    for agent in agents:
        slug = agent["slug"]

        # Claude Code agent wrapper
        claude_rel = f".claude/agents/{slug}.md"
        claude_content = render_claude_agent(agent, schema_version)
        generated.append((claude_rel, claude_content))

        # Cross-tool skill file
        skill_rel = f".agents/skills/{slug}/SKILL.md"
        skill_content = render_skill(agent, schema_version)
        generated.append((skill_rel, skill_content))

    return generated


def do_generate(repo_root: Path) -> None:
    """Generate all files in-place under repo_root."""
    files = generate(repo_root, repo_root)
    created = 0
    unchanged = 0
    updated = 0

    for rel_path, content in files:
        full_path = repo_root / rel_path
        if not full_path.exists():
            write_file(full_path, content)
            created += 1
        else:
            changed = write_file(full_path, content)
            if changed:
                updated += 1
            else:
                unchanged += 1

    total = len(files)
    print(f"Generated {total} files ({created} created, {updated} updated, {unchanged} unchanged)")
    print(f"  - .claude/agents/*.md: {total // 2} files")
    print(f"  - .agents/skills/*/SKILL.md: {total // 2} files")


def do_check(repo_root: Path) -> None:
    """Check that committed files match what would be generated. Exit non-zero on drift."""
    files = generate(repo_root, repo_root)
    drift_count = 0
    missing_count = 0
    ok_count = 0

    for rel_path, expected_content in files:
        full_path = repo_root / rel_path
        if not full_path.exists():
            print(f"  MISSING: {rel_path}")
            missing_count += 1
        else:
            actual = full_path.read_text(encoding="utf-8")
            if actual != expected_content:
                print(f"  DRIFT:   {rel_path}")
                drift_count += 1
            else:
                ok_count += 1

    total = len(files)
    print(f"Checked {total} files: {ok_count} ok, {drift_count} drifted, {missing_count} missing")

    if drift_count > 0 or missing_count > 0:
        print("FAIL: Generated files are out of sync with manifest.json")
        print("Run: python scripts/generate-tool-configs.py")
        sys.exit(1)
    else:
        print("OK: All generated files match manifest.json")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate agent wrapper and skill files from manifest.json"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify committed files match generated output (exits non-zero on drift)",
    )
    args = parser.parse_args()

    # REPO_ROOT = parent of the directory containing this script
    # Script is at scripts/generate-tool-configs.py, so repo root is one level up from scripts/
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    if args.check:
        do_check(repo_root)
    else:
        do_generate(repo_root)


if __name__ == "__main__":
    main()
