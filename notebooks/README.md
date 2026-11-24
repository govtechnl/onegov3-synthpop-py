# DUO's notebook

`BusinessRules.ipynb` was made by DUO's Team Synthetische Data. It shows how to use synthpop-py, and that synthpop-py does not always respect the business rules yet: it synthesises the dataset and then checks each rule with an `assert`. The notebook's comments and output are in Dutch.

## Opening it

```bash
pip install -e ".[notebook]"
jupyter lab notebooks/BusinessRules.ipynb
```

Or open it in VS Code. The notebook reads the dataset from `../data/`, so start it from the `notebooks/` folder (JupyterLab and VS Code do this by default).

## Good to know

- The notebook stops at the first rule that fails. On synthetic data from synthpop-py 1.0.0 that is rule 1. For an overview of all rules at once: `python -m rulecheck <file.csv>`.
- rulecheck measures exactly the same as this notebook. A test in `tests/test_notebook_parity.py` guards that.

## Change compared with the original

One line: the path to the dataset (`'Synthetic_Homicide.csv'` became `'../data/Synthetic_Homicide.csv'`), because the dataset lives in `data/` in this repository. Otherwise the notebook is unchanged.
