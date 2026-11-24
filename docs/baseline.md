# Baseline

How often does synthetic data from synthpop-py break the business rules, without any changes? This is the starting point of the challenge.

## Setup

- Original: `data/Synthetic_Homicide.csv` (1,291 rows)
- Synthesis: synthpop-py 1.0.0 with default settings (sequential CART, default column order), `Synthesiser(random_seed=2834727)`, as in DUO's notebook
- Number of synthetic rows: 50,000, as in DUO's notebook ("many more synthetic rows than original rows, so that the flaws show"). For comparison also 1,291, as many as the original.
- Rules measured with rulecheck, quality with synthpop-py's pairwise S_pMSE
- Environment: Python 3.13.18, synthpop-py 1.0.0, pandas 3.1.1, scikit-learn 1.9.1, numpy 2.5.5. Same results on Python 3.11 and 3.14.

Run it yourself:

```bash
python scripts/baseline.py              # 50,000 rows
python scripts/baseline.py --n 1291     # as many rows as the original
```

## Result

| Rule | Description | 50,000 rows | 1,291 rows |
|---|---|---:|---:|
| 1 | Birth city lies in birth country | 294 (0.59%) | 5 (0.39%) |
| 2 | Age difference matches both ages | 35,556 (71.11%) | 913 (70.72%) |
| 3.1 | Previous crime not after current crime | 260 (0.52%) | 8 (0.62%) |
| 3.2 | Release not before current crime | 349 (0.70%) | 14 (1.08%) |
| 4 | Max 10 years; empty if unsolved | 0 (0.00%) | 0 (0.00%) |
| 5 | Minors max 5 years, with exception | 105 (0.21%) | 3 (0.23%) |
| 6.1 | No evidence if unsolved | 0 (0.00%) | 0 (0.00%) |
| 6.2 | Bullets/ballistics only with firearm | 0 (0.00%) | 0 (0.00%) |
| 6.3 | No confession if mentally disturbed | 16 (0.03%) | 0 (0.00%) |
| 6.4 | Confession only if record complete | 203 (0.41%) | 5 (0.39%) |
| | **Rows with at least 1 violation** | **35,935 (71.87%)** | **921 (71.34%)** |
| | S_pMSE mean (lower is better) | 22.41 | 1.48 |
| | S_pMSE median | 23.38 | 1.55 |
| | S_pMSE maximum | 58.56 | 3.12 |

The original dataset breaks no rule at all.

## What stands out

- **Seven of the ten rules fail.** Only rules 4, 6.1 and 6.2 do not fail in this run. Probably because the allowed values there depend strongly on one column that comes earlier ('Solved vs unsolved homicide' or 'Type of weapon used'), and CART picks up such a relation well. That is no guarantee: with another seed or more rows they can still fail.
- **Rule 2 is by far the biggest.** The age difference is predicted on its own, instead of computed from the two ages. As a result it is wrong in over 70% of the rows.
- **The other rules fail rarely, but structurally.** At 50,000 rows that means dozens to hundreds of impossible records per rule. One impossible record can be enough to lose trust in a dataset.
- **S_pMSE depends strongly on the number of rows.** Only compare quality between datasets with the same number of rows.

## When comparing

- The synthesis is reproducible: the same seed gives exactly the same rows in the same environment. With other versions of synthpop-py, scikit-learn, pandas or numpy the numbers may differ slightly. So run the baseline yourself in your own environment and compare your solution with that.
- Use the same settings as the baseline for your final result: 50,000 rows and seed 2834727. `scripts/evaluate.py` puts the baseline and your result side by side.
