# Aan de slag

## 1. Installeren

Je hebt Python 3.11 of hoger en git nodig. Getest met Python 3.11, 3.13 en 3.14.

```bash
git clone https://github.com/govtechnl/onegov3-synthpop-py.git
cd onegov3-synthpop-py
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"            # rulecheck, synthpop-py, pytest en ruff
pip install -e ".[notebook]"       # optioneel: JupyterLab voor het notebook van DUO
pytest                             # alles groen? Dan werkt je omgeving.
```

## 2. De nulmeting draaien

```bash
python scripts/nulmeting.py
```

Het script synthetiseert de dataset met synthpop-py en standaardinstellingen (50.000 rijen, seed 2834727), telt de overtredingen per regel en meet de kwaliteit. Alles komt in `output/`: de synthetische CSV, een JSON met alle getallen en versies, en een Markdown-tabel. Zie [nulmeting.md](nulmeting.md) voor de uitkomst.

## 3. Synthetische data toetsen

Elke CSV met dezelfde 22 kolommen kun je toetsen:

```bash
python -m rulecheck output/nulmeting_n50000_seed2834727.csv
python -m rulecheck mijn_data.csv --json        # als JSON
python -m rulecheck mijn_data.csv --strict      # exitcode 1 bij een overtreding, handig in tests
```

Of in Python:

```python
from rulecheck import check_rules, violations, any_violation

check_rules(df)        # tabel met overtredingen per regel
violations(df)["2"]    # boolean Series voor regel 2: True is een overtreding
any_violation(df)      # True voor rijen die minstens één regel overtreden
```

## 4. Hoe synthpop-py werkt, in het kort

synthpop-py synthetiseert een tabel **kolom voor kolom**. De eerste kolom wordt gesampled. Elke volgende kolom wordt voorspeld uit de kolommen die al aan de beurt waren, standaard met CART (beslisbomen).

```python
from synthpop import Synthesiser

syn = Synthesiser(random_seed=2834727).fit(df).generate(50_000)
```

- `fit(X)` traint per kolom een synthesemethode op de originele data, met de eerdere kolommen als voorspellers.
- `generate(n)` maakt de kolommen in dezelfde volgorde aan. Elke methode krijgt de synthetische kolommen die al gemaakt zijn.

Hier kun je ingrijpen:

| Knop | Wat het doet |
|---|---|
| `column_order` | De volgorde van synthetiseren. Bepaalt welke kolommen al bekend zijn als een regel moet ingrijpen. Zie [business-rules.md](business-rules.md#kolomvolgorde). |
| `default_syn_method` | De synthesemethode voor alle kolommen (standaard `CartMethod`) |
| `special_syn_method` | Een eigen methode voor specifieke kolommen, als dict `{kolomnaam: methode}` |
| `BaseSynthMethod` | De basisklasse voor een eigen synthesemethode, met `fit(X, y)`, `transform(X)` en `get_feature_names_out()`. `transform(X)` krijgt de synthetische kolommen die al gemaakt zijn. |

De documentatie van synthpop-py legt dit verder uit, met voorbeelden:

- [Custom synthesis methods](https://github.com/duonl/synthpop-py/blob/main/docs/source/user_guides/8_custom_synthesis_methods.md): hoe een eigen synthesemethode werkt
- [Voorbeeld: custom synthesis method](https://github.com/duonl/synthpop-py/blob/main/docs/source/examples/custom_synth.md)
- [Voorbeeld: de volgorde van synthetiseren aanpassen](https://github.com/duonl/synthpop-py/blob/main/docs/source/examples/changing_the_synthesis_order.md)
- [Evaluating utility](https://github.com/duonl/synthpop-py/blob/main/docs/source/user_guides/5_evaluating_utility.md): S_pMSE en andere manieren om kwaliteit te meten
- De volledige documentatie: [synthpop-py.readthedocs.io](https://synthpop-py.readthedocs.io/)

Lees ook [issue #332](https://github.com/duonl/synthpop-py/issues/332) met tips en implementatierichtlijnen van het DUO-team voor business rules.

## 5. Bouwen in synthpop-py zelf

Wil je je oplossing in het pakket zelf bouwen? Eigen branches op de repository van DUO zijn niet mogelijk, dus werk in een fork:

```bash
# fork duonl/synthpop-py op GitHub, dan:
git clone https://github.com/<jouw-account>/synthpop-py.git ../synthpop-py
pip install -e ../synthpop-py      # je fork vervangt de synthpop-py uit PyPI
python -c "import synthpop; print(synthpop.__file__)"   # controle: wijst naar je fork
```

Daarna gebruiken de scripts en tests in deze repository automatisch je eigen versie. Lees de [CONTRIBUTING.md](https://github.com/duonl/synthpop-py/blob/main/CONTRIBUTING.md) van synthpop-py als je je werk later wilt aanbieden. Een bijdrage is welkom, maar niet verplicht. Opname in het pakket vraagt eerst heldere requirements en een review door het DUO-team.

## 6. Je resultaat vergelijkbaar maken

Zodat de jury de teams goed kan vergelijken:

1. Genereer je eindresultaat met **50.000 rijen en seed 2834727**, net als de nulmeting.
2. Gebruik dezelfde 22 kolommen, met dezelfde namen.
3. Zet je resultaat naast de nulmeting:

```bash
python scripts/evaluate.py output/nulmeting_n50000_seed2834727.csv output/mijn_aanpak.csv \
  --labels nulmeting "mijn aanpak" --md output/vergelijking.md --json output/vergelijking.json
```

Je krijgt per regel het aantal overtredingen, de S_pMSE samengevat, en de kolomparen waar de kwaliteit het meest achteruitging. Vergelijk je meerdere aanpakken? Geef ze allemaal mee: de eerste is steeds de referentie.

Onmogelijke records weggooien of overschrijven maakt het aantal overtredingen kleiner, maar verandert ook de verdelingen. Laat dus altijd zien wat je aanpak met de kwaliteit doet.

## 7. Inleveren

Lever in via Alkemio, met een link naar je code op GitHub (een fork van synthpop-py of een eigen repository, open source). Wat de jury wil zien, staat in de challenge brief.
