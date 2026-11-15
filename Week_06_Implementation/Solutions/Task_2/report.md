# Report: Rozdelenie repozitára AI4SE_Playground na chunky

## Priebeh

Skript `chunk_repo.py` prejde všetky súbory naklonovaného repozitára
`Week_06_Implementation/AI4SE_Playground`, rozdelí ich na chunky a uloží ich
do súboru `chunks.jsonl` v tomto priečinku. Repozitár obsahuje iba zdrojový
kód v Pythone: približne 1 400 riadkov v balíku `playground/playground` a
približne 3 000 riadkov unit testov v `playground/tests`. Výsledkom je 798
chunkov.

## Spôsob delenia

Súbory `.py` sa nedelia podľa počtu znakov, ale podľa ich štruktúry pomocou
modulu `ast` zo štandardnej knižnice. Vznikajú tieto typy chunkov:

1. **module** – hlavička súboru: docstring modulu, importy a príkazy na
   úrovni modulu, teda všetko, čo nie je trieda ani funkcia.
2. **class** – hlavička triedy: riadok `class`, docstring, atribúty triedy
   (napr. tabuľka `TRANSITIONS`) a zoznam podpisov všetkých jej metód. Telá
   metód sa sem neopakujú.
3. **method** / **function** – jedna metóda alebo funkcia vrátane
   dekorátorov a docstringu.
4. **test** – jedna testovacia metóda zo súborov `test_*.py`.

Na začiatok textu každého chunku sa pridá krátky kontext s cestou k súboru,
názvom triedy a typom chunku:
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    def __iter__(self) -> Iterator[LineItem]:
        """Iterate over a tuple snapshot of the order's line items."""
        return iter(tuple(self._items))
```
Bez neho by z chunku nebolo jasné, do ktorej triedy a súboru metóda patrí.
Práve podľa súboru a triedy pritom `missing_code.json` určuje, ktorú metódu
treba doplniť.

Ostatné textové súbory (napr. `.md`, `.toml`) by sa delili na okná po
riadkoch s prekryvom. V tomto repozitári sa však žiadne nevyskytujú.

## Veľkosť chunkov

Za základnú jednotku je zvolená jedna metóda, takže veľkosť chunku nie je
pevne daná a určuje ju kód. Medián je 4 riadky a najdlhší chunk má 55
riadkov. Pre úlohu „doplň chýbajúcu metódu“ je to vhodná veľkosť, pretože:

- žiadny chunk nepreseká metódu v polovici, čo by sa pri delení podľa znakov
  stávalo bežne,
- pri vyhľadávaní sa vracajú celé metódy, ktoré model potrebuje vidieť
  (podobné metódy, používané atribúty a testy cieľovej metódy),
- päť takýchto chunkov sa pohodlne zmestí do promptu aj pre malé modely.

Pre prípad dlhých funkcií má skript horný limit 60 riadkov (`--max-lines`).
Dlhšie jednotky sa rozdelia na časti s prekryvom 10 riadkov (`--overlap`),
aby sa nestratil kontext na hraniciach. V tomto repozitári žiadna jednotka
limit neprekročila, takže k deleniu nedošlo.

## Testy a prázdne metódy

Testy sú zahrnuté zámerne. Sú súčasťou repozitára a najpresnejšie opisujú
očakávané správanie kódu, vrátane chýbajúcich metód. Tvoria však 481 z 798
chunkov, s čím treba počítať pri vyhľadávaní v ďalších úlohách.

Metódy, ktorých telo obsahuje iba `pass`, `...` alebo
`raise NotImplementedError`, majú v metadátach `is_stub: true`. Abstraktné
metódy s dekorátorom `@abstractmethod` sa za stuby nepovažujú, lebo sú
prázdne zámerne. Takto skript označil presne 10 metód zo súboru
`missing_code.json`. Príznak umožní v ďalších úlohách vynechať z výsledkov
vyhľadávania prázdny kód.

## Dátová štruktúra

Chunky sú uložené vo formáte JSON Lines (`chunks.jsonl`), jeden objekt na
riadok. Formát je jednoduchý, čitateľný a dá sa načítať po riadkoch bez
ďalších knižníc. Každý chunk obsahuje:

| Pole | Význam |
|---|---|
| `id` | jedinečný identifikátor, napr. `playground/playground/orders.py::Order.__len__` |
| `file`, `cls`, `name` | súbor, trieda a názov jednotky |
| `kind` | `module`, `class`, `method`, `function`, `test` alebo `text` |
| `start_line`, `end_line` | poloha v pôvodnom súbore |
| `is_stub` | či ide o neimplementovanú metódu |
| `signature`, `docstring` | podpis a docstring (využiteľné pri embeddingoch) |
| `code` | pôvodný zdrojový kód jednotky |
| `text` | kontext + kód, teda text určený na embedding a do promptu |
| `part` | poradie časti, ak bola jednotka rozdelená |

## Výsledok

| Typ chunku | Počet |
|---|---|
| module | 26 |
| class | 99 |
| method | 183 |
| function | 9 |
| test | 481 |
| **spolu** | **798** |

## Spustenie

```powershell
python chunk_repo.py
python chunk_repo.py --repo ..\..\AI4SE_Playground --out chunks.jsonl --max-lines 60 --overlap 10
```
Cesty sa dajú zadať ako argumenty. Predvolene skript hľadá repozitár v
`Week_06_Implementation/AI4SE_Playground` a výstup zapíše vedľa seba.
Používa iba štandardnú knižnicu Pythonu.
