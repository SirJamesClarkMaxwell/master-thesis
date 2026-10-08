# Skrypt do kompilacji pracy LaTeX z regeneracją bibliografii
# Użycie: .\kompiluj.ps1

# Funkcja do czyszczenia plików tymczasowych
function Clean-TemporaryFiles {
    Write-Host "`n[Cleanup] Czyszczenie plikow tymczasowych..." -ForegroundColor $INFO
    $filesToRemove = @(
        # Główne pliki pomocnicze
        # "$DOCUMENT.aux",
        "$DOCUMENT.out",
        "$DOCUMENT.toc",
        "$DOCUMENT.lot",
        "$DOCUMENT.lof",
        # "$DOCUMENT.synctex.gz",
        "$DOCUMENT.fls",
        "$DOCUMENT.fdb_latexmk",
        "$DOCUMENT.dvi",
        "$DOCUMENT.bbl",
        "$DOCUMENT.blg",
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
    $output = latexmk -pdf -synctex=1 -c -interaction=nonstopmode -file-line-error -outdir=build "$DOCUMENT.tex"  2>&1
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
    Write-Host "Błąd: Plik $DOCUMENT.tex nie znaleziony!" -ForegroundColor $ERROR
    exit 1
}

# Krok 1: Czyszczenie starych plików pomocniczych
Write-Host "[1/3] Czyszczenie starych plików..." -ForegroundColor $INFO
Remove-Item "$DOCUMENT.bbl", "$DOCUMENT.blg", "$DOCUMENT.out" -Force -ErrorAction SilentlyContinue
Write-Host "OK - Pliki wyczyszczone" -ForegroundColor $SUCCESS

# Krok 2: Pierwszy przebieg pdflatex
Write-Host "[2/3] Pierwszy przebieg pdflatex..." -ForegroundColor $INFO
BUILD
Write-Host "OK - Pierwszy przebieg" -ForegroundColor $SUCCESS

# Krok 4: Drugi przebieg pdflatex
Write-Host "[3/3] Drugi przebieg pdflatex..." -ForegroundColor $INFO
BUILD
Write-Host "OK - Drugi przebieg" -ForegroundColor $SUCCESS


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
    Clean-TemporaryFiles

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
