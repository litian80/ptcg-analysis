# Windows (PowerShell) version of setup.sh. Needs Git and Node 18+ on PATH.
# Usage: powershell -ExecutionPolicy Bypass -File sim\twinleaf\setup.ps1
$ErrorActionPreference = "Stop"
$Commit = "7bb457367c3431c18bbb53d1eef2f29591221ed8"
$Dir = if ($args.Count -gt 0) { $args[0] } else { Join-Path $PSScriptRoot ".twinleaf" }
if (-not (Test-Path (Join-Path $Dir ".git"))) {
  git clone --filter=blob:limit=2m https://github.com/twinleafgg/twinleafgg.git $Dir
}
git -C $Dir fetch --quiet origin $Commit
git -C $Dir checkout --quiet $Commit
Push-Location (Join-Path $Dir "ptcg-server")
npm install --ignore-scripts --no-audit --no-fund
node --max-old-space-size=8192 ./node_modules/typescript/bin/tsc
Pop-Location
Write-Host "Twinleaf ready at $Dir"
