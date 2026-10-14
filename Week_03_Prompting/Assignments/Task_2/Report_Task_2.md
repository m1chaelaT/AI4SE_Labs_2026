Task 2

Prompty ICIO, RTF a CoT z Task 1 som spustila každý v novej session v GitHub Copilot s rovnakým modelom. Predikcie sú uložené v priečinku `predictions` a vyhodnotila som ich skriptom `evaluate_retrieval_predictions.py`.
Výsledky:
- ICIO: 43/155 správne, accuracy 27,74 %, čas inferencie: 2m50s
- RTF: 43/155 správne, accuracy 27,74 %, čas inferencie: 3m15s
- CoT: 154/155 správne, accuracy 99,35 %, čas inferencie: 4m10s


Porovnanie
Najlepšie dopadol CoT, ktorý mal zle iba jeden dotaz. ICIO a RTF mali rovnaký výsledok, okolo 28 %.

Pri ICIO a RTF model väčšinou správne určil podmienky, napríklad mesto a typ jedla, ale vracal iné stĺpce, ako sa očakávalo. ICIO často vracal všetky stĺpce (`*`), RTF iba názov reštaurácie a pri otázkach na najlepšie miesto obidva používali `LIMIT 1`. Skript porovnáva výsledky dotazov, takže tieto odpovede boli vyhodnotené ako nesprávne. Pri pohľahe na štruktúru promptu boli tieto dva dosť poboné, a preto rovnaký výsledok nieje až taký neočakávaný.

V CoT prompte som mala presnejšie napísané, ktoré stĺpce má dotaz vracať, že hodnoty sú malými písmenami a kde sú uložené regióny. Model navyše postupoval krok po kroku, a preto bol oveľa úspešnejší. Odpovede pri CoT sú dlhšie, takže inferencia trvala dlhšie.

