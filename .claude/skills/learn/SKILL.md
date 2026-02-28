---
name: learn
description: Execute the Knowledge Consumption Protocol for the currently active agent
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Execute the Knowledge Consumption Protocol for the currently active agent.

The agent should study the provided source material and distill it into cheatsheets.

Source to study: $ARGUMENTS

Examples:
- `/learn agents/aerospace/miles/cheatsheets/stability-derivatives.md` — distill an existing file
- `/learn https://example.com/docs` — distill a URL (fetch first, then process)
- `/learn "React hooks best practices"` — research a topic and create a cheatsheet

**Source hierarchy:** Prefer official documentation (HIGH → `[VERIFIED]`) over multiple independent web sources (MEDIUM → `[TEXTBOOK]`/`[DERIVED]`) over single-source or training knowledge (LOW → `[UNCERTAIN]`, flag explicitly). Disclose the tier in your cheatsheet frontmatter.

Steps:
1. Read the source material carefully. If the source contains stubs, TODOs, placeholder text, or template brackets (e.g. `[INSERT HERE]`, `# TODO`, empty implementations), flag this before distilling — incomplete sources produce unreliable cheatsheets.
2. Identify key concepts, patterns, pitfalls, and reference data
3. Create a new cheatsheet (or update existing one) following the template in `templates/cheatsheet-template.md`:
   - YAML frontmatter with topic, agent, confidence level, source, date
   - One-line summary
   - Key concepts (dense, actionable)
   - Quick reference tables where applicable
   - WARNING blocks for critical pitfalls
   - EXAMPLES with concrete worked examples
   - Decision guides for common choices
4. Mark confidence levels: [VERIFIED] [TEXTBOOK] [DERIVED] [UNCERTAIN]
5. Update `cheatsheets/_index.md` with the new entry
6. Commit: `git add . && git commit -m "[agent-name] learned: [topic] from [source]"`

Report what cheatsheet was created/updated when complete.
