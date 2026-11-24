# Nulmeting

Hoe vaak overtreedt synthetische data uit synthpop-py de business rules, zonder aanpassingen? Dit is het vertrekpunt van de challenge.

## Opzet

- Origineel: `data/Synthetic_Homicide.csv` (1.291 rijen)
- Synthese: synthpop-py 1.0.0 met standaardinstellingen (sequentiële CART, standaard kolomvolgorde), `Synthesiser(random_seed=2834727)`, zoals in het notebook van DUO
- Aantal synthetische rijen: 50.000, zoals in het notebook van DUO ("veel meer synthetische rijen dan originele rijen, zodat de gebreken goed naar voren komen"). Ter vergelijking ook 1.291, evenveel als het origineel.
- Regels gemeten met rulecheck, kwaliteit met de pairwise S_pMSE van synthpop-py
- Omgeving: Python 3.13.18, synthpop-py 1.0.0, pandas 3.1.1, scikit-learn 1.9.1, numpy 2.5.5

Zelf draaien:

```bash
python scripts/nulmeting.py              # 50.000 rijen
python scripts/nulmeting.py --n 1291     # evenveel rijen als het origineel
```

## Resultaat

| Regel | Omschrijving | 50.000 rijen | 1.291 rijen |
|---|---|---:|---:|
| 1 | Geboorteplaats ligt in geboorteland | 294 (0,59%) | 5 (0,39%) |
| 2 | Leeftijdsverschil klopt met beide leeftijden | 35.556 (71,11%) | 913 (70,72%) |
| 3.1 | Vorige misdaad niet na de huidige | 260 (0,52%) | 8 (0,62%) |
| 3.2 | Vrijlating niet voor de huidige misdaad | 349 (0,70%) | 14 (1,08%) |
| 4 | Maximaal 10 jaar; leeg als onopgelost | 0 (0,00%) | 0 (0,00%) |
| 5 | Minderjarigen maximaal 5 jaar, met uitzondering | 105 (0,21%) | 3 (0,23%) |
| 6.1 | Geen bewijs bij onopgeloste zaak | 0 (0,00%) | 0 (0,00%) |
| 6.2 | Kogels en ballistiek alleen bij vuurwapen | 0 (0,00%) | 0 (0,00%) |
| 6.3 | Geen bekentenis bij ontoerekeningsvatbaarheid | 16 (0,03%) | 0 (0,00%) |
| 6.4 | Bekentenis alleen bij volledig ingevuld record | 203 (0,41%) | 5 (0,39%) |
| | **Rijen met minstens 1 overtreding** | **35.935 (71,87%)** | **921 (71,34%)** |
| | S_pMSE gemiddeld (lager is beter) | 22,41 | 1,48 |
| | S_pMSE mediaan | 23,38 | 1,55 |
| | S_pMSE maximum | 58,56 | 3,12 |

De originele dataset overtreedt geen enkele regel.

## Wat valt op?

- **Zeven van de tien regels gaan mis.** Alleen regels 4, 6.1 en 6.2 gaan in deze meting niet mis. Waarschijnlijk omdat de toegestane waarden daar sterk samenhangen met één kolom die eerder aan de beurt is ('Solved vs unsolved homicide' of 'Type of weapon used'), en CART zo'n samenhang goed overneemt. Een garantie is dat niet: met een andere seed of meer rijen kan het alsnog misgaan.
- **Regel 2 is verreweg de grootste.** Het leeftijdsverschil wordt los voorspeld, in plaats van berekend uit de twee leeftijden. Daardoor klopt het bij ruim 70% van de rijen niet.
- **De andere regels gaan zelden mis, maar wel structureel.** Bij 50.000 rijen gaat het om tientallen tot honderden onmogelijke records per regel. Eén onmogelijk record kan al genoeg zijn om het vertrouwen in een dataset te verliezen.
- **S_pMSE hangt sterk af van het aantal rijen.** Vergelijk kwaliteit dus alleen tussen datasets met hetzelfde aantal rijen.

## Let op bij vergelijken

- De synthese is reproduceerbaar: dezelfde seed geeft in dezelfde omgeving precies dezelfde rijen. Met andere versies van synthpop-py, scikit-learn, pandas of numpy kunnen de aantallen iets verschillen. Draai de nulmeting daarom zelf in je eigen omgeving en vergelijk je oplossing daarmee.
- Gebruik voor je eindresultaat dezelfde instellingen als de nulmeting: 50.000 rijen en seed 2834727. `scripts/evaluate.py` zet de nulmeting en je eigen resultaat naast elkaar.
