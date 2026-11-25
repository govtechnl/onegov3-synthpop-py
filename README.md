# OneGov #3 | synthpop.py

> *Synthetic data rules! Enforce business rules while synthesising with synthpop-py, without losing data quality.*

This repository holds the starter material for challenge 3 of **OneGov #3**, part of the OneGov Hackathon Series hosted by GovTechNL. The challenge comes from the Team Synthetische Data of DUO, the executive agency of the Dutch Ministry of Education, Culture and Science, which develops the open source package [synthpop-py](https://github.com/duonl/synthpop-py).

- **Theme:** Digital autonomy and sovereignty
- **Date:** 9-10 December 2026
- **Location:** The Hague Tech, The Hague
- **Challenge owners:** Cas van Erp and Erina Koomen (Team Synthetische Data, DUO)
- **Tech partner:** [GreenPT](https://greenpt.nl/)
- **Community, teams and submissions:** [alkem.io/onegov-hackathon](https://alkem.io/onegov-hackathon)
- **Contact:** [hack@govtechnl.nl](mailto:hack@govtechnl.nl)
- **Submission deadline:** Thursday 10 December 2026, 14:00, on [Alkemio](https://alkem.io/onegov-hackathon)
- **Programme, prizes, judging and help:** [EVENT.md](EVENT.md)
- **Organised by:** GovTechNL with Digicampus, The Hague Tech, VNG Realisatie, Provincie Zuid-Holland, Platform AI & Overheid and Gemeente Den Haag

## The challenge in one paragraph

A synthesis model learns patterns from data, but not rules. That is how records arise that are statistically plausible but impossible in substance. With default settings, synthpop-py 1.0.0 breaks seven of the ten business rules that DUO wrote for this hackathon, and 72% of the synthetic rows break at least one rule. **How do we implement user-defined business rules in synthpop-py, so that synthetic data follows those rules during synthesis, while preserving statistical quality?**

The full brief is in [CHALLENGE.md](CHALLENGE.md), an English working translation of the [Dutch brief](resources/OneGov3_Challenge_Brief_synthpop_py.pdf), also on Alkemio (the Dutch brief prevails). New teams start with [START_HERE.md](START_HERE.md).

## What's in here

| Path | Purpose |
|---|---|
| [CHALLENGE.md](CHALLENGE.md) | Full challenge brief (English working translation of the Dutch original) |
| [START_HERE.md](START_HERE.md) | Step-by-step start for teams: setup, how synthpop-py works, where you can intervene, how to measure |
| [data/](data/) | DUO's dataset: a synthetic version of the Dutch Homicide Monitor with extra columns, plus a [data card](data/README.md) |
| [docs/business-rules.md](docs/business-rules.md) | The business rules: exact definitions, missing values, and what the column order means for each rule |
| [docs/baseline.md](docs/baseline.md) | How often synthpop-py 1.0.0 breaks the rules today |
| [docs/judging-criteria.md](docs/judging-criteria.md) | The assessment criteria with IDs, and how judging works |
| [docs/integrations/greenpt-api.md](docs/integrations/greenpt-api.md) | Optional LLM access through the tech partner GreenPT |
| [notebooks/BusinessRules.ipynb](notebooks/BusinessRules.ipynb) | DUO's notebook with one check per rule |
| [src/rulecheck/](src/rulecheck/) | The business rules as Python code (by GovTechNL, tested against DUO's notebook), plus an evaluation of rules and quality |
| [scripts/baseline.py](scripts/baseline.py) | Synthesises the dataset with default settings and measures rules and quality |
| [scripts/evaluate.py](scripts/evaluate.py) | Puts your synthetic data next to the baseline |
| [tests/](tests/) | Tests, including a check that rulecheck flags exactly the same rows as DUO's notebook |
| [resources/OneGov3_Challenge_Brief_synthpop_py.pdf](resources/OneGov3_Challenge_Brief_synthpop_py.pdf) | The Dutch challenge brief (v1.0, authoritative) |
| [EVENT.md](EVENT.md) | Programme, deadline, judging, prizes and help, the same for all four OneGov #3 challenges |

**Everything in this repository is synthetic.** No real people or cases. The business rules were made up by DUO for this hackathon and do not describe reality.

## Quick start

You need Python 3.11 or higher (tested with 3.11, 3.13 and 3.14).

```bash
git clone https://github.com/govtechnl/onegov3-synthpop-py.git
cd onegov3-synthpop-py
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest

# Baseline: synthpop-py with default settings, 50,000 rows (about ten seconds)
python scripts/baseline.py

# Check any CSV with the same 22 columns against the rules
python -m rulecheck output/baseline_n50000_seed2834727.csv

# Compare your own synthetic data with the baseline
python scripts/evaluate.py output/baseline_n50000_seed2834727.csv output/my_approach.csv \
  --labels baseline "my approach" --md output/comparison.md
```

In your own code:

```python
import pandas as pd
from rulecheck import check_rules, violations

df = pd.read_csv("output/my_approach.csv")
print(check_rules(df))      # violations per rule
masks = violations(df)      # one boolean Series per rule: True is a violation
```

## The business rules

| Rule | In short | Baseline* |
|---|---|---:|
| 1 | The main perpetrator's birth city lies in the birth country | 294 (0.6%) |
| 2 | The age difference follows from the ages of victim and main perpetrator | 35,556 (71.1%) |
| 3.1 | The previous crime did not take place after the current crime | 260 (0.5%) |
| 3.2 | The release is not before the date of the current crime | 349 (0.7%) |
| 4 | Solved: at most 10 years in prison. Unsolved: no sentence | 0 |
| 5 | Under 18: at most 5 years, with one exception | 105 (0.2%) |
| 6.1 | Unsolved: no main evidence | 0 |
| 6.2 | 'bullets' and 'ballistics' only with a firearm | 0 |
| 6.3 | No 'confession' from a perpetrator who is not criminally responsible | 16 (0.03%) |
| 6.4 | 'confession' only if the record is complete | 203 (0.4%) |
| 6.5 | 'DNA', 'fingerprints' and 'witnesses' are always allowed | n/a |

\* Rows that break the rule, in 50,000 synthetic rows from synthpop-py 1.0.0 with default settings (seed 2834727, as in DUO's notebook). The original dataset breaks no rule at all. Details in [docs/baseline.md](docs/baseline.md); exact definitions in [docs/business-rules.md](docs/business-rules.md).

DUO's notebook is the reference for the rules. rulecheck is tooling by GovTechNL that makes the same checks easier to run: a test checks that it flags exactly the same rows as the notebook.

## How the jury compares results

The jury wants to see, per rule, the number of violations without and with your solution, and the effect on statistical quality. To keep results comparable between teams, use the same settings as the baseline: 50,000 rows, seed 2834727 and the same 22 columns. Then run `scripts/evaluate.py` with the baseline as reference. It reports the violations per rule, a summary of synthpop-py's pairwise S_pMSE (lower is better) and the column pairs whose quality dropped most. Other quality measures are welcome too.

## Building in synthpop-py

Own branches on DUO's repository are not possible: work in a **fork of [duonl/synthpop-py](https://github.com/duonl/synthpop-py)** or in your own repository. A contribution to the package is welcome, but not required; inclusion in synthpop-py first needs clear requirements and a review by the DUO team. Before you start, read [issue #332](https://github.com/duonl/synthpop-py/issues/332) with tips and implementation guidelines from the DUO team, and synthpop-py's [CONTRIBUTING.md](https://github.com/duonl/synthpop-py/blob/main/CONTRIBUTING.md).

## Submitting

Submit via [Alkemio](https://alkem.io/onegov-hackathon) before **Thursday 10 December 2026, 14:00**, with a link to your code and your comparison with the baseline. Your code is open source and on GitHub, as a fork of synthpop-py or in your own repository. This repository only holds the starter material: do not put your solution here. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Handle the topic with care

The dataset is about homicides. Even though it is synthetic, handle it with care, also in examples, pitches and demos. See the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licences and sources

- **Code:** [EUPL-1.2](LICENSE), the same licence as synthpop-py.
- **Data, documentation and challenge text:** CC BY 4.0, see [LICENSE-DATA](LICENSE-DATA).
- **Dataset:** based on Krüsselmann, K., Achterberg, J., Haas, M., Spruit, M. & Liem, M. (2024). *Synthetic Dutch Homicide Monitor* [Data set]. Leiden University/LUMC. [doi.org/10.5281/zenodo.13378063](https://doi.org/10.5281/zenodo.13378063), CC BY 4.0. DUO added columns; see the [data card](data/README.md).
- **Notebook and business rules:** Team Synthetische Data, DUO.

## Contact

- Questions about synthpop-py and the business rules: the challenge owners, via [synthetische.data@duo.nl](mailto:synthetische.data@duo.nl)
- Questions about the hackathon: [hack@govtechnl.nl](mailto:hack@govtechnl.nl)
