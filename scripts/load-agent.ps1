<#
.SYNOPSIS
    Assemble full agent context and output to stdout.

.DESCRIPTION
    Reads the agent manifest, locates the specified agent's files, and
    concatenates GENERAL_RULES.md, CORE.md, mistakes.md, and _index.md
    into a single context block (text or JSON).

.PARAMETER AgentSlug
    The agent's slug identifier (e.g., "miles", "max").

.PARAMETER Format
    Output format: "text" (default) or "json".

.EXAMPLE
    .\scripts\load-agent.ps1 -AgentSlug miles
    .\scripts\load-agent.ps1 -AgentSlug miles -Format json
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$AgentSlug,

    [Parameter(Mandatory = $false)]
    [ValidateSet("text", "json")]
    [string]$Format = "text"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Resolve repo root from script location ──────────────────────────────────
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path

# ── Locate manifest ─────────────────────────────────────────────────────────
$ManifestPath = Join-Path $RepoRoot "agents" "manifest.json"
if (-not (Test-Path $ManifestPath)) {
    Write-Error "manifest.json not found at $ManifestPath"
    exit 1
}

# ── Parse manifest and find agent ────────────────────────────────────────────
$Manifest = Get-Content -Raw $ManifestPath | ConvertFrom-Json
$Agent = $Manifest.agents | Where-Object { $_.slug -eq $AgentSlug }

if (-not $Agent) {
    Write-Error "Agent '$AgentSlug' not found in manifest.json"
    exit 1
}

# ── Extract paths ────────────────────────────────────────────────────────────
$CoreRelPath       = $Agent.paths.core
$MistakesRelPath   = $Agent.paths.mistakes
$IndexRelPath      = $Agent.paths.cheatsheet_index

# ── Resolve full paths ───────────────────────────────────────────────────────
$GeneralRulesFile = Join-Path $RepoRoot "GENERAL_RULES.md"
$CoreFile         = Join-Path $RepoRoot $CoreRelPath
$MistakesFile     = Join-Path $RepoRoot $MistakesRelPath
$IndexFile        = Join-Path $RepoRoot $IndexRelPath

# ── Validate all required files exist ────────────────────────────────────────
$Missing = $false

if (-not (Test-Path $GeneralRulesFile)) {
    Write-Error "GENERAL_RULES.md not found at $GeneralRulesFile"
    $Missing = $true
}
if (-not (Test-Path $CoreFile)) {
    Write-Error "CORE.md not found at $CoreFile"
    $Missing = $true
}
if (-not (Test-Path $MistakesFile)) {
    Write-Error "mistakes.md not found at $MistakesFile"
    $Missing = $true
}
if (-not (Test-Path $IndexFile)) {
    Write-Error "_index.md not found at $IndexFile"
    $Missing = $true
}

if ($Missing) {
    exit 1
}

# ── Read file contents ───────────────────────────────────────────────────────
$GeneralRules    = Get-Content -Raw $GeneralRulesFile
$Core           = Get-Content -Raw $CoreFile
$Mistakes        = Get-Content -Raw $MistakesFile
$CheatsheetIndex = Get-Content -Raw $IndexFile

# ── Output ───────────────────────────────────────────────────────────────────
if ($Format -eq "text") {
    Write-Output "=== GENERAL RULES ==="
    Write-Output $GeneralRules
    Write-Output ""
    Write-Output "=== CORE ==="
    Write-Output $Soul
    Write-Output ""
    Write-Output "=== MISTAKES ==="
    Write-Output $Mistakes
    Write-Output ""
    Write-Output "=== CHEATSHEET INDEX ==="
    Write-Output $CheatsheetIndex
}
elseif ($Format -eq "json") {
    $OutputObject = [ordered]@{
        general_rules    = $GeneralRules
        core             = $Core
        mistakes         = $Mistakes
        cheatsheet_index = $CheatsheetIndex
    }
    $OutputObject | ConvertTo-Json -Depth 10
}
