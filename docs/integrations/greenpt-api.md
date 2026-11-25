# GreenPT API (optional)

[GreenPT](https://greenpt.nl/), the tech partner of the OneGov Hackathon Series, provides an OpenAI-compatible API to LLMs hosted on European infrastructure. It is an **optional resource**: this challenge can be solved entirely without an LLM.

## Where an LLM call might help

- **From plain language to a rule.** Turn a rule a data scientist writes in words ("the release date is never before the crime date") into a draft in your rule format, for a person to check and test.
- **Explaining violations.** Summarise the output of `rulecheck` or `scripts/evaluate.py` in plain language for a pitch or a README.
- **Suggesting candidate rules** (bonus C3), as a starting point that you then check against the data.

## Where an LLM call should **not** be used

- To decide whether a record breaks a rule. That is what `rulecheck` and your own rule code do.
- To generate or repair synthetic data values. The synthesis stays in synthpop-py, so it can be measured.
- With real personal data. Only the synthetic dataset in this repository.

## Practical notes

- **Access.** Every participant can claim free API credits through GreenPT's sign-up link, shared on [Alkemio](https://alkem.io/onegov-hackathon) and at the kick-off. Documentation: [docs.greenpt.ai](https://docs.greenpt.ai/).
- **Secrets.** Keep keys in environment variables, never in a repository.
- **Reproducibility.** Pin a model and log prompts and responses wherever they influence a rule.

If your submission uses GreenPT or another LLM, note in your README and your Alkemio submission **where** and **why**.

GreenPT awards a bonus prize to a team that makes good use of its API; GreenPT selects the winner. See [EVENT.md](../../EVENT.md#prizes).
