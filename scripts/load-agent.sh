#!/usr/bin/env bash
#
# load-agent.sh — Assemble full agent context and output to stdout.
#
# Usage:
#   ./scripts/load-agent.sh <agent-slug>                  # Text (Markdown) output
#   ./scripts/load-agent.sh <agent-slug> --format text    # Explicit text output
#   ./scripts/load-agent.sh <agent-slug> --format json    # JSON output
#
# Requires: Python 3 (for JSON parsing of manifest.json)

set -euo pipefail

# ── Resolve repo root from script location ──────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Parse arguments ──────────────────────────────────────────────────────────
AGENT_SLUG=""
FORMAT="text"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --format)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --format requires a value (text or json)" >&2
                exit 1
            fi
            FORMAT="$2"
            shift 2
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            echo "Usage: $0 <agent-slug> [--format text|json]" >&2
            exit 1
            ;;
        *)
            if [[ -z "$AGENT_SLUG" ]]; then
                AGENT_SLUG="$1"
            else
                echo "Error: Unexpected argument '$1'" >&2
                echo "Usage: $0 <agent-slug> [--format text|json]" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [[ -z "$AGENT_SLUG" ]]; then
    echo "Error: Agent slug is required." >&2
    echo "Usage: $0 <agent-slug> [--format text|json]" >&2
    exit 1
fi

if [[ "$FORMAT" != "text" && "$FORMAT" != "json" ]]; then
    echo "Error: Format must be 'text' or 'json', got '$FORMAT'" >&2
    exit 1
fi

# ── Locate manifest ──────────────────────────────────────────────────────────
MANIFEST="$REPO_ROOT/agents/manifest.json"
if [[ ! -f "$MANIFEST" ]]; then
    echo "Error: manifest.json not found at $MANIFEST" >&2
    exit 1
fi

# ── Extract paths from manifest using Python ─────────────────────────────────
# Convert to native path for Python on Windows (cygpath available in Git Bash)
MANIFEST_NATIVE="$MANIFEST"
if command -v cygpath &>/dev/null; then
    MANIFEST_NATIVE="$(cygpath -w "$MANIFEST")"
fi

AGENT_PATHS="$(python -c "
import json, sys, os

manifest_path = sys.argv[1]
agent_slug = sys.argv[2]

with open(manifest_path, 'r') as f:
    manifest = json.load(f)

for agent in manifest['agents']:
    if agent['slug'] == agent_slug:
        p = agent['paths']
        print(p['core'])
        print(p['mistakes'])
        print(p['cheatsheet_index'])
        sys.exit(0)

print('NOT_FOUND', file=sys.stderr)
sys.exit(1)
" "$MANIFEST_NATIVE" "$AGENT_SLUG" 2>&1)" || {
    echo "Error: Agent '$AGENT_SLUG' not found in manifest.json" >&2
    exit 1
}

# Parse the three lines
CORE_PATH="$(echo "$AGENT_PATHS" | sed -n '1p')"
MISTAKES_PATH="$(echo "$AGENT_PATHS" | sed -n '2p')"
INDEX_PATH="$(echo "$AGENT_PATHS" | sed -n '3p')"

# ── Resolve file paths relative to repo root ─────────────────────────────────
GENERAL_RULES_FILE="$REPO_ROOT/GENERAL_RULES.md"
CORE_FILE="$REPO_ROOT/$CORE_PATH"
MISTAKES_FILE="$REPO_ROOT/$MISTAKES_PATH"
INDEX_FILE="$REPO_ROOT/$INDEX_PATH"

# ── Validate all required files exist ─────────────────────────────────────────
missing=false

if [[ ! -f "$GENERAL_RULES_FILE" ]]; then
    echo "Error: GENERAL_RULES.md not found at $GENERAL_RULES_FILE" >&2
    missing=true
fi
if [[ ! -f "$CORE_FILE" ]]; then
    echo "Error: CORE.md not found at $CORE_FILE" >&2
    missing=true
fi
if [[ ! -f "$MISTAKES_FILE" ]]; then
    echo "Error: mistakes.md not found at $MISTAKES_FILE" >&2
    missing=true
fi
if [[ ! -f "$INDEX_FILE" ]]; then
    echo "Error: _index.md not found at $INDEX_FILE" >&2
    missing=true
fi

if $missing; then
    exit 1
fi

# ── Read file contents ───────────────────────────────────────────────────────
GENERAL_RULES="$(cat "$GENERAL_RULES_FILE")"
CORE="$(cat "$CORE_FILE")"
MISTAKES="$(cat "$MISTAKES_FILE")"
CHEATSHEET_INDEX="$(cat "$INDEX_FILE")"

# ── Output ───────────────────────────────────────────────────────────────────
if [[ "$FORMAT" == "text" ]]; then
    cat <<TEXTEOF
=== GENERAL RULES ===
${GENERAL_RULES}

=== CORE ===
${CORE}

=== MISTAKES ===
${MISTAKES}

=== CHEATSHEET INDEX ===
${CHEATSHEET_INDEX}
TEXTEOF
elif [[ "$FORMAT" == "json" ]]; then
    python -c "
import json, sys

data = {
    'general_rules': sys.stdin.read()
}
" <<< "" >/dev/null 2>&1 || true  # just test python is available

    # Convert paths for Python on Windows
    GR_NATIVE="$GENERAL_RULES_FILE"
    CORE_NATIVE="$CORE_FILE"
    MIST_NATIVE="$MISTAKES_FILE"
    IDX_NATIVE="$INDEX_FILE"
    if command -v cygpath &>/dev/null; then
        GR_NATIVE="$(cygpath -w "$GENERAL_RULES_FILE")"
        CORE_NATIVE="$(cygpath -w "$CORE_FILE")"
        MIST_NATIVE="$(cygpath -w "$MISTAKES_FILE")"
        IDX_NATIVE="$(cygpath -w "$INDEX_FILE")"
    fi

    python -c "
import json, sys

output = {
    'general_rules': open(sys.argv[1], 'r').read(),
    'core': open(sys.argv[2], 'r').read(),
    'mistakes': open(sys.argv[3], 'r').read(),
    'cheatsheet_index': open(sys.argv[4], 'r').read()
}

print(json.dumps(output, indent=2))
" "$GR_NATIVE" "$CORE_NATIVE" "$MIST_NATIVE" "$IDX_NATIVE"
fi
