# De business rules

DUO heeft deze regels zelf bedacht voor de hackathon. **Ze beschrijven niet de werkelijkheid.** De originele dataset voldoet aan alle regels; synthetische data uit synthpop-py 1.0.0 niet (zie [nulmeting.md](nulmeting.md)).

De code in [`src/rulecheck/rules.py`](../src/rulecheck/rules.py) is de precieze definitie. Die volgt het [notebook van DUO](../notebooks/BusinessRules.ipynb), ook in hoe lege waarden meetellen. Een test controleert dat rulecheck en het notebook voor elke rij hetzelfde antwoord geven.

## Overzicht

| Regel | Omschrijving | Kolommen | Lege waarden |
|---|---|---|---|
| 1 | De geboorteplaats van de hoofdverdachte ligt in het geboorteland, volgens de lijst van DUO | Birthcity of main perpetrator, Birthcountry of main perpetrator | Onbekende plaats: altijd goed. Bekende plaats met onbekend land: overtreding. |
| 2 | Leeftijdsverschil = \|leeftijd hoofdverdachte - leeftijd slachtoffer\| | Age difference, Age of main perpetrator, Age of victim | Leeg leeftijdsverschil: goed. Ingevuld verschil terwijl een leeftijd ontbreekt: overtreding. |
| 3.1 | De vorige misdaad van de hoofdverdachte vond niet plaats na de huidige misdaad | Date of previous crime main perpetrator, Date of current crime | Lege datum: goed |
| 3.2 | De vrijlating voor de huidige misdaad ligt niet vóór de datum van die misdaad | Date of current crime, Date of release from current crime main perpetrator | Lege datum: goed. Dezelfde datum: goed. |
| 4 | Opgelost: gevangenisstraf maximaal 10 jaar. Onopgelost: straf is leeg. | Years prison sentence main perpetrator, Solved vs unsolved homicide | Lege straf bij een opgeloste zaak: goed |
| 5 | Een hoofdverdachte jonger dan 18 krijgt maximaal 5 jaar, tenzij die ouder is dan 12 en de relatie '(Step)Parent' of 'Other relative' is | Age of main perpetrator, Years prison sentence main perpetrator, Victim-perpetrator relationship | Lege leeftijd of straf: goed |
| 6.1 | Onopgeloste zaak: hoofdbewijs is leeg | Main evidence type, Solved vs unsolved homicide | |
| 6.2 | 'bullets' en 'ballistics' alleen als het wapen 'Firearm' is | Main evidence type, Type of weapon used | Leeg wapen telt niet als vuurwapen: overtreding |
| 6.3 | Geen 'confession' als de context 'Killing by mentally disturbed person (non-family)' is | Main evidence type, Context of homicide | |
| 6.4 | 'confession' alleen als alle andere kolommen zijn ingevuld, behalve de datum van de vorige misdaad, de datum van vrijlating en de strafmaat | Main evidence type en 18 andere kolommen | Eén lege verplichte kolom bij 'confession': overtreding |
| 6.5 | 'DNA', 'fingerprints' en 'witnesses' zijn altijd toegestaan | Main evidence type | Geen beperking, telt niet mee |

Regels 6.2 tot en met 6.4 gelden voor opgeloste zaken. Voor onopgeloste zaken geldt 6.1: daar hoort helemaal geen hoofdbewijs.

## Kolomvolgorde

synthpop-py synthetiseert kolom voor kolom, standaard in de volgorde van de CSV. Elke kolom wordt voorspeld uit de kolommen die al aan de beurt waren. Een regel kan tijdens het synthetiseren dus pas ingrijpen bij de laatste kolom van de regel: dan zijn de andere kolommen al bekend. Dat bepaalt waar je regels kunt afdwingen, en of je de volgorde (`column_order`) moet aanpassen.

| Nr. | Kolom | Regels |
|---:|---|---|
| 1 | Urban vs rural | 6.4 |
| 2 | Time of day | 6.4 |
| 3 | Single vs multiple homicide victims | 6.4 |
| 4 | Single vs multiple homicide perpetrators | 6.4 |
| 5 | Type of crimescene | 6.4 |
| 6 | Type of weapon used | 6.2, 6.4 |
| 7 | Context of homicide | 6.3, 6.4 |
| 8 | Victim-perpetrator relationship | 5, 6.4 |
| 9 | Solved vs unsolved homicide | 4, 6.1 tot 6.4 |
| 10 | Gender of victim | 6.4 |
| 11 | Gender of main perpetrator | 6.4 |
| 12 | Age of victim | 2, 6.4 |
| 13 | Age of main perpetrator | 2, 5, 6.4 |
| 14 | Age difference | **2**, 6.4 |
| 15 | Main evidence type | **6.1, 6.2, 6.3**, 6.4 |
| 16 | Birthcountry of victim | 6.4 |
| 17 | Birthcity of main perpetrator | 1, 6.4 |
| 18 | Birthcountry of main perpetrator | **1**, 6.4 |
| 19 | Date of current crime | 3.1, 3.2, **6.4** |
| 20 | Date of previous crime main perpetrator | **3.1** |
| 21 | Date of release from current crime main perpetrator | **3.2** |
| 22 | Years prison sentence main perpetrator | **4, 5** |

Vetgedrukt: bij deze kolom zijn in de standaardvolgorde alle andere kolommen van de regel al bekend.

Twee dingen om op te letten:

- **Regel 6.4 hangt af van kolommen vóór én na 'Main evidence type'.** Pas bij kolom 19 is alles bekend, maar dan zijn 'Main evidence type' (15) en de kolommen 16 tot en met 18 al gekozen. Je kunt de regel opknippen: bij kolom 15 geen 'confession' als een van de kolommen 1 tot en met 14 leeg is, en bij de kolommen 16 tot en met 19 geen lege waarde als het hoofdbewijs 'confession' is. Of je verandert de volgorde.
- **Bij regel 1 komt de plaats vóór het land.** Het land wordt dus gekozen bij een al bekende plaats, niet andersom. Je kunt de regel bij het land afdwingen of de volgorde omdraaien.

Een andere volgorde verandert ook de kwaliteit van de synthetische data. Meet dat dus mee.

## Kanttekeningen bij de regels

Dingen die we tegenkwamen bij het omzetten van het notebook naar rulecheck. rulecheck volgt steeds het notebook.

1. **Regel 2 gebruikt het absolute verschil.** De uitleg in het notebook noemt 'leeftijd_dader - leeftijd_slachtoffer', maar de code rekent met de absolute waarde. Het verschil is dus nooit negatief.
2. **Regel 5 gebruikt de letterlijke waarden '(Step)Parent' en 'Other relative'.** De opdrachtbeschrijving spreekt van 'stiefouder of ander familielid'. Welke kant de relatie op werkt, staat niet in de data; de regel kijkt alleen naar de waarde in de kolom.
3. **Regel 6.2 gebruikt kleine letters.** De opdrachtbeschrijving schrijft 'Bullets' en 'Ballistics'; in de data staan 'bullets' en 'ballistics'.
4. **Regel 6.5 is geen beperking.** Het notebook controleert alleen dat de drie waarden voorkomen. rulecheck telt de regel niet mee.
5. **Het notebook stopt bij de eerste regel die faalt.** Elke controle eindigt met een `assert`. Op synthetische data uit synthpop-py 1.0.0 stopt het notebook al bij regel 1. Gebruik `python -m rulecheck` voor een overzicht van alle regels tegelijk.

Vragen over de regels? Stel ze aan de challenge owners: Cas van Erp en Erina Koomen (synthetische.data@duo.nl).
