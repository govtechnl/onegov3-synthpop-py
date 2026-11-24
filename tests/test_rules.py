import math

import pandas as pd
import pytest

from conftest import VALID, records
from rulecheck import COLUMNS, RULES, any_violation, check_rules, violations
from rulecheck import rules as r

NAN = math.nan


def flagged(rule_id: str, *changes: dict) -> list[bool]:
    return violations(records(*changes))[rule_id].tolist()


def test_valid_record_passes_every_rule():
    assert set(VALID) == set(COLUMNS)
    assert not any_violation(records({})).any()


def test_rule_ids_are_unique_and_in_order():
    ids = [rule.id for rule in RULES]
    assert ids == ["1", "2", "3.1", "3.2", "4", "5", "6.1", "6.2", "6.3", "6.4"]


def test_rule_1_birthcity_in_birthcountry():
    assert flagged(
        "1",
        {r.BIRTHCITY_PERP: "Berlin"},  # Berlin is not in the Netherlands
        {r.BIRTHCITY_PERP: "Harlingen", r.BIRTHCOUNTRY_PERP: "Other non-European"},  # listed for both
        {r.BIRTHCOUNTRY_PERP: NAN},  # known city, unknown country
        {r.BIRTHCITY_PERP: NAN},  # unknown city is always allowed
        {r.BIRTHCITY_PERP: NAN, r.BIRTHCOUNTRY_PERP: NAN},
    ) == [True, False, True, False, False]


def test_rule_2_age_difference_is_absolute():
    assert flagged(
        "2",
        {r.AGE_DIFF: 5.0},
        {r.AGE_PERP: 20.0, r.AGE_VICTIM: 30.0, r.AGE_DIFF: 10.0},  # victim older: still 10
        {r.AGE_DIFF: NAN},  # empty difference is allowed
        {r.AGE_PERP: NAN},  # a difference with a missing age is a violation (as in the notebook)
    ) == [True, False, False, True]


def test_rule_3_dates():
    assert flagged(
        "3.1",
        {r.DATE_PREVIOUS: 1_750_000_000.0},
        {r.DATE_PREVIOUS: NAN},
    ) == [True, False]
    assert flagged(
        "3.2",
        {r.DATE_RELEASE: 1_650_000_000.0},
        {r.DATE_RELEASE: 1_700_000_000.0},  # same day is not before
        {r.DATE_RELEASE: NAN},
    ) == [True, False, False]


def test_rule_4_max_sentence():
    assert flagged(
        "4",
        {r.SENTENCE: 10.0},
        {r.SENTENCE: 10.5},
        {r.SOLVED: "Unsolved", r.SENTENCE: 3.0, r.EVIDENCE: NAN},
        {r.SOLVED: "Unsolved", r.SENTENCE: NAN, r.EVIDENCE: NAN},
    ) == [False, True, True, False]


def test_rule_5_minors():
    minor = {r.AGE_PERP: 16.0, r.AGE_VICTIM: 30.0, r.AGE_DIFF: 14.0, r.SENTENCE: 6.0}
    assert flagged(
        "5",
        minor,
        {**minor, r.RELATIONSHIP: "(Step)Parent"},  # exception: older than 12 and family
        {**minor, r.RELATIONSHIP: "Other relative"},
        {**minor, r.AGE_PERP: 12.0, r.AGE_DIFF: 18.0, r.RELATIONSHIP: "(Step)Parent"},  # 12 is not older than 12
        {**minor, r.SENTENCE: 5.0},
        {**minor, r.AGE_PERP: NAN, r.AGE_DIFF: NAN},
    ) == [True, False, False, True, False, False]


def test_rule_6_1_no_evidence_if_unsolved():
    assert flagged(
        "6.1",
        {r.SOLVED: "Unsolved", r.SENTENCE: NAN},
        {r.SOLVED: "Unsolved", r.SENTENCE: NAN, r.EVIDENCE: NAN},
    ) == [True, False]


def test_rule_6_2_bullets_only_with_firearm():
    assert flagged(
        "6.2",
        {r.EVIDENCE: "bullets", r.WEAPON: "Blunt object"},
        {r.EVIDENCE: "ballistics", r.WEAPON: "Firearm"},
        {r.EVIDENCE: "bullets", r.WEAPON: NAN},  # unknown weapon is not a firearm
        {r.EVIDENCE: "DNA", r.WEAPON: "Blunt object"},
    ) == [True, False, True, False]


def test_rule_6_3_no_confession_if_mentally_disturbed():
    assert flagged(
        "6.3",
        {r.EVIDENCE: "confession", r.CONTEXT: r.MENTALLY_DISTURBED},
        {r.EVIDENCE: "DNA", r.CONTEXT: r.MENTALLY_DISTURBED},
    ) == [True, False]


def test_rule_6_4_confession_requires_complete_record():
    assert flagged(
        "6.4",
        {r.EVIDENCE: "confession", r.TIME_OF_DAY: NAN},
        {r.EVIDENCE: "confession", r.DATE_PREVIOUS: NAN, r.DATE_RELEASE: NAN, r.SENTENCE: NAN},  # may be empty
        {r.EVIDENCE: "confession"},
        {r.EVIDENCE: "DNA", r.TIME_OF_DAY: NAN},
    ) == [True, False, False, False]


@pytest.mark.parametrize("column", r.CONFESSION_REQUIRED)
def test_rule_6_4_every_required_column(column):
    df = records({r.EVIDENCE: "confession", column: NAN})
    assert violations(df)["6.4"].iloc[0]


def test_check_rules_report_shape():
    report = check_rules(records({}, {r.AGE_DIFF: 1.0}))
    assert list(report.columns) == ["regel", "omschrijving", "overtredingen", "percentage"]
    row = report.set_index("regel").loc["2"]
    assert row["overtredingen"] == 1
    assert row["percentage"] == 50.0


def test_any_violation_keeps_index():
    df = records({}, {r.AGE_DIFF: 1.0}).set_axis([10, 20])
    result = any_violation(df)
    assert isinstance(result, pd.Series)
    assert result.to_dict() == {10: False, 20: True}
