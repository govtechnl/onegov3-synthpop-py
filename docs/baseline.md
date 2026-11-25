# Baseline

How often does synthetic data from synthpop-py break the business rules, without any changes? This is the starting point of the challenge.

## Setup

- Original: `data/Synthetic_Homicide.csv` (1,291 rows)
- Synthesis: synthpop-py 1.0.0 with default settings (sequential CART, default column order), `Synthesiser(random_seed=2834727)`, as in DUO's notebook
- Number of synthetic rows: 50,000, as in DUO's notebook: many more synthetic rows than original rows, so that the flaws show
- Rules measured with rulecheck, quality with synthpop-py's pairwise S_pMSE
- Environment: Python 3.13.18, synthpop-py 1.0.0, pandas 3.1.1, scikit-learn 1.9.1, numpy 2.5.5. Same results on Python 3.11 and 3.14.

Run it yourself:

```bash
python scripts/baseline.py
```

## Result

| Rule | Description | Violations |
|---|---|---:|
| 1 | Birth city lies in birth country | 294 (0.59%) |
| 2 | Age difference matches both ages | 35,556 (71.11%) |
| 3.1 | Previous crime not after current crime | 260 (0.52%) |
| 3.2 | Release not before current crime | 349 (0.70%) |
| 4 | Max 10 years; empty if unsolved | 0 (0.00%) |
| 5 | Minors max 5 years, with exception | 105 (0.21%) |
| 6.1 | No evidence if unsolved | 0 (0.00%) |
| 6.2 | Bullets/ballistics only with firearm | 0 (0.00%) |
| 6.3 | No confession if mentally disturbed | 16 (0.03%) |
| 6.4 | Confession only if record complete | 203 (0.41%) |
| | **Rows with at least 1 violation** | **35,935 (71.87%)** |
| | S_pMSE mean (lower is better) | 22.41 |
| | S_pMSE median | 23.38 |
| | S_pMSE maximum | 58.56 |

Seven of the ten rules fail in this run. Rule 2 accounts for most of the violations. The original dataset breaks no rule at all.

## When comparing

- The synthesis is reproducible: the same seed gives exactly the same rows in the same environment. With other versions of synthpop-py, scikit-learn, pandas or numpy the numbers may differ slightly. So run the baseline yourself in your own environment and compare your solution with that.
- Use the same settings as the baseline for your final result: 50,000 rows and seed 2834727. `scripts/evaluate.py` puts the baseline and your result side by side.
