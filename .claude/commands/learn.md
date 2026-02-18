Execute the Knowledge Consumption Protocol for the currently active agent.

The agent should study the provided source material and distill it into cheatsheets.

Source to study: $ARGUMENTS

Steps:
1. Read the source material carefully
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
