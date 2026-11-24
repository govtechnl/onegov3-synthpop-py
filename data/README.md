# Datakaart: Synthetic_Homicide.csv

| | |
|---|---|
| Bestand | `Synthetic_Homicide.csv` (komma-gescheiden, UTF-8, kopregel met kolomnamen) |
| Omvang | 1.291 rijen (zaken), 22 kolommen |
| Aangeleverd door | Team Synthetische Data, DUO, voor OneGov Editie #3 |
| Gebaseerd op | Krüsselmann, K., Achterberg, J., Haas, M., Spruit, M. & Liem, M. (2024). *Synthetic Dutch Homicide Monitor* [Data set]. Universiteit Leiden/LUMC. [doi.org/10.5281/zenodo.13378063](https://doi.org/10.5281/zenodo.13378063) |
| Licentie | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), met bronvermelding zoals hierboven |
| Achtergrond | [dutchhomicide.streamlit.app](https://dutchhomicide.streamlit.app/) |

## Wat is dit voor data?

Een synthetische versie van de Dutch Homicide Monitor, over moorden in Nederland. Er staan geen echte personen of zaken in. Een echte dataset met deze inhoud mag niet gedeeld worden; in de hackathon geldt deze synthetische set daarom als de 'echte' dataset. Teams maken er een nieuwe synthetische versie van die aan de business rules voldoet.

## Wat heeft DUO veranderd?

DUO voegde voor de hackathon een aantal kolommen toe, volgens zelf bedachte business rules. **Die regels beschrijven niet de werkelijkheid.** De originele dataset in deze repository overtreedt geen enkele regel. Zie [docs/business-rules.md](../docs/business-rules.md).

## Kolommen

Beschrijvingen van DUO. De waarden staan in het Engels, precies zoals in de bron. Een lege cel is een onbekende waarde.

| Kolom | Beschrijving | Type | Leeg |
|---|---|---|---:|
| Urban vs rural | Gebied waarin de moord is gepleegd | categorisch (2) | 2,5% |
| Time of day | Moment op de dag dat de moord is gepleegd | categorisch (4) | 32,7% |
| Single vs multiple homicide victims | Eén of meerdere slachtoffers | categorisch (2) | 0% |
| Single vs multiple homicide perpetrators | Eén of meerdere verdachten | categorisch (2) | 10,9% |
| Type of crimescene | Omgeving waarin de moord is gepleegd | categorisch (5) | 3,3% |
| Type of weapon used | Het wapen waarmee de moord is gepleegd | categorisch (8) | 10,1% |
| Context of homicide | Achtergrond of context van de moord | categorisch (9) | 13,0% |
| Victim-perpetrator relationship | Relatie tussen het slachtoffer en de hoofdverdachte | categorisch (9) | 31,3% |
| Solved vs unsolved homicide | Of de moord is opgelost | categorisch (2) | 0% |
| Gender of victim | Gender van het slachtoffer | categorisch (2) | 1,0% |
| Gender of main perpetrator | Gender van de hoofdverdachte | categorisch (2) | 7,9% |
| Age of victim | Leeftijd van het slachtoffer | numeriek (0 tot 100) | 4,4% |
| Age of main perpetrator | Leeftijd van de hoofdverdachte | numeriek (7 tot 99) | 11,9% |
| Age difference | Leeftijdsverschil tussen slachtoffer en hoofdverdachte | numeriek (0 tot 86) | 15,8% |
| Main evidence type | Hoofdbewijs van de zaak | categorisch (6) | 13,0% |
| Birthcountry of victim | Geboorteland van het slachtoffer | categorisch (3) | 43,8% |
| Birthcity of main perpetrator | Geboorteplaats van de hoofdverdachte | categorisch (47) | 55,5% |
| Birthcountry of main perpetrator | Geboorteland van de hoofdverdachte | categorisch (3) | 44,2% |
| Date of current crime | Datum van de moord | Unix-tijd in seconden (nov. 2021 tot nov. 2026) | 0% |
| Date of previous crime main perpetrator | Datum van de vorige misdaad van de hoofdverdachte | Unix-tijd in seconden | 43,1% |
| Date of release from current crime main perpetrator | Datum van vrijlating voor de huidige misdaad | Unix-tijd in seconden | 29,5% |
| Years prison sentence main perpetrator | Duur van de gevangenisstraf in jaren | numeriek (0,1 tot 10) | 29,5% |

Het getal tussen haakjes bij categorische kolommen is het aantal verschillende waarden. Datums met lege waarden staan als kommagetal in de CSV (bijvoorbeeld `1865116800.0`); `pandas.to_datetime(kolom, unit="s")` maakt er een datum van.

## Goed om te weten

- De kolomvolgorde in het bestand is ook de standaardvolgorde waarin synthpop-py synthetiseert. Wat dat betekent voor de regels staat in [docs/business-rules.md](../docs/business-rules.md#kolomvolgorde).
- Sommige labels zijn in de bron afgekapt of hebben een komma aan het eind, zoals `Afternoon (12-6` en `Hitting, kicking or other similar physical violence without weapon,`. Laat ze zo: de regels en tests gaan uit van de waarden zoals ze in het bestand staan.
- Bij de geboorteplaatsen staan bewust plaatsnamen die in meer landen voorkomen, zoals Harlingen en Napels. De regel kijkt naar de lijst van DUO, niet naar de echte ligging.
- De dataset gaat over moorden. Ook al is hij synthetisch, ga er zorgvuldig mee om, ook in voorbeelden, pitches en demo's.
