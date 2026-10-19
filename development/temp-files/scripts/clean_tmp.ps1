<#
.SYNOPSIS
    Deletes files older than 30 days from <project root>/.tmp/.

.DESCRIPTION
    Operates only inside <project root>/.tmp/. A file is deleted only when it is
    at least DaysOld days old: both its last-write time and, if the name starts
    with YYYY.MM.DD_, the date in that prefix must be older than the cutoff.
    Reparse points (symlinks, junctions) are never followed or deleted.
    Empty nested folders are removed afterwards; first-level folders stay.
    The .tmp/keep/ folder is skipped entirely.

.PARAMETER DaysOld
    Retention age in days. Cannot be lower than 30. Default: 30.

.PARAMETER ProjectRoot
    Project root that contains .tmp/. Defaults to the git root of the current
    directory, or the current directory when it is not a git repository.

.PARAMETER DryRun
    Report what would be deleted without deleting.

.EXAMPLE
    .\clean_tmp.ps1 -ProjectRoot . -DryRun
#>
[CmdletBinding()]
param(
    [ValidateRange(30, 3650)]
    [int]$DaysOld = 30,

    [string]$ProjectRoot = "",

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($ProjectRoot) -or $ProjectRoot -eq ".") {
    $gitRoot = $null
    try { $gitRoot = (& git rev-parse --show-toplevel 2>$null) } catch { }
    $ProjectRoot = if ($gitRoot) { $gitRoot } else { (Get-Location).Path }
}

$RootPath = (Resolve-Path -LiteralPath $ProjectRoot).Path
$TmpDir = Join-Path $RootPath ".tmp"

if (-not (Test-Path -LiteralPath $TmpDir -PathType Container)) {
    Write-Host "No .tmp/ in $RootPath - nothing to clean."
    exit 0
}

$TmpItem = Get-Item -LiteralPath $TmpDir -Force
if ($TmpItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
    throw ".tmp is a symlink/junction; refusing to clean: $TmpDir"
}

$TmpPrefix = $TmpItem.FullName.TrimEnd([char]92, [char]47) + [System.IO.Path]::DirectorySeparatorChar
$Cutoff = (Get-Date).Date.AddDays(-$DaysOld)

function Test-InsideTmp([string]$Path) {
    return $Path.StartsWith($TmpPrefix, [System.StringComparison]::OrdinalIgnoreCase)
}

# Re-checked right before every deletion: the item and every parent below .tmp must
# still exist and be a plain file/folder (not swapped for a link after the walk).
function Test-PlainPath([string]$Path) {
    $current = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    while ($current -and $current.FullName.TrimEnd([char]92) -ne $TmpItem.FullName.TrimEnd([char]92)) {
        if ($current.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { return $false }
        $current = if ($current -is [System.IO.DirectoryInfo]) { $current.Parent } else { $current.Directory }
    }
    return [bool]$current
}

function Get-EffectiveDate([System.IO.FileInfo]$File) {
    $date = $File.LastWriteTime
    if ($File.Name -match '^(\d{4})\.(\d{2})\.(\d{2})_') {
        try {
            $prefixDate = [datetime]::new([int]$Matches[1], [int]$Matches[2], [int]$Matches[3])
            if ($prefixDate -gt $date) { $date = $prefixDate }
        } catch { }
    }
    return $date
}

# Collect files and directories without following reparse points.
$files = New-Object System.Collections.Generic.List[System.IO.FileInfo]
$dirs = New-Object System.Collections.Generic.List[System.IO.DirectoryInfo]

function Walk([System.IO.DirectoryInfo]$Dir) {
    foreach ($entry in Get-ChildItem -LiteralPath $Dir.FullName -Force) {
        if ($entry.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { continue }
        if ($entry.PSIsContainer) {
            # .tmp/keep/ is never cleaned
            if ($Dir.FullName -eq $TmpItem.FullName -and $entry.Name -ieq "keep") { continue }
            $dirs.Add($entry)
            Walk $entry
        } else {
            $files.Add($entry)
        }
    }
}
Walk $TmpItem

$deleted = 0
$skipped = 0
$bytes = [int64]0
$mode = if ($DryRun) { "DRY RUN" } else { "LIVE" }
Write-Host "clean_tmp [$mode] root=$RootPath cutoff=$($Cutoff.ToString('yyyy-MM-dd')) (older than $DaysOld days)"

foreach ($file in $files) {
    if (-not (Test-InsideTmp $file.FullName)) { continue }
    if ((Get-EffectiveDate $file) -ge $Cutoff) { continue }

    if ($DryRun) {
        Write-Host " [WOULD REMOVE] $($file.FullName)"
        $deleted++
        $bytes += $file.Length
        continue
    }
    try {
        if (-not (Test-PlainPath $file.FullName)) {
            Write-Host " [SKIPPED] $($file.FullName): changed during the run"
            $skipped++
            continue
        }
        $size = $file.Length
        Remove-Item -LiteralPath $file.FullName -Force
        Write-Host " [REMOVED] $($file.FullName)"
        $deleted++
        $bytes += $size
    } catch {
        Write-Host " [SKIPPED] $($file.FullName): $($_.Exception.Message)"
        $skipped++
    }
}

# Remove empty nested folders, deepest first. First-level folders are kept.
if (-not $DryRun) {
    $nested = $dirs | Where-Object { $_.Parent.FullName -ne $TmpItem.FullName } |
        Sort-Object { $_.FullName.Length } -Descending
    foreach ($dir in $nested) {
        if (-not (Test-InsideTmp $dir.FullName)) { continue }
        if (-not (Test-PlainPath $dir.FullName)) { continue }
        if (-not (Get-ChildItem -LiteralPath $dir.FullName -Force | Select-Object -First 1)) {
            try { Remove-Item -LiteralPath $dir.FullName -Force } catch { }
        }
    }
}

Write-Host ("Files {0}: {1}, freed {2} MB, skipped {3}" -f
    $(if ($DryRun) { "to remove" } else { "removed" }), $deleted, [math]::Round($bytes / 1MB, 2), $skipped)
exit 0
