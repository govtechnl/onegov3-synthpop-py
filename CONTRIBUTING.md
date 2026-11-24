# Contributing

Thanks for your interest in the **OneGov #3 | synthpop.py** challenge repository.

This repo is maintained by **GovTechNL**, together with DUO's Team Synthetische Data, for challenge 3 of the hackathon on **9-10 December 2026** at The Hague Tech. Contributions are welcome from organisers, mentors, challenge owners, participating teams and the wider community.

## Two contribution flows

### 1. Hackathon teams: build in your own repository

This is the primary flow during the hackathon.

1. Build your solution in a **fork of [duonl/synthpop-py](https://github.com/duonl/synthpop-py)** or in **your own repository**. Own branches on DUO's repository are not possible.
2. Use this repository to measure your result: `rulecheck`, `scripts/baseline.py` and `scripts/evaluate.py`. See [START_HERE.md](START_HERE.md).
3. Submit via [Alkemio](https://alkem.io/onegov-hackathon), with a link to your code and your comparison with the baseline.

Your solution does not go into this repository. Want to offer your work to synthpop-py later? Read [synthpop-py's CONTRIBUTING.md](https://github.com/duonl/synthpop-py/blob/main/CONTRIBUTING.md). Inclusion needs clear requirements and a review by the DUO team.

### 2. Improving the starter repo

Found a mistake in the data, rulecheck, the scripts or the documentation? Report it with an [issue](https://github.com/govtechnl/onegov3-synthpop-py/issues) or open a pull request. Keep pull requests focused: one change at a time.

## Ground rules

1. **The rules live in code.** A change to a rule in `src/rulecheck/rules.py` must keep matching DUO's notebook. `tests/test_notebook_parity.py` checks that. Unsure what a rule means? Ask the challenge owners.
2. **DUO's notebook stays DUO's.** Only change `notebooks/BusinessRules.ipynb` in agreement with DUO.
3. **No real data.** See the [Code of Conduct](CODE_OF_CONDUCT.md).
4. **Language.** Documentation in this repo is English. DUO's notebook and original assignment description are in Dutch, and the Dutch challenge brief prevails over [CHALLENGE.md](CHALLENGE.md). Your pitch and explanation may be in Dutch or English.

## Development workflow

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs ruff, the tests and a small baseline on every push and pull request. Make sure they pass locally before opening a pull request.

## Licensing of contributions

- This **starter repository** is licensed under **EUPL-1.2** for code (see [LICENSE](LICENSE)), the same licence as synthpop-py, and **CC BY 4.0** for data, documentation and challenge text (see [LICENSE-DATA](LICENSE-DATA)).
- **Hackathon team submissions** must be open source under an **OSI-approved licence**. If you build in a fork of synthpop-py, synthpop-py's licence applies: EUPL-1.2. For your own repository we recommend EUPL-1.2 as well, so your work can move into synthpop-py later.
- Contributions *to this starter repo* fall under the same licences as above.
