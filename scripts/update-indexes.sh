#!/usr/bin/env bash
#
# update-indexes.sh — Regenerate _index.md for every agent's cheatsheets/ directory.
#
# Usage:
#   ./scripts/update-indexes.sh           # Update all _index.md files in-place
#   ./scripts/update-indexes.sh --check   # Exit non-zero if any _index.md is out of date
#
# Idempotent: running twice produces zero diff.

set -euo pipefail

# ── Resolve repo root from script location ──────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CHECK_MODE=false
if [[ "${1:-}" == "--check" ]]; then
    CHECK_MODE=true
fi

# ── Helpers ──────────────────────────────────────────────────────────────────

# Extract a YAML frontmatter field value from a file.
# Usage: extract_frontmatter_field <file> <field>
# Returns empty string if not found.
extract_frontmatter_field() {
    local file="$1"
    local field="$2"
    # Read between first --- pair, then grep for field
    local in_frontmatter=false
    local found_start=false
    while IFS= read -r line; do
        # Strip trailing CR for Windows/CRLF compatibility
        line="${line%$'\r'}"
        if [[ "$line" == "---" ]]; then
            if $found_start; then
                # End of frontmatter
                break
            else
                found_start=true
                continue
            fi
        fi
        if $found_start; then
            # Match field: "value" or field: value
            if [[ "$line" =~ ^${field}:[[:space:]]*\"(.*)\"$ ]]; then
                echo "${BASH_REMATCH[1]}"
                return
            elif [[ "$line" =~ ^${field}:[[:space:]]*(.+)$ ]]; then
                echo "${BASH_REMATCH[1]}"
                return
            fi
        fi
    done < "$file"
    echo ""
}

# Check if a file has YAML frontmatter (starts with ---)
has_frontmatter() {
    local file="$1"
    local first_line
    first_line="$(head -n 1 "$file")"
    # Strip trailing CR for Windows/CRLF compatibility
    first_line="${first_line%$'\r'}"
    [[ "$first_line" == "---" ]]
}

# Extract the first H1 heading from a file
extract_first_h1() {
    local file="$1"
    while IFS= read -r line; do
        if [[ "$line" =~ ^#[[:space:]]+(.+)$ ]]; then
            echo "${BASH_REMATCH[1]}"
            return
        fi
    done < "$file"
    echo ""
}

# Convert kebab-case filename to Title Case (strip .md extension)
kebab_to_title() {
    local name="$1"
    # Remove .md extension
    name="${name%.md}"
    # Replace hyphens with spaces, then title-case each word
    echo "$name" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1'
}

# Get file modification date in YYYY-MM-DD format
get_file_mod_date() {
    local file="$1"
    if [[ "$(uname -s)" == "Darwin" ]]; then
        stat -f "%Sm" -t "%Y-%m-%d" "$file"
    else
        stat -c "%y" "$file" | cut -d' ' -f1
    fi
}

# ── Main Logic ───────────────────────────────────────────────────────────────

updated_count=0
agents_with_cheatsheets=0
stale_count=0

# Find all cheatsheets/ directories under agents/
for cheatsheets_dir in "$REPO_ROOT"/agents/*/*/cheatsheets/; do
    # Skip if glob didn't match anything
    [[ -d "$cheatsheets_dir" ]] || continue

    index_file="${cheatsheets_dir}_index.md"

    # Collect cheatsheet .md files (exclude _index.md), sorted alphabetically
    cheatsheet_files=()
    while IFS= read -r -d '' f; do
        cheatsheet_files+=("$f")
    done < <(find "$cheatsheets_dir" -maxdepth 1 -name '*.md' ! -name '_index.md' -print0 | sort -z)

    # Build new index content
    if [[ ${#cheatsheet_files[@]} -eq 0 ]]; then
        # No cheatsheets — write stub message
        new_content="# Cheatsheet Index

No cheatsheets yet.
"
    else
        agents_with_cheatsheets=$((agents_with_cheatsheets + 1))

        # Build table rows
        table_rows=""
        for cs_file in "${cheatsheet_files[@]}"; do
            filename="$(basename "$cs_file")"

            if has_frontmatter "$cs_file"; then
                topic="$(extract_frontmatter_field "$cs_file" "topic")"
                confidence="$(extract_frontmatter_field "$cs_file" "confidence")"
                last_updated="$(extract_frontmatter_field "$cs_file" "last_updated")"

                # Fallback for topic: use first H1 if frontmatter field is empty
                if [[ -z "$topic" ]]; then
                    topic="$(extract_first_h1 "$cs_file")"
                fi
                # Final fallback: kebab-to-title from filename
                if [[ -z "$topic" ]]; then
                    topic="$(kebab_to_title "$filename")"
                fi
            else
                # No frontmatter at all
                topic="$(kebab_to_title "$filename")"
                confidence="UNKNOWN"
                last_updated="$(get_file_mod_date "$cs_file")"
            fi

            # Fallback confidence/last_updated if frontmatter had empty values
            if [[ -z "$confidence" ]]; then
                confidence="UNKNOWN"
            fi
            if [[ -z "$last_updated" ]]; then
                last_updated="$(get_file_mod_date "$cs_file")"
            fi

            table_rows="${table_rows}| ${filename} | ${topic} | ${confidence} | ${last_updated} |
"
        done

        new_content="# Cheatsheet Index

| Cheatsheet | Topic | Confidence | Last Updated |
|------------|-------|------------|--------------|
${table_rows}"
    fi

    # Compare with existing content using temp file (avoids trailing newline issues)
    tmp_file="$(mktemp)"
    printf '%s' "$new_content" > "$tmp_file"

    files_differ=true
    if [[ -f "$index_file" ]] && diff -q "$tmp_file" "$index_file" > /dev/null 2>&1; then
        files_differ=false
    fi

    if $files_differ; then
        if $CHECK_MODE; then
            # Derive a display-friendly agent path
            relative="${cheatsheets_dir#"$REPO_ROOT"/}"
            echo "STALE: ${relative}_index.md"
            stale_count=$((stale_count + 1))
        else
            printf '%s' "$new_content" > "$index_file"
            updated_count=$((updated_count + 1))
        fi
    fi

    rm -f "$tmp_file"
done

# ── Summary ──────────────────────────────────────────────────────────────────

if $CHECK_MODE; then
    if [[ $stale_count -gt 0 ]]; then
        echo ""
        echo "${stale_count} index file(s) are out of date. Run ./scripts/update-indexes.sh to fix."
        exit 1
    else
        echo "All index files are up to date."
        exit 0
    fi
else
    echo "Updated ${updated_count} index files, ${agents_with_cheatsheets} agents have cheatsheets"
fi
