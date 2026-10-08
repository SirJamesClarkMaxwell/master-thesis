<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Przygotuj plan przeglądu literatury do rozdziału pracy magisterskiej dotyczącego technologii kwantowych opartych na defektach punktowych w heksagonalnym azotku boru (h-BN).

Interesuje mnie fizyka działania następujących technologii kwantowych:
quantum sensing
quantum memory
verification / tests of quantum theory
quantum key distribution
quantum random number generator
lasery oparte na defektach
koncepcja „defect-as-a-device”
Dodatkowo:
Znajdź artykuły (przeglądowe oraz szczegółowe) dotyczące fizycznych mechanizmów działania powyższych technologii — najlepiej takie, które opisują ogólną fizykę zjawisk (optyka kwantowa, spin–photon interface, dynamika układów otwartych, przejścia międzyukładowe, koherencja, sprzężenie spin–fonon itd.) bez silnego odnoszenia się do konkretnego materiału czy konkretnego defektu.
Celem jest uzyskanie „god’s eye view” na fizykę zjawisk wykorzystywanych w tych technologiach, aby następnie móc odnieść je do przypadku multiwakansów zanieczyszczonych węglem w h-BN w mojej pracy magisterskiej.
Punktem odniesienia są przeglądy:
Çakan et al., Quantum Optics Applications of Hexagonal Boron Nitride Defects (Adv. Optical Materials, 2025)
Aharonovich et al., Quantum Emitters in Hexagonal Boron Nitride (Nano Lett. 2022)
Uwzględnij również literaturę cytowaną w tych pracach.

Poniżej masz propozycję struktury przeglądu literatury + listę kluczowych artykułów „ogólnofizycznych”, które możesz potraktować jako bazę do zbudowania „god’s eye view”, a dopiero potem dociążyć je h‑BN i konkretnymi defektami.

***

## Proponowany plan rozdziału (przegląd literatury)

### 1. Wprowadzenie: defekty punktowe jako platforma technologii kwantowych

- Krótka charakterystyka defektów punktowych w ciałach stałych (poziomy zlokalizowane w przerwie energetycznej, stany spinowe, sprzężenie z fotonami i fononami).
- Motywacja: dlaczego defekty w h‑BN są interesujące w kontekście technologii kwantowych (2D, integracja fotoniczna, szeroka przerwa energetyczna, jasne emitery, dostęp do stanów spinowych).
- Odniesienie do przeglądów h‑BN (Aharonovich 2022, Çakan 2025) plus przeglądy ogólne o defektach jako kubitach.[^1][^2][^3][^4]


### 2. Ogólny model fizyczny defektu jako układu kwantowego

2.1. Struktura poziomów energii i przejścia optyczne

- Model kilku poziomów (np. konfiguracja Λ, V, układ trójpoziomowy z przejściami międzyukładowymi).
- ZPL, czynniki Huang–Rhysa i Debye–Wallera, boczne pasma fononowe, rola sprzężenia elektron–fonon.[^4]

2.2. Fizyka spinowa

- Hamiltonian spinu defektu: pola magnetyczne, rozszczepienie w zerowym polu, sprzężenie hiperfajne z jądrami.
- Koherencja i relaksacja: $T_1$, $T_2$, $T_2^*$, mechanizmy dekoherencji (spin–spin, spin–fonon, szum ładunkowy).[^3][^5][^6]

2.3. Dynamika układów otwartych

- Opis w formalizmie Lindblada / master equation, kanały rozpraszania (emisja spontaniczna, ISC, dekoherencja czysto fazowa).
- Związek pomiędzy parametrami master equation a mierzalnymi wielkościami (widma PL, kontrast ODMR, czas życia, widma szumów).[^5][^6]

***

### 3. Spin–photon interface i podstawy optyki kwantowej defektów

3.1. Kryteria „dobrego” defektu jako emitera/łącznika spin–foton

- Silne przejście optyczne (duża oscylator strength, duży DW), wąska linia, minimalne migotanie ładunkowe.
- Czasy koherencji spinu, selektywne reguły wyboru dla przejść zależnych od stanu spinowego.[^7][^3][^4]

3.2. Defekt w rezonatorze / falowodzie

- Reżimy sprzężenia: Purcell, strong coupling, cooperativity $C$, efektywność zbierania fotonów.
- Przykłady realizacji spin–photon interface (QD, centra w diamencie, centra grupy IV), które można traktować jako „modelowe” dla defektów w h‑BN.[^8][^9][^7]

3.3. Mechanizmy generacji i detekcji pojedynczych fotonów

- Statystyka fotonów (funkcja korelacji $g^{(2)}(\tau)$), antygrupowanie jako definicja emitera pojedynczych fotonów.
- Schematy pomiarowe: konfokalna mikroskopia PL, pomiary czasowo‑skorelowane, interferometria Hong–Ou–Mandel.[^10][^4]

***

### 4. Quantum sensing z defektami spinowymi

4.1. Ogólne zasady quantum sensing na spinie defektu

- Defekt spinowy jako czuły magnetometr / termometr / czujnik pola elektrycznego: zależność częstotliwości rezonansu spinowego od wielkości mierzonych.
- Protokoły: Ramsey, spin echo, sekwencje DD, korelowane pomiary wielospinowe.[^6][^5]

4.2. Czynniki ograniczające czułość i rozdzielczość

- Rola koherencji spinu, kontrastu ODMR, czasu akwizycji; limit standard quantum limit vs metody wykorzystujące splątanie.
- Wpływ sprzężenia spin–fonon i szumu magnetycznego otoczenia.[^11][^5][^6]

4.3. Quantum sensing w materiałach 2D (kontekst h‑BN)

- Specyfika defektów w warstwach vdW (nieekranowane pola, głębokie poziomy, możliwość zbliżenia do badanej próbki).
- Przykładowe aplikacje: detekcja fal spinowych, pola magnetycznego cienkich warstw ferromagnetyków – jako inspiracja dla h‑BN.[^12][^13][^11]

***

### 5. Quantum memories oparte na defektach

5.1. Podstawowa architektura pamięci spinowej

- Qubit komunikacyjny (elektronowy) + rejestr pamięci (spiny jądrowe lub inne defekty), schematy $\Lambda$ i Raman.
- Wymagania: długie $T_2$ (nawet w ms–s), kontrolowalne sprzężenie hiperfajne, możliwość adresowania selektywnego.[^14][^8]

5.2. Mechanizmy transferu stanu i przechowywania

- Mapowanie stanu fotonu na spiny (spójne przejścia, adiabatyczne STIRAP, echo spinowe).
- Wpływ dynamiki układów otwartych i szumów na wierność pamięci.[^15][^14]

5.3. Defekty jako elementy węzłów sieci kwantowych

- Koncepcja repeaterów kwantowych z defektami jako pamięciami i interfejsami fotonowymi.
- Przeglądy dotyczące implementacji w diamencie i SiC jako „template” dla przyszłych architektur w h‑BN.[^8][^14]

***

### 6. Testy teorii kwantów i podstawy (verification/tests of quantum theory)

6.1. Defekty jako platforma do testowania fundamentalnych zjawisk

- Generacja i pomiar splątania spin–spin i spin–foton w oparciu o defekty, nierówności Bella, steering, contextuality.
- Rola wysokiej wierności spin–photon interface w testach nielokalności.[^16][^7]

6.2. Otwarte układy kwantowe i dekoherencja jako „test” środowiskowy

- Precyzyjna tomografia kanałów dekoherencji z wykorzystaniem defektów jako sond otoczenia.
- Korelowane sensing networks jako narzędzie do badania korelacji środowiskowych.[^17][^16]

***

### 7. Quantum key distribution (QKD) z emiterami defektowymi

7.1. Wymagania QKD wobec źródeł światła

- Deterministyczne pojedyncze fotony vs źródła oparte na parametrycznej konwersji, znaczenie braku emisji wielofotonowej.
- Stabilność częstotliwościowa, możliwość pracy w telekom, integracja z fotoniką na chipie.[^18][^7]

7.2. Protokoły QKD z defektami

- Schematy oparte na polaryzacji / czasie przylotu fotonów z emitera, potencjalne zastosowanie defektów 2D jako zintegrowanych źródeł.
- Związek z architekturami sieci kwantowych (emitery + pamięci).[^19][^7]

***

### 8. Quantum random number generators (QRNG) oparte na defektach

8.1. Mechanizmy generacji losowości kwantowej

- Losowy czas emisji pojedynczych fotonów, losowy wynik pomiaru stanu spinowego, losowy wybór ścieżki interferometrycznej.
- Znaczenie certyfikowalności losowości (device‑independent, semi‑device‑independent).[^20][^21]

8.2. Przykłady QRNG z centrami barwnymi

- Demonstracje QRNG z centrami NV jako wzorzec (statystyki, stabilność, modelowanie entropii).
- Jakie parametry defektu są kluczowe (jasność, afterpulsing detektora, kontrola stanów defektu).[^21][^20]

***

### 9. Lasery i „defect‑based gain” w ciałach stałych

9.1. Ogólne mechanizmy lasingu w oparciu o centra barwne

- Warunki inwersji obsadzeń w układzie defektowym, rola poziomów metastabilnych i ISC.
- Sprzężenie z wnęką (Q, V, próg lasingu) i znaczenie rozmycia fononowego linii.[^4]

9.2. Potencjał defektów 2D (w tym h‑BN) do implementacji mikrolaserów

- Dyskusja na poziomie fizyki: wymagania co do gęstości defektów, nieprzezroczystości, strat.
- Koncepcje hybrydowe (defekt w h‑BN osadzony na/ w rezonatorze dielektrycznym lub plazmonicznym).[^22][^4]

***

### 10. Koncepcja „defect‑as‑a‑device”

10.1. Od „defektu jako niepożądanej nieczystości” do „defektu jako funkcjonalnego elementu”

- Przeglądy/„guidelines” jak projektować defekty pod konkretną funkcję (sensory, interfejsy, pamięci).[^23][^3][^4]

10.2. Kryteria inżynierii defektów dla różnych zastosowań

- Dla quantum sensing: duże sprzężenie z polem zewnętrznym (magnetycznym, elektrycznym), długi $T_2$.
- Dla komunikacji/QKD: duży DW, małe broadening, kompatybilność z telekom.
- Dla pamięci: silne sprzężenie hiperfajne z jądrami, możliwość adresowania wielospinowego rejestru.[^3][^6][^14]

10.3. Miejsce h‑BN i multiwakansów C‑zanieczyszczonych w tym krajobrazie

- Jakie cechy znanych defektów „idealnych” (NV, SiV, defekty w SiC) są pożądane i które z nich są potencjalnie osiągalne w kompleksach C‑V w h‑BN.
- Odniesienie do strategii „rational design” emitera (modele sprzężenia elektron–fonon, kompromisy między długością fali a wydajnością).[^24][^25][^4]

***

## Kluczowe artykuły (głównie „materials‑agnostic”)

Poniżej lista, którą możesz wpleść w odpowiednie sekcje (podałem typ i przybliżoną rolę, DOIs znajdziesz bez problemu po tytułach):

### Ogólne „guidelines” i przeglądy defektów

- Doherty et al., „Qubit guidelines for solid‑state spin defects” (2020) – bardzo dobry przekrojowy przewodnik po wymaganiach, parametrach i modelowaniu defektów jako kubitów.[^3]
- „A Concise Primer on Solid‑State Quantum Emitters” – przegląd podstaw optyki kwantowej emiterów, metryk (g^(2), indistinguishability, coupling do rezonatorów).[^10]
- „Rational design of efficient defect‑based quantum emitters” (AIP Appl. Phys. 2024) – model sprzężenia elektron–fonon, kompromisy między długością fali a wydajnością, bardzo przydatne do dyskusji DW/Huang–Rhys.[^4]
- „Quantum Sensing with Spin Defects Beyond Diamond” (ACS Nano, 2025) – porównanie NV, SiC, h‑BN, GaN pod kątem sensingowym.[^6]


### Quantum sensing

- „Quantum sensing with spin defects: principles, progress, and perspectives” (Adv. Photonics 2025, przegląd) – uniwersalna podstawa teoretyczna + praktyczne protokoły.[^5]
- „Quantum Sensing with Spin Defects Beyond Diamond” – jw., kładzie nacisk na magnetometrię/elektrometrię/termometrię.[^6]
- „Quantum sensing with optically accessible spin defects in van der Waals layered materials” (Light: Sci. Appl. 2024) – specyficznie o 2D, dobra baza dla sekcji o h‑BN.[^11]
- Prace o sensing fal spinowych i lokalnych pól (np. „Sensing spin wave excitations by spin defects in few‑layer‑thick hexagonal boron nitride”) – jako przykład aplikacji i benchmarku dla Twojej dyskusji.[^13]


### Spin–photon interface, sieci, pamięci

- „Quantum Networks with Deterministic Spin–Photon Interfaces” (QUTE review 2019, raport) – przegląd architektur sieci, interfejsów i zastosowań (QKD, repeatery).[^26][^7]
- „Building Blocks for Quantum Network Based on Group‑IV Split‑Vacancy Centers in Diamond” (Adv. Quantum Technol. 2019) – przegląd wymagań na pamięci, interfejsy itp., materiał‑agnostic.[^8]
- „High‑throughput assessment of defect‑nuclear spin register controllability for quantum memory applications” (2024) – teoretyczna analiza wymagań na rejestry jądrowe.[^14]


### Dynamika układów otwartych i optyka kwantowa

- Rozdział/przegląd w „Quantum sensing with spin defects” oraz „Qubit guidelines…” – mają sekcje z master equations, ISC, spin–phonon, noise spectra.[^5][^3]
- Dodatkowo możesz sięgnąć do standardowych monografii typu Breuer–Petruccione, ale w rozdziale magisterskim wystarczy, że oprzesz formalizm na tych przeglądach.


### QRNG, QKD

- Herrero‑Collantes \& Garcia‑Escartin, „A Comprehensive Review of Quantum Random Number Generators” (ACM Computing Surveys) – przegląd mechanizmów QRNG, z sekcją o źródłach jednofotonowych.[^21]
- „Single Photon Randomness based on a Defect Center in Diamond” – konkretna demonstracja QRNG na NV, świetna jako „template” dla sekcji defektowej.[^20]
- Przeglądy QKD + nowoczesne prace o chipowych SI‑QRNG można przywołać, aby pokazać, jakie wymagania stawiają protokoły wobec źródeł i detektorów.[^19]


### „Defect‑as‑a‑device”

- „Qubit guidelines for solid‑state spin defects” – ma czytelne kryteria projektowe („design rules”).[^3]
- „Comprehensive Scheme for Identifying Defects in Solid‑State Quantum Systems” – metodologia łączenia DFT z wymaganiami funkcjonalnymi (dobry pomost do Twoich obliczeń ab initio).[^27][^23]
- „Rational design of efficient defect‑based quantum emitters” – jw., wprost w duchu „defect‑as‑a‑device”.[^4]

***

## Jak wpiąć Çakan 2025 i Aharonovich 2022

- Na początku rozdziału (sekcja 1) jasno napisz, że Twoja praca rozwija linię przeglądu Çakan i Aharonovicha, ale idziesz bardziej „materials‑agnostic”:
– z Çakan 2025 weź klasyfikację aplikacji w h‑BN (sensing, QKD, quantum memory, QRNG, lasery, etc.) i potraktuj ją jako „mapę zastosowań”,
– z Aharonovich 2022 weź podsumowanie obecnego stanu strukturalnej identyfikacji defektów i inżynierii materiałowej.[^2][^1]
- W każdej z sekcji 4–10 możesz mieć podsekcję typu „Implementacje w h‑BN”, w której odsyłasz do konkretnych części Çakan/Aharonovich oraz do bardziej szczegółowych prac cytowanych tam (np. spinowe VB⁻, centra C‑zanieczyszczone, integracja z falowodami).[^28][^1][^2]

***

## Minimalny „core reading list” (do pierwszego przejrzenia)

Jeśli masz czas na przejrzenie tylko kilku tekstów, które zbudują Ci „god’s eye view”, to:

- Çakan et al., Adv. Optical Mater. 2025 (h‑BN, aplikacje).[^2]
- Aharonovich et al., Nano Lett. 2022 (emitory w h‑BN).[^1]
- Doherty et al., „Qubit guidelines for solid‑state spin defects”.[^3]
- „Quantum sensing with spin defects: principles, progress, and perspectives” (Adv. Photonics).[^5]
- „Quantum Sensing with Spin Defects Beyond Diamond” (ACS Nano).[^6]
- „Rational design of efficient defect‑based quantum emitters”.[^4]
- „Quantum Networks with Deterministic Spin–Photon Interfaces”.[^7][^26]
- „A Comprehensive Review of Quantum Random Number Generators”.[^21]

Na bazie tych prac możesz wypełnić każdy z podrozdziałów fizycznymi mechanizmami (Hamiltoniany, kanały Lindblada, role fononów, reguły wyboru), a następnie w osobnych fragmentach odnieść je do konkretnych defektów C‑multiwakansowych w h‑BN, korzystając z literatury strukturalno‑obliczeniowej, którą już zbierasz.
<span style="display:none">[^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60]</span>

<div align="center">⁂</div>

[^1]: Aharonovich - Quantum Emitters in Hexagonal Boron Nitride 1.pdf

[^2]: Advanced Optical Materials - 2025 - Çakan - Quantum Optics Applications of Hexagonal Boron Nitride Defects(1).pdf

[^3]: https://arxiv.org/ftp/arxiv/papers/2010/2010.16395.pdf

[^4]: https://pubs.aip.org/aip/app/article/9/6/066117/3299506/Rational-design-of-efficient-defect-based-quantum

[^5]: https://www.researching.cn/ArticlePdf/m00090/2025/7/6/064002.pdf

[^6]: https://pubs.acs.org/doi/10.1021/acsnano.5c00802

[^7]: http://arxiv.org/pdf/1811.08242v1.pdf

[^8]: https://advanced.onlinelibrary.wiley.com/doi/10.1002/qute.201900069

[^9]: https://arxiv.org/abs/1906.10721

[^10]: https://arxiv.org/html/2506.06684v1

[^11]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11535532/

[^12]: http://arxiv.org/pdf/2405.00802.pdf

[^13]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11062567/

[^14]: https://arxiv.org/html/2405.10778v2

[^15]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12133220/

[^16]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10914733/

[^17]: https://arxiv.org/abs/2212.01481

[^18]: https://www.semanticscholar.org/paper/cd10c5838248b6d5e958e929d2cb10ff9a643fbe

[^19]: https://www.nature.com/articles/s42005-024-01917-x

[^20]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6895230/

[^21]: https://arxiv.org/html/2203.00261v3

[^22]: https://pubs.acs.org/doi/10.1021/acs.nanolett.3c04301

[^23]: https://arxiv.org/abs/2305.17889

[^24]: Carbon dimer.pdf

[^25]: Babar - Carbon-contaminated topological defects.pdf

[^26]: https://onlinelibrary.wiley.com/doi/abs/10.1002/qute.201800091

[^27]: https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.3c01475

[^28]: https://pubs.acs.org/doi/abs/10.1021/acsnano.5c00802

[^29]: Zobelli - Vacancy migration.pdf

[^30]: Baur_--_Modelowanie_ab-initio_powstawania_kompleksow_C-V-H_w_h-BN(1)-1.pdf

[^31]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10444786/

[^32]: https://arxiv.org/pdf/2310.02709.pdf

[^33]: http://arxiv.org/pdf/2312.02894.pdf

[^34]: https://www.spiedigitallibrary.org/journals/advanced-photonics/volume-7/issue-6/064002/Quantum-sensing-with-spin-defects--principles-progress-and-prospects/10.1117/1.AP.7.6.064002.full

[^35]: https://www.nature.com/articles/s41377-024-01630-y

[^36]: https://www.cqt.sg/highlight/2024-08-spins-quantum-sensing/

[^37]: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1270602/full

[^38]: https://pubs.acs.org/doi/abs/10.1021/acs.nanolett.9b02443

[^39]: http://publicationslist.org/data/r.j.warburton/ref-666/Appel_PRL_2021.pdf

[^40]: https://www.nature.com/articles/s41467-025-64780-6

[^41]: https://www.semanticscholar.org/paper/89b1eda56b8913de950a1028fe252e65eb23f5d5

[^42]: https://www.semanticscholar.org/paper/1fb065b41088b62f512b647c5406c518cbde849a

[^43]: https://www.tandfonline.com/doi/full/10.1080/00018732.2019.1590295

[^44]: https://www.degruyterbrill.com/document/doi/10.1515/nanoph-2019-0092/html

[^45]: https://www.semanticscholar.org/paper/a8637bbf770164cb58785ab65026aecf8db2ab89

[^46]: https://www.ijeast.com/papers/175-179,Tesma405,IJEAST.pdf

[^47]: https://www.semanticscholar.org/paper/f12dc6c9ded7e232dbe8c8ca185ce30bf38b9da9

[^48]: https://onlinelibrary.wiley.com/doi/10.1002/pssa.201900834

[^49]: https://arxiv.org/ftp/arxiv/papers/1906/1906.10721.pdf

[^50]: https://arxiv.org/pdf/2206.01223.pdf

[^51]: http://link.aps.org/pdf/10.1103/PhysRevApplied.11.044036

[^52]: https://arxiv.org/ftp/arxiv/papers/2306/2306.13025.pdf

[^53]: https://arxiv.org/pdf/2503.23593.pdf

[^54]: https://arxiv.org/pdf/1710.03265.pdf

[^55]: https://arxiv.org/pdf/1506.06036.pdf

[^56]: https://www.science.org/doi/10.1126/science.ady8677

[^57]: https://ui.adsabs.harvard.edu/abs/2019PhRvP..11d4036D/abstract

[^58]: http://arxiv.org/abs/1906.10721

[^59]: https://journals.aps.org/prapplied/pdf/10.1103/PhysRevApplied.11.044036

[^60]: http://pubs.acs.org/doi/abs/10.1021/acs.jpclett.3c01475

