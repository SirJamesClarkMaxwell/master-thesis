---
tags: [infra, setup, handoff]
---

# Brief dla Claude na PC

Czytaj razem z [[Infrastruktura_laptop_PC_serwer]]. Ten plik to zadanie; tamten to decyzje i uzasadnienia.

Autor briefu: sesja Claude Code na laptopie, 2026-10-09. Wszystko poniżej zostało zmierzone na laptopie, nie zgadnięte. Rzeczy **niesprawdzone** są oznaczone — zweryfikuj je, nie zakładaj.

---

## 1. Co to za system i po co

Trzy maszyny, każda robi jedną rzecz, której inne nie potrafią:

| maszyna | rola | dlaczego ona |
|---|---|---|
| **laptop** `laptop-3icqand4` / `100.71.58.70` | stacja robocza — pisanie pracy, Obsidian, LaTeX | jest mobilny, więc musi działać offline |
| **PC** `desktop-urd7d0v` / `100.126.10.20` | **serwer** — gateway LLM, właściciel biblioteki Zotero | stoi w domu i jest włączony, więc może świadczyć usługi |
| **klaster** (bitbucket `puntukas/sjcm_mgr`) | obliczenia VASP, źródło prawdy dla 5.5 GB wyników | tam jest moc i tam powstają dane |

Spina je **Tailscale** — połączenie laptop↔PC jest `direct` (`192.168.1.16:41641`), bez przekierowań portów, działa z dowolnej sieci. Na PC otwarte już: **22 (SSH)**, **3389 (RDP)**.

### Zasada projektowa

**Podział po typie danych, nie po maszynie. Każda warstwa ma dokładnie jednego właściciela.**

Odrzucony antywzorzec: „laptop łączy się do serwera na PC, a PC do gita". Dla *tekstu* to regres — laptop nie pracuje gdy PC śpi, nie ma pracy offline, Obsidian i LaTeX po sieci lagują, a git przestaje być kanałem synchronizacji i staje się backupem jednej maszyny. Tekst idzie do gita **z obu maszyn niezależnie**. Przez PC idzie tylko to, czego git nie uniesie.

### Pięć przepływów danych

```
1. TEKST PRACY
   laptop  <--git-->  GitHub SirJamesClarkMaxwell/master-thesis  <--git-->  PC
   Rownorzednie. Oba klony pushuja i pulluja same. 75 plikow, 15 MB.

2. WYWOLANIA LLM
   wtyczka Zotero (laptop LUB PC)
       --> http://desktop-urd7d0v:20128/v1 --> OmniRoute na PC --> provider
   Klucze API istnieja TYLKO na PC. Laptop ich nigdy nie widzi.

3. BIBLIOTEKA ZOTERO
   PC (wlasciciel) --metadane--> Zotero Sync (darmowe, bez limitu) --> laptop
   PC (wlasciciel) --pliki-----> WebDAV na PC                      --> laptop
   369 MB w storage. Darmowy limit plikow Zotero = 300 MB, wiec wlasny WebDAV.

4. DANE VASP (5.5 GB)
   klaster (zrodlo prawdy) --rsync/ssh--> PC (staging) --na zadanie--> laptop
   Nigdy do gita.

5. AGENCI / MCP
   Claude, agenci --> OmniRoute /api/mcp/stream (110 narzedzi) --> providery
                  --> zotero-mcp                                --> biblioteka + vault
```

### Dlaczego gateway w ogóle

Bez OmniRoute każda wtyczka Zotero na każdej maszynie trzyma własny klucz API — czyli N kopii sekretu, N miejsc do aktualizacji, a limity nie są wspólne. Z OmniRoute klucz jest w jednym miejscu, a wtyczki dostają endpoint.

Kluczowa sztuczka: w Zoterach na **obu** maszynach wpisujesz **ten sam** URL

```
http://desktop-urd7d0v:20128/v1
```

Nazwa Tailscale rozwiązuje się również na samym PC, więc konfiguracja wtyczek jest bajt w bajt identyczna i nie ma rozgałęzienia per maszyna. Użytkownik opisywał to jako „sync ustawień" — lepiej jest inaczej: laptop to **klient zdalnej instancji**, więc nie ma czego synchronizować.

---

## 2. Co jest już zrobione (nie powtarzaj)

- Repo `https://github.com/SirJamesClarkMaxwell/master-thesis` istnieje, `main` pushnięty.
- Zawartość repo: **tylko tekst** — 75 plików. `01_Knowledge_Base/` (vault Obsidiana), `00_Project/LaTeX/`, `00_Project/Origin/`, kilka plików w korzeniu.
- `.gitignore` jest **whitelistą** (`/*` ignoruje wszystko, potem `!` przepuszcza wybrane). Konsekwencja: **nowy katalog z danymi jest ignorowany domyślnie — to zamierzone — ale nowy katalog z tekstem trzeba dopisać ręcznie**, inaczej `git status` go nie pokaże.
- Poza repo świadomie: `00_Project/hBN/` (obliczenia + figs), `03_PDF_Library/` (39 PDF, 214 MB), `02_Zoterro/` (martwa kopia profilu Zotero z II 2026), `.venv/`.
- Zotero na laptopie: `C:\Users\fzabi\Zotero`, 75 pozycji, 70 PDF, `storage` = **369 MB**.

Na PC zacznij od:

```powershell
git clone https://github.com/SirJamesClarkMaxwell/master-thesis.git
cd master-thesis
git config pull.rebase true
```

---

## 3. Zadania, w kolejności

### Faza 0 — rozpoznanie, zero zmian

Zmierz, nie zakładaj. Zaraportuj wynik przed fazą 1:

```powershell
tailscale status
node --version; npm --version
git --version
Get-ChildItem "$env:USERPROFILE\.omniroute" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\Zotero" -ErrorAction SilentlyContinue
(Get-ChildItem "$env:USERPROFILE\Zotero\storage" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1MB
(Get-Command rclone -ErrorAction SilentlyContinue).Source
```

Pytania do rozstrzygnięcia pomiarem: czy Zotero na PC ma już bibliotekę, czy OmniRoute już jest, czy `storage` na PC różni się od 369 MB z laptopa.

**Jeśli na PC jest inna, nowsza biblioteka Zotero niż na laptopie — zatrzymaj się i zapytaj, która ma być źródłem prawdy.** Zły wybór niszczy adnotacje.

### Faza 1 — OmniRoute jako usługa na PC

OmniRoute to gateway LLM: jeden endpoint OpenAI-compatible, self-hostable, config i baza w `~/.omniroute/`, klucze szyfrowane AES-256-GCM.

1. Instalacja: `npm install -g omniroute` (alternatywy: Docker, Electron).
2. **Bind na interfejs Tailscale (`100.126.10.20`), nie na `0.0.0.0`.** To nie kosmetyka: OmniRoute trzyma wszystkie klucze API, więc `:20128` wystawiony na LAN/WAN to wyciek kluczy i kradzież limitów. Sprawdź, jak ustawia się adres nasłuchu — **niesprawdzone**, czy to flaga CLI, `.env`, czy pole w configu.
3. Klucze providerów wpisz do OmniRoute. **Nigdy do repo.** `~/.omniroute/` leży poza repo, więc whitelist i tak je blokuje, ale nie twórz plików z kluczami w drzewie repo.
4. **Autostart.** Dokumentacja nie ma instrukcji serwisu pod Windows (jest macOS menu-bar, systemd dla Arch, Podman Quadlet). Zrób Task Scheduler „at logon" albo NSSM. Bez tego gateway nie wstaje po reboocie, a laptop traci LLM-y bez żadnego komunikatu.
5. Włącz wymuszanie scope'ów MCP — jest **opt-in**, czyli domyślnie wyłączone.
6. Wygeneruj dla laptopa token `write`, **nie `admin`**.

Weryfikacja — uruchom i pokaż wyjście, nie zakładaj że działa:

```powershell
curl http://100.126.10.20:20128/v1/models
```

Potem to samo z laptopa po `omniroute connect desktop-urd7d0v`. Dopóki laptop nie dostanie odpowiedzi, faza 1 nie jest skończona.

### Faza 2 — file sync dla Zotero

**Twarda zasada: nigdy nie synchronizuj katalogu danych Zotero plikowo** — Syncthing, OneDrive, rsync, `robocopy` na `C:\Users\fzabi\Zotero`. `zotero.sqlite` się rozsypie i biblioteka pójdzie. Jedyne poprawne kanały to Zotero Sync (metadane) oraz WebDAV albo Zotero Storage (pliki).

Metadane: Zotero Sync, darmowe i bez limitu — włącz na obu maszynach, to samo konto.

Pliki: 369 MB przy darmowym limicie 300 MB. Trzy opcje:

- **WebDAV na PC** (rekomendowane — darmowe, Tailscale już stoi). Najprościej `rclone serve webdav` na katalog lokalny, z `--user`/`--pass`, nasłuch na `100.126.10.20`. Zotero: Settings → Sync → File Syncing → WebDAV → **Verify Server**. Zotero sam zrobi podkatalog `zotero`.
- Zotero Storage 2 GB (~$20/rok) — zero utrzymania, jeśli użytkownik woli zapłacić niż administrować.
- Zotero tylko na PC, laptop przez RDP (3389 już otwarty) — zero ryzyka synca, ale brak pracy offline i autotag tylko z PC.

Rekomendacja projektowa: **Zotero na obu maszynach, synkowane.** Użytkownik chce odpalać autotag z laptopa i czytać offline, więc wariant „tylko PC przez RDP" tego nie spełnia.

### Faza 3 — wtyczki Zotero

**Najpierw sprawdź, czy trzeba cokolwiek pisać.** Użytkownik chce: autotag, Ask AI, Summarize, „collect and parse my notes". To prawdopodobnie zero kodu, tylko instalacja i konfiguracja:

| cel | wtyczka | stan wiedzy |
|---|---|---|
| Ask AI, Summarize | `yilewang/llm-for-zotero` | w preferencjach ustawia się **base URL + klucz + model**; obsługuje `openai_chat_compat`, `anthropic_messages`, `gemini_native`, `responses_api` → wchodzi na OmniRoute bez kodu |
| trigger „nowy item → zrób X" | `windingwind/zotero-actions-tags` | warstwa automatyzacji na zdarzeniach (added/modified/opened/tagged), sama nie woła LLM |
| autotag z istniejącej taksonomii | `roey-angel/zotero-semantic-tagger` | woła Claude API z własnym kluczem; **czy da się podmienić endpoint na OmniRoute — NIESPRAWDZONE**, zweryfikuj w panelu ustawień i README |
| „collect and parse my notes" | `54yyyu/zotero-mcp` | MCP nad biblioteką; ma `OPENAI_BASE_URL` dla embeddingów |
| alternatywa dla Ask AI | `MuiseDestiny/zotero-gpt` | konfigurowalny base URL **NIEPOTWIERDZONY** — jeden przewodnik twierdzi że tak, README nie potwierdza |

Autotag składa się z dwóch wtyczek: `zotero-actions-tags` decyduje **kiedy**, `llm-for-zotero` dostarcza **czym**. Obie przez OmniRoute.

Własną wtyczkę pisz **dopiero** gdy wyjdzie konkretna luka, której żadna z powyższych nie zakrywa. Wtedy: **osobne repo per wtyczka**, nie w `master-thesis`. Dev na PC, bo tam żyje Zotero.

Do zweryfikowania: README OmniRoute wspomina integrację z vaultem Obsidiana (22 narzędzia MCP). Jeśli to prawda, „parse my notes" nad vaultem w `01_Knowledge_Base/` robi się bez kodu. **Nie potwierdzone** — ten fragment README nie został przeczytany.

Weryfikacja fazy: dodaj jeden item do Zotero i pokaż, że tagi pojawiły się same. Log albo zrzut — nie „powinno działać".

### Faza 4 — porządki w PDF-ach (wymaga transferu z laptopa)

Pliki są na **laptopie** w `C:\Users\fzabi\Desktop\master-theisis\03_PDF_Library`, Zotero jest na **PC**. Transfer przez Tailscale (`scp`/`rsync` po ssh). Stan ustalony pomiarem md5 na laptopie:

- **16 PDF-ów jest bit-w-bit identycznych** z plikami w Zotero storage (108 MB) → do skasowania po stronie laptopa, zero straty.
- **16 papers nie ma w Zotero wcale** (30 MB) → przenieść na PC i zaimportować. M.in. Hohenberg-Kohn 1964 „Inhomogeneous Electron Gas", Kohn-Sham 1965, Kohn Nobel Lecture, Freysoldt ×2 (`10.1103/PhysRevLett.102.016402`, `10.1002/pssb.201046289`), Komsa `10.1103/PhysRevB.86.045112`, PBE `10.1063/1.472933`, Peng `10.1103/PhysRevB.88.115201`, Maciaszek SCAN `10.1063/5.0154319`, mstar60 `10.1103/PhysRevB.106.045204`, doktorat Razinkovasa `10.15388/vu.thesis.263`, manual sxdefectalign, baza PAW/US-PP Kressego.
- **7 książek zostaje jako PDF** poza Zotero i poza gitem — Zotero to nie biblioteka książek. Thijssen, Sholl&Steckel, Cancès&Friesecke, Engel&Dreizler, Lee, Alkauskas.
- W Zotero **bez PDF-a**: *First-principles calculations for defects and impurities: Applications to III-nitrides* (Van de Walle & Neugebauer).
- Śmieciowa pozycja `Tłumacz Google` w bibliotece — skasować.

### Faza 5 — staging danych VASP

Ustal katalog na PC i ściągaj z klastra przez `rsync` po ssh. Klaster jest źródłem prawdy; PC to archiwum i staging, nie master. Do gita te dane nie wchodzą nigdy, niezależnie od tego, gdzie git stoi.

---

## 4. Czego NIE robić

1. **Nie commituj** biblioteki Zotero, `03_PDF_Library`, wyników VASP ani niczego z `~/.omniroute`. Whitelist chroni domyślnie — nie obchodź jej.
2. **Nie binduj OmniRoute na `0.0.0.0`.**
3. **Nie syncuj katalogu Zotero plikowo.** Patrz faza 2.
4. **Nie stawiaj własnego serwera git na PC.** GitHub jest offsite i przeżywa wyłączony PC, a 5.5 GB i tak do gita nie należy — self-hosted dodaje zależność i nie rozwiązuje żadnego problemu.
5. **Nie rób `git push --force`** na `main`. Historia jest już na GitHubie i laptop ją śledzi.
6. **Nie zakładaj, że coś działa.** Każda faza ma komendę weryfikującą — uruchom ją i pokaż wyjście.

## 5. Decyzje dla użytkownika, nie dla Ciebie

Zapytaj, nie wybieraj sam:

- WebDAV własny vs Zotero Storage za ~$20/rok
- czy książki (7 PDF, 74 MB) mają gdzieś być synkowane, czy zostają lokalnie na jednej maszynie
- którzy providerzy LLM wchodzą do OmniRoute i czy ma być lokalny model przez Ollamę
- czy biblioteka Zotero na PC, jeśli istnieje i różni się od laptopowej, jest nowsza
