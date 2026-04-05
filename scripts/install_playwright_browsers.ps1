# Install Playwright Firefox browsers into `resources/playwright_browsers`.
# Usage: run from repository root or run this script directly in PowerShell.

$repoRoot = Split-Path -Parent $PSScriptRoot
$target = Join-Path $repoRoot 'resources\playwright_browsers'
New-Item -ItemType Directory -Path $target -Force | Out-Null
$fullTarget = (Resolve-Path $target).Path
Write-Host "Target Playwright browsers path: $fullTarget"

# Prefer the virtualenv python if available
$venvPython = Join-Path $repoRoot '.venv\Scripts\python.exe'
if (Test-Path $venvPython) { $python = $venvPython } else { $python = 'python' }

$env:PLAYWRIGHT_BROWSERS_PATH = $fullTarget
Write-Host "Using python: $python"
Write-Host "Installing Playwright and Firefox to $env:PLAYWRIGHT_BROWSERS_PATH"

& $python -m pip install --upgrade playwright
& $python -m playwright install firefox

Write-Host 'Done. The browsers are installed under:'
Write-Host $env:PLAYWRIGHT_BROWSERS_PATH
