# Úloha 1 – Agentová sieť na spresňovanie požiadaviek

## 1. Úvod

Úlohou bolo vytvoriť agentovú sieť, ktorá zo súboru textov (e-maily, zápisnice, rozhovory, prieskum, návrh špecifikácie) vytvorí jeden dokument softvérových požiadaviek. Sieť je implementovaná v LangGraph a používa modely OpenAI. Pri tvorbe som používala kódovacieho agenta (Claude). Spúšťa sa príkazom `python pipeline.py <vstupný_priečinok>`, pričom na vstupe stačí cesta k priečinku a spracujú sa všetky textové súbory v ňom.

V tomto priečinku je okrem reportu aj výsledný dokument `requirements.md` a graf siete `pipeline_graph.mmd`.

## 2. Architektúra

Sieť má deväť uzlov, ktoré idú za sebou v tomto poradí:

- **load** (bez AI) – načíta dokumenty, pridelí im ID (D01, D02, …) a dlhé dokumenty rozdelí na časti.
- **extract** (gpt-5-mini) – z každej časti vytiahne kandidátov na požiadavky s citáciou zo zdroja a zvlášť aj výroky, ktoré nie sú požiadavkami.
- **merge** (gpt-5.6-luna) – zjednotí kategórie do oblastí, vytvorí slovník pojmov a zlúči duplicitné požiadavky.
- **check_conflicts** (gpt-6-luna) – nájde protichodné požiadavky a položky, ktoré nie sú požiadavkami na systém, a presunie ich do blacklistu.
- **prioritize** (gpt-5.6-luna) – pridelí každej požiadavke prioritu Must/Should/Could/Won't so zdôvodnením.
- **validate** (bez AI) – pridelí finálne ID (REQ-001, …) a skontroluje, či výstup spĺňa body zo zadania.
- **review** (gpt-6-luna) – prejde výsledok validácie a navrhne konkrétne opravy.
- **revise** (gpt-5.6-luna) – vykoná navrhnuté opravy a výsledok ide znova do validate.
- **render** (bez AI) – vytvorí výsledný dokument v Markdowne.

Spätná väzba je teda medzi validate, review a revise. Opakuje sa, kým validácia nenájde chyby a recenzent nenavrhne ďalšie opravy, najviac však štyrikrát.

## 3. Návrhové rozhodnutia

Extraktor spracúva každý dokument zvlášť a paralelne, preto som zvolila najlacnejší model. V prompte je, aby radšej extrahoval viac, keďže duplicity sa odstránia neskôr. ID dokumentov a zoznamy zdrojov dopĺňa vždy kód, nie model, aby bolo trasovanie spoľahlivé. Kód tiež overuje, či sa citácia od modelu naozaj nachádza v zdrojovom texte.

Kandidátov bolo okolo 650, čo je na jedno volanie veľa, preto merger zlučuje po oblastiach a na konci robí ešte kontrolu duplicít naprieč oblasťami. Kód pritom kontroluje, aby žiadny kandidát nezmizol. Pri konfliktoch model vidí aj typ a dátum dokumentov, takže vie, že neskoršie rozhodnutie zo stretnutia má prednosť pred januárovým návrhom. Na konflikty a recenziu som použila najsilnejší model, lebo musia brať do úvahy celý zoznam naraz.

Validátor je bez AI, aby kontrola bola spoľahlivá a opakovateľná. Recenzent a revízor potom opravujú iba konkrétne problémy, čo je rýchlejšie a lacnejšie ako spúšťať celý merger znova.

## 4. Splnenie zadania

- ANS1: šesť uzlov volá LLM (extract, merge, check_conflicts, prioritize, review, revise).
- ANS2: load, validate a render sú bez AI.
- ANS3: spätná väzba validate → review → revise → validate.
- ANS4: tri modely – gpt-5-mini, gpt-5.6-luna, gpt-6-luna.
- ANS5: sieť je `StateGraph` v LangGraph (`pipeline.py`).
- OS1: jeden dokument `requirements.md`.
- OS2: ID REQ-001 atď. prideľuje a kontroluje validátor.
- OS3: duplicity odstraňuje merger a zvyšné recenzent.
- OS4: pri každej požiadavke sú zdrojové dokumenty a citácie, na konci dokumentu je matica trasovania.
- OS5: každá požiadavka má názov, vetu „The system shall …“ a popis, ktorého dĺžku kontroluje validátor.
- OS6: priorita MoSCoW, stupnica je vysvetlená v dokumente.
- OS7: slovník pojmov a kontrola konfliktov.
- OS8: extrakcia „radšej viac“ a kontrola, že sa nestratil žiadny kandidát ani dokument.
- OS9: blacklist v dokumente obsahuje vyradené položky aj s dôvodom.

## 5. Výsledky

Beh trval asi 22 minút. Z 20 dokumentov sa extrahovalo 667 kandidátov a 131 výrokov bolo ignorovaných (napríklad súkromné poznámky v e-mailoch). Po zlúčení duplicít zostalo 279 požiadaviek. Kontrola konfliktov našla jeden rozpor (dôvod vymazania záznamu povinný vs. voliteľný) a odstránila ďalších 10 položiek, ktoré neboli požiadavkami na systém. V prvom kole recenzie validátor našiel 26 chýb, hlavne príliš krátke popisy, a po oprave už žiadne.

Výsledný dokument má 268 požiadaviek s prioritami Must 50, Should 113, Could 103 a Won't 2. Všetkých 20 dokumentov je trasovaných aspoň k jednej požiadavke.

## 6. Obmedzenia

Výsledky sa medzi behmi mierne líšia, keďže jazykové modely nie sú deterministické. Všetky vyradené položky sú preto v blackliste aj s dôvodom, aby sa rozhodnutia modelov dali skontrolovať.
