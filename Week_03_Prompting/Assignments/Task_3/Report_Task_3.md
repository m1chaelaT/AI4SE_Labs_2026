Task 3

Navrhnutá nová metrika:

Metrika by porovnávala, či dotaz našiel správne reštaurácie, aj keď vrátil náhosou iné stĺpce. Zároveň penalizuje chýbajúce alebo nadbytočné riadky. Pôvodná accuracy berie dotaz ako správny iba vtedy, keď sa výsledok presne zhoduje s očakávaným, takže dotaz s dobrými podmienkami, ale inými stĺpcami, dostane 0 rovnako ako úplne zlý dotaz. Nová metrika accuracy nenahrádza, ale dopĺňa ju. Nová metrika by ukazovala ako moc model pochopil, čo má vyhľadať.

Ako by sa metrika počítala

Výsledok každého dotazu porovnávam s očakávaným výsledkom riadok po riadku. Pri porovnaní nezáleží na tom, v akom poradí sú stĺpce, ani na tom, či dotaz vrátil o nejaký stĺpec viac alebo menej. Dôležité je, či riadok patrí správnej reštaurácii. Ak dotaz vráti iba názov reštaurácie a očakáva sa číslo domu aj názov, riadok sa stále počíta ako správny, lebo ide o tú istú reštauráciu. Za nesprávny sa riadok považuje vtedy, keď sa hodnoty nezhodujú, teda ide o inú reštauráciu, alebo keď dotaz vráti stĺpce úplne mimo, napríklad hodnotenie a typ jedla namiesto čísla domu.

Potom sa pri každej otázke pozriem na to, koľko z vrátených riadkov bolo správnych. Ak dotaz vráti reštaurácie navyše, ktoré tam nepatria, skóre klesne. Druhá je, koľko z očakávaných riadkov dotaz našiel. Ak napríklad existujú tri najlepšie reštaurácie a dotaz kvôli `LIMIT 1` vráti iba jednu, dostane približne tretinu bodov za túto časť. Z týchto dvoch hodnôt sa spraví F1 skóre, takže otázka môže byť aj čiastočne správna a nedostane iba 0 alebo 1 ako pri accuracy. Ak dotaz správne nevráti nič, lebo nič také v databáze nie je, dostane plný počet bodov. Ak vráti nič, hoci niečo vrátiť mal, alebo naopak, dostane 0.
--------------------------------------------------------
Na základe môjho návrhu som napísala promt na základe ktorého som cez  Claud - Opus 5.5 Medium dostala výsledný python skript. 

PROMT:
Napíš Python skript, ktorý vypočíta novú metriku pre text-to-SQL predikcie.

Metrika by porovnávala, či dotaz našiel správne reštaurácie, aj keď vrátil náhodou iné stĺpce. Zároveň penalizuje chýbajúce alebo nadbytočné riadky. Nová metrika by ukazovala, ako moc model pochopil, čo má vyhľadať.

Výsledok každého dotazu porovnaj s očakávaným výsledkom riadok po riadku. Pri porovnaní nezáleží na tom, v akom poradí sú stĺpce, ani na tom, či dotaz vrátil o nejaký stĺpec viac alebo menej. Dôležité je, či riadok patrí správnej reštaurácii. Ak dotaz vráti iba názov reštaurácie a očakáva sa číslo domu aj názov, riadok sa stále počíta ako správny. Za nesprávny sa riadok považuje vtedy, keď ide o inú reštauráciu, alebo keď dotaz vráti stĺpce úplne mimo, napríklad hodnotenie a typ jedla namiesto čísla domu.

Pri každej otázke zisti, koľko z vrátených riadkov bolo správnych a koľko z očakávaných riadkov dotaz našiel. Z týchto dvoch hodnôt sa spraví F1 skóre, takže otázka môže byť aj čiastočne správna. Ak dotaz správne nevráti nič, dostane plný počet bodov. Ak vráti nič, hoci niečo vrátiť mal, alebo naopak, dostane 0. Výsledok promptu je priemer cez všetky otázky.

Súbory
- `Task_2/data/restaurants-schema.csv` – schéma: tabuľky RESTAURANT(ID, NAME, FOOD_TYPE, CITY_NAME, RATING), LOCATION(RESTAURANT_ID, HOUSE_NUMBER, STREET_NAME, CITY_NAME), GEOGRAPHIC(CITY_NAME, COUNTY, REGION).
- `Task_2/data/restaurants-db.txt` – dáta, jeden záznam na riadok
- `Task_2/data/restaurants_dataset.csv` – stĺpce `question,result`, kde `result` je JSON pole riadkov, napr. `[[3, "portola park"]]`. Niektoré výsledky sú prázdne, iné majú výsledky.
- `Task_2/predictions/ICIO.csv`, `RTF.csv`, `CoT.csv` – stĺpce `question,predicted_sql`, v rovnakom poradí ako dataset.

Výstup
Skript napíš v jazyku Python. Skóre jednotlivých otázok ulož do `relaxed_f1_scores.csv` (`prompt,question,relaxed_f1`).

---------------------------------------------------------------------------------
## Výsledky

- ICIO: 0,284
- RTF: 0,897
- CoT:  F1 0,994

## Zhodnotenie

CoT bol najlepší pri obidvoch metrikách a jeho hodnota sa takmer nezmenila, pretože jeho dotazy vracali správne riadky aj správne stĺpce.
RTF sa pri novej metrike zlepšil najviac, z 28 % na takmer 90 %. Vracal iba názov reštaurácie, ale väčšinou tie správne, takže otázky pochopil dobre a chyba bola hlavne vo formáte výstupu.
ICIO zostal nízko aj pri novej metrike. 

Nová metrika teda ukázala rozdiel medzi ICIO a RTF, ktorý pôvodná accuracy úplne skryla.
