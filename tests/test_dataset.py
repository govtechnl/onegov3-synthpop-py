from rulecheck import COLUMNS, any_violation, check_rules
from rulecheck.rules import ALWAYS_ALLOWED_EVIDENCE, EVIDENCE


def test_shape_and_columns(original):
    assert original.shape == (1291, 22)
    assert list(original.columns) == COLUMNS


def test_original_data_follows_every_rule(original):
    report = check_rules(original)
    assert report["overtredingen"].sum() == 0
    assert not any_violation(original).any()


def test_rule_6_5_values_occur(original):
    assert set(ALWAYS_ALLOWED_EVIDENCE) <= set(original[EVIDENCE].dropna())
