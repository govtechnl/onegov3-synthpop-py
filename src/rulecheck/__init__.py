"""rulecheck: the business rules of the OneGov #3 synthpop.py challenge as code."""

from .rules import COLUMNS, RULES, Rule, any_violation, check_rules, violations

__all__ = ["COLUMNS", "RULES", "Rule", "any_violation", "check_rules", "violations"]
__version__ = "1.0.0"
