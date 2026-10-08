# Skrypt do kompilacji pracy LaTeX z regeneracją bibliografii
# Użycie: .\kompiluj.ps1 [-Silent]

param([switch]$Silent)

# Funkcja do czyszczenia plików tymczasowych
function Clean-TemporaryFiles {
    Write-Host "`n[Cleanup] Czyszczenie plikow tymczasowych..." -ForegroundColor $INFO
    $filesToRemove = @(
        # Główne pliki pomocnicze
        # "build/$DOCUMENT.aux",
        "build/$DOCUMENT.out",
        "build/$DOCUMENT.toc",
        "build/$DOCUMENT.lot",
        "build/$DOCUMENT.lof",
        #build/ "$DOCUMENT.synctex.gz",
        "build/$DOCUMENT.fls",
        "build/$DOCUMENT.fdb_latexmk",
        "build/$DOCUMENT.dvi",
        "build/$DOCUMENT.bbl",
        "build/$DOCUMENT.blg",
        # "build//chapters",
        # Pliki preambuły
        "tex_files/build"
    )
    
    foreach ($file in $filesToRemove) {
        if (Test-Path $file) {
            Remove-Item $file -Force -ErrorAction SilentlyContinue
        }
    }
    
    # Usuń również pliki .aux z podfolderów (z include{})
    # Get-ChildItem -Filter "*.aux" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    
    Write-Host "OK - Pliki tymczasowe wyczyszczone" -ForegroundColor $SUCCESS
}

# Nazwa głównego pliku bez rozszerzenia
$DOCUMENT = "Franciszek_Zabierowski_mgr"
function BUILD {
    $output = latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error -outdir=build "$DOCUMENT.tex"  2>&1
}
# Kolory do wydruku
$SUCCESS = "Green"
$ERR_COLOR = "Red"
$INFO = "Cyan"

Write-Host "`n========================================" -ForegroundColor $INFO
Write-Host "  LaTeX Compiler with Bibliography" -ForegroundColor $INFO
Write-Host "========================================`n" -ForegroundColor $INFO

# Sprawdzenie czy plik .tex istnieje
if (-not (Test-Path "$DOCUMENT.tex")) {
    Write-Host "Błąd: Plik $DOCUMENT.tex nie znaleziony!" -ForegroundColor $ERROR_COLOR
    exit 1
}

# Krok 1: Czyszczenie starych plików pomocniczych
Write-Host "[1/5] Czyszczenie starych plików..." -ForegroundColor $INFO
Remove-Item "$DOCUMENT.bbl", "$DOCUMENT.blg", "$DOCUMENT.out" -Force -ErrorAction SilentlyContinue
Write-Host "OK - Pliki wyczyszczone" -ForegroundColor $SUCCESS

# Krok 2: Pierwszy przebieg pdflatex
Write-Host "[2/5] Pierwszy przebieg pdflatex..." -ForegroundColor $INFO
BUILD
# $output = latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error -outdir=build "$DOCUMENT.tex"  2>&1
Write-Host "OK - Pierwszy przebieg" -ForegroundColor $SUCCESS

# Krok 3: BibTeX - regeneracja bibliografii
Write-Host "[3/5] Regeneracja bibliografii (bibtex)..." -ForegroundColor $INFO
$bibtex_output = bibtex "$DOCUMENT" 2>&1
Write-Host "OK - Bibliografia wygenerowana" -ForegroundColor $SUCCESS

# Krok 4: Drugi przebieg pdflatex
Write-Host "[4/5] Drugi przebieg pdflatex..." -ForegroundColor $INFO
BUILD
# $output = latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error -outdir=build "$DOCUMENT.tex"  2>&1
Write-Host "OK - Drugi przebieg" -ForegroundColor $SUCCESS

# Krok 5: Trzeci przebieg pdflatex (finalizacja)
Write-Host "[5/5] Trzeci przebieg pdflatex (finalizacja)..." -ForegroundColor $INFO
BUILD
# $output = latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error -outdir=build "$DOCUMENT.tex"  2>&1
Write-Host "OK - Trzeci przebieg" -ForegroundColor $SUCCESS

# Sprawdzenie czy PDF został utworzony
Write-Host "`n========================================" -ForegroundColor $INFO
if (Test-Path "./build/$DOCUMENT.pdf") {
    $pdfFile = Get-Item "./build/$DOCUMENT.pdf"
    $sizeMB = $pdfFile.Length / 1MB
    $sizeDisplay = [math]::Round($sizeMB, 2)
    Write-Host "KOMPILACJA ZAKONCZYLA SIE POMYSLNIE!" -ForegroundColor $SUCCESS
    Write-Host "Plik: ./build/$DOCUMENT.pdf (rozmiar: $sizeDisplay MB)" -ForegroundColor $SUCCESS
    Write-Host "========================================`n" -ForegroundColor $INFO

    # Czyszczenie plików tymczasowych
    # Clean-TemporaryFiles

    Write-Host "`nZachowane pliki:" -ForegroundColor $INFO
    Write-Host "  - ./build/$DOCUMENT.pdf (dokument)" -ForegroundColor $SUCCESS
    Write-Host "  - $DOCUMENT.log (dziennik kompilacji)" -ForegroundColor $SUCCESS
    
}
else {
    Write-Host "BLAD: Nie udalo sie wygenerowac PDF!" -ForegroundColor $ERR_COLOR
    Write-Host "========================================`n" -ForegroundColor $INFO
    
    # Czyszczenie plików tymczasowych także w przypadku błędu
    Clean-TemporaryFiles
    
    exit 1
}
