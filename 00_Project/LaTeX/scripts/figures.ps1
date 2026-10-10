# Exports figure sources to PDF for the thesis. Sources: figures-src\*.svg -> img\figs\<name>.pdf (Inkscape CLI).
# Does nothing when there are no sources (panels can also be composed directly in LaTeX with subcaption).
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path $root 'figures-src'
if (-not (Test-Path $src)) { return }
$svgs = @(Get-ChildItem $src -Filter *.svg -File)
if ($svgs.Count -eq 0) { return }
$ink = Get-Command inkscape -ErrorAction SilentlyContinue
if (-not $ink) { Write-Warning 'figures-src has SVG files but Inkscape is not on PATH - skipping export'; return }
$outDir = Join-Path $root 'img\figs'
New-Item -ItemType Directory -Force $outDir | Out-Null
foreach ($svg in $svgs) {
    $pdf = Join-Path $outDir ($svg.BaseName + '.pdf')
    if ((Test-Path $pdf) -and (Get-Item $pdf).LastWriteTime -ge $svg.LastWriteTime) { continue }   # up to date
    & $ink.Source $svg.FullName --export-type=pdf --export-filename=$pdf 2>&1 | Out-Null
    Write-Host "figure: $($svg.Name) -> img\figs\$($svg.BaseName).pdf"
}
