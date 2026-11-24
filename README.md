# OneGov #3 | synthpop.py

> *Synthetic data rules! Business rules afdwingen tijdens het synthetiseren met synthpop-py, met behoud van de kwaliteit van de data.*

Startrepository voor challenge 3 van **OneGov #3**, onderdeel van de OneGov Hackathon Series van GovTechNL. De challenge komt van het Team Synthetische Data van DUO.

- **Thema:** Digitale autonomie en soevereiniteit
- **Datum:** 9 en 10 december 2026
- **Locatie:** The Hague Tech, Den Haag
- **Challenge owners:** Cas van Erp en Erina Koomen, Team Synthetische Data, DUO
- **Techpartner:** GreenPT
- **Community, teams en inleveren:** [alkem.io/onegov-hackathon](https://alkem.io/onegov-hackathon)
- **Contact:** [hack@govtechnl.nl](mailto:hack@govtechnl.nl)

## De challenge

Een synthesemodel leert patronen uit data, maar geen regels. Daardoor ontstaan records die statistisch kloppen en inhoudelijk onmogelijk zijn. In deze challenge bouw je voor [synthpop-py](https://github.com/duonl/synthpop-py), de open source synthesesoftware van DUO, een manier om business rules tijdens het synthetiseren af te dwingen, met behoud van de kwaliteit van de data.

> **Hoe implementeren we in synthpop-py door de gebruiker gedefinieerde business rules, zodat synthetische data tijdens het synthetiseren aan die regels voldoet, met behoud van de statistische kwaliteit?**

De challenge brief staat op Alkemio. [CHALLENGE.md](CHALLENGE.md) is een Engelse werkvertaling; bij verschillen is de Nederlandse brief leidend.

## Snel aan de slag

Je hebt Python 3.11 of hoger nodig (getest met 3.11, 3.13 en 3.14).

```bash
git clone https://github.com/govtechnl/onegov3-synthpop-py.git
cd onegov3-synthpop-py
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python scripts/nulmeting.py        # synthpop-py met standaardinstellingen, 50.000 rijen
python -m rulecheck output/nulmeting_n50000_seed2834727.csv
pytest
```

De nulmeting duurt op een laptop ongeveer tien seconden. Meer uitleg, ook over hoe synthpop-py werkt en waar je kunt ingrijpen, staat in [docs/aan-de-slag.md](docs/aan-de-slag.md).

## Wat zit erin

| Map of bestand | Wat het is |
|---|---|
| `data/` | De dataset van DUO: een synthetische versie van de Dutch Homicide Monitor met extra kolommen. Zie de [datakaart](data/README.md). |
| `docs/business-rules.md` | De business rules: precieze definitie, omgang met lege waarden en wat de kolomvolgorde betekent |
| `docs/nulmeting.md` | Hoe vaak synthpop-py 1.0.0 de regels nu overtreedt |
| `docs/aan-de-slag.md` | Werkwijze, synthpop-py in het kort en afspraken voor vergelijkbare resultaten |
| `docs/opdracht-duo.md` | De opdrachtbeschrijving van DUO (het origineel staat in `docs/duo/`) |
| `notebooks/BusinessRules.ipynb` | Het notebook van DUO met een controle per regel |
| `src/rulecheck/` | De business rules als Python-code, plus een evaluatie van regels en kwaliteit |
| `scripts/nulmeting.py` | Synthetiseert de dataset met standaardinstellingen en meet regels en kwaliteit |
| `scripts/evaluate.py` | Vergelijkt jouw synthetische data met de nulmeting |
| `tests/` | Tests, waaronder een controle dat rulecheck precies hetzelfde meet als het notebook van DUO |
| `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | Hoe je bijdraagt, en de afspraken over data en het onderwerp |

## De business rules

DUO voegde voor de hackathon kolommen toe volgens zelf bedachte business rules. **De regels beschrijven dus niet de werkelijkheid.**

| Regel | Kort | Nulmeting* |
|---|---|---:|
| 1 | De geboorteplaats van de hoofdverdachte ligt in het geboorteland | 294 (0,6%) |
| 2 | Het leeftijdsverschil volgt uit de leeftijden van slachtoffer en hoofdverdachte | 35.556 (71,1%) |
| 3.1 | De vorige misdaad vond niet plaats na de huidige misdaad | 260 (0,5%) |
| 3.2 | De vrijlating ligt niet vóór de datum van de huidige misdaad | 349 (0,7%) |
| 4 | Opgelost: maximaal 10 jaar gevangenisstraf. Onopgelost: geen straf | 0 |
| 5 | Jonger dan 18: maximaal 5 jaar, met een uitzondering | 105 (0,2%) |
| 6.1 | Onopgelost: geen hoofdbewijs | 0 |
| 6.2 | 'bullets' en 'ballistics' alleen bij een vuurwapen | 0 |
| 6.3 | Geen 'confession' bij een ontoerekeningsvatbare dader | 16 (0,03%) |
| 6.4 | 'confession' alleen bij een volledig ingevuld record | 203 (0,4%) |
| 6.5 | 'DNA', 'fingerprints' en 'witnesses' zijn altijd toegestaan | n.v.t. |

\* Aantal rijen met een overtreding, in 50.000 synthetische rijen uit synthpop-py 1.0.0 met standaardinstellingen (seed 2834727). Bij 71,9% van de rijen gaat minstens één regel mis. De originele dataset overtreedt geen enkele regel. Zie [docs/nulmeting.md](docs/nulmeting.md) en, voor de precieze definities, [docs/business-rules.md](docs/business-rules.md).

In je eigen code:

```python
import pandas as pd
from rulecheck import check_rules, violations

df = pd.read_csv("output/mijn_aanpak.csv")
print(check_rules(df))      # overtredingen per regel
masks = violations(df)      # per regel een boolean Series: True is een overtreding
```

## Hoe meet je je resultaat?

De jury wil per regel het aantal overtredingen zien zonder en met je oplossing, en het effect op de statistische kwaliteit. Zo maak je dat vergelijkbaar met andere teams:

1. Genereer met je oplossing 50.000 rijen met seed 2834727, net als de nulmeting.
2. Sla ze op als CSV met dezelfde 22 kolommen.
3. Vergelijk ze met de nulmeting:

```bash
python scripts/evaluate.py output/nulmeting_n50000_seed2834727.csv output/mijn_aanpak.csv \
  --labels nulmeting "mijn aanpak" --md output/vergelijking.md
```

Het script meet kwaliteit met de S_pMSE van synthpop-py (lager is beter): per kolompaar en samengevat. Het laat ook zien bij welke kolomparen de kwaliteit het meest achteruitging. S_pMSE hangt sterk af van het aantal rijen, dus vergelijk alleen datasets van gelijke omvang. Andere kwaliteitsmaten zijn ook welkom.

## Bijdragen aan synthpop-py

Bouw je in synthpop-py zelf? Werk dan in een fork van [duonl/synthpop-py](https://github.com/duonl/synthpop-py): eigen branches op de repository van DUO zijn niet mogelijk. Een bijdrage aan het pakket is welkom, maar niet verplicht. Voordat iets in synthpop-py wordt opgenomen, zijn heldere requirements en een review door het DUO-team nodig. Lees vooraf [issue #332](https://github.com/duonl/synthpop-py/issues/332) met tips en implementatierichtlijnen van het DUO-team, en de [CONTRIBUTING.md](https://github.com/duonl/synthpop-py/blob/main/CONTRIBUTING.md) van synthpop-py.

## Inleveren

Lever je oplossing in via [Alkemio](https://alkem.io/onegov-hackathon), met een link naar je code en je vergelijking met de nulmeting. Je code is open source en staat op GitHub: als fork van synthpop-py of in een eigen repository. Deze repository is alleen het startmateriaal, dus zet je oplossing hier niet in. Zie ook [CONTRIBUTING.md](CONTRIBUTING.md).

## Zorgvuldig met het onderwerp

De dataset gaat over moorden. Ook al is hij synthetisch, ga er zorgvuldig mee om, ook in voorbeelden, pitches en demo's. Zie de [gedragscode](CODE_OF_CONDUCT.md).

## Licenties en bronnen

- Code in deze repository: [EUPL-1.2](LICENSE), dezelfde licentie als synthpop-py.
- Data, documentatie en challengetekst: CC BY 4.0, zie [LICENSE-DATA](LICENSE-DATA).
- Dataset: gebaseerd op Krüsselmann, K., Achterberg, J., Haas, M., Spruit, M. & Liem, M. (2024). *Synthetic Dutch Homicide Monitor* [Data set]. Universiteit Leiden/LUMC. [doi.org/10.5281/zenodo.13378063](https://doi.org/10.5281/zenodo.13378063), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). DUO voegde kolommen toe; zie de [datakaart](data/README.md).
- Notebook en opdrachtbeschrijving: Team Synthetische Data, DUO.

## Contact

- Vragen over synthpop-py en de business rules: de challenge owners, Cas van Erp en Erina Koomen, via [synthetische.data@duo.nl](mailto:synthetische.data@duo.nl)
- Vragen over de hackathon: [hack@govtechnl.nl](mailto:hack@govtechnl.nl)

---

## In English

Starter repository for challenge 3 (synthpop.py) of OneGov #3, part of the OneGov Hackathon Series by GovTechNL (9-10 December 2026, The Hague Tech, The Hague). The challenge: implement user-defined business rules in [synthpop-py](https://github.com/duonl/synthpop-py), the open source synthesis package of DUO, so that synthetic data follows those rules during synthesis while keeping its statistical quality.

The dataset is a synthetic version of the Dutch Homicide Monitor, with extra columns that DUO added following business rules they made up for this hackathon. With synthpop-py 1.0.0 and default settings, 71.9% of 50,000 synthetic rows break at least one rule. Start with `pip install -e ".[dev]"`, `python scripts/nulmeting.py` (baseline) and `python -m rulecheck <file.csv>` (rule check), and compare your output with `scripts/evaluate.py`. [CHALLENGE.md](CHALLENGE.md) is an English working translation of the challenge brief; the Dutch brief prevails.
