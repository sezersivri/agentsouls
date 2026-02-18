# Mistakes Log — Miles

> Learn from every mistake. Never repeat the same one twice.
> Format: most recent first. Tag severity: [CRITICAL] [MODERATE] [MINOR]

---

## [MINOR] Forgot to update _index.md after creating cheatsheets

**Date:** 2026-02-18
**Project:** agentsouls setup
**What happened:** Created 4 cheatsheets but initially forgot to update `cheatsheets/_index.md` with the new entries.
**Root cause:** Manual process — no automated index update script existed yet.
**Impact:** Other agents (or future sessions) would not discover the cheatsheets via progressive disclosure.
**Fix:** Manually updated `_index.md` with all 4 entries including confidence levels and dates.
**Prevention:** Always update `_index.md` immediately after creating or modifying any cheatsheet. Once the `update-indexes.sh` automation script is available, run it as part of the session-end protocol.

---
