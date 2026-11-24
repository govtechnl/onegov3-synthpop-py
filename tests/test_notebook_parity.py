"""rulecheck must give exactly the same answer as DUO's notebook."""

import json
import re

import numpy as np
import pandas as pd
import pytest

from conftest import NOTEBOOK, ROOT
from rulecheck import violations


def check_cells() -> list[str]:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    # skip reading the data, the (commented) install cell and the synthesis
    return [c for c in code if c.strip() and not c.lstrip().startswith(("import pandas", '# """', "from synthpop"))]


def run_checks(df: pd.DataFrame, keep_asserts: bool) -> dict:
    ns = {"pd": pd, "np": np, "syn_df": df.copy(), "print": lambda *a, **k: None}
    for src in check_cells():
        if not keep_asserts:
            src = re.sub(r"(?m)^(\s*)assert ", r"\1_assert_result = ", src)
        exec(compile(src, str(NOTEBOOK), "exec"), ns)
    return ns


def notebook_masks(df: pd.DataFrame) -> dict:
    ns = run_checks(df, keep_asserts=False)
    s, unsolved = ns["syn_df"], ns["mask_unsolved_syn"]
    ev = s["Main evidence type"]
    crime = ns["mask_crime_syn"]
    return {
        "1": ns["mask_city_mapping"],
        "2": ns["Wrong_age_diff"],
        "3": crime,
        "4": ns["mask_prison_sentence_syn"],
        "5": ns["mask_age_18_syn"],
        "6.1": unsolved & ev.notna(),
        "6.2": ns["mask_firearm_syn"] & ~(s["Type of weapon used"] == "Firearm"),
        "6.3": ns["mask_no_mentally_disturb"] & (ev == "confession"),
        "6.4": ns["mask_any_nan_syn"] & (ev == "confession"),
    }


def test_notebook_reads_the_repository_data():
    assert "pd.read_csv('../data/Synthetic_Homicide.csv')" in NOTEBOOK.read_text(encoding="utf-8")
    assert (NOTEBOOK.parent / "../data/Synthetic_Homicide.csv").resolve() == (ROOT / "data" / "Synthetic_Homicide.csv")


@pytest.mark.parametrize("dataset", ["original", "synthetic_sample"])
def test_same_rows_flagged_as_notebook(dataset, request):
    df = request.getfixturevalue(dataset)
    ours = violations(df)
    ours["3"] = ours["3.1"] | ours["3.2"]
    theirs = notebook_masks(df)
    for rule_id, mask in theirs.items():
        a = ours[rule_id].to_numpy()
        b = pd.Series(mask).fillna(False).astype(bool).to_numpy()
        assert (a == b).all(), f"rule {rule_id}: {int((a != b).sum())} differences"


def test_sample_exercises_the_rules(synthetic_sample):
    counts = {k: int(v.sum()) for k, v in violations(synthetic_sample).items()}
    for rule_id in ["1", "2", "3.1", "3.2", "5", "6.3", "6.4"]:
        assert counts[rule_id] > 0, rule_id


def test_notebook_asserts_pass_on_original(original):
    run_checks(original, keep_asserts=True)  # raises AssertionError if a rule fails


def test_notebook_asserts_fail_on_synthetic(synthetic_sample):
    with pytest.raises(AssertionError):
        run_checks(synthetic_sample, keep_asserts=True)
