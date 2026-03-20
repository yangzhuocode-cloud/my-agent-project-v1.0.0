# Auto-sync master branch updates to all worktrees
# Usage: Run this script after committing framework updates to master

$ErrorActionPreference = "Stop"

Write-Host "Starting sync from master to all worktrees..." -ForegroundColor Green
Write-Host ""

# Check if currently on master branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "master") {
    Write-Host "WARNING: Not on master branch (current: $currentBranch)" -ForegroundColor Yellow
    Write-Host "Recommended to run this script on master branch"
    $continue = Read-Host "Continue? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

# Get all worktrees (exclude main directory)
$worktreeList = git worktree list --porcelain
$worktrees = @()
$lines = $worktreeList -split "`n"
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match "^worktree (.+)$") {
        $path = $matches[1]
        if ($worktrees.Count -gt 0 -or $i -gt 0) {
            $worktrees += $path
        }
    }
}

if ($worktrees.Count -eq 0) {
    Write-Host "No worktrees found, nothing to sync" -ForegroundColor Yellow
    exit 0
}

# Track success and failures
$successCount = 0
$failCount = 0
$failedWorktrees = @()

# Merge master to each worktree
foreach ($worktreePath in $worktrees) {
    $branch = git -C $worktreePath branch --show-current
    $worktreeName = Split-Path -Leaf $worktreePath
    
    Write-Host "Processing worktree: $worktreeName ($branch)" -ForegroundColor Green
    
    # Check for uncommitted changes
    git -C $worktreePath diff-index --quiet HEAD --
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   WARNING: Uncommitted changes found, skipping merge" -ForegroundColor Yellow
        Write-Host "   Tip: Commit or stash changes in this worktree first" -ForegroundColor Yellow
        $failCount++
        $failedWorktrees += "$worktreeName (uncommitted changes)"
        Write-Host ""
        continue
    }
    
    # Try to merge master
    try {
        git -C $worktreePath merge master --no-edit 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   SUCCESS: Merged successfully" -ForegroundColor Green
            $successCount++
        } else {
            throw "Merge failed"
        }
    } catch {
        Write-Host "   FAILED: Merge failed (possible conflicts)" -ForegroundColor Red
        Write-Host "   Tip: Resolve conflicts manually" -ForegroundColor Yellow
        git -C $worktreePath merge --abort 2>$null
        $failCount++
        $failedWorktrees += "$worktreeName (merge conflict)"
    }
    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Green
Write-Host "Sync completed" -ForegroundColor Green
Write-Host "   Success: $successCount" -ForegroundColor Green
Write-Host "   Failed: $failCount" -ForegroundColor Red

if ($failCount -gt 0) {
    Write-Host ""
    Write-Host "Failed worktrees:" -ForegroundColor Yellow
    foreach ($failed in $failedWorktrees) {
        Write-Host "   - $failed"
    }
}

Write-Host "========================================" -ForegroundColor Green

exit 0
