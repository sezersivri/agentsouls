#!/usr/bin/env python3
"""One-off migration: add YAML frontmatter to cheatsheets that lack it.

Usage:
    python scripts/migrate_frontmatter.py          # Dry run (report only)
    python scripts/migrate_frontmatter.py --write  # Write changes to disk

Frontmatter added:
    topic: <extracted from first H1 heading, or kebab-to-title from filename>
    confidence: TEXTBOOK
    last_updated: <today>
    source: training-session

Cheatsheets that already have frontmatter are skipped unchanged.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent

try:
    import json
    manifest_path = _REPO_ROOT / "agents" / "manifest.json"
    _MANIFEST = json.loads(manifest_path.read_text(encoding="utf-8"))
except Exception as e:
    print(f"Error loading manifest: {e}", file=sys.stderr)
    sys.exit(1)


def has_frontmatter(text: str) -> bool:
    """Return True if the text begins with a YAML frontmatter block."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            return True
    return False


def extract_title(text: str, filename: str) -> str:
    """Extract topic from first H1 heading, or fall back to filename."""
    for line in text.split("\n"):
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    # Fallback: kebab-to-title
    name = filename.removesuffix(".md")
    return " ".join(word.capitalize() for word in name.split("-"))


def build_frontmatter(topic: str) -> str:
    today = date.today().strftime("%Y-%m-%d")
    return f"---\ntopic: \"{topic}\"\nconfidence: TEXTBOOK\nlast_updated: \"{today}\"\nsource: training-session\n---\n\n"


def migrate(write: bool) -> int:
    migrated = 0
    skipped = 0

    for agent in _MANIFEST["agents"]:
        slug = agent["slug"]
        cs_dir = _REPO_ROOT / agent["paths"]["cheatsheets"]
        if not cs_dir.is_dir():
            continue

        for md_file in sorted(cs_dir.iterdir()):
            if not md_file.is_file() or md_file.suffix != ".md" or md_file.name == "_index.md":
                continue

            try:
                text = md_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError) as e:
                print(f"  [ERROR] {md_file.relative_to(_REPO_ROOT)}: {e}")
                continue

            if has_frontmatter(text):
                skipped += 1
                continue

            topic = extract_title(text, md_file.name)
            fm = build_frontmatter(topic)
            new_text = fm + text

            rel = md_file.relative_to(_REPO_ROOT)
            if write:
                md_file.write_text(new_text, encoding="utf-8")
                print(f"  [MIGRATED] {rel} — topic: {topic!r}")
            else:
                print(f"  [DRY RUN]  {rel} — would add frontmatter, topic: {topic!r}")
            migrated += 1

    print()
    print(f"Result: {migrated} migrated, {skipped} already had frontmatter")
    if not write and migrated > 0:
        print("Run with --write to apply changes.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate cheatsheet frontmatter")
    parser.add_argument("--write", action="store_true", help="Write changes to disk (default: dry run)")
    args = parser.parse_args()

    print(f"Scanning cheatsheets in: {_REPO_ROOT}")
    print()
    sys.exit(migrate(write=args.write))


if __name__ == "__main__":
    main()
