# Report: Embeddingy chunkov a ich uloženie

## Priebeh

Skript `embed_chunks.py` načíta 798 chunkov z úlohy 2
(`Solutions/Task_2/chunks.jsonl`), pre každý z nich zostaví text určený na
embedding, prevedie ho na číselný vektor a uloží dvojice chunk–embedding do
priečinka `vector_store/<backend>`. Celý výpočet beží lokálne, bez API kľúča
a bez volania externej služby.

## Čo sa embedduje

Neembedduje sa iba samotný kód, ale text, ktorý okrem kódu obsahuje aj
krátky opis chunku:

```text
method Customer.can_afford in playground/playground/models.py
playground playground models py customer can afford
def can_afford(self, total: Money) -> bool:
<docstring, ak existuje>
<zdrojový kód chunku>
```

Dôvod je, že vstupy v úlohe 5 sú kombináciou názvov (trieda, metóda, súbor)
a krátkeho opisu v angličtine z `missing_code.json`. Identifikátory sa preto
rozkladajú na slová (`can_afford` → `can afford`, `InventoryLedger` →
`inventory ledger`), aby sa zhodovali s bežným textom v opise úlohy.
Docstring je napísaný podobne ako opis úlohy a z kódu je vidieť, aké
atribúty a typy metóda používa.

## Embeddingové modely

Skript podporuje dva lokálne backendy, ktoré sa vyberajú parametrom
`--backend`:

1. **`minilm`** (predvolený) – predtrénovaný model
   `sentence-transformers/all-MiniLM-L6-v2`, ktorý vytvára vektory dĺžky 384.
   Je malý (90,9 MB), na CPU notebooku spracoval všetkých 798 chunkov za
   približne 14 sekúnd a po prvom stiahnutí funguje offline. Rozpozná aj slová
   s podobným významom, aj keď sa nezhodujú doslovne. Vyžaduje knižnicu `sentence-transformers`.
2. **`lsa`** (záložný) – jednoduchší model (metóda LSA), ktorý spočíta,
   ako často sa jednotlivé slová v chunku vyskytujú (TF-IDF), a výsledok
   zmenší pomocou SVD na 256 čísel. Vytvorí sa priamo z chunkov repozitára
   a používa iba `numpy`.
   V kóde je veľa presných zhôd názvov (`stock_report`, `credit_limit`),
   preto aj takýto jednoduchý model dáva v tomto repozitári dobré výsledky.

Oba modely vracajú vektory s dĺžkou niekoľko sto čísel, ako vyžaduje zadanie.
Všetky vektory sú L2-normalizované, takže kosínusová podobnosť sa v úlohe 4
dá vypočítať ako obyčajný skalárny súčin.

## Uloženie

Pre každý backend vznikne priečinok `vector_store/<backend>` s týmito
súbormi:

| Súbor | Obsah |
|---|---|
| `embeddings.npy` | matica `float32` s rozmermi počet chunkov × dimenzia |
| `chunks.jsonl` | chunky v rovnakom poradí ako riadky matice |
| `meta.json` | backend, názov modelu, dimenzia, počet chunkov, dátum |
| `lsa_model.npz` | iba pri `lsa`: slovník, hodnoty IDF a matica SVD |

Riadok *i* matice patrí chunku na riadku *i* v `chunks.jsonl`, takže
dvojice chunk–embedding sú dané poradím. Ku každému chunku sa tak dá vrátiť
celý záznam vrátane metadát z úlohy 2 (napr. `is_stub`). Pri 798 vektoroch
zaberá matica menej ako 1 MB a celá sa zmestí do pamäte. Vektorová databáza
(FAISS, Chroma) by tu nepriniesla výhodu, iba ďalšiu závislosť. Oplatila by
sa až pri desiatkach tisíc chunkov.

Trieda `VectorStore` v skripte poskytuje metódy `load()` a `embed_query()`.
Vstupná úloha sa tak v úlohách 4 a 5 prevedie na embedding rovnakým
modelom, akým vznikli embeddingy chunkov. Bez toho by sa vektory nedali
porovnávať.

## Overenie

Ako kontrola bolo spustené vyhľadávanie podľa kosínusovej podobnosti (backend
`lsa`) pre tri úlohy z `missing_code.json`. Medzi piatimi najbližšími
chunkami sa vždy objavila samotná cieľová metóda a jej unit testy:

| Dopyt | Najbližšie chunky |
|---|---|
| `OrderStatus.is_terminal` | 4 testy `test_*_terminal`, stub `OrderStatus.is_terminal` |
| `Customer.can_afford` | `Customer.charge`, hlavička triedy `Customer`, 2 testy `test_can_afford_*`, `Customer.credit_limit` |
| `Warehouse.stock_report` | `Warehouse.receive`, stub `Warehouse.stock_report`, 2 testy `test_stock_report_*`, `OutOfStockError` |

Pre ten istý dopyt `OrderStatus.is_terminal` vrátil backend `minilm` toto
poradie:

| Podobnosť | Chunk |
|---|---|
| 0,606 | `enums.py::OrderStatus.is_terminal` (stub) |
| 0,585 | `orders.py::Order.advance` |
| 0,572 | `enums.py::OrderStatus` (hlavička triedy) |
| 0,563 | `test_enums.py::OrderStatusTests.test_cancelled_is_terminal` |
| 0,563 | `orders.py::OrderStateMachine.allowed_from` |

Oba backendy našli cieľovú metódu, ale líšia sa v tom, čo pridajú navyše.
`lsa` uprednostňuje chunky s rovnakými slovami, takže vráti najmä testy
`test_*_terminal`. `minilm` berie do úvahy aj význam a vráti kód,
ktorý so stavmi objednávky pracuje (`Order.advance`, `allowed_from`), a
hlavičku triedy `OrderStatus` s jej hodnotami. Pre generovanie kódu je
kombinácia definície triedy, súvisiaceho kódu a aspoň jedného testu
užitočnejšia, preto je `minilm` zvolený ako predvolený backend.

Samotné stuby sú prázdne, a teda pre generovanie kódu neužitočné. V úlohe 4
ich preto treba z výsledkov odfiltrovať pomocou príznaku `is_stub`.

## Spustenie

```powershell
pip install -r requirements.txt
python embed_chunks.py                    # backend minilm -> vector_store\minilm
python embed_chunks.py --backend lsa      # bez inštalácie -> vector_store\lsa
```
Cesta k chunkom (`--chunks`) a výstupný priečinok (`--out`) sa dajú zadať ako
argumenty.
