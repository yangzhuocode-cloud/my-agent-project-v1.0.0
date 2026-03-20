# Auto-setup Git Worktree development environment
# Usage: Run this script after cloning the project

$ErrorActionPreference = "Stop"

Write-Host "Setting up Git Worktree development environment..." -ForegroundColor Green
Write-Host ""

# Check if in a Git repository
try {
    git rev-parse --git-dir | Out-Null
} catch {
    Write-Host "ERROR: Current directory is not a Git repository" -ForegroundColor Red
    exit 1
}

# Check if on master branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "master") {
    Write-Host "WARNING: Not on master branch (current: $currentBranch)" -ForegroundColor Yellow
    Write-Host "Recommended to switch to master branch before running this script"
    $continue = Read-Host "Continue? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

# Fetch all remote branches
Write-Host "Fetching remote branch information..." -ForegroundColor Blue
git fetch --all | Out-Null

# Get all remote feature branches
$remoteBranches = git branch -r | Where-Object { $_ -match "origin/feature/" } | ForEach-Object {
    $_.Trim() -replace "origin/", ""
}

if ($remoteBranches.Count -eq 0) {
    Write-Host "No feature branches found, no worktrees to setup" -ForegroundColor Yellow
    exit 0
}

Write-Host "Found the following feature branches:" -ForegroundColor Green
foreach ($branch in $remoteBranches) {
    Write-Host "  - $branch"
}
Write-Host ""

# Create worktree for each feature branch
Write-Host "Creating worktrees..." -ForegroundColor Blue
Write-Host ""

$successCount = 0
$skipCount = 0

foreach ($branch in $remoteBranches) {
    # Extract branch name (remove feature/ prefix)
    $branchName = $branch -replace "feature/", ""
    $worktreePath = "worktrees/$branchName"
    
    # Check if worktree already exists
    if (Test-Path $worktreePath) {
        Write-Host "SKIP: $worktreePath already exists" -ForegroundColor Yellow
        $skipCount++
    } else {
        Write-Host "CREATE: $worktreePath ($branch)" -ForegroundColor Green
        git worktree add $worktreePath $branch
        $successCount++
    }
    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Green
Write-Host "Worktree setup completed" -ForegroundColor Green
Write-Host ""
Write-Host "Current worktree structure:" -ForegroundColor Blue
git worktree list
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Usage tips:" -ForegroundColor Blue
Write-Host "  - Framework development: Work in main directory (master branch)"
Write-Host "  - Agent development: Work in worktrees/<agent-name>/"
Write-Host "  - Sync updates: Run .\scripts\sync-master-to-worktrees.ps1"
Write-Host ""

exit 0
