# Agent Roster

> Directory of all agents. Use this to find the right agent for the job.

## Summoning Protocol

When summoning an agent, the following sequence is automatic:

1. Agent reads `GENERAL_RULES.md`
2. Agent reads their `SOUL.md`
3. Agent checks `memory/mistakes.md`
4. Agent scans `cheatsheets/_index.md`
5. Agent loads relevant cheatsheets for the current task
6. Agent begins work

## Aerospace

| Agent | Role | Model | Location |
|-------|------|-------|----------|
| **Miles** | Aerodynamicist (Lead) | Opus | `agents/aerospace/miles/` |
| **Nash** | CFD Engineer | Sonnet | `agents/aerospace/nash/` |
| **Cole** | DATCOM Specialist | Sonnet | `agents/aerospace/cole/` |

Escalation: Nash/Cole → Miles for complex analysis or conflicting results.

## Software Development

| Agent | Role | Model | Location |
|-------|------|-------|----------|
| **Max** | Architect (Lead) | Opus | `agents/software-dev/max/` |
| **Sam** | Backend Developer | Sonnet | `agents/software-dev/sam/` |
| **Lena** | Frontend Developer | Sonnet | `agents/software-dev/lena/` |
| **Kit** | QA Engineer | Haiku | `agents/software-dev/kit/` |
| **Dash** | DevOps Engineer | Sonnet | `agents/software-dev/dash/` |
| **Ward** | Security Reviewer | Sonnet | `agents/software-dev/ward/` |

Escalation: Individual devs → Max for architecture decisions.

## Research

| Agent | Role | Model | Location |
|-------|------|-------|----------|
| **Sage** | Research Analyst | Sonnet | `agents/research/sage/` |
| **Reed** | Technical Writer | Haiku | `agents/research/reed/` |

Escalation: Reed → Sage for research-heavy content.

## Game Development

| Agent | Role | Model | Location |
|-------|------|-------|----------|
| **Drake** | Game Designer (Lead) | Opus | `agents/game-dev/drake/` |
| **Cody** | Game Developer | Sonnet | `agents/game-dev/cody/` |

Escalation: Cody → Drake for architecture and design decisions.

## iOS Development

| Agent | Role | Model | Location |
|-------|------|-------|----------|
| **Logan** | iOS Lead | Opus | `agents/ios-dev/logan/` |
| **Maya** | iOS Developer | Sonnet | `agents/ios-dev/maya/` |

Escalation: Maya → Logan for architecture and App Store decisions.

## Financial

| Agent | Role | Model | Location |
|-------|------|-------|----------|
| **Blake** | Market Strategist (Lead) | Opus | `agents/financial/blake/` |
| **Kai** | Quantitative Analyst | Sonnet | `agents/financial/kai/` |
| **Finn** | Risk Manager | Sonnet | `agents/financial/finn/` |

Escalation: Kai/Finn → Blake for strategic decisions.

## Cross-Domain Collaboration

| Task Type | Primary | Supporting |
|-----------|---------|------------|
| Scientific software | Max | Sam + Miles |
| CFD automation | Dash | Nash + Sam |
| Research blog | Reed | Sage + domain expert |
| Game with analytics | Drake | Kai + Sam |
| iOS financial app | Logan | Blake + Lena |

## Stats

- **Total:** 18 agents
- **Opus (Leads):** 5 — Miles, Max, Drake, Logan, Blake
- **Sonnet (Specialists):** 11 — Nash, Cole, Sam, Lena, Dash, Ward, Sage, Cody, Maya, Kai, Finn
- **Haiku (Utility):** 2 — Kit, Reed
