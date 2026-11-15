# Report: Vyhľadanie najrelevantnejších chunkov k úlohe

## Priebeh

Skript `retrieve.py` načíta vektorový store z úlohy 3, prevedie vstupnú
úlohu na embedding rovnakým modelom, akým vznikli embeddingy chunkov, a
vráti *n* chunkov s najvyššou podobnosťou. Okrem samostatného dopytu z
príkazového riadka vie skript vyhodnotiť všetkých 10 úloh zo súboru
`missing_code.json` naraz (`--eval`). Trieda `Retriever` a funkcia
`task_to_query` sa v úlohe 5 importujú priamo z tohto skriptu.

## Miera podobnosti

Ako miera podobnosti je zvolená **kosínusová podobnosť**. Porovnáva smer
vektorov, nie ich dĺžku, takže krátky chunk (napr. jednoriadkový getter) nie
je znevýhodnený oproti dlhšiemu. Modely `sentence-transformers` vrátane
MiniLM sú navyše trénované práve na nej. Keďže všetky embeddingy sú od
úlohy 3 L2-normalizované, kosínusová podobnosť sa zjednoduší na skalárny
súčin a podobnosti dopytu so všetkými chunkami sa vypočítajú jedným
násobením matice a vektora:

```python
scores = self.matrix @ q          # (798 × 384) · (384,) -> 798 podobností
```

## Výber n najlepších

Z vypočítaných podobností sa *n* najlepších vyberie funkciou
`np.argpartition` a zoradí sa iba týchto *n* chunkov. Dopyt sa porovná so
všetkými chunkami. Pri 798 chunkoch je to okamžité a výsledok je vždy
presný. Špeciálne knižnice na rýchle približné vyhľadávanie (napr. FAISS) sa
oplatia až pri veľmi veľkom počte chunkov. Tu by iba pridali ďalšiu
závislosť a mohli by vynechať najlepší výsledok.

Predvolená hodnota je *n* = 5, rovnaká ako v úlohe 5. Je to dosť na to, aby
sa do promptu dostal kód okolitej triedy aj testy, a zároveň dosť málo na
to, aby kontext ostal krátky aj pre malé modely.

## Filtrovanie

Pred výberom sa niektoré chunky vylúčia, aby nezaberali miesto medzi *n*
výsledkami:

| Parameter | Účinok |
|---|---|
| `skip_stubs=True` (predvolené) | vynechá prázdne metódy s `is_stub: true` z úlohy 2 |
| `kinds` | ponechá iba vybrané typy chunkov, napr. `{"method", "class"}` |
| `exclude_ids` | vynechá konkrétne chunky podľa `id` |
| `min_score` | zahodí výsledky pod zvolenou hranicou podobnosti |

Filter stubov je dôležitý. Bez neho by sa prázdna cieľová metóda (napr.
`def __len__(self) -> int: pass`) objavovala medzi najlepšími výsledkami,
lebo sa s dopytom zhoduje názvom, ale modelu by neposkytla nijaký užitočný
kód.

## Dopyt

Funkcia `task_to_query` zostaví z položky v `missing_code.json` text v
rovnakom tvare, aký majú chunky v úlohe 3: typ a umiestnenie, identifikátory
rozložené na slová a docstring. Dopyt a chunky sú tak napísané v rovnakom
tvare:

```text
method Customer.can_afford in playground/playground/models.py
playground playground models py customer can afford
Return True if ``balance + total`` does not exceed the credit limit.
```

## Vyhodnotenie

Pre každú úlohu z `missing_code.json` sa sleduje, či sa medzi piatimi
vrátenými chunkami nachádza aspoň jeden chunk z cieľovej triedy a aspoň
jeden unit test cieľovej metódy. Úplné výsledky sú v súbore
`eval_<backend>.json`.

**Backend `lsa`:** kód cieľovej triedy v 9/10 úloh, test metódy v 9/10 úloh.

| Úloha | Trieda | Test | Poznámka |
|---|---|---|---|
| `OrderStatus.is_terminal` | ✗ | ✓ | všetkých 5 výsledkov sú testy, chýba definícia enumu |
| `InventoryLedger.__contains__` | ✓ | ✗ | `add_stock`, `available`, `__len__` |
| `Warehouse.stock_report` | ✓ | ✓ | |
| `OrderStateMachine.transition` | ✓ | ✓ | `can_transition`, `allowed_from` a 2 testy |
| `OrderLog.by_status` | ✓ | ✓ | 3 testy a hlavička triedy |
| `Customer.can_afford` | ✓ | ✓ | |
| `Order.__len__` | ✓ | ✓ | nájde aj `__len__` iných tried ako vzor |
| `BulkDiscountPricing.price` | ✓ | ✓ | |
| `EventBus.__contains__` | ✓ | ✓ | |
| `Money.__bool__` | ✓ | ✓ | |

**Backend `minilm`:** kód cieľovej triedy v 10/10 úloh, test metódy v 4/10
úloh.

| Úloha | Trieda | Test | Poznámka |
|---|---|---|---|
| `OrderStatus.is_terminal` | ✓ | ✓ | definícia enumu (0,810), 2 testy, `Order.advance` |
| `InventoryLedger.__contains__` | ✓ | ✗ | 5 metód triedy vrátane `__len__` a `_require_sku` |
| `Warehouse.stock_report` | ✓ | ✗ | `receive`, hlavička triedy, hlavička modulu |
| `OrderStateMachine.transition` | ✓ | ✗ | `can_transition`, `allowed_from`, hlavička triedy |
| `OrderLog.by_status` | ✓ | ✗ | hlavička triedy, `__init__`, `__iter__` |
| `Customer.can_afford` | ✓ | ✓ | `charge`, `credit_limit`, `balance` a 1 test |
| `Order.__len__` | ✓ | ✗ | `__len__` iných tried ako vzor, `items` |
| `BulkDiscountPricing.price` | ✓ | ✗ | všetky atribúty triedy a `__init__` |
| `EventBus.__contains__` | ✓ | ✓ | `__init__`, `subscribe` a 2 chunky testov |
| `Money.__bool__` | ✓ | ✓ | porovnávacie metódy `Money` a 1 test |

## Porovnanie backendov

Backendy sa navzájom dopĺňajú. `lsa` porovnáva doslovne rovnaké slová, a
preto uprednostňuje testy, ktorých názvy opakujú názov metódy
(`test_shipped_is_terminal`, `test_can_afford_*`). Pri
`OrderStatus.is_terminal` vrátil päť testov a žiadnu definíciu enumu.
`minilm` berie do úvahy význam, a preto vracia hlavne kód z tej istej triedy:
konštruktor, atribúty a príbuzné metódy, z ktorých je vidieť, s akými
premennými (`self._items`, `self._on_hand`) má nová metóda pracovať. Testy
sa dostanú do top 5 iba v 4 úlohách.

Pre generovanie kódu je dôležitejšie vidieť štruktúru triedy, preto úloha 5
používa `minilm`. Výsledky ukazujú, že najlepší kontext by poskytla
kombinácia oboch prístupov (hybridné vyhľadávanie): niekoľko chunkov s
kódom triedy podľa významu a jeden či dva testy podľa zhody názvu. Tento
nápad je rozpracovaný v bonusovej úlohe.

## Spustenie

```powershell
python retrieve.py "Return the number of line items." --n 5
python retrieve.py --eval                                    # backend minilm
python retrieve.py --eval --store ..\Task_3\vector_store\lsa  # backend lsa
```
