# One entry point for building the thesis. Steps: bib (optional) -> figures (optional) -> latexmk (pdflatex + biber).
#   powershell -ExecutionPolicy Bypass -File scripts\build.ps1            # normal (dark background, as on screen)
#   powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Print     # white background for printing / submission
#   powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Bib       # refresh bibliography.bib from Zotero first
#   powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Clean     # remove build artifacts and exit
param(
    [switch]$Print,
    [switch]$Bib,
    [switch]$Clean
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
    if ($Clean) { & "$PSScriptRoot\clean.ps1"; return }
    if ($Bib) { & "$PSScriptRoot\bib.ps1" }
    & "$PSScriptRoot\figures.ps1"

    $doc = 'Franciszek_Zabierowski_mgr'
    New-Item -ItemType Directory -Force 'build' | Out-Null
    $log = 'build\latexmk.log'
    # -Print: \def\PRINTVERSION{1} is injected before the document so the preamble skips the dark background.
    # -g forces a full rebuild so a switch between screen and print never leaves stale output.
    $pre = if ($Print) { '-usepretex -pretex="\def\PRINTVERSION{1}"' } else { '' }
    # cmd /c with a file redirect: latexmk writes harmless warnings to stderr, which PowerShell would treat as errors.
    cmd /c "latexmk -g -pdf -synctex=1 -interaction=nonstopmode -file-line-error $pre -outdir=build $doc.tex > $log 2>&1"
    $code = $LASTEXITCODE
    $pdf = "build\$doc.pdf"
    $text = Get-Content $log -Encoding UTF8
    $problems = @($text | Select-String -Pattern '^\S+:\d+: |^! |LaTeX Warning: (Citation|Reference).*undefined|Package biblatex Warning|Biber warning|WARN - ' |
        Where-Object { $_.Line -notmatch 'does not contain any citations' } | Select-Object -First 12)
    if ($code -ne 0 -or -not (Test-Path $pdf)) {
        $problems | ForEach-Object { Write-Host $_.Line -ForegroundColor Red }
        throw "build failed (latexmk exit $code), see $log"
    }
    $problems | ForEach-Object { Write-Host $_.Line -ForegroundColor Yellow }
    $mb = [math]::Round((Get-Item $pdf).Length / 1MB, 2)
    $mode = if ($Print) { 'print (white)' } else { 'screen (dark)' }
    Write-Host "OK: $pdf ($mb MB, $mode)" -ForegroundColor Green
} finally { Pop-Location }
