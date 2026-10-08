---
tags: [infra, setup]
---

# Infrastruktura: laptop + PC + klaster

**Zasada: podział po typie danych, nie po maszynie. Każda warstwa ma jednego właściciela.**

Antywzorzec, który odrzuciliśmy: „laptop → serwer na PC → git" dla tekstu. Laptop nie pracuje gdy PC śpi, nie ma pracy offline, Obsidian i LaTeX po sieci lagują, a git przestaje być kanałem synchronizacji i staje się backupem jednej maszyny.

## Warstwy

| warstwa | właściciel | kanał | status |
|---|---|---|---|
| tekst pracy (notes, LaTeX, Origin) | oba równorzędnie | GitHub `SirJamesClarkMaxwell/master-thesis`, bezpośrednio z obu | ✅ |
| klucze API + routing LLM | **PC** | OmniRoute `:20128`, laptop jako zdalny klient | do zrobienia |
| biblioteka Zotero (369 MB) | **PC** | Zotero Sync (metadane) + WebDAV na PC (pliki) | do zrobienia |
| dane VASP (5.5 GB) | **klaster** | rsync/ssh na żądanie, PC jako staging | do zrobienia |
| wtyczki Zotero (kod) | oba, dev na PC | osobne repo per wtyczka | do zrobienia |

Sieć: Tailscale, PC = `desktop-urd7d0v` / `100.126.10.20`, połączenie **direct**. Otwarte: 22 (SSH), 3389 (RDP).

## OmniRoute — PC jako gateway

OmniRoute to gateway LLM, nie wtyczka Zotero: jeden endpoint OpenAI-compatible, self-hostable, `~/.omniroute/` trzyma config i bazę, klucze szyfrowane AES-256-GCM.

Po co: **klucze API istnieją w jednym miejscu.** Każda wtyczka Zotero na obu maszynach gada z tym samym endpointem, więc jej konfiguracja jest identyczna i nie ma czego synchronizować.

```bash
# PC
npm install -g omniroute          # albo Docker / Electron
omniroute                         # :20128

# laptop — klient zdalnej instancji, bez kluczy lokalnie
omniroute connect desktop-urd7d0v
omniroute contexts use default    # powrót na lokalną
```

Token jest scoped (`read` / `write` / `admin`) — laptopowi dawaj `write`, nie `admin`. Trasy uruchamiające procesy zostają loopback-only, więc zdalny token ich nie ruszy.

Endpoint do wpisania w **obu** Zoterach, identyczny:
```
http://desktop-urd7d0v:20128/v1
```
(Na PC ta nazwa też się rozwiązuje, więc nie ma rozgałęzienia per maszyna.)

### Ostre krawędzie

1. **Bind na interfejs Tailscale, nie `0.0.0.0`.** OmniRoute trzyma wszystkie klucze — wystawienie `:20128` na LAN/WAN to wyciek kluczy i kradzież limitów. Tailscale ACL + scoped token.
2. **Brak instrukcji serwisu pod Windows** w dokumentacji (jest macOS menu-bar, systemd, Podman Quadlet). Na PC trzeba Task Scheduler „at logon" albo NSSM, inaczej gateway nie wstaje po reboocie.
3. **PC wyłączony = laptop bez gateway'a.** Fallback: model `auto` działa bez klucza (OpenCode Free), albo lokalna instancja jako druga kontekst i `omniroute contexts use`.
4. MCP: stdio (`omniroute --mcp`), HTTP `/api/mcp/stream` (110 narzędzi, 33 scope'y), SSE. Wymuszanie scope'ów jest **opt-in** — włączyć.

## Zotero

**Nigdy nie synchronizuj katalogu danych Zotero plikowo** (Syncthing, OneDrive, rsync). `zotero.sqlite` się rozsypie. Jedyne poprawne kanały to Zotero Sync i WebDAV.

Darmowy file sync Zotero = 300 MB. `C:\Users\fzabi\Zotero\storage` = **369 MB** → nie mieścisz się. Opcje: WebDAV na PC (darmowo, Tailscale już stoi), Zotero Storage 2 GB (~$20/rok), albo Zotero tylko na PC przez RDP (zero synca, brak pracy offline).

Metadane syncują się darmowo i bez limitu niezależnie od wyboru.

### Wtyczki — najpierw sprawdź, czy nie trzeba nic pisać

| chcę | czym | uwaga |
|---|---|---|
| Ask AI, Summarize | `yilewang/llm-for-zotero` | w preferencjach ustawiasz **base URL + klucz + model** → wchodzi na OmniRoute bez kodu |
| trigger „nowy item → autotag" | `windingwind/zotero-actions-tags` | warstwa automatyzacji na zdarzeniach, nie LLM |
| autotag z istniejącej taksonomii | `roey-angel/zotero-semantic-tagger` | woła Claude API z własnym kluczem; **czy da się podmienić endpoint — niesprawdzone** |
| „collect and parse my notes" | `54yyyu/zotero-mcp` | MCP nad biblioteką, ma `OPENAI_BASE_URL` dla embeddingów |
| | `MuiseDestiny/zotero-gpt` | konfigurowalny base URL **niepotwierdzony**, sprawdzić w panelu ustawień |

Autotag = `zotero-actions-tags` (kiedy) + `llm-for-zotero` (czym), oba przez OmniRoute. Dopiero gdy wyjdzie konkretna luka — pisać własną wtyczkę.

README OmniRoute wspomina integrację z vaultem Obsidiana (22 narzędzia MCP). Jeśli to prawda, „parse my notes" nad [[00_Inbox]] robi się bez kodu — **do zweryfikowania**.

## Git

Repo `master-thesis` = **tylko tekst**, 75 plików. `.gitignore` jest **whitelistą**: nowy katalog z danymi jest ignorowany domyślnie, nowy katalog z tekstem trzeba dopisać ręcznie.

Poza repo: `00_Project/hBN/` (obliczenia + figs), `03_PDF_Library/`, `02_Zoterro/` (martwa kopia profilu z II 2026), `.venv/`.

Wtyczki Zotero → **osobne repo per wtyczka**, nie w tym. Dev na PC, bo tam żyje Zotero.

Własny serwer git na PC: niepotrzebny. GitHub jest offsite i przeżywa wyłączony PC, a 5.5 GB danych nie należy do gita niezależnie od tego, gdzie ten git stoi.

## Otwarte

- 16 PDF-ów w `03_PDF_Library` jest bit-w-bit w Zotero (108 MB do odzysku)
- 16 papers nie ma w Zotero wcale (m.in. Hohenberg-Kohn 1964, Kohn-Sham 1965, Freysoldt ×2, Komsa, PBE) → zaimportować, potem skasować
- 7 książek zostaje jako PDF — Zotero ich nie weźmie
- w Zotero bez PDF-a: *First-principles calculations for defects and impurities: Applications to III-nitrides* (Van de Walle & Neugebauer)
- śmieciowa pozycja `Tłumacz Google` w bibliotece
