# Notebook van DUO

`BusinessRules.ipynb` is gemaakt door het Team Synthetische Data van DUO. Het laat zien hoe je synthpop-py gebruikt, en dat synthpop-py de business rules nu niet altijd meeneemt: het synthetiseert de dataset en controleert daarna elke regel met een `assert`.

## Openen

```bash
pip install -e ".[notebook]"
jupyter lab notebooks/BusinessRules.ipynb
```

Of open het in VS Code. Het notebook leest de dataset uit `../data/`, dus start het vanuit de map `notebooks/` (dat doen JupyterLab en VS Code standaard).

## Goed om te weten

- Het notebook stopt bij de eerste regel die faalt. Op synthetische data uit synthpop-py 1.0.0 is dat regel 1. Voor een overzicht van alle regels tegelijk: `python -m rulecheck <bestand.csv>`.
- rulecheck meet precies hetzelfde als dit notebook. Een test in `tests/test_notebook_parity.py` bewaakt dat.

## Wijziging ten opzichte van het origineel

Eén regel: het pad naar de dataset (`'Synthetic_Homicide.csv'` werd `'../data/Synthetic_Homicide.csv'`), omdat de dataset in deze repository in `data/` staat. Verder is het notebook ongewijzigd.
