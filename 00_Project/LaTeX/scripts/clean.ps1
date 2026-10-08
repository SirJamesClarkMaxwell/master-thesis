function Clean-TemporaryFiles {
    Write-Host "`n[Cleanup] Czyszczenie plikow tymczasowych..." -ForegroundColor $INFO
    $filesToRemove = @(
        # Główne pliki pomocnicze
        "$DOCUMENT.aux",
        "$DOCUMENT.out",
        "$DOCUMENT.toc",
        "$DOCUMENT.lot",
        "$DOCUMENT.lof",
        "$DOCUMENT.synctex.gz",
        "$DOCUMENT.fls",
        "$DOCUMENT.fdb_latexmk",
        "$DOCUMENT.dvi",
        "$DOCUMENT.bbl",
        "$DOCUMENT.blg",
        "build//chapters",
        # Pliki preambuły
        "tex_files/build"
    )
    
    foreach ($file in $filesToRemove) {
        if (Test-Path $file) {
            Remove-Item $file -Force -ErrorAction SilentlyContinue
        }
    }
    
    # Usuń również pliki .aux z podfolderów (z include{})
    Get-ChildItem -Filter "*.aux" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    
    Write-Host "OK - Pliki tymczasowe wyczyszczone" -ForegroundColor $SUCCESS
}
$SUCCESS = "Green"
$ERR_COLOR = "Red"
$INFO = "Cyan"
$DOCUMENT = "build//Franciszek_Zabierowski_mgr"
Clean-TemporaryFiles