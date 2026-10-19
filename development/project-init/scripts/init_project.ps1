<#
.SYNOPSIS
    Deterministic, non-destructive part of project-init (Windows PowerShell).

.DESCRIPTION
    Creates what is missing and never modifies or deletes anything that exists:
    folders, the .tmp/ line in .gitignore (append only), docs/README.md,
    AGENTS.md and CLAUDE.md (only when absent), and junctions to the temp-files
    skill. An existing AGENTS.md/CLAUDE.md, a plain copy of the skill or a
    dangling link is reported as [needs-review] and left untouched; the agent
    normalizes instructions afterwards with the user's confirmation.

    One line per item: [created|skipped|needs-review|would-create|failed] item - detail.
    Exit code 1 when any item failed, otherwise 0.

.PARAMETER ProjectRoot
    Existing project root.

.PARAMETER TempFilesPath
    Folder of the temp-files skill. Default: ../../temp-files relative to this
    script. Pass it explicitly when this skill is reached through a link.

.PARAMETER GitInit
    Run git init when <root>/.git is missing.

.PARAMETER Claude
    Also create .claude/, CLAUDE.md (@AGENTS.md) and .claude/skills/temp-files.

.PARAMETER DryRun
    Report what would be created without changing anything.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [string]$TempFilesPath = "",
    [switch]$GitInit,
    [switch]$Claude,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$SkillDir = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($TempFilesPath)) {
    $TempFilesPath = Join-Path (Split-Path -Parent $SkillDir) "temp-files"
}
$TemplatePath = Join-Path $SkillDir "assets\AGENTS.template.md"
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$script:Failed = 0

function Report([string]$Status, [string]$Item, [string]$Detail = "") {
    if ($Status -eq "failed") { $script:Failed++ }
    if ($Detail) { Write-Host "[$Status] $Item - $Detail" } else { Write-Host "[$Status] $Item" }
}

function Step([string]$Item, [scriptblock]$Body) {
    try { & $Body } catch { Report "failed" $Item $_.Exception.Message }
}

function Ensure-Dir([string]$Rel) {
    Step $Rel {
        $path = Join-Path $Root $Rel
        if (Test-Path -LiteralPath $path -PathType Container) { Report "skipped" $Rel; return }
        if (Test-Path -LiteralPath $path) { Report "failed" $Rel "exists and is not a folder"; return }
        if ($DryRun) { Report "would-create" $Rel; return }
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Report "created" $Rel
    }
}

# Creates a file only when absent. An existing file is never touched.
function Ensure-File([string]$Rel, [string]$Content, [string]$ExistingStatus = "skipped") {
    Step $Rel {
        $path = Join-Path $Root $Rel
        if (Test-Path -LiteralPath $path) { Report $ExistingStatus $Rel "exists, left untouched"; return }
        if ($DryRun) { Report "would-create" $Rel; return }
        [System.IO.File]::WriteAllText($path, $Content, $Utf8)
        Report "created" $Rel
    }
}

function Ensure-Link([string]$Rel) {
    Step $Rel {
        $link = Join-Path $Root $Rel
        $item = Get-Item -LiteralPath $link -Force -ErrorAction SilentlyContinue
        if ($item) {
            if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                if (Test-Path -LiteralPath (Join-Path $link "SKILL.md")) { Report "skipped" $Rel "link is healthy" }
                else { Report "needs-review" $Rel "dangling link, left untouched" }
            } else {
                Report "needs-review" $Rel "exists and is not a link, left untouched"
            }
            return
        }
        if (-not (Test-Path -LiteralPath (Join-Path $TempFilesPath "SKILL.md"))) {
            Report "failed" $Rel "temp-files skill not found at $TempFilesPath"
            return
        }
        if ($DryRun) { Report "would-create" $Rel; return }
        $parent = Split-Path -Parent $link
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        New-Item -ItemType Junction -Path $link -Target $TempFilesPath | Out-Null
        Report "created" $Rel "junction to $TempFilesPath"
    }
}

# 1. git
Step ".git" {
    if (-not $GitInit) { return }
    if (Test-Path -LiteralPath (Join-Path $Root ".git")) { Report "skipped" ".git"; return }
    if ($DryRun) { Report "would-create" ".git"; return }
    & git -C $Root init --quiet
    if ($LASTEXITCODE -ne 0) { throw "git init exited with $LASTEXITCODE" }
    Report "created" ".git"
}

# 2. folders
Ensure-Dir "docs"
Ensure-Dir ".agents/skills"
Ensure-Dir ".tmp"
if ($Claude) { Ensure-Dir ".claude" }

# 3. .gitignore: append-only
Step ".gitignore" {
    $path = Join-Path $Root ".gitignore"
    if (-not (Test-Path -LiteralPath $path)) {
        if ($DryRun) { Report "would-create" ".gitignore"; return }
        [System.IO.File]::WriteAllText($path, ".tmp/`n", $Utf8)
        Report "created" ".gitignore"
        return
    }
    $text = [System.IO.File]::ReadAllText($path)
    $present = @($text -split "`r?`n" | ForEach-Object { $_.Trim() } |
        Where-Object { $_ -in @(".tmp/", "/.tmp/", ".tmp", "/.tmp") })
    if ($present.Count -gt 0) { Report "skipped" ".gitignore" ".tmp/ already ignored"; return }
    if ($DryRun) { Report "would-create" ".gitignore" "append .tmp/"; return }
    $nl = if ($text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $prefix = if ($text.Length -gt 0 -and -not $text.EndsWith("`n")) { $nl } else { "" }
    [System.IO.File]::AppendAllText($path, "$prefix.tmp/$nl", $Utf8)
    Report "created" ".gitignore" "appended .tmp/"
}

# 4. docs and instruction files
Ensure-File "docs/README.md" "# Documentation`n`nTable of contents for project documentation.`n"
Step "AGENTS.md" {
    $template = [System.IO.File]::ReadAllText($TemplatePath)
    Ensure-File "AGENTS.md" $template "needs-review"
}
if ($Claude) {
    Step "CLAUDE.md" {
        $path = Join-Path $Root "CLAUDE.md"
        if ((Test-Path -LiteralPath $path) -and
            @(Get-Content -LiteralPath $path | Where-Object { $_.Trim() -eq "@AGENTS.md" }).Count -gt 0) {
            Report "skipped" "CLAUDE.md" "already imports @AGENTS.md"
            return
        }
        Ensure-File "CLAUDE.md" "@AGENTS.md`n" "needs-review"
    }
}

# 5. temp-files links
Ensure-Link ".agents/skills/temp-files"
if ($Claude) { Ensure-Link ".claude/skills/temp-files" }

if ($script:Failed -gt 0) { exit 1 }
exit 0
