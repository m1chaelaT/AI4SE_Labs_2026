# Report: Návrh pipeline na generovanie kódu so znalosťou repozitára

## Východisko

Pipeline z úloh 2 až 5 (AST chunky, embeddingy MiniLM, top 5 podľa
kosínusovej podobnosti, jedno volanie `gpt-5-mini`) vyriešila úplne
správne 6 z 10 metód a zvýšila počet prechádzajúcich testov zo 429 na 467 z
481. Pri všetkých štyroch chybných metódach mal model k dispozícii kód, ale
chýbala mu konkrétna informácia, ktorú musel odhadnúť:

| Metóda | Čo chýbalo v kontexte | Kde sa informácia nachádzala |
|---|---|---|
| `OrderStateMachine.transition` | trieda `InvalidTransitionError` | import na začiatku `orders.py`, test `test_transition_illegal_raises` |
| `BulkDiscountPricing.price` | operácie triedy `Money` | typová anotácia `-> Money` v podpise metódy, trieda v `models.py` |
| `OrderLog.by_status` | požiadavka vyhodiť `TypeError` | test `test_by_status_non_status_raises_on_first_next` |
| `InventoryLedger.__contains__` | presné správanie pri nulovom stave | test `test_contains_present_even_if_zero_on_hand_after_commit` |

Chyby teda nespôsobil slabý model, ale to, že sa do promptu nedostal
správny kontext. Návrh sa preto sústreďuje hlavne na výber kontextu.

## Je porovnávanie embeddingov najlepšia stratégia?

Ako jediný mechanizmus nie. Embeddingy hľadajú text, ktorý je *podobný*
zadaniu. Pri generovaní kódu však model potrebuje predovšetkým kód, ktorý so
zadaním *súvisí*: typy z podpisu metódy, importované výnimky, volané metódy
a testy, ktoré metódu používajú. Tieto väzby sa dajú zistiť priamo z kódu (z importov a typov v
podpise), netreba ich odhadovať podľa podobnosti. V
našom prípade by stačilo prečítať importy a typové anotácie cieľového modulu
a model by dostal `InvalidTransitionError` aj `Money` s istotou.

Úloha 4 ukázala aj ďalšiu slabinu: rôzne metódy vyhľadávania nachádzajú
rôzne veci. MiniLM našiel kód cieľovej triedy v 10 z 10 úloh, ale test
metódy iba v 4 z 10. LSA, ktoré porovnáva rovnaké slová, malo pomer 9/10 a
9/10, no pri `is_terminal` vrátilo iba testy bez definície enumu.
Embeddingy sú užitočné ako doplnok, ktorý nájde podobný kód, aj keď s
cieľovou metódou priamo nesúvisí (napr. `__len__` iných tried ako vzor).
Najlepšie je kombinovať ich s vyhľadávaním podľa zhody názvov (napr. BM25).

## Bolo by lepšie iné množstvo chunkov?

Pevný počet chunkov nie je ideálny, lebo chunky majú veľmi rôznu dĺžku (od
2 do 55 riadkov). Lepšie je určiť **limit tokenov** pre kontext a napĺňať ho
podľa dôležitosti: najprv povinný kontext, potom výsledky vyhľadávania, kým
sa limit nenaplní. V úlohe 5 mal prompt približne 600
až 850 tokenov, takže aj malé modely by zniesli kontext niekoľkonásobne
väčší.

Pri takomto malom repozitári treba zvážiť aj úplne iný prístup. Celý
zdrojový kód balíka má približne 52 000 znakov, teda rádovo 13 000 tokenov,
a zmestí sa do kontextového okna súčasných modelov. Retrieval je nutný až
pri repozitároch, ktoré sa do kontextu nezmestia, prípadne keď treba
výrazne šetriť tokeny. Pre malý projekt by bolo najjednoduchšie a
najspoľahlivejšie poslať modelu celý cieľový súbor a stručnú „mapu“ zvyšku
repozitára.

## Malo by byť delenie na chunky sofistikovanejšie?

Delenie podľa AST z úlohy 2 je dobrý základ, lebo nikdy nepreseká metódu.
Chunky by však nemali byť iba plochým zoznamom kúskov textu. Užitočnejšie by bolo uložiť chunky po úrovniach a zaznamenať aj väzby
medzi nimi:

- **Úrovne:** súbor → trieda (kostra s podpismi) → metóda. Podľa potreby sa
  dá vybrať celá trieda alebo iba jej kostra.
- **Väzby z kódu:** importy, typy v podpisoch, volané metódy, dedičnosť.
- **Väzby z testov:** ktoré testy volajú ktorú metódu, zistené z volaní ako
  `self.ledger.__contains__` alebo `"EL-1001" in self.ledger` a z názvov
  testov.
- **Mapa repozitára:** podpisy všetkých tried a metód v niekoľkých stovkách
  tokenov, aby model mal prehľad o celom repozitári bez toho, aby videl všetok kód.

## Navrhovaná pipeline

```text
1. Indexovanie (raz pre celý repozitár)
   triedy, metódy, importy, väzby test -> metóda, mapa repozitára,
   index na vyhľadávanie
        |
        v
2. Zostavenie kontextu (pre každú úlohu)
   povinné: cieľová trieda, testy metódy, použité typy a výnimky
   + mapa repozitára + výsledky vyhľadávania do limitu tokenov
        |
        v
3. Generovanie
   LLM vráti metódu -> kontrola syntaxe -> zápis do súboru
        |
        v
4. Overenie a oprava (max. k pokusov)
   spustiť testy metódy -> pri chybe poslať modelu chybovú hlášku
   -> nová verzia -> na konci celá sada testov
```

1. **Indexovanie.** Skript raz prejde celý repozitár a zaznamená všetky triedy a
   metódy s podpismi a docstringmi, čo ktorý modul importuje a ktoré metódy
   volá, a ktoré testy testujú ktorú metódu. Popri tom vytvorí index na
   vyhľadávanie (BM25 + embeddingy).
2. **Zostavenie kontextu.** Pre každú úlohu sa najprv
   pridajú informácie, ktoré sú potrebné takmer vždy: cieľová trieda celá,
   všetky testy cieľovej metódy a definície typov, ktoré metóda používa
   alebo ktoré modul importuje. Nasleduje mapa repozitára. Zvyšok limitu tokenov sa doplní výsledkami vyhľadávania.
3. **Generovanie.** Rovnako ako v úlohe 5: model vráti jednu metódu, tá sa
   overí cez `ast` a vloží do súboru.
4. **Overenie a oprava.** Spustia sa testy cieľovej metódy. Ak zlyhajú,
   traceback sa vráti modelu ako spätná väzba a model dostane ďalší pokus.
   Napríklad správa `AssertionError: InvalidTransitionError not raised` by
   modelu priamo povedala, akú výnimku má použiť. Na konci sa spustí celá
   sada testov, aby sa odhalili regresie v iných častiach kódu.

Ďalším krokom by bolo nahradiť pevne daný postup agentom, ktorý má nástroje
na čítanie súborov, vyhľadávanie (`grep`) a spúšťanie testov a sám
rozhoduje, čo potrebuje vidieť. Takto fungujú súčasní kódoví asistenti
vrátane Copilota, ktorý v úlohe 1 naklonoval repozitár.

## Očakávaný prínos

| Chyba z úlohy 5 | Komponent, ktorý ju rieši |
|---|---|
| `transition` vyhadzuje `ValueError` | importované výnimky v povinnom kontexte, test metódy, spätná väzba z testov |
| `price` používa `Money // int` | definícia typu `Money` z podpisu metódy |
| `by_status` nekontroluje typ | testy metódy v povinnom kontexte |
| `__contains__` podľa opisu, nie podľa testu | testy metódy, spätná väzba z testov |

## Obmedzenia

- **Cena.** Väčší kontext a slučka opráv zvyšujú spotrebu tokenov. V úlohe
  5 stál jeden pokus asi 1 000 tokenov, pri troch pokusoch s väčším
  kontextom by to mohlo byť niekoľkonásobne viac. Na druhej strane by
  odpadli neúspešné pokusy, ktoré tokeny minuli zbytočne, ako pri
  `BulkDiscountPricing.price`.
- **Závislosť od testov.** Pipeline sa opiera o existujúce testy. Ak testy
  chýbajú alebo sú neúplné, ostáva iba statická analýza a vyhľadávanie.
  Existuje aj riziko, že model kód „prispôsobí testom“ namiesto toho, aby
  implementoval zamýšľané správanie.
- **Rozpory v zadaní.** Pri `__contains__` si opis a test odporujú. Pipeline
  by mala test brať ako zdroj pravdy, ale zároveň takýto rozpor nahlásiť
  človeku, namiesto toho aby ho potichu vyriešila.

## Záver

Pre generovanie kódu so znalosťou repozitára je najdôležitejšie *čo* sa do
kontextu dostane. Na to sú lepšie väzby, ktoré sa dajú z kódu zistiť presne, než podobnosť
embeddingov. Navrhovaná pipeline preto kombinuje tri veci: kontext zistený priamo z
kódu, doplnkové vyhľadávanie do limitu tokenov a overenie testami, ktorých
chyby sa vrátia modelu. Všetky štyri chyby z úlohy 5 by riešila aspoň jedna z
týchto zložiek. Pri malých repozitároch, ako je AI4SE_Playground, je
navyše namieste zvážiť, či retrieval vôbec potrebujeme, keď sa celý zdrojový
kód zmestí do kontextu modelu.
