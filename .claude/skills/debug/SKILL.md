---
name: debug
description: Execute the Scientific Debugging Protocol for the currently active agent
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Execute the Scientific Debugging Protocol.

Problem to debug: $ARGUMENTS

This protocol applies scientific method to bug investigation. Follow it in order — do not skip to fixes.

## 1. State the Problem Precisely

Before touching any code, write down:
- **Observed behavior:** What is actually happening (exact error message, output, or symptom)
- **Expected behavior:** What should happen and why
- **Reproducibility:** Can you reliably trigger it? Under what conditions?

## 2. Gather Evidence First

Read the relevant code. Do NOT guess or change anything yet. Collect:
- Stack traces, error messages, logs
- Relevant code paths from entry point to failure point
- Recent changes (`git log --oneline -10`) that could have introduced this

## 3. Form Falsifiable Hypotheses

State 1–3 specific hypotheses. Each must be:
- **Falsifiable:** A test exists that could prove it wrong
- **Specific:** "The auth token is expired" not "something is wrong with auth"
- **Testable without modifying production behavior** (use logs, isolated tests, or read-only checks)

For each hypothesis, define:
- **Prediction:** If true, I will observe X
- **Test:** Specific command, log statement, or isolated test
- **Success criteria:** What confirms or refutes it

## 4. Test One Variable at a Time

Test hypotheses from most to least likely. For each test:
1. Make exactly one change (add a log, run an isolated function, check a value)
2. Record what you observed
3. Mark hypothesis confirmed or eliminated

Never change two things at once — this destroys diagnostic signal.

## 5. Fix the Root Cause

Once exactly one hypothesis remains confirmed:
- Fix the root cause, not the symptom
- Write a test that would have caught this bug
- Verify the fix does not break related behavior (run existing tests)

## 6. Document the Finding

Log in `memory/mistakes.md`:
- What the bug was and where
- Root cause (not just the symptom)
- What made it hard to find
- Prevention rule for next time

**Key disciplines:**
- Treat your own code as foreign — question every design assumption
- Seek disconfirming evidence (try to prove your hypothesis wrong before acting on it)
- If 5 hypotheses have been eliminated and the bug persists, re-read the problem statement — the premise may be wrong

Report the root cause, fix applied, and prevention rule when complete.
