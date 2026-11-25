# The business rules

DUO made up these rules for the hackathon. **They do not describe reality.** The original dataset follows every rule; synthetic data from synthpop-py 1.0.0 does not (see [baseline.md](baseline.md)).

The code in [`src/rulecheck/rules.py`](../src/rulecheck/rules.py) is the exact definition. It follows [DUO's notebook](../notebooks/BusinessRules.ipynb), including how missing values count. A test checks that rulecheck and the notebook give the same answer for every row.

## Overview

| Rule | Description | Columns | Missing values |
|---|---|---|---|
| 1 | The main perpetrator's birth city lies in the birth country, according to DUO's list | Birthcity of main perpetrator, Birthcountry of main perpetrator | Unknown city: always fine. Known city with unknown country: violation. |
| 2 | Age difference = \|age of main perpetrator - age of victim\| | Age difference, Age of main perpetrator, Age of victim | Empty age difference: fine. A filled-in difference while an age is missing: violation. |
| 3.1 | The main perpetrator's previous crime did not take place after the current crime | Date of previous crime main perpetrator, Date of current crime | Empty date: fine |
| 3.2 | The release for the current crime is not before the date of that crime | Date of current crime, Date of release from current crime main perpetrator | Empty date: fine. Same date: fine. |
| 4 | Solved: prison sentence at most 10 years. Unsolved: the sentence is empty. | Years prison sentence main perpetrator, Solved vs unsolved homicide | Empty sentence for a solved case: fine |
| 5 | A main perpetrator under 18 gets at most 5 years, unless older than 12 and the relationship is '(Step)Parent' or 'Other relative' | Age of main perpetrator, Years prison sentence main perpetrator, Victim-perpetrator relationship | Empty age or sentence: fine |
| 6.1 | Unsolved case: the main evidence is empty | Main evidence type, Solved vs unsolved homicide | |
| 6.2 | 'bullets' and 'ballistics' only if the weapon is 'Firearm' | Main evidence type, Type of weapon used | An empty weapon does not count as a firearm: violation |
| 6.3 | No 'confession' if the context is 'Killing by mentally disturbed person (non-family)' | Main evidence type, Context of homicide | |
| 6.4 | 'confession' only if all other columns are filled in, except the date of the previous crime, the release date and the sentence | Main evidence type and 18 other columns | One empty required column with 'confession': violation |
| 6.5 | 'DNA', 'fingerprints' and 'witnesses' are always allowed | Main evidence type | No constraint, not counted |

Rules 6.2 to 6.4 apply to solved cases. For unsolved cases rule 6.1 applies: there should be no main evidence at all.

## Column order

synthpop-py synthesises column by column, by default in the order of the CSV. Each column is predicted from the columns that came before it. During synthesis, a rule can therefore only act at the last of its columns: that is when the other columns are known. This decides where you can enforce a rule, and whether you need to change the order (`column_order`).

| No. | Column | Rules |
|---:|---|---|
| 1 | Urban vs rural | 6.4 |
| 2 | Time of day | 6.4 |
| 3 | Single vs multiple homicide victims | 6.4 |
| 4 | Single vs multiple homicide perpetrators | 6.4 |
| 5 | Type of crimescene | 6.4 |
| 6 | Type of weapon used | 6.2, 6.4 |
| 7 | Context of homicide | 6.3, 6.4 |
| 8 | Victim-perpetrator relationship | 5, 6.4 |
| 9 | Solved vs unsolved homicide | 4, 6.1 to 6.4 |
| 10 | Gender of victim | 6.4 |
| 11 | Gender of main perpetrator | 6.4 |
| 12 | Age of victim | 2, 6.4 |
| 13 | Age of main perpetrator | 2, 5, 6.4 |
| 14 | Age difference | **2**, 6.4 |
| 15 | Main evidence type | **6.1, 6.2, 6.3**, 6.4 |
| 16 | Birthcountry of victim | 6.4 |
| 17 | Birthcity of main perpetrator | 1, 6.4 |
| 18 | Birthcountry of main perpetrator | **1**, 6.4 |
| 19 | Date of current crime | 3.1, 3.2, **6.4** |
| 20 | Date of previous crime main perpetrator | **3.1** |
| 21 | Date of release from current crime main perpetrator | **3.2** |
| 22 | Years prison sentence main perpetrator | **4, 5** |

In bold: in the default order, all other columns of the rule are known at this column.

Two things to watch:

- **Rule 6.4 depends on columns before and after 'Main evidence type'.** Only at column 19 is everything known, but by then 'Main evidence type' (15) and columns 16 to 18 have already been chosen. You can split the rule: at column 15, no 'confession' if one of columns 1 to 14 is empty, and at columns 16 to 19, no empty value if the main evidence is 'confession'. Or you change the order.
- **For rule 1, the city comes before the country.** So the country is chosen for a city that is already known, not the other way round. You can enforce the rule at the country, or swap the order.

A different order also changes the quality of the synthetic data. Measure that too.

## Clarifications

rulecheck follows DUO's notebook. DUO confirmed the first three points.

1. **Rule 2 uses the absolute difference**, so the age difference is never negative.
2. **Rule 5 uses the values '(Step)Parent' and 'Other relative'** as they appear in the column 'Victim-perpetrator relationship'.
3. **Rule 6.2 uses lower case:** 'bullets' and 'ballistics', as in the data.
4. **Rule 6.5 is not a constraint.** The notebook only checks that the three values occur. rulecheck does not count the rule.
5. **The notebook stops at the first rule that fails.** Each check ends with an `assert`. On synthetic data from synthpop-py 1.0.0, the notebook already stops at rule 1. Use `python -m rulecheck` for an overview of all rules at once.

Questions about the rules? Ask the challenge owners, Cas van Erp and Erina Koomen ([synthetische.data@duo.nl](mailto:synthetische.data@duo.nl)).
