# Judging criteria

The criteria from the challenge brief, with IDs so teams, mentors and the jury can refer to them. The Dutch brief prevails.

A submission that fails any Must criterion is not a valid submission, regardless of how well it scores on the rest.

## ✅ Must: minimum requirements for a valid submission

| # | Criterion | What the jury looks for |
|---|---|---|
| M1 | A working prototype that takes user-defined business rules into account when synthesising with synthpop-py. | A demo or recording: rules go in, synthetic data comes out of synthpop-py |
| M2 | Per rule, the number of violations without and with the solution, measured on DUO's dataset with rulecheck or DUO's notebook. | The table from `scripts/evaluate.py`, 50,000 rows, seed 2834727 |
| M3 | Insight into the effect on statistical quality, for example with synthpop-py's S_pMSE score or another metric. | Quality before and after, at the baseline settings (50,000 rows, seed 2834727) |
| M4 | The solution is open source and includes a short explanation of how to add a rule. | Public repository, linked in Alkemio, under an OSI-approved licence; a README section on adding a rule |

## ⭐ Should: distinguishing qualities

| # | Criterion | What the jury looks for |
|---|---|---|
| S1 | A data scientist can add rules for another dataset without changing the solution's code. | Rules as configuration or a small API, shown on a second example |
| S2 | The number of violations drops as close to zero as possible for all rules, without noticeable loss of quality. | All ten checkable rules, not only the easy ones |
| S3 | The solution fits the architecture of synthpop-py, for example as a synthesis method or as a step in synthesis. | Uses `special_syn_method`, `column_order` or a comparable extension point |
| S4 | The team substantiates the trade-off between enforcing rules and preserving quality. | A short argument backed by the measurements |

## ⚠ Should not: pitfalls to avoid

| # | Pitfall | Why it weakens a submission |
|---|---|---|
| X1 | Silently discarding or overwriting impossible records, without showing what that does to the distributions. | Hides the cost the challenge asks you to measure |
| X2 | Hardcoding rules for this one dataset. | Fails S1 |
| X3 | Claiming quality without measuring it. | Fails M3 |

## ✨ Could: bonus

| # | Criterion | What the jury looks for |
|---|---|---|
| C1 | Comparing several approaches, for example enforcing during synthesis versus repairing afterwards. | Two or more approaches measured the same way |
| C2 | A visualisation of violations and quality before and after. | A chart or small dashboard |
| C3 | Suggestions for rules missing from the rule set, based on the data. | Candidate rules with the evidence for them |
| C4 | A contribution with tests and documentation, ready for review by the DUO team, or bug fixes for synthpop-py found along the way. | A fork of synthpop-py with tests, or a bug report or fix |

## How judging works

Musts are pass or fail. Teams pitch per challenge in a first round (10 December, 14:00-15:00), a technical jury reviews every submission in Alkemio, and the best team per challenge goes to the final, where the grand jury scores six criteria from 1 to 5. See [EVENT.md](../EVENT.md#how-judging-works).
