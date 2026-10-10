# Removes LaTeX build artifacts (build\ directory contents); never touches sources or bibliography.bib.
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
    & latexmk -C -outdir=build 2>&1 | Out-Null
    Write-Host 'OK: build artifacts removed'
} finally { Pop-Location }
