# Opdrachtbeschrijving van DUO

> Overgenomen uit de opdrachtbeschrijving van het Team Synthetische Data van DUO. Het origineel staat in [`duo/Beschrijving Opdracht.docx`](duo/Beschrijving%20Opdracht.docx). Alleen de opmaak is aangepast. De precieze definitie van elke regel, zoals het notebook die controleert, staat in [business-rules.md](business-rules.md).

## Opdracht: Synthetic data rules!

Implementatie van user-defined business rules tijdens het synthese process in python. Business rules zijn begrenzingen op de data, welke eventueel door een gebruiker gedefinieerd kunnen worden tijdens analyses/processen. Vaak zijn Business rules logische gevolgen van de realiteit achter de data. Denk hierbij aan: examencijfers zijn altijd afgerond op 1 decimaal, er zijn geen leerlingen in VMBO leerjaar 5, etc.

Voor meer informatie, tips, en implementatierichtlijnen zie: <https://github.com/duonl/synthpop-py/issues/332>

## De dataset

Ook al beheert DUO enorm interessante data hebben wij voor deze hackathon gekozen voor een dataset die iets meer tot de verbeelding spreekt. Namelijk: een synthetische dataset over alle moorden die in Nederland zijn gepleegd. Omdat we logischerwijs niet een 'echte dataset' met deze inhoud mogen delen (en ook niet hebben) behandelen we deze synthetische set als de 'echte dataset'. In deze hackathon zullen jullie een synthetische dataset maken, die voldoet aan de business rules, van de 'echte dataset' (Dus, in essentie synthetiseren we een al gesynthetiseerde dataset).

Achtergrond informatie over de dataset kan worden gevonden op: <https://dutchhomicide.streamlit.app/>

En: Krüsselmann, K., Achterberg, J., Haas, M., Spruit, M. & Liem, M. (2024). Synthetic Dutch Homicide Monitor [Data set]. Leiden University/Leiden University Medical Center. (<https://doi.org/10.5281/zenodo.13378063>)

Voor deze hackathon hebben wij een aantal extra kolommen, volgens door ons gedefinieerde business rules, toegevoegd. De meeste van deze business rules worden momenteel overschreden tijdens het synthetiseren met synthpop-py. Zie ook de Jupyter Notebook.

## Business rules

Belangrijk om hier te melden is dat wij deze business rules zelf hebben verzonnen om zo een accurate dataset voor deze hackathon te maken. **De business rules dragen dus geen realiteit.**

1. Geboorteplaats (kolom: *Birthcity of main perpetrator*) moet in het geboorteland liggen (kolom: *Birthcountry of main perpetrator*).
2. Het leeftijdsverschil (kolom: *Age difference*) moet logisch volgen uit de kolommen van het slachtoffer (kolom: *Age of victim*) en dader (kolom: *Age of main perpetrator*).
3. Er zijn drie kolommen die momenten in tijd aangeven: *Date of current crime*, *Date of previous crime main perpetrator*, *Date of release from current crime main perpetrator*. Het is onmogelijk dat 1) de datum van de vorige misdaad is gebeurd ná de huidige misdaad. En 2) de datum van uit de gevangenis komen voor de huidige misdaad plaatsvindt voor de datum van deze misdaad.
4. De maximale gevangenisstraf (kolom: *Years prison sentence main perpetrator*) is 10 jaar, zolang de misdaad opgelost is (kolom: *Solved vs unsolved homicide* heeft waarde *Solved*). Als deze niet opgelost is, is de waarde missend.
5. Kinderen onder de achttien (kolom: *Age of main perpetrator*), kunnen maximaal een gevangenisstraf krijgen van 5 jaar, tenzij zij ouder zijn dan 12 én de relatie tot het slachtoffer hun stiefouder of ander familielid is (kolom: *Victim-perpetrator relationship*).
6. Er zijn veel mogelijkheden met betrekking tot de mogelijke waarden in kolom *Main evidence type*. Deze staan hieronder opgesteld:
   - 6.1 Leeg als de zaak ongeplost is (kolom: *Solved vs unsolved homicide* heeft waarde *Unsolved*)
   - 6.2 De waarde *Bullets* en *Ballistics* zijn alleen mogelijk wanneer het moordwapen een vuurwapen is (kolom: *Type of weapon used*)
   - 6.3 De waarde *confession* is niet toegestaan als de moord is gepleegd door iemand die ontoerekeningsvatbaar is (kolom: *context of homicide* is gelijk aan "*Killing by mentally disturbed person (non-family)*").
   - 6.4 De waarde *confession* is alleen toegestaan als alle kolommen behalve *Date of previous crime main perpetrator*, *Date of release from current crime main perpetrator*, *Years prison sentence main perpetrator* **niet**-leeg zijn. Immers wordt bij een bekentenis alle informatie vrijgegeven.
   - 6.5 De waarden *DNA*, *fingerprints* en *witnesses* zijn altijd toegestaan

## Variabelen lijst

| Variabele | Beschrijving | Datatype |
|---|---|---|
| Urban vs rural | Gebied waarin de moord is gepleegd | Categoriaal |
| Time of day | Moment op de dag dat de moord is gepleegd | Categoriaal |
| Single vs multiple homicide victims | Indicator voor of er enkele of meerdere slachtoffers zijn | Categoriaal |
| Single vs multiple homicide perpetrators | Indicator voor of er een enkele of meerdere verdachten zijn | Categoriaal |
| Type of crimescene | Omgeving waarin de moord is gepleegd | Categoriaal |
| Type of weapon used | Het wapen waarmee de moord is gepleegd | Categoriaal |
| Context of homicide | Achtergrondinformatie/context over de moord | Categoriaal |
| Victim-perpetrator relationship | Relatie tussen het slachtoffer en de hoofdverdachte | Categoriaal |
| Solved vs unsolved homicide | Indicator voor of de moord is opgelost | Categoriaal |
| Gender of victim | Gender van het slachtoffer | Categoriaal |
| Gender of main perpetrator | Gender van de hoofdverdachte | Categoriaal |
| Age of victim | Leeftijd van het slachtoffer | Numeriek |
| Age of main perpetrator | Leeftijd van de hoofdverdachte | Numeriek |
| Age difference | Het verschil in leeftijd tussen slachtoffer en hoofdverdachte | Numeriek |
| Main evidence type | Hoofd bewijs van de zaak | Categoriaal |
| Birthcountry of victim | Geboorteland van het slachtoffer | Categoriaal |
| Birthcountry of main perpetrator | Geboorteland van de hoofdverdachte | Categoriaal |
| Birthcity of main perpetrator | Geboortestad van de hoofdverdachte | Categoriaal |
| Date of current crime | Datum van de moord | Unix Timestamp |
| Date of previous crime main perpetrator | Datum van de vorige misdaad | Unix Timestamp |
| Date of release from current crime main perpetrator | Datum van vrijlating | Unix Timestamp |
| Years prison sentence main perpetrator | Duur van de gevangenisstraf voor de hoofdverdachte | Numeriek |

## Overige links

- GitHub: <https://github.com/duonl/synthpop-py>
- GitHub Issue Business Rules: <https://github.com/duonl/synthpop-py/issues/332>
- Read the Docs: <https://synthpop-py.readthedocs.io/en/develop/index.html>
