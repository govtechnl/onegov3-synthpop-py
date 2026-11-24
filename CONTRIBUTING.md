# Bijdragen

Deze repository is het startmateriaal voor challenge 3 (synthpop.py) van OneGov #3, op 9 en 10 december 2026 in The Hague Tech. GovTechNL beheert de repository, samen met het Team Synthetische Data van DUO.

## Twee manieren om bij te dragen

### 1. Als hackathonteam: bouw in je eigen repository

1. Bouw je oplossing in een **fork van [duonl/synthpop-py](https://github.com/duonl/synthpop-py)** of in een **eigen repository**. Eigen branches op de repository van DUO zijn niet mogelijk.
2. Gebruik deze repository om je resultaat te meten: `rulecheck`, `scripts/nulmeting.py` en `scripts/evaluate.py`. Zie [docs/aan-de-slag.md](docs/aan-de-slag.md).
3. Lever in via [Alkemio](https://alkem.io/onegov-hackathon), met een link naar je code en je vergelijking met de nulmeting.

Je oplossing hoort dus niet in deze repository. Wil je je werk later aanbieden aan synthpop-py? Lees dan de [CONTRIBUTING.md van synthpop-py](https://github.com/duonl/synthpop-py/blob/main/CONTRIBUTING.md). Opname vraagt heldere requirements en een review door het DUO-team.

### 2. Het startmateriaal verbeteren

Fout gevonden in de data, rulecheck, de scripts of de documentatie? Meld het via een [issue](https://github.com/govtechnl/onegov3-synthpop-py/issues) of stuur een pull request. Houd een pull request klein: één verandering per keer.

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

De CI draait ruff en pytest bij elke push en pull request.

## Afspraken

1. **De regels staan in code.** Een verandering aan een regel in `src/rulecheck/rules.py` moet blijven kloppen met het notebook van DUO. `tests/test_notebook_parity.py` controleert dat. Twijfel je over wat een regel bedoelt? Vraag het de challenge owners.
2. **Het notebook van DUO blijft van DUO.** Verander `notebooks/BusinessRules.ipynb` alleen in overleg met DUO.
3. **Geen echte data.** Zie de [gedragscode](CODE_OF_CONDUCT.md).
4. **Taal.** De documentatie in deze repository is Nederlands, met een Engelse samenvatting in de README en een Engelse werkvertaling van de brief in [CHALLENGE.md](CHALLENGE.md). Code en commentaar in de code zijn Engels, net als in synthpop-py. Je eigen werk mag in het Nederlands of Engels.

## Licenties

- **Deze repository:** code onder **EUPL-1.2** (zie [LICENSE](LICENSE)), dezelfde licentie als synthpop-py. Data, documentatie en challengetekst onder **CC BY 4.0** (zie [LICENSE-DATA](LICENSE-DATA)).
- **Je inzending:** open source onder een door de OSI goedgekeurde licentie. Bouw je in een fork van synthpop-py, dan geldt de licentie van synthpop-py: EUPL-1.2. Voor een eigen repository raden we EUPL-1.2 aan, zodat je werk later makkelijk in synthpop-py past.
- **Bijdragen aan deze repository** vallen onder dezelfde licenties als hierboven.
