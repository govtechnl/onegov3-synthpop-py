# Start Here (Hackathon Teams)

If you are starting the challenge now, follow this order.

## 1) Understand the scope (10 min)

- Read [CHALLENGE.md](CHALLENGE.md), especially the assessment criteria. Every Must is blocking.
- Read [docs/business-rules.md](docs/business-rules.md): the rules, how missing values count, and which rules clash with synthpop-py's default column order.
- Look at [docs/baseline.md](docs/baseline.md): where synthpop-py goes wrong today.

## 2) Set up (10 min)

You need Python 3.11 or higher and git. Tested with Python 3.11, 3.13 and 3.14 on Linux, and 3.13 on Windows and macOS.

```bash
git clone https://github.com/govtechnl/onegov3-synthpop-py.git
cd onegov3-synthpop-py
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"            # rulecheck, synthpop-py, pytest and ruff
pip install -e ".[notebook]"       # optional: JupyterLab for DUO's notebook
pytest                             # all green? Your environment works.
```

## 3) Run the baseline (5 min)

```bash
python scripts/baseline.py
```

The script synthesises the dataset with synthpop-py's default settings (50,000 rows, seed 2834727), counts the violations per rule and measures quality. Everything lands in `output/`: the synthetic CSV, a JSON with all numbers and package versions, and a Markdown table.

## 4) Check synthetic data against the rules

Any CSV with the same 22 columns:

```bash
python -m rulecheck output/baseline_n50000_seed2834727.csv
python -m rulecheck my_data.csv --json        # as JSON
python -m rulecheck my_data.csv --strict      # exit code 1 on any violation, handy in tests
```

Or in Python:

```python
from rulecheck import check_rules, violations, any_violation

check_rules(df)        # table with violations per rule
violations(df)["2"]    # boolean Series for rule 2: True is a violation
any_violation(df)      # True for rows that break at least one rule
```

## 5) Understand how synthpop-py works (20 min)

synthpop-py synthesises a table **column by column**. The first column is sampled. Every next column is predicted from the columns that came before it, by default with CART (decision trees).

```python
from synthpop import Synthesiser

syn = Synthesiser(random_seed=2834727).fit(df).generate(50_000)
```

- `fit(X)` trains one synthesis method per column on the original data, with the earlier columns as predictors.
- `generate(n)` creates the columns in the same order. Each method receives the synthetic columns that already exist.

This is where you can intervene:

| Hook | What it does |
|---|---|
| `column_order` | The order of synthesis. Decides which columns are known when a rule has to act. See [docs/business-rules.md](docs/business-rules.md#column-order). |
| `default_syn_method` | The synthesis method for all columns (default: `CartMethod`) |
| `special_syn_method` | Your own method for specific columns, as a dict `{column_name: method}` |
| `BaseSynthMethod` | Base class for your own synthesis method, with `fit(X, y)`, `transform(X)` and `get_feature_names_out()`. `transform(X)` receives the synthetic columns created so far. |

synthpop-py's documentation explains this further, with examples:

- [Custom synthesis methods](https://github.com/duonl/synthpop-py/blob/main/docs/source/user_guides/8_custom_synthesis_methods.md): how your own synthesis method works
- [Example: custom synthesis method](https://github.com/duonl/synthpop-py/blob/main/docs/source/examples/custom_synth.md)
- [Example: changing the synthesis order](https://github.com/duonl/synthpop-py/blob/main/docs/source/examples/changing_the_synthesis_order.md)
- [Evaluating utility](https://github.com/duonl/synthpop-py/blob/main/docs/source/user_guides/5_evaluating_utility.md): S_pMSE and other ways to measure quality
- Full documentation: [synthpop-py.readthedocs.io](https://synthpop-py.readthedocs.io/)

Also read [issue #332](https://github.com/duonl/synthpop-py/issues/332) with tips and implementation guidelines on business rules from the DUO team.

## 6) Pick your angle

The brief suggests three directions. They do not exclude each other:

- **Enforce during synthesis:** let synthpop-py only choose values that fit the columns already generated, for example with your own synthesis method via `special_syn_method`. The R package synthpop does something similar with restricted values (`rules` and `rvalues`).
- **Generate again:** detect violations and regenerate the wrong values or records, with a limit on the number of attempts.
- **Derive instead of synthesise:** some rules allow only one value, such as the age difference. Compute such a column from other columns, like passive synthesis in the R package.

Whatever you pick: think about how a data scientist passes rules to synthpop-py (a rule format, an API or a configuration file), and make sure it works for another dataset without changing your code.

## 7) Build in synthpop-py itself (optional)

Own branches on DUO's repository are not possible, so work in a fork:

```bash
# fork duonl/synthpop-py on GitHub, then:
git clone https://github.com/<your-account>/synthpop-py.git ../synthpop-py
pip install -e ../synthpop-py      # your fork replaces synthpop-py from PyPI
python -c "import synthpop; print(synthpop.__file__)"   # check: points to your fork
```

From then on, the scripts and tests in this repository use your version. Read synthpop-py's [CONTRIBUTING.md](https://github.com/duonl/synthpop-py/blob/main/CONTRIBUTING.md) if you want to offer your work later. A contribution is welcome, but not required. Inclusion in the package first needs clear requirements and a review by the DUO team.

## 8) Make your result comparable

So the jury can compare teams:

1. Generate your final result with **50,000 rows and seed 2834727**, like the baseline.
2. Use the same 22 columns, with the same names.
3. Put your result next to the baseline:

```bash
python scripts/evaluate.py output/baseline_n50000_seed2834727.csv output/my_approach.csv \
  --labels baseline "my approach" --md output/comparison.md --json output/comparison.json
```

You get the number of violations per rule, an S_pMSE summary, and the column pairs whose quality dropped most. Comparing several approaches? Pass them all: the first file is always the reference.

Discarding or overwriting impossible records lowers the number of violations, but also changes the distributions. Always show what your approach does to quality.

## 9) Submit

Submit via [Alkemio](https://alkem.io/onegov-hackathon), with a link to your code on GitHub (a fork of synthpop-py or your own repository, open source) and your comparison with the baseline. The full list of deliverables is in [CHALLENGE.md](CHALLENGE.md#what-do-you-deliver).
