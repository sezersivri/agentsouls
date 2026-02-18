---
description: "Coding and workflow conventions shared across all agents"
last_updated: "2026-02-18"
---

# Team Conventions

## Code Style

### Python
- Use `black` for formatting (line length 88)
- Use `ruff` for linting
- Type hints on all public function signatures
- Docstrings for public modules, classes, and functions (Google style)
- Import order: stdlib → third-party → local (enforced by `isort`)

### TypeScript/JavaScript
- Use `prettier` for formatting
- Use `eslint` with project config
- Prefer TypeScript over JavaScript for new code
- Use strict mode

### General
- Kebab-case for filenames
- Meaningful variable names — no single-letter names except loop counters
- Functions should do one thing
- Max function length: ~50 lines (guideline, not strict)

## Git Conventions

- Commit format: `[agent-name] [action]: brief description`
- One logical change per commit
- Never force-push
- Branch naming: `feature/description`, `fix/description`, `agent/agent-name/description`

## Testing

- Write tests before or alongside code, not after
- Test names describe behavior: `test_returns_error_when_input_is_negative`
- Minimum coverage: 80% for new code
- Run tests before committing

## Documentation

- README.md in every project root
- Inline comments only for non-obvious logic
- Cheatsheets for domain knowledge (not inline comments)

## File Organization

- One module per concern
- Group by feature, not by type (e.g., `auth/` not `controllers/`, `models/`, `views/`)
- Keep dependencies explicit
