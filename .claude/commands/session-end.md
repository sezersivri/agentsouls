Execute the Session End Protocol for the currently active agent.

This is MANDATORY before ending any work session. Complete ALL steps:

1. **Update session log:** Add an entry to the agent's `memory/session-log.md` with:
   - Date, project, task, outcome (SUCCESS/PARTIAL/FAILED)
   - What was done, what was learned, mistakes made, decisions made
   - Cheatsheets updated, follow-up needed

2. **Record mistakes:** If any mistakes were made during this session, add them to `memory/mistakes.md` with:
   - Severity tag [CRITICAL/MODERATE/MINOR]
   - What happened, root cause, impact, fix, prevention rule

3. **Record decisions:** If any key technical decisions were made, add them to `memory/decisions.md` with:
   - Context, options considered, decision, rationale, consequences

4. **Update cheatsheets:** If new knowledge was learned, create or update cheatsheets in the agent's `cheatsheets/` directory and update `_index.md`

5. **Cross-agent learnings:** If anything learned affects other agents, update `shared-knowledge/cross-agent-learnings.md`

6. **Commit:** `git add . && git commit -m "[agent-name] session YYYY-MM-DD: brief description"`

Report what was updated when complete.
