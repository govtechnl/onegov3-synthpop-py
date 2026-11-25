# Challenge brief: Synthetic data rules! Business rules in synthpop-py

*English working translation of the Dutch challenge brief (v1.0). The [Dutch brief](resources/OneGov3_Challenge_Brief_synthpop_py.pdf), also on [Alkemio](https://alkem.io/onegov-hackathon), prevails.*

A synthesis model learns patterns from data, but not rules. That is how records arise that are statistically plausible but impossible in substance. Teams build, for synthpop-py (DUO's open source synthesis software), a way to enforce business rules during synthesis while preserving the quality of the data.

| | |
|---|---|
| Project | OneGov Hackathon Series, edition #3 |
| Theme | Digital autonomy and sovereignty |
| Submitted by | Team Synthetische Data, DUO (Ministry of Education, Culture and Science) |
| Challenge no. | Challenge 3 |
| Date | 9-10 December 2026 |
| Location | The Hague Tech, The Hague |

## Challenge owners

Cas van Erp and Erina Koomen of DUO's Team Synthetische Data are the challenge owners. They prepare the dataset and the business rules and answer questions about synthpop-py. Contact: synthetische.data@duo.nl.

## Background

Government organisations hold valuable data, but often may not share it at the level of individuals. Synthetic data offers a way out: artificial data that reproduces the statistical patterns of real data, without a one-to-one relation to real people. DUO ran a pilot with synthetic data from 2022 to 2025 and now structurally provides synthetic datasets to researchers and partners.

For this, the Team Synthetische Data builds synthpop-py: an open source Python package based on the R package synthpop, developed with the consent of, and in cooperation with, its makers. Version 1.0.0 was released on 27 October 2026 under the EUPL 1.2.

synthpop-py synthesises column by column, by default with CART (decision trees). Each column is predicted from the columns that came before it. This way the package picks up the relations in the data, but not the rules behind them. Business rules are therefore on the synthpop-py roadmap.

This ties in with the theme of this edition. An open package with a broad group of users and contributors makes government less dependent on one team or one vendor. DUO wrote earlier that the long-term maintenance of the R package is uncertain, because there is no supporting organisation behind it. The team therefore wants to develop synthpop-py further together with users and contributors.

## Problem statement

Anyone who creates synthetic data runs into the same limits:

- A synthesis model learns patterns, not rules. This produces records that are statistically plausible but impossible in substance, such as a pupil in year 5 of vmbo.
- Business rules are often logical consequences of the reality behind the data, such as exam grades that are always rounded to one decimal. A data scientist knows them, but synthpop-py cannot take them into account yet.
- Repairing afterwards comes at a price: whoever discards or alters wrong records silently changes the distributions and relations that mattered.
- One impossible record undermines trust in the whole dataset, even if the statistics are otherwise right.

In the baseline for this challenge, synthetic data from synthpop-py 1.0.0 breaks seven of the ten rules that can be checked. In 72% of the rows at least one rule fails.

## The challenge

> How do we implement user-defined business rules in synthpop-py, so that synthetic data follows those rules during synthesis, while preserving statistical quality?

Business rules are constraints on the data that a user defines. For this challenge, DUO provides them in advance, together with the dataset. The question is how synthpop-py takes them into account during synthesis, and what that costs in quality. Teams are free in their approach: a creative idea is just as welcome as code that fits directly into the package.

## The dataset and the business rules

DUO manages a lot of interesting data, but for this hackathon chose a dataset that speaks more to the imagination: a synthetic version of the Dutch Homicide Monitor (Leiden University and LUMC), about homicides in the Netherlands. A real dataset with this content may not be shared. In the hackathon, this synthetic set therefore counts as the 'real' dataset: teams create a new synthetic version of it that follows the business rules.

The dataset has 1,291 cases and 22 columns: characteristics of the case, the victim and the main perpetrator, plus dates, evidence and sentence. For the hackathon, DUO added a number of columns following business rules they made up themselves. So the rules do not describe reality.

Source: Krüsselmann, K., Achterberg, J., Haas, M., Spruit, M. & Liem, M. (2024). Synthetic Dutch Homicide Monitor [Data set]. Leiden University/LUMC. [doi.org/10.5281/zenodo.13378063](https://doi.org/10.5281/zenodo.13378063) (CC BY 4.0). Background: [dutchhomicide.streamlit.app](https://dutchhomicide.streamlit.app/).

### The six business rules

| Rule | Description | Baseline |
|---|---|---:|
| 1 | The birth city of the main perpetrator lies in the birth country. | 294 (0.6%) |
| 2 | The age difference follows from the ages of victim and main perpetrator. | 35,556 (71.1%) |
| 3.1 | The main perpetrator's previous crime did not take place after the current crime. | 260 (0.5%) |
| 3.2 | The release for the current crime is not before the date of that crime. | 349 (0.7%) |
| 4 | For a solved case the prison sentence is at most 10 years. For an unsolved case it is empty. | 0 |
| 5 | A main perpetrator under 18 gets at most 5 years, unless older than 12 and the relationship with the victim is '(Step)Parent' or 'Other relative'. | 105 (0.2%) |
| 6.1 | For an unsolved case the main evidence (Main evidence type) is empty. | 0 |
| 6.2 | 'bullets' and 'ballistics' are only possible if the weapon is a firearm. | 0 |
| 6.3 | No 'confession' for a homicide by a perpetrator who is not criminally responsible ('Killing by mentally disturbed person (non-family)'). | 16 (0.03%) |
| 6.4 | 'confession' only if all other columns are filled in, except the date of the previous crime, the release date and the sentence. | 203 (0.4%) |
| 6.5 | 'DNA', 'fingerprints' and 'witnesses' are always allowed. | n/a |

Baseline: number of rows that break the rule, in 50,000 synthetic rows from synthpop-py 1.0.0 with default settings (CART, seed 2834727), as in DUO's notebook. The original dataset breaks no rule at all. The exact definition of each rule is available as code in the starter repository.

## Possible approaches

Three directions for inspiration. They do not exclude each other.

| Enforce during synthesis | Generate again | Derive instead of synthesise |
|---|---|---|
| Let synthpop-py only choose values per column that fit the columns already generated, for example with your own synthesis method via special_syn_method. The R package synthpop does something similar with restricted values (rules and rvalues). | Detect violations and regenerate the wrong values or records in a targeted way, until they follow the rules. Limit the number of attempts and show what it does to the distributions. | Some rules allow only one value, such as the age difference. You can compute such a column from other columns instead of synthesising it, like passive synthesis in the R package. |

How a data scientist passes their rules to synthpop-py is part of every approach: a rule format, an API or a configuration file. The order in which synthpop-py synthesises columns (column_order) determines which columns are already known at the moment a rule has to intervene.

## Resources and starter material

GovTechNL prepares a starter repository together with DUO: [github.com/govtechnl/onegov3-synthpop-py](https://github.com/govtechnl/onegov3-synthpop-py). Teams are free to deviate from it.

| Resource | What it is | Use |
|---|---|---|
| [Starter repository onegov3-synthpop-py](https://github.com/govtechnl/onegov3-synthpop-py) | Dataset, the business rules as Python code (rulecheck), DUO's notebook, a baseline and tests | Clone the repo, run the baseline and check your own output with rulecheck. |
| [synthpop-py](https://github.com/duonl/synthpop-py) | The package itself (EUPL 1.2), with user guide, examples and developer guide on synthpop-py.readthedocs.io | Fork the package if you build in synthpop-py itself. Own branches on DUO's repository are not possible. |
| [Issue #332: business rules](https://github.com/duonl/synthpop-py/issues/332) | Tips and implementation guidelines from the DUO team | Read this before you start. |
| [R package synthpop](https://www.synthpop.org.uk/) | The original package, with restricted values and passive synthesis | Inspiration for how rules and derived columns work in synthpop. |
| [Dutch Homicide Monitor](https://dutchhomicide.streamlit.app/) | Background on the original dataset | Context for the columns and values. |
| GreenPT API (tech partner) | OpenAI-compatible API with credits per participant | Optional, for example to turn rules in plain language into code. See [docs/integrations/greenpt-api.md](docs/integrations/greenpt-api.md). |

All data in the repository is synthetic. No real personal data goes through the challenge.

## What do you deliver?

- A working prototype in Python that takes user-defined business rules into account when synthesising with synthpop-py.
- Per rule, the number of violations without and with your solution, measured on DUO's dataset, and the effect on statistical quality.
- A short explanation: your approach, how a data scientist adds a rule, and the assumptions and limitations.
- The source code, published open source on GitHub: as a fork of synthpop-py or in your own repository.
- A pitch (max. 3 minutes) and a pitch deck (max. 10 slides).
- Your submission via [Alkemio](https://alkem.io/onegov-hackathon), with a link to the code, before **Thursday 10 December 2026, 14:00**.

## Assessment criteria

Teams are assessed by an expert jury with expertise in synthetic data and open source software development. Four levels:

The criteria with IDs (M1 to M4, S1 to S4, X1 to X3, C1 to C4) are in [docs/judging-criteria.md](docs/judging-criteria.md).

**✅ Must: minimum requirements for a valid submission**

- A working prototype that takes user-defined business rules into account when synthesising with synthpop-py.
- Per rule, the number of violations without and with the solution, measured on DUO's dataset with rulecheck or DUO's notebook.
- Insight into the effect on statistical quality, for example with synthpop-py's S_pMSE score or another metric.
- The solution is open source and includes a short explanation of how to add a rule.

**⭐ Should: distinguishing qualities**

- A data scientist can add rules for another dataset without changing the solution's code.
- The number of violations drops as close to zero as possible for all rules, without noticeable loss of quality.
- The solution fits the architecture of synthpop-py, for example as a synthesis method or as a step in synthesis.
- The team substantiates the trade-off between enforcing rules and preserving quality.

**⚠️ Should not: pitfalls to avoid**

- Silently discarding or overwriting impossible records, without showing what that does to the distributions.
- Hardcoding rules for this one dataset.
- Claiming quality without measuring it.

**✨ Could: bonus**

- Comparing several approaches, for example enforcing during synthesis versus repairing afterwards.
- A visualisation of violations and quality before and after.
- Suggestions for rules missing from the rule set, based on the data.
- A contribution with tests and documentation, ready for review by the DUO team, or bug fixes for synthpop-py that you come across along the way.

## Conditions

**Technology.** synthpop-py 1.0.0 runs on Python 3.11 or higher, with pandas and scikit-learn (pip install synthpop-py). The package synthesises one table at a time, column by column. A rule that constrains column B based on column A can only intervene during synthesis if A came first. The R package places the same requirement on its rules.

**Contributing to synthpop-py.** Own branches on DUO's repository are not possible: work in a fork. A contribution to the package is welcome, but not required. Before anything is included in synthpop-py, clear requirements and a review by the DUO team are needed. Merging directly after the hackathon is therefore not the expectation.

**Out of scope.** An adjustable privacy level and support for large datasets are not part of this challenge.

**Handle the topic with care.** The dataset is about homicides. Even though it is synthetic, handle it with care, also in examples, pitches and demos.

## Why you want to be there

- The winning team of this challenge pitches its solution at DUO.
- You help build synthpop-py, open source government software, together with the team that develops the package.
- The DUO team is happy to stay in touch with teams that want to keep building after the hackathon. Bug fixes are always welcome.
- Everything you build is published open source.

## Disclaimer

The solutions created during this hackathon are published as open source. The challenge is an innovation exercise: inclusion in synthpop-py is not guaranteed and first requires clear requirements and a review by DUO's Team Synthetische Data. The dataset and the business rules are synthetic and do not describe reality.

Questions about the hackathon: hack@govtechnl.nl
