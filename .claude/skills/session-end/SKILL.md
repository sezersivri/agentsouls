---
name: session-end
description: Execute the Session End Protocol for the currently active agent
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Execute the Session End Protocol for the currently active agent.

This is MANDATORY before ending any work session. Complete ALL steps:

1. **Update session log:** Add an entry to the agent's `memory/session-log.md` with:
   - Date, project, task, outcome (SUCCESS/PARTIAL/FAILED)
   - What was done, what was learned, mistakes made, decisions made
   - Cheatsheets updated, follow-up needed

2. **Update brief:** Rewrite `memory/brief.md` with 1-3 bullet summary of current state after this session. Keep under 20 lines. This is what future-you reads on summon — make it useful, not exhaustive. Overwrite the body; do not append.

3. **Record mistakes:** If any mistakes were made during this session, add them to `memory/mistakes.md` with:
   - Severity tag [CRITICAL/MODERATE/MINOR]
   - What happened, root cause, impact, fix, prevention rule

4. **Record decisions:** If any key technical decisions were made, add them to `memory/decisions.md` with:
   - Context, options considered, decision, rationale, consequences

5. **Update cheatsheets:** If new knowledge was learned, create or update cheatsheets in the agent's `cheatsheets/` directory and update `_index.md`

6. **Cross-agent learnings:** If anything learned affects other agents, update `shared-knowledge/cross-agent-learnings.md`

7. **Commit:** `git add . && git commit -m "[agent-name] session YYYY-MM-DD: brief description"`

Report what was updated when complete.
