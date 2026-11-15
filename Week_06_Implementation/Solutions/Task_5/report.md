# Report: Riešenie programovacích úloh pomocou RAG pipeline

## Priebeh

Skript `solve_tasks.py` spája výsledky predchádzajúcich úloh do jednej
pipeline. Pre každú z 10 úloh v `missing_code.json` nájde relevantné chunky,
pošle ich spolu so zadaním jazykovému modelu a vrátený kód zapíše do
cieľového súboru v `Week_06_Implementation/AI4SE_Playground`. Unit testy
repozitára sa spúšťajú pred generovaním (bez API) aj po ňom (s API) a oba
behy sa porovnajú. Pri každom volaní modelu sa zaznamená počet spotrebovaných
tokenov.

## Pipeline

1. **Obnovenie stubov** – pred každým behom sa súbory vrátia do pôvodného
   stavu zo zálohy `original_backup/`, takže každý beh začína rovnako.
2. **Testy pred** – spustí sa celá sada unit testov (`unittest`, 481 testov)
   v samostatnom procese. Výsledok sa uloží do `logs/tests_before.txt` a
   `logs/tests_before.json`.
3. **Retrieval** – z položky úlohy sa zostaví dopyt (`task_to_query` z úlohy
   4) a vyberie sa 5 najpodobnejších chunkov z vektorového storu `minilm`.
   Prázdne stuby sa vynechajú.
4. **Prompt** – obsahuje zadanie (súbor, trieda, metóda, opis), aktuálny stub
   so signatúrou a dekorátormi, 5 nájdených chunkov s ich podobnosťou a
   požiadavky na odpoveď: zachovať signatúru, nepridávať importy, dodržať
   konvencie z kódu a vrátiť iba jednu metódu v bloku ```python. Všetky
   prompty sú uložené v `logs/prompts/`.
5. **Volanie LLM** – model `gpt-5-mini` cez OpenAI API s parametrom
   `reasoning_effort=low`. Odpovede sú uložené v `logs/responses/`.
6. **Zápis kódu** – z odpovede sa pomocou `ast` vyberie definícia cieľovej
   metódy, aj keď ju model zabalil do triedy alebo doplnil textom. Ak model
   vynechal dekorátor stubu (napr. `@property`) alebo docstring, doplnia sa.
   Metóda sa vloží namiesto stubu so správnym odsadením. Súbor sa zapíše
   iba vtedy, ak je po zmene syntakticky správny. Ak sa z odpovede nedá
   kód použiť, nasleduje jeden opakovaný pokus.
7. **Testy po** – testy sa spustia znova, výsledok sa porovná s behom pred
   generovaním a zapíše sa do `logs/summary.md` a `logs/results.json`.

## Výsledky testov

| Beh | Spustené | Prešlo | Zlyhalo (FAIL) | Chyby (ERROR) |
|---|---|---|---|---|
| pred generovaním (stuby, bez API) | 481 | 429 | 35 | 17 |
| po generovaní (s API) | 481 | **467** | 1 | 13 |

Vygenerovaný kód opravil 40 testov a 2 testy, ktoré predtým prechádzali,
začali padať. Celkovo tak prechádza o 38 testov viac (97,1 % namiesto
89,2 %). Model vrátil použiteľný kód pre všetkých 10 úloh na prvý pokus,
takže opakovaný pokus nebol potrebný.

Dva „novo padajúce“ testy v skutočnosti predtým prechádzali iba náhodou.
Prázdny stub vracia `None`. Test `test_call_matches_price` porovnával dve
hodnoty `None` a `test_by_status_non_status_raises_on_first_next` očakával
`TypeError`, ktorý vznikol, keď sa zavolalo `next(None)`.

## Výsledky podľa úloh

| Úloha | Výsledok | Príčina chyby |
|---|---|---|
| `OrderStatus.is_terminal` | ✓ | |
| `InventoryLedger.__contains__` | ✗ (1 test) | opis úlohy je v rozpore s testom |
| `Warehouse.stock_report` | ✓ | |
| `OrderStateMachine.transition` | ✗ (7 testov) | chýbala trieda výnimky |
| `OrderLog.by_status` | ✗ (1 test) | chýbal test s požiadavkou na kontrolu typu |
| `Customer.can_afford` | ✓ | |
| `Order.__len__` | ✓ | |
| `BulkDiscountPricing.price` | ✗ (7 testov) | chýbal opis triedy `Money` |
| `EventBus.__contains__` | ✓ | |
| `Money.__bool__` | ✓ | |

Šesť z desiatich metód je úplne správnych. Všetky štyri chyby majú rovnakú
príčinu: medzi piatimi nájdenými chunkami chýbala informácia, ktorú model
potreboval, a model ju preto musel odhadnúť.

- **`OrderStateMachine.transition`** – model vyhodil `ValueError`, ale testy
  očakávajú `InvalidTransitionError(source, target)` z `exceptions.py`. Trieda
  je v module importovaná, no jej definícia ani test, ktorý ju používa, sa
  medzi chunky nedostali. Chyba sa prenáša aj do 3 testov `Order.advance`.
- **`BulkDiscountPricing.price`** – model použil `Money // 100`, ale trieda
  `Money` operátor `//` nepodporuje, pracuje sa s ňou cez `cents` a `*`.
  Retrieval vrátil iba metódy triedy `BulkDiscountPricing`, žiadnu z `Money`.
  Chyba sa prenáša aj do testu celkovej ceny objednávky.
- **`OrderLog.by_status`** – generátor nekontroluje typ argumentu. Že má pri
  neplatnom stave vyhodiť `TypeError`, je uvedené iba v teste, ktorý sa do
  kontextu nedostal.
- **`InventoryLedger.__contains__`** – model sa presne držal opisu („SKU s
  kladným stavom na sklade“). Test však očakáva `True` aj pri nulovom stave,
  ak SKU v evidencii ostalo. Opis v `missing_code.json` a test si tu
  odporujú, takže bez testu v kontexte nemal model ako správnu odpoveď
  odvodiť.

Tieto chyby zodpovedajú zisteniu z úlohy 4. Backend `minilm` vracia najmä
kód z tej istej triedy a test metódy našiel iba v 4 z 10 úloh. Pri
`transition`, `by_status` a `__contains__` bol test práve tou chýbajúcou
informáciou. Pri `price` by pomohlo pridávať do kontextu aj definície typov,
s ktorými metóda pracuje.

## Spotreba tokenov

Pri každom volaní sa z odpovede API zaznamenal objekt `usage`. Počty sú
priamo z API, nie odhadnuté.

| Úloha | Prompt | Odpoveď | z toho reasoning | Spolu |
|---|---|---|---|---|
| `OrderStatus.is_terminal` | 639 | 178 | 128 | 817 |
| `InventoryLedger.__contains__` | 800 | 290 | 192 | 1 090 |
| `Warehouse.stock_report` | 753 | 358 | 256 | 1 111 |
| `OrderStateMachine.transition` | 854 | 307 | 192 | 1 161 |
| `OrderLog.by_status` | 672 | 123 | 64 | 795 |
| `Customer.can_afford` | 771 | 186 | 128 | 957 |
| `Order.__len__` | 606 | 102 | 64 | 708 |
| `BulkDiscountPricing.price` | 830 | 554 | 448 | 1 384 |
| `EventBus.__contains__` | 728 | 199 | 128 | 927 |
| `Money.__bool__` | 720 | 43 | 0 | 763 |
| **spolu (10 volaní)** | **7 373** | **2 340** | **1 600** | **9 713** |

Celý beh spotreboval **9 713 tokenov**, v priemere necelých 1 000 na úlohu.
Približne tri štvrtiny tvorí prompt, teda zadanie a 5 chunkov. Z 2 340
tokenov odpovede pripadá 1 600 na interné „premýšľanie“ reasoning modelu.
Nastavenie `reasoning_effort=low` túto časť udržalo nízku. Najviac tokenov
spotrebovala úloha `BulkDiscountPricing.price`, kde model najdlhšie
premýšľal, a aj tak ju nevyriešil správne, lebo mu chýbal kontext.
Embeddingy a vyhľadávanie bežia lokálne na počítači, takže žiadne tokeny nemíňajú.

## Výstupy

| Súbor | Obsah |
|---|---|
| `solve_tasks.py` | celá pipeline |
| `logs/tests_before.txt`, `.json` | testy pred generovaním |
| `logs/tests_after.txt`, `.json` | testy po generovaní |
| `logs/summary.md` | porovnanie testov a tabuľka tokenov |
| `logs/results.json` | všetky údaje o behu vrátane vygenerovaného kódu |
| `logs/prompts/`, `logs/responses/` | prompty a odpovede modelu pre každú úlohu |

Vygenerované metódy sú zapísané priamo v súboroch
`AI4SE_Playground/playground/playground/*.py`.

## Spustenie

```powershell
pip install -r requirements.txt
python solve_tasks.py --baseline                 # iba testy pred, bez API
python solve_tasks.py --dry-run                  # iba prompty, bez API
python solve_tasks.py --reasoning-effort low     # celý beh (gpt-5-mini)
python solve_tasks.py --reset                    # obnovenie stubov
```
API kľúč sa načíta z premennej `OPENAI_API_KEY` alebo zo súboru `.env`
(git ho ignoruje). Model sa dá zmeniť parametrom `--model` na ktorýkoľvek z
modelov povolených v zadaní.
