#!/usr/bin/env python3
"""Validate the agentsouls repository structure, manifests, and generated files.

Usage:
    python scripts/validate.py          # Run all checks, exit non-zero on any FAIL
    python scripts/validate.py --check  # Same as above (read-only mode is default)
    python scripts/validate.py --fix    # Auto-fix safe issues (_index.md regeneration only)

Checks performed:
    1.  Manifest validation (schema, required fields)
    2.  Path resolution (all manifest paths exist)
    3.  CORE.md frontmatter (required YAML fields)
    4.  Cheatsheet frontmatter (warning if missing)
    5.  _index.md accuracy (matches actual cheatsheet files)
    6.  UTF-8 validation (all .md files)
    7.  Generated file drift (.claude/agents/*.md, .agents/skills/*/SKILL.md)
    8.  Memory file structure (session-log.md, mistakes.md, decisions.md)
    9.  Skills validation (framework skills exist with valid frontmatter)
    10. v2 fields (skills refs resolve; optional field values valid when present)

Requirements: Python 3.10+, no external dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure scripts/ is on sys.path for sibling imports
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from templates import (
    VALID_ISOLATION_MODES,
    VALID_MEMORY_SCOPES,
    VALID_PERMISSION_MODES,
    render_claude_agent,
    render_skill,
    sort_agents,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_MANIFEST_FIELDS = [
    "name",
    "slug",
    "domain",
    "role",
    "description",
    "model",
]

REQUIRED_PATH_FIELDS = [
    "core",
    "cheatsheets",
    "cheatsheet_index",
    "memory",
    "mistakes",
    "session_log",
    "decisions",
]

REQUIRED_CORE_FRONTMATTER = ["agent_name", "domain", "role", "model"]

AUTO_GENERATED_HEADER = "<!-- AUTO-GENERATED from agents/manifest.json"

FRAMEWORK_SKILLS = ["summon", "session-end", "learn"]

# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

_results: list[tuple[str, str, str]] = []  # (status, check_name, message)


def record(status: str, check: str, message: str) -> None:
    """Record a check result."""
    _results.append((status, check, message))


def print_results() -> int:
    """Print all results and return exit code (0 = all pass, 1 = any FAIL)."""
    has_fail = False
    for status, check, message in _results:
        tag = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN"}.get(status, status)
        print(f"  [{tag}] {check}: {message}")
        if status == "FAIL":
            has_fail = True
    print()
    total = len(_results)
    passes = sum(1 for s, _, _ in _results if s == "PASS")
    fails = sum(1 for s, _, _ in _results if s == "FAIL")
    warns = sum(1 for s, _, _ in _results if s == "WARN")
    print(f"Summary: {total} checks — {passes} PASS, {fails} FAIL, {warns} WARN")
    return 1 if has_fail else 0


# ---------------------------------------------------------------------------
# YAML frontmatter parser (minimal, no external deps)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse YAML frontmatter between --- delimiters. Returns None if no frontmatter."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        match = re.match(r'^(\w[\w_-]*)\s*:\s*"?([^"]*)"?\s*$', line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return None  # Never found closing ---


# ---------------------------------------------------------------------------
# Index generation logic (mirrors update-indexes.sh)
# ---------------------------------------------------------------------------

def kebab_to_title(filename: str) -> str:
    """Convert a kebab-case .md filename to Title Case."""
    name = filename.removesuffix(".md")
    return " ".join(word.capitalize() for word in name.split("-"))


def build_index_content(cheatsheets_dir: Path) -> str:
    """Build the expected _index.md content for a cheatsheets directory."""
    md_files = sorted(
        f for f in cheatsheets_dir.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name != "_index.md"
    )

    if not md_files:
        return "# Cheatsheet Index\n\nNo cheatsheets yet.\n"

    rows: list[str] = []
    for cs_file in md_files:
        try:
            text = cs_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            text = ""

        fm = parse_frontmatter(text) if text else None
        if fm:
            topic = fm.get("topic", "") or ""
            confidence = fm.get("confidence", "") or "UNKNOWN"
            last_updated = fm.get("last_updated", "") or ""
        else:
            topic = ""
            confidence = "UNKNOWN"
            last_updated = ""

        # Fallback topic: first H1 heading
        if not topic:
            for line in text.split("\n"):
                m = re.match(r"^#\s+(.+)$", line)
                if m:
                    topic = m.group(1).strip()
                    break

        # Final fallback: kebab-to-title from filename
        if not topic:
            topic = kebab_to_title(cs_file.name)

        if not last_updated:
            try:
                import datetime
                mtime = cs_file.stat().st_mtime
                last_updated = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            except OSError:
                last_updated = "unknown"

        rows.append(f"| {cs_file.name} | {topic} | {confidence} | {last_updated} |")

    table = "\n".join(rows)
    return (
        "# Cheatsheet Index\n"
        "\n"
        "| Cheatsheet | Topic | Confidence | Last Updated |\n"
        "|------------|-------|------------|--------------|"
        "\n"
        f"{table}\n"
    )


# ---------------------------------------------------------------------------
# Generated file drift check
# ---------------------------------------------------------------------------

def generate_expected_files(manifest: dict) -> list[tuple[str, str]]:
    """Return list of (relative_path, expected_content) for all generated files."""
    schema_version = manifest["schema_version"]
    agents = sort_agents(manifest["agents"])
    files: list[tuple[str, str]] = []
    for agent in agents:
        slug = agent["slug"]
        files.append((f".claude/agents/{slug}.md", render_claude_agent(agent, schema_version)))
        files.append((f".agents/skills/{slug}/SKILL.md", render_skill(agent, schema_version)))
    return files


# ---------------------------------------------------------------------------
# Check implementations (1–8: existing, 9–12: new)
# ---------------------------------------------------------------------------

def check_manifest(repo_root: Path) -> dict | None:
    """Check 1: Manifest validation."""
    manifest_path = repo_root / "agents" / "manifest.json"

    if not manifest_path.exists():
        record("FAIL", "manifest-exists", "agents/manifest.json not found")
        return None

    try:
        text = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(text)
    except json.JSONDecodeError as e:
        record("FAIL", "manifest-json", f"Invalid JSON: {e}")
        return None
    except UnicodeDecodeError as e:
        record("FAIL", "manifest-utf8", f"Not valid UTF-8: {e}")
        return None

    if "schema_version" not in manifest:
        record("FAIL", "manifest-schema", "Missing 'schema_version' field")
        return None

    if "agents" not in manifest or not isinstance(manifest["agents"], list):
        record("FAIL", "manifest-agents", "Missing or invalid 'agents' array")
        return None

    all_ok = True
    for agent in manifest["agents"]:
        slug = agent.get("slug", agent.get("name", "UNKNOWN"))
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in agent:
                record("FAIL", "manifest-fields", f"Agent '{slug}' missing required field: {field}")
                all_ok = False

        paths = agent.get("paths", {})
        for pfield in REQUIRED_PATH_FIELDS:
            if pfield not in paths:
                record("FAIL", "manifest-paths", f"Agent '{slug}' missing paths.{pfield}")
                all_ok = False

    if all_ok:
        record("PASS", "manifest-validation", f"Valid manifest with {len(manifest['agents'])} agents")

    return manifest


def check_path_resolution(repo_root: Path, manifest: dict) -> None:
    """Check 2: All paths in manifest resolve to existing files/directories."""
    all_ok = True
    for agent in manifest["agents"]:
        slug = agent["slug"]
        paths = agent.get("paths", {})
        for key, rel_path in paths.items():
            full_path = repo_root / rel_path
            if rel_path.endswith("/"):
                if not full_path.is_dir():
                    record("FAIL", "path-resolution", f"Agent '{slug}': {key} directory not found: {rel_path}")
                    all_ok = False
            else:
                if not full_path.is_file():
                    record("FAIL", "path-resolution", f"Agent '{slug}': {key} file not found: {rel_path}")
                    all_ok = False

    if all_ok:
        record("PASS", "path-resolution", "All manifest paths resolve to existing files/directories")


def check_core_frontmatter(repo_root: Path, manifest: dict) -> None:
    """Check 3: Each CORE.md has required YAML frontmatter fields."""
    all_ok = True
    for agent in manifest["agents"]:
        slug = agent["slug"]
        core_path = repo_root / agent["paths"]["core"]
        if not core_path.is_file():
            continue

        try:
            text = core_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            record("FAIL", "core-frontmatter", f"Agent '{slug}': Cannot read CORE.md: {e}")
            all_ok = False
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            record("FAIL", "core-frontmatter", f"Agent '{slug}': CORE.md has no YAML frontmatter")
            all_ok = False
            continue

        for field in REQUIRED_CORE_FRONTMATTER:
            if field not in fm or not fm[field]:
                record("FAIL", "core-frontmatter", f"Agent '{slug}': CORE.md missing frontmatter field: {field}")
                all_ok = False

    if all_ok:
        record("PASS", "core-frontmatter", "All CORE.md files have required frontmatter")


def check_cheatsheet_frontmatter(repo_root: Path, manifest: dict) -> None:
    """Check 4: Cheatsheet .md files should have YAML frontmatter (WARN if missing)."""
    warn_count = 0
    total_checked = 0

    for agent in manifest["agents"]:
        slug = agent["slug"]
        cs_dir = repo_root / agent["paths"]["cheatsheets"]
        if not cs_dir.is_dir():
            continue

        for md_file in sorted(cs_dir.iterdir()):
            if not md_file.is_file() or md_file.suffix != ".md" or md_file.name == "_index.md":
                continue
            total_checked += 1

            try:
                text = md_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                warn_count += 1
                continue

            fm = parse_frontmatter(text)
            if fm is None:
                record(
                    "WARN",
                    "cheatsheet-frontmatter",
                    f"Agent '{slug}': {md_file.name} has no YAML frontmatter",
                )
                warn_count += 1

    if warn_count == 0:
        record("PASS", "cheatsheet-frontmatter", f"All {total_checked} cheatsheets have frontmatter")


def check_index_accuracy(repo_root: Path, manifest: dict, fix: bool) -> None:
    """Check 5: _index.md lists exactly the cheatsheet files present."""
    stale_count = 0
    fixed_count = 0
    total_checked = 0

    for agent in manifest["agents"]:
        slug = agent["slug"]
        cs_dir = repo_root / agent["paths"]["cheatsheets"]
        if not cs_dir.is_dir():
            continue

        total_checked += 1
        index_path = repo_root / agent["paths"]["cheatsheet_index"]
        expected = build_index_content(cs_dir)

        if not index_path.is_file():
            if fix:
                index_path.write_text(expected, encoding="utf-8")
                fixed_count += 1
            else:
                record("FAIL", "index-accuracy", f"Agent '{slug}': _index.md not found")
                stale_count += 1
            continue

        try:
            actual = index_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            stale_count += 1
            continue

        expected_files = set(re.findall(r"\|\s*(\S+\.md)\s*\|", expected))
        actual_files = set(re.findall(r"\|\s*`?(\S+\.md)`?\s*\|", actual))

        if expected_files != actual_files:
            if fix:
                index_path.write_text(expected, encoding="utf-8")
                fixed_count += 1
            else:
                missing = expected_files - actual_files
                extra = actual_files - expected_files
                details = []
                if missing:
                    details.append(f"missing: {', '.join(sorted(missing))}")
                if extra:
                    details.append(f"extra: {', '.join(sorted(extra))}")
                record(
                    "FAIL",
                    "index-accuracy",
                    f"Agent '{slug}': _index.md file list mismatch ({'; '.join(details)})",
                )
                stale_count += 1

    if fix and fixed_count > 0:
        record("PASS", "index-accuracy", f"Fixed {fixed_count} _index.md files")
    elif stale_count == 0:
        record("PASS", "index-accuracy", f"All {total_checked} _index.md files are accurate")


def check_utf8(repo_root: Path) -> None:
    """Check 6: All .md files are valid UTF-8."""
    bad_files: list[str] = []
    total = 0

    for md_file in repo_root.rglob("*.md"):
        parts = md_file.relative_to(repo_root).parts
        if ".git" in parts:
            continue
        if "node_modules" in parts:
            continue

        total += 1
        try:
            md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            rel = md_file.relative_to(repo_root)
            bad_files.append(str(rel))

    if bad_files:
        for f in bad_files:
            record("FAIL", "utf8-validation", f"Invalid UTF-8: {f}")
    else:
        record("PASS", "utf8-validation", f"All {total} .md files are valid UTF-8")


def check_generated_drift(repo_root: Path, manifest: dict) -> None:
    """Check 7: Generated files match what manifest would produce."""
    expected_files = generate_expected_files(manifest)
    drift_count = 0
    missing_count = 0

    for rel_path, expected_content in expected_files:
        full_path = repo_root / rel_path
        if not full_path.exists():
            record("FAIL", "generated-drift", f"Missing generated file: {rel_path}")
            missing_count += 1
            continue

        try:
            actual = full_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            record("FAIL", "generated-drift", f"Cannot read {rel_path}: {e}")
            drift_count += 1
            continue

        if AUTO_GENERATED_HEADER not in actual:
            record("FAIL", "generated-drift", f"Missing AUTO-GENERATED header: {rel_path}")
            drift_count += 1
            continue

        if actual != expected_content:
            record("FAIL", "generated-drift", f"Content drift detected: {rel_path}")
            drift_count += 1

    total = len(expected_files)
    if drift_count == 0 and missing_count == 0:
        record("PASS", "generated-drift", f"All {total} generated files match manifest")


def check_memory_structure(repo_root: Path, manifest: dict) -> None:
    """Check 8: Memory files exist for each agent."""
    all_ok = True
    memory_files = ["session_log", "mistakes", "decisions"]

    for agent in manifest["agents"]:
        slug = agent["slug"]
        for mf in memory_files:
            rel_path = agent["paths"].get(mf, "")
            if not rel_path:
                record("FAIL", "memory-structure", f"Agent '{slug}': missing paths.{mf} in manifest")
                all_ok = False
                continue
            full_path = repo_root / rel_path
            if not full_path.is_file():
                record("FAIL", "memory-structure", f"Agent '{slug}': {mf} file not found: {rel_path}")
                all_ok = False

    if all_ok:
        record("PASS", "memory-structure", "All agents have required memory files")


def check_skills_validation(repo_root: Path) -> None:
    """Check 9: Framework skills exist with valid frontmatter."""
    all_ok = True

    for skill_name in FRAMEWORK_SKILLS:
        skill_path = repo_root / ".claude" / "skills" / skill_name / "SKILL.md"
        if not skill_path.is_file():
            record("FAIL", "skills-validation", f"Framework skill missing: .claude/skills/{skill_name}/SKILL.md")
            all_ok = False
            continue

        try:
            text = skill_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            record("FAIL", "skills-validation", f"Cannot read skill {skill_name}: {e}")
            all_ok = False
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            record("FAIL", "skills-validation", f"Skill '{skill_name}' has no YAML frontmatter")
            all_ok = False
            continue

        if "name" not in fm:
            record("FAIL", "skills-validation", f"Skill '{skill_name}' missing 'name' in frontmatter")
            all_ok = False
        if "description" not in fm:
            record("FAIL", "skills-validation", f"Skill '{skill_name}' missing 'description' in frontmatter")
            all_ok = False

    if all_ok:
        record("PASS", "skills-validation", f"All {len(FRAMEWORK_SKILLS)} framework skills valid")


def check_v2_fields(repo_root: Path, manifest: dict) -> None:
    """Check 10: v2.0 fields have valid values; skills refs resolve."""
    schema = manifest.get("schema_version", "1.0")
    if not schema.startswith("2"):
        record("PASS", "v2-fields", "Skipped (schema < 2.0)")
        return

    all_ok = True

    for agent in manifest["agents"]:
        slug = agent["slug"]

        # permissionMode
        perm = agent.get("permissionMode", "default")
        if perm not in VALID_PERMISSION_MODES:
            record("FAIL", "v2-fields", f"Agent '{slug}': invalid permissionMode '{perm}'")
            all_ok = False

        # tools — must be null or list of strings
        tools = agent.get("tools", None)
        if tools is not None and not isinstance(tools, list):
            record("FAIL", "v2-fields", f"Agent '{slug}': tools must be null or array")
            all_ok = False

        # memory
        mem = agent.get("memory", None)
        if mem not in VALID_MEMORY_SCOPES:
            record("FAIL", "v2-fields", f"Agent '{slug}': invalid memory scope '{mem}'")
            all_ok = False

        # isolation
        iso = agent.get("isolation", None)
        if iso not in VALID_ISOLATION_MODES:
            record("FAIL", "v2-fields", f"Agent '{slug}': invalid isolation mode '{iso}'")
            all_ok = False

        # skills — each ref must resolve to a framework skill
        skills = agent.get("skills", [])
        if not isinstance(skills, list):
            record("FAIL", "v2-fields", f"Agent '{slug}': skills must be an array")
            all_ok = False
        else:
            for skill_ref in skills:
                skill_path = repo_root / ".claude" / "skills" / skill_ref / "SKILL.md"
                if not skill_path.is_file():
                    record("FAIL", "v2-fields", f"Agent '{slug}': skill ref '{skill_ref}' does not resolve to .claude/skills/{skill_ref}/SKILL.md")
                    all_ok = False

    if all_ok:
        record("PASS", "v2-fields", "All v2.0 fields valid and skill refs resolve")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate agentsouls repository structure")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run all checks in read-only mode (default behavior)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix safe issues (only _index.md regeneration)",
    )
    args = parser.parse_args()

    repo_root = _SCRIPT_DIR.parent

    print(f"Validating agentsouls repository at: {repo_root}")
    print()

    # Check 1: Manifest validation
    manifest = check_manifest(repo_root)

    if manifest is None:
        print()
        exit_code = print_results()
        sys.exit(exit_code)

    # Check 2: Path resolution
    check_path_resolution(repo_root, manifest)

    # Check 3: CORE.md frontmatter
    check_core_frontmatter(repo_root, manifest)

    # Check 4: Cheatsheet frontmatter
    check_cheatsheet_frontmatter(repo_root, manifest)

    # Check 5: _index.md accuracy
    check_index_accuracy(repo_root, manifest, fix=args.fix)

    # Check 6: UTF-8 validation
    check_utf8(repo_root)

    # Check 7: Generated file drift
    check_generated_drift(repo_root, manifest)

    # Check 8: Memory file structure
    check_memory_structure(repo_root, manifest)

    # Check 9: Skills validation
    check_skills_validation(repo_root)

    # Check 10: v2 fields validation
    check_v2_fields(repo_root, manifest)

    print()
    exit_code = print_results()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
