#!/usr/bin/env python3
"""Generate Claude Code agent wrappers and cross-tool skill files from manifest.json.

Usage:
    python generate-tool-configs.py          # Generate all files
    python generate-tool-configs.py --check  # Verify committed files match (exits non-zero on drift)

AUTO-GENERATED files produced:
    .claude/agents/{slug}.md   — Claude Code agent wrappers
    .agents/skills/{slug}/SKILL.md — Cross-tool skill files

Requirements: Python 3.10+, no external dependencies.
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure scripts/ is on sys.path for sibling imports
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from templates import render_claude_agent, render_skill, sort_agents

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


def write_file(path: Path, content: str) -> bool:
    """Write content to path, creating parent dirs. Returns True if file changed."""
    path.parent.mkdir(parents=True, exist_ok=True)
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

    repo_root = _SCRIPT_DIR.parent

    if args.check:
        do_check(repo_root)
    else:
        do_generate(repo_root)


if __name__ == "__main__":
    main()
