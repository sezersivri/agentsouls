# Private Setup Guide

Agents are personal. This guide walks you through setting up your own private Agent Souls repository where you create and maintain agents tailored to your workflow.

## Option A: Private Fork (Recommended)

Best for most users. You get your own private copy and can pull framework updates from upstream.

### 1. Fork the repo

Go to [github.com/sezersivri/agentsouls](https://github.com/sezersivri/agentsouls) and click **Fork**.

### 2. Make it private

In your fork's settings:
- Go to **Settings** → scroll to **Danger Zone**
- Click **Change repository visibility**
- Set to **Private**

### 3. Clone your private fork

```bash
git clone https://github.com/YOUR-USERNAME/agentsouls.git
cd agentsouls
```

### 4. Delete example agents

The repo ships with Miles and Sam as examples. Remove them:

```bash
# Remove agent directories
rm -rf agents/aerospace/miles agents/software-dev/sam

# Remove generated tool configs
rm -f .claude/agents/miles.md .claude/agents/sam.md
rm -rf .agents/skills/miles .agents/skills/sam
```

### 5. Clear the manifest

Edit `agents/manifest.json` and replace the `agents` array with an empty array:

```json
{
  "schema_version": "1.0",
  "repo_root_convention": "All paths relative to repo root",
  "agents": []
}
```

### 6. Create your first agent

```bash
# Pick a domain and name
mkdir -p agents/software-dev/nova/{cheatsheets,memory,references}

# Copy templates
cp templates/CORE-TEMPLATE.md agents/software-dev/nova/CORE.md
cp templates/session-log-template.md agents/software-dev/nova/memory/session-log.md
cp templates/mistakes-template.md agents/software-dev/nova/memory/mistakes.md
cp templates/decisions-template.md agents/software-dev/nova/memory/decisions.md

# Create cheatsheet index
cat > agents/software-dev/nova/cheatsheets/_index.md << 'EOF'
# Cheatsheet Index

No cheatsheets yet.
EOF
```

Edit `agents/software-dev/nova/CORE.md` — fill in the agent's identity, role, personality, hard rules, and expertise. This is where the real value lives.

### 7. Add to manifest

Add your agent to the `agents` array in `agents/manifest.json`:

```json
{
  "name": "Nova",
  "slug": "nova",
  "domain": "software-dev",
  "role": "Backend Developer",
  "description": "Backend developer responsible for API design and implementation.",
  "model": "sonnet",
  "capabilities": ["python", "fastapi", "postgresql"],
  "tags": ["specialist", "software-dev"],
  "paths": {
    "core": "agents/software-dev/nova/CORE.md",
    "cheatsheets": "agents/software-dev/nova/cheatsheets/",
    "cheatsheet_index": "agents/software-dev/nova/cheatsheets/_index.md",
    "memory": "agents/software-dev/nova/memory/",
    "mistakes": "agents/software-dev/nova/memory/mistakes.md",
    "session_log": "agents/software-dev/nova/memory/session-log.md",
    "decisions": "agents/software-dev/nova/memory/decisions.md"
  },
  "delegates_to": [],
  "defers_to": [],
  "escalates_to": []
}
```

### 8. Generate and validate

```bash
python scripts/generate-tool-configs.py
python scripts/validate.py
```

### 9. Commit and push

```bash
git add .
git commit -m "[nova] init: add Backend Developer agent"
git push
```

### 10. Pull upstream updates

When the framework gets improvements, pull them into your fork:

```bash
git remote add upstream https://github.com/sezersivri/agentsouls.git
git fetch upstream
git merge upstream/main
```

This updates scripts, templates, and documentation without touching your agents.

---

## Option B: Template Clone (No Upstream Link)

Best if you want full independence and don't need framework updates.

### 1. Use as template or clone

**GitHub template:**
- Go to [github.com/sezersivri/agentsouls](https://github.com/sezersivri/agentsouls)
- Click **Use this template** → **Create a new repository**
- Set visibility to **Private**

**Or clone and disconnect:**
```bash
git clone https://github.com/sezersivri/agentsouls.git my-agents
cd my-agents
rm -rf .git
git init
git add .
git commit -m "init: agent souls framework"
```

### 2. Create a private repo on GitHub

```bash
gh repo create YOUR-USERNAME/my-agents --private --source=. --push
```

### 3. Set up your agents

Follow steps 4–9 from Option A above: delete examples, clear manifest, create your agents, generate, validate, commit.

---

## Tips

### Naming your agents

Pick short, memorable names. One syllable works best for `/summon` commands. The name should feel like a teammate, not a tool.

### Model selection

| Model | Best for | Cost |
|-------|----------|------|
| `opus` | Lead roles, architecture decisions, complex analysis | Highest |
| `sonnet` | Implementation, domain work, most specialist tasks | Medium |
| `haiku` | Testing, documentation, routine tasks | Lowest |

### Building knowledge over time

Agents get better with use. After each session:
- The agent logs what happened (`session-log.md`)
- Records mistakes to avoid next time (`mistakes.md`)
- Logs key decisions (`decisions.md`)
- Builds cheatsheets from learned knowledge

The `/session-end` command handles this automatically.

### Multiple projects

Use the submodule pattern to share agents across projects:

```bash
# In your project
git submodule add git@github.com:YOUR-USERNAME/my-agents.git .agents
```

Your agents travel with you, accumulating knowledge across all your projects.
